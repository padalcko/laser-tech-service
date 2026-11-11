#!/usr/bin/env python3
"""Normalize existing case HTML to the Pharaon components without rewriting copy.
HTML remains the content source; only main markup is transformed. Standard library.
"""
from html.parser import HTMLParser
from html import escape, unescape
from pathlib import Path
import site_locales
import re, argparse
ROOT = Path(__file__).resolve().parents[1]
VOID = set('area base br col embed hr img input link meta param source track wbr'.split())
class Node:
    def __init__(self, tag='', attrs=(), raw='', parent=None):
        self.tag, self.attrs, self.raw, self.parent = tag, dict(attrs), raw, parent
        self.children=[]; self.end=''; self.dirty=False
    def has(self, cls): return cls in self.attrs.get('class','').split()
    def set(self,key,value): self.attrs[key]=value; self.dirty=True
    def classes(self,*classes): self.set('class',' '.join(classes))
    def all(self, cls=None, tag=None):
        return [n for c in self.children if isinstance(c,Node) for n in [c]+c.all() if (cls is None or n.has(cls)) and (tag is None or n.tag==tag)]
    def text(self): return unescape(re.sub('<[^>]*>','',self.render()))
    def render(self):
        opening=self.raw if not self.dirty else '<'+self.tag+''.join(' '+k+(('="'+escape(v,quote=True)+'"') if v is not None else '') for k,v in self.attrs.items())+'>'
        return opening+''.join(c.render() if isinstance(c,Node) else c for c in self.children)+self.end
    def move(self,parent):
        if self.parent: self.parent.children.remove(self)
        parent.children.append(self); self.parent=parent
class Tree(HTMLParser):
    def __init__(self,s):
        super().__init__(convert_charrefs=False); self.root=Node(); self.current=self.root; self.feed(s)
    def handle_starttag(self,t,a):
        n=Node(t,a,self.get_starttag_text(),self.current); self.current.children.append(n)
        if t not in VOID:self.current=n
    def handle_startendtag(self,t,a): self.handle_starttag(t,a)
    def handle_endtag(self,t):
        n=self.current
        while n.parent and n.tag!=t:n=n.parent
        if n.parent:n.end='</'+t+'>';self.current=n.parent
    def handle_data(self,s):self.current.children.append(s)
    def handle_entityref(self,s):self.handle_data('&'+s+';')
    def handle_charref(self,s):self.handle_data('&#'+s+';')
    def handle_comment(self,s):self.handle_data('<!--'+s+'-->')
def element(tag,cls,parent):
    n=Node(tag,parent=parent);n.classes(cls);n.end='</'+tag+'>';parent.children.append(n);return n

def paths():
    registered = {url for url, (_, _, status) in site_locales.index(site_locales.load()).items() if status == 'published'}
    return sorted(p for folder in ['realizacje','ru/realizacje','en/case-studies'] for p in (ROOT/folder).glob('*/index.html') if '/' + p.parent.relative_to(ROOT).as_posix() + '/' in registered)
RESULT=re.compile(r'^(rezultat|wynik|efekt|podsumowanie|result|outcome|summary|результат|итог)',re.I)
def transform(source,reference):
    match=re.search(r'<main\b.*?</main>',source,re.S);tree=Tree(match.group()); main=tree.root.all(tag='main')[0]
    if main.attrs.get('data-case-layout')=='pharaon':return source
    main.set('data-case-layout','pharaon')
    for n in main.all('case-photo--compact'):
        n.classes(*[c for c in n.attrs['class'].split() if c!='case-photo--compact'])
    # Normalize existing two-column rows to the reference: image first.
    for grid in main.all('case-work-grid'):
        grid.classes('case-work-grid')
        photos=grid.all('case-work-image')
        if photos:
            photo=photos[0]
            if photo.parent is grid:grid.children.remove(photo);grid.children.insert(0,photo)
    # Promote existing result copy; never invent outcomes for cases without it.
    for section in main.all(tag='section'):
        headings=section.all(tag='h2')
        if section.has('case-section') and headings and RESULT.search(headings[0].text().strip()) and not section.all('case-gallery') and not section.all('case-work-grid'):
            section.classes('case-result')
            for n in section.all('case-text'):n.classes('case-result__content')
    # Use each case's own gallery images beside its existing narrative.
    photos=[f for g in main.all('case-gallery') for f in g.all(tag='figure') if f.all(tag='img')]
    candidates=[]
    for section in main.all(tag='section'):
        texts=section.all('case-text')
        if section.has('case-section') and texts and texts[0].all(tag='h2') and not section.all('case-work-grid'):
            content=texts[0]
            if content.all(tag='p') and len(content.text().strip())>60 and not content.all(tag='a'):candidates.append((section,content))
            elif content.all('case-service-list'):candidates.append((section,content))
    # Leave at least one photo with the original gallery heading and captions.
    for (section,content),photo in zip(candidates,photos[:-1]):
        parent=content.parent
        grid=element('div','case-work-grid',parent)
        parent.children.remove(grid);parent.children.insert(parent.children.index(content),grid)
        photo.move(grid);photo.classes('case-work-image')
        content.move(grid);content.classes('case-work-content')
    for i,section in enumerate(s for s in main.all(tag='section') if s.has('case-section')):
        section.classes('case-section',*(['case-section--soft'] if i%2 else []))
    for n in main.all('case-work-image'):
        if n.tag=='figure' and 'style' in n.attrs:
            n.set('style', re.sub(r'(?:aspect-ratio|height)\s*:[^;]+;?', '', n.attrs['style']).strip())
        for img in n.all(tag='img'):img.set('sizes','(max-width: 900px) calc(100vw - 48px), 512px')
    # Retain bespoke CTA wording and forms; supply the localized reference CTA only if absent.
    if not main.all('realizacje-cta') and not main.all('contact-section'):
        cta=Tree(reference).root.all('realizacje-cta')[0];cta.move(main)
    return source[:match.start()]+re.sub(r'[ \t]+(?=\n)', '', tree.root.render())+source[match.end():]

def run():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    refs={lang:(ROOT/folder/'przeglad-serwis-pharaon-1470-wroclaw/index.html').read_text() for lang,folder in [('pl','realizacje'),('ru','ru/realizacje')]}
    en=next(p for p in (ROOT/'en/case-studies').glob('*/index.html') if 'pharaon' in str(p));refs['en']=en.read_text()
    changed=[]
    for p in paths():
        source=p.read_text();lang=re.search(r'<html[^>]*lang="([^"]+)"',source).group(1);updated=transform(source,refs[lang])
        if source!=updated:
            changed.append(str(p.relative_to(ROOT)))
            if not args.check:p.write_text(updated)
    print(f'{len(paths())} case pages scanned; {len(changed)} '+('stale' if args.check else 'updated'))
    if args.check and changed:raise SystemExit(1)
if __name__=='__main__':run()

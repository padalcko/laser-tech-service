#!/usr/bin/env python3
"""Apply the maintenance article's shared author, CTA and compact photo layout.
Existing HTML remains the source of article copy. No runtime JS is required.
"""
from pathlib import Path
import site_locales
import argparse, importlib.util, json, re
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('case_layout',ROOT/'scripts/build-case-layout.py')
markup=importlib.util.module_from_spec(spec);spec.loader.exec_module(markup)
Tree,Node,element=markup.Tree,markup.Node,markup.element
AUTHOR={'@type':'Person','name':'Олександр Падалко','url':'https://raccoon-studio.com.ua/'}
SIGNATURE='<div class="article-signature">Олександр Падалко<br /><a href="https://raccoon-studio.com.ua/" target="_blank" rel="noopener noreferrer">Raccoon Seo Studio</a><br />Wrocław, 2026</div>'
LABELS={
 'pl':('Potrzebujesz serwisu urządzenia?', 'Prześlij model urządzenia, zdjęcia i krótki opis problemu, aby omówić dalszy sposób działania.', 'Skontaktuj się z serwisem','/kontakt/'),
 'ru':('Нужен сервис оборудования?', 'Пришлите модель аппарата, фотографии и краткое описание проблемы, чтобы обсудить дальнейшие действия.', 'Связаться с сервисом','/ru/kontakt/'),
 'en':('Does your equipment need servicing?', 'Send the device model, photos and a short description of the problem to discuss the next steps.', 'Contact the service team','/en/contact/')}
def paths():
 registered = {url for url, (_, _, status) in site_locales.index(site_locales.load()).items() if status == 'published'}
 return sorted(p for d in ['blog','ru/blog','en/blog'] for p in (ROOT/d).glob('*/index.html') if '/' + p.parent.relative_to(ROOT).as_posix() + '/' in registered)
def remove(n):n.parent.children.remove(n)
def add_html(parent,html):
 for child in list(Tree(html).root.children):
  if isinstance(child,Node):child.move(parent)
  else:parent.children.append(child)
def strip_dimensions(node):
 if 'style' in node.attrs:
  node.set('style',re.sub(r'(?:max-width|min-width|width|max-height|min-height|height|aspect-ratio|object-fit|transform|margin-left)\s*:[^;]+;?','',node.attrs['style']).strip())
def transform(source):
 lang=re.search(r'<html[^>]+lang="([^"]+)"',source)[1]
 match=re.search(r'<main\b.*?</main>',source,re.S);tree=Tree(match[0]);main=tree.root.all(tag='main')[0]
 main.classes('article-page'); main.set('data-blog-layout','maintenance')
 articles=main.all(tag='article');assert len(articles)==1
 articles[0].classes('article')
 contents=main.all('article-content');assert len(contents)==1
 content=contents[0]
 for n in list(main.all('article-signature')):remove(n)
 # Remove old bylines from the header, retaining dates and reading estimates.
 names=['laser tech service','padalko','padalcko','падалко','zajcew','зайцев']
 for meta in main.all('article-meta'):
  for n in list(meta.children):
   if isinstance(n,Node) and n.tag!='time' and any(x in n.text().strip().lower() for x in names):remove(n)
 # Preserve existing topical CTA text and destinations; normalize their controls.
 for cta in main.all('article-cta'):
  if not cta.all('article-cta__eyebrow'):
   eyebrow=Tree('<span class="article-cta__eyebrow">Laser Tech Service</span>').root.children[0];eyebrow.parent=cta;cta.children.insert(0,eyebrow)
  actions=cta.all('article-cta__actions')
  if not actions:
   actions=[element('div','article-cta__actions',cta)]
   for link in list(cta.all(tag='a')):
    if link.has('btn') or link.has('article-cta__button') or link.parent is cta:link.move(actions[0])
  action=actions[0]
  links=action.all(tag='a')
  if not any(n.attrs.get('href','').rstrip('/')==LABELS[lang][3].rstrip('/') for n in links):
   add_html(action,f'<a href="{LABELS[lang][3]}">{LABELS[lang][2]}</a>')
  if not any('wa.me/' in n.attrs.get('href','') for n in links):
   add_html(action,'<a href="https://wa.me/48790402597" target="_blank" rel="noopener noreferrer">WhatsApp</a>')
  links=action.all(tag='a')
  primary=next((n for n in links if n.attrs.get('href','').rstrip('/')==LABELS[lang][3].rstrip('/')),links[0])
  action.children.remove(primary);action.children.insert(0,primary)
  for link in links:
   if 'style' in link.attrs:del link.attrs['style'];link.dirty=True
   link.classes('article-cta__button','article-cta__button--primary' if link is primary else 'article-cta__button--secondary')
 # Articles without a CTA get the reference structure with locale-neutral service copy.
 if not main.all('article-cta'):
  title,lead,label,href=LABELS[lang]
  add_html(content,f'<div class="article-cta"><span class="article-cta__eyebrow">Laser Tech Service</span><h2>{title}</h2><p>{lead}</p><div class="article-cta__actions"><a class="article-cta__button article-cta__button--primary" href="{href}">{label}</a><a class="article-cta__button article-cta__button--secondary" href="https://wa.me/48790402597" target="_blank" rel="noopener noreferrer">WhatsApp</a></div></div>')
 # The sole signature is the last article block, matching the reference.
 add_html(content,SIGNATURE)
 for figure in main.all('article-image'):
  if 'data-photo-width' not in figure.attrs:
   cap=re.search(r'max-width:\s*(\d+)px',figure.attrs.get('style',''))
   cap=int(cap[1])/2 if cap else 480
   figure.set('data-photo-width',str(int(cap)))
   heights=[int(h) for im in figure.all(tag='img') for h in re.findall(r'max-height:\s*(\d+)px',im.attrs.get('style',''))]
   figure.set('data-photo-height',str(min(heights)//2 if heights else 480))
  strip_dimensions(figure)
  cap=int(figure.attrs['data-photo-width']);height=int(figure.attrs['data-photo-height'])
  figure.set('style',f'max-width: {cap}px; --article-photo-height: {height}px;')
  for img in figure.all(tag='img'):
   strip_dimensions(img)
   img.set('sizes',f'(max-width: {cap+48}px) calc(100vw - 48px), {cap}px')
 updated=source[:match.start()]+re.sub(r'[ \t]+(?=\n)','',tree.root.render())+source[match.end():]
 author_meta='<meta name="author" content="'+AUTHOR['name']+'" />'
 if re.search(r'<meta\b[^>]*name="author"[^>]*>',updated):updated=re.sub(r'<meta\b[^>]*name="author"[^>]*>',author_meta,updated)
 else:updated=updated.replace('</head>','    '+author_meta+'\n  </head>',1)
 def schema(match):
  data=json.loads(match[1]);changed=False
  nodes=data.get('@graph',[data]) if isinstance(data,dict) else data
  for node in nodes:
   types=node.get('@type',[]);types=[types] if isinstance(types,str) else types
   if any(t in ['Article','BlogPosting','NewsArticle','TechArticle'] for t in types):
    if node.get('author')!=AUTHOR:node['author']=AUTHOR.copy();changed=True
  return '<script type="application/ld+json">'+json.dumps(data,ensure_ascii=False,indent=2)+'</script>' if changed else match[0]
 return re.sub(r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',schema,updated,flags=re.S)
def run():
 parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args();changed=[]
 for path in paths():
  source=path.read_text();updated=transform(source)
  if source!=updated:
   changed.append(str(path.relative_to(ROOT)))
   if not args.check:path.write_text(updated)
 print(f'{len(paths())} blog pages; {len(changed)} '+('stale' if args.check else 'updated'))
 if args.check and changed:raise SystemExit(1)
if __name__=='__main__':run()

#!/usr/bin/env python3
"""Read-only release audit; supplement the existing SEO/AI validators."""
from pathlib import Path
from html.parser import HTMLParser
import collections, importlib.util, json, re, sys
import xml.etree.ElementTree as ET
import tomllib
from urllib.parse import urlsplit
import site_locales

ROOT=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location('ai',ROOT/'scripts/build-ai-search.py');ai=importlib.util.module_from_spec(sp);sp.loader.exec_module(ai)
pages=ai.discover();issues=collections.defaultdict(list);warnings=collections.defaultdict(list)
class Strict(HTMLParser):
    def __init__(self,s):
        super().__init__();self.stack=[];self.errors=[];self.feed(s)
        if self.stack:self.errors.append(('unclosed',self.stack))
    def handle_starttag(self,t,attrs):
        if len(dict(attrs))!=len(attrs):self.errors.append(('duplicate attributes',t))
        if t not in ai.VOID:self.stack.append(t)
    def handle_startendtag(self,t,attrs):pass
    def handle_endtag(self,t):
        if not self.stack or self.stack[-1]!=t:self.errors.append(('nesting',t,self.stack[-3:]))
        elif self.stack:self.stack.pop()
meta=collections.defaultdict(list)
for p in pages:
    route=p['canonical'];tree=p['tree'];main=next(tree.all('main'))
    errors=Strict(p['source']).errors
    if errors:issues['html_structure'].append((route,errors))
    for key in ['description','og:title','og:description','twitter:title','twitter:description']:
        if not p['meta'].get(key):issues['missing_meta'].append((route,key))
    title=next(tree.all('title')).text();meta['title:'+title].append(route);meta['description:'+p['meta']['description']].append(route)
    if len(title)>100:warnings['title_over_100'].append((route,len(title)))
    if len(p['meta']['description'])>250:issues['description_over_250'].append(route)
    last = 0
    for heading in p['tags']:
        if heading.tag not in ['h1','h2','h3','h4','h5','h6']: continue
        parent = heading.parent; footer = False
        while parent:
            footer |= parent.tag == 'footer'; parent = parent.parent
        if footer: continue
        rank = int(heading.tag[1])
        if rank > last + 1: issues['heading_order'].append((route,heading.text()))
        last = rank
    for n in p['tags']:
        if n.tag=='button' and any(x.tag in ['h1','h2','h3','h4','h5','h6','a','button'] for x in n.all() if x is not n):issues['button_content'].append(route)
        if n.tag=='a' and n.attrs.get('target')=='_blank' and not set(n.attrs.get('rel','').split()) & {'noopener','noreferrer'}:issues['external_link_rel'].append(route)
        if n.tag=='img' and 'alt' not in n.attrs:issues['missing_alt'].append(route)
        if n.tag=='script' and 'src' in n.attrs and any(t in n.attrs['src'] for t in ['localhost','127.0.0.1']):issues['test_endpoint'].append(route)
    if p['lang']=='en':
        if 'Equipment service by prior arrangement' in p['source']:issues['removed_section'].append(route)
        nav=next(n for n in p['tags'] if n.attrs.get('id')=='primaryNavigation')
        if '(Polish)' in nav.text():issues['nav_language_suffix'].append(route)
        for n in nav.all('a'):
            if 'LTS Market' in n.text() and n.attrs.get('href')!='https://ltsmarket.pl/en/':issues['market_url'].append(route)
        if re.search(r'[А-Яа-яЁё]',main.text()):warnings['cyrillic_in_english_main'].append(route)
    if not any(n.has('language-switcher__globe') for n in p['tags']):issues['missing_globe'].append(route)
for value,urls in meta.items():
    if len(urls)>1:issues['duplicate_metadata'].append(urls)
for path in ROOT.rglob('*.json'):
    if '.git' not in path.parts:json.loads(path.read_text())
ET.parse(ROOT/'sitemap.xml')
netlify=tomllib.loads((ROOT/'netlify.toml').read_text())
header_rules={rule['for']:rule.get('values',{}) for rule in netlify.get('headers',[])}
for path in ('/docs/*','/scripts/*'):
    assert header_rules.get(path,{}).get('X-Robots-Tag')=='noindex', path
headers=(ROOT/'_headers').read_text()
custom_headers=headers.split('# END GENERATED AI HEADERS',1)[1]
for path in ('/reports/*','/content/*'):
    pattern=rf'(?m)^{re.escape(path)}\s*\n\s+X-Robots-Tag:\s*noindex\s*$'
    assert re.search(pattern,custom_headers), path
for path in (ROOT/'img').rglob('*.svg'):ET.parse(path)
icon_dimensions={}
for name in ('instagram2','facebook2','whatsapp2','telegram2','phone','social',
             'gold-instagram','gold-whatsapp','gold-facebook','gold-telegram'):
    path=ROOT/'img/icons'/f'{name}.svg'
    dimensions=ET.parse(path).getroot().attrib
    icon_dimensions[f'/img/icons/{name}.svg']=(dimensions['width'],dimensions['height'])
for path in ROOT.rglob('*.html'):
    if '.git' in path.parts:continue
    source=path.read_text()
    tree=ai.Parser(source).root
    links=[n for n in tree.all('link')]
    styles={n.attrs.get('href') for n in links if n.attrs.get('rel')=='stylesheet'}
    if '/css/main.css' in styles:
        assert '/css/reset.css' in styles,(path,'missing direct reset stylesheet')
        assert any('fonts.googleapis.com/css2?family=Montserrat' in (href or '') for href in styles),(path,'missing direct Montserrat stylesheet')
        assert any(n.attrs.get('rel')=='preconnect' and n.attrs.get('href')=='https://fonts.googleapis.com' for n in links),(path,'missing Google Fonts preconnect')
        assert any(n.attrs.get('rel')=='preconnect' and n.attrs.get('href')=='https://fonts.gstatic.com' and 'crossorigin' in n.attrs for n in links),(path,'missing Google Fonts CDN preconnect')
    script_urls=[n.attrs.get('src','').lower() for n in tree.all('script')]
    assert not any('jarallax-video' in url for url in script_urls),(path,'unused Jarallax video plugin remains')
    has_parallax=bool(re.search(r'\bdata-jarallax(?:\s|=|>)|\bclass=["\'][^"\']*\bjarallax\b',source,re.I))
    has_jarallax=any('jarallax' in url and 'jarallax-video' not in url for url in script_urls)
    assert has_parallax==has_jarallax,(path,'Jarallax core does not match actual markup use')
    for image in tree.all('img'):
        src=image.attrs.get('src')
        if image.attrs.get('sizes'):
            assert image.attrs.get('srcset'),(path,src,'sizes without srcset')
        if image.attrs.get('srcset'):
            for candidate in image.attrs['srcset'].split(','):
                parts=candidate.strip().split()
                assert len(parts)==2 and re.fullmatch(r'\d+w',parts[1]),(path,src,'invalid srcset candidate',candidate)
                candidate_path=urlsplit(parts[0]).path
                if candidate_path.startswith('/'):
                    assert (ROOT/candidate_path.lstrip('/')).is_file(),(path,src,'missing srcset asset',candidate_path)
        if src in icon_dimensions:
            assert (image.attrs.get('width'),image.attrs.get('height'))==icon_dimensions[src],(path,src)
for page in pages:
    page_type=page['route_group']['type']
    if page_type in ('services','service-detail'):
        assert any(n.tag=='link' and n.attrs.get('rel')=='preload' and
                   n.attrs.get('as')=='image' and
                   n.attrs.get('href')=='/img/urzadzenia-laserowe-w-gabinecie.webp'
                   for n in page['tags']),page['canonical']
    if page_type=='case-study':
        hero=next((n for n in page['tags'] if n.has('case-hero__image')),None)
        image=next(hero.all('img'),None) if hero else None
        assert image and image.attrs.get('fetchpriority')=='high',page['canonical']
error=(ROOT/'404.html').read_text();assert 'noindex' in error and '<h1' in error
assert not re.search(r'(?m)^\s*@import\b',(ROOT/'css/main.css').read_text(),re.I)
assert '/404.html' not in (ROOT/'sitemap.xml').read_text()
registry=site_locales.load();planned=[r['url'] for g in registry['pages'] for r in g['routes'].values() if r['status']=='planned']
assert all('/international-service' in u for u in planned) and len(planned)==3
assert not list(ROOT.rglob('*.pyc')) and not list(ROOT.rglob('__pycache__'))
result={'canonical_pages':len(pages),'languages':dict(collections.Counter(p['lang'] for p in pages)),'planned':planned,'issues':issues,'warnings':warnings}
print(json.dumps(result,ensure_ascii=False,indent=2));sys.exit(bool(issues))

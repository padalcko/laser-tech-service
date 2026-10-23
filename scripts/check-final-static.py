#!/usr/bin/env python3
"""Read-only release audit; supplement the existing SEO/AI validators."""
from pathlib import Path
from html.parser import HTMLParser
import collections, importlib.util, json, re, sys
import xml.etree.ElementTree as ET
import tomllib
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
ET.parse(ROOT/'sitemap.xml');tomllib.loads((ROOT/'netlify.toml').read_text())
for path in (ROOT/'img').rglob('*.svg'):ET.parse(path)
error=(ROOT/'404.html').read_text();assert 'noindex' in error and '<h1' in error
assert '/404.html' not in (ROOT/'sitemap.xml').read_text()
registry=site_locales.load();planned=[r['url'] for g in registry['pages'] for r in g['routes'].values() if r['status']=='planned']
assert all('/international-service' in u for u in planned) and len(planned)==3
assert not list(ROOT.rglob('*.pyc')) and not list(ROOT.rglob('__pycache__'))
result={'canonical_pages':len(pages),'languages':dict(collections.Counter(p['lang'] for p in pages)),'planned':planned,'issues':issues,'warnings':warnings}
print(json.dumps(result,ensure_ascii=False,indent=2));sys.exit(bool(issues))

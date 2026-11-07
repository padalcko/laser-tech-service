#!/usr/bin/env python3
"""Validate approved corporate copy, page structure, links and shared menus."""
import json,re,sys
from pathlib import Path
from html import unescape
from html.parser import HTMLParser
import site_locales as locales
ROOT=locales.ROOT
sys.path.insert(0,str(ROOT/'scripts'))
import importlib.util
spec=importlib.util.spec_from_file_location('about',ROOT/'scripts/build-about.py');about=importlib.util.module_from_spec(spec);spec.loader.exec_module(about)
class Scan(HTMLParser):
 def __init__(self):super().__init__();self.tags=[];self.text=[]
 def handle_starttag(self,tag,attrs):self.tags.append((tag,dict(attrs)))
 def handle_data(self,data):self.text.append(data)
def normalize(s):return ' '.join(unescape(s).split())
for lang,url in about.ROUTES.items():
 p=ROOT/url.lstrip('/')/'index.html';s=p.read_text();main=re.search(r'<main\b.*?</main>',s,re.S)[0];scan=Scan();scan.feed(main);text=normalize(' '.join(scan.text))
 assert len([1 for t,a in scan.tags if t=='section'])==10
 assert len([1 for t,a in scan.tags if t=='h1'])==1
 for section in about.COPY[lang]['sections']:
  for block in section['blocks']:
   if block in ['Subtitle:','Intro:','CTA:','Lead:','Body:','Highlight:','Statement:','Buttons:']:continue
   for line in block.splitlines():
    if line in ['CTA:', 'Buttons:']: continue
    line=re.sub(r'^(?:H[12]: |Eyebrow: |CTA: |Card \d+ — |\d+\. |- )','',line).strip('*').removesuffix(':')
    # List labels and descriptions have a semantic heading boundary instead of an em dash.
    for part in line.split(' — ') if block.startswith(('- ', '1.', '2.', '3.', '4.', '5.')) else [line]:
     assert normalize(part) in text,(lang,part)
 for tag,a in scan.tags:
  if tag=='a' and a.get('href','').startswith('/'):
   dest=a['href'].split('#')[0];target=ROOT/dest.lstrip('/')
   assert target.exists(),(lang,dest)
  if tag=='img':
   assert (ROOT/a['src'].lstrip('/')).exists()
   assert a.get('width') and a.get('height') and a.get('alt') and a.get('srcset')
   assert a.get('loading')=='lazy'
 schemas=[json.loads(x) for x in re.findall(r'<script type="application/ld\+json">(.*?)</script>',s,re.S)]
 assert [x['@type'] for x in schemas]==['AboutPage','BreadcrumbList']
 assert schemas[0]['about']['@id']==locales.load()['base_url']+'/#organization'
 assert 'noindex' not in s
 assert 'Złota Firma' in text
 assert len(re.findall('class="about-person"',main))==3
 assert len(re.findall('class="realizacja-card"',main))==3
 assert '2024' in text
registry=locales.load();count=0
for g in registry['pages']:
 for lang,r in g['routes'].items():
  if r['status']!='published':continue
  s=(ROOT/r['url'].lstrip('/')/'index.html').read_text()
  assert s.count('id="workSubmenu"')==1
  assert s.count('aria-controls="workSubmenu"')==1
  assert f'href="{about.ROUTES[lang]}"' in s
  count+=1
print(f'PASS approved PL/RU/EN copy, ten sections, three portraits/cases, local links/images, AboutPage/BreadcrumbList, and {count} published menus')

#!/usr/bin/env python3
"""Validate the three-language Sapphire case and equipment-age article."""
import importlib.util,json,re
from pathlib import Path
import site_locales as locales
R=Path(__file__).resolve().parents[1];spec=importlib.util.spec_from_file_location('ai',R/'scripts/build-ai-search.py');ai=importlib.util.module_from_spec(spec);spec.loader.exec_module(ai)
reg=locales.load();groups=[g for g in reg['pages'] if g['id'] in ['realizacje:serwis-lasera-sapphire-wymiana-plynu','blog:lasery-dinozaury-wiek-stan-techniczny']];assert len(groups)==2
case=next(g for g in groups if g['type']=='case-study');assert set(case['routes'])=={'pl','ru','en'}
blog=next(g for g in groups if g['type']!='case-study')
pages={p['canonical']:p for p in ai.discover()};audit=json.loads((R/'img/realizacje/sapphire-serwis/image-audit.json').read_text());assert audit['reviewed']==11 and len(audit['selected'])==9 and len(audit['excluded'])==2
files={f['path']:f for p in audit['selected'] for f in p['files']};assert len(files)==27
for path,f in files.items():
 raw=(R/path.lstrip('/')).read_bytes();assert raw[:4]==b'RIFF' and raw[8:12]==b'WEBP';assert len(raw)==f['bytes'];offset=12
 while offset+8<=len(raw):
  assert raw[offset:offset+4] not in (b'EXIF',b'XMP ');size=int.from_bytes(raw[offset+4:offset+8],'little');offset+=8+size+size%2
for g in groups:
 for lang,url in locales.published(g).items():
  p=pages[ai.BASE+url];main=next(p['tree'].all('main'));is_case=g['type']=='case-study';assert p['alternates']==locales.alternates(g,ai.BASE)
  assert set(p['alternates'])=={'pl','ru','en','x-default'}
  assert len(list(main.all('h1')))==1 and '31.05.2018' in main.text()
  assert {'pl':'Legnicy','ru':'Легнице','en':'Legnica'}[lang] in main.text()
  assert not any(old in main.text() for old in ['LightSheer','Wrocław','Вроцлав','ET BP over temperature'])
  if lang=='pl':
   for phrase in ['serwis laserów','naprawa laserów','regeneracja laserów']:assert phrase in main.text().lower()
  schemas=[x for x in p['schemas'] if x.get('@type') in ('Article','BlogPosting')];assert len(schemas)==1 and schemas[0]['headline']==next(main.all('h1')).text()
  assert schemas[0]['datePublished']==schemas[0]['dateModified']=='2026-10-27'
  assert not any(x.get('@type')=='FAQPage' for x in p['schemas'])
  ims=list(main.all('img'));assert len(ims)==(9 if is_case else 4)
  assert len({n.attrs['src'] for n in ims})==len(ims)
  for i,n in enumerate(ims):
   f=files[n.attrs['src']];assert int(n.attrs['width'])==f['width'] and int(n.attrs['height'])==f['height'];assert n.attrs['alt'] and n.attrs['sizes'];assert n.attrs['loading']==('eager' if i==0 else 'lazy')
   for item in n.attrs['srcset'].split(','):
    path,width=item.split();assert files[path]['width']==int(width[:-1])
  hub=url.rsplit('/',2)[0]+'/';cards=[n for n in pages[ai.BASE+hub]['tree'].all('article') if n.has('realizacja-card' if is_case else 'blog-card')];matching=[c for c in cards if any(a.attrs.get('href')==url for a in c.all('a'))];assert len(matching)==1;assert len(list(matching[0].all('img')))==(1 if is_case else 0)
  if not is_case:
   assert len(list(main.all('h2')))>=10
   assert len(re.findall(r'\w+',main.text()))>=650
   assert any(a.attrs.get('href')==case['routes'][lang]['url'] for a in main.all('a'))
  else:
   assert any(a.attrs.get('href')==blog['routes'][lang]['url'] for a in main.all('a'))
   assert schemas[0]['contentLocation']['name']=='Legnica'
  assert 'G-6QFRWP5RX5' in p['source'] and 'AW-17614450660' in p['source']
print('PASS: three localized cases and articles, 27 assets, six cards, SEO, source date, same-language links and analytics')

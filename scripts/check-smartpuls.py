#!/usr/bin/env python3
"""Validate the six smartPULS IPL pages against the approved source copy."""
from pathlib import Path
import json,re,importlib.util
from urllib.parse import urlsplit,unquote
import site_locales
from image_srcset_test_utils import assert_srcset_candidates
R=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('ai',R/'scripts/build-ai-search.py');ai=importlib.util.module_from_spec(spec);spec.loader.exec_module(ai)
texts=json.loads((R/'content/smartpuls-texts.json').read_text());routes=json.loads((R/'content/smartpuls-routes.json').read_text());meta=json.loads((R/'content/smartpuls-meta.json').read_text());audit=json.loads((R/'img/realizacje/smartpuls-swidnica/image-audit.json').read_text());refs=json.loads((R/'content/warsaw-808-routes.json').read_text())
files={f['path']:f for im in audit for f in im['files']};assert len(audit)==3 and len(files)==18
for path,f in files.items():
 raw=(R/path.lstrip('/')).read_bytes();assert raw[:4]==b'RIFF' and raw[8:12]==b'WEBP';assert len(raw)==f['bytes'];offset=12
 while offset+8<=len(raw):
  assert raw[offset:offset+4] not in (b'EXIF',b'XMP ',b'ICCP');size=int.from_bytes(raw[offset+4:offset+8],'little');offset+=8+size+size%2
assert [Path(a['source']).stem for a in audit]==['IMG_8453','IMG_8454','IMG_8455']
pages={p['canonical']:p for p in ai.discover()};norm=lambda s:' '.join(s.split())
for kind,localized in routes.items():
 for lang,url in localized.items():
  p=pages[ai.BASE+url];source=p['source'];main=next(p['tree'].all('main'));t=texts[kind+'-'+lang];expected=[t['h1'],t['reading'],*t['blocks']]
  expected=[v.replace('**','').removeprefix('### ') for v in expected]
  # User requested removing the duplicated contact paragraph from blog CTAs.
  if kind=='blog':expected=[v for v in expected if not v.startswith('Laser Tech Service  \n') ]
  authored=[n.text() for n in main.all() if n.attrs.get('data-authored')=='true'];assert list(map(norm,authored))==list(map(norm,expected)),url
  assert len(list(main.all('h1')))==1
  assert p['alternates']=={**{l:ai.BASE+u for l,u in localized.items()},'x-default':ai.BASE+localized['pl']}
  assert p['meta']['description']==meta[kind+'-'+lang][1]
  assert '<title>'+meta[kind+'-'+lang][0]+'</title>' in source
  for field in ['og:title','og:description','og:image','og:url','twitter:title','twitter:description','twitter:image']:assert p['meta'][field]
  assert p['meta']['og:url']==ai.BASE+url
  assert len(re.findall('property="og:locale:alternate"',source))==2
  reading=list(n for n in main.all() if 'data-reading-time' in n.attrs);assert len(reading)==1;assert reading[0].attrs['data-reading-time']==('2' if kind=='case' else '5')
  assert any(s.get('@type')=='Organization' for s in p['schemas'])
  assert next(p['tree'].all('html')).attrs['lang']==lang
  assert 'noindex' not in p['meta'].get('robots','')
  schemas=[s for s in p['schemas'] if s.get('@type') in ('Article','BlogPosting')];assert len(schemas)==1
  schema=schemas[0];assert schema['headline']==t['h1'];assert schema['datePublished']==schema['dateModified']=='2026-11-06';assert schema['contentLocation']['name']=='Świdnica'
  assert not any(s.get('@type')=='FAQPage' for s in p['schemas']);assert any(s.get('@type')=='BreadcrumbList' for s in p['schemas'])
  if lang=='pl':
   assert not re.search('[\u0400-\u04ff]',main.text())
   for keyword in ['serwis laserów','regeneracja laserów','naprawa laserów']:assert keyword in main.text().lower(),(url,keyword)
  ims=list(main.all('img'));assert len(ims)==(2 if kind=='case' else 3);assert len({n.attrs['src'] for n in ims})==len(ims)
  for i,n in enumerate(ims):
   f=files[n.attrs['src']];assert int(n.attrs['width'])==f['width'] and int(n.attrs['height'])==f['height'];assert n.attrs['sizes'];assert n.attrs['loading']==('eager' if i==0 else 'lazy');assert n.attrs['alt']==next(a['alt'][lang] for a in audit if f in a['files']);assert_srcset_candidates(n.attrs['srcset'],files,R)
  for n in p['tree'].all():
   for attr in ['href','src']:
    value=n.attrs.get(attr,'');parts=urlsplit(value)
    if not value or parts.scheme or value.startswith('#'):continue
    assert (R/unquote(parts.path).lstrip('/')).exists(),(url,value)
  peer=routes['blog' if kind=='case' else 'case'][lang];assert any(n.attrs.get('href')==peer for n in main.all('a'))
  hub=url.rsplit('/',2)[0]+'/';cards=[n for n in pages[ai.BASE+hub]['tree'].all('article') if n.has('realizacja-card' if kind=='case' else 'blog-card')];assert any(a.attrs.get('href')==url for a in cards[0].all('a'));assert sum(any(a.attrs.get('href')==url for a in card.all('a')) for card in cards)==1
  template=(R/refs[kind][lang].lstrip('/')/'index.html').read_text()
  assert re.search(r'<footer class="footer".*?</footer>',source,re.S)[0]==re.search(r'<footer class="footer".*?</footer>',template,re.S)[0]
  clean=lambda s:re.sub(r'<div class="language-switcher".*?</div>','',re.search(r'<nav class="nav".*?</nav>',s,re.S)[0],flags=re.S)
  assert clean(source)==clean(template)
  scripts=lambda s:re.findall(r'<script(?! type="application/ld\+json")[^>]*>.*?</script>',s,re.S)
  assert scripts(source)==scripts(template)
print('PASS: six complete localized texts; 18 metadata-free WebP files; schema, SEO, links, gallery markup, first-position cards and unchanged reference navigation/footer/scripts')

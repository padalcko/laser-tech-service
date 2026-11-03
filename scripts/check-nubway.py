#!/usr/bin/env python3
"""Validate authored NUBWAY copy, six routes, images and unchanged site components."""
from pathlib import Path
import json,re,importlib.util,subprocess,hashlib
from urllib.parse import urlsplit,unquote
import site_locales
R=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('ai',R/'scripts/build-ai-search.py');ai=importlib.util.module_from_spec(spec);spec.loader.exec_module(ai)
texts=json.loads((R/'content/nubway-vacuum-valve-texts.json').read_text());routes=json.loads((R/'content/nubway-vacuum-valve-routes.json').read_text());audit=json.loads((R/'img/realizacje/nubway-vacuum-valve/image-audit.json').read_text());pages={p['canonical']:p for p in ai.discover()};registry=site_locales.load();groups={g['id']:g for g in registry['pages']}
norm=lambda s:' '.join(s.split())
files={f['path']:f for im in audit for f in im['files']};assert len(audit)==12 and len(files)==36
for path,f in files.items():
 raw=(R/path.lstrip('/')).read_bytes();assert raw[:4]==b'RIFF' and raw[8:12]==b'WEBP';assert len(raw)==f['bytes'];offset=12
 while offset+8<=len(raw):
  assert raw[offset:offset+4] not in (b'EXIF',b'XMP ',b'ICCP');size=int.from_bytes(raw[offset+4:offset+8],'little');offset+=8+size+size%2
for kind,localized in routes.items():
 for lang,url in localized.items():
  p=pages[ai.BASE+url];source=p['source'];main=next(p['tree'].all('main'));authored=[n.text() for n in main.all() if n.attrs.get('data-authored')=='true'];expected=[]
  for b in texts[kind+'-'+lang].split('\n\n'):
   if b.startswith('H1:\n'):expected.append(b[4:])
   elif b.startswith(('H2: ','H3: ')):expected.append(b[4:])
   elif b.startswith('- '):expected.extend(line[2:] for line in b.splitlines())
   else:expected.append(b)
  assert list(map(norm,authored))==list(map(norm,expected)),('Authored text mismatch',url)
  assert len(list(main.all('h1')))==1
  assert len(list(main.all('h2')))>=4
  assert p['alternates']=={**{l:ai.BASE+u for l,u in localized.items()},'x-default':ai.BASE+localized['pl']}
  for field in ['description','og:title','og:description','og:image','og:url','twitter:title','twitter:description','twitter:image']:assert p['meta'][field]
  schemas=[s for s in p['schemas'] if s.get('@type') in ('Article','BlogPosting')];assert len(schemas)==1
  schema=schemas[0];assert schema['headline']==authored[0];assert schema['datePublished']==schema['dateModified']=='2026-11-03';assert schema['contentLocation']['name']=='Wrocław'
  assert not any(s.get('@type')=='FAQPage' for s in p['schemas'])
  assert any(s.get('@type')=='BreadcrumbList' for s in p['schemas'])
  ims=list(main.all('img'));assert len(ims)==(12 if kind=='case' else 6);assert len({n.attrs['src'] for n in ims})==len(ims)
  for i,n in enumerate(ims):
   f=files[n.attrs['src']];assert int(n.attrs['width'])==f['width'] and int(n.attrs['height'])==f['height'];assert n.attrs['sizes'];assert n.attrs['loading']==('eager' if kind=='case' and i==0 else 'lazy');assert n.attrs['alt']==next(a['alt'][lang] for a in audit if f in a['files'])
   for item in n.attrs['srcset'].split(','):
    path,width=item.split();assert files[path]['width']==int(width[:-1])
  for n in p['tree'].all():
   for attr in ['href','src']:
    value=n.attrs.get(attr,'');parts=urlsplit(value)
    if not value or parts.scheme or value.startswith('#'):continue
    path=R/unquote(parts.path).lstrip('/');assert path.exists(),(url,value)
  peer=routes['blog' if kind=='case' else 'case'][lang];assert any(n.attrs.get('href')==peer for n in main.all('a'))
  hub=url.rsplit('/',2)[0]+'/';cards=[n for n in pages[ai.BASE+hub]['tree'].all('article') if n.has('realizacja-card' if kind=='case' else 'blog-card')];assert any(a.attrs.get('href')==url for a in cards[0].all('a'));assert sum(any(a.attrs.get('href')==url for a in card.all('a')) for card in cards)==1
  ref=groups['realizacje:przegrzewanie-lasera-diodowego-gliwice-wymiana-filtra' if kind=='case' else 'blog:filtr-wody-laser-diodowy-kiedy-wymieniac']['routes'][lang]['url'];template=(R/ref.lstrip('/')/'index.html').read_text()
  assert re.search(r'<footer class="footer".*?</footer>',source,re.S)[0]==re.search(r'<footer class="footer".*?</footer>',template,re.S)[0]
  clean=lambda s:re.sub(r'<div class="language-switcher".*?</div>','',re.search(r'<nav class="nav".*?</nav>',s,re.S)[0],flags=re.S)
  assert clean(source)==clean(template)
  assert re.findall(r'<script(?! type="application/ld\+json")[^>]*>.*?</script>',source,re.S)==re.findall(r'<script(?! type="application/ld\+json")[^>]*>.*?</script>',template,re.S)
changed=subprocess.check_output(['git','diff','--name-only'],cwd=R,text=True).splitlines();assert not any(p.startswith(('css/','js/')) or p in ['robots.txt','netlify.toml','_redirects','404.html'] for p in changed)
old=groups['realizacje:naprawa-nubway-nbw-vsiii-wroclaw']
for r in old['routes'].values():
 path=r['url'].lstrip('/')+'index.html';assert path not in changed
print('PASS: six verbatim authored texts (paragraph/list order), six localized pages, 36 metadata-free WebP files, SEO/schema, internal links, first-position cards, unchanged old NUBWAY case/header/footer/scripts/global CSS/JS')

#!/usr/bin/env python3
"""Check the Gliwice case/article, source images and shared-component boundaries."""
import importlib.util,json,re,subprocess
from pathlib import Path
from urllib.parse import urlsplit,unquote
import site_locales as locales
R=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('ai',R/'scripts/build-ai-search.py');ai=importlib.util.module_from_spec(spec);spec.loader.exec_module(ai)
reg=locales.load();ids=['realizacje:przegrzewanie-lasera-diodowego-gliwice-wymiana-filtra','blog:filtr-wody-laser-diodowy-kiedy-wymieniac'];groups=[g for g in reg['pages'] if g['id'] in ids];assert len(groups)==2
pages={p['canonical']:p for p in ai.discover()};audit=json.loads((R/'img/realizacje/gliwice-filtr-wody/image-audit.json').read_text());assert len(audit)==3
files={f['path']:f for im in audit for f in im['files']};assert len(files)==9
for path,f in files.items():
 raw=(R/path.lstrip('/')).read_bytes();assert raw[:4]==b'RIFF' and raw[8:12]==b'WEBP';assert len(raw)==f['bytes'];offset=12
 while offset+8<=len(raw):
  assert raw[offset:offset+4] not in (b'EXIF',b'XMP ',b'ICCP');size=int.from_bytes(raw[offset+4:offset+8],'little');offset+=8+size+size%2
for group in groups:
 assert set(group['routes'])=={'pl','ru','en'}
 for lang,url in locales.published(group).items():
  p=pages[ai.BASE+url];main=next(p['tree'].all('main'));source=p['source'];is_case=group['type']=='case-study'
  assert len(list(main.all('h1')))==1 and len(list(main.all('h2')))>=4
  assert p['alternates']==locales.alternates(group,ai.BASE)
  assert ('Gliwice' if lang!='ru' else 'Гливице') in main.text() or lang=='pl' and 'Gliwic' in main.text()
  assert '808' in main.text()
  assert not any(x in main.text() for x in ['Sapphire','LightSheer','Legnica','Wrocław','31.05.2018'])
  if lang=='pl':
   for phrase in ['serwis laserów','regeneracja laserów','naprawa laserów']:assert phrase in main.text().lower()
  schemas=[x for x in p['schemas'] if x.get('@type') in ('Article','BlogPosting')];assert len(schemas)==1;schema=schemas[0]
  assert schema['headline']==next(main.all('h1')).text()
  assert schema['datePublished']==schema['dateModified']=='2026-10-28'
  assert schema['contentLocation']['name']=='Gliwice'
  assert not any(x.get('@type')=='FAQPage' for x in p['schemas'])
  ims=list(main.all('img'));assert len(ims)==3 and len({n.attrs['src'] for n in ims})==3
  for i,n in enumerate(ims):
   f=files[n.attrs['src']];assert int(n.attrs['width'])==f['width'] and int(n.attrs['height'])==f['height'];assert n.attrs['alt'] and n.attrs['sizes'];assert n.attrs['loading']==('eager' if is_case and i==0 else 'lazy')
   for item in n.attrs['srcset'].split(','):
    path,width=item.split();assert files[path]['width']==int(width[:-1])
  for n in p['tree'].all():
   for attr in ['href','src']:
    value=n.attrs.get(attr,'');parts=urlsplit(value)
    if not value or parts.scheme or value.startswith('#'):continue
    path=R/unquote(parts.path).lstrip('/');assert path.exists(),(url,value)
  hub=url.rsplit('/',2)[0]+'/';cards=[n for n in pages[ai.BASE+hub]['tree'].all('article') if n.has('realizacja-card' if is_case else 'blog-card')]
  assert any(a.attrs.get('href')==url for a in cards[0].all('a'))
  assert sum(any(a.attrs.get('href')==url for a in card.all('a')) for card in cards)==1
  assert len(list(cards[0].all('img')))==(1 if is_case else 0)
  peer=next(g for g in groups if g!=group)['routes'][lang]['url'];assert any(a.attrs.get('href')==peer for a in main.all('a'))
  old=next(g for g in reg['pages'] if g['id']==('realizacje:serwis-lasera-sapphire-wymiana-plynu' if is_case else 'blog:lasery-dinozaury-wiek-stan-techniczny'))
  template=(R/old['routes'][lang]['url'].lstrip('/')/'index.html').read_text()
  assert re.search(r'<footer class="footer".*?</footer>',source,re.S)[0]==re.search(r'<footer class="footer".*?</footer>',template,re.S)[0]
  clean=lambda s:re.sub(r'<div class="language-switcher".*?</div>','',re.search(r'<nav class="nav".*?</nav>',s,re.S)[0],flags=re.S)
  assert clean(source)==clean(template)
  assert re.findall(r'<script(?! type="application/ld\+json")[^>]*>.*?</script>',source,re.S)==re.findall(r'<script(?! type="application/ld\+json")[^>]*>.*?</script>',template,re.S)
# Global styling, widget, forms and routing configuration must remain untouched.
changed=subprocess.check_output(['git','diff','--name-only'],cwd=R,text=True).splitlines()
assert not any(p.startswith(('css/','js/')) or p in ['robots.txt','netlify.toml','_redirects','404.html'] for p in changed)
print('PASS: 6 localized pages, 9 metadata-free WebP assets, first cards, same-language links, SEO/schema and unchanged shared components')

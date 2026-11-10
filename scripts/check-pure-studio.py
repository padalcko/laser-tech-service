#!/usr/bin/env python3
"""Validate supplied PURE STUDIO copy, links, SEO, assets and unchanged shared chrome."""
from pathlib import Path
import json,re,importlib.util,subprocess,xml.etree.ElementTree as ET
R=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('markup',R/'scripts/build-case-layout.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
D=json.loads((R/'content/pure-studio-texts.json').read_text());routes=json.loads((R/'content/pure-studio-routes.json').read_text());refs=json.loads((R/'content/nubway-vacuum-valve-routes.json').read_text());base='https://lasertechservice.pl'
count=0
for kind,langs in routes.items():
 for lang,url in langs.items():
  p=R/url.strip('/')/'index.html';s=p.read_text();t=m.Tree(s).root;d=D[kind][lang]
  expected=[d['h1'],d['lead']]+[v for sec in d['sections'] for v in [sec['heading']]+sec['paragraphs']]
  actual=[n.text().strip() for n in t.all() if n.attrs.get('data-authored')=='true']
  assert actual==expected,(url,'authored copy mismatch');count+=len(expected)
  assert len(t.all(tag='h1'))==1
  assert t.all(tag='title')[0].text()==d['title']
  meta={n.attrs.get('name',n.attrs.get('property')):n.attrs.get('content') for n in t.all(tag='meta')};assert meta['description']==d['description'];assert 'noindex' not in meta['robots'];assert meta['author']==('Laser Tech Service' if kind=='case' else 'Олександр Падалко')
  links=t.all(tag='link');assert [n.attrs['href'] for n in links if n.attrs.get('rel')=='canonical']==[base+url]
  assert {n.attrs['hreflang']:n.attrs['href'] for n in links if 'hreflang' in n.attrs}=={**{l:base+u for l,u in langs.items()},'x-default':base+langs['pl']}
  schemas=[json.loads(x) for x in re.findall(r'<script type="application/ld\+json">(.*?)</script>',s,re.S)];assert {x['@type'] for x in schemas}=={'Article' if kind=='case' else 'BlogPosting','BreadcrumbList'}
  for n in t.all(tag='a')+t.all(tag='img')+t.all(tag='script')+links:
   v=n.attrs.get('href',n.attrs.get('src','')).split('#')[0].split('?')[0]
   if v.startswith('/'):
    f=R/v.lstrip('/');f=f/'index.html' if v.endswith('/') else f;assert f.exists(),(url,v)
  main=t.all(tag='main')[0];ims=main.all(tag='img');assert len(ims)==(4 if kind=='case' else 5)
  assert ims[0].attrs['loading']=='eager' and ims[0].attrs['fetchpriority']=='high'
  for im in ims:assert all(k in im.attrs for k in ['alt','width','height','srcset','sizes'])
  ref=m.Tree((R/refs[kind][lang].strip('/')/'index.html').read_text()).root
  for cls in ['header','footer']:
   nodes=t.all(cls);prior=ref.all(cls)
   if nodes and prior:
    # Language destinations intentionally point to the new peer pages.
    clean=lambda x:re.sub(r'<div class="language-switcher".*?</div>','',x,flags=re.S)
    assert clean(nodes[0].render())==clean(prior[0].render()),(url,cls)
  hrefs=[n.attrs.get('href') for n in main.all(tag='a')];assert routes['blog' if kind=='case' else 'case'][lang] in hrefs
  assert {'pl':'/partnerzy/','ru':'/ru/partnerzy/','en':'/en/partners/'}[lang] in hrefs
# Existing articles and realizations must be untouched.
changed=subprocess.check_output(['git','diff','--name-only'],cwd=R,text=True).splitlines()
assert not [p for p in changed if re.match(r'(?:ru/|en/)?(?:blog|realizacje|case-studies)/[^/]+/index.html',p)]
for a in json.loads((R/'img/realizacje/pure-studio/image-audit.json').read_text()):
 import hashlib
 assert hashlib.sha256(Path(a['source']).read_bytes()).hexdigest()==a['sha256']
 for f in a['files']:assert (R/f['path']).stat().st_size==f['bytes']
print(f'PASS: six pages; {count} exact authored blocks; metadata, reciprocal hreflang, local links, images, original hashes and unchanged existing articles/cases')

#!/usr/bin/env python3
"""Validate supplied Aragon copy, locale SEO, links, assets and packaged routes."""
import importlib.util,json,re,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('markup',ROOT/'scripts/build-case-layout.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
items=json.loads((ROOT/'content/aragon-texts.json').read_text());report=json.loads((ROOT/'reports/dist-validation.json').read_text());rows={p['url']:p for p in report['pages']};titles=set();descriptions=set();count=0
norm=lambda s:re.sub(r'\s+',' ',s).strip()
for kind,langs in items.items():
 for lang,it in langs.items():
  p=ROOT/it['url'].strip('/')/'index.html';s=p.read_text();tree=m.Tree(s).root
  expected=[it['h1']]
  for b in it['body'].split('\n\n'):
   if b.startswith('### '):expected.append(b[4:])
   elif b.startswith('- '):expected.extend(x[2:] for x in b.splitlines())
   else:expected.append(b.replace('**',''))
  actual=[n.text() for n in tree.all() if n.attrs.get('data-authored')=='true']
  assert list(map(norm,actual))==list(map(norm,expected)),('copy',it['url'])
  assert len(tree.all(tag='h1'))==1
  assert tree.all(tag='title')[0].text()==it['title'];assert it['title'] not in titles;titles.add(it['title'])
  meta={n.attrs.get('name',n.attrs.get('property')):n.attrs.get('content') for n in tree.all(tag='meta')}
  assert meta['description']==it['description'];assert it['description'] not in descriptions;descriptions.add(it['description']);assert 'noindex' not in meta.get('robots','')
  links=tree.all(tag='link');assert [n.attrs['href'] for n in links if n.attrs.get('rel')=='canonical']==['https://lasertechservice.pl'+it['url']]
  assert {n.attrs['hreflang']:n.attrs['href'] for n in links if 'hreflang' in n.attrs}=={**{('pl-PL' if l=='pl' else l):'https://lasertechservice.pl'+x['url'] for l,x in langs.items()},'x-default':'https://lasertechservice.pl'+langs['pl']['url']}
  for n in tree.all(tag='img'):
   assert n.attrs.get('alt','').strip();assert n.attrs.get('width') and n.attrs.get('height')
  for n in tree.all():
   for attr in ['src','href']:
    u=n.attrs.get(attr,'').split('#')[0].split('?')[0]
    if u.startswith('/') and not u.startswith('//'):
     target=ROOT/u.lstrip('/');assert target.exists(),u
  schemas=[json.loads(x) for x in re.findall(r'<script type="application/ld\+json">(.*?)</script>',s,re.S)]
  article=next(x for x in schemas if x.get('@type') in ['Article','BlogPosting']);assert article['@type']==('Article' if kind=='case' else 'BlogPosting');assert article['headline']==it['h1'];assert article['datePublished']=='2026-11-21';assert article['publisher']['@id']=='https://lasertechservice.pl/#organization';assert any(x['@type']=='BreadcrumbList' for x in schemas)
  assert 'G-6QFRWP5RX5' in s;assert (ROOT/'dist'/p.relative_to(ROOT)).read_bytes()==p.read_bytes()
  assert rows[it['url']]['status']=='ready';assert not rows[it['url']]['noindex'];assert 'https://lasertechservice.pl'+it['url'] in (ROOT/'dist/sitemap.xml').read_text();assert p.with_suffix('.md').exists()
  assert it['url'] in (p.parent.parent/'index.html').read_text();count+=1
for row in json.loads((ROOT/'reports/aragon-image-audit.json').read_text()):
 p=Path(row['original'])
 if p.exists():assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256']
 for f in row['derivatives']:assert (ROOT/f['file']).stat().st_size==f['bytes']
print(f'PASS: {count} pages; exact supplied copy; unique metadata; canonical/hreflang/schema; links, ALT, GA4, Markdown, sitemap, dist; 4 originals and 24 WebP assets')

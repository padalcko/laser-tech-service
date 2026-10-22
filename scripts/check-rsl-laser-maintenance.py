#!/usr/bin/env python3
"""RSL and laser maintenance content audit. Requires Pillow; run from repo root."""
from site_locales import expected_alternates
import json,re,subprocess,collections,xml.etree.ElementTree as ET
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from PIL import Image
R=Path(__file__).resolve().parents[1];BASE='https://lasertechservice.pl';new=['ru/realizacje/naprawa-rsl-masaz-warszawa/index.html','ru/realizacje/przeglad-techniczny-lasera-do-depilacji/index.html','realizacje/naprawa-rsl-masaz-warszawa/index.html','realizacje/przeglad-techniczny-lasera-do-depilacji/index.html','blog/uszkodzony-przewod-manipulatora/index.html','ru/blog/povrezhdennyj-kabel-manipuly/index.html','blog/wymiana-wody-w-laserze-do-depilacji/index.html','ru/blog/zamena-vody-v-lazere-dlya-epilyacii/index.html']
VOID={'area','base','br','col','embed','hr','img','input','link','meta','param','source','track','wbr'}
class P(HTMLParser):
 def __init__(self,t):super().__init__(convert_charrefs=True);self.tags=[];self.ids=[];self.stack=[];self.errors=[];self.feed(t);self.close()
 def handle_starttag(self,tag,attrs):
  d=dict(attrs);self.tags.append((tag,d));
  if len(d)!=len(attrs):self.errors.append(('duplicate attribute',tag))
  if 'id' in d:self.ids.append(d['id'])
  if tag not in VOID:self.stack.append(tag)
 def handle_startendtag(self,tag,attrs):
  self.handle_starttag(tag,attrs)
  if tag not in VOID:self.handle_endtag(tag)
 def handle_endtag(self,tag):
  if not self.stack or self.stack[-1]!=tag:self.errors.append(('nesting',tag,self.stack[-3:]))
  if tag in self.stack:
   while self.stack.pop()!=tag:pass

def resolve(value,source):
 u=urlsplit(value)
 if u.scheme in ('mailto','tel','javascript','data') or u.netloc and u.netloc not in ('lasertechservice.pl','www.lasertechservice.pl'):return None
 q=unquote(u.path)
 target=(R/q.lstrip('/') if q.startswith('/') else source.parent/q) if q else source
 if target.is_dir():target=target/'index.html'
 return target.resolve(),unquote(u.fragment)
parsers={p:P(p.read_text()) for p in R.rglob('*.html')}
refs=0
for p,parser in parsers.items():
 for tag,a in parser.tags:
  values=[a[k] for k in ('href','src','poster') if k in a]
  for v,w in re.findall(r'(\S+) (\d+)w',a.get('srcset','')):
   values.append(v);target=resolve(v,p)
   if target:
    with Image.open(target[0]) as im:assert im.width==int(w),(p,v)
  for v in values:
   target=resolve(v,p)
   if target:
    refs+=1;q,frag=target;assert q.is_file(),(p,v)
    if frag and q in parsers:assert frag in parsers[q].ids,(p,v)
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9','x':'http://www.w3.org/1999/xhtml'}
entries=ET.parse(R/'sitemap.xml').findall('s:url',ns);urls={e.find('s:loc',ns).text:e for e in entries}
assert len(entries)==len(urls)
for rel in new:
 p=R/rel;t=p.read_text();pa=parsers[p];ru=rel.startswith('ru/');lang='ru' if ru else 'pl';case='/realizacje/' in '/'+rel;own=BASE+'/'+rel.removesuffix('index.html')
 assert not pa.errors and not pa.stack,(rel,pa.errors)
 assert len(pa.ids)==len(set(pa.ids))
 assert len(re.findall(r'<h1\b',t))==1
 assert [a['lang'] for tag,a in pa.tags if tag=='html']==[lang]
 assert [a['href'] for tag,a in pa.tags if tag=='link' and a.get('rel')=='canonical']==[own]
 al={a['hreflang']:a['href'] for tag,a in pa.tags if tag=='link' and a.get('hreflang')}
 assert al==expected_alternates(own)
 switch={a.get('hreflang'):BASE+a['href'] for tag,a in pa.tags if tag=='a' and 'language-switcher__link' in a.get('class','')}
 assert switch=={k:v for k,v in al.items() if k != 'x-default'}
 assert {x.get('hreflang'):x.get('href') for x in urls[own].findall('x:link',ns)}==al
 for u in al.values():
  peer=parsers[resolve(u,p)[0]]
  assert {a['hreflang']:a['href'] for tag,a in peer.tags if tag=='link' and a.get('hreflang')}==al
 schemas=[json.loads(x) for x in re.findall(r'<script type="application/ld\+json">(.*?)</script>',t,re.S)]
 assert [x['@type'] for x in schemas]==['Article' if case else 'BlogPosting','BreadcrumbList']
 article,crumb=schemas
 assert article['mainEntityOfPage']['@id']==own and article['datePublished']=='2026-10-09'
 assert article['author']['@id']==article['publisher']['@id']==BASE+'/#organization'
 assert article['inLanguage']==('ru-RU' if ru else 'pl-PL')
 assert crumb['itemListElement'][-1]['item']==own
 meta={a.get('name',a.get('property')):a.get('content') for tag,a in pa.tags if tag=='meta'}
 assert meta['og:title']==meta['twitter:title']==re.search('<title>(.*?)</title>',t,re.S)[1]
 assert meta['description']==meta['og:description']==meta['twitter:description']==article['description']
 assert meta['og:url']==own and meta['og:image']==meta['twitter:image']==article['thumbnailUrl']
 imgs=[a for tag,a in pa.tags if tag=='img' and any('/'+g+'/' in a.get('src','') for g in ['serwis-lasera-do-depilacji','rsl-warszawa'])]
 assert len(imgs)==(5 if 'naprawa-rsl' in rel else 1) if case else len(imgs)==(2 if 'kabel' in rel or 'przewod' in rel else 1)
 for j,a in enumerate(imgs):
  with Image.open(resolve(a['src'],p)[0]) as im:assert (int(a['width']),int(a['height']))==im.size
  assert a['alt'] and a['srcset'] and a['sizes'] and a['decoding']=='async'
  assert a.get('loading')=='lazy' if j else a.get('fetchpriority')=='high'
  assert bool(re.search('[А-Яа-я]',a['alt']))==ru
  assert ('/rsl-warszawa/' in a['src'])==('rsl' in rel or 'przewod' in rel or 'kabel' in rel)
 # Chrome and integrations match existing templates, except language destination URLs.
 template=('ru/' if ru else '')+('realizacje/pilna-naprawa-lasera-co2-poznan/index.html' if case else 'blog/'+('co2-lazer-ne-reagiruet-na-pedal-diagnostika' if ru else 'laser-co2-nie-reaguje-na-pedal-diagnostyka')+'/index.html')
 old=(R/template).read_text()
 for pattern in [r'<footer class="footer">.*?</footer>',r'<div class="menu">.*?</menu>',r'<nav class="nav".*?</nav>']:
  a=re.search(pattern,t,re.S)[0];b=re.search(pattern,old,re.S)[0]
  if 'nav' in pattern:
   a=re.sub(r'href="[^"]+"(?=\s+class="language-switcher)','href="LANG"',a);b=re.sub(r'href="[^"]+"(?=\s+class="language-switcher)','href="LANG"',b)
  assert a==b,(rel,'shared component')
 scripts=lambda x:[s for s in re.findall(r'<script\b.*?</script>',x,re.S) if 'application/ld+json' not in s]
 assert scripts(t)==scripts(old)
 assert re.findall(r'<noscript>.*?</noscript>',t,re.S)==re.findall(r'<noscript>.*?</noscript>',old,re.S)
 main=re.search(r'<main\b.*?</main>',t,re.S)[0]
 if not ru:assert not re.search('[А-Яа-яЁё]',main),rel
for rel in ['blog/index.html','ru/blog/index.html','realizacje/index.html','ru/realizacje/index.html']:
 t=(R/rel).read_text();old=subprocess.check_output(['git','show','HEAD:'+rel],text=True)
 cls='realizacja-card' if '/realizacje/' in '/'+rel else 'blog-card'
 cards=re.findall(r'<article class="'+cls+r'">.*?</article>',t,re.S)
 previous=re.findall(r'<article class="'+cls+r'">.*?</article>',old,re.S)
 assert cards[2:]==previous
 if cls=='blog-card':assert all('<img' not in c for c in cards[:2])
 assert re.sub(r'<article class="'+cls+r'">.*?</article>\s*','',t,count=2,flags=re.S).split('<div class="'+('realizacje-grid' if cls=='realizacja-card' else 'blog-grid')+'">')[0]==old.split('<div class="'+('realizacje-grid' if cls=='realizacja-card' else 'blog-grid')+'">')[0]
assets=[]
for group in ('serwis-lasera-do-depilacji','rsl-warszawa'):
 for p in (R/'img/realizacje'/group).glob('*.webp'):
  with Image.open(p) as im:assert not im.getexif() and not im.info.get('exif') and not im.info.get('xmp');im.load()
  assets.append(p)
assert len(assets)==18
for rel in ['robots.txt','index.html','css/main.css','css/blog.css','css/realizacje.css','js/main.js','_redirects','netlify.toml']:
 p=R/rel
 if p.exists():assert p.read_bytes()==subprocess.check_output(['git','show','HEAD:'+rel]),rel
oldentries=ET.fromstring(subprocess.check_output(['git','show','HEAD:sitemap.xml'],text=True)).findall('s:url',ns)
assert len(entries)==len(oldentries)+8
for e in oldentries:
 other=urls[e.find('s:loc',ns).text];e.tail=other.tail=None;assert ET.tostring(e)==ET.tostring(other)
print(json.dumps({'pages':len(new),'site_html_pages':len(parsers),'local_references':refs,'sitemap_urls':len(entries),'webp_assets':len(assets),'checks':'PASS: structure, links, images, schema, canonical, hreflang, shared components, scripts, indexes, unchanged protected files'},ensure_ascii=False,indent=2))

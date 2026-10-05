#!/usr/bin/env python3
"""Poznan content/image audit against HEAD. Requires Pillow; run from repo root."""
import json,re,subprocess,collections,xml.etree.ElementTree as ET
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from PIL import Image
R=Path(__file__).resolve().parents[1];BASE='https://lasertechservice.pl';new=['realizacje/wymiana-modulu-diodowego-lasera-po-zalaniu-poznan/index.html','ru/realizacje/wymiana-modulu-diodowego-lasera-po-zalaniu-poznan/index.html','blog/dlaczego-nie-warto-samodzielnie-wymieniac-uszczelek-w-laserze/index.html','ru/blog/pochemu-ne-stoit-samostoyatelno-menyat-uplotneniya-v-lazere/index.html']
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
errors=[];refs=0
for p,parser in parsers.items():
 for tag,a in parser.tags:
  values=[]
  for attr in ('href','src','poster'):
   if attr in a:values.append(a[attr])
  if 'srcset' in a:
   for v,w in re.findall(r'(\S+) (\d+)w',a['srcset']):
    values.append(v)
    target=resolve(v,p)
    if target:
     with Image.open(target[0]) as im:assert im.width==int(w),(p,v)
  if tag=='meta' and (a.get('name')=='twitter:image' or a.get('property')=='og:image'):values.append(a.get('content',''))
  for v in values:
   x=resolve(v,p)
   if not x:continue
   target,frag=x;refs+=1
   if not target.is_file():errors.append((str(p.relative_to(R)),v,'missing file'));continue
   if frag and target.suffix=='.html' and target in parsers and frag not in parsers[target].ids:errors.append((str(p.relative_to(R)),v,'missing anchor'))

ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9','x':'http://www.w3.org/1999/xhtml'}
entries=ET.parse(R/'sitemap.xml').findall('s:url',ns)
urls={e.find('s:loc',ns).text:e for e in entries}
assert len(entries)==len(urls)
for u in urls:assert resolve(u,R/'index.html')[0].is_file(),u
oldentries=ET.fromstring(subprocess.check_output(['git','show','HEAD:sitemap.xml'],text=True)).findall('s:url',ns)
assert len(entries)==len(oldentries)+4
for e in oldentries:
 other=urls[e.find('s:loc',ns).text];e.tail=other.tail=None
 assert ET.tostring(e)==ET.tostring(other)
for rel in new:
 p=R/rel;t=p.read_text();parser=parsers[p];ru=rel.startswith('ru/');lang='ru' if ru else 'pl';kind='blog' if '/blog/' in '/'+rel else 'case';own=BASE+'/'+rel.removesuffix('index.html')
 assert not parser.errors and not parser.stack,(rel,parser.errors,parser.stack)
 assert len(parser.ids)==len(set(parser.ids)),rel
 assert len(re.findall(r'<h1\b',t))==1,rel
 assert [d['lang'] for tag,d in parser.tags if tag=='html']==[lang]
 canon=[d['href'] for tag,d in parser.tags if tag=='link' and d.get('rel')=='canonical'];assert canon==[own]
 alternates={d['hreflang']:d['href'] for tag,d in parser.tags if tag=='link' and d.get('rel')=='alternate'}
 assert set(alternates)=={'pl','ru','x-default'} and alternates['x-default']==alternates['pl'] and alternates[lang]==own
 for peerurl in alternates.values():
  peer=parsers[resolve(peerurl,p)[0]]
  assert {d['hreflang']:d['href'] for tag,d in peer.tags if tag=='link' and d.get('rel')=='alternate'}==alternates
 switch={d.get('hreflang'):BASE+d['href'] for tag,d in parser.tags if tag=='a' and 'language-switcher__link' in d.get('class','')}
 assert switch=={k:alternates[k] for k in ['pl','ru']}
 schemas=[json.loads(x) for x in re.findall(r'<script type="application/ld\+json">(.*?)</script>',t,re.S)]
 assert [x['@type'] for x in schemas]==['Article','BreadcrumbList']
 article,crumb=schemas;assert article['mainEntityOfPage']['@id']==own and article['datePublished']=='2026-10-05' and article['dateModified']=='2026-10-05'
 assert article['author']['name']=='Laser Tech Service' and article['inLanguage']==('ru-RU' if ru else 'pl-PL')
 assert crumb['itemListElement'][-1]['item']==own
 for c in crumb['itemListElement'][:-1]:assert 'href="'+c['item'].replace(BASE,'')+'"' in t
 for u in article['image']+[article['thumbnailUrl']]:assert resolve(u,p)[0].is_file()
 meta={d.get('name',d.get('property')):d.get('content') for tag,d in parser.tags if tag=='meta'}
 title=re.search('<title>(.*?)</title>',t,re.S)[1]
 assert meta['og:title']==meta['twitter:title']==title
 assert meta['og:description']==meta['twitter:description']==meta['description']==article['description']
 assert meta['og:url']==own and meta['og:image']==meta['twitter:image']==article['thumbnailUrl']
 for a in [d for tag,d in parser.tags if tag=='img' and '/wymiana-modulu-diodowego-poznan/' in d.get('src','')]:
  im=Image.open(resolve(a['src'],p)[0]);assert (int(a['width']),int(a['height']))==im.size
  assert a['alt'] and a['srcset'] and a['sizes'] and a['decoding']=='async'
  assert bool(re.search('[А-Яа-я]',a['alt']))==ru
 other=[x for x in new if x.startswith('ru/')==ru and ('/blog/' in '/'+x)!=(kind=='blog')][0]
 assert 'href="/'+other.removesuffix('index.html')+'"' in t
 template=('ru/' if ru else '')+('realizacje/serwis-gme-exsys-308/index.html' if kind=='case' else 'blog/laser-tech-service-zlota-firma-2026/index.html')
 old=(R/template).read_text()
 for pattern in [r'<footer class="footer">.*?</footer>',r'<div class="menu">.*?</menu>',r'<nav class="nav".*?</nav>']:
  a=re.search(pattern,t,re.S)[0];b=re.search(pattern,old,re.S)[0]
  if 'nav' in pattern:
   a=re.sub(r'href="[^"]+"(?=\s+class="language-switcher)', 'href="LANG"',a)
   b=re.sub(r'href="[^"]+"(?=\s+class="language-switcher)', 'href="LANG"',b)
  assert a==b,(rel,pattern)
 assert re.findall(r'<script(?![^>]*ld\+json)[^>]*>.*?</script>',t,re.S)==re.findall(r'<script(?![^>]*ld\+json)[^>]*>.*?</script>',old,re.S)
 assert re.findall(r'<link[^>]*rel="stylesheet"[^>]*>',t)==re.findall(r'<link[^>]*rel="stylesheet"[^>]*>',old)
 assert not re.search('GME|ExSys|Złota|Золот|Pharaon|Oleksandr',t),rel
 e=urls[own];assert e.find('s:lastmod',ns).text=='2026-10-05'
 assert {x.get('hreflang'):x.get('href') for x in e.findall('x:link',ns)}==alternates
 idx=('ru/' if ru else '')+('blog/' if kind=='blog' else 'realizacje/')+'index.html';idxtext=(R/idx).read_text()
 cls='blog-card' if kind=='blog' else 'realizacja-card';cards=re.findall(r'<article class="'+cls+r'">.*?</article>',idxtext,re.S)
 assert own.replace(BASE,'') in cards[0] and sum(own.replace(BASE,'') in c for c in cards)==1
 oldindex=subprocess.check_output(['git','show','HEAD:'+idx],text=True)
 assert re.sub(r'\s+',' ',idxtext.replace(cards[0],''))==re.sub(r'\s+',' ',oldindex)
# Global JSON-LD parsing, metadata uniqueness, all new assets referenced.
for p in parsers:
 for raw in re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',p.read_text(),re.S):json.loads(raw)
for rel in new:
 text=(R/rel).read_text();title=re.search('<title>(.*?)</title>',text,re.S)[1]
 assert sum(title in x.read_text() for x in parsers)==1
allhtml=''.join(x.read_text() for x in parsers)
for p in (R/'img/realizacje/wymiana-modulu-diodowego-poznan').iterdir():assert '/'+str(p.relative_to(R)) in allhtml
assert not subprocess.check_output(['git','diff','--name-only','--','css','js','index.html'])
# The site-wide icon repair restores the truncated phone path on the RU homepage.
ru_home=(R/'ru/index.html').read_text()
old_ru_home=subprocess.check_output(['git','show','HEAD:ru/index.html'],text=True)
phone_pattern=r'd="M22 16\.92[^"]+"'
assert re.sub(phone_pattern,'d="PHONE"',ru_home)==re.sub(phone_pattern,'d="PHONE"',old_ru_home)
phone=re.search(phone_pattern,ru_home)[0]
assert phone==re.search(phone_pattern,(R/'index.html').read_text())[0] or ' '.join(phone.split())==' '.join(re.search(phone_pattern,(R/'index.html').read_text())[0].split())
assert not errors,errors
print(json.dumps(dict(html_total=len(parsers),new_pages=len(new),local_references_checked=refs,broken_links=errors,sitemap_urls=len(urls),new_html_nesting='PASS',canonical_hreflang_schema='PASS',shared_chrome='PASS',cards='PASS',images='PASS',sitemap='PASS'),ensure_ascii=False,indent=2))

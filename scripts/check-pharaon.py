#!/usr/bin/env python3
"""Pre-commit Pharaon content/image audit against HEAD. Requires Pillow; run from repo root."""
import json,re,subprocess,collections,xml.etree.ElementTree as ET
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from PIL import Image
R=Path(__file__).resolve().parents[1];BASE='https://lasertechservice.pl';new=['realizacje/przeglad-serwis-pharaon-1470-wroclaw/index.html', 'blog/pharaon-1470-historia-technologia-lasera/index.html', 'ru/realizacje/przeglad-serwis-pharaon-1470-wroclaw/index.html', 'ru/blog/pharaon-1470-istoriya-lazernoy-tehnologii/index.html']
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
for rel in new:
 p=R/rel;t=p.read_text();parser=parsers[p];ru=rel.startswith('ru/');kind='blog' if '/blog/' in '/'+rel else 'case';own=BASE+'/'+rel.removesuffix('index.html')
 assert not parser.errors and not parser.stack,(rel,parser.errors,parser.stack)
 assert not [k for k,n in collections.Counter(parser.ids).items() if n>1],rel
 assert len(re.findall(r'<h1\b',t))==1,rel
 assert [d['lang'] for tag,d in parser.tags if tag=='html']==['ru' if ru else 'pl']
 canon=[d['href'] for tag,d in parser.tags if tag=='link' and d.get('rel')=='canonical'];assert canon==[own],(rel,canon)
 alternates={d['hreflang']:d['href'] for tag,d in parser.tags if tag=='link' and d.get('rel')=='alternate'};assert set(alternates)=={'pl','ru','x-default'};assert alternates['x-default']==alternates['pl'];assert alternates['ru' if ru else 'pl']==own
 for lang,url in alternates.items():
  target=resolve(url,p)[0];peer=parsers[target];peeralt={d['hreflang']:d['href'] for tag,d in peer.tags if tag=='link' and d.get('rel')=='alternate'};assert peeralt==alternates
 switch={d.get('hreflang'):BASE+d['href'] for tag,d in parser.tags if tag=='a' and 'language-switcher__link' in d.get('class','')};assert switch=={k:alternates[k] for k in ['pl','ru']}
 schemas=[json.loads(s) for s in re.findall(r'<script type="application/ld\+json">(.*?)</script>',t,re.S)];assert [s['@type'] for s in schemas]==['Article','BreadcrumbList']
 article,crumb=schemas;assert article['mainEntityOfPage']['@id']==own;assert article['datePublished']=='2026-09-30';assert article['dateModified']=='2026-09-30';assert crumb['itemListElement'][-1]['item']==own
 if kind=='blog':assert article['author']['name']=='Oleksandr Padalko' and 'article-signature">Oleksandr Padalko' in t
 assert '3000 NAIN' not in t and '3000-nain' not in t
 for tag,d in parser.tags:
  if tag=='img' and d.get('src','').endswith('.webp'):
   with Image.open(resolve(d['src'],p)[0]) as im:assert (int(d['width']),int(d['height']))==im.size
 # Header, footer, social menu and scripts match the current language/category template.
 tpl=(('ru/' if ru else '')+'realizacje/naprawa-3000-nain-bloku-zasilania/index.html' if kind=='case' else ('ru/blog/3000-nain-lazer-istoriya-konstrukciya-servis/index.html' if ru else 'blog/3000-nain-laser-historia-konstrukcja-serwis/index.html'))
 template=(R/tpl).read_text()
 for start,end in [('<footer class="footer">','</footer>'),('<div class="menu">','</menu>')]:assert t[t.index(start):t.index(end,t.index(start))+len(end)]==template[template.index(start):template.index(end,template.index(start))+len(end)]
 nav=re.search(r'<nav class="nav".*?</nav>',t,re.S)[0];oldnav=re.search(r'<nav class="nav".*?</nav>',template,re.S)[0]
 for v in alternates.values():nav=nav.replace(urlsplit(v).path,'PAGE')
 for u in re.findall(r'href="([^"]+)"\s+class="language-switcher__link',oldnav):oldnav=oldnav.replace(u,'PAGE')
 assert nav==oldnav,(rel,'nav mismatch')
 for category in ['css','js']:
  oldlinks=[d.get('href',d.get('src')) for tag,d in P(template).tags if (tag=='link' and d.get('rel')=='stylesheet') or (tag=='script' and 'src' in d)]
  links=[d.get('href',d.get('src')) for tag,d in parser.tags if (tag=='link' and d.get('rel')=='stylesheet') or (tag=='script' and 'src' in d)]
  assert links==oldlinks
# Sitemap contains exact reciprocal metadata for all new pages; all targets exist.
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9','x':'http://www.w3.org/1999/xhtml'};tree=ET.parse('sitemap.xml');urls={}
for e in tree.findall('s:url',ns):
 url=e.find('s:loc',ns).text;assert url not in urls;urls[url]=e;assert resolve(url,R/'index.html')[0].exists(),url
for rel in new:
 url=BASE+'/'+rel.removesuffix('index.html');e=urls[url];assert e.find('s:lastmod',ns).text=='2026-09-30'
 assert {x.attrib['hreflang']:x.attrib['href'] for x in e.findall('x:link',ns)}=={d['hreflang']:d['href'] for tag,d in parsers[R/rel].tags if tag=='link' and d.get('rel')=='alternate'}
# Check newly added URLs have exactly one matching card, and unchanged old content remains.
for rel in new:
 url='/'+rel.removesuffix('index.html');kind='blog' if '/blog/' in url else 'realizacje';index=R/('ru/' if rel.startswith('ru/') else '')/kind/'index.html';text=index.read_text();cards=re.findall(r'<article class="'+('blog-card' if kind=='blog' else 'realizacja-card')+r'">.*?</article>',text,re.S);assert sum(url in c for c in cards)==1;assert url in cards[0]
 assert len(cards)==len(re.findall(r'<article class="'+('blog-card' if kind=='blog' else 'realizacja-card')+r'">',subprocess.check_output(['git','show','HEAD:'+str(index.relative_to(R))],text=True)))+1
assert not subprocess.check_output(['git','diff','--name-only','--','js'])
print(json.dumps({'html_total':len(parsers),'new_pages':len(new),'local_references_checked':refs,'broken_links':errors,'sitemap_urls':len(urls),'new_html_nesting':'PASS','new_ids':'PASS','canonical_hreflang_schema':'PASS','shared_chrome':'PASS','cards':'PASS'},ensure_ascii=False,indent=2))

assert not errors

import hashlib
parsers={p:P(p.read_text()) for p in R.rglob('*.html')};issues=collections.defaultdict(list);titles=collections.defaultdict(list);descs=collections.defaultdict(list);imgcount=0;sets=0;highs=0;lazy=0;schemas=0
renames={'img/alex.webp': 'img/laser-aleksandrytowy.webp', 'img/cryo.webp': 'img/urzadzenie-cryo-vacuum.webp', 'img/diod.webp': 'img/laser-diodowy-do-depilacji.webp', 'img/ir.webp': 'img/masazer-rolkowo-prozniowy-ir.webp', 'img/massage.webp': 'img/urzadzenie-do-masazu.webp', 'img/map.webp': 'img/mapa-zasiegu-serwisu-polska.webp', 'img/laser.webp': 'img/budowa-glowicy-lasera-diodowego.webp', 'img/laser-600w.webp': 'img/budowa-glowicy-lasera-diodowego-600w.webp', 'img/inst.webp': 'img/profil-instagram-laser-tech-service.webp', 'img/instscreen.webp': 'img/profil-instagram-laser-tech-service-zblizenie.webp', 'img/manipul.webp': 'img/rozebrana-manipula-na-stole-serwisowym.webp', 'img/sprzet.webp': 'img/wnetrze-urzadzenia-laserowego.webp', 'img/welcome.webp': 'img/urzadzenia-laserowe-w-gabinecie.webp', 'img/przed.webp': 'img/zabrudzona-chlodnica-przed-czyszczeniem.webp', 'img/po.webp': 'img/chlodnica-po-czyszczeniu.webp', 'img/przed1.webp': 'img/modul-diodowy-przed-naprawa.webp', 'img/po1.webp': 'img/modul-diodowy-po-naprawie.webp', 'img/przed2.webp': 'img/wyswietlacz-miernika-przed-serwisem.webp', 'img/po2.webp': 'img/wyswietlacz-miernika-po-serwisie.webp', 'img/realizacje/beauty-planet-3d-contour-wroclaw/beauty-planet-3d-contour-manipula-vacuum-rf.webp': 'img/realizacje/beauty-planet-3d-contour-wroclaw/beauty-planet-3d-contour-panel-vacuum-rf.webp', 'img/Group76.svg': 'img/rysunek-glowicy-lasera-diodowego.svg', 'img/pngegg 1.svg': 'img/mapa-wojewodztw-polski.svg'}
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9','x':'http://www.w3.org/1999/xhtml'}
entries={e.find('s:loc',ns).text:e for e in ET.parse('sitemap.xml').findall('s:url',ns)}
for p,parser in parsers.items():
 rel=str(p.relative_to(R));t=p.read_text();tags=parser.tags;own=BASE+'/'+rel.removesuffix('index.html');ru=rel.startswith('ru/')
 titles[re.sub(r'\s+',' ',re.search(r'<title>(.*?)</title>',t,re.S)[1]).strip()].append(rel)
 metas={a.get('name',a.get('property')):a.get('content') for tag,a in tags if tag=='meta'};descs[metas.get('description')].append(rel)
 canon=[a.get('href') for tag,a in tags if tag=='link' and a.get('rel')=='canonical'];alt={a.get('hreflang'):a.get('href') for tag,a in tags if tag=='link' and a.get('rel')=='alternate'}
 if rel!='404.html':
  if canon!=[own]:issues['canonical'].append((rel,canon))
  if own not in entries:issues['sitemap_missing'].append(rel)
  if alt.get('ru' if ru else 'pl')!=own or alt.get('x-default')!=alt.get('pl'):issues['hreflang'].append((rel,alt))
  for lang,url in alt.items():
   peer=resolve(url,p)[0]
   pa={a.get('hreflang'):a.get('href') for tag,a in parsers[peer].tags if tag=='link' and a.get('rel')=='alternate'}
   if pa!=alt:issues['hreflang_reciprocity'].append((rel,url,pa))
  ea={e.get('hreflang'):e.get('href') for e in entries[own].findall('x:link',ns)}
  if ea!=alt:issues['sitemap_hreflang'].append((rel,ea,alt))
 high=0
 for tag,a in tags:
  if a.get('fetchpriority')=='high':high+=1
  if tag=='img':
   imgcount+=1
   if 'alt' not in a:issues['missing_alt'].append(rel)
   if a.get('alt','').lower() in ['image','photo','laser','zdjęcie']:issues['generic_alt'].append((rel,a))
   if ru and a.get('src','').endswith('.webp') and not re.search('[А-Яа-яЁё]',a.get('alt','')):issues['alt_language'].append((rel,a.get('alt')))
   if a.get('loading')=='lazy':lazy+=1
   if a.get('loading')=='lazy' and a.get('fetchpriority')=='high':issues['lazy_high'].append(rel)
   target=resolve(a.get('src',''),p)
   if target and target[0].suffix.lower() not in ['.svg']:
    with Image.open(target[0]) as im:
     w=int(a.get('width',0));h=int(a.get('height',0))
     if not w or not h or abs(w/h-im.width/im.height)>0.001:issues['dimensions'].append((rel,a.get('src'),w,h,im.size))
  if 'srcset' in a:
   sets+=1;seen=[]
   for candidate in a['srcset'].split(','):
    match=re.fullmatch(r'\s*(\S+)\s+(\d+)w\s*',candidate)
    if not match:issues['srcset'].append((rel,candidate));continue
    u,w=match.groups();seen.append(int(w));target=resolve(u,p)[0]
    if not target.exists():issues['srcset'].append((rel,u))
    else:
     with Image.open(target) as im:
      if im.width!=int(w):issues['srcset'].append((rel,u,w,im.width))
   if seen!=sorted(set(seen)) or not a.get('sizes'):issues['srcset'].append((rel,'order/sizes'))
 if high>1:issues['multiple_high'].append(rel)
 highs+=high
 for s in re.findall(r'<script type="application/ld\+json">(.*?)</script>',t,re.S):
  schemas+=1
  try:json.loads(s)
  except Exception as e:issues['schema'].append((rel,str(e)))
for key,values in [('duplicate_titles',titles),('duplicate_descriptions',descs)]:
 for v,paths in values.items():
  if len(paths)>1:issues[key].append(paths)
# Compare every existing file against HEAD: only allowed image changes and new cards/sitemap.
changed=subprocess.check_output(['git','diff','--name-only','--diff-filter=M'],text=True).splitlines()
for rel in changed:
 p=R/rel;old=subprocess.check_output(['git','show','HEAD:'+rel],text=True);now=p.read_text();mapped=old
 for a,b in renames.items():mapped=mapped.replace(a,b)
 if p.suffix=='.html':
  def normalize(s):
   s=re.sub(r'\balt="[^"]*"','alt="ALT"',s)
   s=re.sub(r'<article class="(?:realizacja-card|blog-card)">(?:(?!</article>).)*pharaon-1470.*?</article>','',s,flags=re.S) if False else s
   return s
  # Remove only the four new cards for equality check.
  for css in ['realizacja-card','blog-card']:
   now=re.sub(r'<article class="'+css+r'">.*?</article>',lambda m:'' if 'pharaon-1470' in m[0] else m[0],now,flags=re.S)
  if re.sub(r'\s+',' ',normalize(now)).strip()!=re.sub(r'\s+',' ',normalize(mapped)).strip():issues['scope'].append(rel)
 elif rel not in ['sitemap.xml', 'scripts/audit-images.py'] and now!=mapped:issues['scope'].append(rel)
# Moves retain byte-for-byte originals, even SVGs.
for a,b in renames.items():
 raw=subprocess.check_output(['git','show','HEAD:'+a]);assert (R/b).read_bytes()==raw,b
for p in R.rglob('*'):
 if not p.is_file() or any(x.startswith('.') for x in p.relative_to(R).parts) or p.suffix not in {'.html','.css','.js','.json','.xml','.webmanifest'} and p.name!='_redirects':continue
 try:t=p.read_text()
 except UnicodeError:continue
 for a in renames:
  if a in t:issues['old_reference'].append((str(p),a))
print(json.dumps({'html':len(parsers),'images_checked':imgcount,'srcset_sets':sets,'lazy_images':lazy,'high_priority_resources':highs,'json_ld_blocks':schemas,'sitemap_urls':len(entries),'issues':dict(issues)},ensure_ascii=False,indent=2))
assert not issues, dict(issues)

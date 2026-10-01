#!/usr/bin/env python3
"""Pre-commit GME audit against HEAD; run from repo root with Pillow installed."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
from PIL import Image
import re,json,collections,xml.etree.ElementTree as ET,subprocess
R=Path(__file__).resolve().parents[1];B='https://lasertechservice.pl';slug='serwis-gme-exsys-308';issues=collections.defaultdict(list);counts=collections.Counter()
class Parser(HTMLParser):
 def __init__(self,s):super().__init__(convert_charrefs=True);self.tags=[];self.ids=[];self.feed(s)
 def handle_starttag(self,t,attrs):
  a=dict(attrs);self.tags.append((t,a))
  if 'id' in a:self.ids.append(a['id'])
def resolve(u,p):
 s=urlsplit(u)
 if s.scheme in ('mailto','tel','data','javascript') or s.netloc and s.netloc not in ['lasertechservice.pl','www.lasertechservice.pl']:return
 path=unquote(s.path);q=(R/path.lstrip('/') if path.startswith('/') else p.parent/path) if path else p
 if q.is_dir():q=q/'index.html'
 return q.resolve(),unquote(s.fragment)
parsers={p:Parser(p.read_text()) for p in R.rglob('*.html')};ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9','x':'http://www.w3.org/1999/xhtml'}
entries=ET.parse('sitemap.xml').findall('s:url',ns);sitemap={};titles=collections.defaultdict(list);descs=collections.defaultdict(list)
for e in entries:
 u=e.find('s:loc',ns).text
 if u in sitemap:issues['sitemap'].append(('duplicate',u))
 sitemap[u]=e
 q=resolve(u,R/'index.html')
 if not q or not q[0].exists():issues['sitemap'].append(('missing',u))
redirects={line.split()[0]:line.split()[1] for line in Path('_redirects').read_text().splitlines() if line.strip() and not line.startswith('#') and len(line.split())>=2}
def check(u,p):
 q=resolve(u,p)
 if not q:return
 counts['local_references']+=1
 target,frag=q
 if not target.is_file():issues['broken_links'].append((str(p.relative_to(R)),u))
 elif frag and target in parsers and frag not in parsers[target].ids:issues['broken_links'].append((str(p.relative_to(R)),u,'fragment'))
 if urlsplit(u).path in redirects:issues['redirect_references'].append((str(p.relative_to(R)),u))
for p,parser in parsers.items():
 rel=str(p.relative_to(R));text=p.read_text();tags=parser.tags;own=B+'/'+rel.removesuffix('index.html');counts['html']+=1
 mt=re.search('<title>(.*?)</title>',text,re.S);title=mt[1].strip() if mt else '';titles[title].append(rel)
 meta={a.get('name',a.get('property')):a.get('content') for t,a in tags if t=='meta'};descs[meta.get('description','')].append(rel)
 if not title:issues['missing_title'].append(rel)
 if not meta.get('description'):issues['missing_description'].append(rel)
 alternates={a.get('hreflang'):a.get('href') for t,a in tags if t=='link' and a.get('rel')=='alternate'}
 if rel!='404.html':
  if [a.get('href') for t,a in tags if t=='link' and a.get('rel')=='canonical']!=[own]:issues['canonical'].append(rel)
  if alternates.get('ru' if rel.startswith('ru/') else 'pl')!=own or alternates.get('x-default')!=alternates.get('pl'):issues['hreflang'].append(rel)
  for lang,u in alternates.items():
   q=resolve(u,p)
   if not q or q[0] not in parsers:issues['hreflang'].append((rel,u));continue
   peer={a.get('hreflang'):a.get('href') for t,a in parsers[q[0]].tags if t=='link' and a.get('rel')=='alternate'}
   if peer!=alternates:issues['hreflang'].append((rel,'reciprocity'))
  if own not in sitemap:issues['sitemap'].append(('missing',own))
  else:
   al={e.get('hreflang'):e.get('href') for e in sitemap[own].findall('x:link',ns)}
   if al!=alternates:issues['sitemap'].append((rel,'alternates'))
 for t,a in tags:
  for attr in ['href','src','poster']:
   if a.get(attr):check(a[attr],p)
  if t=='img':
   counts['img']+=1
   if 'alt' not in a:issues['missing_alt'].append(rel)
   q=resolve(a.get('src',''),p)
   if q and q[0].is_file() and q[0].suffix.lower()!='.svg':
    with Image.open(q[0]) as im:
     try:w,h=int(a.get('width',0)),int(a.get('height',0));assert w and h and abs(w/h-im.width/im.height)<.001
     except (ValueError,AssertionError):issues['dimensions'].append((rel,a.get('src')))
   if slug in rel:
    if not a.get('alt'):issues['new_empty_alt'].append((rel,a.get('src')))
    if '/gme-exsys-308/' in a.get('src',''):
     if not a.get('decoding') or not a.get('srcset') or not a.get('sizes'):issues['new_images'].append(rel)
     if rel.startswith('ru/') and not re.search('[А-Яа-я]',a['alt']):issues['new_alt_language'].append(rel)
  if a.get('srcset'):
   counts['srcset']+=1;seen=[]
   for c in a['srcset'].split(','):
    m=re.fullmatch(r'\s*(\S+)\s+(\d+)w\s*',c)
    if not m:issues['srcset'].append((rel,c));continue
    u,w=m.groups();check(u,p);q=resolve(u,p);seen.append(int(w))
    if q and q[0].is_file():
     with Image.open(q[0]) as im:
      if im.width!=int(w):issues['srcset'].append((rel,u))
   if sorted(set(seen))!=seen or not a.get('sizes'):issues['srcset'].append((rel,'sizes/order'))
 for k in ['og:image','twitter:image']:
  if meta.get(k):check(meta[k],p)
 def walk(v):
  if isinstance(v,dict):
   for k,x in v.items():walk(x)
  elif isinstance(v,list):
   for x in v:walk(x)
  elif isinstance(v,str) and v.startswith(B+'/'):check(v,p)
 for raw in re.findall(r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',text,re.S):
  counts['json_ld']+=1
  try:walk(json.loads(raw))
  except ValueError:issues['json_ld'].append(rel)
 if slug in rel:
  lang='ru' if rel.startswith('ru/') else 'pl'
  assert text.count('<h1 ')==1 and '4xF6oegzCUQ' not in text
  assert 'pharaon' not in text.lower() and 'Denica' not in text
  schemas=[json.loads(x) for x in re.findall(r'<script type="application/ld\+json">(.*?)</script>',text,re.S)]
  assert [x['@type'] for x in schemas]==['Article','BreadcrumbList','VideoObject']
  a,c,v=schemas;assert a['headline'] in text and a['description']==meta['description'];assert c['itemListElement'][-1]['item']==own
  assert v['embedUrl']=='https://www.youtube.com/embed/ytdL7NfbsFc' and v['duration']=='PT43S' and v['uploadDate']=='2026-10-01T05:50:25-07:00'
  iframes=[a for t,a in tags if t=='iframe' and 'youtube' in a.get('src','')];assert len(iframes)==1 and iframes[0]['title'] and iframes[0]['loading']=='lazy'
  assert meta['og:title']==meta['twitter:title']==title and meta['og:description']==meta['twitter:description']==meta['description'] and meta['og:url']==own
  assert len(parser.ids)==len(set(parser.ids))
  assert {a['hreflang']:B+a['href'] for t,a in tags if t=='a' and 'language-switcher__link' in a.get('class','')}=={k:alternates[k] for k in ['pl','ru']}
  template=R/('ru/' if lang=='ru' else '')/'realizacje/przeglad-serwis-pharaon-1470-wroclaw/index.html';old=template.read_text()
  for pattern in [r'<footer class="footer">.*?</footer>',r'<nav class="nav".*?</nav>',r'<div class="menu">.*?</menu>']:
   x=re.search(pattern,text,re.S)[0];y=re.search(pattern,old,re.S)[0].replace('przeglad-serwis-pharaon-1470-wroclaw',slug);assert x==y,(rel,pattern)
  oldscripts=re.findall(r'<script(?![^>]*ld\+json)[^>]*>.*?</script>',old,re.S);scripts=re.findall(r'<script(?![^>]*ld\+json)[^>]*>.*?</script>',text,re.S);assert scripts==oldscripts
for name,values in [('duplicate_title',titles),('duplicate_description',descs)]:
 for value,paths in values.items():
  if len(paths)>1:issues[name].append(paths)
for lang in ['pl','ru']:
 rel=('ru/' if lang=='ru' else '')+'realizacje/index.html';now=(R/rel).read_text();old=subprocess.check_output(['git','show','HEAD:'+rel],text=True)
 cards=re.findall(r'<article class="realizacja-card">.*?</article>',now,re.S);assert slug in cards[0] and sum(slug in c for c in cards)==1
 assert re.sub(r'\s+',' ',now.replace(cards[0],''))==re.sub(r'\s+',' ',old)
oldtree=ET.fromstring(subprocess.check_output(['git','show','HEAD:sitemap.xml'],text=True));oldentries=oldtree.findall('s:url',ns)
assert len(entries)==len(oldentries)+2
for e in oldentries:
 other=sitemap[e.find('s:loc',ns).text];e.tail=other.tail=None
 assert ET.tostring(e)==ET.tostring(other)
manifest=json.loads(Path('site.webmanifest').read_text())
for icon in manifest['icons']:check(icon['src'],R/'index.html')
counts['sitemap_urls']=len(sitemap)
result={'counts':dict(counts),'issues':dict(issues)};print(json.dumps(result,ensure_ascii=False,indent=2));assert not issues

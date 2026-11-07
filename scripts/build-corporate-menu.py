#!/usr/bin/env python3
"""Move Blog under the existing Work link; insert About between Partners and Contact."""
import argparse,json,re
from html import escape
import site_locales as locales
LABELS={'pl':('O nas','Podmenu realizacji'),'ru':('О нас','Подменю реализаций'),'en':('About Us','Our Work submenu')}
def balanced(source,start,tag):
 depth=0
 for m in re.finditer(r'</?'+tag+r'\b[^>]*>',source[start:]):
  depth+=-1 if m[0].startswith('</') else 1
  if depth==0:return start+m.end()
 raise ValueError(tag)
def update(source,lang,url,groups):
 start=re.search(r'<ul\b[^>]*id="primaryNavigation"[^>]*>',source).start();end=balanced(source,start,'ul')
 block=source[start:end];opening=block[:block.index('>')+1];inside=block[len(opening):-5]
 items=[];pos=0
 while m:=re.search(r'<li\b',inside[pos:]):
  a=pos+m.start();b=balanced(inside,a,'li');items.append(inside[a:b]);pos=b
 routes={key:groups[key]['routes'][lang]['url'] for key in ['blog','realizacje','partnerzy','kontakt','about']}
 def matches(item,key):return f'href="{routes[key]}"' in item
 work=next(item for item in items if matches(item,'realizacje'))
 worklink=re.search(r'<a\b[^>]*href="'+re.escape(routes['realizacje'])+r'"[^>]*>.*?</a>',work,re.S)[0]
 blogitem=next((item for item in items if matches(item,'blog') and not matches(item,'realizacje')),None)
 bloglink=re.search(r'<a\b[^>]*href="'+re.escape(routes['blog'])+r'"[^>]*>(.*?)</a>',blogitem or work,re.S)
 assert bloglink
 active=' aria-current="page"' if url==routes['blog'] else ''
 worknew=f'<li class="nav-list__item nav-services nav-work"><div class="nav-services__row">{worklink}<button class="nav-submenu-toggle" type="button" aria-label="{LABELS[lang][1]}" aria-expanded="false" aria-controls="workSubmenu" hidden><span aria-hidden="true">▾</span></button></div><ul class="nav-submenu" id="workSubmenu" hidden><li><a href="{routes["blog"]}"{active}>{bloglink[1].strip()}</a></li></ul></li>'
 active=' nav-list__link--active" aria-current="page"' if url==routes['about'] else '"'
 about=f'<li class="nav-list__item"><a href="{routes["about"]}" class="nav-list__link{active}>{LABELS[lang][0]}</a></li>'
 output=[]
 for item in items:
  if matches(item,'realizacje'):output.append(worknew)
  elif matches(item,'blog') or matches(item,'about'):continue
  else:
   if matches(item,'kontakt'):output.append(about)
   output.append(item)
 updated=source[:start]+opening+'\n            '+'\n            '.join(output)+'\n          </ul>'+source[end:]
 if url=='/404.html':
  m=re.search(r'(<script id="error-locales" type="application/json">)(.*?)(</script>)',updated,re.S)
  data=json.loads(m[2])
  for l in LABELS:
   data['text'][l]['O nas']=LABELS[l][0];data['text'][l]['Podmenu realizacji']=LABELS[l][1]
   data['routes'][l][routes['about']]=groups['about']['routes'][l]['url']
  updated=updated[:m.start()]+m[1]+'\n'+json.dumps(data,ensure_ascii=False,indent=2)+'\n    '+m[3]+updated[m.end():]
 return updated

def build(check=False):
 registry=locales.load();groups={g['id']:g for g in registry['pages']};stale=[]
 targets=[(locales.ROOT/r['url'].lstrip('/')/'index.html',lang,r['url']) for g in registry['pages'] for lang,r in g['routes'].items() if r['status']=='published']
 targets.append((locales.ROOT/'404.html','pl','/404.html'))
 for path,lang,url in targets:
  source=path.read_text();new=update(source,lang,url,groups)
  if source!=new:
   stale.append(str(path.relative_to(locales.ROOT)))
   if not check:path.write_text(new)
 print(f'Corporate navigation: {len(targets)} pages; changed/stale: {len(stale)}')
 if check and stale:raise SystemExit(1)
if __name__=='__main__':
 parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');build(parser.parse_args().check)

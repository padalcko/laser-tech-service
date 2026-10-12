#!/usr/bin/env python3
"""Check visible FAQ/schema parity, local business consistency and discovery metadata."""
import importlib.util,json,re,collections
from pathlib import Path
spec=importlib.util.spec_from_file_location('ai',Path(__file__).resolve().with_name('build-ai-search.py'));a=importlib.util.module_from_spec(spec);spec.loader.exec_module(a)
pages=a.discover();issues=collections.defaultdict(list);incoming=collections.Counter();nap=[];counts=collections.Counter()
def walk(v):
 if isinstance(v,dict):
  yield v
  for x in v.values():yield from walk(x)
 elif isinstance(v,list):
  for x in v:yield from walk(x)
def norm(t):return re.sub(r'\W','',t).lower()
for p in pages:
 main=next(p['tree'].all('body'));visible=norm(main.text());url=p['canonical'];counts['pages']+=1
 for n in p['tags']:
  if n.tag=='a':
   target=a.absolute(n.attrs.get('href',''),url).split('#')[0]
   if target!=url:incoming[target]+=1
  if n.tag=='img' and 'alt' not in n.attrs:issues['missing_alt'].append(url)
 for data in p['schemas']:
  for v in walk(data):
   if v.get('@type')=='LocalBusiness':nap.append({k:v.get(k) for k in ['address','geo','openingHours','telephone','email']})
   if v.get('@type')=='Question':
    counts['faq_questions']+=1
    if norm(v['name']) not in visible:issues['faq_question_not_visible'].append(url)
    answer=v.get('acceptedAnswer',{}).get('text','')
    if norm(re.sub('<[^>]*>','',answer)) not in visible:issues['faq_answer_not_visible'].append(url)
   if v.get('@type') in ['Article','BlogPosting']:
    if v.get('datePublished','')>v.get('dateModified','9999'):issues['date_order'].append(url)
 for field in ['og:title','og:description','og:image','og:url']:
  if not p['meta'].get(field):issues['missing_'+field].append(url)
for p in pages:
 if not incoming[p['canonical']]:issues['orphan'].append(p['canonical'])
print(json.dumps({'counts':counts,'nap_variants':len({json.dumps(n,sort_keys=True) for n in nap}),'issues':issues},ensure_ascii=False,indent=2))

if issues or len({json.dumps(n,sort_keys=True) for n in nap}) != 1:
 raise SystemExit(1)

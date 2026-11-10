#!/usr/bin/env python3
"""Validate the shared blog presentation, author and unchanged article content."""
import importlib.util,json,re,subprocess,argparse
from collections import Counter
from pathlib import Path
spec=importlib.util.spec_from_file_location('blog_layout',Path(__file__).with_name('build-blog-layout.py'))
layout=importlib.util.module_from_spec(spec);spec.loader.exec_module(layout)
parser=argparse.ArgumentParser();parser.add_argument('--compare-head',action='store_true',help='Compare copy/media against the pre-change HEAD');args=parser.parse_args()
def main_tree(source):return layout.Tree(re.search(r'<main\b.*?</main>',source,re.S)[0]).root
for path in layout.paths():
 source=path.read_text();tree=main_tree(source);rel=str(path.relative_to(layout.ROOT))
 assert layout.transform(source)==source,('stale',rel)
 signatures=tree.all('article-signature');assert len(signatures)==1,rel
 assert signatures[0].render()==layout.SIGNATURE,rel
 assert signatures[0].parent.children[-1] is signatures[0],rel
 assert f'<meta name="author" content="{layout.AUTHOR["name"]}" />' in source,rel
 authors=[]
 for raw in re.findall(r'<script[^>]*type="application/ld\+json"[^>]*>(.*?)</script>',source,re.S):
  schema=json.loads(raw)
  for node in schema.get('@graph',[schema]):
   if 'author' in node:authors.append(node['author'])
 assert authors and all(a==layout.AUTHOR for a in authors),rel
 for cta in tree.all('article-cta'):
  assert len(cta.all('article-cta__eyebrow'))==1,rel
  assert len(cta.all('article-cta__button--primary'))==1,rel
  assert any('wa.me/' in n.attrs.get('href','') for n in cta.all('article-cta__button--secondary')),rel
 for fig in tree.all('article-image'):
  assert 0<int(fig.attrs['data-photo-width'])<=480,rel
  assert 0<int(fig.attrs['data-photo-height'])<=480,rel
 if args.compare_head:
  old=subprocess.check_output(['git','show','HEAD:'+rel],text=True);before=main_tree(old);after=main_tree(source)
  for tag,attr in [('img','src'),('iframe','src'),('form','action'),('time','datetime')]:
   assert Counter(n.attrs.get(attr) for n in before.all(tag=tag))==Counter(n.attrs.get(attr) for n in after.all(tag=tag)),(rel,tag)
  for t in [before,after]:
   for cls in ['article-signature','article-meta']:
    for n in list(t.all(cls)):layout.remove(n)
  for tag in ['h1','h2','h3','p','li','figcaption']:
   a=Counter(re.sub(r'\s+',' ',n.text()).strip() for n in before.all(tag=tag));b=Counter(re.sub(r'\s+',' ',n.text()).strip() for n in after.all(tag=tag));assert not a-b,(rel,tag,a-b)
  assert old[old.index('</main>')+7:]==source[source.index('</main>')+7:],rel
print('PASS: 96 blog layouts, single reference signature, metadata/schema author, CTA controls, photo caps and idempotence'+('; original copy/media/forms/dates preserved' if args.compare_head else ''))

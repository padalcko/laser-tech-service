#!/usr/bin/env python3
"""Validate generated AI resources and current HTML without network or dependencies."""
import collections, importlib.util, json, re, sys
from pathlib import Path
from urllib.parse import urlsplit, unquote
from urllib.robotparser import RobotFileParser
import xml.etree.ElementTree as ET
spec=importlib.util.spec_from_file_location('ai',Path(__file__).with_name('build-ai-search.py'))
ai=importlib.util.module_from_spec(spec);spec.loader.exec_module(ai)
R,B=ai.ROOT,ai.BASE
issues=collections.defaultdict(list);counts=collections.Counter();external=set()
def problem(kind,value):issues[kind].append(value)
pages=ai.discover();lookup={p['canonical']:p for p in pages}
allhtml={p:ai.Parser(p.read_text()).root for p in R.rglob('*.html') if '.git' not in p.parts}
redirects={x.split()[0]:x.split()[1] for x in (R/'_redirects').read_text().splitlines() if x.strip() and not x.startswith('#')}
def link(url,source):
    counts['links_checked']+=1
    u=urlsplit(url)
    if u.scheme in ('mailto','tel','data','javascript'):return
    if u.netloc and u.netloc!='lasertechservice.pl':external.add(url);return
    if not u.path:return
    path=unquote(u.path)
    if path in redirects:problem('redirect_links',[str(source),url])
    target=R/path.lstrip('/') if path.startswith('/') else source.parent/path
    if target.is_dir():target=target/'index.html'
    if not target.is_file():problem('broken_links',[str(source.relative_to(R)),url]);return
    if u.fragment and target.suffix=='.html':
        ids={n.attrs.get('id') for n in allhtml[target].all()}
        if unquote(u.fragment) not in ids:problem('broken_fragments',[str(source.relative_to(R)),url])
def walk(value):
    if isinstance(value,dict):
        yield value
        for x in value.values():yield from walk(x)
    elif isinstance(value,list):
        for x in value:yield from walk(x)
def norm(text):return re.sub(r'[^\w]+','',text.lower())
robot=RobotFileParser();robot.parse((R/'robots.txt').read_text().splitlines())
for agent in ('Googlebot','Bingbot','OAI-SearchBot','ChatGPT-User','PerplexityBot'):
    for page in pages:
        for url in (page['canonical'],page['md']):
            counts['search_crawler_checks']+=1
            if not robot.can_fetch(agent,url):problem('blocked_search_crawler',[agent,url])
for field in ('title','description'):
    values=collections.defaultdict(list)
    for page in pages:
        value=(next((n.text() for n in page['tags'] if n.tag=='title'),'')
               if field=='title' else page['meta'].get('description',''))
        if not value:problem('missing_'+field,page['canonical'])
        values[value].append(page['canonical'])
    for value,urls in values.items():
        if len(urls)>1:problem('duplicate_'+field,urls)
expected=ai.outputs(pages)
for path,content in expected.items():
    if not path.exists() or path.read_text()!=content:problem('stale_resources',str(path.relative_to(R)))
for path,tree in allhtml.items():
    counts['html_pages']+=1
    for n in tree.all():
        for a in ('href','src','poster'):
            if n.attrs.get(a):link(n.attrs[a],path)
        if n.attrs.get('srcset'):
            for entry in n.attrs['srcset'].split(','):link(entry.strip().split()[0],path)
    for raw in ai.SCHEMA_RE.findall(path.read_text()):
        try:data=json.loads(raw)
        except ValueError:problem('schema_problems',[str(path),'invalid JSON']);continue
        counts['json_ld_blocks']+=1
        for v in walk(data):
            t=v.get('@type')
            if t:counts['schema_'+str(t)]+=1
            if t in ('Organization','LocalBusiness') and v.get('name')=='Laser Tech Service':
                if v.get('@id')!=ai.ORG or v.get('url')!=B+'/':problem('schema_problems',[str(path),'entity identity'])
            if t=='LocalBusiness':
                if v.get('telephone')!='+48 790 402 597' or v.get('email')!='contact@lasertechservice.pl':problem('nap_conflicts',str(path))
            if t=='VideoObject' and v.get('embedUrl'):
                embeds=[n.attrs.get('src') for n in tree.all('iframe')]
                if v['embedUrl'] not in embeds:problem('video_mismatch',[str(path),v['embedUrl']])
            for key in ['url','image','thumbnailUrl','contentUrl','embedUrl']:
                value=v.get(key)
                for u in value if isinstance(value,list) else [value]:
                    if isinstance(u,str) and u.startswith(B+'/'):link(u,path)
    described=[n for n in tree.all('link') if n.attrs.get('rel')=='describedby']
    if len(described)!=1 or described[0].attrs.get('href')!='/llms.txt':problem('html_integration',str(path))
for page in pages:
    path=page['path'];tags=page['tags'];own=page['canonical'];lang=page['lang'];mdpath=path.with_suffix('.md');md=mdpath.read_text()
    counts['markdown_resources']+=1;counts[page['kind']+'_markdown']+=1
    alt={n.attrs['hreflang']:n.attrs.get('href') for n in tags if n.tag=='link' and n.attrs.get('hreflang')}
    # Polish-only cases have no translated alternate; paired pages stay reciprocal.
    monolingual_case = page['kind']=='case' and lang=='pl' and not alt
    if not monolingual_case and (set(alt)!=set(['pl','ru','x-default']) or alt.get(lang)!=own or alt.get('x-default')!=alt.get('pl')):problem('hreflang_problems',own)
    for u in alt.values():
        if u not in lookup or lookup[u]['alternates']!=alt:problem('hreflang_problems',[own,u])
    links=[n.attrs.get('href') for n in tags if n.tag=='link' and n.attrs.get('rel')=='alternate' and n.attrs.get('type')=='text/markdown']
    if links!=[page['md']]:problem('html_integration',own)
    if not md.startswith('# '+page['title']+'\n') or own not in md:problem('source_consistency',own)
    if ('Język: Polski' if lang=='pl' else 'Язык: Русский') not in md:problem('language_consistency',own)
    # Compare retained paragraphs/headings/lists independently of the renderer.
    plain=re.sub(r'!?\[([^\]]*)\]\([^)]*\)',r'\1',md);normalized=norm(plain)
    for node in page['tags']:
        if node.tag not in ('p','h2','h3','li'):continue
        ancestor=node;skip=False
        while ancestor:
            if ai.excluded(ancestor) or ancestor.tag=='section' and any(ancestor.all('form')):skip=True;break
            ancestor=ancestor.parent
        if skip:continue
        text=node.text().replace('▼','')
        if text and norm(text) not in normalized:problem('source_consistency',[own,text[:120]])
        counts['source_content_blocks_checked']+=1
    if re.search(r'<(?:script|style|form|iframe)\b|/Users/|webhook|GTM-[A-Z0-9]+',md,re.I):problem('private_or_ui_content',own)
    if not robot.can_fetch('GPTBot',page['md']) or not robot.can_fetch('Googlebot',page['md']):problem('blocked_resources',page['md'])
# Parse every generated Markdown URL including external ones, and all llms links.
resources=[p['path'].with_suffix('.md') for p in pages]+[R/'llms.txt',R/'llms-full.txt']
for path in resources:
    for u in re.findall(r'\]\(([^\s)]+)\)',path.read_text()):link(u,path)
    if not robot.can_fetch('*',B+'/'+str(path.relative_to(R))):problem('blocked_resources',str(path))
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9','x':'http://www.w3.org/1999/xhtml'}
entries=ET.parse(R/'sitemap.xml').findall('s:url',ns);seen=set()
for e in entries:
    u=e.find('s:loc',ns).text
    if u in seen:problem('duplicate_canonical',u)
    seen.add(u);link(u,R/'sitemap.xml')
    if u not in lookup or not u.endswith('/') or u.endswith('.md'):problem('sitemap_problems',u);continue
    if {x.get('hreflang'):x.get('href') for x in e.findall('x:link',ns)}!=lookup[u]['alternates']:problem('sitemap_problems',u)
if seen!=set(lookup):problem('sitemap_problems','inventory mismatch')
# Every current indexable HTML file must be discoverable (not only existing sitemap rows).
for path,tree in allhtml.items():
    meta={n.attrs.get('name'):n.attrs.get('content','') for n in tree.all('meta')}
    if 'noindex' in meta.get('robots',''):continue
    c=[n.attrs.get('href') for n in tree.all('link') if n.attrs.get('rel')=='canonical']
    if len(c)!=1:problem('missing_canonical',str(path))
    elif c[0] not in lookup:problem('sitemap_problems',c[0])
headers=(R/'_headers').read_text()
for p in pages:
    block=urlsplit(p['md']).path+'\n  Content-Type: text/markdown; charset=utf-8\n  X-Content-Type-Options: nosniff\n  Link: <'+p['canonical']+'>; rel="canonical"'
    if block not in headers:problem('markdown_http_canonical',p['md'])
counts['sitemap_urls']=len(entries);counts['unique_external_urls']=len(external)
report={'counts':dict(counts),'issues':dict(issues),'external_urls':sorted(external)}
print(json.dumps(report,ensure_ascii=False,indent=2))
if issues:sys.exit(1)

#!/usr/bin/env python3
"""Generate static AI representations from current production HTML; standard library only.

Run normally to regenerate, or --check to detect stale files without writing.
HTML and sitemap are the source of truth. No network, history, or runtime dependencies.
"""
from pathlib import Path
import site_locales
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit, quote
import argparse, collections, hashlib, json, re, xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://lasertechservice.pl'
ORG = BASE + '/#organization'
NS = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
VOID = set('area base br col embed hr img input link meta param source track wbr'.split())
SKIP = set('head script style nav footer menu noscript form input select textarea button svg'.split())
SKIP_CLASSES = {'menu', 'language-switcher', 'article-back', 'article-meta', 'case-tags',
                'article-category', 'article-signature', 'article-cta', 'realizacje-cta',
                'map-section', 'case-video-wrapper', 'faq-question__icon', 'devices-carousel'}
SCHEMA_RE = re.compile(r'<script\b[^>]*type="application/ld\+json"[^>]*>(.*?)</script>', re.S)
BEGIN, END = '<!-- AI resources: generated -->', '<!-- /AI resources -->'

class Node:
    def __init__(self, tag='', attrs=(), parent=None, data=''):
        self.tag, self.attrs, self.parent, self.data = tag, dict(attrs), parent, data
        self.children = []
    def all(self, tag=None):
        for child in self.children:
            if tag is None or child.tag == tag:
                yield child
            yield from child.all(tag)
    def text(self):
        return re.sub(r'\s+', ' ', self.data + ''.join(c.text_raw() for c in self.children)).strip()
    def text_raw(self):
        return self.data + ''.join(c.text_raw() for c in self.children)
    def has(self, cls):
        return cls in self.attrs.get('class', '').split()

class Parser(HTMLParser):
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.root = Node(); self.current = self.root
        self.feed(source)
    def handle_starttag(self, tag, attrs):
        node = Node(tag, attrs, self.current)
        self.current.children.append(node)
        if tag not in VOID:
            self.current = node
    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in VOID:
            self.handle_endtag(tag)
    def handle_endtag(self, tag):
        node = self.current
        while node.parent:
            if node.tag == tag:
                self.current = node.parent; return
            node = node.parent
    def handle_data(self, data):
        self.current.children.append(Node(parent=self.current, data=data))

def absolute(value, canonical):
    return quote(urljoin(canonical, value), safe=':/?#&=%+@,;~!$\'*-._')

def discover():
    registry = site_locales.load(ROOT / 'scripts/site-locales.json')
    routes = site_locales.index(registry)
    sitemap = ET.parse(ROOT / 'sitemap.xml')
    urls = [e.text for e in sitemap.findall('s:url/s:loc', NS)]
    assert len(urls) == len(set(urls)), 'Duplicate sitemap URLs'
    expected = {BASE + url for url, (_, _, status) in routes.items() if status == 'published'}
    assert set(urls) == expected, 'Sitemap and published registry routes differ'
    pages = []
    for url in sorted(urls):
        assert url.startswith(BASE + '/') and url.endswith('/'), url
        path = ROOT / urlsplit(url).path.lstrip('/') / 'index.html'
        source = path.read_text(encoding='utf-8')
        tree = Parser(source).root
        tags = list(tree.all())
        meta = {n.attrs.get('name', n.attrs.get('property')): n.attrs.get('content', '')
                for n in tags if n.tag == 'meta'}
        assert 'noindex' not in meta.get('robots', ''), path
        canonical = [n.attrs.get('href') for n in tags if n.tag == 'link' and n.attrs.get('rel') == 'canonical']
        assert canonical == [url], (path, canonical)
        lang = next(n.attrs['lang'] for n in tags if n.tag == 'html')
        group, registered_lang, status = routes[urlsplit(url).path]
        assert lang == registered_lang and status == 'published', path
        expected_alternates = site_locales.alternates(group, BASE)
        actual_alternates = [n for n in tags if n.tag == 'link' and n.attrs.get('hreflang')]
        assert len(actual_alternates) == len(expected_alternates), path
        assert {n.attrs['hreflang']: n.attrs['href'] for n in actual_alternates} == expected_alternates, path
        h1s = [n for n in tags if n.tag == 'h1']; assert len(h1s) == 1, path
        kind = {'case-study': 'case', 'article': 'article', 'services': 'service',
                'service-detail': 'service', 'pricing': 'service'}.get(group['type'], 'other')
        pages.append(dict(path=path, source=source, tree=tree, tags=tags, meta=meta,
                          canonical=url, lang=lang, page_type=group['type'], group_id=group['id'],
                          route_group=group, languages=registry['languages'], title=h1s[0].text(), kind=kind,
                          md=url+'index.md', alternates={n.attrs['hreflang']:n.attrs['href']
                          for n in tags if n.tag=='link' and n.attrs.get('hreflang')},
                          schemas=[json.loads(m) for m in SCHEMA_RE.findall(source)]))
    return pages

def excluded(node):
    classes = set(node.attrs.get('class', '').split())
    return ((node.tag in SKIP and not (node.tag == 'button' and node.has('faq__question'))) or bool(classes & SKIP_CLASSES) or
            node.attrs.get('aria-hidden') == 'true' or 'hidden' in node.attrs or
            any('eyebrow' in c or 'breadcrumb' in c or c.endswith('__number') for c in classes))

def content_roots(page):
    # Several legacy home/index sections are siblings of main. Keep their public content.
    return [next(n for n in page['tags'] if n.tag == 'body')]

def render(node, page, seen_images):
    if excluded(node) or node.tag == 'h1': return ''
    if node.tag == 'section' and any(node.all('form')): return ''
    if not node.tag:
        return re.sub(r'\s+', ' ', node.data).replace('▼', '')
    if node.tag == 'img':
        src, alt = node.attrs.get('src', ''), node.attrs.get('alt', '').strip()
        if not alt or '/icons/' in src or src in seen_images: return ''
        seen_images.add(src)
        return '\n\n!['+alt.replace('[','\\[').replace(']','\\]')+']('+absolute(src,page['canonical'])+')\n\n'
    if node.tag == 'iframe':
        src = node.attrs.get('src', '')
        if 'youtube.com/embed/' not in src: return ''
        return '\n\n['+node.attrs.get('title', 'Video')+']('+absolute(src,page['canonical'])+')\n\n'
    body = ''.join(render(c, page, seen_images) for c in node.children)
    if node.tag == 'a':
        href = node.attrs.get('href', '')
        if not href or href.startswith(('javascript:', '#')) and href == '#': return body
        label = re.sub(r'\s+', ' ', body).strip()
        if node.has('partner-card'):
            link_label = {'pl': 'Strona partnera', 'ru': 'Страница партнёра', 'en': 'Partner website'}[page['lang']]
            return body + '\n\n[' + link_label + '](' + absolute(href, page['canonical']) + ')\n\n'
        # Linked photographs already carry their own evidence URL.
        if not label or '![' in label: return body
        return '['+label+']('+absolute(href,page['canonical'])+')'
    if node.tag in ('h2','h3','h4','h5','h6'):
        return '\n\n'+'#'*int(node.tag[1])+' '+body.strip()+'\n\n'
    if node.tag == 'li': return '\n- '+body.strip().replace('\n\n','\n  ')+'\n'
    if node.tag == 'ol':
        items=[render(c,page,seen_images).strip().removeprefix('- ') for c in node.children if c.tag=='li']
        return '\n\n'+'\n'.join(str(i)+'. '+value for i,value in enumerate(items,1))+'\n\n'
    if node.tag == 'ul': return '\n'+body.strip()+'\n\n'
    if node.tag == 'blockquote': return '\n\n> '+body.strip().replace('\n','\n> ')+'\n\n'
    if node.has('case-info__item'):
        values=[c.text() for c in node.children if c.tag and c.text()]
        return '\n- '+': '.join(values)+'\n'
    if node.tag == 'br': return '\n'
    if node.tag in ('strong','b'): return '**'+body.strip()+'**' if body.strip() else ''
    if node.tag in ('em','i'): return '*'+body.strip()+'*' if body.strip() else ''
    if node.tag in ('p','div','section','header','main','article','figure','figcaption','address','details','summary','dl','dt','dd'):
        return '\n\n'+body.strip()+'\n\n' if body.strip() else ''
    return body

def clean(text):
    text = re.sub(r'[ \t]+\n', '\n', text)
    text = re.sub(r'\n[ \t]+', '\n', text)
    return re.sub(r'\n{3,}', '\n\n', text).strip()

def relationships(page, pages):
    lookup = {p['canonical']:p for p in pages}
    seen = set(); groups = collections.defaultdict(list)
    # Relationships use links actually present in this HTML; no speculative matches.
    for n in page['tags']:
        if n.tag != 'a' or not n.attrs.get('href'): continue
        u = urljoin(page['canonical'], n.attrs['href']).split('#')[0]
        if u in seen or u == page['canonical']: continue
        seen.add(u)
        if u not in lookup: continue
        peer = lookup[u]
        if peer['lang'] != page['lang']: continue
        if peer['kind'] in ('case','article','service'):
            groups[peer['kind']].append(peer)
    # Service evidence relationships are also explicit in the page's JSON-LD.
    for schema in page['schemas']:
        for evidence in schema.get('subjectOf', []) if isinstance(schema.get('subjectOf', []), list) else []:
            u=evidence.get('url') if isinstance(evidence, dict) else None
            if u in lookup and u not in seen and lookup[u]['lang']==page['lang']:
                groups[lookup[u]['kind']].append(lookup[u]); seen.add(u)
    return groups

def markdown(page, pages):
    ru = page['lang'] == 'ru'
    en = page['lang'] == 'en'
    source_label, language_label = ('HTML source','Language') if en else (('Источник HTML','Язык') if ru else ('Źródło HTML','Język'))
    title=page['title']; out='# '+title+'\n\n'
    out+=f'{source_label}: [{title}]({page["canonical"]})\n\n{language_label}: '+page['languages'][page['lang']]+'\n\n'
    peers=[f'[{page["languages"][l]}]({BASE + u})' for l,u in site_locales.published(page['route_group']).items() if l!=page['lang']]
    if peers: out+=('Other language version: ' if en else 'Версия на другом языке: ' if ru else 'Inna wersja językowa: ')+', '.join(peers)+'\n\n'
    out+='> '+page['meta'].get('description','')+'\n\n'
    for schema in page['schemas']:
        if schema.get('@type') in ('Article','BlogPosting'):
            author=schema.get('author',{})
            if isinstance(author,dict) and author.get('name'):
                out+=('Author: ' if en else 'Автор: ' if ru else 'Autor: ')+author['name']+'\n\n'
            if schema.get('datePublished'):
                out+=('Publication date: ' if en else 'Дата публикации: ' if ru else 'Data publikacji: ')+schema['datePublished']+'\n\n'
    out+=clean(''.join(render(n,page,set()) for n in content_roots(page)))+'\n'
    # Explicit relationships are drawn solely from existing page links.
    labels={'case':('Related repairs' if en else 'Связанные работы' if ru else 'Powiązane realizacje'),
            'article':('Related articles' if en else 'Связанные статьи' if ru else 'Powiązane artykuły'),
            'service':('Service offerings' if en else 'Услуги сервиса' if ru else 'Usługi serwisowe')}
    for kind, peers in relationships(page,pages).items():
        out+='\n## '+labels[kind]+'\n\n'+''.join('- ['+p['title']+']('+p['canonical']+')\n' for p in peers)
    # Preserve actual video sources even when decorative iframe wrappers were excluded.
    videos=[]
    for n in page['tags']:
        if n.tag=='iframe' and 'youtube.com/embed/' in n.attrs.get('src',''):
            pair=(n.attrs.get('title','Video'),n.attrs['src'])
            if pair not in videos: videos.append(pair)
    if videos:out+='\n## '+('Video' if en else 'Видео' if ru else 'Wideo')+'\n\n'+''.join('- ['+t+']('+u+')\n' for t,u in videos)
    return clean(out)+'\n'

def integration(source, md):
    source=re.sub(re.escape(BEGIN)+r'.*?'+re.escape(END)+r'\n?', '', source, flags=re.S)
    block=BEGIN+'\n'
    if md:block+=f'    <link rel="alternate" type="text/markdown" href="{md}" />\n'
    block+='    <link rel="describedby" href="/llms.txt" />\n'+END+'\n'
    return source.replace('</head>',block+'</head>',1)

def llms(pages):
    lookup={p['canonical']:p for p in pages}
    def item(path, description, md=False):
        p=lookup[BASE+path]
        return f'- [{p["title"]}]({p["md"] if md else p["canonical"]}): {description}\n'
    out='''# Laser Tech Service

> Laser Tech Service repairs and maintains laser and cosmetic equipment. The business is based in Wrocław and serves clients across Poland.

The website is published in Polish and Russian. HTML pages are the canonical sources; their Markdown representations preserve the original language and link to language equivalents. Repair cases document work on specific devices, while blog articles explain technology, diagnostics and maintenance. A repair case does not establish manufacturer authorization or universal model compatibility. The site also documents selected jobs in Görlitz, Germany; this is not a claim of unrestricted international coverage.

## About

'''
    out+=item('/','Company, specialization and service geography.')
    out+=item('/','Polish company overview in Markdown.',True)
    out+='\n## Main Pages\n\n'
    for path,desc in [('/uslugi/','Service scope and equipment categories.'),('/realizacje/','Index of documented repairs and maintenance.'),('/blog/','Technical knowledge and company articles.'),('/partnerzy/','Partners presented on the website.'),('/kontakt/','Business contact information and address.')]:out+=item(path,desc)
    out+='\n## Services\n\n'
    out+=item('/uslugi/','Diagnostics, diode replacement, handpieces, cooling, power supplies, electronics and preventive maintenance; Wrocław and Poland.',True)
    out+=item('/ru/uslugi/','Russian representation of the services page.',True)
    for p in pages:
        if p['kind']=='service' and p['page_type']!='services':
            description = p['meta']['description']
            target = p['md']
            if p['page_type']=='pricing':
                target = p['canonical']
                description = (p['meta']['description'] if p['lang']=='en' else 'Orientacyjne ceny diagnostyki, naprawy i konserwacji. Koszt części może być rozliczany osobno; końcowa wycena po diagnostyce.' if p['lang'] == 'pl' else 'Ориентировочные цены диагностики, ремонта и обслуживания. Запчасти могут рассчитываться отдельно; окончательная стоимость после диагностики.')
            out+=f'- [{p["title"]}]({target}): {description}\n'
    out+='\n## Repair Cases\n\n'
    out+=item('/realizacje/','Polish catalogue; each case has a Markdown version. Russian translations are linked where available.',True)
    out+=item('/ru/realizacje/','Russian catalogue of translated repair cases.',True)
    for p in pages:
        if p['kind']=='case' and p['lang']=='pl':out+=f'- [{p["title"]}]({p["canonical"]}): {p["meta"]["description"]}\n'
    out+='\n## Knowledge Base / Blog\n\n'
    out+=item('/blog/','Polish article catalogue; use article Markdown for full text and related cases.',True)
    out+=item('/ru/blog/','Russian article catalogue.',True)
    for p in pages:
        if p['kind']=='article' and p['lang']=='pl':out+=f'- [{p["title"]}]({p["canonical"]}): {p["meta"]["description"]}\n'
    out+='\n## Partners\n\n'+item('/partnerzy/','Partners: AnnVi (cosmetology and podology, Wrocław), Magia Kosmetyczna (beauty salon, Bydgoszcz), Cuprum Laser Tech (laser surface cleaning) and Cuprum Beauty Lab (diode laser hair removal, Lubin).',True)
    out+='\n## Contact\n\n'+item('/kontakt/','Marsz. Józefa Piłsudskiego 74 lok. 320, 50-020 Wrocław, Poland; +48 790 402 597; contact@lasertechservice.pl.',True)
    out+='\n## Languages\n\n'+item('/','Polish website.')+item('/ru/','Russian website.')
    out+='\n## Important Resources\n\n- [Expanded site text]('+BASE+'/llms-full.txt): Company, services, equipment, cases, articles, locations, partners, contact and language map.\n- [XML sitemap]('+BASE+'/sitemap.xml): Canonical HTML pages and language equivalents.\n- [Crawler rules]('+BASE+'/robots.txt): Access rules; independent from this resource map.\n'
    out+='\n## Optional\n\n'
    for path,desc in [('/realizacje/wymiana-modulu-diodowego-lasera-po-zalaniu-poznan/','Diode module replacement after coolant ingress in Poznań.'),('/blog/dlaczego-nie-warto-samodzielnie-wymieniac-uszczelek-w-laserze/','Seal replacement risks and the related water-damage case.'),('/realizacje/naprawa-3000-nain-bloku-zasilania/','Power-supply repair with links to the recorded videos.')]:out+=item(path,desc,True)
    extra = [p for p in pages if p['lang'] not in ('pl', 'ru')]
    if extra:
        out = out.replace('published in Polish and Russian.', 'published in ' + ', '.join(dict.fromkeys(p['languages'][p['lang']] for p in pages)) + '.')
        out += '\n## Additional published language pages\n\n'
        for p in extra:
            if p['kind'] == 'service' and p['page_type'] != 'services':
                continue  # Already included in Services above.
            out += f'- [{p["title"]}]({p["md"]}): {p["meta"].get("description", "")}\n'
    return out

def full_text(pages, representations):
    out='# Laser Tech Service — expanded site text\n\nCanonical HTML remains the source of truth. Page content below retains its Polish or Russian language.\n'
    sections=[('Company',lambda p:p['page_type']=='home'),
              ('Services',lambda p:p['kind']=='service'),
              ('Repair Cases',lambda p:p['kind']=='case'),
              ('Knowledge Articles',lambda p:p['kind']=='article'),
              ('Partners',lambda p:p['page_type']=='partners'),
              ('Contact',lambda p:p['page_type']=='contact')]
    for heading,predicate in sections:
        out+='\n## '+heading+'\n'
        for p in pages:
            if predicate(p):
                md=representations[p['path'].with_suffix('.md')]
                # Shift heading hierarchy when embedding complete source content.
                md=re.sub(r'^(#{1,6}) ',lambda m:'#' * min(len(m[1])+2,6)+' ',md,flags=re.M)
                out+='\n'+md
        if heading=='Services':
            out+='\n## Equipment\n\n'
            for p in pages:
                if p['kind']=='service':
                    lists=[n for n in p['tags'] if n.tag=='li' and any(word in n.text().lower() for word in ['diod','диод','ipl','yag','co2','rf','lpg','krio','крио','pikosek','пикосек'])]
                    out+='\n### '+p['languages'][p['lang']]+'\n\n'+''.join('- '+n.text()+'\n' for n in lists)
                    out+='\n[HTML]('+p['canonical']+')\n'
    out+='\n## Locations\n\n'
    for p in pages:
        if p['kind']=='case' and p['lang']=='pl':
            # Only explicit per-case location fields/hero context, never city inference from footer.
            loc=[]
            for n in p['tags']:
                if n.has('case-info__item') and re.search('Lokalizacja|Miasto',n.text()):loc.append(n.text())
            if not loc and re.search(r'Wrocław|Poznań|Görlitz|Lublin|Legnica',p['title']):loc=[p['title']]
            if loc:out+='- ['+p['title']+']('+p['canonical']+'): '+'; '.join(loc)+'\n'
    out+='\n## Languages\n\n'
    for p in pages:
        if p['lang']=='pl':
            out+='- [Polski: '+p['title']+']('+p['canonical']+')'
            language_routes = site_locales.published(p['route_group'])
            if any(l != 'pl' for l in language_routes):
                for lang, route in language_routes.items():
                    url = BASE + route
                    if lang != 'pl' and lang in p['languages']:
                        out+=' — ['+p['languages'][lang]+']('+url+')'
            else:
                out+=' — Polish only'
            out+='\n'
    extra = [p for p in pages if p['lang'] not in ('pl', 'ru')]
    if extra:
        out = out.replace('its Polish or Russian language.', 'its original published language.')
        for p in extra:
            if 'pl' not in site_locales.published(p['route_group']):
                out += '- [' + p['languages'][p['lang']] + ': ' + p['title'] + '](' + p['canonical'] + ')\n'
    return out

def outputs(pages):
    generated={p['path'].with_suffix('.md'):markdown(p,pages) for p in pages}
    generated[ROOT/'llms.txt']=llms(pages)
    generated[ROOT/'llms-full.txt']=full_text(pages,generated)
    for p in pages:generated[p['path']]=integration(p['source'],p['md'])
    p=ROOT/'404.html';generated[p]=integration(p.read_text(),None)
    # Exact resource routes: no wildcard assumptions, no changes to HTML routing.
    headers='# Generated by scripts/build-ai-search.py. Canonical HTML for alternate representations.\n'
    for p in pages:
        headers+='\n'+urlsplit(p['md']).path+'\n  Content-Type: text/markdown; charset=utf-8\n  X-Content-Type-Options: nosniff\n  Link: <'+p['canonical']+'>; rel="canonical", <'+BASE+'/llms.txt>; rel="describedby"\n'
    for name in ['llms.txt','llms-full.txt']:
        headers+='\n/'+name+'\n  Content-Type: text/plain; charset=utf-8\n  X-Content-Type-Options: nosniff\n'
    start, end = '# BEGIN GENERATED AI HEADERS', '# END GENERATED AI HEADERS'
    target=ROOT/'_headers'
    existing=target.read_text() if target.exists() else ''
    block=start+'\n'+headers+end+'\n'
    if start in existing:
        headers=re.sub(re.escape(start)+r'.*?'+re.escape(end)+r'\n?',lambda m:block,existing,flags=re.S)
    else:
        headers=existing.rstrip()+('\n\n' if existing.strip() else '')+block
    generated[target]=headers
    return generated

def main():
    args=argparse.ArgumentParser(description=__doc__);args.add_argument('--check',action='store_true');opts=args.parse_args()
    pages=discover();generated=outputs(pages);stale=[]
    for path,text in generated.items():
        if not path.exists() or path.read_text()!=text:
            stale.append(str(path.relative_to(ROOT)))
            if not opts.check:path.write_text(text,encoding='utf-8')
    expected={p['path'].with_suffix('.md') for p in pages}
    orphan=[str(p.relative_to(ROOT)) for p in ROOT.rglob('index.md') if p not in expected and '.git' not in p.parts]
    if orphan:raise SystemExit('Orphan resources require review (not deleted): '+', '.join(orphan))
    print(json.dumps({'pages':len(pages),'counts':dict(collections.Counter(p['kind'] for p in pages)),
                      'stale' if opts.check else 'updated':stale},ensure_ascii=False,indent=2))
    if opts.check and stale:raise SystemExit(1)

if __name__=='__main__':main()

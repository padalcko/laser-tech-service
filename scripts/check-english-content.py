#!/usr/bin/env python3
"""Stage 3C: content route, media, dates, schemas, index order and form parity."""
import importlib.util
import json
import re
from pathlib import Path
import site_locales

spec = importlib.util.spec_from_file_location('ai', Path(__file__).with_name('build-ai-search.py'))
ai = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ai)
pages = ai.discover()
lookup = {p['canonical']: p for p in pages}
content = [p for p in pages if p['lang'] == 'en' and p['route_group']['type'] in ('article', 'case-study', 'blog', 'case-studies')]
assert len(content) == 45
assert len(pages) == 195

def walk(v):
    if isinstance(v, dict):
        yield v
        for value in v.values(): yield from walk(value)
    elif isinstance(v, list):
        for value in v: yield from walk(value)

def media(p):
    keys = ('src', 'srcset', 'sizes', 'width', 'height', 'loading', 'allow', 'allowfullscreen', 'data-full', 'poster', 'controls', 'preload')
    return [(n.tag, {k:n.attrs[k] for k in keys if k in n.attrs}) for n in p['tags'] if n.tag in ('img','source','video','iframe')]

def dates(p):
    return [(k,v) for s in p['schemas'] for n in walk(s) for k,v in n.items() if k in ('datePublished','dateModified','uploadDate')]

for p in content:
    pl = lookup[p['alternates']['pl']]
    assert media(p) == media(pl), ('media', p['canonical'])
    assert dates(p) == dates(pl), ('dates', p['canonical'])
    assert [n.attrs.get('datetime') for n in p['tags'] if n.tag=='time'] == [n.attrs.get('datetime') for n in pl['tags'] if n.tag=='time']
    assert len(list(p['tree'].all('h1'))) == 1
    assert p['meta']['og:locale'] == 'en_GB'
    assert p['alternates'] == site_locales.expected_alternates(p['canonical'])
    schemas = [n for s in p['schemas'] for n in walk(s)]
    assert any(n.get('@type')=='BreadcrumbList' for n in schemas)
    if p['route_group']['type']=='article':
        assert any(n.get('@type') in ('Article','BlogPosting') for n in schemas)
    assert all(' ' not in n.get('@type','') for n in schemas if isinstance(n.get('@type'),str))
    assert next(n for n in p['tags'] if n.tag=='html').attrs['data-lazar-enabled']=='false'
    def fields(page):
        return [(n.tag,n.attrs.get('name'),n.attrs.get('type')) for n in page['tags'] if n.tag in ('input','textarea','select')]
    assert fields(p)==fields(pl), ('form contract',p['canonical'])
    for n in p['tags']:
        if n.tag=='input' and n.attrs.get('name')=='language': assert n.attrs.get('value')=='en'
        if n.tag=='a' and n.attrs.get('href','').startswith('/en/'):
            assert ai.BASE+n.attrs['href'].split('#')[0] in lookup
    main = next(p['tree'].all('main'))
    assert not re.search(r'\b(?:urządzeni[aeu]|napraw[ayę]|głowic[ayę]|czytaj|zobacz|dlaczego|przegląd|prawidłow[ayoe]|wymiana|serwisowanie)\b',main.text(),re.I),p['canonical']
    if p['route_group']['type'] in ('blog','case-studies'):
        kind='article' if p['route_group']['type']=='blog' else 'case-study'
        def linked_groups(page):
            result=[]
            for n in next(page['tree'].all('main')).all('a'):
                u=ai.absolute(n.attrs.get('href',''),page['canonical']).split('#')[0]
                target=lookup.get(u)
                if target and target['route_group']['type']==kind: result.append(target['route_group']['id'])
            return result
        assert linked_groups(p)==linked_groups(pl),('index order',p['canonical'])
        assert len(set(linked_groups(p)))==(21 if kind=='article' else 22)
        for n in main.all('a'):
            href=n.attrs.get('href','')
            assert not href.startswith(('/blog/','/realizacje/'))
        if kind=='article': assert not list(main.all('img')),'Blog cards remain text-only'
print('PASS: 45 content pages, 195 canonical routes; source media/date/form parity, index order, EN links, schemas and chat gate')

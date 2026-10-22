#!/usr/bin/env python3
"""Validate publication, reciprocal SEO, and planned-route exclusion (read only)."""
import copy
import importlib.util
import json
import tempfile
from pathlib import Path
import site_locales as locales

spec = importlib.util.spec_from_file_location('ai', Path(__file__).with_name('build-ai-search.py'))
ai = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ai)
registry = locales.load()
pages = ai.discover()  # Checks sitemap equality, canonical, lang, and exact reciprocal alternates.
for url, (_, _, status) in locales.index(registry).items():
    if status == 'planned':
        assert not (ai.ROOT / url.lstrip('/') / 'index.html').exists(), 'Planned route has HTML: ' + url
        assert not (ai.ROOT / url.lstrip('/') / 'index.md').exists(), 'Planned route has Markdown: ' + url
        for name in ('sitemap.xml', 'ai-catalog.json', 'llms.txt', 'llms-full.txt', '_headers'):
            assert ai.BASE + url not in (ai.ROOT / name).read_text(), (name, url)

# Registry failures must fail closed; no mutation of source files.
with tempfile.TemporaryDirectory(prefix='lts-locales-') as directory:
    target = Path(directory) / 'registry.json'
    for mutation in ('id', 'url', 'status', 'language', 'default', 'prefix'):
        bad = copy.deepcopy(registry)
        first, second = bad['pages'][:2]
        if mutation == 'id': second['id'] = first['id']
        if mutation == 'url': second['routes']['pl']['url'] = first['routes']['pl']['url']
        if mutation == 'status': first['routes']['en']['status'] = 'ready'
        if mutation == 'language': first['routes']['xx'] = first['routes'].pop('en')
        if mutation == 'default':
            first['routes']['en']['status'] = 'planned'
            first['x_default'] = first['routes']['en']['url']
        if mutation == 'prefix': first['routes']['en']['url'] = '/wrong-prefix/'
        target.write_text(json.dumps(bad))
        try: locales.load(target)
        except AssertionError: pass
        else: raise AssertionError('Accepted invalid ' + mutation)

# A third published translation exposes only the correct peer and preserves x-default.
group = copy.deepcopy(registry['pages'][0])
group['routes']['en']['status'] = 'planned'
assert 'en' not in locales.published(group)
group['routes']['en']['status'] = 'published'
alts = locales.alternates(group, ai.BASE)
assert set(alts) == {'pl', 'ru', 'en', 'x-default'}
assert alts['x-default'] == ai.BASE + group['x_default']
assert alts['en'] == ai.BASE + group['routes']['en']['url']
print(json.dumps({'groups': len(registry['pages']), 'published_pages': len(pages),
                  'published_languages': sorted({p['lang'] for p in pages}),
                  'planned_routes': sum(status == 'planned' for _, _, status in locales.index(registry).values()),
                  'mutation_checks': 'PASS'}, indent=2))

# Exercise real discovery with all planned EN routes published, using in-memory IO only.
# This covers every page type and EN-only international groups without writing HTML.
from unittest.mock import patch
import xml.etree.ElementTree as ET
from html import escape
future = copy.deepcopy(registry)
for group in future['pages']:
    for route in group['routes'].values():
        route['status'] = 'published'
future_index = locales.index(future)
source_read = Path.read_text
sitemap = ET.parse(ai.ROOT / 'sitemap.xml')
existing_urls = {e.text for e in sitemap.findall('s:url/s:loc', ai.NS)}
for url, (_, lang, _) in future_index.items():
    if ai.BASE + url not in existing_urls:
        entry = ET.SubElement(sitemap.getroot(), '{' + ai.NS['s'] + '}url')
        ET.SubElement(entry, '{' + ai.NS['s'] + '}loc').text = ai.BASE + url

def future_read(path, *args, **kwargs):
    if path == ai.ROOT / 'scripts/site-locales.json':
        return json.dumps(future)
    if path.suffix == '.html' and path.name == 'index.html':
        route = '/' + str(path.parent.relative_to(ai.ROOT)).strip('.')
        route = route.rstrip('/') + '/'
        group, lang, _ = future_index[route]
        links = ''.join(f'<link rel="alternate" hreflang="{l}" href="{u}">' for l, u in locales.alternates(group, ai.BASE).items())
        if lang == 'en':
            return f'<html lang="en"><head><link rel="canonical" href="{ai.BASE + route}">{links}</head><body><h1>{escape(group["id"])}</h1></body></html>'
        source = source_read(path, *args, **kwargs)
        source = ai.re.sub(r'<link\b[^>]*hreflang="[^"]+"[^>]*>', '', source)
        return source.replace('</head>', links + '</head>')
    return source_read(path, *args, **kwargs)

with patch.object(Path, 'read_text', future_read), patch.object(ai.ET, 'parse', return_value=sitemap):
    future_pages = ai.discover()
assert len(future_pages) == len(future_index)
assert {p['page_type'] for p in future_pages if p['lang'] == 'en'} == locales.TYPES
assert all(p['kind'] == 'case' for p in future_pages if p['page_type'] == 'case-study')
# A sitemap entry alone must never promote a planned route to published.
if any(status == 'planned' for _, _, status in locales.index(registry).values()):
    with patch.object(ai.ET, 'parse', return_value=sitemap):
        try: ai.discover()
        except AssertionError as error: assert 'Sitemap' in str(error)
        else: raise AssertionError('Planned EN sitemap entries accepted')
print('PASS: in-memory PL/RU/EN discovery for every page type and EN-only international routes; planned sitemap rejected')

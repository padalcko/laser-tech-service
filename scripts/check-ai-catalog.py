#!/usr/bin/env python3
"""Validate catalog freshness and source-sensitive extraction with in-memory mutations."""
import copy
import importlib.util
import tempfile
from pathlib import Path

spec = importlib.util.spec_from_file_location('catalog', Path(__file__).with_name('build-ai-catalog.py'))
c = importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
pages = c.ai.discover()
expected = c.build(pages)
c.validate(expected, pages)
assert not c.generate(check=True), 'Catalog is stale; run build-ai-catalog.py'

# A price change must affect only its language's published starting amount, not a cennik figure.
changed = copy.deepcopy(pages)
p = next(p for p in changed if p['canonical'].endswith('/uslugi/wymiana-i-kalibracja-diod-laserowych/') and p['lang'] == 'pl')
node = next(n for n in c.body_nodes(p) if n.has('service-price'))
node.children = []; node.data = 'od 975 zł'
rebuilt = c.build(changed)
service = next(r for r in rebuilt['services'] if r['primary_url'] == p['canonical'])
assert service['localizations']['pl']['starting_price']['amount'] == 975
assert service['localizations']['ru']['starting_price']['amount'] == 800
assert service['id'] == next(r for r in expected['services'] if r['primary_url'] == p['canonical'])['id']
assert len(service['localizations']['pl']['available_work']) == 4

# No fabricated translation if one actual sitemap-listed language page is removed.
without_ru = [p for p in pages if p['canonical'] != service['localizations']['ru']['url']]
solo = next(r for r in c.build(without_ru)['services'] if r['id'] == service['id'])
assert set(solo['localizations']) == {'pl'}

# Removal and URL changes follow discovery; stale records are not retained.
article = next(p for p in pages if p['kind'] == 'article')
remaining = c.build([p for p in pages if p is not article])
assert len(remaining['articles']) == len(expected['articles']) - 1
renamed = copy.deepcopy(pages)
p = next(p for p in renamed if p['canonical'] == article['canonical'])
p['canonical'] = c.BASE + '/blog/test-new-route/'
assert any(r['canonical_url'] == p['canonical'] for r in c.build(renamed)['articles'])
assert all(r['canonical_url'] != article['canonical'] for r in c.build(renamed)['articles'])

# Invalid price provenance and duplicate IDs must fail validation.
for corrupt in ('price', 'id'):
    bad = copy.deepcopy(expected)
    if corrupt == 'id': bad['articles'][1]['id'] = bad['articles'][0]['id']
    else: bad['services'][0]['localizations']['pl']['starting_price']['amount'] = 1
    try: c.validate(bad, pages)
    except AssertionError: pass
    else: raise AssertionError('Invalid ' + corrupt + ' accepted')

# The timestamp and all bytes remain stable; --check never rewrites stale output.
with tempfile.TemporaryDirectory() as directory:
    c.TARGET = Path(directory) / 'ai-catalog.json'
    assert c.generate()
    first = c.TARGET.read_bytes()
    assert not c.generate()
    assert first == c.TARGET.read_bytes()
    c.TARGET.write_text('{}\n')
    assert c.generate(check=True)
    assert c.TARGET.read_text() == '{}\n'
print('PASS: freshness, source prices, missing translation, removals, URL changes, duplicate IDs, deterministic bytes and read-only check')

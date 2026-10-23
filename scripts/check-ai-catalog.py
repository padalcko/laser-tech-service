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
assert set(solo['localizations']) == set(service['localizations']) - {'ru'}

# Removal and URL changes follow discovery; stale records are not retained.
article = next(p for p in pages if p['kind'] == 'article')
remaining = c.build([p for p in pages if p is not article])
assert len(remaining['articles']) == len(expected['articles']) - 1
renamed = copy.deepcopy(pages)
p = next(p for p in renamed if p['canonical'] == article['canonical'])
p['canonical'] = c.BASE + '/blog/test-new-route/'
assert any(r['canonical_url'] == p['canonical'] for r in c.build(renamed)['articles'])
assert all(r['canonical_url'] != article['canonical'] for r in c.build(renamed)['articles'])

# Synthetic third locale: render/extract in memory, never create an English file.
en = copy.deepcopy(next(p for p in pages if p['canonical'] == service['primary_url']))
en_url = c.BASE + en['route_group']['routes']['en']['url']
en.update(lang='en', canonical=en_url, path=c.ROOT / en_url.removeprefix(c.BASE).strip('/') / 'index.html', md=en_url + 'index.md', title='Laser diode replacement and calibration')
en['route_group']['routes']['en']['status'] = 'published'
en['alternates']['en'] = en_url
for n in c.body_nodes(en):
    if n.has('service-price'):
        n.children = []; n.data = 'from 800 PLN'
    if n.tag == 'h2' and n.text().startswith('Co obejmuje'):
        n.children = []; n.data = 'Service scope'
trilingual = copy.deepcopy([p for p in pages if p['canonical'] != en_url])
for p in trilingual:
    if p['group_id'] == en['group_id']:
        p['alternates']['en'] = en_url
trilingual.append(en)
three = c.build(trilingual)
record = next(r for r in three['services'] if r['id'] == service['id'])
assert set(record['localizations']) == {'pl', 'ru', 'en'}
assert record['localizations']['en']['starting_price']['amount'] == 800
assert len(record['localizations']['en']['available_work']) == 4
assert record['primary_url'] == service['primary_url']
assert three['languages'] == ['pl', 'ru', 'en']
assert 'Language: English' in c.ai.markdown(en, trilingual)
assert en_url + 'index.md' in c.ai.llms(trilingual)
assert en_url in c.ai.full_text(trilingual, {p['path'].with_suffix('.md'): c.ai.markdown(p, trilingual) for p in trilingual})
assert set(expected['languages']) == {p['lang'] for p in pages}

# Currency-first English prices must preserve thousands and reject malformed amounts.
price_page = copy.deepcopy(en)
price_node = next(n for n in c.body_nodes(price_page) if n.has('service-price'))
for label, amount in [('from PLN 1,200', 1200), ('from PLN 800', 800), ('from PLN 1,200.50', 1200.5), ('from PLN 1,20', None), ('from EUR 330', 330), ('from EUR 1,200', 1200), ('from EUR 1,20', None)]:
    price_node.children = []; price_node.data = label
    parsed = c.price(price_page)
    assert (parsed['amount'] if parsed else None) == amount, label
    if parsed: assert parsed['currency'] == ('EUR' if 'EUR' in label else 'PLN')

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

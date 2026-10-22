#!/usr/bin/env python3
"""Validate published EN sources, source prices, forms and the chat release gate."""
import importlib.util
import json
from pathlib import Path
import site_locales
from eur_pricing import convert

spec = importlib.util.spec_from_file_location('ai', Path(__file__).with_name('build-ai-search.py'))
ai = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ai)
pages = ai.discover()
english = [p for p in pages if p['lang'] == 'en']
lookup = {p['canonical']: p for p in pages}
assert len(pages) == 195 and len(english) == 65
assert len([p for p in english if p['route_group']['type'] == 'service-detail']) == 15

def schemas(page):
    return [node for s in page['schemas'] for node in s.get('@graph', [s])]

def fields(page):
    return [(n.tag, n.attrs.get('name'), n.attrs.get('type')) for n in page['tags'] if n.tag in ('input', 'select', 'textarea')]

for p in english:
    original = lookup[p['alternates']['pl']]
    assert next(n for n in p['tags'] if n.tag == 'html').attrs['data-lazar-enabled'] == 'false'
    assert p['meta']['og:locale'] == 'en_GB'
    assert p['meta']['og:title'] and p['meta']['twitter:title'] and p['meta']['description']
    crumbs = next(s for s in schemas(p) if s.get('@type') == 'BreadcrumbList')['itemListElement']
    assert crumbs[0]['item'] == ai.BASE + '/en/' and crumbs[-1]['item'] == p['canonical']
    for org in [s for s in schemas(p) if s.get('@type') == 'LocalBusiness']:
        source = next(s for s in schemas(original) if s.get('@type') == 'LocalBusiness')
        assert {k:v for k,v in org.items() if k != 'description'} == {k:v for k,v in source.items() if k != 'description'}
    for node in p['tags']:
        if node.tag == 'a' and node.attrs.get('href', '').startswith('/en/'):
            assert ai.BASE + node.attrs['href'].split('#')[0] in lookup, node.attrs
    assert p['alternates'] == site_locales.expected_alternates(p['canonical'])
    assert fields(p) == fields(original), p['canonical']
    if p['route_group']['type'] == 'service-detail':
        service = next(s for s in schemas(p) if s.get('@type') == 'Service')
        assert service['provider']['@id'] == ai.BASE + '/#organization'
        assert service['url'] == p['canonical']
        faq = next(s for s in schemas(p) if s.get('@type') == 'FAQPage')['mainEntity']
        questions = [n for n in p['tags'] if n.has('faq__question')]
        assert len(faq) == len(questions) == len([n for n in original['tags'] if n.has('faq__question')])
        inputs = {n.attrs['name']:n.attrs.get('value') for n in p['tags'] if n.tag == 'input' and 'name' in n.attrs}
        source_inputs = {n.attrs['name']:n.attrs.get('value') for n in original['tags'] if n.tag == 'input' and 'name' in n.attrs}
        assert inputs['language'] == 'en' and inputs['source'].startswith('en-')
        assert inputs['serviceType'] == source_inputs['serviceType']
        assert not any(n.tag == 'article' and not n.text() for n in p['tags'])
        for n in p['tags']:
            if n.has('service-cases-grid'):
                assert any(c.tag in ('article', 'figure') for c in n.all()), p['canonical']
        nav = next(n for n in p['tags'] if n.attrs.get('id') == 'primaryNavigation')
        assert '(Polish)' not in nav.text()

services = lookup[ai.BASE + '/en/services/']
catalog = json.loads((ai.ROOT / 'ai-catalog.json').read_text())
assert catalog['languages'] == ['pl', 'ru', 'en']
assert len(catalog['services']) == 15
for record in catalog['services']:
    assert set(record['localizations']) == {'pl', 'ru', 'en'}
    source, en = record['localizations']['pl'], record['localizations']['en']
    url = en['url'].removeprefix(ai.BASE)
    link = next(n for n in services['tags'] if n.tag == 'a' and n.attrs.get('href') == url)
    assert 'Polish' not in link.text()
    price = source['starting_price']
    if price:
        assert en['starting_price']['amount'] == convert(str(price['amount']))
        assert en['starting_price']['currency'] == 'EUR'
    else:
        assert en['starting_price'] is None
    assert len(en['available_work']) == len(source['available_work']) > 0
    label = 'from EUR ' + format(convert(str(price['amount'])), ',') if price else 'quoted individually after diagnostics'
    assert label in link.parent.text(), url
assert 'On-Site Equipment Service' not in lookup[ai.BASE+'/en/']['source']
assert 'Ship Equipment for Repair in Poland' not in lookup[ai.BASE+'/en/']['source']
assert '/en/international-service/' not in lookup[ai.BASE+'/en/']['source']
print('PASS: 195 pages / 65 EN, reciprocal SEO, 15 service prices/scopes, FAQ, form contracts, no planned links, chat gated')

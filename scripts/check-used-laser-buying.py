#!/usr/bin/env python3
"""Validate the bilingual used-laser buying guide and its integration."""
from site_locales import expected_alternates
import importlib.util
import json
import math
from pathlib import Path
import re
import xml.etree.ElementTree as ET
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('ai', ROOT / 'scripts/build-ai-search.py')
ai = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ai)
ROUTES = {'pl': '/blog/jak-kupic-uzywany-laser-do-depilacji/',
          'ru': '/ru/blog/kak-kupit-bu-lazer-dlya-epilyacii/'}
report = {}
for lang, route in ROUTES.items():
    source = (ROOT / route.lstrip('/') / 'index.html').read_text()
    tree = ai.Parser(source).root
    main = next(tree.all('main'))
    article = next(n for n in main.all() if n.has('article-content'))
    words = len(re.findall(r'\b\w+\b', article.text()))
    assert 2000 <= words <= 2800, (lang, words)
    assert len(list(main.all('h1'))) == 1
    assert len([n for n in main.all('details') if n.has('article-faq')]) == 9
    assert len(list(main.all('summary'))) == 9
    assert all(list(n.all('p')) for n in main.all('details'))
    assert len(list(main.all('ol'))) == 1
    assert len(list(next(main.all('ol')).all('li'))) == 14
    assert not list(main.all('form')), 'No new form contracts'
    for amount in ['25 000', '12 000', '55 000', '5 000', '37 000', '60 000', '23 000']:
        assert amount in article.text(), amount
    assert any(n.attrs.get('href') == 'https://ltsmarket.pl/' for n in article.all('a'))
    for a in article.all('a'):
        href = a.attrs.get('href', '')
        if href.startswith('/'):
            assert href.startswith('/ru/') == (lang == 'ru'), (route, href)
    scripts = [json.loads(s) for s in ai.SCHEMA_RE.findall(source)]
    assert {s['@type'] for s in scripts} == {'BlogPosting', 'BreadcrumbList'}
    post = next(s for s in scripts if s['@type'] == 'BlogPosting')
    assert post['headline'] == next(main.all('h1')).text()
    assert post['mainEntityOfPage']['@id'] == ai.BASE + route
    assert post['author']['@id'] == ai.ORG
    assert post['dateModified'] == '2026-10-12'
    expected = expected_alternates(ai.BASE + route)
    assert {n.attrs['hreflang']: n.attrs['href'] for n in tree.all('link') if 'hreflang' in n.attrs} == expected
    assert [n.attrs['href'] for n in tree.all('link') if n.attrs.get('rel') == 'canonical'] == [ai.BASE + route]
    images = list(main.all('img'))
    assert len(images) == 2
    for i, img in enumerate(images):
        assert img.attrs['alt'] and img.attrs['decoding'] == 'async'
        assert img.attrs['loading'] == ('eager' if i == 0 else 'lazy')
        if i == 0:
            assert img.attrs['fetchpriority'] == 'high'
        with Image.open(ROOT / img.attrs['src'].lstrip('/')) as picture:
            assert picture.size == (int(img.attrs['width']), int(img.attrs['height']))
            assert picture.format == 'WEBP'
        for item in img.attrs['srcset'].split(','):
            path, width = item.split()
            with Image.open(ROOT / path.lstrip('/')) as picture:
                assert picture.width == int(width[:-1])
    prefix = '/ru' if lang == 'ru' else ''
    index = ai.Parser((ROOT / (prefix + '/blog/').lstrip('/') / 'index.html').read_text()).root
    cards = [n for n in index.all('article') if n.has('blog-card')]
    matching = [c for c in cards if any(n.attrs.get('href') == route for n in c.all('a'))]
    assert len(matching) == 1, route
    card = matching[0]
    assert not list(card.all('img')), 'Blog cards remain text-only'
    assert all(any(n.has('blog-card__reading-time') for n in c.all()) for c in cards)
    reading = next(n.text() for n in card.all() if n.has('blog-card__reading-time'))
    assert str(math.ceil(words / 200)) in reading
    report[lang] = {'words': words, 'faq': 9, 'checklist': 14, 'responsive_images': len(images), 'cards': len(cards)}
urls = [e.text for e in ET.parse(ROOT / 'sitemap.xml').findall('s:url/s:loc', ai.NS)]
assert len(urls) == len(set(urls))
assert all(urls.count(ai.BASE + route) == 1 for route in ROUTES.values())
print(json.dumps({'result': 'passed', 'pages': report}, ensure_ascii=False, indent=2))

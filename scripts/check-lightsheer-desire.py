#!/usr/bin/env python3
"""Verify the bilingual LightSheer repair and technical guide, including assets."""
from site_locales import expected_alternates
import importlib.util
import json
import math
from pathlib import Path
import re
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('ai', ROOT / 'scripts/build-ai-search.py')
ai = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ai)
ROUTES = {
    ('case', 'pl'): '/realizacje/naprawa-lumenis-lightsheer-desire-olesnica/',
    ('case', 'ru'): '/ru/realizacje/remont-lumenis-lightsheer-desire-olesnica/',
    ('blog', 'pl'): '/blog/lightsheer-desire-chlodzenie-niezawodnosc/',
    ('blog', 'ru'): '/ru/blog/lightsheer-desire-ohlazhdenie-nadezhnost/',
}
pages = {p['canonical']: p for p in ai.discover()}
seen_assets = set()
paragraphs = {}
counts = {}
for (kind, lang), route in ROUTES.items():
    page = pages[ai.BASE + route]
    tree = page['tree']
    main = next(tree.all('main'))
    assert len(list(main.all('h1'))) == 1
    assert '{{' not in page['source']
    counterpart = ROUTES[kind, 'ru' if lang == 'pl' else 'pl']
    assert any(n.attrs.get('href') == counterpart for n in tree.all('a')), 'Language switcher'
    expected_alt = expected_alternates(ai.BASE + route)
    assert page['alternates'] == expected_alt
    linked = ROUTES['blog' if kind == 'case' else 'case', lang]
    assert any(n.attrs.get('href') == linked for n in main.all('a'))
    for n in main.all('a'):
        url = n.attrs.get('href', '')
        if url.startswith('/') and not url.startswith('/img/'):
            assert url.startswith('/ru/') == (lang == 'ru'), url
    schemas = page['schemas']
    assert {s['@type'] for s in schemas} == {'Article' if kind == 'case' else 'BlogPosting', 'BreadcrumbList'}
    article = next(s for s in schemas if s['@type'] in ('Article', 'BlogPosting'))
    assert article['headline'] == next(main.all('h1')).text()
    assert article['author']['@id'] == ai.ORG
    assert article['dateModified'] == '2026-10-14'
    assert 'datePublished' not in article, 'No invented deployment date'
    images = list(main.all('img'))
    assert len(images) == (10 if kind == 'case' else 3)
    assert len({n.attrs['src'] for n in images}) == len(images)
    assert any('zanieczyszczony-filtr-siatkowy' in n.attrs['src'] for n in images)
    for i, n in enumerate(images):
        assert n.attrs['alt'] and n.attrs['sizes']
        assert n.attrs['loading'] == ('eager' if i == 0 else 'lazy')
        if i == 0:
            assert n.attrs['fetchpriority'] == 'high'
        with Image.open(ROOT / n.attrs['src'].lstrip('/')) as im:
            assert im.size == (int(n.attrs['width']), int(n.attrs['height']))
            assert im.format == 'WEBP'
            assert not any(k in im.info for k in ('exif', 'xmp'))
        for entry in n.attrs['srcset'].split(','):
            url, width = entry.split()
            seen_assets.add(url)
            with Image.open(ROOT / url.lstrip('/')) as im:
                assert im.width == int(width[:-1])
    paragraphs[kind, lang] = {p.text() for p in main.all('p') if len(p.text()) > 160}
    index_route = ('/ru' if lang == 'ru' else '') + ('/realizacje/' if kind == 'case' else '/blog/')
    cards = [n for n in pages[ai.BASE + index_route]['tree'].all('article') if n.has('realizacja-card' if kind == 'case' else 'blog-card')]
    matching = [c for c in cards if any(n.attrs.get('href') == route for n in c.all('a'))]
    assert len(matching) == 1
    card = matching[0]
    if kind == 'blog':
        assert not list(card.all('img'))
        content = next(n for n in main.all() if n.has('article-content'))
        words = len(re.findall(r'\b\w+\b', content.text()))
        assert 1400 <= words <= 2000, words
        assert str(math.ceil(words / 200)) in next(n.text() for n in card.all() if n.has('blog-card__reading-time'))
        assert 'HIT' in content.text() and 'ChillTip' in content.text() and '805' in content.text()
    else:
        words = len(re.findall(r'\b\w+\b', main.text()))
        assert len(list(next(main.all('ol')).all('li'))) == 10
        assert len(list(card.all('img'))) == 1
        assert 'O-ring' in main.text()
    counts[kind + '-' + lang] = {'words': words, 'images': len(images)}
for lang in ('pl', 'ru'):
    assert not (paragraphs['case', lang] & paragraphs['blog', lang]), 'Distinct case and guide'
actual = {'/' + str(p.relative_to(ROOT)) for p in (ROOT / 'img/realizacje/lightsheer-desire-olesnica').glob('*.webp')}
assert len(actual) == 30 and actual == seen_assets, 'All responsive assets are used'
print(json.dumps({'result': 'passed', 'pages': counts, 'responsive_assets': len(actual)}, ensure_ascii=False, indent=2))

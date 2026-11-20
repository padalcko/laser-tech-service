#!/usr/bin/env python3
"""Scoped QA for supplied Zielona Gora texts, routes, photos and SEO."""
from pathlib import Path
import importlib.util
import json
import re
import xml.etree.ElementTree as ET
from html import unescape

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('markup', ROOT / 'scripts/build-case-layout.py')
markup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(markup)
texts = json.loads((ROOT / 'content/zielona-gora-texts.json').read_text())
photos = json.loads((ROOT / 'content/zielona-gora-images.json').read_text())
registry = json.loads((ROOT / 'scripts/site-locales.json').read_text())
base = registry['base_url']
groups = [g for g in registry['pages'] if g['id'] in (
    'realizacje:naprawa-lasera-diodowego-zielona-gora',
    'blog:laser-nie-dziala-czujnik-przeplywu-wody')]
assert len(groups) == 2
norm = lambda s: re.sub(r'\s+', ' ', s).strip()
plain = lambda s: norm(s.replace('**', ''))
sitemap = ET.parse(ROOT / 'sitemap.xml')
urls = [n.text for n in sitemap.findall('{*}url/{*}loc')]
for group in groups:
    kind = 'case' if group['type'] == 'case-study' else 'blog'
    expected_alts = {('pl-PL' if l == 'pl' else l): base + r['url'] for l, r in group['routes'].items()}
    expected_alts['x-default'] = base + group['x_default']
    for lang, route in group['routes'].items():
        url = route['url']
        path = ROOT / url.lstrip('/') / 'index.html'
        source = path.read_text()
        tree = markup.Tree(source).root
        main = tree.all(tag='main')[0]
        d = texts[kind + '-' + lang]
        assert len(main.all(tag='h1')) == 1
        assert norm(main.all(tag='h1')[0].text()) == d['title']
        lead = main.all('case-hero__lead' if kind == 'case' else 'article-lead')[0]
        assert norm(lead.text()) == norm(d['lead'])
        expected = [plain(x) for sec in d['sections'] for x in [sec['heading'], *sec['paragraphs']]]
        # The supplied sections are followed only by related links and the shared CTA.
        candidates = [n for n in main.all() if n.tag in ('h2', 'p') and not n.has('case-hero__lead') and not n.has('article-lead')]
        actual = [norm(n.text()) for n in candidates[:len(expected)]]
        assert actual == expected, (url, [(a,b) for a,b in zip(actual,expected) if a != b])
        assert tree.all(tag='title')[0].text() == d['seo_title']
        meta = {n.attrs.get('name', n.attrs.get('property')): n.attrs.get('content') for n in tree.all(tag='meta')}
        assert meta['description'] == d['description']
        assert 'noindex' not in meta.get('robots', '')
        links = tree.all(tag='link')
        assert [n.attrs['href'] for n in links if n.attrs.get('rel') == 'canonical'] == [base+url]
        assert {n.attrs['hreflang']:n.attrs['href'] for n in links if 'hreflang' in n.attrs} == expected_alts
        switcher = tree.all('language-switcher')[0]
        assert {n.attrs['lang']:n.attrs['href'] for n in switcher.all(tag='a')} == {l:r['url'] for l,r in group['routes'].items()}
        schemas = [json.loads(n.text()) for n in tree.all(tag='script') if n.attrs.get('type') == 'application/ld+json']
        article = next(s for s in schemas if s.get('@type') in ('Article','BlogPosting'))
        assert article['headline'] == d['title'] and article['description'] == d['description']
        assert article['inLanguage'] == lang and article['mainEntityOfPage']['@id'] == base + url
        assert article['datePublished'] == article['dateModified'] == '2026-11-20'
        assert article['contentLocation']['name'] == 'Zielona Góra'
        assert any(s.get('@type') == 'BreadcrumbList' for s in schemas)
        assert not any(s.get('@type') == 'FAQPage' for s in schemas)
        assert urls.count(base+url) == 1
        assert meta['og:url'] == base+url
        assert meta['og:image'] == meta['twitter:image'] == base+photos['8507' if kind == 'case' else '8513']['src']
        images = main.all(tag='img')
        assert len(images) == (16 if kind == 'case' else 5)
        assert images[0].attrs['loading'] == 'eager' and images[0].attrs['fetchpriority'] == 'high'
        for image in images:
            a = image.attrs
            assert a['alt'] and int(a['width']) > 0 and int(a['height']) > 0
            assert (ROOT/a['src'].lstrip('/')).is_file()
        assert all(im.attrs['loading'] == 'lazy' for im in images[1:])
        if kind == 'case':
            assert all('object-fit' not in im.attrs.get('style', '') for im in images), 'Use Pharaon image styles without overrides'
            gallery = main.all('case-gallery')[0]
            assert {n.attrs['src'] for n in gallery.all(tag='img')} == {p['src'] for p in photos.values()}
        for link in main.all(tag='a'):
            href = link.attrs.get('href','').split('#')[0]
            if href.startswith('/'):
                target = ROOT/href.lstrip('/')
                assert (target/'index.html').is_file() if href.endswith('/') else target.is_file(), (url, href)
        assert 'Gliwice' not in source and 'Гливице' not in source and '808 nm' not in source
        print('PASS', url)
for photo in photos.values():
    for variant in photo['variants']:
        assert (ROOT / variant['src'].lstrip('/')).stat().st_size == variant['bytes']
print('PASS: six exact supplied texts, SEO/schema, reciprocal hreflang, links, galleries, 60 image assets')

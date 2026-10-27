#!/usr/bin/env python3
"""Check the Wrocław cooling case and downtime guide against the publication contract."""
import importlib.util
import json
import re
import subprocess
from pathlib import Path
import site_locales as locales

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('ai', ROOT / 'scripts/build-ai-search.py')
ai = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ai)
registry = locales.load()
groups = [g for g in registry['pages'] if g['id'] in (
    'realizacje:naprawa-chlodzenia-lightsheer-desire-wroclaw',
    'blog:laser-po-roku-przestoju-uklad-chlodzenia')]
assert len(groups) == 2
pages = {p['canonical']: p for p in ai.discover()}
audit = json.loads((ROOT / 'img/realizacje/lightsheer-desire-wroclaw/image-audit.json').read_text())
assert len(audit) == 10
assets = {f['path']: f for photo in audit for f in photo['files']}
assert len(assets) == 30
for path, facts in assets.items():
    raw = (ROOT / path.lstrip('/')).read_bytes()
    assert raw[:4] == b'RIFF' and raw[8:12] == b'WEBP'
    assert len(raw) == facts['bytes']
    # WebP container chunks: the exports must not carry EXIF or XMP metadata.
    offset = 12
    while offset + 8 <= len(raw):
        name = raw[offset:offset+4]
        assert name not in (b'EXIF', b'XMP ')
        size = int.from_bytes(raw[offset+4:offset+8], 'little')
        offset += 8 + size + size % 2
for group in groups:
    kind = 'case' if group['type'] == 'case-study' else 'blog'
    peer = next(g for g in groups if g is not group)
    for lang, route in locales.published(group).items():
        p = pages[ai.BASE + route]
        main = next(p['tree'].all('main'))
        assert len(list(main.all('h1'))) == 1
        assert p['alternates'] == locales.alternates(group, ai.BASE)
        assert set(p['alternates']) == {'pl', 'ru', 'en', 'x-default'}
        schema = next(s for s in p['schemas'] if s['@type'] in ('Article', 'BlogPosting'))
        assert schema['headline'] == next(main.all('h1')).text()
        assert schema['datePublished'] == schema['dateModified'] == '2026-10-27'
        assert len([s for s in p['schemas'] if s['@type'] == 'BreadcrumbList']) == 1
        assert not any(s['@type'] == 'FAQPage' for s in p['schemas'])
        assert any(a.attrs.get('href') == locales.published(peer)[lang] for a in main.all('a'))
        assert 'ET BP over temperature' in main.text()
        for old in ('Oleśnica', 'Олесниц', 'PLN 200,000', 'O-ring', 'ChillTip'):
            assert old not in main.text(), (route, old)
        if lang == 'pl':
            for keyword in ('serwis laserów', 'regeneracja laserów', 'naprawa laserów'):
                assert keyword in main.text().lower()
        images = list(main.all('img'))
        assert len(images) == (10 if kind == 'case' else 4)
        assert len({i.attrs['src'] for i in images}) == len(images)
        for i, node in enumerate(images):
            f = assets[node.attrs['src']]
            assert node.attrs['width'] == str(f['width']) and node.attrs['height'] == str(f['height'])
            assert node.attrs['alt'] and node.attrs['sizes']
            assert node.attrs['loading'] == ('eager' if i == 0 else 'lazy')
            for item in node.attrs['srcset'].split(','):
                url, width = item.split()
                assert assets[url]['width'] == int(width[:-1])
        if kind == 'case':
            assert len(list(next(main.all('ol')).all('li'))) == 10
        else:
            assert len(list(main.all('h2'))) >= 6
            assert '1–2' in main.text()
        hub = route.rsplit('/', 2)[0] + '/'
        cards = [n for n in pages[ai.BASE + hub]['tree'].all('article') if n.has('realizacja-card' if kind == 'case' else 'blog-card')]
        matching = [n for n in cards if any(a.attrs.get('href') == route for a in n.all('a'))]
        assert len(matching) == 1
        assert len(list(matching[0].all('img'))) == (1 if kind == 'case' else 0)
        assert '/js/main.js' in p['source']
# Shared design, business integrations and partner pages are outside this task.
changed = subprocess.check_output(['git', 'diff', '--name-only'], cwd=ROOT, text=True).splitlines()
assert not any(p.startswith(('css/', 'js/', 'partnerzy/', 'ru/partnerzy/', 'en/partners/')) for p in changed)
print('PASS: six pages, 30 assets, ten repair steps, three-language SEO, reciprocal links, six cards and unchanged shared design/integrations')

#!/usr/bin/env python3
"""Validate partner order, links, generated markup and unchanged page boundaries."""
import importlib.util
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('partners', ROOT / 'scripts/build-partners.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)
data = builder.load()
assert not builder.build(check=True)
ordered = sorted(data['partners'], key=lambda p: p['priority'], reverse=True)
assert [p['id'] for p in ordered] == ['lts-market', 'annvi', 'magia-kosmetyczna', 'cuprum-laser-tech', 'cuprum-beauty-lab', 'lumine']
for lang, filename in data['pages'].items():
    source = (ROOT / filename).read_text()
    cards = re.findall(r'<a class="partner-card".*?</a>', source, re.S)
    assert len(cards) == len(ordered)
    assert cards == [builder.render(p, lang).lstrip() for p in ordered]
    first = cards[0]
    assert 'href="https://ltsmarket.pl/"' in first
    assert 'target="_blank" rel="noopener noreferrer"' in first
    assert 'nofollow' not in first and 'ltsmarket.eu' not in first
    assert '+48 575 254 431' in first and 'sales@ltsmarket.pl' in first
    assert first.count('<a ') == 1, 'No nested anchors'
    for image in re.findall(r'<img .*?/>', first, re.S):
        assert 'width="402" height="402"' in image
        assert 'loading="lazy" decoding="async"' in image
        for path in re.findall(r'/img/[^\s"]+\.webp', image):
            raw = (ROOT / path.lstrip('/')).read_bytes()
            assert raw[:4] == b'RIFF' and raw[8:12] == b'WEBP'
    for schema in re.findall(r'<script type="application/ld\+json">(.*?)</script>', source, re.S):
        json.loads(schema)
    # Compare the existing cards and all non-grid HTML against the baseline commit.
    previous = subprocess.check_output(['git', 'show', 'HEAD:' + filename], cwd=ROOT, text=True)
    if 'href="https://ltsmarket.pl/"' not in '\n'.join(re.findall(r'<a class="partner-card".*?</a>', previous, re.S)):
        assert re.findall(r'<a class="partner-card".*?</a>', previous, re.S) == cards[1:]
        assert builder.BLOCK.sub('GRID', previous) == builder.BLOCK.sub('GRID', source)
# Changing priority must be detected in every locale without writing any HTML.
snapshots = {p: (ROOT / p).read_bytes() for p in data['pages'].values()}
original_load = builder.load
market = next(p for p in data['partners'] if p['id'] == 'lts-market')
market['priority'] = -1
builder.load = lambda: data
assert set(builder.build(check=True)) == set(data['pages'].values())
builder.load = original_load
assert all((ROOT / p).read_bytes() == raw for p, raw in snapshots.items())
assert not builder.build(check=True)
print('PASS: three localized pages, priority mutation/read-only checks, six cards each, official links, contacts, WebP, schema and preserved existing markup')

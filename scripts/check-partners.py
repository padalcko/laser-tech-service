#!/usr/bin/env python3
"""Check generated partner gallery, localized details and accessible controls."""
import importlib.util
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('partners', ROOT / 'scripts/build-partners.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)
data = builder.load()
assert not builder.build(check=True)
ordered = sorted(data['partners'], key=lambda p: p['priority'], reverse=True)
for lang, filename in data['pages'].items():
    source = (ROOT / filename).read_text()
    cards = re.findall(r'<article class="partner-card".*?</article>', source, re.S)
    assert cards == [builder.render(p, lang).lstrip() for p in ordered]
    assert source.count('<dialog ') == 1
    assert source.count('src="/js/partners.js"') == 1
    assert source.count('data-filter=') == 4
    for partner, card in zip(ordered, cards):
        button = re.search(r'<button .*?</button>', card, re.S)[0]
        assert '<a ' not in button
        assert 'aria-haspopup="dialog"' in button
        assert partner['content'][lang]['image_html'] in card
        for text in partner['content'][lang]['descriptions_html']:
            assert text in card
        if partner.get('phone'):
            assert f'href="tel:{partner["phone"]}"' in card
        for image in re.findall(r'<img .*?/>', card, re.S):
            assert 'alt="' in image and 'width="' in image and 'height="' in image
            for path in re.findall(r'/img/[^\s"]+\.webp', image):
                assert (ROOT / path.lstrip('/')).is_file()
    for label in builder.LABELS[lang][:5]:
        assert label in source
print(f'PASS: {len(ordered)} partners in PL/RU/EN, order, original content, images, contacts and dialog markup')

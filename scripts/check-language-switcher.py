#!/usr/bin/env python3
"""Validate generated dropdowns and publication gating, without writing HTML."""
import copy
import importlib.util
from pathlib import Path
import site_locales as locales

spec = importlib.util.spec_from_file_location('switcher', Path(__file__).with_name('build-language-switcher.py'))
switcher = importlib.util.module_from_spec(spec)
spec.loader.exec_module(switcher)
registry = locales.load()
count = 0
for group in registry['pages']:
    for lang, url in locales.published(group).items():
        source = (locales.ROOT / url.lstrip('/') / 'index.html').read_text()
        components = switcher.PATTERN.findall(source)
        assert components == [switcher.render(group, lang, registry['languages'])], url
        for peer, route in group['routes'].items():
            if route['status'] == 'planned':
                assert route['url'] not in components[0], url
        count += 1
# Prove EN appears only when published; preserve per-page counterpart and native names.
group = copy.deepcopy(next(g for g in registry['pages'] if g['type'] == 'service-detail'))
group['routes']['en']['status'] = 'planned'
assert 'English</a>' not in switcher.render(group, 'pl', registry['languages'])
group['routes']['en']['status'] = 'published'
rendered = switcher.render(group, 'en', registry['languages'])
assert 'English</a>' in rendered and f'href="{group["routes"]["en"]["url"]}"' in rendered
assert '<span>EN</span>' in rendered and 'language-switcher__globe' in rendered and 'aria-current="page">English' in rendered
print(f'PASS: {count} published dropdowns, EN publication gate and native language labels')

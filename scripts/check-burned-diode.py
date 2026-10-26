#!/usr/bin/env python3
"""Check the three-language burned-diode case and article, including regional SEO tags."""
import importlib.util
import json
import re
from pathlib import Path
import site_locales as locales
spec = importlib.util.spec_from_file_location('ai', Path(__file__).with_name('build-ai-search.py'))
ai = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ai)
registry = locales.load()
groups = [g for g in registry['pages'] if g['id'] in (
    'realizacje:wymiana-spalonej-diody-laserowej',
    'blog:spalona-dioda-laserowa-naprawa-glowicy')]
assert len(groups) == 2
pages = {p['canonical']: p for p in ai.discover()}
for g in groups:
    expected = locales.alternates(g, ai.BASE)
    assert set(expected) == {'pl-PL', 'ru-RU', 'en', 'x-default'}
    for lang, url in locales.published(g).items():
        p = pages[ai.BASE + url]
        assert p['alternates'] == expected
        assert len([n for n in p['tags'] if n.tag == 'h1']) == 1
        md = p['path'].with_suffix('.md').read_text()
        for peer in locales.published(g).values():
            assert ai.BASE + peer in md
        hub = '/' + '/'.join(url.strip('/').split('/')[:-1]) + '/'
        hub_source = (ai.ROOT / hub.lstrip('/') / 'index.html').read_text()
        cards = re.findall(r'<article class="(?:blog-card|realizacja-card)".*?</article>', hub_source, re.S)
        card = [s for s in cards if f'href="{url}"' in s]
        assert len(card) == 1
        if g['type'] == 'article':
            assert '<img' not in card[0]
        else:
            assert 'serwis-laserow-wymiana-diody-laserowej.webp' in card[0]
            assert 'object-fit: contain' not in card[0]
        main = re.search(r'<main\b.*?</main>', p['source'], re.S).group()
        image_tags = list(ai.Parser(main).root.all('img'))
        assert len({n.attrs['src'] for n in image_tags}) == (2 if g['type']=='article' else 4)
        for n in image_tags:
            assert n.attrs['width']=='864' and n.attrs['height']=='1536'
            assert n.attrs['alt'] and n.attrs['loading'] in ('eager','lazy')
            if g['type'] == 'article':
                assert 'object-fit: contain' in n.attrs['style']
            else:
                assert 'object-fit: contain' not in n.attrs.get('style', '')
        schemas = [x for x in p['schemas'] if x.get('@type') in ('Article','BlogPosting')]
        assert len(schemas)==1 and schemas[0]['headline']==p['title']
        assert not any(x in main for x in ('LightSheer','ESTETECH','Oleśnica','Poznań'))
# Optional regional labels must not change legacy groups.
legacy = next(g for g in registry['pages'] if g['id']=='home')
assert set(locales.alternates(legacy, ai.BASE))=={'pl','ru','en','x-default'}
print('PASS: six pages, regional hreflang, Markdown peers, six cards, schemas, shared images and legacy locale contract')

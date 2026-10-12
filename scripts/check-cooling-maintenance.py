from pathlib import Path
from urllib.parse import urlsplit
from urllib.robotparser import RobotFileParser
import importlib.util
import json
import re
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
BASE = 'https://lasertechservice.pl'
ORGANIZATION = BASE + '/#organization'
CASES = {
    'pl': '/realizacje/wymiana-wentylatorow-chlodzenia-lasera-wroclaw/',
    'ru': '/ru/realizacje/zamena-ventilyatorov-ohlazhdeniya-lazera-vrotslav/'
}
ARTICLES = {
    'pl': '/blog/czyszczenie-ukladu-chlodzenia-lasera-wentylatory-przegrzanie/',
    'ru': '/ru/blog/ochistka-sistemy-ohlazhdeniya-lazera-ventilyatory-peregrev/'
}
SPEC = importlib.util.spec_from_file_location('ai_search', ROOT / 'scripts/build-ai-search.py')
AI = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AI)
SITEMAP = ET.parse(ROOT / 'sitemap.xml')
NAMESPACES = {
    's': 'http://www.sitemaps.org/schemas/sitemap/0.9',
    'x': 'http://www.w3.org/1999/xhtml'
}
ROBOTS = RobotFileParser()
ROBOTS.parse((ROOT / 'robots.txt').read_text().splitlines())
TITLES = set()
DESCRIPTIONS = set()
COUNTS = {'pages': 0, 'responsive_images': 0, 'faq_answers': 0, 'local_links': 0}
PARAGRAPHS = {}

def local_target(url):
    parsed = urlsplit(url)
    if parsed.scheme and (parsed.scheme not in ('http', 'https') or parsed.netloc != 'lasertechservice.pl'):
        return None
    if not parsed.path.startswith('/'):
        return None
    target = ROOT / parsed.path.lstrip('/')
    return target / 'index.html' if target.is_dir() else target

for kind, routes in [('case', CASES), ('article', ARTICLES)]:
    for language, route in routes.items():
        canonical = BASE + route
        page_path = ROOT / route.lstrip('/') / 'index.html'
        source = page_path.read_text()
        tree = AI.Parser(source).root
        nodes = list(tree.all())
        assert next(tree.all('html')).attrs['lang'] == language, route
        assert len(list(tree.all('h1'))) == 1, route
        title = next(tree.all('title')).text()
        assert title and title not in TITLES, route
        TITLES.add(title)
        metadata = {node.attrs.get('name', node.attrs.get('property')): node.attrs.get('content') for node in tree.all('meta')}
        description = metadata['description']
        assert description and description not in DESCRIPTIONS, route
        DESCRIPTIONS.add(description)
        assert 'noindex' not in metadata['robots'], route
        assert metadata['og:url'] == canonical, route
        assert metadata['og:title'] == metadata['twitter:title'] == title, route
        assert metadata['og:description'] == metadata['twitter:description'] == description, route
        assert metadata['twitter:card'] == 'summary_large_image', route
        assert metadata['og:image'] == metadata['twitter:image'], route
        assert local_target(metadata['og:image']).is_file(), route
        assert metadata['og:image:alt'] == metadata['twitter:image:alt'], route
        links = list(tree.all('link'))
        assert [node.attrs['href'] for node in links if node.attrs.get('rel') == 'canonical'] == [canonical], route
        alternates = {node.attrs['hreflang']: node.attrs['href'] for node in links if 'hreflang' in node.attrs}
        expected = {'pl': BASE + routes['pl'], 'ru': BASE + routes['ru'], 'x-default': BASE + routes['pl']}
        assert alternates == expected, route
        switcher = next(node for node in tree.all('div') if node.has('language-switcher'))
        assert {node.attrs.get('hreflang'): node.attrs['href'] for node in switcher.all('a')} == routes, route
        entries = [entry for entry in SITEMAP.findall('s:url', NAMESPACES) if entry.find('s:loc', NAMESPACES).text == canonical]
        assert len(entries) == 1, route
        assert {node.attrib['hreflang']: node.attrib['href'] for node in entries[0].findall('x:link', NAMESPACES)} == expected, route
        schemas = [json.loads(raw) for raw in AI.SCHEMA_RE.findall(source)]
        assert len(schemas) == 2, route
        article_schema, breadcrumb_schema = schemas
        assert article_schema['@type'] == ('Article' if kind == 'case' else 'BlogPosting'), route
        assert article_schema['headline'] == next(tree.all('h1')).text(), route
        assert article_schema['description'] == description, route
        assert article_schema['mainEntityOfPage']['@id'] == canonical, route
        assert article_schema['author'] == article_schema['publisher'] == {'@id': ORGANIZATION}, route
        assert article_schema['dateModified'] == '2026-10-12', route
        assert 'datePublished' not in article_schema, route
        assert article_schema['inLanguage'] == ('pl-PL' if language == 'pl' else 'ru-RU'), route
        assert breadcrumb_schema['@type'] == 'BreadcrumbList', route
        assert [item['position'] for item in breadcrumb_schema['itemListElement']] == [1, 2, 3], route
        assert breadcrumb_schema['itemListElement'][-1]['item'] == canonical, route
        main = next(tree.all('main'))
        photos = list(main.all('img'))
        assert len(photos) == (4 if kind == 'case' else 2), route
        assert len({photo.attrs['alt'] for photo in photos}) == len(photos), route
        for position, photo in enumerate(photos):
            attributes = photo.attrs
            assert attributes['alt'] and int(attributes['width']) > 0 and int(attributes['height']) > 0, route
            assert attributes['sizes'] and attributes['decoding'] == 'async', route
            variants = [entry.strip().split() for entry in attributes['srcset'].split(',')]
            assert len(variants) == 3, route
            for url, descriptor in variants:
                assert local_target(url).is_file() and descriptor.endswith('w'), url
            if position == 0:
                assert attributes['loading'] == 'eager' and attributes['fetchpriority'] == 'high', route
            else:
                assert attributes['loading'] == 'lazy', route
            assert 'height: auto' in attributes['style'], route
            COUNTS['responsive_images'] += 1
        for node in nodes:
            for attribute in ('href', 'src'):
                url = node.attrs.get(attribute)
                if not url:
                    continue
                target = local_target(url)
                if target is not None:
                    assert target.is_file(), (route, url)
                    COUNTS['local_links'] += 1
        for agent in ('Googlebot', 'Bingbot', 'OAI-SearchBot', 'ChatGPT-User', 'PerplexityBot'):
            assert ROBOTS.can_fetch(agent, canonical), (agent, route)
        counterpart = ARTICLES[language] if kind == 'case' else CASES[language]
        assert any(node.attrs.get('href') == counterpart for node in main.all('a')), route
        service = '/ru/uslugi/' if language == 'ru' else '/uslugi/'
        assert any(node.attrs.get('href') == service for node in main.all('a')), route
        if kind == 'article':
            faq_title = 'Najczęstsze pytania' if language == 'pl' else 'Частые вопросы'
            faq = source.split(f'<h2>{faq_title}</h2>')[1].split('<h2>')[0]
            assert len(re.findall('<summary>', faq)) == len(re.findall('<p>', faq)) == 6, route
            for term in ('CFM', 'RPM', 'PWM', 'Pa', 'mmH₂O'):
                assert term in main.text(), (route, term)
            COUNTS['faq_answers'] += 6
        index_route = ('/ru' if language == 'ru' else '') + ('/realizacje/' if kind == 'case' else '/blog/')
        index = AI.Parser((ROOT / index_route.lstrip('/') / 'index.html').read_text()).root
        card_class = 'realizacja-card' if kind == 'case' else 'blog-card'
        card = next(node for node in index.all('article') if node.has(card_class))
        assert any(node.attrs.get('href') == route for node in card.all('a')), route
        if kind == 'case':
            assert 'Wrocław' in card.text() and len(list(card.all('img'))) == 1, route
        PARAGRAPHS[kind, language] = {node.text() for node in main.all('p') if len(node.text()) > 180}
        COUNTS['pages'] += 1

for language in ('pl', 'ru'):
    assert not (PARAGRAPHS['case', language] & PARAGRAPHS['article', language]), language

print(json.dumps({'result': 'passed', 'counts': COUNTS}, ensure_ascii=False, indent=2))

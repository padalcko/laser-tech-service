"""Shared route registry. HTML owns content; only published routes are discoverable."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TYPES = {'home', 'services', 'service-detail', 'pricing', 'blog', 'article',
         'case-studies', 'case-study', 'contact', 'partners'}


def load(path=None):
    data = json.loads((path or ROOT / 'scripts/site-locales.json').read_text())
    assert data['schema_version'] == 1
    assert data['base_url'] == 'https://lasertechservice.pl'
    ids, urls = set(), set()
    for group in data['pages']:
        assert group['id'] and group['id'] not in ids, 'Duplicate page ID'
        ids.add(group['id'])
        assert group['type'] in TYPES, group['id']
        assert group['routes'], group['id']
        for lang, route in group['routes'].items():
            assert lang in data['languages'], lang
            url = route['url']
            assert re.fullmatch(r'/(?:[a-z0-9-]+/)*', url), url
            assert (url.startswith('/' + lang + '/') if lang != 'pl'
                    else not url.startswith(tuple('/' + l + '/' for l in data['languages'] if l != 'pl'))), url
            assert url not in urls, 'Duplicate route: ' + url
            urls.add(url)
            assert route['status'] in ('planned', 'published'), url
        live = published(group)
        assert group['x_default'] is None or group['x_default'] in live.values(), group['id']
    return data


def published(group):
    return {lang: route['url'] for lang, route in group['routes'].items()
            if route['status'] == 'published'}


def index(data):
    return {route['url']: (group, lang, route['status'])
            for group in data['pages'] for lang, route in group['routes'].items()}


def alternates(group, base):
    result = {lang: base + url for lang, url in published(group).items()}
    if group['x_default'] is not None:
        result['x-default'] = base + group['x_default']
    return result


def resolve(routes, data):
    """Resolve legacy service-case route references; registry owns publication state."""
    lookup = index(data)
    groups = []
    for lang, url in routes.items():
        assert url in lookup, 'Unregistered case/service route: ' + url
        group, registered_lang, _ = lookup[url]
        assert registered_lang == lang, url
        groups.append(group)
    assert groups and all(g['id'] == groups[0]['id'] for g in groups), routes
    return groups[0]


def expected_alternates(url):
    """SEO contract for scoped legacy validators, independent of route spelling."""
    data = load()
    assert url.startswith(data['base_url'] + '/'), url
    group, _, status = index(data)[url.removeprefix(data['base_url'])]
    assert status == 'published', url
    return alternates(group, data['base_url'])

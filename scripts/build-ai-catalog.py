#!/usr/bin/env python3
"""Generate the custom AI catalog from sitemap-listed canonical HTML (stdlib only)."""
import argparse
import datetime as dt
import hashlib
import importlib.util
import json
import re
from pathlib import Path
from urllib.parse import urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('ai_search', ROOT / 'scripts/build-ai-search.py')
ai = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ai)
BASE = ai.BASE
TARGET = ROOT / 'ai-catalog.json'


def nodes(value):
    if isinstance(value, list):
        for item in value:
            yield from nodes(item)
    elif isinstance(value, dict):
        yield value
        for item in value.values():
            yield from nodes(item)


def schema(page, types):
    return next((n for n in nodes(page['schemas']) if n.get('@type') in types), {})


def identifier(kind, url):
    return kind + ':' + urlsplit(url).path.strip('/').replace('/', ':')


def body_nodes(page):
    main = next((n for n in page['tags'] if n.tag == 'main'), None)
    return list(main.all()) if main else []


def headings_content(page, pattern):
    """Only explicit body section headings; never nav/footer or arbitrary text."""
    result = []
    for heading in body_nodes(page):
        if heading.tag not in ('h2', 'h3') or not re.match(pattern, heading.text(), re.I):
            continue
        siblings = heading.parent.children
        for n in siblings[siblings.index(heading) + 1:]:
            if n.tag in ('h2', 'h3'):
                break
            if n.tag == 'p':
                result.append(n.text())
            elif n.tag in ('ul', 'ol'):
                result.extend(x.text() for x in n.all('li'))
    return list(dict.fromkeys(result))


def facts(page):
    out = {}
    for n in body_nodes(page):
        if n.has('case-info__item'):
            label = next((x.text() for x in n.all('span')), '')
            value = next((x.text() for x in n.all('strong')), '')
            if label and value:
                out[label.lower().strip(': ')] = value
    return out


def field(values, labels):
    return next((values[k] for k in labels if k in values), None)


def category(text):
    # Controlled equipment labels, only explicit terminology in the service heading.
    for regex, name in [(r'\bRF\b', 'RF'), (r'kri|кри', 'cryotherapy'),
                        (r'CO[₂2]', 'CO2'), (r'\bIPL\b', 'IPL'),
                        (r'diod|диод', 'diode_laser'), (r'elektronik|электроник', 'electronics'),
                        (r'głowic|головок|манипул', 'handpieces')]:
        if re.search(regex, text, re.I):
            return name
    return None


def price(page):
    values = [n.text() for n in body_nodes(page) if n.has('service-price')]
    if len(values) != 1:
        return None
    match = re.fullmatch(r'(?:od|от)\s+([\d\s]+(?:[.,]\d{1,2})?)\s*(?:zł|PLN)', values[0], re.I)
    if not match:
        return None
    amount = float(re.sub(r'\s+', '', match[1]).replace(',', '.'))
    # Preserve nearby qualifications: starting amount is not a complete repair quote.
    hero = next(n for n in body_nodes(page) if n.tag == 'header')
    return {'amount': int(amount) if amount.is_integer() else amount, 'currency': 'PLN',
            'type': 'starting_from', 'source_text': values[0],
            'conditions': [n.text() for n in hero.all('p') if n.has('price-note')],
            'source_url': page['canonical']}


def build(pages):
    lookup = {p['canonical']: p for p in pages}
    homepage = lookup[BASE + '/']
    org = schema(homepage, {'LocalBusiness'})
    business = {k: org[k] for k in ('name', 'url', 'telephone', 'email', 'address', 'areaServed', 'sameAs', 'description') if k in org}
    business['source_url'] = homepage['canonical']
    business['main_city'] = org.get('address', {}).get('addressLocality')
    service_pages = {p['canonical']: p for p in pages if p['kind'] == 'service' and schema(p, {'Service'}) and any(n.has('service-landing') for n in p['tags'])}
    services, service_ids, seen = [], {}, set()
    for url, p in sorted(service_pages.items()):
        if url in seen:
            continue
        pair = {p['lang']: p}
        for lang, alt in p['alternates'].items():
            if lang in ('pl', 'ru') and alt in service_pages and service_pages[alt]['lang'] == lang and service_pages[alt]['alternates'].get(p['lang']) == url:
                pair[lang] = service_pages[alt]
        primary = pair.get('pl', p)['canonical']
        sid = identifier('service', primary)
        record = {'id': sid, 'equipment_category': category(p['title']), 'primary_url': primary, 'localizations': {}}
        for lang, peer in sorted(pair.items()):
            seen.add(peer['canonical']); service_ids[peer['canonical']] = sid
            service = schema(peer, {'Service'})
            scope = next((n for n in body_nodes(peer) if n.tag == 'section' and any(x.tag == 'h2' and re.match(r'^(?:Co obejmuje|Zakres|Что входит)', x.text(), re.I) for x in n.all())), None)
            record['localizations'][lang] = {'name': peer['title'], 'description': service.get('description', peer['meta'].get('description', '')),
                'url': peer['canonical'], 'starting_price': price(peer),
                'available_work': [n.text() for n in scope.all('h3')] if scope else []}
        services.append(record)
    articles, cases = [], []
    for p in pages:
        if p['kind'] not in ('article', 'case'):
            continue
        meta = schema(p, {'Article', 'BlogPosting'})
        record = {'id': identifier(p['kind'], p['canonical']), 'title': p['title'], 'language': p['lang'],
                  'canonical_url': p['canonical'], 'description': meta.get('description', p['meta'].get('description', ''))}
        if p['kind'] == 'article':
            record['topics'] = meta.get('articleSection', meta.get('keywords', [])) or list(dict.fromkeys(n.text() for n in body_nodes(p) if n.has('article-category')))
            if isinstance(record['topics'], str):
                record['topics'] = [record['topics']]
            for key in ('datePublished', 'dateModified'):
                if meta.get(key):
                    record[key] = meta[key]
            links = {urljoin(p['canonical'], n.attrs.get('href', '')).split('#')[0] for n in body_nodes(p) if n.tag == 'a'}
            record['related_services'] = sorted({service_ids[u] for u in links if u in service_ids})
            articles.append(record)
        else:
            info = facts(p)
            about = meta.get('about', {})
            record.update(city=field(info, ['miasto', 'lokalizacja', 'город', 'место']),
                          equipment_type=field(info, ['urządzenie', 'typ urządzenia', 'оборудование', 'тип оборудования']),
                          equipment=about if about else None,
                          fault=headings_content(p, r'^(?:Problem|Objaw|Usterka|Неисправност|Проблем|Симптом)'),
                          performed_work=headings_content(p, r'^(?:Naprawa|Wykonane prace|Zakres (?:prac|naprawy)|Ремонт|Выполненные работы|Что (?:сделали|было сделано))'),
                          result=headings_content(p, r'^(?:Rezultat|Efekt|Wynik|Результат|Итог)'))
            if not record['fault']:
                fault = field(info, ['problem', 'usterka', 'проблема', 'неисправность'])
                record['fault'] = [fault] if fault else []
            cases.append(record)
    resources = {'sitemap': BASE + '/sitemap.xml', 'llms': BASE + '/llms.txt', 'llms_full': BASE + '/llms-full.txt',
                 'markdown': {p['canonical']: p['md'] for p in pages}}
    return {'schema_version': '1.0', 'catalog_type': 'business_content_catalog', 'business': business, 'languages': ['pl', 'ru'],
            'services': sorted(services, key=lambda x:x['id']), 'articles': sorted(articles, key=lambda x:x['id']),
            'case_studies': sorted(cases, key=lambda x:x['id']), 'resources': resources}


def validate(catalog, pages):
    published = {p['canonical']: p for p in pages}
    ids = [r['id'] for group in ('services', 'articles', 'case_studies') for r in catalog[group]]
    assert len(ids) == len(set(ids)), 'Duplicate IDs'
    for group in ('articles', 'case_studies'):
        expected = {p['canonical'] for p in pages if p['kind'] == ('article' if group == 'articles' else 'case')}
        assert {r['canonical_url'] for r in catalog[group]} == expected
        for r in catalog[group]:
            assert published[r['canonical_url']]['lang'] == r['language']
    for r in catalog['services']:
        for lang, loc in r['localizations'].items():
            assert published[loc['url']]['lang'] == lang
            assert loc['starting_price'] == price(published[loc['url']])
    def urls(value):
        if isinstance(value, dict):
            for k, v in value.items():
                yield from urls(k); yield from urls(v)
        elif isinstance(value, list):
            for v in value: yield from urls(v)
        elif isinstance(value, str) and re.match(r'https?://', value):
            yield value
    for url in urls(catalog):
        assert url.startswith('https://'), url
        if urlsplit(url).netloc == urlsplit(BASE).netloc:
            path = ROOT / urlsplit(url).path.lstrip('/')
            assert path.is_file() or (path / 'index.html').is_file(), url
    return True


def generate(check=False):
    pages = ai.discover()  # Fail closed on stale sitemap, missing HTML, noindex or canonical mismatch.
    content = build(pages)
    validate(content, pages)
    old = json.loads(TARGET.read_text()) if TARGET.exists() else {}
    previous = {k:v for k,v in old.items() if k != 'generated_at'}
    stamp = old.get('generated_at') if previous == content else None
    if not stamp:
        stamp = dt.datetime.now(dt.timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')
    dt.datetime.fromisoformat(stamp.replace('Z', '+00:00'))
    result = {**content, 'generated_at': stamp}
    text = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    stale = not TARGET.exists() or TARGET.read_text() != text
    if stale and not check:
        TARGET.write_text(text, encoding='utf-8')
    print(json.dumps({'services':len(content['services']), 'articles':len(content['articles']), 'case_studies':len(content['case_studies']), 'stale':stale, 'sha256':hashlib.sha256(text.encode()).hexdigest()}))
    return stale


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Read-only freshness and integrity check')
    options = parser.parse_args()
    raise SystemExit(1 if generate(options.check) and options.check else 0)

#!/usr/bin/env python3
"""Render linked case cards into service HTML. Standard library; run before AI build."""
from pathlib import Path
from html import escape
import argparse, json, re
import site_locales
ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--check', action='store_true')
args = parser.parse_args()
config = json.loads((ROOT / 'scripts/service-cases.json').read_text())
registry = site_locales.load()
stale = []
for service in config.values():
    for lang, route in site_locales.published(site_locales.resolve(service['pages'], registry)).items():
        cards = []
        # Match the compact Alma card even when a section contains just one case.
        image_sizes = "(min-width: 1200px) 280px, (min-width: 1024px) 22vw, (min-width: 650px) 45vw, 90vw"
        labels = {'pl': ['Objaw', 'Przyczyna', 'Rezultat', 'Pełna realizacja'],
                  'ru': ['Симптом', 'Причина', 'Результат', 'Полное описание'],
                  'en': ['Symptom', 'Cause', 'Result', 'Full case study']}[lang]
        evidence = []
        for case in service['cases']:
            case_routes = site_locales.published(site_locales.resolve(case['pages'], registry))
            source_lang = lang
            url = case_routes.get(lang)
            if url is None and lang in service.get('case_language_fallbacks', {}):
                source_lang = service['case_language_fallbacks'][lang]
                url = case_routes.get(source_lang)
            if url is None:
                continue  # A planned translation is never a published destination.
            assert lang in case['content'], 'Missing published case card translation: ' + url
            content = case['content'][lang]
            evidence.append(url)
            assert (ROOT / url.strip('/') / 'index.html').is_file(), url
            img = case['image']
            assert (ROOT / img['src'].lstrip('/')).is_file(), img['src']
            attrs = ' '.join(f'{k}="{escape(v, quote=True)}"' for k, v in img.items())
            card = f'<article class="contact-card price-card service-case"><img {attrs} sizes="{image_sizes}" loading="lazy" decoding="async" alt="{escape(content["title"])}" /><h3>{escape(content["title"])}</h3>'
            card += ''.join(f'<p><strong>{label}:</strong> {escape(content[key])}</p>' for label, key in zip(labels, ['symptom', 'cause', 'result']))
            language_note = f' ({registry["languages"][source_lang]})' if source_lang != lang else ''
            if lang == 'en' and source_lang == 'pl':
                language_note = ' (in Polish)'
            card += f'<a href="{url}">{labels[3]}{language_note} →</a></article>'
            cards.append(card)
        path = ROOT / route.strip('/') / 'index.html'
        source = path.read_text()
        block = '<!-- BEGIN SERVICE CASES -->\n<div class="service-cases-grid">\n' + '\n'.join(cards) + '\n</div>\n<!-- END SERVICE CASES -->'
        updated, count = re.subn(r'<!-- BEGIN SERVICE CASES -->.*?<!-- END SERVICE CASES -->', lambda _: block, source, flags=re.S)
        assert count == 1, path
        # Keep machine-readable case relationships aligned with the visible cards.
        def schema(match):
            value = json.loads(match.group(1))
            nodes = value.get('@graph', [value])
            for node in nodes:
                if node.get('@type') == 'Service':
                    node['subjectOf'] = [{'@type': 'WebPage', 'url': registry['base_url'] + url} for url in evidence]
            return '<script type="application/ld+json">' + json.dumps(value, ensure_ascii=False, indent=2) + '</script>'
        updated = re.sub(r'<script type="application/ld\+json">(.*?)</script>', schema, updated, flags=re.S)
        if source != updated:
            stale.append(str(path.relative_to(ROOT)))
            if not args.check:
                path.write_text(updated)
print(('STALE: ' if args.check else 'Updated: ') + ', '.join(stale) if stale else 'Service case cards are current.')
raise SystemExit(1 if args.check and stale else 0)

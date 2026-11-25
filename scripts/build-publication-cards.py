#!/usr/bin/env python3
"""Normalize every public blog/case card; never rewrite article copy or metadata."""
import argparse
import importlib.util
import json
import re
from html import escape
from pathlib import Path
from public_site import public_files, ROOT

spec = importlib.util.spec_from_file_location('case_markup', ROOT / 'scripts/build-case-layout.py')
markup = importlib.util.module_from_spec(spec)
spec.loader.exec_module(markup)
TITLES = json.loads((ROOT / 'scripts/publication-card-titles.json').read_text())
CARD = re.compile(r'<article\b[^>]*class="[^"]*\b(?:blog-card|realizacja-card|service-case)\b[^\"]*"[^>]*>.*?</article>', re.S)
CSS = '<link rel="stylesheet" href="/css/publication-cards.css" />'
LABELS = {'pl': ('Przeczytaj artykuł', 'Zobacz realizację'), 'ru': ('Читать статью', 'Смотреть реализацию'), 'en': ('Read article', 'View case study')}

def add(node, cls):
    if not node.has(cls):
        node.classes(*node.attrs.get('class', '').split(), cls)

def transform(source):
    lang = re.search(r'<html\b[^>]*lang="([^"]+)"', source)[1]
    def card(match):
        tree = markup.Tree(match[0]); c = tree.root.all(tag='article')[0]
        blog, service = c.has('blog-card'), c.has('service-case')
        # Image/caption-only equipment panels are not publication cards.
        if not any(n.tag in ('h2', 'h3') for n in c.all()): return match[0]
        add(c, 'lts-card')
        if service: add(c, 'lts-card--service')
        heading = next(n for n in c.all() if n.tag in ('h2', 'h3'))
        add(heading, 'lts-card__title')
        if not blog and not service:
            for extra in list(c.all()):
                if extra.has('realizacja-card__tags') or extra.has('realizacja-card__services'):
                    extra.parent.children.remove(extra)
        links = c.all(tag='a'); cta = links[-1]
        add(cta, 'lts-card__cta')
        href = cta.attrs['href']
        title = TITLES.get(href)
        if title and (not service or len(title) < len(heading.text().strip())):
            target = heading.all(tag='a')[0] if heading.all(tag='a') else heading
            target.children = [escape(title)]
        if not re.search(r'[^\W\d_]', cta.text(), re.UNICODE):
            cta.children = [LABELS[lang][0 if blog else 1] + ' <span aria-hidden="true">→</span>']
        for n in c.all():
            if n.has('blog-card__content') or n.has('realizacja-card__content'): add(n, 'lts-card__body')
            if n.has('blog-card__description') or n.has('realizacja-card__text') or n.has('realizacja-card__description'): add(n, 'lts-card__description')
        return tree.root.render()
    updated = CARD.sub(card, source)
    if updated != source:
        updated = re.sub(r'[ \t]+(?=\n)', '', updated)
    if 'lts-card__title' in updated and CSS not in updated:
        updated = updated.replace('</head>', '  ' + CSS + '\n</head>', 1)
    if 'lts-card__title' not in updated:
        updated = updated.replace('  ' + CSS + '\n', '')
    return updated

def run():
    parser = argparse.ArgumentParser(); parser.add_argument('--check', action='store_true'); args = parser.parse_args()
    changed=[]; count=0
    for rel in public_files():
        if rel.suffix != '.html': continue
        path=ROOT/rel; source=path.read_text()
        if not CARD.search(source): continue
        updated=transform(source); count += updated.count('lts-card__title')
        if updated != source:
            changed.append(str(rel))
            if not args.check: path.write_text(updated)
    print(f'{count} publication cards; {len(changed)} '+('stale pages' if args.check else 'pages updated'))
    if args.check and changed: raise SystemExit(1)

if __name__ == '__main__': run()

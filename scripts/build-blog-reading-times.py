#!/usr/bin/env python3
"""Fill missing card reading estimates (200 words/minute); preserve existing estimates."""
import argparse
import html
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CARD = re.compile(r'<article class="blog-card">.*?</article>', re.S)
LABELS = {'pl': 'Około {} min czytania', 'ru': 'Около {} мин чтения', 'en': 'About {} min read'}


def build(check=False):
    missing = []
    for lang, filename in [('pl', 'blog/index.html'), ('ru', 'ru/blog/index.html'), ('en', 'en/blog/index.html')]:
        path = ROOT / filename
        source = path.read_text()
        def update(match):
            card = match[0]
            for cls in ['blog-card__top', 'blog-card__content', 'blog-card__title', 'blog-card__description', 'blog-card__footer', 'blog-card__link']:
                assert f'class="{cls}"' in card, (filename, cls)
            if 'class="blog-card__reading-time"' in card:
                assert card.count('class="blog-card__reading-time"') == 1
                return card
            url = re.search(r'href="([^"]+)"', card)[1]
            article = (ROOT / url.strip('/') / 'index.html').read_text()
            main = re.search(r'<main\b[^>]*>(.*?)</main>', article, re.S)[1]
            text = html.unescape(re.sub(r'<[^>]+>', ' ', main))
            minutes = max(1, math.ceil(len(re.findall(r'\b\w+\b', text)) / 200))
            missing.append((lang, url, minutes))
            return card.replace('<footer class="blog-card__footer">', '<footer class="blog-card__footer"><span class="blog-card__reading-time">' + LABELS[lang].format(minutes) + '</span>', 1)
        updated = CARD.sub(update, source)
        if updated != source and not check:
            path.write_text(updated)
    for lang, url, minutes in missing:
        print(f'{lang}: {minutes} min — {url}')
    print(f'Missing reading times: {len(missing)}' if check else f'Added reading times: {len(missing)}')
    return missing


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    missing = build(args.check)
    if args.check and missing:
        raise SystemExit(1)

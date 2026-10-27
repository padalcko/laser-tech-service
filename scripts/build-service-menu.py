#!/usr/bin/env python3
"""Keep the B2B entry immediately after pricing in existing service submenus."""
import argparse
import re
from html import escape
import site_locales as locales


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    registry = locales.load()
    b2b = next(g for g in registry['pages'] if g['id'] == 'uslugi:serwis-dla-sieci-salonow')
    pricing = next(g for g in registry['pages'] if g['type'] == 'pricing')
    labels = {'pl': 'Dla sieci i salonów', 'ru': 'Для сетей и салонов', 'en': 'For Chains & Salons'}
    targets = {locales.ROOT / r['url'].lstrip('/') / 'index.html': (lang, r['url'])
               for g in registry['pages'] for lang, r in g['routes'].items()
               if r['status'] == 'published'}
    targets[locales.ROOT / '404.html'] = ('pl', '/404.html')
    stale, count = [], 0
    for path, (lang, route) in targets.items():
        source = path.read_text()
        menu = re.search(r'<ul class="nav-submenu" id="servicesSubmenu"[^>]*>.*?</ul>', source, re.S)
        assert menu, f'Missing services submenu: {path}'
        # Remove only our own entry, preserving every other item and attribute.
        url = b2b['routes'][lang]['url']
        block = re.sub(r'<li><a href="' + re.escape(url) + r'"[^>]*>.*?</a></li>', '', menu[0])
        price = re.search(r'<li><a href="' + re.escape(pricing['routes'][lang]['url']) + r'"[^>]*>.*?</a></li>', block)
        assert price, f'Missing price entry: {path}'
        current = ' aria-current="page"' if route == url else ''
        entry = f'<li><a href="{url}"{current}>{escape(labels[lang])}</a></li>'
        block = block[:price.end()] + entry + block[price.end():]
        updated = source[:menu.start()] + block + source[menu.end():]
        count += 1
        if updated != source:
            stale.append(str(path.relative_to(locales.ROOT)))
            if not args.check:
                path.write_text(updated)
    print(f'Service menus: {count}; {"stale" if args.check else "updated"}: {len(stale)}')
    if args.check and stale:
        raise SystemExit(1)


if __name__ == '__main__':
    main()

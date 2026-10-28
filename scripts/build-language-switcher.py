#!/usr/bin/env python3
"""Update only the language component from published registry peers; --check is read-only."""
import argparse
import json
import re
from html import escape
import site_locales as locales

GLOBE = '<svg class="language-switcher__globe" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a17 17 0 0 1 0 20 17 17 0 0 1 0-20Z"/></svg>'

LABELS = {'pl': 'Wybór języka', 'ru': 'Выбор языка', 'en': 'Choose language'}
PATTERN = re.compile(r'<div class="language-switcher"[^>]*>.*?</div>', re.S)


def render(group, language, names):
    links = []
    for lang, url in locales.published(group).items():
        active = ' language-switcher__link--active' if lang == language else ''
        current = ' aria-current="page"' if lang == language else ''
        links.append(f'      <a href="{escape(url)}" class="language-switcher__link{active}" lang="{lang}" hreflang="{lang}"{current}>{escape(names[lang])}</a>')
    return (f'<div class="language-switcher" aria-label="{LABELS[language]}">\n'
            '  <details class="language-switcher__dropdown">\n'
            f'    <summary class="language-switcher__toggle" aria-label="{LABELS[language]}: {names[language]}">{GLOBE}<span>{language.upper()}</span> <span aria-hidden="true">▾</span></summary>\n'
            '    <ul class="language-switcher__options">\n' +
            '\n'.join('      <li>' + link.strip() + '</li>' for link in links) +
            '\n    </ul>\n  </details>\n</div>')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    registry = locales.load()
    targets = [(locales.ROOT / url.lstrip('/') / 'index.html', group, lang)
               for group in registry['pages'] for lang, url in locales.published(group).items()]
    # 404 owns its in-document PL/RU/EN switcher; it has no translated routes.
    stale = []
    for path, group, lang in targets:
        source = path.read_text()
        updated, count = PATTERN.subn(lambda _: render(group, lang, registry['languages']), source)
        assert count == 1, f'Expected one language component: {path}'
        if source != updated:
            stale.append(str(path.relative_to(locales.ROOT)))
            if not args.check:
                path.write_text(updated)
    # The shared chat uses the same published contact routes as navigation.
    contact = next(g for g in registry['pages'] if g['type'] == 'contact')
    routes = dict(locales.published(contact))
    client = locales.ROOT / 'js/lazar-ai.js'
    source = client.read_text()
    block = '// BEGIN LAZAR CONTACT ROUTES\n  const contactRoutes = ' + json.dumps(routes, ensure_ascii=False) + ';\n  // END LAZAR CONTACT ROUTES'
    updated, count = re.subn(r'// BEGIN LAZAR CONTACT ROUTES.*?// END LAZAR CONTACT ROUTES', lambda _: block, source, flags=re.S)
    assert count == 1, 'Expected one generated Lazar contact-route block'
    if source != updated:
        stale.append('js/lazar-ai.js')
        if not args.check:
            client.write_text(updated)
    print(f'Language components: {len(targets)}; ' + ('stale' if args.check else 'updated') + f': {len(stale)}')
    if args.check and stale:
        raise SystemExit(1)


if __name__ == '__main__':
    main()

# Unified blog presentation — 2026-11-10

Reference: https://lasertechservice.pl/ru/blog/planovoe-obsluzhivanie-diodnogo-lazera-pochemu-eto-vazhno/

Scope: all 32 articles in PL/RU/EN (96 published pages). Article copy remains in the existing HTML sources. `scripts/build-blog-layout.py` is integrated into the production build and is idempotent; it does not need a third-party parser or client-side JavaScript.

- Every article ends with the same right-aligned reference signature: Олександр Падалко / Raccoon Seo Studio / Wrocław, 2026. Former bylines are removed. Meta author and Article/BlogPosting JSON-LD use the same Person. Publisher remains Laser Tech Service.
- CTA blocks retain their topical headings, descriptions and existing destinations. Their structure, eyebrow and button styles are unified. Each provides a localized contact action and WhatsApp; related case links are retained as secondary actions. Articles without a CTA receive a localized general service CTA.
- Button classes no longer inherit the generic inline-link text color on a gold background. Explicit foreground/background colors cover default and hover states; visible keyboard focus and multiline button labels support narrow screens.
- Standard photo maximum width is reduced from 960 to 480 px. Existing 420 px compact figures become 210 px, with their former 320 px height cap reduced to 160 px. Other photos have a 480 px height cap. Images remain proportional, centered and fluid on mobile; no photo is replaced or removed. Responsive sizes are updated.
- The outer article structure is consistent across locales; shared header, footer, navigation, analytics, forms and video embeds are preserved.

Validation commands:

```sh
python3 scripts/build-blog-layout.py --check
python3 scripts/check-blog-layout.py
# During implementation, compare content and media with the pre-change HEAD:
python3 scripts/check-blog-layout.py --compare-head
node scripts/check-blog-layout.cjs
```

Static validation passed for all 96 pages: unique signature, author metadata/schema, CTA controls, image caps, generator idempotence, original headings/paragraphs/lists/captions, photo sources/counts, videos, forms and publication dates. Locale registry, GEO/SEO, AI search and `git diff --check` passed. Markdown mirrors and `llms-full.txt` were refreshed.

Changes are local; no commit, push or deployment. Third-party requests are blocked during browser QA; real form submission and third-party video playback are outside this validation.

Browser validation: Chrome covered all 96 routes at 320, 768 and 1440 px (288 layouts). The initial pass found inline button colors on the three smartPULS translations; those overrides were removed and all nine affected layouts passed the targeted rerun. Final minimum CTA contrast is 9.88:1. Photo bounds, unique bottom signature, keyboard focus, CTA hit targets, no overflow, and no JavaScript/local HTTP errors passed. Desktop/mobile reference and representative CTA screenshots were visually inspected.

# SEO Redirect and Canonical Audit — 2026-11-07

## Executive summary

The production redirect and canonical setup is consistent with the site's trailing-slash URL structure. All 12 Google Search Console URLs were requested against production. Each returned one permanent redirect and ended at HTTP 200; no loops, multi-hop redirect chains, cross-language redirects, or 404 destinations were observed.

The one exception to a final URL being the canonical URL is `/index.html`: it remains a 200 alias after HTTP-to-HTTPS normalization, but its canonical points to the homepage `/`. It is not in the sitemap and no public internal links point to it. This is a consistent canonical signal, not a sitemap or internal-link defect.

No confirmed production defect required changing redirect, canonical, hreflang, or sitemap configuration. The existing GSC “Page with redirect” entries represent intentional URL variants and should not be removed just to clear that report category.

## Production checks

Requests were made to `https://lasertechservice.pl` on 2026-11-07. Redirect chains were collected with `curl -L` and response bodies were inspected for canonical and language tags.

| # | Requested URL | Initial status and `Location` | Redirects | Final URL (status) | Final canonical | Sitemap | Language |
|---|---|---|---:|---|---|---|---|
| 1 | `http://lasertechservice.pl/` | 301 → `https://lasertechservice.pl/` | 1 | `https://lasertechservice.pl/` (200) | `https://lasertechservice.pl/` | Yes | Polish |
| 2 | `https://lasertechservice.pl/kontakt` | 301 → `/kontakt/` | 1 | `https://lasertechservice.pl/kontakt/` (200) | `https://lasertechservice.pl/kontakt/` | Yes | Polish |
| 3 | `https://lasertechservice.pl/uslugi` | 301 → `/uslugi/` | 1 | `https://lasertechservice.pl/uslugi/` (200) | `https://lasertechservice.pl/uslugi/` | Yes | Polish |
| 4 | `https://lasertechservice.pl/uslugi.html` | 301 → `/uslugi/` | 1 | `https://lasertechservice.pl/uslugi/` (200) | `https://lasertechservice.pl/uslugi/` | Yes | Polish |
| 5 | `https://lasertechservice.pl/ru/uslugi.html` | 301 → `/ru/uslugi/` | 1 | `https://lasertechservice.pl/ru/uslugi/` (200) | `https://lasertechservice.pl/ru/uslugi/` | Yes | Russian |
| 6 | `http://lasertechservice.pl/index.html` | 301 → `https://lasertechservice.pl/index.html` | 1 | `https://lasertechservice.pl/index.html` (200) | `https://lasertechservice.pl/` | Canonical `/` is listed; `/index.html` is not | Polish |
| 7 | `https://lasertechservice.pl/ru/kontakt` | 301 → `/ru/kontakt/` | 1 | `https://lasertechservice.pl/ru/kontakt/` (200) | `https://lasertechservice.pl/ru/kontakt/` | Yes | Russian |
| 8 | `https://lasertechservice.pl/ru/kontakt.html` | 301 → `/ru/kontakt/` | 1 | `https://lasertechservice.pl/ru/kontakt/` (200) | `https://lasertechservice.pl/ru/kontakt/` | Yes | Russian |
| 9 | `https://www.lasertechservice.pl/` | 301 → `https://lasertechservice.pl/` | 1 | `https://lasertechservice.pl/` (200) | `https://lasertechservice.pl/` | Yes | Polish |
| 10 | `https://lasertechservice.pl/kontakt.html` | 301 → `/kontakt/` | 1 | `https://lasertechservice.pl/kontakt/` (200) | `https://lasertechservice.pl/kontakt/` | Yes | Polish |
| 11 | `http://lasertechservice.pl/ru/` | 301 → `https://lasertechservice.pl/ru/` | 1 | `https://lasertechservice.pl/ru/` (200) | `https://lasertechservice.pl/ru/` | Yes | Russian |
| 12 | `https://lasertechservice.pl/ru/uslugi` | 301 → `/ru/uslugi/` | 1 | `https://lasertechservice.pl/ru/uslugi/` (200) | `https://lasertechservice.pl/ru/uslugi/` | Yes | Russian |

## Netlify and URL architecture

- [netlify.toml](../netlify.toml) builds and publishes `dist/`.
- [_redirects](../_redirects) defines permanent `301!` redirects for the four legacy `.html` service/contact routes. Production confirms they each redirect directly to the matching trailing-slash page.
- There are no repository redirect rules for HTTP-to-HTTPS or `www` to non-`www`. Production Netlify edge/domain behavior provides one permanent redirect for each tested alias.
- Production also normalizes the no-slash forms (`/kontakt`, `/uslugi`, and Russian equivalents) to the trailing-slash format in one hop.
- No redirect loops, chains, wrong-language destinations, or redirect-to-404 destinations were found among the 12 URLs.
- No redirect or routing configuration was changed. Netlify Forms and application behavior were not affected.

## Canonical, hreflang, and sitemap

A production crawl of every sitemap entry found:

- 261 unique `<loc>` URLs, all HTTPS on the non-`www` host.
- All 261 sitemap URLs returned HTTP 200 without a redirect.
- All 261 pages declared a self-referencing canonical matching the sitemap URL.
- All 261 pages declared a language tag, and their hreflang links matched the sitemap alternates.
- 1,044 hreflang alternate links were checked; no missing sitemap destinations or duplicate `<loc>` entries were found.
- The production sitemap excludes `.html` aliases, `/index.html`, HTTP, and `www` URLs.
- Existing locale codes include `pl`, `ru`, `en`, and regional `pl-PL`/`ru-RU` where configured, plus `x-default`; the local locale checks accepted the site's current language registry.

The `/index.html` endpoint is not a sitemap URL and does not have public internal links. Its canonical correctly points to the sitemap homepage. A path-level redirect could make this alias converge at the HTTP layer too, but would need to be coordinated with Netlify's HTTPS edge behavior to avoid adding a second redirect to the HTTP form. No change was made because the current canonical is correct and the requested no-chain behavior is already met.

## Internal links and public endpoints

- No exact internal references were found for the four `.html` aliases, the no-slash contact/services variants, or `/index.html` in public HTML, Markdown, TXT, or XML files.
- The site's canonical links, language switcher, and public Markdown representations use the trailing-slash canonical routes.
- Production `robots.txt`, `sitemap.xml`, `llms.txt`, and `llms-full.txt` returned HTTP 200. `robots.txt` allows crawling and references the production sitemap.

## Files changed

- `docs/SEO_REDIRECT_CANONICAL_AUDIT_2026-11-07.md` — this internal audit report.
- No site source, sitemap, redirect, canonical, hreflang, or Netlify configuration files were changed for this audit.

## Build and regression results

- `python3 scripts/build-site.py && python3 scripts/package-site.py` — passed; public output remains `dist/`.
- `python3 scripts/check-ai-search.py` — passed; no sitemap/canonical/hreflang/link issues.
- `python3 scripts/check-site-locales.py` and `python3 scripts/check-language-switcher.py` — passed for the published PL/RU/EN routes.
- `python3 -B scripts/check-final-static.py` — passed; 261 canonical pages, 87 each in Polish, Russian, and English; no issues or warnings.
- Production representative pages for Polish, Russian, and English, plus `robots.txt`, `sitemap.xml`, `llms.txt`, and `llms-full.txt`, returned HTTP 200.
- Internal `docs/`, `reports/`, `scripts/`, and `content/` directories are excluded from `dist/`; the audit report is kept in `docs/`.
- No design, page content, URL, canonical, hreflang, analytics, CookieYes, or form behavior changes were made.

## Conclusion and Google Search Console follow-up

The listed redirect URLs do not all need to disappear from the “Page with redirect” category. Their permanent redirects are expected canonicalization behavior; GSC can continue to report the source aliases while indexing their canonical destinations.

After the next normal deployment, no special redirect fix validation is required for this audit because no production routing defect was changed. In Search Console:

1. Inspect the canonical destinations in the table and confirm Google-selected canonical URLs when available.
2. Keep the existing canonical sitemap submitted; it contains the 261 final URLs.
3. Treat the redirect source URLs as expected variants. Do not request indexing for the redirecting aliases.
4. Do not interpret the audit as confirmation that Google has indexed any page; indexing status must be confirmed in Search Console.

Search Console account access was not available during this audit.

# AI-readable resources

HTML is the source of truth. The site remains a Polish/Russian static site; no English HTML routes or client-side dependencies were added.

## Files and discovery

- `/llms.txt`: compact Markdown map, with an English entity overview and original page titles/descriptions. Links identify canonical HTML and key Markdown resources.
- `/llms-full.txt`: optional expanded text, grouped by Company, Services, Equipment, Repair Cases, Knowledge Articles, Partners, Contact, Locations and Languages. This is a supplemental resource, not a separate standard or landing page.
- Each indexable `index.html` has a sibling `index.md`, including all service pages, individual cases and articles. Content stays in the language of its HTML source.
- `404.html` has no Markdown equivalent.
- HTML head: `rel="alternate" type="text/markdown"` points to its resource; `rel="describedby"` points to `/llms.txt` (also on 404).
- `_headers`: exact Netlify resource routes, UTF-8 content types and HTTP `Link: <HTML URL>; rel="canonical"` for Markdown. HTML canonicals are unchanged. No Markdown or llms entries are added to sitemap.

The current [llms.txt proposal](https://llmstxt.org/) recommends these discovery relations and directory `index.md` resources. `describedby` is a [registered relation](https://www.iana.org/assignments/link-relations). This is an emerging convention, not a guarantee that any agent will consume these files. Google states that [AI features do not require additional AI files or special schema](https://developers.google.com/search/docs/appearance/ai-features).

## Regenerate after content changes

From the repository root, using Python 3 and its standard library:

```sh
python3 scripts/build-ai-search.py
python3 scripts/build-ai-search.py --check
python3 scripts/check-ai-search.py
```

No package installation or build framework is needed. The generator reads current HTML and sitemap, not git history. It strips navigation, repeated footers, forms, scripts, styles and decorative UI; preserves meaningful text, headings, lists, photographs, public links and video URLs; and extracts existing relationships. The validator checks freshness, retained content blocks, paths, fragments, language pairs, schema, sitemap and robots rules.

Do not edit generated Markdown, llms files, HTML AI-link blocks or the generated block in `_headers` manually. Add unrelated header rules outside `BEGIN/END GENERATED AI HEADERS`; the generator preserves them. Review orphan Markdown resources explicitly when retiring a page; the generator reports them and never deletes them automatically.

## New Realizacja or Blog Article

1. Create the normal HTML page with verified facts and the existing design. Include its actual language, one H1, metadata, canonical, language counterparts and appropriate JSON-LD.
2. Use existing content structure (`p`, headings, lists, images, links). Put real video URLs and useful links to services/cases/articles into HTML. Do not add facts only to Markdown.
3. Add its card to the appropriate language index and its canonical URL/reciprocal alternates to `sitemap.xml`. Do not invent a translation if no corresponding page exists; the current site uses complete PL/RU pairs, which the validator enforces.
4. Regenerate and validate with the commands above. Review the new `index.md`, `llms.txt`, `llms-full.txt`, `_headers` and HTML discovery links.
5. Include all generated changes with the HTML change. Commit/push/deploy remain separate user-authorized actions.

New service pages under `/uslugi/` or `/ru/uslugi/` are discovered from sitemap as well. New partner content is extracted from the relevant HTML source. If the primary route architecture changes, review the generator's category rules and curated key-resource list.

## Entity and factual consistency

Use `https://lasertechservice.pl/#organization` for Laser Tech Service in LocalBusiness/Organization and provider/publisher references. The organization URL is `https://lasertechservice.pl/`, while page canonical URLs remain language-specific. Preserve real human authors.

The full business definitions use existing public name, telephone, email, Wrocław address, Poland service area and existing Instagram/Facebook/Telegram URLs. WhatsApp remains a contact channel. No new logo was selected: the visible site wordmark is text and existing schema did not establish a logo URL. Do not invent a logo, authorization, rating, review, credential, city or repaired component.

Service pages contain `Service` definitions with `subjectOf` links to the actual diode, power-supply and cooling repair cases. Their Markdown lists the same relationships. Extend these only with relevant case evidence; avoid automatically linking every case to every article.

When contact facts or service scope change, update canonical HTML/JSON-LD first, review the short English entity overview in the generator, then regenerate. The compact overview and curated resource descriptions are deliberately small editorial text; they need review if business facts change.

## Validation boundaries

`check-ai-search.py` checks all local link targets and fragments, all generated outputs, source-text consistency and schema/video relationships. It lists external URLs but does not make network requests. External HTTP checks and actual video playback are separate checks; HTTP 200 alone is not proof of playable video.

Netlify is confirmed by production HTTP headers. Local static HTTP testing verifies resource paths/content; it does not prove deployed `_headers` behavior. After a separately authorized deployment, check Markdown `Content-Type`, HTTP canonical and describedby headers on Netlify. Preserve `robots.txt`; it currently has no explicit AI-crawler blocks. Do not add invented robots directives.

Developer documentation stays out of sitemap and the public AI indexes. The complete implementation audit is in `docs/ai-search-report.md`.

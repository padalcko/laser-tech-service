# Laser Tech Service publication contract

Кожна нова сторінка Laser Tech Service повинна автоматично включатися до production build без ручного редагування списків файлів.

- Edit source HTML outside `dist/`, or the corresponding generator/data in `scripts/` and `content/`. Never edit `dist/` as source.
- Public HTML routes are discovered recursively outside private directories. PL lives at the root; RU under `ru/`; EN under `en/`. New nested route directories require no packaging list changes. Put photos with public assets or alongside the page.
- `scripts/public_site.py` defines public file types and private directory exclusions. Do not publish secrets, development configuration, reports, or repository documentation. Do not add another build mechanism.
- `scripts/site-locales.json` owns curated translation groups and generated AI resources, not the publication inventory. Do not invent translations. New standalone HTML is packaged automatically; self-canonical indexable pages are automatically added to the built sitemap, using their existing hreflang only. Curated AI/translation-group participation still uses the existing content registry.
- After changing pages, run `npm run build` (includes validation), then `npm run validate:dist` when independently checking the result. Inspect `reports/dist-validation.json` and confirm every new route is present. Never require another user prompt to refresh `dist/`.
- Run `npm run test:build` after changing the publication pipeline. It uses a temporary isolated source snapshot to test new pages, assets, rejection of incomplete output, cleanup and reproducibility.
- `dist/` is ignored and untracked in Git. Netlify builds from source with `npm run build`, publishing `dist`. Keep that single deployment path; GitHub Actions validates but never deploys.
- Preserve design, content, navigation, SEO, analytics and consent integrations. Packaging preserves HTML and asset bytes.
- Do not commit, push or deploy without explicit user permission. Report local checks separately from remote CI and actual Netlify deployment.

## Shared blog and case card standard (PL/RU/EN)

- Every blog/case card, including About and service-page excerpts, uses the shared `lts-card` component in `css/publication-cards.css`. `scripts/build-publication-cards.py` discovers and normalizes all public cards during the existing build, after content generators. Do not add per-card geometry or locale-specific style fixes.
- Keep card headings at the shared 20px / 1.4 typography with a three-line reserved block. Write concise, meaningful card-only titles in `scripts/publication-card-titles.json` when needed; do not truncate with ellipsis or hide text. Never alter article H1, body, SEO/GEO, metadata or URLs to fit a card.
- Preserve the existing brand, original photos and complete descriptions. Shared grid/subgrid tracks align images, categories, titles and descriptions; cards have equal height per row and CTA controls align at the bottom. Service excerpt cards share the same component with their existing symptom/cause/result rows.
- Every CTA must have visible, localized text and a valid destination; an arrow alone is invalid. Check Primelase and all other cards, not only recent publications.
- For new publications run the build and `python3 scripts/build-publication-cards.py --check`, then verify all card layouts with `scripts/check-publication-cards.cjs` on desktop, tablet and mobile. Titles must actually fit within three lines without clipping; check row alignment, photos, CTA visibility and horizontal overflow. Keep short titles separate from full article titles.

# Pharaon realization layout — 2026-11-10

Scope: 32 case studies, 96 published PL/RU/EN pages. Reference: https://lasertechservice.pl/realizacje/przeglad-serwis-pharaon-1470-wroclaw/

Existing HTML is the content source. `scripts/build-case-layout.py` runs before derived resources in the site build; `data-case-layout="pharaon"` marks migrated pages. New content should use the existing Pharaon components directly. No third-party parser dependency.

- Full-size hero; image-first work rows; alternating white/soft sections; existing result copy uses the dark result component.
- Existing galleries, videos, FAQ, forms and bespoke CTA copy remain. A localized reference CTA is supplied on pages missing one.
- Original headings, paragraphs, list items, photo sources/counts, videos and forms were compared against the clean pre-edit Git baseline. Content outside `main` remains byte-identical.
- Cases with only one photograph retain it in the hero and use text sections. No extra photographs or technical facts were invented. Information bars remain where source metadata exists.
- Moved photo links retain the full-size viewer. Responsive `sizes` reflects the larger work images.

## Inventory (each row has PL/RU/EN versions)

| Polish route | Work rows | Page images |
| --- | ---: | ---: |
| beauty-planet-3d-contour-naprawa-przewodu-wroclaw | 0 | 11 |
| naprawa-3000-nain-bloku-zasilania | 5 | 18 |
| naprawa-alma-accent-gorlitz | 3 | 14 |
| naprawa-beauty-planet-3d-contour-wroclaw | 4 | 18 |
| naprawa-chlodzenia-lightsheer-desire-wroclaw | 3 | 20 |
| naprawa-lumenis-lightsheer-desire-olesnica | 5 | 20 |
| naprawa-multipolar-rf-lublin | 4 | 19 |
| naprawa-nubway-nbw-vsiii-wroclaw | 4 | 18 |
| naprawa-pompy-lasera-e808-praga | 2 | 22 |
| naprawa-rsl-masaz-warszawa | 4 | 15 |
| naprawa-wycieku-chlodzenia-glowicy-klient-praga | 3 | 20 |
| nubway-nbw-vsiii-naprawa-zaworu-podcisnienia-wroclaw | 2 | 22 |
| pilna-naprawa-lasera-co2-poznan | 4 | 16 |
| przeglad-estelase-power-p808l | 3 | 16 |
| przeglad-serwis-pharaon-1470-wroclaw | 4 | 15 |
| przeglad-techniczny-lasera-do-depilacji | 0 | 11 |
| przegrzewanie-glowicy-lasera-lubin-naprawa-przewodow | 1 | 14 |
| przegrzewanie-lasera-diodowego-gliwice-wymiana-filtra | 1 | 13 |
| serwis-cavi-shape-advanced-wroclaw | 4 | 27 |
| serwis-glowicy-lasera-diodowego-poznan | 5 | 22 |
| serwis-gme-exsys-308 | 2 | 13 |
| serwis-hifu-kimed-k1-w1601-gorlitz | 4 | 19 |
| serwis-lasera-diodowego-808nm-warszawa | 5 | 21 |
| serwis-lasera-diodowego-wymiana-glowicy-wroclaw | 4 | 18 |
| serwis-lasera-do-usuwania-tatuazu-wymiana-filtra | 3 | 16 |
| serwis-lasera-sapphire-wymiana-plynu | 3 | 19 |
| smartpuls-ipl-swidnica | 2 | 13 |
| wymiana-modulu-diodowego-lasera-po-zalaniu-poznan | 2 | 14 |
| wymiana-modulu-peltiera-estetech-poznan | 2 | 17 |
| wymiana-peltiera-naprawa-lasera-nd-yag | 5 | 19 |
| wymiana-spalonej-diody-laserowej | 1 | 15 |
| wymiana-wentylatorow-chlodzenia-lasera-wroclaw | 3 | 14 |

## Validation

- Chrome: all 96 routes at 320, 768 and 1440 px (288 layouts); all main images decoded, no horizontal overflow or JavaScript errors; image-first grid and responsive column counts checked.
- Full-size photo dialogs checked on migrated LightSheer and NUBWAY pages. Desktop/mobile screenshots visually reviewed against the reference components.
- Final targeted recheck of the three diode-replacement translations after row ordering adjustment.
- Locale registry, GEO/SEO and AI search/catalogue checks passed. Generated Markdown and `llms-full.txt` refreshed. `git diff --check` passed.
- Local changes only: no commit, push or deployment. External requests blocked during browser QA; embedded third-party playback and live form delivery were not exercised.

# Gliwice — реалізація та стаття PL/RU/EN

Дата публікації матеріалів: **2026-10-28**. Дату ремонту не вказано.

Створено три мовні версії реалізації та три версії статті за чинними шаблонами Sapphire. Усі надані абзаци блогу збережено. Додано лише структурні заголовки, фотографії, CTA та внутрішні посилання. Нові картки стоять першими в кожному з шести списків; картки блогу залишаються текстовими.

## Фінальні URL

### Реалізація

- PL: https://lasertechservice.pl/realizacje/przegrzewanie-lasera-diodowego-gliwice-wymiana-filtra/
- RU: https://lasertechservice.pl/ru/realizacje/peregrev-diodnogo-lazera-glivitse-zamena-filtra/
- EN: https://lasertechservice.pl/en/case-studies/diode-laser-overheating-gliwice-water-filter/

### Блог

- PL: https://lasertechservice.pl/blog/filtr-wody-laser-diodowy-kiedy-wymieniac/
- RU: https://lasertechservice.pl/ru/blog/kogda-menyat-vodyanoy-filtr-diodnogo-lazera/
- EN: https://lasertechservice.pl/en/blog/diode-laser-water-filter-replacement/

## Фотографії

Джерела — надані HEIC, а не JPG із текстового переліку. Усі три фото переглянуто: відповідність описам підтверджено. Коректну орієнтацію застосовано до пікселів; EXIF/XMP/ICC не перенесено. Без генерації, ретуші чи зміни стану обладнання. WebP quality 84; пропорції збережено, збільшення роздільності немає.

Файли розташовані в `img/realizacje/gliwice-filtr-wody/`. Повний аудит: `image-audit.json`.

| WebP | Розміри | Байтів |
|---|---|---:|
| serwis-lasera-diodowego-gliwice-808nm-480w.webp | 480 × 853 | 35,858 |
| serwis-lasera-diodowego-gliwice-808nm-768w.webp | 768 × 1365 | 65,576 |
| serwis-lasera-diodowego-gliwice-808nm.webp | 1280 × 2276 | 126,782 |
| wymiana-filtra-wody-laser-diodowy-gliwice-480w.webp | 480 × 853 | 42,550 |
| wymiana-filtra-wody-laser-diodowy-gliwice-768w.webp | 768 × 1365 | 89,034 |
| wymiana-filtra-wody-laser-diodowy-gliwice.webp | 1280 × 2276 | 190,050 |
| uklad-chlodzenia-lasera-diodowego-gliwice-480w.webp | 480 × 853 | 31,374 |
| uklad-chlodzenia-lasera-diodowego-gliwice-768w.webp | 768 × 1365 | 57,656 |
| uklad-chlodzenia-lasera-diodowego-gliwice.webp | 1280 × 2276 | 112,202 |

Разом: **751,082 байтів** у 9 WebP. Кожна з 6 сторінок використовує всі 3 фотографії. `srcset`, `sizes`, width/height, localized ALT і `decoding="async"` присутні. Герой реалізації — eager; галерея й усі фото всередині статей — lazy.

## SEO, GEO, AI та перевірки

- Унікальні title/description, один H1, H2, breadcrumbs, canonical, OG/Twitter.
- Реальні PL/RU/EN counterparts, x-default PL; перемикач згенеровано стандартним інструментом.
- Article/BlogPosting та BreadcrumbList за шаблоном; автор/видавець Laser Tech Service. FAQPage не додано.
- У sitemap додано 6 канонічних URL без `.html`, lastmod 2026-10-28, без дублікатів. Sitemap у цьому репозиторії є вхідним джерелом, а не результатом окремого генератора.
- `llms.txt`, `llms-full.txt`, AI Catalog, Markdown-дзеркала та Markdown-заголовки `_headers` оновлено чинними генераторами.
- `build-site.py`: PASS; мовний реєстр/перемикач, service menu/cases, AI, GEO/SEO та EUR-перевірки.
- `build-ai-search.py --check`, `check-ai-search.py`: PASS.
- `build-ai-catalog.py --check`, `check-ai-catalog.py`: PASS; фінальний стан актуальний. 16 послуг, 75 статей, 78 реалізацій.
- `check-geo-seo.py`: 222 сторінки, 272 чинні FAQ, issues `{}`.
- `check-gliwice.py`: 6 сторінок, 9 WebP без метаданих, SEO/schema, шість перших карток, чинні внутрішні шляхи, взаємні посилання.
- `check-gliwice.cjs`: 36 станів на 320/375/390/768/1024/1440 px, 18 завантажених фотографій, діалоги галереї, 12 фактичних переходів мовами, шість списків, правильні назви Lazar; без горизонтального overflow та JS-помилок.
- Локальні HTTP-запити нових сторінок: 200.
- `git diff --check`: PASS.

## Межі змін

Початковий Git був чистим. Глобальні CSS/JS, header/footer, навігація, Lazar, форми, аналітика, robots.txt, Netlify-конфігурація та `_redirects` не змінені. На нових сторінках header/footer і скрипти звірено з відповідними мовними еталонами; виняток у header — цільові URL мовного перемикача. Старі HTML-сторінки деталей не змінювалися; у списки додано лише нові картки. Галерея, компактні фотографії та CTA використовують чинні класи шаблону.

## Обмеження та публікація

Commit, push, deploy не виконувалися. Нові URL — фінальні заплановані адреси, локально перевірені; доступність після публікації та індексацію Google/AI не перевірено. Зовнішні запити заблоковано браузерним тестом: реальні повідомлення, webhook Lazar і аналітичні події не надсилалися. Наявну політику EN-backend Lazar не змінено.

## Створені та змінені файли

### Нові

- `blog/filtr-wody-laser-diodowy-kiedy-wymieniac/index.html`
- `blog/filtr-wody-laser-diodowy-kiedy-wymieniac/index.md`
- `en/blog/diode-laser-water-filter-replacement/index.html`
- `en/blog/diode-laser-water-filter-replacement/index.md`
- `en/case-studies/diode-laser-overheating-gliwice-water-filter/index.html`
- `en/case-studies/diode-laser-overheating-gliwice-water-filter/index.md`
- `img/realizacje/gliwice-filtr-wody/image-audit.json`
- `img/realizacje/gliwice-filtr-wody/serwis-lasera-diodowego-gliwice-808nm-480w.webp`
- `img/realizacje/gliwice-filtr-wody/serwis-lasera-diodowego-gliwice-808nm-768w.webp`
- `img/realizacje/gliwice-filtr-wody/serwis-lasera-diodowego-gliwice-808nm.webp`
- `img/realizacje/gliwice-filtr-wody/uklad-chlodzenia-lasera-diodowego-gliwice-480w.webp`
- `img/realizacje/gliwice-filtr-wody/uklad-chlodzenia-lasera-diodowego-gliwice-768w.webp`
- `img/realizacje/gliwice-filtr-wody/uklad-chlodzenia-lasera-diodowego-gliwice.webp`
- `img/realizacje/gliwice-filtr-wody/wymiana-filtra-wody-laser-diodowy-gliwice-480w.webp`
- `img/realizacje/gliwice-filtr-wody/wymiana-filtra-wody-laser-diodowy-gliwice-768w.webp`
- `img/realizacje/gliwice-filtr-wody/wymiana-filtra-wody-laser-diodowy-gliwice.webp`
- `realizacje/przegrzewanie-lasera-diodowego-gliwice-wymiana-filtra/index.html`
- `realizacje/przegrzewanie-lasera-diodowego-gliwice-wymiana-filtra/index.md`
- `ru/blog/kogda-menyat-vodyanoy-filtr-diodnogo-lazera/index.html`
- `ru/blog/kogda-menyat-vodyanoy-filtr-diodnogo-lazera/index.md`
- `ru/realizacje/peregrev-diodnogo-lazera-glivitse-zamena-filtra/index.html`
- `ru/realizacje/peregrev-diodnogo-lazera-glivitse-zamena-filtra/index.md`
- `scripts/check-gliwice.cjs`
- `scripts/check-gliwice.py`
- `reports/gliwice-service-report.md`

### Змінені

- `_headers`
- `ai-catalog.json`
- `blog/index.html`
- `blog/index.md`
- `en/blog/index.html`
- `en/blog/index.md`
- `en/case-studies/index.html`
- `en/case-studies/index.md`
- `llms-full.txt`
- `llms.txt`
- `realizacje/index.html`
- `realizacje/index.md`
- `ru/blog/index.html`
- `ru/blog/index.md`
- `ru/realizacje/index.html`
- `ru/realizacje/index.md`
- `scripts/site-locales.json`
- `sitemap.xml`

## Запропонований commit (не виконано)

`feat: add Gliwice diode laser cooling repair case and multilingual blog`

Add emergency diode laser cooling repair case in Gliwice, PL/RU/EN blog articles, optimized WebP images, structured data, SEO metadata, sitemap and AI catalog updates.

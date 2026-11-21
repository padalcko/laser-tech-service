# Aragon / Beauty Planet — локальний звіт

Створено 4 матеріали × PL/RU/EN: 12 HTML-сторінок та 12 Markdown-версій. Надані тексти збережено без змін; автоматична перевірка порівнює всі заголовки, абзаци та пункти списків.

## Підготовлені URL

### case

- PL: https://lasertechservice.pl/realizacje/serwis-lasera-aragon-wroclaw/
- RU: https://lasertechservice.pl/ru/realizacje/obsluzhivanie-lasera-aragon-vrotslav/
- EN: https://lasertechservice.pl/en/case-studies/aragon-diode-laser-service-wroclaw/

### filters

- PL: https://lasertechservice.pl/blog/filtr-chlodzenia-lasera-diodowego/
- RU: https://lasertechservice.pl/ru/blog/filtr-ohlazhdeniya-diodnogo-lasera/
- EN: https://lasertechservice.pl/en/blog/diode-laser-cooling-filter-maintenance/

### checklist

- PL: https://lasertechservice.pl/blog/przeglad-techniczny-lasera-diodowego-checklista/
- RU: https://lasertechservice.pl/ru/blog/chek-list-obsluzhivaniya-diodnogo-lasera/
- EN: https://lasertechservice.pl/en/blog/diode-laser-maintenance-checklist/

### water

- PL: https://lasertechservice.pl/blog/jaka-woda-do-lasera-diodowego/
- RU: https://lasertechservice.pl/ru/blog/kakuyu-vodu-zalivat-v-diodnyy-lazer/
- EN: https://lasertechservice.pl/en/blog/diode-laser-cooling-water-guide/

## Фото

- IMG_8476.heic → `filtry-ukladu-chlodzenia-lasera-porownanie.webp`
- IMG_8477.heic → `wymiana-wody-chlodzacej-laser-diodowy.webp`
- IMG_8478.heic → `laser-aragon-beauty-planet-diagnostyka.webp`
- IMG_8479.heic → `serwis-lasera-aragon-wroclaw-wymiana-filtra.webp`

4 оригінали HEIC не змінені, SHA-256 перевірено. Створено 24 WebP: 320/480/640/768/960/1280 px. Збережено пропорції та повний кадр; додано стриманий водяний знак унизу праворуч за прикладом попереднього NUBWAY-матеріалу. Формалізованої загальної політики водяних знаків у репозиторії не знайдено. Фото фільтрів — у статті 1; води — у статті 3; дисплея — у кейсі та статті 2.

## Зміни

- Нові `content/aragon-texts.json`, `content/aragon-routes.json`, `scripts/check-aragon.py`.
- 12 каталогів HTML/Markdown за маршрутами вище; 24 фото в `img/realizacje/aragon-wroclaw/`.
- Оновлено 6 списків блогу/реалізацій; нові картки першими.
- Оновлено `scripts/site-locales.json`, `sitemap.xml`, `_headers`, `ai-catalog.json`, `llms.txt`, `llms-full.txt`, похідні Markdown.
- Чинний build автоматично оновив останні реалізації у трьох сторінках «Про нас».
- Дизайн, глобальні CSS/JS, GA4 G-6QFRWP5RX5, GTM і consent не змінені; використано чинні локалізовані шаблони.

## SEO

Унікальні надані Title/Description, один H1, self-canonical, взаємні pl-PL/ru/en/x-default, OG/Twitter, Article/BlogPosting, чинний автор і посилання на сутність організації, BreadcrumbList. Дата публікації 2026-11-21; дату ремонту не вигадано. Матеріали пов’язані між собою й із чинними сторінками діагностики, ремонту охолодження та обслуговування.

## Перевірки

- `npm` відсутній у середовищі. Виконано точні команди з package.json: `python3 scripts/build-site.py` та `python3 scripts/validate-dist.py` — PASS.
- `reports/dist-validation.json`: 292 source / 292 dist, 291 sitemap URL; 0 critical errors, missing_pages=[], warnings=[]. Усі 12 нових маршрутів ready та indexable.
- `python3 scripts/check-aragon.py` — PASS: точність тексту, SEO/schema, посилання, ALT, GA4, sitemap/Markdown, відповідність dist, оригінали й WebP.
- `python3 scripts/build-ai-search.py --check`, `python3 scripts/check-ai-catalog.py`, `git diff --check` — PASS.
- Перевірки locale, language switcher, AI, GEO/SEO, video SEO, цін та упаковки виконані штатною збіркою — PASS.
- Локальний Chrome: лише 12 нових маршрутів, 24 розміри (320/1440), 12 меню, 12 мовних перемикачів, 3 фотодіалоги — PASS. Усі фото завантажені; горизонтального скролу, JS і локальних HTTP-помилок немає. Сторонні запити заблоковано під час тесту.
- Механізм публікації не змінювався, тому test:build не потрібний.

## Межі перевірки

Ручних блокерів не виявлено. Production, індексацію пошуковиками та фактичне надсилання GA4/GTM-подій не перевіряли. Commit, push і deploy не виконували.

## Уточнення оформлення посилань

У всіх 12 нових сторінках 72 посилання в блоках пов’язаних матеріалів і послуг оформлено чинним SVG-глобусом за зразком smartPULS: золотий значок, відступи, область натискання від 44 px. Тексти й адреси збережено. Повторні build, validate-dist, check-aragon та diff-check — PASS. Браузер: 24 розміри (320/1440), глобуси, клавіатурний фокус, відсутність горизонтального скролу — PASS.

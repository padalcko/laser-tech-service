# LightSheer DESIRE — Вроцлав: звіт

Дата підготовки матеріалів: 27.10.2026. Реалізацію та окрему інформаційну статтю створено PL/RU/EN у локальному репозиторії. Commit, push та deploy не виконувалися; наведені production URL є підготовленими маршрутами, а не підтвердженням публікації онлайн.

## Сторінки

| Тип | Мова | URL |
|---|---|---|
| Реалізація | PL | https://lasertechservice.pl/realizacje/naprawa-chlodzenia-lightsheer-desire-wroclaw/ |
| Реалізація | RU | https://lasertechservice.pl/ru/realizacje/remont-ohlazhdeniya-lightsheer-desire-vrotslav/ |
| Реалізація | EN | https://lasertechservice.pl/en/case-studies/lightsheer-desire-cooling-tubing-repair-wroclaw/ |
| Блог | PL | https://lasertechservice.pl/blog/laser-po-roku-przestoju-uklad-chlodzenia/ |
| Блог | RU | https://lasertechservice.pl/ru/blog/lazer-posle-goda-prostoya-sistema-ohlazhdeniya/ |
| Блог | EN | https://lasertechservice.pl/en/blog/laser-unused-for-a-year-cooling-system/ |

## Фото

10 вихідних HEIC перетворено на 30 WebP: 480×853, 768×1365 та 1152×2048 px. EXIF-орієнтацію застосовано, EXIF/XMP видалено. Без AI, ретуші, заміни деталей, кадрування вихідних файлів або збільшення роздільності. Галерея використовує існуючі квадратні прев’ю з відкриттям повного кадру. У статтях — чотири фото висотою до 320 px зі збереженням повної композиції. Картки блогу без зображень.

Усі файли розташовані в `img/realizacje/lightsheer-desire-wroclaw/`. У таблиці зазначені базові назви; адаптивні версії мають суфікси `-480w.webp` і `-768w.webp`. Однакові файли спільні для PL/RU/EN.

| Джерело | Базовий файл | 480w, KiB | 768w, KiB | 1152w, KiB |
|---|---|---:|---:|---:|
| IMG_8080.heic | lumenis-lightsheer-desire-cooling-error.webp | 19.8 | 46.3 | 92.1 |
| IMG_8081.heic | lumenis-lightsheer-coolant-reservoir.webp | 47.8 | 96.5 | 172.0 |
| IMG_8082.heic | lumenis-lightsheer-internal-cooling-components.webp | 52.5 | 100.6 | 177.2 |
| IMG_8085.heic | lumenis-lightsheer-panel-removal.webp | 37.3 | 71.6 | 134.3 |
| IMG_8087.heic | lumenis-lightsheer-internal-electronics.webp | 74.1 | 168.3 | 346.8 |
| IMG_8088.heic | lumenis-lightsheer-yellowed-cooling-tube.webp | 27.7 | 55.7 | 105.5 |
| IMG_8089.heic | lumenis-lightsheer-old-tube-cross-section.webp | 34.7 | 69.2 | 127.2 |
| IMG_8095.heic | lumenis-lightsheer-cooling-circuit-after-service.webp | 62.1 | 128.6 | 229.6 |
| IMG_8099.heic | lumenis-lightsheer-after-repair-check.webp | 28.8 | 55.0 | 97.1 |
| IMG_8100.heic | lumenis-lightsheer-desire-after-service.webp | 53.7 | 131.2 | 274.1 |

Загалом: **3,191,962 байтів (3.04 MiB)**. Точні розміри в байтах, пікселях і відповідність джерел — `image-audit.json` у папці фото.

Не використані: IMG_8083 (окремий кадр маніпули), IMG_8096 (менше технічної інформації). Додано IMG_8099 для ілюстрації перевірки. Виправлено розбіжності з попередніми описами: IMG_8087 — електроніка, IMG_8088 — пожовкла трубка, IMG_8089 — зріз трубки, IMG_8095 — контур охолодження, IMG_8100 — робота з апаратом. ALT описують видиме; фото не використовуються як самостійний доказ результатів вимірювань.

## Контент і інтеграція

- Місто ремонту — Вроцлав. Жодних вигаданих цін, дат ремонту, серійних номерів, рейтингу або цитат клієнта.
- У статті прямо відокремлено загальну тему річного простою від цього ремонту: тривалість простою конкретного апарата невідома.
- Перевірка раз на 1–2 тижні — лише умовна можливість за дозволом виробника та узгодженим графіком, не підтверджений регламент Lumenis. Немає рекомендації робити 20–30 імпульсів.
- Збережено десять етапів ремонту та всі три польські ключові фрази; RU/EN локалізовані.
- Унікальні title/description, один H1, canonical, взаємні hreflang PL/RU/EN/x-default, OG/Twitter, Article/BlogPosting та BreadcrumbList. FAQ не додано.
- `datePublished` і `dateModified`: 2026-10-27 — дата підготовлених до публікації матеріалів, не дата ремонту. Якщо публікація відбудеться іншого дня, перед deploy слід узгодити дату публікації.
- Оновлено шість каталогів реалізацій/блогу, sitemap.xml, scripts/site-locales.json, ai-catalog.json, llms.txt, llms-full.txt, Markdown-версії та автоматичні Link-заголовки у _headers.
- HTML лишається джерелом контенту згідно з архітектурою репозиторію. Повторна штатна генерація не видаляє сторінки та картки. Нову систему генерації не створено.
- Глобальні CSS/JS, сторінки партнерів, навігація, footer і аналітика не змінені. Не додано нових ідентифікаторів GA/GTM/Ads; скрипти нових сторінок збігаються з відповідними мовними шаблонами.
- Lazar збережено. Наявний режим EN без надсилання до бекенду залишено як у шаблонах.

## Перевірки

Пройдено:

- `python3 scripts/build-site.py`: повна штатна збірка.
- `check-site-locales.py`, `check-language-switcher.py`, `check-geo-seo.py`.
- `check-ai-search.py`: 208 HTML-файлів, 26 355 локальних перевірок посилань, 457 блоків JSON-LD, 207 sitemap URL; issues порожній.
- `check-ai-catalog.py`: актуальність, детермінованість і контрольні сценарії.
- `build-ai-search.py --check`, `build-ai-catalog.py --check`: жодного застарілого результату.
- `check-desire-wroclaw.py`: шість сторінок, усі адаптивні фото, десять етапів, SEO, взаємні посилання, картки та незмінність спільного дизайну.
- Pillow: фактичні піксельні розміри WebP збігаються з HTML; EXIF/XMP відсутні.
- Chrome/Playwright: 36 комбінацій шести сторінок і ширин 320/360/390/430/768/1440 px. Без горизонтального скролу, усі фото декодуються; галерея/Escape, три мовні посилання й Lazar працюють; помилок JavaScript немає. Додатково перевірено шість каталогів на 320 px.
- Знімки мобільного оформлення реалізації й статті переглянуто візуально. Браузерні докази: `/tmp/lts-desire-wroclaw/browser-results.json` та PNG у тій самій папці.
- Footer, основна навігація та всі non-schema скрипти побайтово звірені з мовними шаблонами.
- `git diff --check`: успішно.

Під час роботи виправлено два RU-посилання на контакти. Для інструментів знадобився дозволений запуск локального сервера й Chrome поза sandbox та тимчасова установка HEIC-конвертера в /tmp. Початкове очікування видимості контейнера Lazar у тесті замінено перевіркою видимої кнопки, оскільки контейнер сам не має розміру. Невиправлених помилок у проведених перевірках немає.

Межі перевірки: зовнішні запити браузерного тесту блокувалися. Реальне надсилання форм/чатів, аналітика, індексація, Lighthouse/CWV та production-публікація не перевірялися. Push/deploy потребують окремого дозволу згідно з ТЗ і не виконані.

## Повний перелік створених і змінених файлів

- `_headers`
- `ai-catalog.json`
- `blog/index.html`
- `blog/index.md`
- `blog/laser-po-roku-przestoju-uklad-chlodzenia/index.html`
- `blog/laser-po-roku-przestoju-uklad-chlodzenia/index.md`
- `en/blog/index.html`
- `en/blog/index.md`
- `en/blog/laser-unused-for-a-year-cooling-system/index.html`
- `en/blog/laser-unused-for-a-year-cooling-system/index.md`
- `en/case-studies/index.html`
- `en/case-studies/index.md`
- `en/case-studies/lightsheer-desire-cooling-tubing-repair-wroclaw/index.html`
- `en/case-studies/lightsheer-desire-cooling-tubing-repair-wroclaw/index.md`
- `img/realizacje/lightsheer-desire-wroclaw/image-audit.json`
- `img/realizacje/lightsheer-desire-wroclaw/lumenis-lightsheer-after-repair-check-480w.webp`
- `img/realizacje/lightsheer-desire-wroclaw/lumenis-lightsheer-after-repair-check-768w.webp`
- `img/realizacje/lightsheer-desire-wroclaw/lumenis-lightsheer-after-repair-check.webp`
- `img/realizacje/lightsheer-desire-wroclaw/lumenis-lightsheer-coolant-reservoir-480w.webp`
- `img/realizacje/lightsheer-desire-wroclaw/lumenis-lightsheer-coolant-reservoir-768w.webp`
- `img/realizacje/lightsheer-desire-wroclaw/lumenis-lightsheer-coolant-reservoir.webp`
- `img/realizacje/lightsheer-desire-wroclaw/lumenis-lightsheer-cooling-circuit-after-service-480w.webp`
- `img/realizacje/lightsheer-desire-wroclaw/lumenis-lightsheer-cooling-circuit-after-service-768w.webp`
- `img/realizacje/lightsheer-desire-wroclaw/lumenis-lightsheer-cooling-circuit-after-service.webp`
- `img/realizacje/lightsheer-desire-wroclaw/lumenis-lightsheer-desire-after-service-480w.webp`
- `img/realizacje/lightsheer-desire-wroclaw/lumenis-lightsheer-desire-after-service-768w.webp`
- `img/realizacje/lightsheer-desire-wroclaw/lumenis-lightsheer-desire-after-service.webp`
- `img/realizacje/lightsheer-desire-wroclaw/lumenis-lightsheer-desire-cooling-error-480w.webp`
- `img/realizacje/lightsheer-desire-wroclaw/lumenis-lightsheer-desire-cooling-error-768w.webp`
- `img/realizacje/lightsheer-desire-wroclaw/lumenis-lightsheer-desire-cooling-error.webp`
- `img/realizacje/lightsheer-desire-wroclaw/lumenis-lightsheer-internal-cooling-components-480w.webp`
- `img/realizacje/lightsheer-desire-wroclaw/lumenis-lightsheer-internal-cooling-components-768w.webp`
- `img/realizacje/lightsheer-desire-wroclaw/lumenis-lightsheer-internal-cooling-components.webp`
- `img/realizacje/lightsheer-desire-wroclaw/lumenis-lightsheer-internal-electronics-480w.webp`
- `img/realizacje/lightsheer-desire-wroclaw/lumenis-lightsheer-internal-electronics-768w.webp`
- `img/realizacje/lightsheer-desire-wroclaw/lumenis-lightsheer-internal-electronics.webp`
- `img/realizacje/lightsheer-desire-wroclaw/lumenis-lightsheer-old-tube-cross-section-480w.webp`
- `img/realizacje/lightsheer-desire-wroclaw/lumenis-lightsheer-old-tube-cross-section-768w.webp`
- `img/realizacje/lightsheer-desire-wroclaw/lumenis-lightsheer-old-tube-cross-section.webp`
- `img/realizacje/lightsheer-desire-wroclaw/lumenis-lightsheer-panel-removal-480w.webp`
- `img/realizacje/lightsheer-desire-wroclaw/lumenis-lightsheer-panel-removal-768w.webp`
- `img/realizacje/lightsheer-desire-wroclaw/lumenis-lightsheer-panel-removal.webp`
- `img/realizacje/lightsheer-desire-wroclaw/lumenis-lightsheer-yellowed-cooling-tube-480w.webp`
- `img/realizacje/lightsheer-desire-wroclaw/lumenis-lightsheer-yellowed-cooling-tube-768w.webp`
- `img/realizacje/lightsheer-desire-wroclaw/lumenis-lightsheer-yellowed-cooling-tube.webp`
- `llms-full.txt`
- `llms.txt`
- `realizacje/index.html`
- `realizacje/index.md`
- `realizacje/naprawa-chlodzenia-lightsheer-desire-wroclaw/index.html`
- `realizacje/naprawa-chlodzenia-lightsheer-desire-wroclaw/index.md`
- `reports/lightsheer-desire-wroclaw-report.md`
- `ru/blog/index.html`
- `ru/blog/index.md`
- `ru/blog/lazer-posle-goda-prostoya-sistema-ohlazhdeniya/index.html`
- `ru/blog/lazer-posle-goda-prostoya-sistema-ohlazhdeniya/index.md`
- `ru/realizacje/index.html`
- `ru/realizacje/index.md`
- `ru/realizacje/remont-ohlazhdeniya-lightsheer-desire-vrotslav/index.html`
- `ru/realizacje/remont-ohlazhdeniya-lightsheer-desire-vrotslav/index.md`
- `scripts/check-desire-wroclaw.py`
- `scripts/site-locales.json`
- `sitemap.xml`

# Lubin — звіт реалізації

Дата матеріалів: 2026-10-29. Дата ремонту не зазначена. Зміни лише локальні; commit, push і deploy не виконувалися.

## Реалізація

Створено кейс і статтю PL/RU/EN за останніми сторінками Gliwice. Картки додано першими у шести списках. HTML є джерелом контенту; маршрути зареєстровано в `scripts/site-locales.json`, а Markdown, llms та AI Catalog оновлено штатними генераторами. Sitemap доповнено шістьма URL відповідно до реєстру.

Збережено наданий текст, додано підтверджену перевірку роботи маніпули після підключення. Не додано моделі, виробника, потужності, ціни, вимірювань або заміни діода. Загальне пояснення опору відокремлено від діагнозу конкретного ремонту. Текст про гарантію залишено умовним: він не стверджує авторизацію Laser Tech Service будь-яким виробником.

## Канонічні URL після публікації

Кейс:

- PL: https://lasertechservice.pl/realizacje/przegrzewanie-glowicy-lasera-lubin-naprawa-przewodow/
- RU: https://lasertechservice.pl/ru/realizacje/peregrev-lazernoy-manipuly-lyubin-remont-provodov/
- EN: https://lasertechservice.pl/en/case-studies/overheating-laser-handpiece-lubin-diode-wiring/

Блог:

- PL: https://lasertechservice.pl/blog/przegrzewanie-glowicy-lasera-zbyt-dlugie-przewody/
- RU: https://lasertechservice.pl/ru/blog/peregrev-lazernoy-manipuly-dlinnye-provoda/
- EN: https://lasertechservice.pl/en/blog/laser-handpiece-overheating-long-wires/

## Фотографії

Використано чотири надані HEIC, а не відсутні JPG, зазначені у ТЗ. Повний кадр, без генерації, видалення деталей або зміни зовнішності. Виконано м’яку корекцію балансу білого, яскравості, контрасту та різкості. WebP без EXIF/XMP/ICC; без збільшення оригіналів. Головне фото кейсу — IMG_7808; блогу та його OG — IMG_7809. ALT локалізовано за видимим вмістом.

Усі фото мають варіанти 480×853, 768×1365 та 1280 px завширшки; таблиця містить точні розміри найбільшого варіанта. Hero кейсу eager, решта lazy; srcset/sizes/width/height задані.

| Оригінал | Основний WebP | Розмір | 480 / 768 / 1280, KiB |
|---|---|---|---|
| IMG_7808.heic | serwis-lasera-lubin-naprawa-manipuly.webp | 1280×2276 | 46.9 / 93.4 / 200.4 |
| IMG_7809.heic | laser-diodowy-przewody-polaczenie-lubin.webp | 1280×2276 | 39.0 / 78.1 / 160.4 |
| IMG_7810.heic | naprawa-polaczenia-diody-laserowej-lubin.webp | 1280×2275 | 59.8 / 117.3 / 223.2 |
| IMG_7811.heic | naprawiona-manipula-lasera-lubin.webp | 1280×2276 | 28.5 / 48.6 / 91.2 |

Разом 12 WebP: 1186.9 KiB. Детальний аудит: `img/realizacje/lubin-przewody-diody/image-audit.json`.

## Перевірки

- `python3 scripts/build-site.py` — PASS після доповнення sitemap новими зареєстрованими маршрутами. Перший запуск до оновлення sitemap очікувано виявив невідповідність реєстру; фінальна збірка успішна.
- `python3 scripts/check-lubin.py` — PASS: шість сторінок, 12 WebP, розміри/метадані, перші картки без дублікатів, внутрішні посилання, мовні відповідники, схема, незмінні спільні компоненти.
- `python3 scripts/build-ai-search.py --check` — PASS, 228 сторінок, `stale: []`.
- `python3 scripts/build-ai-catalog.py --check` — PASS, 16 послуг, 78 статей, 81 кейс, `stale: false`.
- `python3 scripts/check-ai-catalog.py` — PASS, включно з перевірками актуальності, видалень, дублікатів, маршрутів та детермінізму. Проміжні `stale: true` у логах належать тестовим мутаціям; підсумкова перевірка актуальності виконана окремо.
- `check-ai-search.py` і `check-geo-seo.py` у складі build — PASS, `issues: {}`. Sitemap: 228 унікальних канонічних URL. Robots дозволяє сканування й містить правильну адресу sitemap; файл не змінювався.
- SEO: унікальні H1/title/description, canonical без `.html`, взаємні PL/RU/EN та x-default, OG/Twitter, Article/BlogPosting, BreadcrumbList, автор/видавець та дата матеріалів. Додано взаємні посилання кейс ↔ стаття та локалізовані діагностика/ремонт електроніки.
- `scripts/check-lubin.cjs` — локальний Chrome: шість URL HTTP 200, 36 перевірок розкладки на 320/375/390/768/1024/1440 px, 24 завантаження фото, діалоги галереї, 12 переходів між мовами, шість перших карток, без горизонтального переповнення та JS-помилок.
- Скриншоти: `/tmp/lts-lubin/`; візуально переглянуто PL-кейс 390 px та EN-блог 1440 px. Автоматичні перевірки охоплюють усі шість сторінок. Результати: `/tmp/lts-lubin/browser-results.json`.
- Lazar: на всіх шести сторінках перевірено локалізовану кнопку, відкриття/закриття панелі та поле вводу; PL/RU sending gate увімкнено, EN вимкнено відповідно до чинної конфігурації. Повідомлення не надсилалися.
- `git diff --check` — PASS.

## Межі та збереження

Дизайн, глобальні CSS/JS, header/footer, глобальна навігація, Lazar, форми та інтеграції не змінювалися. Компоненти нових сторінок порівняно з еталонами. Шість попередньо змінених HTML/Markdown файлів партнерів збережено байт у байт; їхні зміни не належать цьому завданню. Їхній контент також збережено в перегенерованому `llms-full.txt`.

Зовнішні запити під час браузерних тестів заблоковано. Реальне надсилання Lazar, доставка заявок, аналітика, production HTTP, індексація Google/AI та live Core Web Vitals не перевірялися. EN backend gate збережено. Локальні URL не означають, що сторінки вже опубліковано.

## Створені файли

- `blog/przegrzewanie-glowicy-lasera-zbyt-dlugie-przewody/index.html`
- `blog/przegrzewanie-glowicy-lasera-zbyt-dlugie-przewody/index.md`
- `en/blog/laser-handpiece-overheating-long-wires/index.html`
- `en/blog/laser-handpiece-overheating-long-wires/index.md`
- `en/case-studies/overheating-laser-handpiece-lubin-diode-wiring/index.html`
- `en/case-studies/overheating-laser-handpiece-lubin-diode-wiring/index.md`
- `img/realizacje/lubin-przewody-diody/image-audit.json`
- `img/realizacje/lubin-przewody-diody/laser-diodowy-przewody-polaczenie-lubin-480w.webp`
- `img/realizacje/lubin-przewody-diody/laser-diodowy-przewody-polaczenie-lubin-768w.webp`
- `img/realizacje/lubin-przewody-diody/laser-diodowy-przewody-polaczenie-lubin.webp`
- `img/realizacje/lubin-przewody-diody/naprawa-polaczenia-diody-laserowej-lubin-480w.webp`
- `img/realizacje/lubin-przewody-diody/naprawa-polaczenia-diody-laserowej-lubin-768w.webp`
- `img/realizacje/lubin-przewody-diody/naprawa-polaczenia-diody-laserowej-lubin.webp`
- `img/realizacje/lubin-przewody-diody/naprawiona-manipula-lasera-lubin-480w.webp`
- `img/realizacje/lubin-przewody-diody/naprawiona-manipula-lasera-lubin-768w.webp`
- `img/realizacje/lubin-przewody-diody/naprawiona-manipula-lasera-lubin.webp`
- `img/realizacje/lubin-przewody-diody/serwis-lasera-lubin-naprawa-manipuly-480w.webp`
- `img/realizacje/lubin-przewody-diody/serwis-lasera-lubin-naprawa-manipuly-768w.webp`
- `img/realizacje/lubin-przewody-diody/serwis-lasera-lubin-naprawa-manipuly.webp`
- `realizacje/przegrzewanie-glowicy-lasera-lubin-naprawa-przewodow/index.html`
- `realizacje/przegrzewanie-glowicy-lasera-lubin-naprawa-przewodow/index.md`
- `ru/blog/peregrev-lazernoy-manipuly-dlinnye-provoda/index.html`
- `ru/blog/peregrev-lazernoy-manipuly-dlinnye-provoda/index.md`
- `ru/realizacje/peregrev-lazernoy-manipuly-lyubin-remont-provodov/index.html`
- `ru/realizacje/peregrev-lazernoy-manipuly-lyubin-remont-provodov/index.md`
- `scripts/check-lubin.cjs`
- `scripts/check-lubin.py`
- `docs/lubin-report.md`

## Змінені файли цього завдання

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

## Запропонований коміт (не виконано)

```text
feat: add Lubin laser handpiece overheating repair case

Add Lubin laser diode wiring repair case, multilingual blog content, optimized WebP photos, SEO metadata, structured data, sitemap and AI catalog integration.
```

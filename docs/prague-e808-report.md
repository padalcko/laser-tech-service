# Unique Light System E808, Praha — звіт

Дата матеріалів: 2026-11-02. Дату ремонту не вигадано. Зміни локальні; commit, push і deploy не виконувалися.

## Що створено

Кейс і окрема інформаційна стаття PL/RU/EN. Еталон: останні сторінки Lubin; ті самі класи, галереї, CTA, header/footer, меню, перемикач мов і Lazar. Нові картки перші у шести каталогах; старі матеріали збережені.

HTML є джерелом контенту, `scripts/site-locales.json` — реєстром маршрутів. Markdown, llms та AI Catalog оновлені штатною збіркою. Sitemap доповнено відповідно до реєстру. CSS/JS та глобальний дизайн у межах цього завдання не змінювались.

Факти ремонту походять із наданого завдання: клієнт у Празі, E808, Water flow error за наявності рідини, пошкоджені вугільні щітки двигуна помпи, дев’ять зазначених етапів ремонту, відновлений обіг без покупки нового вузла. Суму економії, ціну, виробника помпи, вимірювання, гарантії та чеське представництво не додано.

## Канонічні URL після публікації

Кейс:

- PL: https://lasertechservice.pl/realizacje/naprawa-pompy-lasera-e808-praga/
- RU: https://lasertechservice.pl/ru/realizacje/remont-pompy-lazera-e808-praga/
- EN: https://lasertechservice.pl/en/case-studies/e808-laser-cooling-pump-repair-prague/

Блог:

- PL: https://lasertechservice.pl/blog/water-flow-error-laser-pompa-obiegowa/
- RU: https://lasertechservice.pl/ru/blog/water-flow-error-lazer-cirkulyacionnaya-pompa/
- EN: https://lasertechservice.pl/en/blog/laser-water-flow-error-circulation-pump/

## Фотографії

Переглянуто всі 15 оригіналів, відібрано 12. Оригінали у Downloads не змінювалися; контрольні SHA-256 використаних оригіналів записані в `img/realizacje/praga-e808-pompa/image-audit.json`. Повні кадри, коректна орієнтація, без генерації деталей. WebP quality 84, без EXIF/XMP/ICC, без збільшення зображень. Для кожного фото: 480, 768 і 1280 px завширшки, точні width/height, srcset/sizes та ALT PL/RU/EN.

Головне фото кейсу: IMG_8279, майстер біля апарата. Головне фото статті й OG: IMG_8275, розібраний двигун помпи. У кейсі 12 фотографій, у статті 5 вибраних. Hero кейсу eager/high; решта зображень lazy за еталоном.

| Оригінал | Основний WebP | Розмір | Вага основного, KiB |
|---|---|---|---|
| IMG_8279.heic | serwis-unique-light-system-e808-praga.webp | 1280×2276 | 283.4 |
| IMG_8263.heic | laser-unique-light-system-e808-widok-ogolny.webp | 1280×2276 | 172.7 |
| IMG_8266.heic | e808-water-flow-error-ekran.webp | 1280×2276 | 89.2 |
| IMG_8268.heic | e808-dostep-serwisowy-obudowa.webp | 1280×2276 | 303.3 |
| IMG_8269.heic | e808-otwarta-obudowa-chlodzenie.webp | 1280×720 | 79.1 |
| IMG_8273.heic | pompa-obiegowa-e808-po-demontazu.webp | 1280×2276 | 157.7 |
| IMG_8274.heic | pompa-e808-przy-otwartym-aparacie.webp | 1280×2276 | 208.9 |
| IMG_8275.heic | rozebrany-silnik-pompy-e808-szczotki.webp | 1280×2276 | 143.5 |
| IMG_8276.heic | czyszczenie-komutatora-pompy-e808.webp | 1280×2276 | 227.8 |
| IMG_8272.heic | napelnianie-ukladu-chlodzenia-e808.webp | 1280×2276 | 159.2 |
| IMG_8278.heic | ekran-e808-po-naprawie-pompy.webp | 1280×2276 | 140.0 |
| IMG_8280.heic | e808-manipula-ekran-po-serwisie.webp | 1280×2276 | 116.3 |

36 WebP разом: 3470.9 KiB. Браузер вибирає відповідний розмір через srcset.

Не опубліковано IMG_8265 (табличка із серійним номером), IMG_8270 (подібний огляд внутрішнього контуру) та IMG_8271 (дубль заповнення, обрано IMG_8272). Серійний номер не внесено до текстів або ALT.

Фото IMG_8274 показує помпу в руках майстра біля відкритого апарата. ALT описує саме це, а не стверджує, що кадр доводить завершення монтажу. Установлення відремонтованої помпи описано як підтверджений користувачем етап робіт.

## Технічні джерела статті

- https://support.maxongroup.com/hc/en-us/articles/360004252074-Commutation-Graphite-brushes-GB-or-Precious-metal-brushes-EB — загальна інформація про щіткові системи.
- https://www.teyuchiller.com/deal-with-the-laser-chiller-flow-alarm.html — загальні причини сигналізації потоку, зокрема помпа, засмічення та датчик.

У статтях джерела позначені як загальні технічні матеріали, а не як ідентифікація виробника помпи E808. Помилка потоку не подається як однозначна ознака пошкоджених щіток. Згадано альтернативні причини, економічну доцільність залежно від діагностики та необхідність справного охолодження.

## Перевірки

- `python3 scripts/build-site.py`: PASS. У складі збірки пройшли locale, switcher, menu, partner/service-card, AI-search, GEO/SEO та pricing перевірки.
- `python3 scripts/check-prague-e808.py`: PASS. Шість сторінок, 36 WebP, точні розміри/ALT, metadata-free assets, перші картки без дублікатів, внутрішні посилання, schema, однакові спільні компоненти.
- `python3 scripts/build-ai-search.py --check`: PASS, 234 сторінки, `stale: []`.
- `python3 scripts/build-ai-catalog.py --check`: PASS, 16 послуг, 81 стаття, 84 кейси, `stale: false`.
- `python3 scripts/check-ai-catalog.py`: результат зазначено після завершення окремого запуску нижче.
- SEO/GEO: `issues: {}`. Унікальні H1/title/description, canonical без `.html`, PL/RU/EN/x-default, OG/Twitter, Article/BlogPosting, BreadcrumbList, author/publisher, дата матеріалів. 234 унікальні URL sitemap; robots не змінювався.
- Взаємні посилання кейс ↔ стаття та локалізовані послуги ремонту охолодження й діагностики. Три обов’язкові польські ключові фрази присутні природно в релевантному блоці послуг.
- `scripts/check-prague-e808.cjs`: PASS. Усі шість сторінок HTTP 200; 30 розкладок на 320/375/430/768/1440 px; 51 завантаження фотографій; діалоги галереї; 12 реальних мовних переходів; шість перших карток; відкриття/закриття Lazar та локалізовані назви. Горизонтального переповнення та JS-помилок немає.
- Візуально переглянуто PL-кейс 375 px та EN-статтю 1440 px. Скриншоти й JSON результатів: `/tmp/lts-prague/`.
- `git diff --check`: PASS.

## Межі перевірки

Браузерні тести локальні, зовнішні запити заблоковані. Реальна доставка повідомлень Lazar/форм, production HTTP, індексація Google/AI та live Core Web Vitals не перевірялися. EN backend gate збережено. Нові URL ще не опубліковані цим завданням.

Незавершена попередня оптимізація головної сторінки (`index.html`, `scripts/check-home-loading.cjs`) збережена байт у байт від початку цього завдання і не є частиною результату E808. Її фінальна перевірка залишається окремою роботою.

## Створені файли

- `blog/water-flow-error-laser-pompa-obiegowa/index.html`
- `blog/water-flow-error-laser-pompa-obiegowa/index.md`
- `en/blog/laser-water-flow-error-circulation-pump/index.html`
- `en/blog/laser-water-flow-error-circulation-pump/index.md`
- `en/case-studies/e808-laser-cooling-pump-repair-prague/index.html`
- `en/case-studies/e808-laser-cooling-pump-repair-prague/index.md`
- `img/realizacje/praga-e808-pompa/czyszczenie-komutatora-pompy-e808-480w.webp`
- `img/realizacje/praga-e808-pompa/czyszczenie-komutatora-pompy-e808-768w.webp`
- `img/realizacje/praga-e808-pompa/czyszczenie-komutatora-pompy-e808.webp`
- `img/realizacje/praga-e808-pompa/e808-dostep-serwisowy-obudowa-480w.webp`
- `img/realizacje/praga-e808-pompa/e808-dostep-serwisowy-obudowa-768w.webp`
- `img/realizacje/praga-e808-pompa/e808-dostep-serwisowy-obudowa.webp`
- `img/realizacje/praga-e808-pompa/e808-manipula-ekran-po-serwisie-480w.webp`
- `img/realizacje/praga-e808-pompa/e808-manipula-ekran-po-serwisie-768w.webp`
- `img/realizacje/praga-e808-pompa/e808-manipula-ekran-po-serwisie.webp`
- `img/realizacje/praga-e808-pompa/e808-otwarta-obudowa-chlodzenie-480w.webp`
- `img/realizacje/praga-e808-pompa/e808-otwarta-obudowa-chlodzenie-768w.webp`
- `img/realizacje/praga-e808-pompa/e808-otwarta-obudowa-chlodzenie.webp`
- `img/realizacje/praga-e808-pompa/e808-water-flow-error-ekran-480w.webp`
- `img/realizacje/praga-e808-pompa/e808-water-flow-error-ekran-768w.webp`
- `img/realizacje/praga-e808-pompa/e808-water-flow-error-ekran.webp`
- `img/realizacje/praga-e808-pompa/ekran-e808-po-naprawie-pompy-480w.webp`
- `img/realizacje/praga-e808-pompa/ekran-e808-po-naprawie-pompy-768w.webp`
- `img/realizacje/praga-e808-pompa/ekran-e808-po-naprawie-pompy.webp`
- `img/realizacje/praga-e808-pompa/image-audit.json`
- `img/realizacje/praga-e808-pompa/laser-unique-light-system-e808-widok-ogolny-480w.webp`
- `img/realizacje/praga-e808-pompa/laser-unique-light-system-e808-widok-ogolny-768w.webp`
- `img/realizacje/praga-e808-pompa/laser-unique-light-system-e808-widok-ogolny.webp`
- `img/realizacje/praga-e808-pompa/napelnianie-ukladu-chlodzenia-e808-480w.webp`
- `img/realizacje/praga-e808-pompa/napelnianie-ukladu-chlodzenia-e808-768w.webp`
- `img/realizacje/praga-e808-pompa/napelnianie-ukladu-chlodzenia-e808.webp`
- `img/realizacje/praga-e808-pompa/pompa-e808-przy-otwartym-aparacie-480w.webp`
- `img/realizacje/praga-e808-pompa/pompa-e808-przy-otwartym-aparacie-768w.webp`
- `img/realizacje/praga-e808-pompa/pompa-e808-przy-otwartym-aparacie.webp`
- `img/realizacje/praga-e808-pompa/pompa-obiegowa-e808-po-demontazu-480w.webp`
- `img/realizacje/praga-e808-pompa/pompa-obiegowa-e808-po-demontazu-768w.webp`
- `img/realizacje/praga-e808-pompa/pompa-obiegowa-e808-po-demontazu.webp`
- `img/realizacje/praga-e808-pompa/rozebrany-silnik-pompy-e808-szczotki-480w.webp`
- `img/realizacje/praga-e808-pompa/rozebrany-silnik-pompy-e808-szczotki-768w.webp`
- `img/realizacje/praga-e808-pompa/rozebrany-silnik-pompy-e808-szczotki.webp`
- `img/realizacje/praga-e808-pompa/serwis-unique-light-system-e808-praga-480w.webp`
- `img/realizacje/praga-e808-pompa/serwis-unique-light-system-e808-praga-768w.webp`
- `img/realizacje/praga-e808-pompa/serwis-unique-light-system-e808-praga.webp`
- `realizacje/naprawa-pompy-lasera-e808-praga/index.html`
- `realizacje/naprawa-pompy-lasera-e808-praga/index.md`
- `ru/blog/water-flow-error-lazer-cirkulyacionnaya-pompa/index.html`
- `ru/blog/water-flow-error-lazer-cirkulyacionnaya-pompa/index.md`
- `ru/realizacje/remont-pompy-lazera-e808-praga/index.html`
- `ru/realizacje/remont-pompy-lazera-e808-praga/index.md`
- `scripts/check-prague-e808.cjs`
- `scripts/check-prague-e808.py`
- `docs/prague-e808-report.md`

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

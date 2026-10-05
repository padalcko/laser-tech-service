# Ремонт у Познані — звіт, 2026-10-05

Створено реалізацію та пов’язану статтю польською й російською. Commit, push і deployment не виконувалися. Нові URL підготовлені локально; на production їх не перевіряли.

## Створені файли

- `realizacje/wymiana-modulu-diodowego-lasera-po-zalaniu-poznan/index.html`
- `blog/dlaczego-nie-warto-samodzielnie-wymieniac-uszczelek-w-laserze/index.html`
- `ru/realizacje/wymiana-modulu-diodowego-lasera-po-zalaniu-poznan/index.html`
- `ru/blog/pochemu-ne-stoit-samostoyatelno-menyat-uplotneniya-v-lazere/index.html`
- `img/realizacje/wymiana-modulu-diodowego-poznan/uszkodzony-modul-diodowy-poznan-480w.webp`
- `img/realizacje/wymiana-modulu-diodowego-poznan/uszkodzony-modul-diodowy-poznan-768w.webp`
- `img/realizacje/wymiana-modulu-diodowego-poznan/uszkodzony-modul-diodowy-poznan.webp`
- `img/realizacje/wymiana-modulu-diodowego-poznan/zdemontowany-modul-diodowy-po-zalaniu-poznan-480w.webp`
- `img/realizacje/wymiana-modulu-diodowego-poznan/zdemontowany-modul-diodowy-po-zalaniu-poznan-768w.webp`
- `img/realizacje/wymiana-modulu-diodowego-poznan/zdemontowany-modul-diodowy-po-zalaniu-poznan.webp`
- `img/realizacje/wymiana-modulu-diodowego-poznan/slady-cieczy-wewnatrz-modulu-lasera-poznan-480w.webp`
- `img/realizacje/wymiana-modulu-diodowego-poznan/slady-cieczy-wewnatrz-modulu-lasera-poznan-768w.webp`
- `img/realizacje/wymiana-modulu-diodowego-poznan/slady-cieczy-wewnatrz-modulu-lasera-poznan.webp`
- `img/realizacje/wymiana-modulu-diodowego-poznan/rozebrana-manipula-lasera-uklad-chlodzenia-poznan-480w.webp`
- `img/realizacje/wymiana-modulu-diodowego-poznan/rozebrana-manipula-lasera-uklad-chlodzenia-poznan-768w.webp`
- `img/realizacje/wymiana-modulu-diodowego-poznan/rozebrana-manipula-lasera-uklad-chlodzenia-poznan.webp`
- `scripts/check-poznan.py`
- `docs/poznan-diode-seal-report.md`

## Змінені файли

- `realizacje/index.html`
- `ru/realizacje/index.html`
- `blog/index.html`
- `ru/blog/index.html`
- `sitemap.xml`

## Структура і дизайн

Статичні сторінки з окремими `index.html`. Шаблон Realizacje — чинний GME ExSys 308, Blog — чинна публікація Złota Firma 2026 відповідною мовою. Збережено навігацію, footer, social menu, скрипти, CSS-класи, CTA й адаптивну сітку. У мовних перемикачах замінено лише адреси поточної пари сторінок. CSS/JS, головні сторінки та старі картки не редагувалися.

Картки Blog PL/RU текстові, без фотографій, відповідно до наявного оформлення. Картки Realizacje повторюють поточну структуру `realizacja-card`.

## Відбір і оптимізація фотографій

Переглянуто всі 6 кадрів. Використано №1, №3, №5, №6. №2 (`2BC674D1-C084-4203-BF6D-794499B95D83.PNG`) дублює крупний план модуля; №4 (`6C9FA602-1BF1-46F0-ABDE-94988013BF35.PNG`) — ракурс демонтованої збірки. Їх не копіювали в репозиторій.

Фото №1: hero та картка Realizacje. №3: галерея Realizacje й фото у Blog. №5: галерея, головне фото Blog та OG/Twitter Blog. №6: галерея Realizacje. Усі знімки показують розбирання й пошкоджений вузол; жоден не підписаний як нова деталь або результат вимірювання. Галерейні фото відкривають повний WebP за натисканням.

WebP quality 86; пропорції збережено, без збільшення оригіналів. Основні зображення до 1600 px по висоті, адаптивні версії 480/768 px по ширині. Повторне використання спільних файлів у PL/RU/Blog/Realizacje. Оригінали в Downloads не перейменовували й не видаляли: OLD → NEW нижче означає перетворення на production-asset. У репозиторії немає PNG-копій.

| OLD | NEW (основний файл) | До, px / bytes | Після, px / bytes | Економія |
|---|---|---|---|---|
| `49AD47FC-E32F-4429-B12B-84CD32D3E507.PNG` | `img/realizacje/wymiana-modulu-diodowego-poznan/uszkodzony-modul-diodowy-poznan.webp` | 1122×1402 / 2,318,298 | 1122×1402 / 193,356 | 91.7% |
| `83A7A843-D20B-47FC-A764-C25EB9FEE47E.PNG` | `img/realizacje/wymiana-modulu-diodowego-poznan/zdemontowany-modul-diodowy-po-zalaniu-poznan.webp` | 941×1672 / 2,535,709 | 900×1600 / 246,472 | 90.3% |
| `6C98CC08-6C7D-4FA2-8139-EB14470EEF53.PNG` | `img/realizacje/wymiana-modulu-diodowego-poznan/slady-cieczy-wewnatrz-modulu-lasera-poznan.webp` | 941×1672 / 2,692,136 | 900×1600 / 268,218 | 90.0% |
| `EDCA143A-AE05-4E63-BDDC-9C7CF05F4629.PNG` | `img/realizacje/wymiana-modulu-diodowego-poznan/rozebrana-manipula-lasera-uklad-chlodzenia-poznan.webp` | 941×1672 / 3,040,819 | 900×1600 / 404,804 | 86.7% |

Сума: оригінали **10,586,962 bytes** → 4 основні WebP **1,112,850 bytes** (−89.5%). Усі 12 WebP разом: **2,356,058 bytes**.

| WebP-файл | Розміри | Bytes |
|---|---|---|
| `uszkodzony-modul-diodowy-poznan-480w.webp` | 480×600 | 53,916 |
| `uszkodzony-modul-diodowy-poznan-768w.webp` | 768×960 | 113,814 |
| `uszkodzony-modul-diodowy-poznan.webp` | 1122×1402 | 193,356 |
| `zdemontowany-modul-diodowy-po-zalaniu-poznan-480w.webp` | 480×853 | 97,948 |
| `zdemontowany-modul-diodowy-po-zalaniu-poznan-768w.webp` | 768×1365 | 195,324 |
| `zdemontowany-modul-diodowy-po-zalaniu-poznan.webp` | 900×1600 | 246,472 |
| `slady-cieczy-wewnatrz-modulu-lasera-poznan-480w.webp` | 480×853 | 100,708 |
| `slady-cieczy-wewnatrz-modulu-lasera-poznan-768w.webp` | 768×1365 | 212,760 |
| `slady-cieczy-wewnatrz-modulu-lasera-poznan.webp` | 900×1600 | 268,218 |
| `rozebrana-manipula-lasera-uklad-chlodzenia-poznan-480w.webp` | 480×853 | 146,440 |
| `rozebrana-manipula-lasera-uklad-chlodzenia-poznan-768w.webp` | 768×1365 | 322,298 |
| `rozebrana-manipula-lasera-uklad-chlodzenia-poznan.webp` | 900×1600 | 404,804 |

### ALT PL/RU

ALT однаковий для всіх розмірів конкретного фото; мова відповідає сторінці.

- `uszkodzony-modul-diodowy-poznan.webp`
  - PL: Uszkodzony moduł diodowy ze śladami cieczy i osadów
  - RU: Повреждённый диодный модуль со следами жидкости и отложений
- `zdemontowany-modul-diodowy-po-zalaniu-poznan.webp`
  - PL: Zdemontowany moduł diodowy z zabrudzeniami obok otwartej obudowy
  - RU: Демонтированный диодный модуль с загрязнениями рядом с открытым корпусом
- `slady-cieczy-wewnatrz-modulu-lasera-poznan.webp`
  - PL: Krople cieczy i ciemne osady wewnątrz obudowy modułu laserowego
  - RU: Капли жидкости и тёмные отложения внутри корпуса лазерного модуля
- `rozebrana-manipula-lasera-uklad-chlodzenia-poznan.webp`
  - PL: Rozebrana manipuła lasera z przewodami chłodzenia i wymontowanym modułem
  - RU: Разобранная манипула лазера с трубками охлаждения и снятым модулем

## URL, Title, Description

### case / PL

- URL / canonical: https://lasertechservice.pl/realizacje/wymiana-modulu-diodowego-lasera-po-zalaniu-poznan/
- Файл: `realizacje/wymiana-modulu-diodowego-lasera-po-zalaniu-poznan/index.html`
- Title: Wymiana modułu diodowego po zalaniu – Poznań | LTS
- Description: Naprawa lasera w Poznaniu: wymiana zalanego modułu diodowego i prawidłowy montaż uszczelki. Zdjęcia uszkodzeń i przyczyna kosztownej awarii.

### blog / PL

- URL / canonical: https://lasertechservice.pl/blog/dlaczego-nie-warto-samodzielnie-wymieniac-uszczelek-w-laserze/
- Файл: `blog/dlaczego-nie-warto-samodzielnie-wymieniac-uszczelek-w-laserze/index.html`
- Title: Samodzielna wymiana uszczelki w laserze – ryzyko | LTS
- Description: Źle założona uszczelka doprowadziła do zalania diody w laserze w Poznaniu. Wyjaśniamy ryzyko, koszty i objawy wymagające wyłączenia urządzenia.

### case / RU

- URL / canonical: https://lasertechservice.pl/ru/realizacje/wymiana-modulu-diodowego-lasera-po-zalaniu-poznan/
- Файл: `ru/realizacje/wymiana-modulu-diodowego-lasera-po-zalaniu-poznan/index.html`
- Title: Замена залитого диодного модуля в Познани | LTS
- Description: Ремонт лазера в Познани: замена залитого диодного модуля и правильная установка прокладки. Фотографии повреждений и причина дорогостоящей поломки.

### blog / RU

- URL / canonical: https://lasertechservice.pl/ru/blog/pochemu-ne-stoit-samostoyatelno-menyat-uplotneniya-v-lazere/
- Файл: `ru/blog/pochemu-ne-stoit-samostoyatelno-menyat-uplotneniya-v-lazere/index.html`
- Title: Самостоятельная замена прокладки в лазере: риски | LTS
- Description: Неправильно установленная прокладка привела к залитию диода лазера в Познани. Разбираем риски, расходы и признаки, при которых аппарат нужно выключить.

## Canonical, hreflang, schema, sitemap

Кожна сторінка має self-canonical, один H1, вкладені H2 без пропусків рівнів; повний Open Graph і Twitter metadata з локалізованим ALT, розмірами й абсолютним URL фото. BreadcrumbList відповідає видимим breadcrumbs. Article schema застосовано і в Blog, і в Realizacje, як у поточному шаблоні кейсу. Автор та видавець — Laser Tech Service, без вигаданого автора, марки чи моделі. `datePublished` / `dateModified`: 2026-10-05 — дата публікації, не дата ремонту.

У кожній мовній парі:

- case:
  - `pl`: https://lasertechservice.pl/realizacje/wymiana-modulu-diodowego-lasera-po-zalaniu-poznan/
  - `ru`: https://lasertechservice.pl/ru/realizacje/wymiana-modulu-diodowego-lasera-po-zalaniu-poznan/
  - `x-default`: https://lasertechservice.pl/realizacje/wymiana-modulu-diodowego-lasera-po-zalaniu-poznan/
- blog:
  - `pl`: https://lasertechservice.pl/blog/dlaczego-nie-warto-samodzielnie-wymieniac-uszczelek-w-laserze/
  - `ru`: https://lasertechservice.pl/ru/blog/pochemu-ne-stoit-samostoyatelno-menyat-uplotneniya-v-lazere/
  - `x-default`: https://lasertechservice.pl/blog/dlaczego-nie-warto-samodzielnie-wymieniac-uszczelek-w-laserze/

У sitemap додано рівно ці 4 canonical URL, кожен із `lastmod=2026-10-05` і трьома взаємними alternate-посиланнями вище. Всі адреси мають trailing slash. Старі записи збережено, дублікатів немає. Загалом 68 sitemap URL.

## Додані внутрішні посилання

- Індекс Realizacje PL → реалізація PL; RU → реалізація RU.
- Індекс Blog PL → стаття PL; RU → стаття RU.
- Реалізація PL ↔ Blog PL; реалізація RU ↔ Blog RU.
- PL ↔ RU в мовному перемикачі кожної нової пари.
- Breadcrumbs → головна та відповідний мовний індекс.
- CTA Blog → відповідна реалізація та `/kontakt/` або `/ru/kontakt/`.
- CTA Realizacje збережено зі штатного шаблону: WhatsApp та телефон.

## Факти й технічні джерела

Факти ремонту взяті виключно з наданого завдання. Не додано модель, виробника, потужність, довжини хвиль, ціни, об’єм рідини, результати вимірювань або гарантійні правила виробника. Видимі сліди описано як рідину, забруднення та темні відкладення; корозію не оголошено підтвердженою лише за кольором поверхні. Розділ результату відділяє виконані заміни від загального переліку перевірок після складання, не стверджуючи наявності ненаданого протоколу.

Загальні технічні пояснення звірено з первинними матеріалами й посилання додано в обидві статті:

- [Parker — конструкція і прижим ущільнень](https://discover.parker.com/edge-bonded-integral-seal-technology).
- [nLIGHT — технічний матеріал про надійність діодних лазерів, архівна копія матеріалу виробника](https://datasheet.datasheetarchive.com/originals/crawler/nlight.net/ef9033aa9994329e205f591e35319ec9.pdf).
- [Coherent — діодні стеки та варіанти охолодження](https://www.coherent.com/components-accessories/diode-lasers/stacks).

Ці джерела не використовуються для ідентифікації апарата з ремонту.

## Результати перевірок

Команда: `PYTHONPATH=/tmp/ltsmarket-image-tools python3 scripts/check-poznan.py` (потрібен Pillow).

- 69 HTML-сторінок; 3306 локальних посилань; 0 битих файлів/якорів.
- 4 нові сторінки: правильна вкладеність HTML, один H1, без повторів ID.
- PL/RU language switch, self-canonical, взаємні hreflang, x-default — PASS.
- JSON-LD: синтаксис перевірено на всьому сайті; Article/BreadcrumbList нових сторінок — PASS.
- Усі WebP/srcset існують; ширини дескрипторів, intrinsic width/height, ALT та sizes — PASS.
- Lazy loading для галереї, другого фото статті та карток; головне фото без lazy.
- Кожна нова картка додана рівно один раз; старі картки збережено.
- Sitemap: 68 URL, лише 4 нові записи, старі записи незмінні, дублікатів немає.
- Footer, social menu, навігація (окрім адрес мовних перемикачів), скрипти й підключення CSS збігаються з шаблонами.
- CSS, JS, головні сторінки не змінені; інші assets не видалялися.
- Усі 12 нових assets використано; невикористаних копій немає.
- `git diff --check` — PASS.

Браузер: локальний HTTP-сервер і Chrome через Playwright, ширини **1440 / 768 / 390 px**, висота viewport 1000 px. 4 нові сторінки + 4 індекси × 3 ширини = **24 перевірки**. Всі HTTP 200, по одному H1, нуль нерозкритих зображень, нуль горизонтальних переповнень, нуль JS pageerror. Створено full-page screenshots; візуально переглянуто desktop/tablet/mobile приклади PL/RU, сторінки кейсу, статті та карток. Зовнішні трекери заблоковано під час тесту; аналітику не перевіряли.

Окремо реальними кліками на ширині 390 px перевірено PL→RU→PL / RU→PL→RU, відкриття/закриття мобільного меню та переходи Blog↔Realizacje на всіх 4 нових сторінках — PASS.

Браузерні артефакти поточної сесії: `/tmp/poznan-browser-results.json`, `/tmp/poznan-interactions.json`, `/tmp/poznan-*.png`. Це локальна перевірка; production HTTP, Google Search Console та індексацію не перевіряли.

## Git і публікація

Зміни залишені в робочому дереві. Commit: не створено. Push: не виконано. Deployment: не виконано.

## Корекція карток Blog

За уточненням користувача з нових карток PL/RU прибрано фотографії. Зображення всередині статей збережено. Статично перевірено відсутність img/figure у всіх картках обох індексів; попередні браузерні знімки зроблено до цієї корекції.

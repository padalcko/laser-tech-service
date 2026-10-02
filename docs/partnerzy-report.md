# Розділ «Партнери» — звіт

Дата: 2026-10-02. Реалізовано локально. Commit, push і deployment не виконувалися.

## URL та SEO

- PL: https://lasertechservice.pl/partnerzy/
- RU: https://lasertechservice.pl/ru/partnerzy/
- Canonical кожної сторінки вказує на її власний URL вище.
- На обох сторінках взаємні hreflang: `pl` → PL, `ru` → RU, `x-default` → PL.
- Мовний перемикач веде на відповідну сторінку партнерів.
- Додано Open Graph, Twitter Card, WebPage та BreadcrumbList JSON-LD.
- OG/Twitter використовують наявне зображення LTS `/img/urzadzenia-laserowe-w-gabinecie.webp`.
- Breadcrumbs: Strona główna / Partnerzy та Главная / Партнёры.
- `robots` = `index, follow, max-image-preview:large`; robots.txt не забороняє індексацію.
- У sitemap додано рівно два URL із трьома мовними alternate для кожного. Загалом 62 унікальні URL; попередні записи збережено.
- Нових альтернативних HTML-файлів поза директоріями маршрутів не створено. Продакшн-відповіді нових URL не перевірялися: зміни не опубліковані.

### PL

Title: Nasi partnerzy | Laser Tech Service

Description: Poznaj partnerów Laser Tech Service — salony, gabinety kosmetologiczne i specjalistów, których pracę oraz sprzęt znamy i polecamy naszym klientom.

### RU

Title: Наши партнёры | Laser Tech Service

Description: Партнёры Laser Tech Service — салоны, косметологические кабинеты и специалисты, чью работу и оборудование мы знаем и рекомендуем нашим клиентам.

## ANNVI: перевірені дані та джерело

Офіційне джерело: http://annvi.pl/ (HTML отримано 2026-10-02).

- Назва бренду на сайті: AnnVi.
- Місто: Wrocław.
- Діяльність: косметологія і подологія; сайт також містить розділи лазерної депіляції й естетичної медицини.
- Адреса на офіційному сайті: Wrocław, ul. Pochyła 23/1D. У картці використано лише місто.
- Офіційний логотип: http://annvi.pl/images/logo.png, посилання з header сайту.
- Використано цей логотип, а не screenshot. Локальний файл: `/img/partnerzy/annvi-kosmetologia-podologia-wroclaw-logo.webp`.
- Розмір: 201 × 127 px, без збільшення оригіналу; lossless WebP, 3908 байтів замість 9781 байта PNG (приблизно −60%).
- В HTML задані width/height, локалізовані alt, loading="lazy", decoding="async". Hotlink відсутній.
- Зовнішнє посилання картки збережено точно за завданням: https://annvi.pl/, target="_blank", rel="noopener noreferrer".

**Зовнішня проблема:** HTTPS-запит до annvi.pl повернув curl error 60: сертифікат не відповідає hostname. HTTP-версія доступна. Отже, HTTPS-посилання партнера не можна звітувати як успішно перевірене; власнику ANNVI потрібно виправити сертифікат. Перевірка www через веб-інструмент також не дала доступного результату.

## Дизайн та навігація

- Перед Kontakt / Контакты додано Partnerzy / Партнёры у всіх 61 попередніх HTML-файлах, включно з 404. Разом із новими сторінками навігація перевірена у 63 файлах.
- Desktop і burger використовують той самий `#primaryNavigation`.
- Збережені існуючі header, мовний перемикач, footer, логотип, Montserrat, палітра, контейнер, радіуси та CSS-змінні.
- Hero і breadcrumbs повторно використовують `realizacje.css`; текст і акцент — наявні `article-content` та blockquote з `blog.css`.
- `partnerzy.css` додає тільки стилі розділу й карток.
- Мінімальна зміна `main.css`: меню може переносити пункти на вузькому desktop; mobile зберігає одну колонку та отримує достатню висоту/прокрутку для семи пунктів. Breakpoint burger залишено 760 px; шрифти й логотип не змінено.
- Порівняння з HEAD підтвердило: в існуючих HTML змінено лише додавання пункту меню. Footer нових сторінок ідентичний footer відповідних мовних сторінок Realizacje.

## Перевірки

- HTML5 parser: 0 помилок на нових сторінках. Це локальна перевірка парсером, не зовнішній W3C Validator.
- Усі JSON-LD блоки сайту парсяться як JSON; перевірено WebPage, BreadcrumbList, canonical, hreflang та language switch нових сторінок.
- Повний HTML-аудит локальних href/src/poster: 0 відсутніх файлів/маршрутів, 0 відсутніх зображень. Це не перевірка всіх зовнішніх сайтів.
- Sitemap XML парситься; URL не дублюються.
- `git diff --check`: пройдено.
- Headless Google Chrome: нові PL/RU сторінки та головні PL/RU сторінки на ширинах 1440, 1024, 1000, 901, 900, 820, 768, 761, 760, 650, 390, 320 px (48 комбінацій).
- Сітка: 4 колонки >1000 px; 2 колонки 761–1000 px; 1 колонка ≤760 px. Використано наявні breakpoint-и blog.css.
- На 1440/820/390 px перевірено також 8 тимчасових DOM-карток із довшою назвою: однакова висота, співвідношення зображень 16:10, кілька рядків. Тестові партнери не записувалися у HTML.
- Нові сторінки та їхній header не мають горизонтального переповнення на перевірених ширинах.
- Burger відкривається, показує Kontakt/Контакты, закривається Escape; виконано реальний перехід з mobile-меню до Partnerzy та PL → RU через мовний перемикач.
- Desktop hover картки: translateY(-2px); фокус клавіатури та reduced-motion передбачено CSS.
- Візуально переглянуто screenshot-и desktop/tablet/mobile.

**Наявна проблема поза завданням:** `/ru/` на 320 px має scrollWidth 372 px. Те саме відтворено з початковими HTML/CSS із HEAD (до змін). Меню не переповнюється; контент головної сторінки не змінювався.

## Додавання наступного партнера

Скопіюйте весь `<a class="partner-card">…</a>` у `.partners-grid` обох мовних сторінок. Замініть URL, локальне зображення, його реальні width/height, alt, назву та категорію/місто. Зберігайте цілісний зовнішній link і бейдж партнера. Для фотографії замість логотипу можна лишити object-fit: contain; блок зображення завжди 16:10. Новий CSS для кожного партнера не потрібний.

## Створені файли

- `partnerzy/index.html`
- `ru/partnerzy/index.html`
- `css/partnerzy.css`
- `img/partnerzy/annvi-kosmetologia-podologia-wroclaw-logo.webp`
- `docs/partnerzy-report.md`

## Змінені файли

- `404.html`
- `blog/3000-nain-laser-historia-konstrukcja-serwis/index.html`
- `blog/5-oznak-wymiany-diody-w-laserze/index.html`
- `blog/beauty-planet-3d-contour-mozliwosci-serwis/index.html`
- `blog/dlaczego-maly-przewod-powoduje-duze-problemy/index.html`
- `blog/dlaczego-pala-sie-moduly-diodowe-w-laserach/index.html`
- `blog/dlaczego-warto-korzystac-z-profesjonalnego-serwisu/index.html`
- `blog/hifu-co-to-jest-jak-dziala-zastosowanie-serwis/index.html`
- `blog/index.html`
- `blog/pharaon-1470-historia-technologia-lasera/index.html`
- `blog/planowy-przeglad-lasera-diodowego-dlaczego-to-wazne/index.html`
- `blog/serwis-glowicy-lasera-diodowego-szczelnosc-optyka/index.html`
- `blog/uzywany-laser-diodowy-z-historia-serwisowa/index.html`
- `css/main.css`
- `index.html`
- `kontakt/index.html`
- `realizacje/beauty-planet-3d-contour-naprawa-przewodu-wroclaw/index.html`
- `realizacje/index.html`
- `realizacje/naprawa-3000-nain-bloku-zasilania/index.html`
- `realizacje/naprawa-alma-accent-gorlitz/index.html`
- `realizacje/naprawa-beauty-planet-3d-contour-wroclaw/index.html`
- `realizacje/naprawa-multipolar-rf-lublin/index.html`
- `realizacje/naprawa-nubway-nbw-vsiii-wroclaw/index.html`
- `realizacje/przeglad-estelase-power-p808l/index.html`
- `realizacje/przeglad-serwis-pharaon-1470-wroclaw/index.html`
- `realizacje/serwis-cavi-shape-advanced-wroclaw/index.html`
- `realizacje/serwis-glowicy-lasera-diodowego-poznan/index.html`
- `realizacje/serwis-gme-exsys-308/index.html`
- `realizacje/serwis-hifu-kimed-k1-w1601-gorlitz/index.html`
- `realizacje/serwis-lasera-diodowego-wymiana-glowicy-wroclaw/index.html`
- `realizacje/serwis-lasera-do-usuwania-tatuazu-wymiana-filtra/index.html`
- `ru/blog/3000-nain-lazer-istoriya-konstrukciya-servis/index.html`
- `ru/blog/5-priznakov-zameny-dioda-v-lazere/index.html`
- `ru/blog/beauty-planet-3d-contour-vozmozhnosti-servis/index.html`
- `ru/blog/hifu-chto-eto-kak-rabotaet-primenenie-servis/index.html`
- `ru/blog/index.html`
- `ru/blog/obsluzhivanie-manipuly-lazera-germetichnost-optika/index.html`
- `ru/blog/pharaon-1470-istoriya-lazernoy-tehnologii/index.html`
- `ru/blog/planovoe-obsluzhivanie-diodnogo-lazera-pochemu-eto-vazhno/index.html`
- `ru/blog/pochemu-malenkiy-kabel-sozdayot-bolshie-problemy/index.html`
- `ru/blog/pochemu-sgorayut-diodnye-moduli-v-lazerah/index.html`
- `ru/blog/pochemu-stoit-polzovatsya-professionalnym-servisom/index.html`
- `ru/blog/pochemu-vazhno-pokupat-lazer-s-istoriey-servisa/index.html`
- `ru/index.html`
- `ru/kontakt/index.html`
- `ru/realizacje/beauty-planet-3d-contour-naprawa-przewodu-wroclaw/index.html`
- `ru/realizacje/index.html`
- `ru/realizacje/naprawa-3000-nain-bloku-zasilania/index.html`
- `ru/realizacje/naprawa-alma-accent-gorlitz/index.html`
- `ru/realizacje/naprawa-beauty-planet-3d-contour-wroclaw/index.html`
- `ru/realizacje/naprawa-multipolar-rf-lublin/index.html`
- `ru/realizacje/naprawa-nubway-nbw-vsiii-wroclaw/index.html`
- `ru/realizacje/przeglad-estelase-power-p808l/index.html`
- `ru/realizacje/przeglad-serwis-pharaon-1470-wroclaw/index.html`
- `ru/realizacje/serwis-cavi-shape-advanced-wroclaw/index.html`
- `ru/realizacje/serwis-glowicy-lasera-diodowego-poznan/index.html`
- `ru/realizacje/serwis-gme-exsys-308/index.html`
- `ru/realizacje/serwis-hifu-kimed-k1-w1601-gorlitz/index.html`
- `ru/realizacje/serwis-lasera-diodowego-wymiana-glowicy-wroclaw/index.html`
- `ru/realizacje/serwis-lasera-do-usuwania-tatuazu-wymiana-filtra/index.html`
- `ru/uslugi/index.html`
- `sitemap.xml`
- `uslugi/index.html`

## git diff --stat

Звичайний git diff не враховує нові untracked-файли, перелічені вище. Файли не додавалися до staging.

```text
 404.html                                                                     |  4 ++++
 blog/3000-nain-laser-historia-konstrukcja-serwis/index.html                  |  4 ++++
 blog/5-oznak-wymiany-diody-w-laserze/index.html                              |  4 ++++
 blog/beauty-planet-3d-contour-mozliwosci-serwis/index.html                   |  4 ++++
 blog/dlaczego-maly-przewod-powoduje-duze-problemy/index.html                 |  4 ++++
 blog/dlaczego-pala-sie-moduly-diodowe-w-laserach/index.html                  |  4 ++++
 blog/dlaczego-warto-korzystac-z-profesjonalnego-serwisu/index.html           |  4 ++++
 blog/hifu-co-to-jest-jak-dziala-zastosowanie-serwis/index.html               |  4 ++++
 blog/index.html                                                              |  4 ++++
 blog/pharaon-1470-historia-technologia-lasera/index.html                     |  4 ++++
 blog/planowy-przeglad-lasera-diodowego-dlaczego-to-wazne/index.html          |  4 ++++
 blog/serwis-glowicy-lasera-diodowego-szczelnosc-optyka/index.html            |  4 ++++
 blog/uzywany-laser-diodowy-z-historia-serwisowa/index.html                   |  4 ++++
 css/main.css                                                                 | 11 ++++++++---
 index.html                                                                   |  4 ++++
 kontakt/index.html                                                           |  4 ++++
 realizacje/beauty-planet-3d-contour-naprawa-przewodu-wroclaw/index.html      |  4 ++++
 realizacje/index.html                                                        |  4 ++++
 realizacje/naprawa-3000-nain-bloku-zasilania/index.html                      |  4 ++++
 realizacje/naprawa-alma-accent-gorlitz/index.html                            |  4 ++++
 realizacje/naprawa-beauty-planet-3d-contour-wroclaw/index.html               |  4 ++++
 realizacje/naprawa-multipolar-rf-lublin/index.html                           |  4 ++++
 realizacje/naprawa-nubway-nbw-vsiii-wroclaw/index.html                       |  4 ++++
 realizacje/przeglad-estelase-power-p808l/index.html                          |  4 ++++
 realizacje/przeglad-serwis-pharaon-1470-wroclaw/index.html                   |  4 ++++
 realizacje/serwis-cavi-shape-advanced-wroclaw/index.html                     |  4 ++++
 realizacje/serwis-glowicy-lasera-diodowego-poznan/index.html                 |  4 ++++
 realizacje/serwis-gme-exsys-308/index.html                                   |  4 ++++
 realizacje/serwis-hifu-kimed-k1-w1601-gorlitz/index.html                     |  4 ++++
 realizacje/serwis-lasera-diodowego-wymiana-glowicy-wroclaw/index.html        |  4 ++++
 realizacje/serwis-lasera-do-usuwania-tatuazu-wymiana-filtra/index.html       |  4 ++++
 ru/blog/3000-nain-lazer-istoriya-konstrukciya-servis/index.html              |  4 ++++
 ru/blog/5-priznakov-zameny-dioda-v-lazere/index.html                         |  4 ++++
 ru/blog/beauty-planet-3d-contour-vozmozhnosti-servis/index.html              |  4 ++++
 ru/blog/hifu-chto-eto-kak-rabotaet-primenenie-servis/index.html              |  4 ++++
 ru/blog/index.html                                                           |  4 ++++
 ru/blog/obsluzhivanie-manipuly-lazera-germetichnost-optika/index.html        |  4 ++++
 ru/blog/pharaon-1470-istoriya-lazernoy-tehnologii/index.html                 |  4 ++++
 ru/blog/planovoe-obsluzhivanie-diodnogo-lazera-pochemu-eto-vazhno/index.html |  4 ++++
 ru/blog/pochemu-malenkiy-kabel-sozdayot-bolshie-problemy/index.html          |  4 ++++
 ru/blog/pochemu-sgorayut-diodnye-moduli-v-lazerah/index.html                 |  4 ++++
 ru/blog/pochemu-stoit-polzovatsya-professionalnym-servisom/index.html        |  4 ++++
 ru/blog/pochemu-vazhno-pokupat-lazer-s-istoriey-servisa/index.html           |  4 ++++
 ru/index.html                                                                |  4 ++++
 ru/kontakt/index.html                                                        |  4 ++++
 ru/realizacje/beauty-planet-3d-contour-naprawa-przewodu-wroclaw/index.html   |  4 ++++
 ru/realizacje/index.html                                                     |  4 ++++
 ru/realizacje/naprawa-3000-nain-bloku-zasilania/index.html                   |  4 ++++
 ru/realizacje/naprawa-alma-accent-gorlitz/index.html                         |  4 ++++
 ru/realizacje/naprawa-beauty-planet-3d-contour-wroclaw/index.html            |  4 ++++
 ru/realizacje/naprawa-multipolar-rf-lublin/index.html                        |  4 ++++
 ru/realizacje/naprawa-nubway-nbw-vsiii-wroclaw/index.html                    |  4 ++++
 ru/realizacje/przeglad-estelase-power-p808l/index.html                       |  4 ++++
 ru/realizacje/przeglad-serwis-pharaon-1470-wroclaw/index.html                |  4 ++++
 ru/realizacje/serwis-cavi-shape-advanced-wroclaw/index.html                  |  4 ++++
 ru/realizacje/serwis-glowicy-lasera-diodowego-poznan/index.html              |  4 ++++
 ru/realizacje/serwis-gme-exsys-308/index.html                                |  4 ++++
 ru/realizacje/serwis-hifu-kimed-k1-w1601-gorlitz/index.html                  |  4 ++++
 ru/realizacje/serwis-lasera-diodowego-wymiana-glowicy-wroclaw/index.html     |  4 ++++
 ru/realizacje/serwis-lasera-do-usuwania-tatuazu-wymiana-filtra/index.html    |  4 ++++
 ru/uslugi/index.html                                                         |  4 ++++
 sitemap.xml                                                                  | 12 ++++++++++++
 uslugi/index.html                                                            |  4 ++++
 63 files changed, 264 insertions(+), 3 deletions(-)
```

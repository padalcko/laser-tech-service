# Peltier + Nd:YAG — звіт про локальну реалізацію

Дата перевірки: 2026-10-19. Commit, push і deploy не виконувалися.

## Обсяг та джерела

Створено реалізацію і статтю блогу польською та російською. Російський текст реалізації взято з останнього повідомлення користувача (збережено позначення ND); повний текст блогу — з вкладеного файлу. Польські переклади зберігають структуру та всі факти. Тексти не скорочено. Не додано марку, модель, місто, виміряні параметри чи причинний зв’язок між підключенням маніпул і несправністю ND:YAG.

Використано чинні статичні HTML-сторінки, спільні CSS, навігацію, футер, соціальне меню та JS перегляду фото. Нової архітектури чи глобальних стилів немає.

## Маршрути (підготовлені локально, не опубліковані)

- case PL: https://lasertechservice.pl/realizacje/wymiana-peltiera-naprawa-lasera-nd-yag/
- case RU: https://lasertechservice.pl/ru/realizacje/zamena-pelte-remont-lazera-nd-yag/
- blog PL: https://lasertechservice.pl/blog/podlaczenie-glowic-przegrzewanie-kalibracja-nd-yag/
- blog RU: https://lasertechservice.pl/ru/blog/podklyuchenie-manipul-peregrev-kalibrovka-nd-yag/

## Фотографії

Джерело: `~/Downloads/laser-tech-service-ndyag-zdjecia-webp.zip`. Усі вісім фото використано в галереї реалізації. Головне фото — спеціаліст у футболці LTS (п’ятий рядок нижче). У блозі три компактні фото біля відповідних розділів. Картки блогу без зображень.

Оригінальні пропорції 9:16 збережені у статтях і галереї. Доступний перегляд збільшеного фото. Для кожного зображення створено WebP 480×853, 768×1365 і 1152×2048; EXIF не переносився. У HTML задано width/height, srcset, sizes, локалізовані alt, lazy loading нижче hero. 24 файли сумарно займають 3 331 568 байтів.

Деякі назви файлів архіву помилково описували епіляційну головку як ND:YAG. Назви нових активів і alt уточнено за видимим вмістом, без приписування фотографії результатів вимірювань.

| Файл у ZIP | Файл у `img/realizacje/peltier-nd-yag/` |
|---|---|
| `laser-nd-yag-modul-optyczny-kontrola.webp` | `glowica-do-depilacji-powierzchnia-kontaktowa.webp` |
| `laser-nd-yag-panel-sterowania-diagnostyka.webp` | `panel-aparatu-tryb-nd-yag.webp` |
| `laser-nd-yag-serwis-w-salonie-kosmetycznym.webp` | `aparat-dwie-glowice-serwis.webp` |
| `laser-nd-yag-ustawienia-energii-czestotliwosci.webp` | `ekran-nd-yag-energia-czestotliwosc.webp` |
| `laser-tech-service-serwis-glowicy-nd-yag-technician.webp` | `specjalista-laser-tech-service-naprawa-nd-yag.webp` |
| `naprawa-glowicy-nd-yag-okablowanie.webp` | `glowica-depilacja-odsloniete-przewody.webp` |
| `naprawa-manipuly-lasera-nd-yag-przewody.webp` | `serwis-manipuly-nd-yag.webp` |
| `serwis-laser-nd-yag-modul-wewnetrzny.webp` | `glowica-depilacja-wnetrze-obudowy.webp` |

Кожен файл також має варіанти `-480w.webp` та `-768w.webp`.

## SEO та AI

- Унікальні title/description, canonical, взаємні hreflang PL/RU/x-default, OG і Twitter для чотирьох сторінок.
- Один H1 на сторінку, Article/BlogPosting та BreadcrumbList.
- Чотири нові sitemap URL; усі попередні записи залишено без змін.
- Картки у чотирьох мовних списках; взаємні посилання між блогом і реалізацією, на діагностику, відновлення головок, техобслуговування та контакт.
- AI-ресурси згенеровано існуючим `scripts/build-ai-search.py`: нові index.md, оновлені індекси, llms.txt, llms-full.txt і правила _headers.
- robots.txt, головні сторінки, CSS, JS, форми та інтеграції не змінювалися.

## Перевірки

- `python3 scripts/build-ai-search.py --check`: stale = [].
- `python3 scripts/check-ai-search.py`: issues = {}; 104 sitemap URL, 104 Markdown-ресурси, 12 085 посилань перевірено.
- `python3 scripts/check-geo-seo.py`: issues = {}.
- `git diff --check`: без помилок.
- Окрема перевірка чотирьох сторінок: 278 текстових блоків/пунктів збережені в правильному порядку, 298 локальних посилань/ресурсів, 24 входження фото; canonical, hreflang, schema, фото, спільне меню та футер узгоджені.
- Chrome/Playwright через локальний HTTP: усі чотири сторінки на 320, 375, 390, 768, 1024, 1440 px; чотири списки на 320 і 1440 px. Немає горизонтального overflow чи незавантажених фото.
- Локальне спостереження Layout Instability API під час завантаження і прокручування: максимум 0.000750 для 24 перевірок нових сторінок; це не production CWV.
- Перемикач мов веде на відповідну сторінку, мобільне меню відкривається, фото відкриваються у dialog і закриваються Escape. JavaScript pageerror = [].

Зовнішні запити аналітики блокувалися лише у тестовому браузері, код інтеграцій збережено. Перевірки стосуються локального сайту; production, Lighthouse, реальні Core Web Vitals, доставка форм і аналітика не перевірялися.

## Файли

Нові HTML + згенеровані Markdown:

- `realizacje/wymiana-peltiera-naprawa-lasera-nd-yag/index.html`
- `realizacje/wymiana-peltiera-naprawa-lasera-nd-yag/index.md`
- `ru/realizacje/zamena-pelte-remont-lazera-nd-yag/index.html`
- `ru/realizacje/zamena-pelte-remont-lazera-nd-yag/index.md`
- `blog/podlaczenie-glowic-przegrzewanie-kalibracja-nd-yag/index.html`
- `blog/podlaczenie-glowic-przegrzewanie-kalibracja-nd-yag/index.md`
- `ru/blog/podklyuchenie-manipul-peregrev-kalibrovka-nd-yag/index.html`
- `ru/blog/podklyuchenie-manipul-peregrev-kalibrovka-nd-yag/index.md`

Нові фото: 24 WebP у `img/realizacje/peltier-nd-yag/` (назви вище).

Оновлені файли:

- `_headers`
- `blog/index.html`
- `blog/index.md`
- `llms-full.txt`
- `llms.txt`
- `realizacje/index.html`
- `realizacje/index.md`
- `ru/blog/index.html`
- `ru/blog/index.md`
- `ru/realizacje/index.html`
- `ru/realizacje/index.md`
- `sitemap.xml`

Додано цей звіт: `docs/peltier-nd-yag-report.md`. Тимчасові аудит-скрипти, JSON-результати й скриншоти: `/tmp/lts-ndyag/`.

## Обмеження та статус

Критичних проблем у локальних перевірках не виявлено. Публікація не виконувалася; URL вище описують майбутні адреси після deploy.

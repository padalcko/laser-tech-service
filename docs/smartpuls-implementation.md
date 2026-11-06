# smartPULS IPL — Świdnica: звіт інтеграції

Створено рівно шість HTML-сторінок за шаблонами Варшавської реалізації та статті. Усі шість наданих текстів звірено з оригінальним вкладенням без зміни жодного слова. Виділення збережені, наданий абзац часу читання перенесено до метаданих біля H1. Дата публікації матеріалів — 2026-11-06; дата ремонту не вигадувалася.

## Адреси й час читання
- case pl: https://lasertechservice.pl/realizacje/smartpuls-ipl-swidnica/ — 2 хв.
- case ru: https://lasertechservice.pl/ru/realizacje/smartpuls-ipl-svidnica/ — 2 хв.
- case en: https://lasertechservice.pl/en/case-studies/smartpuls-ipl-swidnica/ — 2 хв.
- blog pl: https://lasertechservice.pl/blog/smartpuls-ipl-linux-30000-impulsow/ — 5 хв.
- blog ru: https://lasertechservice.pl/ru/blog/smartpuls-ipl-linux-30000-vspyshek/ — 5 хв.
- blog en: https://lasertechservice.pl/en/blog/smartpuls-ipl-linux-30000-pulses/ — 5 хв.

Час — надані користувачем орієнтовні значення. Наявний build-blog-reading-times.py зберігає задані оцінки в картках; нову систему обчислення не додано.

## Фотографії

Використано три оригінали HEIC, SHA-256 до/після збігаються. Два додаткові JPG не підміняють оригінали. Легка корекція яскравості й контрасту ×1.02, без генерації, кадрування або зміни деталей. Watermark не додано: обрані еталони використовують фото без нього. 18 WebP шириною 320/480/640/768/960/1280 px; разом 1 252 666 байтів; EXIF/XMP/ICC вилучено.

- IMG_8453.heic → smartpuls-ipl-device-service-swidnica.webp; оригінал 3213×5712; WebP 1280×2276.
- IMG_8454.heic → smartpuls-ipl-handpiece-lamp-repair-swidnica.webp; оригінал 2268×4032; WebP 1280×2276.
- IMG_8455.heic → smartpuls-ipl-linux-boot-kws-laser-tech-service.webp; оригінал 3213×5712; WebP 1280×2276.

Реалізація: маніпула + апарат. Блог: Linux + апарат + маніпула. ALT локалізовані й описують видиме; повний кадр збережений у файлах. Галерея використовує чинний переглядач. Головне фото має eager/high, другорядні — lazy, усі мають width/height/srcset/sizes.

## SEO/GEO

- Унікальні title/description; один H1, H2 за текстом.
- Абсолютний self-canonical, взаємні PL/RU/EN hreflang, x-default PL.
- OG/Twitter, og:locale і дві og:locale:alternate, тематичне OG image.
- Article / BlogPosting, BreadcrumbList, Organization; JSON-LD валідний.
- contentLocation: Świdnica, Dolnośląskie, PL; жодного вигаданого офісу.
- Посилання на відповідні мовні сторінки IPL, діагностики, відновлення маніпул, електроніки; взаємні кейс ↔ блог.
- Sitemap, Markdown, AI catalog, llms і _headers оновлено чинними генераторами.
- FAQPage, рейтинги, вимірювання не додано.

## Перевірки

- build-site.py — PASS: мовний реєстр, навігація, AI-search, GEO/SEO, ціни.
- check-smartpuls.py — PASS: повнота текстів, читання, 18 WebP, SEO/JSON-LD, посилання, картки, незмінність хедера/футера/скриптів проти еталона.
- build-ai-search.py --check — PASS: 258 сторінок, stale: [].
- check-ai-catalog.py — PASS: freshness, mutation tests, read-only checks.
- git diff --check — PASS.
- Chrome: 30 макетів (6 сторінок × 320/375/430/768/1440), 75 завантажень фото, 6 відкриттів галереї, 12 мовних переходів, 18 перевірок мобільного меню, 6 переходів із карток.
- Окремо: 6 кліків CTA до контактів, 6 переходів кейс ↔ блог; CTA не обрізані на 320 px.
- Немає горизонтального переповнення, білої смуги перед футером, JS/локальних HTTP-помилок. Телефон/email/WhatsApp перевірено за href, без активації або надсилання повідомлень.
- Візуально переглянуто desktop PL case і mobile RU blog.

## Продуктивність

Локальні заміри Chrome, три повтори на маршрут/ширину, зовнішні запити блоковано. Медіана LCP PL case: 172/184 ms на 375/1440; еталон 196/188 ms. PL blog: 176/168 ms; еталон 164/176 ms. Максимальний CLS нових сторінок 0.000373. Це лабораторні локальні виміри, не Lighthouse і не польові метрики.

## Створені файли
- realizacje/smartpuls-ipl-swidnica/index.html
- realizacje/smartpuls-ipl-swidnica/index.md
- ru/realizacje/smartpuls-ipl-svidnica/index.html
- ru/realizacje/smartpuls-ipl-svidnica/index.md
- en/case-studies/smartpuls-ipl-swidnica/index.html
- en/case-studies/smartpuls-ipl-swidnica/index.md
- blog/smartpuls-ipl-linux-30000-impulsow/index.html
- blog/smartpuls-ipl-linux-30000-impulsow/index.md
- ru/blog/smartpuls-ipl-linux-30000-vspyshek/index.html
- ru/blog/smartpuls-ipl-linux-30000-vspyshek/index.md
- en/blog/smartpuls-ipl-linux-30000-pulses/index.html
- en/blog/smartpuls-ipl-linux-30000-pulses/index.md
- content/smartpuls-texts.json
- content/smartpuls-routes.json
- content/smartpuls-meta.json
- scripts/check-smartpuls.py
- scripts/check-smartpuls.cjs
- img/realizacje/smartpuls-swidnica/image-audit.json
- docs/smartpuls-implementation.md
- img/realizacje/smartpuls-swidnica/smartpuls-ipl-device-service-swidnica-320w.webp
- img/realizacje/smartpuls-swidnica/smartpuls-ipl-device-service-swidnica-480w.webp
- img/realizacje/smartpuls-swidnica/smartpuls-ipl-device-service-swidnica-640w.webp
- img/realizacje/smartpuls-swidnica/smartpuls-ipl-device-service-swidnica-768w.webp
- img/realizacje/smartpuls-swidnica/smartpuls-ipl-device-service-swidnica-960w.webp
- img/realizacje/smartpuls-swidnica/smartpuls-ipl-device-service-swidnica.webp
- img/realizacje/smartpuls-swidnica/smartpuls-ipl-handpiece-lamp-repair-swidnica-320w.webp
- img/realizacje/smartpuls-swidnica/smartpuls-ipl-handpiece-lamp-repair-swidnica-480w.webp
- img/realizacje/smartpuls-swidnica/smartpuls-ipl-handpiece-lamp-repair-swidnica-640w.webp
- img/realizacje/smartpuls-swidnica/smartpuls-ipl-handpiece-lamp-repair-swidnica-768w.webp
- img/realizacje/smartpuls-swidnica/smartpuls-ipl-handpiece-lamp-repair-swidnica-960w.webp
- img/realizacje/smartpuls-swidnica/smartpuls-ipl-handpiece-lamp-repair-swidnica.webp
- img/realizacje/smartpuls-swidnica/smartpuls-ipl-linux-boot-kws-laser-tech-service-320w.webp
- img/realizacje/smartpuls-swidnica/smartpuls-ipl-linux-boot-kws-laser-tech-service-480w.webp
- img/realizacje/smartpuls-swidnica/smartpuls-ipl-linux-boot-kws-laser-tech-service-640w.webp
- img/realizacje/smartpuls-swidnica/smartpuls-ipl-linux-boot-kws-laser-tech-service-768w.webp
- img/realizacje/smartpuls-swidnica/smartpuls-ipl-linux-boot-kws-laser-tech-service-960w.webp
- img/realizacje/smartpuls-swidnica/smartpuls-ipl-linux-boot-kws-laser-tech-service.webp

## Оновлені файли
- _headers
- ai-catalog.json
- blog/index.html
- blog/index.md
- en/blog/index.html
- en/blog/index.md
- en/case-studies/index.html
- en/case-studies/index.md
- llms-full.txt
- llms.txt
- realizacje/index.html
- realizacje/index.md
- ru/blog/index.html
- ru/blog/index.md
- ru/realizacje/index.html
- ru/realizacje/index.md
- scripts/site-locales.json
- sitemap.xml

## Межі й стан

Глобальні CSS/JS, header/footer, мовна архітектура, соціальне меню, аналітика й Лазар не змінювалися. Попередні локальні виправлення білої смуги трьох Варшавських статей збережено без змін.

Невирішених помилок у виконаних перевірках немає. Production, індексацію й зовнішню доставку звернень не перевіряли. Усі зміни локальні; commit/push/deploy не виконувалися.

## Уточнення CTA користувачем

CTA блогу PL/RU/EN оформлено за еталоном статті про згорілі діодні модулі: заголовок, пояснення, кнопки Контакти й WhatsApp. За прямою вказівкою користувача прибрано дубльований абзац Laser Tech Service / телефон / email з трьох CTA блогу; оригінальний наданий текст збережено у content/smartpuls-texts.json. Це погоджений виняток із початкової вимоги незмінності текстів.

## Оновлення за еталоном Pharaon 1470

Три реалізації smartPULS перероблено за локалізованими сторінками przeglad-serwis-pharaon-1470-wroclaw: hero з моделлю й вступом, case-info, case-work-grid, case-result та точний локалізований CTA еталона. Фото апарата повторно використано в hero і секції робіт; Linux залишається тільки в блозі. Дубльовані контакти видалено за вказівкою користувача.

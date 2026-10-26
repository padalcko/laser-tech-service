# Заміна згорілого лазерного діода: PL / RU / EN

26.10.2026. Зміни локальні. Commit, push, deploy не виконані. Facebook не змінювався.

## Інспекція

Початкове робоче дерево чисте. Наявні матеріали про залитий діодний модуль та причини відмов описують інші випадки; дубліката цього ремонту не було. Еталони: реалізації LightSheer DESIRE та статті про Peltier у кожній мові. Збережено CSS, header/footer, текстові картки блогу, компактну галерею і її переглядач. Нових CSS-файлів немає.

## Шість URL та SEO

URL нижче — адреси після публікації; їх наявність у production не перевірена.

### Реалізація PL

- URL: https://lasertechservice.pl/realizacje/wymiana-spalonej-diody-laserowej/
- Title: Wymiana spalonej diody — naprawa głowicy | Laser Tech Service
- Description: Wymiana spalonej diody laserowej w Laser Tech Service: rozmontowanie głowicy, demontaż uszkodzonego elementu i montaż sprawnej diody. Głowica ponownie działa.

### Блог PL

- URL: https://lasertechservice.pl/blog/spalona-dioda-laserowa-naprawa-glowicy/
- Title: Spalona dioda laserowa: naprawa czy nowa głowica?
- Description: Czy spalona dioda oznacza konieczność zakupu nowej głowicy? Poznaj rzeczywisty przypadek wymiany diody i możliwości naprawy manipuły w Laser Tech Service.

### Реалізація RU

- URL: https://lasertechservice.pl/ru/realizacje/zamena-sgorevshego-lazernogo-dioda/
- Title: Замена сгоревшего диода — ремонт манипулы | Laser Tech Service
- Description: Замена сгоревшего лазерного диода в Laser Tech Service: разборка манипулы, демонтаж неисправного элемента и установка исправного. Манипула снова работает.

### Блог RU

- URL: https://lasertechservice.pl/ru/blog/sgorel-lazernyy-diod-remont-manipuly/
- Title: Сгорел лазерный диод: ремонт или новая манипула?
- Description: Нужна ли новая манипула, если сгорел лазерный диод? Реальный случай замены диода, результат ремонта и выбор между ремонтом и заменой манипулы.

### Реалізація EN

- URL: https://lasertechservice.pl/en/case-studies/burned-out-laser-diode-replacement/
- Title: Burned-Out Laser Diode Replacement | Laser Tech Service
- Description: Laser Tech Service replaced a burned-out diode: the handpiece was disassembled, the failed diode removed and a working replacement installed. It works again.

### Блог EN

- URL: https://lasertechservice.pl/en/blog/burned-out-laser-diode-handpiece-repair/
- Title: Burned-Out Laser Diode: Repair or Replace the Handpiece?
- Description: Does a burned-out laser diode mean you need a new handpiece? Explore a real diode replacement, the repair outcome and what to consider before replacement.

## WebP

Окремі файли доступні, ZIP не знадобився. Усі мови використовують ті самі чотири файли в `img/realizacje/wymiana-spalonej-diody-laserowej/`. SHA-256 кожної копії збігається з джерелом: повторного стиснення немає. Розміри перевірено sips.

| Файл | Вміст | Розміри | Байтів | KiB |
|---|---|---|---:|---:|
| serwis-laserow-wymiana-diody-laserowej.webp | Спеціаліст за роботою | 864 × 1536 | 311452 | 304.2 |
| wymiana-spalonej-diody-laserowej.webp | Окремий модуль діода | 864 × 1536 | 145002 | 141.6 |
| naprawa-glowicy-laserowej-wymiana-diody.webp | Розібрана маніпула | 864 × 1536 | 354796 | 346.5 |
| regeneracja-laserow-naprawa-manipuly.webp | Внутрішні компоненти | 864 × 1536 | 211076 | 206.1 |

Картки реалізацій PL/RU/EN використовують фото спеціаліста, який розбирає маніпулу, зі штатним object-fit: cover, як сусідні картки. Детальні сторінки — всі чотири фото; статті — компактні фото модуля і спеціаліста. Картки блогу без фото. Alt локалізовано, width/height задані, головне фото реалізації eager, інші lazy. Фото реалізацій оформлено за еталоном Peltier/Nd:YAG: головне фото природної висоти, галерея 9:16 без порожніх полів і обрізання. Переглядач повного фото збережено.

## Внутрішні посилання

Реалізації посилаються на відповідні статті й три послуги. Статті містять контекстні посилання на заміну діодів і свою реалізацію, а також список послуг. CTA ведуть на ремонт головок або локалізовані контакти.

### PL

- https://lasertechservice.pl/uslugi/wymiana-i-kalibracja-diod-laserowych/
- https://lasertechservice.pl/uslugi/regeneracja-glowic-i-manipulatorow/
- https://lasertechservice.pl/uslugi/diagnostyka-laserow-diodowych/

### RU

- https://lasertechservice.pl/ru/uslugi/zamena-i-kalibrovka-lazernyh-diodov/
- https://lasertechservice.pl/ru/uslugi/vosstanovlenie-golovok-i-manipul/
- https://lasertechservice.pl/ru/uslugi/diagnostika-diodnyh-lazerov/

### EN

- https://lasertechservice.pl/en/services/laser-diode-replacement-calibration/
- https://lasertechservice.pl/en/services/laser-handpiece-repair/
- https://lasertechservice.pl/en/services/diode-laser-diagnostics/

## SEO, мови та індекси

- Один H1, унікальні метадані, canonical, OG/Twitter, breadcrumbs і BreadcrumbList. Article для реалізацій, BlogPosting для статей.
- Взаємні pl-PL, ru-RU, en, x-default (PL) на шести нових сторінках і в sitemap. Необов’язкове поле hreflang в registry зберігає старий контракт pl/ru/en для інших сторінок. Генератор Markdown/llms бере переклади з registry, щоб регіональні теги не приховували мовні відповідники.
- Перемикачі згенеровано штатним скриптом: PL/RU/EN ведуть на той самий матеріал, а не на головні сторінки.
- У registry published означає включення в локальну збірку й індекси; deploy не відбувся.
- Sitemap має 201 унікальний URL, додано шість; старі маршрути збережені. Sitemap підтримується як вихідний XML: окремого генератора в build pipeline немає.
- Штатні генератори оновили шість нових index.md, Markdown шести каталогів, llms.txt, llms-full.txt, ai-catalog.json і _headers. robots.txt незмінний.

## Перевірки

- `python3 scripts/build-site.py` — PASS: локалі, перемикачі, AI/Markdown, GEO/SEO та штатні перевірки цін.
- `python3 scripts/check-burned-diode.py` — PASS: шість сторінок і карток, регіональні теги, Markdown-переклади, schema, фото та незмінний контракт старих локалей.
- `python3 scripts/check-ai-catalog.py` — PASS, включно з mutation checks.
- `python3 scripts/build-ai-search.py --check` і `python3 scripts/build-ai-catalog.py --check` — PASS.
- Фінальний загальний AI-check: 202 HTML, 201 Markdown, 25 483 перевірених посилань, 445 JSON-LD блоків; issues: {}. GEO/SEO: 201 сторінка, 272 FAQ; issues: {}.
- Chrome/Playwright: шість нових сторінок + шість каталогів, 72 перевірки ширин 320/360/390/430/768/1440 px. Після завершення зміни viewport горизонтального скролу немає. Фото декодуються; JS pageerror: 0.
- Перемикачі відкриваються і містять правильні три URL. Нові сторінки та внутрішні посилання з main повертають локальний HTTP 200.
- Усі 12 мініатюр галерей відкривають повне фото і закриваються Escape.
- Lazar відкривається/закривається на шести сторінках. Англійська версія зберігає штатний data-sending-enabled=false. Повідомлення не надсилались.
- Header (крім мовних цільових URL), footer та аналітика збігаються з мовними еталонами. CSS, main.js, case-gallery.js, lazar-ai.js, robots.txt і partnerzy/index.html/index.md побайтово незмінні щодо HEAD.
- `git diff --check` — PASS.

Докази: `/tmp/lts-diode/browser.json`, скриншоти `/tmp/lts-diode/page-*-390.png` і `page-*-1440.png`. Візуально переглянуто мобільну PL реалізацію, десктопну EN реалізацію та мобільну RU статтю.

Межі: локальні HTTP/Chrome і статичні тести. Зовнішні запити в браузері заблоковані. Production, backend Lazar, доставку заявок, аналітику та Lighthouse/CWV не перевіряли.

## Файли

Змінені:

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
- `scripts/build-ai-search.py`
- `scripts/site-locales.json`
- `scripts/site_locales.py`
- `sitemap.xml`

Створені:

- `blog/spalona-dioda-laserowa-naprawa-glowicy/index.html`
- `blog/spalona-dioda-laserowa-naprawa-glowicy/index.md`
- `docs/burned-diode-report.md`
- `en/blog/burned-out-laser-diode-handpiece-repair/index.html`
- `en/blog/burned-out-laser-diode-handpiece-repair/index.md`
- `en/case-studies/burned-out-laser-diode-replacement/index.html`
- `en/case-studies/burned-out-laser-diode-replacement/index.md`
- `img/realizacje/wymiana-spalonej-diody-laserowej/naprawa-glowicy-laserowej-wymiana-diody.webp`
- `img/realizacje/wymiana-spalonej-diody-laserowej/regeneracja-laserow-naprawa-manipuly.webp`
- `img/realizacje/wymiana-spalonej-diody-laserowej/serwis-laserow-wymiana-diody-laserowej.webp`
- `img/realizacje/wymiana-spalonej-diody-laserowej/wymiana-spalonej-diody-laserowej.webp`
- `realizacje/wymiana-spalonej-diody-laserowej/index.html`
- `realizacje/wymiana-spalonej-diody-laserowej/index.md`
- `ru/blog/sgorel-lazernyy-diod-remont-manipuly/index.html`
- `ru/blog/sgorel-lazernyy-diod-remont-manipuly/index.md`
- `ru/realizacje/zamena-sgorevshego-lazernogo-dioda/index.html`
- `ru/realizacje/zamena-sgorevshego-lazernogo-dioda/index.md`
- `scripts/check-burned-diode.py`

## Рекомендований коміт

`feat: add laser diode replacement case and articles in PL RU EN`

Опис: додано фактичну реалізацію заміни згорілого діода й технічну статтю трьома мовами, картки, чотири оригінальні WebP, внутрішні посилання, SEO/schema та мовні відповідники; оновлено sitemap і згенеровані AI/Markdown-ресурси. Дизайн, аналітика й Lazar збережені. Перевірено статичними валідаторами та локальним Chrome на 320–1440 px.

Коміт не створено. Push і deploy не виконано.

# Stage 3C — English Case Studies & Technical Blog

Дата: 2026-10-22. Робота виконана локально поверх незакомічених Stage 1/2A/2B/3A. Commit, push, deploy і відновлення до HEAD не виконувалися.

## Результат і фактичний початковий стан

Створено 45 EN HTML та 45 відповідних Markdown: 22 реалізації, 21 стаття і два індекси. Stage 3A вже був у файлах: 15 EN посадкових послуг. Stage 3B не був реалізований: міжнародні маршрути залишено planned, нових міжнародних сторінок немає.

| Показник | До Stage 3C | Після |
|---|---:|---:|
| Канонічні сторінки / sitemap / Markdown | 148 | 193 |
| PL / RU / EN | 65 / 65 / 18 | 65 / 65 / 63 |
| HTML разом із 404 | 149 | 194 |
| EN planned | 50 | 5 |
| AI Catalog: послуги | 15 | 15 |
| AI Catalog: мовні записи статей | 42 | 63 |
| AI Catalog: мовні записи кейсів | 44 | 66 |

Published означає стан локального реєстру, а не фактичний deploy. П'ять planned EN маршрутів — pricing, partners і три international-service.

## Джерела, переклад і збереження фактів

Використано поточні PL/RU статті та реалізації, реєстр маршрутів і service-cases.json. Структура і повний зміст EN базуються на PL-джерелах; збережено технічні застереження, моделі, міста, симптоми, ремонтні дії й результати. Відсутні в джерелах вимірювання або компоненти не додавалися. Невстановлений виробник CO₂-апарата та інші нейтральні назви не підмінялися припущеннями.

Порівняння числових значень основного тексту PL/RU виявило редакційні відмінності в HIFU, Złota Firma і Pharaon: повторення глибин/року в тексті, словесне «кінець першого десятиліття XXI століття» проти «2000-х», 2ring проти «двухкольцевой». Ці відмінності не використані для створення нових характеристик. Для EN використано British English, десяткові крапки й англійські розділювачі тисяч; величини та PLN-суми збережені. Дати ISO у schema і datetime збігаються з PL.

PL/RU основний HTML-контент усіх 45 груп побайтово збігається зі знімком перед Stage 3C. CSS, JS, оригінальні зображення й відеофайли не змінювалися. Жоден файл початкового знімка не видалено. На PL/RU змінені мовні компоненти/SEO та похідні AI-ресурси, а не зміст статей.

Індекси повторюють чинний дизайн і порядок: 22 картки реалізацій із фото, 21 текстова картка блогу без додавання фотографій. Дати, медіа URL, srcset/sizes, dimensions, lazy loading і параметри iframe збережені. Alt, підписи, title та aria перекладені. Фотографії не дублювалися й не ретушувалися.

## SEO, навігація та AI

Усі 45 готових маршрутів переведено planned → published зі збереженням ID, PL/RU URL і x-default. Додано self-canonical, EN metadata, en_GB, BreadcrumbList, локалізований Article/BlogPosting та інші наявні схеми. Виправлено чотири відсутні BreadcrumbList лише в нових EN-версіях успадкованих шаблонів. HIFU FAQ schema узгоджено з видимим EN-текстом.

Оновлено взаємні hreflang-кластери 135 сторінок, sitemap і мовний dropdown штатним генератором. Усі наявні EN-меню та контекстні переходи використовують готові EN Blog/Case Studies. Посилання на неперекладені pricing/partners та польські матеріали позначені відповідно; planned маршрути не видаються за готові. Генератор service-cases використав нові EN-кейси у відповідних EN-послугах.

Markdown, llms.txt, llms-full.txt, _headers та AI Catalog згенеровані штатними інструментами. 42 попередні ID статей і 44 ID кейсів звірені з існуючими записами Git HEAD і збережені; нові записи є мовними ресурсами, а не новими бізнес-сутностями. Кількість бізнес-послуг залишилася 15. Виправлено лише актуальні очікувані кількості сторінок у попередніх EN-тестах.

## Перевірки

Успішно:

- Production build `PYTHONDONTWRITEBYTECODE=1 python3 scripts/build-site.py`, включно з перевірками реєстру, dropdown, AI search і GEO/SEO.
- Повторна збірка побайтово стабільна: порівняно 861 файл робочого дерева, змін немає.
- `check-english-content.py`: усі 45 нових сторінок, parity медіа/дат/полів, порядок індексів, EN посилання, schema і закритий EN-чат.
- `check-english-pages.py`: 193 канонічні сторінки / 63 EN, reciprocal SEO, 15 цін і контрактів послуг, форми, FAQ, відсутність planned-посилань.
- `check-ai-search.py`: 194 HTML, 24 408 перевірених посилань, 428 JSON-LD блоків; issues порожні. `check-geo-seo.py`: 193 сторінки, 272 FAQ questions, issues порожні.
- Freshness `--check` для build-ai-search, build-ai-catalog, build-service-cases і build-language-switcher: stale відсутні.
- `check-ai-catalog.py`: перевірки актуальності та контрольні зміни даних/маршрутів із відновленням файлів.
- `check-english-content.cjs`: 45 HTTP 200, 135 layout-сценаріїв (45 × 320/390/1440), завантаження зображень, фотодіалоги/Escape, dropdown/клавіатура, burger, вісім EN→RU→EN переходів, відсутність overflow і JS pageerror. Перевірено адреси/параметри відео; зовнішнє відтворення заблоковане.
- `check-english-pages.cjs`: усі 193 HTTP URL, дев'ять layout-сценаріїв, дві форми та gated EN Lazar з mock backend.
- `check-english-services.cjs`: 193 HTTP URL, 45 layouts, 15 mock-форм, мовні переходи, зображення та прихований чат.
- `check-english-content-form.cjs`: форма EN-статті про діодні модулі — required validation, loading, HTTP 500/success, точний payload, language=en і одна success-подія аналітики. Source збережений із PL-оригіналу; нові поля або consent, яких не було в джерельній формі, не додавалися.
- `check-lazar-ai.cjs`: 27 layout/scenario груп PL/RU/EN плюс storage denial, лише mock webhook.
- `check-language-runtime.cjs`: 47 груп та перемикання без JavaScript.
- `check-lightsheer-desire.py`, `check-cooling-maintenance.py`, `check-used-laser-buying.py`.
- `git diff --check`; Python cache відсутній.

Історичні одноразові аудити з очікуваннями старого HEAD/порядку карток (poznan, co2-poznan, pharaon, gme, rsl-laser-maintenance) не змінювалися й не входили до цього набору актуальних acceptance-тестів.

## Форми, Лазар і обмеження перевірки

Жодних реальних заявок або запитів до n8n не надсилалося. Endpoint, payload-контракти, session ID та події аналітики не змінені. Усі 63 EN HTML мають data-lazar-enabled=false; mock-тести вмикають чат лише в перехопленій відповіді тестового браузера. PL/RU поведінка перевірена наявними regression-тестами.

Backend EN і фактичне отримання заявок не підтверджені. Перед відкриттям EN-чату потрібна окремо погоджена перевірка workflow, мови відповідей і сесій. Live SEO, індексація, зовнішні відео, GA4/GTM delivery та production CWV не перевірялися. Зовнішні джерела статей збережені з оригіналів, а не заявлені як повторно перевірені на поточну дату.

У частині оригінальної інфографіки, зокрема HIFU та матеріалів про охолодження, є вбудовані польські написи. Їх збережено за вимогою не редагувати фото; HTML-підписи й alt англійські. Майбутня локалізація растрових написів потребує окремого завдання.

## Скриншоти та результати

32 основні скриншоти: обидва індекси, три статті та три кейси на 320/390/1440 px і full-page desktop. Додатково — mock-форма статті. Візуально переглянуто індекси та представницькі статтю/кейс, збережено поточну палітру й компоненти.

| Сторінка | 1440 | 390 | 320 | Full |
|---|---|---|---|---|
| Blog | [1440](qa/stage3c/blog-1440.png) | [390](qa/stage3c/blog-390.png) | [320](qa/stage3c/blog-320.png) | [full](qa/stage3c/blog-full.png) |
| Case Studies | [1440](qa/stage3c/case-studies-1440.png) | [390](qa/stage3c/case-studies-390.png) | [320](qa/stage3c/case-studies-320.png) | [full](qa/stage3c/case-studies-full.png) |
| HIFU | [1440](qa/stage3c/blog-hifu-technology-applications-service-1440.png) | [390](qa/stage3c/blog-hifu-technology-applications-service-390.png) | [320](qa/stage3c/blog-hifu-technology-applications-service-320.png) | [full](qa/stage3c/blog-hifu-technology-applications-service-full.png) |
| LightSheer guide | [1440](qa/stage3c/blog-lightsheer-desire-cooling-reliability-1440.png) | [390](qa/stage3c/blog-lightsheer-desire-cooling-reliability-390.png) | [320](qa/stage3c/blog-lightsheer-desire-cooling-reliability-320.png) | [full](qa/stage3c/blog-lightsheer-desire-cooling-reliability-full.png) |
| Diode modules | [1440](qa/stage3c/blog-why-laser-diode-modules-fail-1440.png) | [390](qa/stage3c/blog-why-laser-diode-modules-fail-390.png) | [320](qa/stage3c/blog-why-laser-diode-modules-fail-320.png) | [full](qa/stage3c/blog-why-laser-diode-modules-fail-full.png) |
| Estetech | [1440](qa/stage3c/case-studies-estetech-peltier-module-replacement-poznan-1440.png) | [390](qa/stage3c/case-studies-estetech-peltier-module-replacement-poznan-390.png) | [320](qa/stage3c/case-studies-estetech-peltier-module-replacement-poznan-320.png) | [full](qa/stage3c/case-studies-estetech-peltier-module-replacement-poznan-full.png) |
| GME | [1440](qa/stage3c/case-studies-gme-exsys-308-service-inspection-1440.png) | [390](qa/stage3c/case-studies-gme-exsys-308-service-inspection-390.png) | [320](qa/stage3c/case-studies-gme-exsys-308-service-inspection-320.png) | [full](qa/stage3c/case-studies-gme-exsys-308-service-inspection-full.png) |
| CO₂ Poznań | [1440](qa/stage3c/case-studies-urgent-co2-laser-repair-poznan-1440.png) | [390](qa/stage3c/case-studies-urgent-co2-laser-repair-poznan-390.png) | [320](qa/stage3c/case-studies-urgent-co2-laser-repair-poznan-320.png) | [full](qa/stage3c/case-studies-urgent-co2-laser-repair-poznan-full.png) |

[Browser results](qa/stage3c/results.json), [static audit](qa/stage3c/static-results.json), [article mock form](qa/stage3c/article-form.png), [article form results](qa/stage3c/article-form-results.json).

## Повний перелік 45 нових URL

### Індекс реалізацій

- https://lasertechservice.pl/en/case-studies/

### Індекс блогу

- https://lasertechservice.pl/en/blog/

### Реалізації

- https://lasertechservice.pl/en/case-studies/beauty-planet-handpiece-cable-replacement-wroclaw/
- https://lasertechservice.pl/en/case-studies/3000-nain-power-supply-repair/
- https://lasertechservice.pl/en/case-studies/alma-accent-cooling-hose-repair-gorlitz/
- https://lasertechservice.pl/en/case-studies/beauty-planet-vacuum-rf-repair-wroclaw/
- https://lasertechservice.pl/en/case-studies/lumenis-lightsheer-desire-cooling-repair-olesnica/
- https://lasertechservice.pl/en/case-studies/multipolar-rf-repair-lublin/
- https://lasertechservice.pl/en/case-studies/nubway-nbw-vsiii-repair-wroclaw/
- https://lasertechservice.pl/en/case-studies/rsl-massage-device-repair-warsaw/
- https://lasertechservice.pl/en/case-studies/urgent-co2-laser-repair-poznan/
- https://lasertechservice.pl/en/case-studies/estelase-power-p808l-maintenance/
- https://lasertechservice.pl/en/case-studies/pharaon-1470-maintenance-wroclaw/
- https://lasertechservice.pl/en/case-studies/hair-removal-laser-maintenance/
- https://lasertechservice.pl/en/case-studies/cavi-shape-advanced-service-wroclaw/
- https://lasertechservice.pl/en/case-studies/diode-laser-handpiece-service-poznan/
- https://lasertechservice.pl/en/case-studies/gme-exsys-308-service-inspection/
- https://lasertechservice.pl/en/case-studies/hifu-kimed-k1-w1601-service-gorlitz/
- https://lasertechservice.pl/en/case-studies/diode-laser-handpiece-replacement-wroclaw/
- https://lasertechservice.pl/en/case-studies/nd-yag-tattoo-removal-laser-filter-service/
- https://lasertechservice.pl/en/case-studies/flood-damaged-diode-module-replacement-poznan/
- https://lasertechservice.pl/en/case-studies/estetech-peltier-module-replacement-poznan/
- https://lasertechservice.pl/en/case-studies/peltier-replacement-nd-yag-laser-repair/
- https://lasertechservice.pl/en/case-studies/laser-cooling-fan-replacement-wroclaw/

### Статті

- https://lasertechservice.pl/en/blog/3000-nain-laser-history-design-service/
- https://lasertechservice.pl/en/blog/five-signs-laser-diode-needs-inspection/
- https://lasertechservice.pl/en/blog/beauty-planet-3d-contour-features-service/
- https://lasertechservice.pl/en/blog/laser-cooling-system-cleaning-overheating/
- https://lasertechservice.pl/en/blog/why-a-small-cable-causes-big-problems/
- https://lasertechservice.pl/en/blog/risks-of-replacing-laser-seals-yourself/
- https://lasertechservice.pl/en/blog/why-laser-diode-modules-fail/
- https://lasertechservice.pl/en/blog/professional-aesthetic-equipment-service/
- https://lasertechservice.pl/en/blog/hifu-technology-applications-service/
- https://lasertechservice.pl/en/blog/how-to-buy-a-used-hair-removal-laser/
- https://lasertechservice.pl/en/blog/co2-laser-not-responding-to-foot-pedal/
- https://lasertechservice.pl/en/blog/laser-tech-service-zlota-firma-2026/
- https://lasertechservice.pl/en/blog/lightsheer-desire-cooling-reliability/
- https://lasertechservice.pl/en/blog/peltier-module-laser-handpiece-cooling/
- https://lasertechservice.pl/en/blog/pharaon-1470-laser-history-technology/
- https://lasertechservice.pl/en/blog/scheduled-diode-laser-maintenance/
- https://lasertechservice.pl/en/blog/handpiece-connections-overheating-nd-yag-calibration/
- https://lasertechservice.pl/en/blog/diode-laser-handpiece-seals-optics/
- https://lasertechservice.pl/en/blog/damaged-handpiece-cable/
- https://lasertechservice.pl/en/blog/used-diode-laser-service-history/
- https://lasertechservice.pl/en/blog/hair-removal-laser-cooling-water-maintenance/

## Файли саме Stage 3C

Порівняно зі знімком робочого дерева перед Stage 3C, а не зі старим HEAD. Перелік містить згенеровані Markdown/AI-ресурси та QA-артефакти.

### Створено (130)

- `docs/multilingual-stage3c-report.md`
- `docs/qa/stage3c/article-form-results.json`
- `docs/qa/stage3c/article-form.png`
- `docs/qa/stage3c/blog-1440.png`
- `docs/qa/stage3c/blog-320.png`
- `docs/qa/stage3c/blog-390.png`
- `docs/qa/stage3c/blog-full.png`
- `docs/qa/stage3c/blog-hifu-technology-applications-service-1440.png`
- `docs/qa/stage3c/blog-hifu-technology-applications-service-320.png`
- `docs/qa/stage3c/blog-hifu-technology-applications-service-390.png`
- `docs/qa/stage3c/blog-hifu-technology-applications-service-full.png`
- `docs/qa/stage3c/blog-lightsheer-desire-cooling-reliability-1440.png`
- `docs/qa/stage3c/blog-lightsheer-desire-cooling-reliability-320.png`
- `docs/qa/stage3c/blog-lightsheer-desire-cooling-reliability-390.png`
- `docs/qa/stage3c/blog-lightsheer-desire-cooling-reliability-full.png`
- `docs/qa/stage3c/blog-why-laser-diode-modules-fail-1440.png`
- `docs/qa/stage3c/blog-why-laser-diode-modules-fail-320.png`
- `docs/qa/stage3c/blog-why-laser-diode-modules-fail-390.png`
- `docs/qa/stage3c/blog-why-laser-diode-modules-fail-full.png`
- `docs/qa/stage3c/case-studies-1440.png`
- `docs/qa/stage3c/case-studies-320.png`
- `docs/qa/stage3c/case-studies-390.png`
- `docs/qa/stage3c/case-studies-estetech-peltier-module-replacement-poznan-1440.png`
- `docs/qa/stage3c/case-studies-estetech-peltier-module-replacement-poznan-320.png`
- `docs/qa/stage3c/case-studies-estetech-peltier-module-replacement-poznan-390.png`
- `docs/qa/stage3c/case-studies-estetech-peltier-module-replacement-poznan-full.png`
- `docs/qa/stage3c/case-studies-full.png`
- `docs/qa/stage3c/case-studies-gme-exsys-308-service-inspection-1440.png`
- `docs/qa/stage3c/case-studies-gme-exsys-308-service-inspection-320.png`
- `docs/qa/stage3c/case-studies-gme-exsys-308-service-inspection-390.png`
- `docs/qa/stage3c/case-studies-gme-exsys-308-service-inspection-full.png`
- `docs/qa/stage3c/case-studies-urgent-co2-laser-repair-poznan-1440.png`
- `docs/qa/stage3c/case-studies-urgent-co2-laser-repair-poznan-320.png`
- `docs/qa/stage3c/case-studies-urgent-co2-laser-repair-poznan-390.png`
- `docs/qa/stage3c/case-studies-urgent-co2-laser-repair-poznan-full.png`
- `docs/qa/stage3c/results.json`
- `docs/qa/stage3c/static-results.json`
- `en/blog/3000-nain-laser-history-design-service/index.html`
- `en/blog/3000-nain-laser-history-design-service/index.md`
- `en/blog/beauty-planet-3d-contour-features-service/index.html`
- `en/blog/beauty-planet-3d-contour-features-service/index.md`
- `en/blog/co2-laser-not-responding-to-foot-pedal/index.html`
- `en/blog/co2-laser-not-responding-to-foot-pedal/index.md`
- `en/blog/damaged-handpiece-cable/index.html`
- `en/blog/damaged-handpiece-cable/index.md`
- `en/blog/diode-laser-handpiece-seals-optics/index.html`
- `en/blog/diode-laser-handpiece-seals-optics/index.md`
- `en/blog/five-signs-laser-diode-needs-inspection/index.html`
- `en/blog/five-signs-laser-diode-needs-inspection/index.md`
- `en/blog/hair-removal-laser-cooling-water-maintenance/index.html`
- `en/blog/hair-removal-laser-cooling-water-maintenance/index.md`
- `en/blog/handpiece-connections-overheating-nd-yag-calibration/index.html`
- `en/blog/handpiece-connections-overheating-nd-yag-calibration/index.md`
- `en/blog/hifu-technology-applications-service/index.html`
- `en/blog/hifu-technology-applications-service/index.md`
- `en/blog/how-to-buy-a-used-hair-removal-laser/index.html`
- `en/blog/how-to-buy-a-used-hair-removal-laser/index.md`
- `en/blog/index.html`
- `en/blog/index.md`
- `en/blog/laser-cooling-system-cleaning-overheating/index.html`
- `en/blog/laser-cooling-system-cleaning-overheating/index.md`
- `en/blog/laser-tech-service-zlota-firma-2026/index.html`
- `en/blog/laser-tech-service-zlota-firma-2026/index.md`
- `en/blog/lightsheer-desire-cooling-reliability/index.html`
- `en/blog/lightsheer-desire-cooling-reliability/index.md`
- `en/blog/peltier-module-laser-handpiece-cooling/index.html`
- `en/blog/peltier-module-laser-handpiece-cooling/index.md`
- `en/blog/pharaon-1470-laser-history-technology/index.html`
- `en/blog/pharaon-1470-laser-history-technology/index.md`
- `en/blog/professional-aesthetic-equipment-service/index.html`
- `en/blog/professional-aesthetic-equipment-service/index.md`
- `en/blog/risks-of-replacing-laser-seals-yourself/index.html`
- `en/blog/risks-of-replacing-laser-seals-yourself/index.md`
- `en/blog/scheduled-diode-laser-maintenance/index.html`
- `en/blog/scheduled-diode-laser-maintenance/index.md`
- `en/blog/used-diode-laser-service-history/index.html`
- `en/blog/used-diode-laser-service-history/index.md`
- `en/blog/why-a-small-cable-causes-big-problems/index.html`
- `en/blog/why-a-small-cable-causes-big-problems/index.md`
- `en/blog/why-laser-diode-modules-fail/index.html`
- `en/blog/why-laser-diode-modules-fail/index.md`
- `en/case-studies/3000-nain-power-supply-repair/index.html`
- `en/case-studies/3000-nain-power-supply-repair/index.md`
- `en/case-studies/alma-accent-cooling-hose-repair-gorlitz/index.html`
- `en/case-studies/alma-accent-cooling-hose-repair-gorlitz/index.md`
- `en/case-studies/beauty-planet-handpiece-cable-replacement-wroclaw/index.html`
- `en/case-studies/beauty-planet-handpiece-cable-replacement-wroclaw/index.md`
- `en/case-studies/beauty-planet-vacuum-rf-repair-wroclaw/index.html`
- `en/case-studies/beauty-planet-vacuum-rf-repair-wroclaw/index.md`
- `en/case-studies/cavi-shape-advanced-service-wroclaw/index.html`
- `en/case-studies/cavi-shape-advanced-service-wroclaw/index.md`
- `en/case-studies/diode-laser-handpiece-replacement-wroclaw/index.html`
- `en/case-studies/diode-laser-handpiece-replacement-wroclaw/index.md`
- `en/case-studies/diode-laser-handpiece-service-poznan/index.html`
- `en/case-studies/diode-laser-handpiece-service-poznan/index.md`
- `en/case-studies/estelase-power-p808l-maintenance/index.html`
- `en/case-studies/estelase-power-p808l-maintenance/index.md`
- `en/case-studies/estetech-peltier-module-replacement-poznan/index.html`
- `en/case-studies/estetech-peltier-module-replacement-poznan/index.md`
- `en/case-studies/flood-damaged-diode-module-replacement-poznan/index.html`
- `en/case-studies/flood-damaged-diode-module-replacement-poznan/index.md`
- `en/case-studies/gme-exsys-308-service-inspection/index.html`
- `en/case-studies/gme-exsys-308-service-inspection/index.md`
- `en/case-studies/hair-removal-laser-maintenance/index.html`
- `en/case-studies/hair-removal-laser-maintenance/index.md`
- `en/case-studies/hifu-kimed-k1-w1601-service-gorlitz/index.html`
- `en/case-studies/hifu-kimed-k1-w1601-service-gorlitz/index.md`
- `en/case-studies/index.html`
- `en/case-studies/index.md`
- `en/case-studies/laser-cooling-fan-replacement-wroclaw/index.html`
- `en/case-studies/laser-cooling-fan-replacement-wroclaw/index.md`
- `en/case-studies/lumenis-lightsheer-desire-cooling-repair-olesnica/index.html`
- `en/case-studies/lumenis-lightsheer-desire-cooling-repair-olesnica/index.md`
- `en/case-studies/multipolar-rf-repair-lublin/index.html`
- `en/case-studies/multipolar-rf-repair-lublin/index.md`
- `en/case-studies/nd-yag-tattoo-removal-laser-filter-service/index.html`
- `en/case-studies/nd-yag-tattoo-removal-laser-filter-service/index.md`
- `en/case-studies/nubway-nbw-vsiii-repair-wroclaw/index.html`
- `en/case-studies/nubway-nbw-vsiii-repair-wroclaw/index.md`
- `en/case-studies/peltier-replacement-nd-yag-laser-repair/index.html`
- `en/case-studies/peltier-replacement-nd-yag-laser-repair/index.md`
- `en/case-studies/pharaon-1470-maintenance-wroclaw/index.html`
- `en/case-studies/pharaon-1470-maintenance-wroclaw/index.md`
- `en/case-studies/rsl-massage-device-repair-warsaw/index.html`
- `en/case-studies/rsl-massage-device-repair-warsaw/index.md`
- `en/case-studies/urgent-co2-laser-repair-poznan/index.html`
- `en/case-studies/urgent-co2-laser-repair-poznan/index.md`
- `scripts/check-english-content-form.cjs`
- `scripts/check-english-content.cjs`
- `scripts/check-english-content.py`

### Змінено (219)

- `_headers`
- `ai-catalog.json`
- `blog/3000-nain-laser-historia-konstrukcja-serwis/index.html`
- `blog/3000-nain-laser-historia-konstrukcja-serwis/index.md`
- `blog/5-oznak-wymiany-diody-w-laserze/index.html`
- `blog/5-oznak-wymiany-diody-w-laserze/index.md`
- `blog/beauty-planet-3d-contour-mozliwosci-serwis/index.html`
- `blog/beauty-planet-3d-contour-mozliwosci-serwis/index.md`
- `blog/czyszczenie-ukladu-chlodzenia-lasera-wentylatory-przegrzanie/index.html`
- `blog/czyszczenie-ukladu-chlodzenia-lasera-wentylatory-przegrzanie/index.md`
- `blog/dlaczego-maly-przewod-powoduje-duze-problemy/index.html`
- `blog/dlaczego-maly-przewod-powoduje-duze-problemy/index.md`
- `blog/dlaczego-nie-warto-samodzielnie-wymieniac-uszczelek-w-laserze/index.html`
- `blog/dlaczego-nie-warto-samodzielnie-wymieniac-uszczelek-w-laserze/index.md`
- `blog/dlaczego-pala-sie-moduly-diodowe-w-laserach/index.html`
- `blog/dlaczego-pala-sie-moduly-diodowe-w-laserach/index.md`
- `blog/dlaczego-warto-korzystac-z-profesjonalnego-serwisu/index.html`
- `blog/dlaczego-warto-korzystac-z-profesjonalnego-serwisu/index.md`
- `blog/hifu-co-to-jest-jak-dziala-zastosowanie-serwis/index.html`
- `blog/hifu-co-to-jest-jak-dziala-zastosowanie-serwis/index.md`
- `blog/index.html`
- `blog/index.md`
- `blog/jak-kupic-uzywany-laser-do-depilacji/index.html`
- `blog/jak-kupic-uzywany-laser-do-depilacji/index.md`
- `blog/laser-co2-nie-reaguje-na-pedal-diagnostyka/index.html`
- `blog/laser-co2-nie-reaguje-na-pedal-diagnostyka/index.md`
- `blog/laser-tech-service-zlota-firma-2026/index.html`
- `blog/laser-tech-service-zlota-firma-2026/index.md`
- `blog/lightsheer-desire-chlodzenie-niezawodnosc/index.html`
- `blog/lightsheer-desire-chlodzenie-niezawodnosc/index.md`
- `blog/modul-peltiera-chlodzenie-glowicy-lasera/index.html`
- `blog/modul-peltiera-chlodzenie-glowicy-lasera/index.md`
- `blog/pharaon-1470-historia-technologia-lasera/index.html`
- `blog/pharaon-1470-historia-technologia-lasera/index.md`
- `blog/planowy-przeglad-lasera-diodowego-dlaczego-to-wazne/index.html`
- `blog/planowy-przeglad-lasera-diodowego-dlaczego-to-wazne/index.md`
- `blog/podlaczenie-glowic-przegrzewanie-kalibracja-nd-yag/index.html`
- `blog/podlaczenie-glowic-przegrzewanie-kalibracja-nd-yag/index.md`
- `blog/serwis-glowicy-lasera-diodowego-szczelnosc-optyka/index.html`
- `blog/serwis-glowicy-lasera-diodowego-szczelnosc-optyka/index.md`
- `blog/uszkodzony-przewod-manipulatora/index.html`
- `blog/uszkodzony-przewod-manipulatora/index.md`
- `blog/uzywany-laser-diodowy-z-historia-serwisowa/index.html`
- `blog/uzywany-laser-diodowy-z-historia-serwisowa/index.md`
- `blog/wymiana-wody-w-laserze-do-depilacji/index.html`
- `blog/wymiana-wody-w-laserze-do-depilacji/index.md`
- `en/contact/index.html`
- `en/index.html`
- `en/services/aesthetic-equipment-maintenance/index.html`
- `en/services/aesthetic-equipment-maintenance/index.md`
- `en/services/co2-laser-service/index.html`
- `en/services/co2-laser-service/index.md`
- `en/services/cryotherapy-cryolipolysis-equipment-service/index.html`
- `en/services/cryotherapy-cryolipolysis-equipment-service/index.md`
- `en/services/diode-laser-diagnostics/index.html`
- `en/services/diode-laser-diagnostics/index.md`
- `en/services/index.html`
- `en/services/ipl-equipment-service/index.html`
- `en/services/ipl-equipment-service/index.md`
- `en/services/laser-cooling-system-repair/index.html`
- `en/services/laser-cooling-system-repair/index.md`
- `en/services/laser-diode-replacement-calibration/index.html`
- `en/services/laser-diode-replacement-calibration/index.md`
- `en/services/laser-handpiece-repair/index.html`
- `en/services/laser-handpiece-repair/index.md`
- `en/services/lpg-endermology-equipment-repair/index.html`
- `en/services/nd-yag-laser-service/index.html`
- `en/services/nd-yag-laser-service/index.md`
- `en/services/picosecond-laser-service/index.html`
- `en/services/post-warranty-equipment-service/index.html`
- `en/services/post-warranty-equipment-service/index.md`
- `en/services/power-supply-electronics-repair/index.html`
- `en/services/power-supply-electronics-repair/index.md`
- `en/services/rf-equipment-repair/index.html`
- `en/services/rf-equipment-repair/index.md`
- `en/services/touchscreen-control-panel-repair/index.html`
- `llms-full.txt`
- `llms.txt`
- `realizacje/beauty-planet-3d-contour-naprawa-przewodu-wroclaw/index.html`
- `realizacje/beauty-planet-3d-contour-naprawa-przewodu-wroclaw/index.md`
- `realizacje/index.html`
- `realizacje/index.md`
- `realizacje/naprawa-3000-nain-bloku-zasilania/index.html`
- `realizacje/naprawa-3000-nain-bloku-zasilania/index.md`
- `realizacje/naprawa-alma-accent-gorlitz/index.html`
- `realizacje/naprawa-alma-accent-gorlitz/index.md`
- `realizacje/naprawa-beauty-planet-3d-contour-wroclaw/index.html`
- `realizacje/naprawa-beauty-planet-3d-contour-wroclaw/index.md`
- `realizacje/naprawa-lumenis-lightsheer-desire-olesnica/index.html`
- `realizacje/naprawa-lumenis-lightsheer-desire-olesnica/index.md`
- `realizacje/naprawa-multipolar-rf-lublin/index.html`
- `realizacje/naprawa-multipolar-rf-lublin/index.md`
- `realizacje/naprawa-nubway-nbw-vsiii-wroclaw/index.html`
- `realizacje/naprawa-nubway-nbw-vsiii-wroclaw/index.md`
- `realizacje/naprawa-rsl-masaz-warszawa/index.html`
- `realizacje/naprawa-rsl-masaz-warszawa/index.md`
- `realizacje/pilna-naprawa-lasera-co2-poznan/index.html`
- `realizacje/pilna-naprawa-lasera-co2-poznan/index.md`
- `realizacje/przeglad-estelase-power-p808l/index.html`
- `realizacje/przeglad-estelase-power-p808l/index.md`
- `realizacje/przeglad-serwis-pharaon-1470-wroclaw/index.html`
- `realizacje/przeglad-serwis-pharaon-1470-wroclaw/index.md`
- `realizacje/przeglad-techniczny-lasera-do-depilacji/index.html`
- `realizacje/przeglad-techniczny-lasera-do-depilacji/index.md`
- `realizacje/serwis-cavi-shape-advanced-wroclaw/index.html`
- `realizacje/serwis-cavi-shape-advanced-wroclaw/index.md`
- `realizacje/serwis-glowicy-lasera-diodowego-poznan/index.html`
- `realizacje/serwis-glowicy-lasera-diodowego-poznan/index.md`
- `realizacje/serwis-gme-exsys-308/index.html`
- `realizacje/serwis-gme-exsys-308/index.md`
- `realizacje/serwis-hifu-kimed-k1-w1601-gorlitz/index.html`
- `realizacje/serwis-hifu-kimed-k1-w1601-gorlitz/index.md`
- `realizacje/serwis-lasera-diodowego-wymiana-glowicy-wroclaw/index.html`
- `realizacje/serwis-lasera-diodowego-wymiana-glowicy-wroclaw/index.md`
- `realizacje/serwis-lasera-do-usuwania-tatuazu-wymiana-filtra/index.html`
- `realizacje/serwis-lasera-do-usuwania-tatuazu-wymiana-filtra/index.md`
- `realizacje/wymiana-modulu-diodowego-lasera-po-zalaniu-poznan/index.html`
- `realizacje/wymiana-modulu-diodowego-lasera-po-zalaniu-poznan/index.md`
- `realizacje/wymiana-modulu-peltiera-estetech-poznan/index.html`
- `realizacje/wymiana-modulu-peltiera-estetech-poznan/index.md`
- `realizacje/wymiana-peltiera-naprawa-lasera-nd-yag/index.html`
- `realizacje/wymiana-peltiera-naprawa-lasera-nd-yag/index.md`
- `realizacje/wymiana-wentylatorow-chlodzenia-lasera-wroclaw/index.html`
- `realizacje/wymiana-wentylatorow-chlodzenia-lasera-wroclaw/index.md`
- `ru/blog/3000-nain-lazer-istoriya-konstrukciya-servis/index.html`
- `ru/blog/3000-nain-lazer-istoriya-konstrukciya-servis/index.md`
- `ru/blog/5-priznakov-zameny-dioda-v-lazere/index.html`
- `ru/blog/5-priznakov-zameny-dioda-v-lazere/index.md`
- `ru/blog/beauty-planet-3d-contour-vozmozhnosti-servis/index.html`
- `ru/blog/beauty-planet-3d-contour-vozmozhnosti-servis/index.md`
- `ru/blog/co2-lazer-ne-reagiruet-na-pedal-diagnostika/index.html`
- `ru/blog/co2-lazer-ne-reagiruet-na-pedal-diagnostika/index.md`
- `ru/blog/hifu-chto-eto-kak-rabotaet-primenenie-servis/index.html`
- `ru/blog/hifu-chto-eto-kak-rabotaet-primenenie-servis/index.md`
- `ru/blog/index.html`
- `ru/blog/index.md`
- `ru/blog/kak-kupit-bu-lazer-dlya-epilyacii/index.html`
- `ru/blog/kak-kupit-bu-lazer-dlya-epilyacii/index.md`
- `ru/blog/laser-tech-service-zlota-firma-2026/index.html`
- `ru/blog/laser-tech-service-zlota-firma-2026/index.md`
- `ru/blog/lightsheer-desire-ohlazhdenie-nadezhnost/index.html`
- `ru/blog/lightsheer-desire-ohlazhdenie-nadezhnost/index.md`
- `ru/blog/modul-pelte-ohlazhdenie-manipuly-lazera/index.html`
- `ru/blog/modul-pelte-ohlazhdenie-manipuly-lazera/index.md`
- `ru/blog/obsluzhivanie-manipuly-lazera-germetichnost-optika/index.html`
- `ru/blog/obsluzhivanie-manipuly-lazera-germetichnost-optika/index.md`
- `ru/blog/ochistka-sistemy-ohlazhdeniya-lazera-ventilyatory-peregrev/index.html`
- `ru/blog/ochistka-sistemy-ohlazhdeniya-lazera-ventilyatory-peregrev/index.md`
- `ru/blog/pharaon-1470-istoriya-lazernoy-tehnologii/index.html`
- `ru/blog/pharaon-1470-istoriya-lazernoy-tehnologii/index.md`
- `ru/blog/planovoe-obsluzhivanie-diodnogo-lazera-pochemu-eto-vazhno/index.html`
- `ru/blog/planovoe-obsluzhivanie-diodnogo-lazera-pochemu-eto-vazhno/index.md`
- `ru/blog/pochemu-malenkiy-kabel-sozdayot-bolshie-problemy/index.html`
- `ru/blog/pochemu-malenkiy-kabel-sozdayot-bolshie-problemy/index.md`
- `ru/blog/pochemu-ne-stoit-samostoyatelno-menyat-uplotneniya-v-lazere/index.html`
- `ru/blog/pochemu-ne-stoit-samostoyatelno-menyat-uplotneniya-v-lazere/index.md`
- `ru/blog/pochemu-sgorayut-diodnye-moduli-v-lazerah/index.html`
- `ru/blog/pochemu-sgorayut-diodnye-moduli-v-lazerah/index.md`
- `ru/blog/pochemu-stoit-polzovatsya-professionalnym-servisom/index.html`
- `ru/blog/pochemu-stoit-polzovatsya-professionalnym-servisom/index.md`
- `ru/blog/pochemu-vazhno-pokupat-lazer-s-istoriey-servisa/index.html`
- `ru/blog/pochemu-vazhno-pokupat-lazer-s-istoriey-servisa/index.md`
- `ru/blog/podklyuchenie-manipul-peregrev-kalibrovka-nd-yag/index.html`
- `ru/blog/podklyuchenie-manipul-peregrev-kalibrovka-nd-yag/index.md`
- `ru/blog/povrezhdennyj-kabel-manipuly/index.html`
- `ru/blog/povrezhdennyj-kabel-manipuly/index.md`
- `ru/blog/zamena-vody-v-lazere-dlya-epilyacii/index.html`
- `ru/blog/zamena-vody-v-lazere-dlya-epilyacii/index.md`
- `ru/realizacje/beauty-planet-3d-contour-naprawa-przewodu-wroclaw/index.html`
- `ru/realizacje/beauty-planet-3d-contour-naprawa-przewodu-wroclaw/index.md`
- `ru/realizacje/index.html`
- `ru/realizacje/index.md`
- `ru/realizacje/naprawa-3000-nain-bloku-zasilania/index.html`
- `ru/realizacje/naprawa-3000-nain-bloku-zasilania/index.md`
- `ru/realizacje/naprawa-alma-accent-gorlitz/index.html`
- `ru/realizacje/naprawa-alma-accent-gorlitz/index.md`
- `ru/realizacje/naprawa-beauty-planet-3d-contour-wroclaw/index.html`
- `ru/realizacje/naprawa-beauty-planet-3d-contour-wroclaw/index.md`
- `ru/realizacje/naprawa-multipolar-rf-lublin/index.html`
- `ru/realizacje/naprawa-multipolar-rf-lublin/index.md`
- `ru/realizacje/naprawa-nubway-nbw-vsiii-wroclaw/index.html`
- `ru/realizacje/naprawa-nubway-nbw-vsiii-wroclaw/index.md`
- `ru/realizacje/naprawa-rsl-masaz-warszawa/index.html`
- `ru/realizacje/naprawa-rsl-masaz-warszawa/index.md`
- `ru/realizacje/pilna-naprawa-lasera-co2-poznan/index.html`
- `ru/realizacje/pilna-naprawa-lasera-co2-poznan/index.md`
- `ru/realizacje/przeglad-estelase-power-p808l/index.html`
- `ru/realizacje/przeglad-estelase-power-p808l/index.md`
- `ru/realizacje/przeglad-serwis-pharaon-1470-wroclaw/index.html`
- `ru/realizacje/przeglad-serwis-pharaon-1470-wroclaw/index.md`
- `ru/realizacje/przeglad-techniczny-lasera-do-depilacji/index.html`
- `ru/realizacje/przeglad-techniczny-lasera-do-depilacji/index.md`
- `ru/realizacje/remont-lumenis-lightsheer-desire-olesnica/index.html`
- `ru/realizacje/remont-lumenis-lightsheer-desire-olesnica/index.md`
- `ru/realizacje/serwis-cavi-shape-advanced-wroclaw/index.html`
- `ru/realizacje/serwis-cavi-shape-advanced-wroclaw/index.md`
- `ru/realizacje/serwis-glowicy-lasera-diodowego-poznan/index.html`
- `ru/realizacje/serwis-glowicy-lasera-diodowego-poznan/index.md`
- `ru/realizacje/serwis-gme-exsys-308/index.html`
- `ru/realizacje/serwis-gme-exsys-308/index.md`
- `ru/realizacje/serwis-hifu-kimed-k1-w1601-gorlitz/index.html`
- `ru/realizacje/serwis-hifu-kimed-k1-w1601-gorlitz/index.md`
- `ru/realizacje/serwis-lasera-diodowego-wymiana-glowicy-wroclaw/index.html`
- `ru/realizacje/serwis-lasera-diodowego-wymiana-glowicy-wroclaw/index.md`
- `ru/realizacje/serwis-lasera-do-usuwania-tatuazu-wymiana-filtra/index.html`
- `ru/realizacje/serwis-lasera-do-usuwania-tatuazu-wymiana-filtra/index.md`
- `ru/realizacje/wymiana-modulu-diodowego-lasera-po-zalaniu-poznan/index.html`
- `ru/realizacje/wymiana-modulu-diodowego-lasera-po-zalaniu-poznan/index.md`
- `ru/realizacje/zamena-modulya-pelte-estetech-poznan/index.html`
- `ru/realizacje/zamena-modulya-pelte-estetech-poznan/index.md`
- `ru/realizacje/zamena-pelte-remont-lazera-nd-yag/index.html`
- `ru/realizacje/zamena-pelte-remont-lazera-nd-yag/index.md`
- `ru/realizacje/zamena-ventilyatorov-ohlazhdeniya-lazera-vrotslav/index.html`
- `ru/realizacje/zamena-ventilyatorov-ohlazhdeniya-lazera-vrotslav/index.md`
- `scripts/check-english-pages.cjs`
- `scripts/check-english-pages.py`
- `scripts/check-english-services.cjs`
- `scripts/site-locales.json`
- `sitemap.xml`

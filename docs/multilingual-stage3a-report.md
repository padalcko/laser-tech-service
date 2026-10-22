# Stage 3A — 15 English Service Landing Pages

Дата: 2026-10-22. Робота виконана локально поверх незакомічених Stage 1, 2A і 2B. Відновлення до HEAD, commit, push і deploy не виконувалися.

## Результат і маршрути

Створено рівно 15 EN посадкових та 15 Markdown-відповідників. Усі URL збігаються з попередніми planned-маршрутами; slug, стабільні ID та x-default не змінені. Джерела — відповідні PL/RU посадкові. Перекладено заголовки, технічний зміст, симптоми, процедури, обмеження, FAQ, форми, alt/aria та metadata професійною British English.

| EN URL | Початкова ціна |
|---|---|
| `/en/services/diode-laser-diagnostics/` | PLN 600 |
| `/en/services/aesthetic-equipment-maintenance/` | PLN 1,200 |
| `/en/services/touchscreen-control-panel-repair/` | PLN 600 |
| `/en/services/laser-cooling-system-repair/` | PLN 1,000 |
| `/en/services/lpg-endermology-equipment-repair/` | PLN 800 |
| `/en/services/rf-equipment-repair/` | PLN 600 |
| `/en/services/power-supply-electronics-repair/` | PLN 600 |
| `/en/services/laser-handpiece-repair/` | PLN 800 |
| `/en/services/ipl-equipment-service/` | PLN 800 |
| `/en/services/co2-laser-service/` | PLN 1,200 |
| `/en/services/nd-yag-laser-service/` | PLN 800 |
| `/en/services/picosecond-laser-service/` | PLN 1,200 |
| `/en/services/post-warranty-equipment-service/` | Індивідуально після діагностики |
| `/en/services/cryotherapy-cryolipolysis-equipment-service/` | PLN 1,200 |
| `/en/services/laser-diode-replacement-calibration/` | PLN 800 |

Ціни взято з PL-джерел без конвертації в EUR і без націнки 20%. Вартість частин і додаткових робіт не підмінено початковою сумою. Збережено окрему калібровку CO₂ за PLN 1,600 та зазначену у джерелі працю із заміни діоди за PLN 1,200; це не нові ціни. Умови безкоштовної діагностики при ремонті/обслуговуванні й окремої оплати виїзду та транспорту збережені відповідно до кожної сторінки.

## Дизайн і зміст

Використано HTML-композицію відповідного PL-еталона, чинні `css/service-landing.css`, hero, картки, технічні секції, FAQ, CTA, форми, footer і зображення. Нових дизайнерських секцій немає. Видалено лише порожні `<p>` у скопійованих EN картках симптомів; картки з заголовками збережено. Глобальні CSS, JavaScript, зображення та головні сторінки не змінювалися.

Збережено обмеження ремонту герметичних джерел, залежність калібрування від документації та оснащення, відмінність вимірювання енергії від тривалості імпульсу, відсутність заяви про авторизацію LPG Systems, модельну сумісність запчастин та вимоги до охолоджувальної рідини. Не додано представництв, гарантій, строків, географії чи нових послуг.

В EN-каталозі всі 15 посилань ведуть на готові EN посадкові. Релевантні посилання між послугами також переведено на опубліковані EN URL. Нові головні меню мають англійські назви без `(Polish)`; неперекладені блог, кейси, партнери та прайс залишаються доступними за існуючими PL URL. Головні сторінки й попередні меню поза новими посадковими не переписувалися.

Приклади ремонту мають перекладені підписи, а переходи на наявні PL-кейси явно позначені `in Polish`. Для згенерованих карток додано явний `case_language_fallbacks.en=pl` у `service-cases.json`; URL бере реєстр, а не вигаданий EN-маршрут. Якщо згодом EN-кейс опубліковано, генератор автоматично обере його замість fallback. PL/RU картки не змінені. Порожніх контейнерів кейсів немає, EN-блогів/кейсів/міжнародних сторінок не створено.

## SEO, реєстр і AI

На всіх 15 EN сторінках: `lang=en`, self-canonical, унікальні title/description, OG/Twitter, `og:locale=en_GB`, Service із незмінним provider `https://lasertechservice.pl/#organization`, BreadcrumbList і FAQPage за фактичними видимими питаннями та відповідями. Додано 104 EN FAQ schema questions.

Для 30 відповідних PL/RU HTML синхронізовано hreflang, OG alternate і мовний компонент через чинний `build-language-switcher.py`. Їхні main/footer побайтово збігаються з джерельними main/footer у HEAD; додатково SHA256-порівняння зі станом на початку Stage 3A підтвердило незмінність решти HTML, CSS, JS і зображень поза погодженим переліком. Sitemap зберігає попередні URL та структуру; додає рівно 15 EN URL і взаємні мовні зв’язки відповідних груп. Planned-маршрути не публікуються.

Оновлено llms, Markdown, `_headers` та AI Catalog штатною збіркою. У каталозі залишаються 15 бізнес-послуг зі стабільними PL-primary ID, тепер кожна має PL/RU/EN локалізації. Початкові суми та кількість пунктів складу робіт EN перевірено проти PL; післягарантійний сервіс має null, без вигаданої мінімальної суми.

Генератор AI Catalog доповнено розпізнаванням британського формату `from PLN 1,200` зі збереженням старих PL/RU і `from 800 PLN`. Додано перевірки тисяч, дробових сум і відхилення некоректного `from PLN 1,20`. Розпізнавання заголовків складу робіт підтримує фактичні EN заголовки нових сторінок.

| Показник | До Stage 3A | Після |
|---|---:|---:|
| Канонічні HTML / sitemap URL | 133 | 148 |
| PL / RU / EN | 65 / 65 / 3 | 65 / 65 / 18 |
| HTML з урахуванням 404 | 134 | 149 |
| Markdown | 133 | 148 |
| EN детальні послуги | 0 | 15 |
| Тримовні групи | 3 | 18 |
| Planned EN маршрути | 65 | 50 |
| AI Catalog: послуги / статті / кейси | 15 / 42 / 44 | 15 / 42 / 44 |

Published означає стан локального реєстру та збірки, а не виконаний deploy.

## Форми, Лазар і backend

Нові форми мають `language=en`, локалізований `source=en-…`, незмінні `serviceType` та набір полів відповідного PL-еталона. Webhook, payload, session ID та аналітичні механізми не змінювалися. Кожна з 15 форм перевірена через mock: required/consent, loading, HTTP 500, успіх, точний набір payload-полів, language/source/serviceType/pageUrl і одна success-подія `service_lead_submit`.

Усі 18 EN HTML зберігають `data-lazar-enabled=false`. Нові сторінки не показують чат і не надсилають до нього запити. Англійський інтерфейс Лазаря перевірявся лише з test override і mock backend.

**Реальний n8n не перевірено.** Жодних реальних заявок/чат-запитів не відправляли. Підтримка нових en-source, приймання EN-заявок і англійські відповіді Лазаря потребують окремої серверної перевірки. До підтвердження backend EN-чат має залишатися прихованим.

## Перевірки

PASS:

- `build-site.py`: реєстр, мовний компонент, картки кейсів, Markdown/llms, AI Catalog, AI Search і GEO/SEO.
- Повторний `build-site.py`: SHA256 усіх файлів до/після однакові; жодних побайтових змін.
- `check-site-locales.py`, `check-language-switcher.py`, `check-ai-search.py`, `check-geo-seo.py`, `check-ai-catalog.py`.
- `build-ai-search.py --check`, `build-ai-catalog.py --check`, `build-service-cases.py --check`, `build-language-switcher.py --check`: stale відсутні.
- `check-english-pages.py`: 148 сторінок, 18 EN, 15 послуг, reciprocal SEO, provider, FAQ, ціни та склад робіт, незмінний контракт форм, відсутність planned-посилань і chat gate.
- Статичний аудит: 149 HTML, 148 Markdown, 18 700 локальних посилань/ресурсів, 228 FAQ schema questions; issues порожні.
- `check-english-services.cjs`: HTTP 200 для всіх 148 канонічних URL; 45 layout-сценаріїв (15 × 320/390/1440 px), без overflow, незавантажених видимих зображень і JS pageerror. PL/RU/EN переходи в обидва боки, dropdown 44 px, клавіатура, Escape, клік поза меню, burger, FAQ; 15 mock-форм; прихований чат.
- `check-english-pages.cjs`: регресія перших трьох EN сторінок — 9 layout-сценаріїв, дві mock-форми та gated mock-чат. Loading-тест тепер тримає mock-відповідь до перевірки кнопки, усуваючи залежність від швидкості Chrome.
- `check-lazar-ai.cjs`: 27 layout/scenario груп PL/RU/EN і storage denial; лише mock backend.
- `check-language-runtime.cjs`: 47 груп і перемикання без JavaScript.
- `check-lightsheer-desire.py`, `check-cooling-maintenance.py`, `check-used-laser-buying.py`.
- Структурне зіставлення всіх 15 PL/RU/EN: однакові кількості FAQ, процедурних списків і форм, незмінний serviceType.
- `git diff --check`; Python cache відсутній.

Історичні разові аудити з очікуваннями старого HEAD/порядку кейсів, описані у Stage 2B, на цьому етапі не змінювалися й повторно не запускалися. Вони не є частиною production build.

## Скриншоти

| Тип сторінки | Desktop 1440 | Mobile 390 | Mobile 320 | Повна сторінка |
|---|---|---|---|---|
| Діагностика | [1440](qa/stage3a/diode-laser-diagnostics-1440.png) | [390](qa/stage3a/diode-laser-diagnostics-390.png) | [320](qa/stage3a/diode-laser-diagnostics-320.png) | [Full](qa/stage3a/diode-laser-diagnostics-full.png) |
| Екрани | [1440](qa/stage3a/touchscreen-control-panel-repair-1440.png) | [390](qa/stage3a/touchscreen-control-panel-repair-390.png) | [320](qa/stage3a/touchscreen-control-panel-repair-320.png) | [Full](qa/stage3a/touchscreen-control-panel-repair-full.png) |
| CO₂ | [1440](qa/stage3a/co2-laser-service-1440.png) | [390](qa/stage3a/co2-laser-service-390.png) | [320](qa/stage3a/co2-laser-service-320.png) | [Full](qa/stage3a/co2-laser-service-full.png) |

[Результати браузерної перевірки](qa/stage3a/results.json). Візуально переглянуто desktop діагностики та mobile екранів і CO₂.

## Ризики та межі перевірки

- Реальні n8n, доставка заявок і backend EN не підтверджені; чат закритий.
- SEO та HTTP перевірено локально. Live URL, індексація, production Lighthouse/CWV і отримання подій у GA4/GTM не перевірялися. Зовнішні мережеві запити у браузерних тестах блокувалися.
- Блог, кейси, прайс та партнери ще не мають EN сторінок; відповідні переходи ведуть на існуючі PL матеріали. На нових посадкових головне меню не містить `(Polish)` відповідно до завдання, а посилання в змістових секціях позначені `in Polish`.
- Зображення залишені оригінальними; вбудовані в растри написи не перекладалися. HTML-тексти й alt перекладені.
- Умови, строки й технічні твердження взято з джерел; нової міжнародної географії або обіцянок не додано.

## Файли Stage 3A

Перелік нижче — відносно SHA256-знімка на початку Stage 3A, не весь накопичений diff попередніх етапів.

### Створено

- `docs/multilingual-stage3a-report.md`
- `docs/qa/stage3a/co2-laser-service-1440.png`
- `docs/qa/stage3a/co2-laser-service-320.png`
- `docs/qa/stage3a/co2-laser-service-390.png`
- `docs/qa/stage3a/co2-laser-service-full.png`
- `docs/qa/stage3a/diode-laser-diagnostics-1440.png`
- `docs/qa/stage3a/diode-laser-diagnostics-320.png`
- `docs/qa/stage3a/diode-laser-diagnostics-390.png`
- `docs/qa/stage3a/diode-laser-diagnostics-full.png`
- `docs/qa/stage3a/results.json`
- `docs/qa/stage3a/touchscreen-control-panel-repair-1440.png`
- `docs/qa/stage3a/touchscreen-control-panel-repair-320.png`
- `docs/qa/stage3a/touchscreen-control-panel-repair-390.png`
- `docs/qa/stage3a/touchscreen-control-panel-repair-full.png`
- `en/services/aesthetic-equipment-maintenance/index.html`
- `en/services/aesthetic-equipment-maintenance/index.md`
- `en/services/co2-laser-service/index.html`
- `en/services/co2-laser-service/index.md`
- `en/services/cryotherapy-cryolipolysis-equipment-service/index.html`
- `en/services/cryotherapy-cryolipolysis-equipment-service/index.md`
- `en/services/diode-laser-diagnostics/index.html`
- `en/services/diode-laser-diagnostics/index.md`
- `en/services/ipl-equipment-service/index.html`
- `en/services/ipl-equipment-service/index.md`
- `en/services/laser-cooling-system-repair/index.html`
- `en/services/laser-cooling-system-repair/index.md`
- `en/services/laser-diode-replacement-calibration/index.html`
- `en/services/laser-diode-replacement-calibration/index.md`
- `en/services/laser-handpiece-repair/index.html`
- `en/services/laser-handpiece-repair/index.md`
- `en/services/lpg-endermology-equipment-repair/index.html`
- `en/services/lpg-endermology-equipment-repair/index.md`
- `en/services/nd-yag-laser-service/index.html`
- `en/services/nd-yag-laser-service/index.md`
- `en/services/picosecond-laser-service/index.html`
- `en/services/picosecond-laser-service/index.md`
- `en/services/post-warranty-equipment-service/index.html`
- `en/services/post-warranty-equipment-service/index.md`
- `en/services/power-supply-electronics-repair/index.html`
- `en/services/power-supply-electronics-repair/index.md`
- `en/services/rf-equipment-repair/index.html`
- `en/services/rf-equipment-repair/index.md`
- `en/services/touchscreen-control-panel-repair/index.html`
- `en/services/touchscreen-control-panel-repair/index.md`
- `scripts/check-english-services.cjs`

### Змінено

- `_headers`
- `ai-catalog.json`
- `en/services/index.html`
- `en/services/index.md`
- `llms-full.txt`
- `llms.txt`
- `ru/uslugi/diagnostika-diodnyh-lazerov/index.html`
- `ru/uslugi/diagnostika-diodnyh-lazerov/index.md`
- `ru/uslugi/poslegarantiynoe-obsluzhivanie/index.html`
- `ru/uslugi/poslegarantiynoe-obsluzhivanie/index.md`
- `ru/uslugi/remont-blokov-pitaniya-i-elektroniki/index.html`
- `ru/uslugi/remont-blokov-pitaniya-i-elektroniki/index.md`
- `ru/uslugi/remont-oborudovaniya-lpg/index.html`
- `ru/uslugi/remont-oborudovaniya-lpg/index.md`
- `ru/uslugi/remont-oborudovaniya-rf/index.html`
- `ru/uslugi/remont-oborudovaniya-rf/index.md`
- `ru/uslugi/remont-sensornyh-ekranov/index.html`
- `ru/uslugi/remont-sensornyh-ekranov/index.md`
- `ru/uslugi/remont-sistem-ohlazhdeniya/index.html`
- `ru/uslugi/remont-sistem-ohlazhdeniya/index.md`
- `ru/uslugi/servis-ipl/index.html`
- `ru/uslugi/servis-ipl/index.md`
- `ru/uslugi/servis-lazerov-co2/index.html`
- `ru/uslugi/servis-lazerov-co2/index.md`
- `ru/uslugi/servis-lazerov-nd-yag/index.html`
- `ru/uslugi/servis-lazerov-nd-yag/index.md`
- `ru/uslugi/servis-oborudovaniya-dlya-krioterapii/index.html`
- `ru/uslugi/servis-oborudovaniya-dlya-krioterapii/index.md`
- `ru/uslugi/servis-pikosekundnyh-lazerov/index.html`
- `ru/uslugi/servis-pikosekundnyh-lazerov/index.md`
- `ru/uslugi/tehnicheskoe-obsluzhivanie-oborudovaniya/index.html`
- `ru/uslugi/tehnicheskoe-obsluzhivanie-oborudovaniya/index.md`
- `ru/uslugi/vosstanovlenie-golovok-i-manipul/index.html`
- `ru/uslugi/vosstanovlenie-golovok-i-manipul/index.md`
- `ru/uslugi/zamena-i-kalibrovka-lazernyh-diodov/index.html`
- `ru/uslugi/zamena-i-kalibrovka-lazernyh-diodov/index.md`
- `scripts/build-ai-catalog.py`
- `scripts/build-service-cases.py`
- `scripts/check-ai-catalog.py`
- `scripts/check-english-pages.cjs`
- `scripts/check-english-pages.py`
- `scripts/service-cases.json`
- `scripts/site-locales.json`
- `sitemap.xml`
- `uslugi/diagnostyka-laserow-diodowych/index.html`
- `uslugi/diagnostyka-laserow-diodowych/index.md`
- `uslugi/konserwacja-urzadzen-kosmetologicznych/index.html`
- `uslugi/konserwacja-urzadzen-kosmetologicznych/index.md`
- `uslugi/naprawa-ekranow-dotykowych/index.html`
- `uslugi/naprawa-ekranow-dotykowych/index.md`
- `uslugi/naprawa-ukladow-chlodzenia/index.html`
- `uslugi/naprawa-ukladow-chlodzenia/index.md`
- `uslugi/naprawa-urzadzen-lpg/index.html`
- `uslugi/naprawa-urzadzen-lpg/index.md`
- `uslugi/naprawa-urzadzen-rf/index.html`
- `uslugi/naprawa-urzadzen-rf/index.md`
- `uslugi/naprawa-zasilaczy-i-elektroniki/index.html`
- `uslugi/naprawa-zasilaczy-i-elektroniki/index.md`
- `uslugi/regeneracja-glowic-i-manipulatorow/index.html`
- `uslugi/regeneracja-glowic-i-manipulatorow/index.md`
- `uslugi/serwis-ipl/index.html`
- `uslugi/serwis-ipl/index.md`
- `uslugi/serwis-laserow-co2/index.html`
- `uslugi/serwis-laserow-co2/index.md`
- `uslugi/serwis-laserow-nd-yag/index.html`
- `uslugi/serwis-laserow-nd-yag/index.md`
- `uslugi/serwis-laserow-pikosekundowych/index.html`
- `uslugi/serwis-laserow-pikosekundowych/index.md`
- `uslugi/serwis-pogwarancyjny/index.html`
- `uslugi/serwis-pogwarancyjny/index.md`
- `uslugi/serwis-urzadzen-do-krioterapii/index.html`
- `uslugi/serwis-urzadzen-do-krioterapii/index.md`
- `uslugi/wymiana-i-kalibracja-diod-laserowych/index.html`
- `uslugi/wymiana-i-kalibracja-diod-laserowych/index.md`

Усі зміни залишені локально для перевірки. Stage 3A виконано; серверна перевірка n8n та публікація залишаються окремими діями.

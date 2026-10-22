# Stage 2B — First English Pages

Дата: 2026-10-22. Зміни залишені локально поверх Stage 1 і Stage 2A. Відновлення до HEAD, commit, push і deploy не виконувалися.

## Створені сторінки

- `/en/` — Home: англійська версія поточної композиції головної, SEO для aesthetic equipment repair, professional laser service, diode laser repair, laser handpiece repair, IPL та Nd:YAG.
- `/en/services/` — Services: усі 15 наявних категорій, початкові ціни з канонічних PL-послуг та індивідуальна оцінка післягарантійного сервісу. Додатковий наявний пункт Output checks and optimisation збережено без вигаданої ціни.
- `/en/contact/` — Contact: контактні дані, форма, згода, кнопки, процес обслуговування й підписи англійською.

Використано відповідні PL/RU сторінки як фактичні джерела, British English, чинні CSS, зображення й компоненти. CSS і зображення не змінювалися. Посилання на ще не перекладені детальні послуги, прайс, кейси, блог, партнерів та PDF явно позначено `(Polish)`. PL/RU посилання самого мовного перемикача залишаються з рідними назвами мов.

На головній додано блок із двома наявними за стилем contact-card:

- **On-Site Equipment Service** — тільки після підтвердження можливості, місця і витрат на виїзд.
- **Ship Equipment for Repair in Poland** — погодження придатності обладнання/компонентів до перевезення, пакування та доставки до Вроцлава до відправлення.

Не заявлено безумовного обслуговування всієї Європи. Посилань на planned міжнародні маршрути немає. Нових представництв, послуг, цін чи гарантій не додано. Наявні в PL FAQ строки 1–3 робочі дні та стандартна гарантія 3–6 місяців перекладені з джерела, а не встановлені заново; залежність від складності, обладнання та частин збережена.

## Послуги та ціни

| Послуга | Ціна |
|---|---|
| Diode laser diagnostics | from PLN 600 |
| Laser diode replacement and calibration | from PLN 800 |
| Handpiece and applicator refurbishment | from PLN 800 |
| Cooling system repair | from PLN 1,000 |
| Power supply and electronics repair | from PLN 600 |
| Touchscreen and control panel repair | from PLN 600 |
| IPL equipment servicing | from PLN 800 |
| Nd:YAG laser servicing | from PLN 800 |
| CO₂ laser servicing | from PLN 1,200 |
| Picosecond laser servicing | from PLN 1,200 |
| RF equipment repair | from PLN 600 |
| LPG equipment repair | from PLN 800 |
| Cryotherapy equipment servicing | from PLN 1,200 |
| Aesthetic equipment cleaning and maintenance | from PLN 1,200 |
| Post-warranty servicing | individually after diagnostics |

Пояснено, що початкова сума не є ціною повного модуля/джерела/дисплея; частини й додаткові роботи оцінюються окремо, виїзд і транспорт оплачуються окремо, фінальна вартість погоджується після діагностики. Окрема калібровка CO₂ — PLN 1,600 відповідно до чинної PL-сторінки; не включена автоматично в ремонт від PLN 1,200. Для деталей є явно позначені переходи до PL-джерел. 15 EN посадкових не створювалися.

## SEO та генерація

Тільки три записи en у `site-locales.json` переведено у published; стабільні ID та x-default не змінені. Інші 65 EN маршрутів залишаються planned.

Кожна EN сторінка має lang=en, self-canonical, унікальні title/description, EN OG/Twitter, og:locale=en_GB, BreadcrumbList. FAQ JSON-LD перекладено синхронно з видимими відповідями. LocalBusiness зберігає ідентичність `/#organization`, фактичні адресу, телефон, географію, години й соціальні канали; Service на EN-каталозі посилається на ту саму організацію.

Для шести відповідних PL/RU сторінок додано EN hreflang та OG alternate. Sitemap містить три нові URL і взаємні мовні посилання для дев'яти сторінок трьох груп. Решта sitemap-маршрутів не змінені.

Мовний компонент згенерований чинним `build-language-switcher.py`. PL/RU/EN доступні тільки в трьох готових групах. На інших сторінках EN не видається за готовий переклад. `404.html` зберігає попередні PL/RU посилання на головні: це не мовна група EN-404.

Згенеровано три Markdown-сторінки, оновлено мовні посилання в шести PL/RU Markdown, llms, llms-full, `_headers` і AI Catalog. Catalog.languages тепер pl/ru/en; resources містять усі 133 сторінки. 15 сервісних записів поки мають лише фактичні PL/RU детальні локалізації: EN-каталог не підміняє 15 окремих посадкових. Статті й кейси залишилися PL/RU.

| Показник | До Stage 2B | Після |
|---|---:|---:|
| Канонічні сторінки у sitemap | 130 | 133 |
| PL / RU / EN HTML | 65 / 65 / 0 | 65 / 65 / 3 |
| Markdown | 130 | 133 |
| Тримовні групи | 0 | 3 |
| Planned EN маршрути | 68 | 65 |
| AI Catalog: послуги / статті / кейси | 15 / 42 / 44 | 15 / 42 / 44 |

Published тут означає готовність у локальному реєстрі та збірці; сайт не розгортався.

## Лазар, форми та n8n

На всіх трьох EN HTML встановлено `data-lazar-enabled="false"`. `js/lazar-ai.js` завершує ініціалізацію для EN, якщо значення не дорівнює true. Немає видимої кнопки, чату або автоматичного запиту; наявні прямі контакти доступні. PL/RU Лазар працює без зміни поведінки, endpoint та session ID.

Для mock-тестів браузер змінює атрибут лише в перехопленій HTML-відповіді. Так перевірено ASK LAZAR, англійський інтерфейс/помилки, `/en/contact/`, language=en та стабільний session ID. Test-only увімкнення не зберігається в HTML і не є перемикачем через query/localStorage.

EN-форми зберігають початковий склад полів PL-джерел. Homepage і Contact не мали serviceType — його не додано. Поля source локалізовані в en-homepage / en-contact, language=en. Webhook, структура payload, обробка успіху/помилки й service_lead_submit збережені. Нових полів міжнародної логістики немає.

**Backend EN не підтверджено.** Серверний workflow недоступний; реальні запити до n8n не виконувалися. Перед відкриттям чату потрібно перевірити language=en, prompt/мову відповіді, обробку помилок і зміну мови в наявній сесії. Реальне приймання EN заявок та маршрутизація en-homepage/en-contact також потребують окремо погодженої серверної перевірки. Публічний EN-чат до цього залишається прихованим.

## Перевірки

PASS:

- `build-site.py` і повторна збірка: жодних побайтових змін при повторному запуску.
- `check-site-locales.py`, `check-language-switcher.py`, `check-ai-search.py`, `check-geo-seo.py`, `check-ai-catalog.py`.
- `build-ai-search.py --check`, `build-ai-catalog.py --check`, `build-service-cases.py --check`, `build-language-switcher.py --check`: stale відсутні.
- `check-english-pages.py`: рівно три EN HTML, business facts проти PL, self-canonical/reciprocal SEO, BreadcrumbList, 15 цін, незмінний контракт полів, відсутність planned-посилань, chat gate.
- Загальний статичний аудит: 134 HTML з урахуванням 404, 133 канонічні сторінки/Markdown, 16 381 перевірене посилання, 124 FAQ schema questions; issues порожні.
- `check-english-pages.cjs`: усі 133 канонічні URL повернули HTTP 200; 9 layout-сценаріїв (3 EN сторінки × 320/390/1440), зображення завантажуються, немає горизонтального overflow чи JS pageerror. Dropdown, перехід EN → PL → EN, клавіатура, burger, FAQ, відсутність planned-посилань і прихований чат.
- EN Home і Contact: required/consent validation, loading, 500 та success через mock webhook, точні payload-поля, language/source, одна success-подія service_lead_submit.
- `check-lazar-ai.cjs`: 27 layout/scenario груп PL/RU/EN плюс storage denial; усі webhook mock, EN тільки з test override.
- `check-language-runtime.cjs`: 47 груп PL/RU та en/en-GB/unknown runtime, включно з перемиканням без JavaScript. Оновлено перевірку End для фактичної останньої опублікованої мови.
- `check-lightsheer-desire.py`, `check-cooling-maintenance.py`, `check-used-laser-buying.py`.
- `git diff --check`; Python cache відсутній. CSS, оригінальні зображення та всі попередні локальні зміни Stage 1/2A збережено.

П'ять історичних разових аудитів не PASS: `check-poznan.py`, `check-co2-poznan.py` очікують HEAD + 4 URL; `check-pharaon.py`, `check-gme.py` очікують історичний кейс першим; `check-rsl-laser-maintenance.py` порівнює старий порядок карток із HEAD. Поточний запуск відтворив ті самі відомі з Stage 1/2A умови. Їх не послаблювали; production build від них не залежить.

## Скриншоти

| Сторінка | Desktop 1440 | Mobile 390 | Mobile 320 | Повна сторінка |
|---|---|---|---|---|
| Home | [Desktop](qa/stage2b/home-1440.png) | [390](qa/stage2b/home-390.png) | [320](qa/stage2b/home-320.png) | [Full](qa/stage2b/home-full.png) |
| Services | [Desktop](qa/stage2b/services-1440.png) | [390](qa/stage2b/services-390.png) | [320](qa/stage2b/services-320.png) | [Full](qa/stage2b/services-full.png) |
| Contact | [Desktop](qa/stage2b/contact-1440.png) | [390](qa/stage2b/contact-390.png) | [320](qa/stage2b/contact-320.png) | [Full](qa/stage2b/contact-full.png) |

[Home form](qa/stage2b/home-form.png), [Contact form](qa/stage2b/contact-form.png), [Lazar — увімкнений тільки в mock-тесті](qa/stage2b/lazar-mock-only.png), [browser results](qa/stage2b/results.json).

## Відкриті ризики

- n8n/реальне отримання EN заявок і відповіді Лазаря не перевірені; чат закритий за замовчуванням.
- SEO перевірено на локальній збірці. Live URL, індексація, production Lighthouse/CWV та фактичне отримання GA4/GTM подій не перевірялися; гарантії індексації немає.
- Англійськими є HTML-тексти, alt/aria та runtime. Оригінальні фотографії/інфографіка збережені без ретуші; на частині зображень є вбудовані польські написи. PDF залишається польськомовним і позначений відповідно. Повна локалізація написів у растрових матеріалах потребує окремих локалізованих версій зображень.
- Строки й гарантія відповідають наявним джерелам. Міжнародні умови описані лише як попередньо погоджувана можливість, без нової blanket-географії чи окремих представництв.

## Файли

Нижче наведено зміни саме Stage 2B відносно стану на початку роботи, а не весь накопичений diff Stage 1/2A.

### Створено

- `en/contact/index.html`
- `en/contact/index.md`
- `en/index.html`
- `en/index.md`
- `en/services/index.html`
- `en/services/index.md`
- `scripts/check-english-pages.cjs`
- `scripts/check-english-pages.py`
- `docs/multilingual-stage2b-report.md`
- `docs/qa/stage2b/contact-1440.png`
- `docs/qa/stage2b/contact-320.png`
- `docs/qa/stage2b/contact-390.png`
- `docs/qa/stage2b/contact-form.png`
- `docs/qa/stage2b/contact-full.png`
- `docs/qa/stage2b/home-1440.png`
- `docs/qa/stage2b/home-320.png`
- `docs/qa/stage2b/home-390.png`
- `docs/qa/stage2b/home-form.png`
- `docs/qa/stage2b/home-full.png`
- `docs/qa/stage2b/lazar-mock-only.png`
- `docs/qa/stage2b/results.json`
- `docs/qa/stage2b/services-1440.png`
- `docs/qa/stage2b/services-320.png`
- `docs/qa/stage2b/services-390.png`
- `docs/qa/stage2b/services-full.png`

### Змінено

- `_headers`
- `ai-catalog.json`
- `index.html`
- `index.md`
- `js/lazar-ai.js`
- `kontakt/index.html`
- `kontakt/index.md`
- `llms-full.txt`
- `llms.txt`
- `ru/index.html`
- `ru/index.md`
- `ru/kontakt/index.html`
- `ru/kontakt/index.md`
- `ru/uslugi/index.html`
- `ru/uslugi/index.md`
- `scripts/build-language-switcher.py`
- `scripts/check-language-runtime.cjs`
- `scripts/check-lazar-ai.cjs`
- `scripts/check-site-locales.py`
- `scripts/site-locales.json`
- `sitemap.xml`
- `uslugi/index.html`
- `uslugi/index.md`

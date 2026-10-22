# Stage 1 — архітектура PL/RU/EN

Дата: 2026-10-21. Усі зміни локальні. Commit, push і deploy не виконувалися.

## Архітектура

`scripts/site-locales.json` — єдиний реєстр ідентичності, типів і публікації мовних маршрутів. Містить 65 наявних груп PL/RU з EN `planned` та три окремі EN-only міжнародні групи, також `planned`. Разом: 68 груп, 130 published і 68 planned маршрутів. Міжнародним сторінкам не призначено вигаданих PL/RU відповідників.

Кожна група має незмінний `id`, `type`, `x_default` та `routes`: мова → `{url, status}`. URL — шлях від кореня; домен заданий один раз у `base_url`. ID початково утворені з PL-шляху, але після створення мають залишатися незмінними, навіть за майбутнього перейменування URL. Реєстр не містить текстів, цін, описів чи бізнес-даних. Наявні `x_default` збережені точно; для неопублікованих міжнародних груп він поки `null`.

`scripts/site_locales.py` перевіряє унікальність ID/URL, мовні префікси, типи, статуси і x-default. Надає лише published-маршрути та очікувану карту hreflang. Класифікація генераторів залежить від `type`, а не від польського написання `/uslugi/` або `/realizacje/`.

`build-ai-search.py` вимагає точного збігу published-реєстру із sitemap, self-canonical, HTML lang і взаємними hreflang. Помилка статусу/маршруту зупиняє збірку. Запис `planned` не генерує HTML, Markdown чи AI-записів. Markdown підтримує EN службові підписи та мовні посилання. llms додає лише реально відкриті discovery EN-сторінки; нинішній PL/RU вміст і порядок збережено.

`build-ai-catalog.py` підтримує третю локалізацію послуг, англійські назви секцій/полів і `from … PLN`, не вигадуючи значення за відсутності джерела. Список мов походить із опублікованих сторінок. Наявні ID послуг, їхні primary URL і бізнес-дані залишаються тими самими.

`build-service-cases.py` зіставляє старі посилання в `service-cases.json` із групами реєстру, отримує мовні URL і статуси з реєстру. Сам `service-cases.json` збережений як джерело зв'язків, зображень і текстів карток. Неопубліковані переклади кейсів пропускаються; для опублікованого кейсу відсутній текст картки відповідною мовою — помилка. Видимі картки й Service.subjectOf отримують однаковий список доказів. Переклад не підміняється іншою мовою.

## Файли

Створено:

- `scripts/site-locales.json`
- `scripts/site_locales.py`
- `scripts/check-site-locales.py`
- `docs/multilingual-stage1-report.md`

Змінено:

- `scripts/build-ai-search.py`
- `scripts/build-ai-catalog.py`
- `scripts/build-service-cases.py`
- `scripts/build-site.py`
- `scripts/check-ai-search.py`
- `scripts/check-ai-catalog.py`
- `scripts/check-lazar-ai.cjs`
- `scripts/check-lightsheer-desire.py`
- `scripts/check-cooling-maintenance.py`
- `scripts/check-used-laser-buying.py`
- `scripts/check-poznan.py`
- `scripts/check-co2-poznan.py`
- `scripts/check-pharaon.py`
- `scripts/check-gme.py`
- `scripts/check-rsl-laser-maintenance.py`

В останніх восьми Python-аудитах змінено лише очікування мовних SEO-карт/посилань. Їхні предметні PL/RU перевірки зображень, текстів і історичних змін збережені. `check-geo-seo.py` вже використовує спільне discovery і не потребував правок. `check-lazar-ai.cjs` обирає опубліковані мови й маршрути з реєстру; EN перевірятиметься після публікації. Очікуваний майбутній підпис EN — `ASK LAZAR`; реалізації цього підпису в runtime поки немає.

## До / після

| Показник | До | Після |
|---|---:|---:|
| Канонічні HTML у sitemap | 130 | 130 |
| Опубліковані PL/RU пари | 65 | 65 |
| Опубліковані EN HTML / Markdown | 0 / 0 | 0 / 0 |
| Markdown сторінки | 130 | 130 |
| AI Catalog: послуги / статті / кейси | 15 / 42 / 44 | 15 / 42 / 44 |
| AI Catalog: мови | pl, ru | pl, ru |
| Єдиний реєстр маршрутів | відсутній | 68 груп |

SHA256 порівняння з початковим станом: усі наявні файли поза `scripts/` побайтово незмінні, зокрема всі HTML/Markdown, CSS/JS, зображення, sitemap, robots, `_headers`, llms, ai-catalog.json, netlify.toml. Єдиний новий файл поза scripts — цей звіт. AI Catalog SHA256: `a97b40e15cb0e20ac48ef8dc46ca1d64ab0bd7b63bb6dda20126419a3dd82428`.

## Перевірки

Успішно:

- `build-site.py` повторно; `build-ai-search.py --check`, `build-ai-catalog.py --check`, `build-service-cases.py --check` — жодних застарілих ресурсів; вихідні артефакти стабільні.
- `check-site-locales.py`: 130 published, 68 planned; відсутність planned HTML/Markdown і посилань у sitemap/AI ресурсах; відхилення дублікатів ID/URL, невідомих мов, статусів, неправильних префіксів та unpublished x-default.
- Реальне discovery з підміною IO лише у пам'яті: всі 68 EN-маршрутів імітовано як published, усі типи сторінок та EN-only міжнародні групи розпізнаються; при поверненні статусу planned EN-записи sitemap відхиляються. HTML-файли не створювались.
- `check-ai-catalog.py`: третя локалізація у пам'яті, EN starting price/секції, стабільний ID послуги, Markdown/llms, відсутність фіктивних перекладів, ціни, timestamp, детермінованість і read-only check.
- `check-ai-search.py`: 131 HTML з урахуванням 404, 130 Markdown, 130 sitemap URL, 16 001 посилання; issues порожні.
- `check-geo-seo.py`: 130 сторінок, 112 FAQ schema questions, одна NAP-версія, issues порожні.
- `check-lightsheer-desire.py`, `check-cooling-maintenance.py`, `check-used-laser-buying.py`.
- `check-lazar-ai.cjs`: 18 груп layout/scenario та storage denial, PL/RU, mobile/desktop, помилки/retry, payload/analytics, без реальних звернень до webhook.
- Локальний HTTP: усі 130 URL повертають 200.
- Python syntax, `git diff --check`, контроль незмінності опублікованих артефактів.

П'ять історичних разових pre-commit аудитів не проходять і в незмінених версіях з HEAD:

- `check-poznan.py`, `check-co2-poznan.py`: очікують sitemap = HEAD + 4 URL.
- `check-pharaon.py`, `check-gme.py`: очікують свій старий кейс першим у поточному списку.
- `check-rsl-laser-maintenance.py`: очікує стару структуру списку карток відносно HEAD.

Це не нові регресії; для кожного підтверджено такий самий AssertionError на тій самій історичній умові у версії з HEAD. Умови не послаблювалися в межах мовної задачі. Поточний production build не залежить від цих разових аудитів.

Команди запускалися з `PYTHONDONTWRITEBYTECODE=1`; production build передає цей прапорець дочірнім процесам. Наявні ігноровані Python-кеші прибрано. Тимчасові тестові дані не додані до репозиторію.

## Другий етап і ризики

Архітектура готова до другого етапу створення EN-контенту. Це не означає готовність англійської версії до публікації.

Для кожного перекладу одним узгодженим набором змін потрібно:

1. Підготувати справжній EN HTML із self-canonical, `lang=en`, локалізованими метаданими й schema.
2. Перевести тільки відповідний маршрут у `published`, не змінюючи стабільний ID і поточний x-default.
3. Оновити reciprocal hreflang в усіх опублікованих версіях цієї групи та відповідні sitemap-рядки. Самостійного переписування sitemap або HTML SEO на цьому етапі не додано: реєстр перевіряє контракт і блокує розбіжності.
4. Додати реальні EN тексти карток для вже опублікованих кейсів, якщо вони використовуються на EN-послузі.
5. Запустити build і валідатори; перевірити вихідні артефакти та браузер.

Окремо на другому етапі необхідні EN runtime-підписи форм/Лазаря, підтримка EN у n8n, доступний перемикач і браузерні тести. Ці production CSS/JS, webhook та GTM/GA4 не змінювались. Реальні n8n/GA4/GTM та production URL не тестувалися.

EN-only міжнародні сторінки мають окремі ID; не можна пов'язувати їх hreflang з нееквівалентними PL/RU сторінками. Потрібне підтвердження фактичної географії виїздів, умов доставки та ремонту. Додавання маршруту не підтверджує бізнес-послугу. Для EN-only сторінок майбутній x-default слід визначити явно; зараз він не публікується.

Англійські секції для AI Catalog повинні відповідати підтримуваним семантичним заголовкам (наприклад, Service scope, Work performed, Result); відсутні факти не заповнюються припущеннями. Історичні разові аудити варто окремо перетворити на постійні регресійні тести — це виходить за межі Stage 1.

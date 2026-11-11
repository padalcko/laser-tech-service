# Аудит і автоматизація публікації — 2026-11-11

## Причина та фактична архітектура

Це статичний HTML/CSS/JS-сайт із Python-генераторами (стандартна бібліотека), без Vite/Next/Astro. Контентні джерела — HTML у корені та вкладених мовних/тематичних каталогах, а для окремих компонентів — scripts/ і content/. Реєстр scripts/site-locales.json керує наявними перекладами та AI-ресурсами.

До змін netlify.toml уже визначав publish = "dist" і команду python3 scripts/build-site.py && python3 scripts/package-site.py. Проте build-site.py сам не пакував результат, окремої перевірки dist не було, package.json і GitHub Actions були відсутні. Локальний dist був застарілим: 9 HTML відсутні, 201 HTML відрізнявся від поточного source. Статичні URL та перелік існуючих джерел не були проблемою: пакувальник використовував copytree, а не ручний список сторінок.

У HEAD пакувальник не виключав dist зі свого обходу. Початкові незакомічені зміни вже додавали це виключення; виправлення збережене у новому механізмі. Крім того, оптимізатор та check-ai-search повторно сканували dist як джерело. Старий AI-checker відхиляв коректне коротке Organization-посилання з @id без повторного url на трьох Pure Studio сторінках. Тепер правильний @id залишається обов'язковим, а url обов'язковий для LocalBusiness і перевіряється в Organization, коли вказаний. Контент JSON-LD не змінювався.

Це встановлені локальні причини ненадійності. Причину конкретного попереднього production deploy неможливо остаточно встановити без журналів Netlify.

## Інвентар

| Показник | Значення |
|---|---:|
| Source HTML | 271 |
| PL, включно зі спільною 404 | 91 |
| RU | 90 |
| EN | 90 |
| Старий dist | 262 |
| Відсутні раніше | 9 |
| Лише у старому dist | 0 |
| Поточний dist | 271 |
| Публічні файли | 1783 |
| Sitemap URL | 270 |

Спільна 404 має noindex і правильно виключена із sitemap. Усі наявні категорії, включно з головними, послугами, прайсом, мережами, обладнанням у послугах, блогом, реалізаціями, партнерами, About і контактами перевіряються через повний файловий інвентар, а не список категорій. Окремих вигаданих мовних версій не створено. Дублювання source/dist — очікувана генерація; унікальність canonical/sitemap перевірена.

Відновлені у локальному dist маршрути:

- `/blog/dlaczego-regularny-serwis-lasera-jest-wazny-pure-studio/`
- `/blog/pomiar-mocy-lasera-laserpoint/`
- `/en/blog/laser-power-measurement-laserpoint/`
- `/en/blog/why-regular-laser-maintenance-matters-pure-studio/`
- `/en/case-studies/diode-laser-service-pure-studio-wroclaw/`
- `/realizacje/serwis-lasera-diodowego-pure-studio-wroclaw/`
- `/ru/blog/izmerenie-moshchnosti-lazera-laserpoint/`
- `/ru/blog/pochemu-vazhno-obsluzhivat-lazer-pure-studio/`
- `/ru/realizacje/obsluzhivanie-diodnogo-lazera-pure-studio-vrotslav/`

## Єдиний процес

- `npm ci --ignore-scripts` — відтворювана установка; npm-залежностей немає. Python build не потребує сторонніх пакетів.
- `npm run build` — існуючі генератори та перевірки → пакування → validate-dist. Будь-який ненульовий код зупиняє Netlify.
- `npm run validate:dist` — незалежна перевірка готового результату.
- `npm run test:build` — ізольовані наскрізні регресійні тести.

`public_site.py` автоматично виявляє всі HTML та дозволені типи ресурсів за межами приватних каталогів. Вкладені шляхи зберігаються. Приховані файли, scripts/content/docs/reports, node_modules, конфігурації пакетів та службова документація не публікуються. Символічні посилання в публічному дереві відхиляються. Це не copytree всього репозиторію.

HTML, CSS, JS, фото, SEO та службові файли копіюються побайтово. Реєстр перекладів не є списком пакування: нова самостійна HTML-сторінка потрапляє до dist без його редагування. Індексована сторінка з правильним self-canonical автоматично додається до sitemap у dist з її фактичними hreflang. Source sitemap та SEO-тексти не переписуються. Noindex-сторінки також публікуються, але не додаються в sitemap. Неправильна canonical/мова або відсутній ресурс зупиняють build. Участь у розширених AI-ресурсах/групах перекладів залишається окремим існуючим контентним контрактом.

Перевірка порівнює всі source/dist файли та HTML, виявляє зайві/застарілі файли, перевіряє локальні HTML-посилання, srcset, CSS url/import, літеральні JS-шляхи до основних ресурсів, canonical/hreflang та їх взаємність, sitemap і redirects. Зовнішні URL не трактуються як локальні; redirects враховуються. SPA у цьому проєкті немає. Динамічно обчислювані JS-запити потребують окремого runtime QA.

## Змінені файли системи

- package.json, package-lock.json — стандартні npm-команди без нового фреймворку.
- scripts/build-site.py — пакування та валідація в кінці єдиного процесу.
- scripts/package-site.py, scripts/public_site.py — безпечне автоматичне пакування й sitemap доповнення.
- scripts/validate-dist.py — повний машинозчитуваний інвентар та блокування неповного результату.
- scripts/test-publication.py — регресійний сценарій у тимчасовій копії.
- scripts/build-case-layout.py, scripts/build-blog-layout.py — існуючі layout-міграції застосовуються лише до їхніх реєстрованих сторінок; довільні нові HTML не примушуються до структури чужого шаблону.
- scripts/build-performance-assets.py — виключено dist і приватні каталоги зі сканування.
- scripts/check-ai-search.py — перевіряє свій AI-реєстр і 404; загальне охоплення всіх сторінок забезпечує validate-dist. Виправлено перевірку короткого Organization reference.
- netlify.toml — base = ".", command = "npm run build", publish = "dist", Node 22 / Python 3.13.
- .github/workflows/build.yml — push/PR: npm ci, build із validation, regression, артефакти звітів; жодного deploy.
- AGENTS.md — постійний контракт роботи з source та обов'язкової збірки.

## Перевірки та межі доказів

Локально npm ci, npm run build і validate:dist проходять. Перевірено 271 HTML, 1783 публічні файли, 270 URL sitemap, відсутність критичних broken links і збереження байтів source/dist. HTTP-перевірка локального dist: 271/271 маршрутів повертають 200. Це звичайний статичний HTTP-сервер, а не емуляція Netlify headers/redirects.

Ізольований тест починає без dist, додає 9 нових сторінок (реалізація/блог/послуга × PL/RU/EN) з фото та одну noindex-сторінку. Повний build знаходить усі без змін реєстрів. Перевірено відхилення відсутнього HTML/фото, застарілого HTML, випадкового приватного файлу та broken link. Після видалення fixture-джерел нова збірка повертається до 271 сторінки. Повторний повний build дає ідентичні SHA-256 усіх файлів dist. Тести виконуються у чистій тимчасовій копії поточного source; вихідні сторінки не забруднюються fixture-файлами.

GitHub Actions workflow створено, але віддалений запуск не виконувався: push заборонено користувачем. Браузерний хост недоступний, звернення до native Chrome завершилося timeout; візуальне та інтерактивне QA не підтверджено.

Read-only production перевірка: головна повертає 200 і Server: Netlify. Три LaserPoint URL повертають 200, шість Pure Studio URL — 404. Це стан попередньої публікації, не результат нового deploy. Панель Netlify і deployment logs недоступні; пов'язану гілку, стан automatic publishing і live build settings не підтверджено.

## Подальша публікація

`dist/` був і залишається ignored/untracked; міграція Git не потрібна. Після дозволеного commit/push Git-connected Netlify має виконувати root netlify.toml. Файлова конфігурація має пріоритет над відповідними UI-полями: https://docs.netlify.com/build/configure-builds/file-based-configuration/ . Якщо сайт зараз публікується вручну, треба під'єднати репозиторій padalcko/laser-tech-service/потрібну production-гілку, увімкнути automatic builds і перевірити журнал із командою npm run build та publish dist. Нових платних сервісів не потрібно.

Commit, push і production deploy не виконувалися. Наявні на початку локальні зміни About/Markdown/llms збережені. Дизайн, header/footer, меню, Lazar, тексти, фото, стилі та аналітика цим завданням не змінювалися.

## Машинозчитувані докази

- reports/dist-audit-before.json — повний список втрачених і застарілих HTML до змін.
- reports/dist-validation.json — кожна сторінка, URL, мова, SEO/byte parity, ресурси, готовність.
- reports/dist-regression.json — автоматичне включення, негативні тести, очищення, відтворюваність.
- reports/dist-http.json — локальні HTTP-статуси всіх сторінок.
- reports/dist-production-readonly.json — HTTP-спостереження чинного сайту без деплою.

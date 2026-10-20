# Сім посадкових послуг PL/RU — звіт

Дата: 2026-10-20. Зміни локальні. Commit, push і deploy не виконувалися.

## Інспекція

Перед роботою репозиторій був чистий. Перевірено PL/RU еталони діагностики діодних лазерів, `css/service-landing.css`, каталог і прайс, структуру SEO/форм, `scripts/service-cases.json`, генератори AI/Markdown і AI Catalog. Рекомендовані 14 маршрутів не існували. У каталогах уже були всі сім пунктів; їх перетворено на посилання без додаткових карток.

## Сторінки та ціни

### Naprawa układów chłodzenia urządzeń laserowych

- PL: `https://lasertechservice.pl/uslugi/naprawa-ukladow-chlodzenia/`
- RU: `https://lasertechservice.pl/ru/uslugi/remont-sistem-ohlazhdeniya/`
- Ціна: від 1 000 zł.

### Naprawa ekranów dotykowych i paneli sterowania

- PL: `https://lasertechservice.pl/uslugi/naprawa-ekranow-dotykowych/`
- RU: `https://lasertechservice.pl/ru/uslugi/remont-sensornyh-ekranov/`
- Ціна: від 600 zł.

### Serwis i naprawa laserów Nd:YAG

- PL: `https://lasertechservice.pl/uslugi/serwis-laserow-nd-yag/`
- RU: `https://lasertechservice.pl/ru/uslugi/servis-lazerov-nd-yag/`
- Ціна: від 800 zł.

### Serwis i naprawa laserów pikosekundowych

- PL: `https://lasertechservice.pl/uslugi/serwis-laserow-pikosekundowych/`
- RU: `https://lasertechservice.pl/ru/uslugi/servis-pikosekundnyh-lazerov/`
- Ціна: від 1 200 zł.

### Serwis i naprawa urządzeń LPG do endermologii

- PL: `https://lasertechservice.pl/uslugi/naprawa-urzadzen-lpg/`
- RU: `https://lasertechservice.pl/ru/uslugi/remont-oborudovaniya-lpg/`
- Ціна: від 800 zł.

### Czyszczenie i konserwacja urządzeń kosmetologicznych

- PL: `https://lasertechservice.pl/uslugi/konserwacja-urzadzen-kosmetologicznych/`
- RU: `https://lasertechservice.pl/ru/uslugi/tehnicheskoe-obsluzhivanie-oborudovaniya/`
- Ціна: від 1 200 zł.

### Serwis pogwarancyjny urządzeń kosmetologicznych

- PL: `https://lasertechservice.pl/uslugi/serwis-pogwarancyjny/`
- RU: `https://lasertechservice.pl/ru/uslugi/poslegarantiynoe-obsluzhivanie/`
- Ціна: індивідуально після діагностики.

## Композиція і зміст

Збережено фактичну композицію еталона: hero → чотири напрямки робіт → симптоми/причини звернення → етапи → вартість → технічний підхід → релевантні приклади/фото → пов’язані послуги → шість FAQ → форма. Всього 84 FAQ.

На кожній сторінці зазначено безкоштовну діагностику при замовленні ремонту або обслуговування спеціалістами Laser Tech Service, окрему оплату виїзду й транспортних витрат та погодження остаточної вартості робіт і частин. Мінімальна ціна не оголошується ціною дорогого модуля, джерела, дисплея або повного калібрування. Для післягарантійної послуги числової стартової ціни немає.

Технічні межі: рідина і промивання за документацією моделі; окрема заміна digitizer лише за конструктивної можливості; прошивки після оцінки моделі; Nd:YAG не ототожнено з усіма ламповими Q-Switch; для пікосекундних лазерів немає обіцянки ремонту будь-якого герметичного джерела чи вимірювання тривалості імпульсу; авторизація LPG Systems не заявляється; ТО не гарантує відсутності майбутніх поломок; наявність запчастин для всіх моделей не обіцяється.

## Фото

- Охолодження: наявний кейс заміни вентиляторів у Вроцлаві.
- Nd:YAG: наявний двомовний кейс ремонту Пельтьє і Nd:YAG, фото роботи з маніпулою 1152×2048 та готові 480/768 варіанти.
- ТО: існуюче фото очищеного теплообмінника 1280×960, посилання на існуючий кейс технічного огляду.
- Післягарантійний сервіс: існуючий кейс заміни залитого діодного модуля, у джерелі прямо описано негарантійний ремонт.
- Для ремонту екранів, LPG і пікосекундних джерел не знайдено достовірно відповідних фото виконаних робіт; випадкові зображення не додавалися. Для social preview використано наявний знак бренду.

Фото — WebP з width/height, локалізованими alt і lazy loading. Картки використовують загальний компактний формат Alma. Нових фото, блогів чи реалізацій немає.

## SEO та AI

Кожна сторінка має унікальні title, description, H1, canonical, взаємні PL/RU/x-default hreflang, OG/Twitter, Service та BreadcrumbList. Provider посилається на існуючий `#organization`; LocalBusiness не дублюється. Є внутрішні зв’язки між новими й наявними релевантними послугами, прайсом і джерельними кейсами.

Sitemap: 130 URL. Створено 14 відповідних Markdown-сторінок, оновлено каталогові Markdown, llms і `_headers` штатним генератором. AI Catalog: 15 послуг / 30 мовних посадкових, 42 статті, 44 кейси. Розширено розпізнавання категорій у чинному генераторі для Nd:YAG, пікосекундних лазерів, LPG, панелей, охолодження та косметологічного обладнання; категорії виводяться з фактичних заголовків. Паралельної бази даних немає.

## Перевірки

- Статичний аудит: 14 HTML, 84 FAQ, 988 локальних посилань/ресурсів, вкладеність HTML, унікальні ID, один H1, canonical/hreflang і sitemap, JSON-LD, структура полів форми та ідентичність footer/скриптів еталону — успішно.
- Ціни, чотири напрямки робіт, умови діагностики, виїзду і транспорту перевірено в усіх HTML та записах AI Catalog. Післягарантійна ціна у каталозі — null.
- `python3 scripts/build-site.py` — успішно, разом із `check-ai-search.py` та `check-geo-seo.py`, issues порожні.
- `build-ai-search.py --check`, `build-service-cases.py --check`, `check-ai-catalog.py` і `git diff --check` — успішно.
- SHA256-аудит: глобальні CSS/JS, фото, головні сторінки, попередні посадкові, блоги й реалізації не змінені; файлів не видалено.

Браузерна перевірка пройшла: 90 перевірок відображення (84 нових + 6 регресійних), без overflow, невдалого завантаження зображень і JS pageerror. Усі 14 форм пройшли перевірки. Результати `/tmp/lts-seven/browser-results.json`; сценарій `/tmp/lts-seven/browser.cjs`; знімки екрана в тій самій папці. Перевірено 14 сторінок на 320, 375, 390, 430, 768 і 1440 px, FAQ клавіатурою, мобільне меню, мовні перемикачі, CTA, required-поля, honeypot, success/error відповіді, payload та події конверсії; окремо — fallback без JavaScript та шість регресійних маршрутів.

## Обмеження

Результати стосуються локальної збірки. Webhook форм у браузерних тестах перехоплюється, сторонні запити блокуються. Реальні заявки, обробка n8n, отримання подій у GA4/GTM, production Lighthouse/CWV і live URL не перевірялися. Збережено наявні header/footer, Лазаря, соціальні канали та механіку форм; глобальні стилі не змінювалися. AI-файли не є гарантією індексації.

## Створені файли

- `ru/uslugi/poslegarantiynoe-obsluzhivanie/index.html`
- `ru/uslugi/poslegarantiynoe-obsluzhivanie/index.md`
- `ru/uslugi/remont-oborudovaniya-lpg/index.html`
- `ru/uslugi/remont-oborudovaniya-lpg/index.md`
- `ru/uslugi/remont-sensornyh-ekranov/index.html`
- `ru/uslugi/remont-sensornyh-ekranov/index.md`
- `ru/uslugi/remont-sistem-ohlazhdeniya/index.html`
- `ru/uslugi/remont-sistem-ohlazhdeniya/index.md`
- `ru/uslugi/servis-lazerov-nd-yag/index.html`
- `ru/uslugi/servis-lazerov-nd-yag/index.md`
- `ru/uslugi/servis-pikosekundnyh-lazerov/index.html`
- `ru/uslugi/servis-pikosekundnyh-lazerov/index.md`
- `ru/uslugi/tehnicheskoe-obsluzhivanie-oborudovaniya/index.html`
- `ru/uslugi/tehnicheskoe-obsluzhivanie-oborudovaniya/index.md`
- `uslugi/konserwacja-urzadzen-kosmetologicznych/index.html`
- `uslugi/konserwacja-urzadzen-kosmetologicznych/index.md`
- `uslugi/naprawa-ekranow-dotykowych/index.html`
- `uslugi/naprawa-ekranow-dotykowych/index.md`
- `uslugi/naprawa-ukladow-chlodzenia/index.html`
- `uslugi/naprawa-ukladow-chlodzenia/index.md`
- `uslugi/naprawa-urzadzen-lpg/index.html`
- `uslugi/naprawa-urzadzen-lpg/index.md`
- `uslugi/serwis-laserow-nd-yag/index.html`
- `uslugi/serwis-laserow-nd-yag/index.md`
- `uslugi/serwis-laserow-pikosekundowych/index.html`
- `uslugi/serwis-laserow-pikosekundowych/index.md`
- `uslugi/serwis-pogwarancyjny/index.html`
- `uslugi/serwis-pogwarancyjny/index.md`
- `docs/seven-service-pages-report.md`

## Змінені файли

- `_headers`
- `ai-catalog.json`
- `llms-full.txt`
- `llms.txt`
- `ru/uslugi/index.html`
- `ru/uslugi/index.md`
- `scripts/build-ai-catalog.py`
- `scripts/service-cases.json`
- `sitemap.xml`
- `uslugi/index.html`
- `uslugi/index.md`

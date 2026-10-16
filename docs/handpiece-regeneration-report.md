# Відновлення головок і маніпул — звіт

Дата: 2026-10-16. Реалізовано локально, без commit, push або deploy.

## Сторінки

- PL: `/uslugi/regeneracja-glowic-i-manipulatorow/`
- RU: `/ru/uslugi/vosstanovlenie-golovok-i-manipul/`

Еталон: локальні PL/RU сторінки діагностики діодних лазерів. Спроба прочитати публічний RU URL через вебінструмент повернула помилку; реалізацію та браузерне порівняння виконано за актуальним репозиторієм.

## Реалізація

Hero з ціною від 800 zł, умовами діагностики й окремої оплати виїзду/транспорту, CTA до форми та телефону. Сім симптомів із застереженням, що вони не є діагнозом. П'ять напрямків ремонту, сім етапів, ціни й умови, чотири пояснення технічного підходу сервісу, три реальні кейси, технічні статті, вісім FAQ та завершальна форма.

Використано наявні компоненти `main.css`, `cennik.css`, `blog.css`, `service-landing.css`, іконки `service-diagnostics.svg`, FAQ і скрипти форми. Глобальні CSS/JS та Lazar не змінені. Форма використовує чинний webhook і контракт полів, з `serviceType=laser-handpiece-regeneration` та окремим PL/RU source. Контейнер форми збережено з ідентифікатором `diagnostic-form`, щоб повторно використати стилі еталона.

Ціна від 800 zł не означає повну заміну всіх деталей. Окремі роботи та компоненти оцінюються індивідуально; чинні ціни прайсу не змінені. Не обіцяється ремонт кожної моделі або фіксований строк.

Картки кейсів генеруються через чинні `scripts/service-cases.json` і `build-service-cases.py`: залитий діодний модуль, негерметична головка, модуль Пельтьє ESTETECH. Три компактні картки в ряд на десктопі, дві на планшеті, одна на мобільному. Використано справжні наявні WebP, з розмірами, локалізованими alt, lazy loading та наявними responsive-варіантами. Матеріалів достатньо; нових зображень не вигадано.

## Перелінковка, SEO й AI

У PL/RU каталозі наявну назву послуги перетворено на посилання. Додано зворотні посилання зі сторінок діагностики та трьох релевантних реалізацій кожною мовою. Нові сторінки посилаються на діагностику, прайс, каталог ремонту й обслуговування, кейси та статті про діоди, TEC і герметичність. Окремих сторінок послуг ремонту діодних лазерів і техобслуговування в каталозі немає — використано наявний каталог, без вигаданих URL.

Унікальні title, description, H1, canonical, reciprocal PL/RU/x-default hreflang, OG/Twitter, хлібні крихти, Service та BreadcrumbList JSON-LD; Service посилається на спільний #organization і реальні кейси. Без вигаданих Offer, рейтингів чи відгуків. FAQ працює у видимому HTML без додавання FAQPage, як на еталоні. Актуальна документація Google повідомляє про припинення FAQ rich results: https://developers.google.com/search/updates (записи 8 травня та 15 червня 2026).

Оновлено sitemap з двома HTML URL і мовними зв'язками; Markdown не включено в sitemap. Чинним генератором створено обидва index.md, оновлено Markdown сторінок зі зворотними посиланнями, llms.txt, llms-full.txt та _headers. AI-файли доповнюють HTML і не гарантують індексації.

## Перевірки

- `python3 scripts/build-service-cases.py --check` — PASS.
- `python3 scripts/build-ai-search.py --check` — PASS, stale: [].
- `python3 scripts/check-ai-search.py` — issues: {}; 100 Markdown ресурсів, 100 sitemap URL, 11 529 перевірених локальних посилань.
- `python3 scripts/check-geo-seo.py` — issues: {}.
- Окрема перевірка обох сторінок: один H1, вісім FAQ, унікальні id, усі локальні посилання та fragment anchors існують, schema парситься, спільний обробник форми підключено один раз.
- Chrome/Playwright: PL і RU × 320, 375, 390, 430, 768, 1024, 1440 px — 14/14 PASS. Завантажено Montserrat. Без горизонтального переповнення, pageerror і локальних HTTP 4xx/5xx. Перевірено 1/2/3 колонки кейсів, декодування фото, мовні посилання, canonical, FAQ з Enter/Space, прокрутку CTA до форми.
- Форми: 14 успішних mock-відправлень, перевірено language/source/serviceType та очищення полів. Реальні заявки не надсилались; роботу сервера n8n цим тестом не підтверджено.
- Візуально переглянуто PL/RU mobile hero, форму та desktop case cards. Артефакти: `/tmp/lts-regeneration/`, результати `browser.json`, сценарій `browser.cjs`.
- `git diff --check` — PASS. У проєкті немає package.json та окремих npm lint/typecheck/build; виконано чинні генератори й валідатори.

Невирішених локальних проблем не виявлено. Публічні URL нових сторінок ще не перевірялися після деплою, Lighthouse/CWV та індексація Google не перевірялися. Непов'язані сторінки не редагувалися; глобальні SEO-валідатори пройшли, але кожну стару сторінку в браузері повторно не тестували.

## Створені файли

- `uslugi/regeneracja-glowic-i-manipulatorow/index.html`
- `uslugi/regeneracja-glowic-i-manipulatorow/index.md`
- `ru/uslugi/vosstanovlenie-golovok-i-manipul/index.html`
- `ru/uslugi/vosstanovlenie-golovok-i-manipul/index.md`
- `docs/handpiece-regeneration-report.md`

## Змінені файли

- `_headers`
- `llms-full.txt`
- `llms.txt`
- `realizacje/serwis-glowicy-lasera-diodowego-poznan/index.html`
- `realizacje/serwis-glowicy-lasera-diodowego-poznan/index.md`
- `realizacje/wymiana-modulu-diodowego-lasera-po-zalaniu-poznan/index.html`
- `realizacje/wymiana-modulu-diodowego-lasera-po-zalaniu-poznan/index.md`
- `realizacje/wymiana-modulu-peltiera-estetech-poznan/index.html`
- `realizacje/wymiana-modulu-peltiera-estetech-poznan/index.md`
- `ru/realizacje/serwis-glowicy-lasera-diodowego-poznan/index.html`
- `ru/realizacje/serwis-glowicy-lasera-diodowego-poznan/index.md`
- `ru/realizacje/wymiana-modulu-diodowego-lasera-po-zalaniu-poznan/index.html`
- `ru/realizacje/wymiana-modulu-diodowego-lasera-po-zalaniu-poznan/index.md`
- `ru/realizacje/zamena-modulya-pelte-estetech-poznan/index.html`
- `ru/realizacje/zamena-modulya-pelte-estetech-poznan/index.md`
- `ru/uslugi/diagnostika-diodnyh-lazerov/index.html`
- `ru/uslugi/diagnostika-diodnyh-lazerov/index.md`
- `ru/uslugi/index.html`
- `ru/uslugi/index.md`
- `scripts/service-cases.json`
- `sitemap.xml`
- `uslugi/diagnostyka-laserow-diodowych/index.html`
- `uslugi/diagnostyka-laserow-diodowych/index.md`
- `uslugi/index.html`
- `uslugi/index.md`

## Уточнення оформлення

Перед п’ятьма посиланнями блоку технічних статей додано декоративну золоту іконку глобуса в обох мовах. Прибрано абзац про виїзд, телефон та e-mail між заголовком і формою. Додано ізольовані правила `.service-related-links` у `css/service-landing.css` та символ `globe` у `img/icons/service-diagnostics.svg`; інші компоненти не змінені. Markdown оновлено, перевірка актуальності та `git diff --check` пройдені.

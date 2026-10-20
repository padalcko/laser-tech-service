# RF, кріотерапія та лазерні діоди — звіт

Дата: 2026-10-20. Зміни локальні; commit, push і deploy не виконувалися.

## Інспекція та реалізація

Еталон: `uslugi/diagnostyka-laserow-diodowych/index.html` та його RU-пара. Збережено композицію: hero → чотири напрямки робіт → симптоми → етапи → ціна → переваги → фото/приклад → пов’язані матеріали → FAQ → форма. Використано наявні класи `service-landing`, `price-grid`, `contact-card`, `service-steps`, `service-case`, FAQ та SVG-іконки. На кожній сторінці 8 FAQ. Глобальні CSS/JS і бібліотеки не змінювалися.

Header, footer, соціальні контакти, телефон, WhatsApp, скрипти аналітики та контракт форми збережено. Змінені лише назви послуги, `serviceType` та відповідні `source` у нових формах. Сервісні ідентифікатори: `rf-service`, `cryotherapy-service`, `laser-diode-service`.

## Маршрути

- rf / pl: `https://lasertechservice.pl/uslugi/naprawa-urzadzen-rf/`
- rf / ru: `https://lasertechservice.pl/ru/uslugi/remont-oborudovaniya-rf/`
- cryo / pl: `https://lasertechservice.pl/uslugi/serwis-urzadzen-do-krioterapii/`
- cryo / ru: `https://lasertechservice.pl/ru/uslugi/servis-oborudovaniya-dlya-krioterapii/`
- diode / pl: `https://lasertechservice.pl/uslugi/wymiana-i-kalibracja-diod-laserowych/`
- diode / ru: `https://lasertechservice.pl/ru/uslugi/zamena-i-kalibrovka-lazernyh-diodov/`

## Вартість і технічні обмеження

- RF: від 600 zł; калібрування тільки за можливостями моделі та процедурами виробника. Мікроголкові механізми — лише для відповідних моделей.
- Кріотерапія/кріоліполіз: від 1 200 zł; вакуумні вузли тільки для вакуумних моделей. Ремонт холодильного контуру після оцінки ремонтопридатності.
- Діоди: від 800 zł за початкову сервісну послугу. Чинний прайс окремо вказує 1 200 zł за роботу із заміни діода. Обидві суми розмежовано в ціновому блоці та FAQ; модуль, додаткові компоненти й обсяг калібрування оцінюються індивідуально. Прайс не змінено. У hero також зазначено, що модуль оцінюється окремо.
- Діагностика безкоштовна при замовленні ремонту або обслуговування; виїзд оплачується окремо.
- Показання дисплея не названо вимірюванням оптичної потужності; немає обіцянок універсальної сумісності чи заводської потужності без вимірювань.

## Фото та перелінковка

Використано існуючі WebP з розмірами, локалізованими alt і lazy loading. RF — реальна головка Alma Accent із задокументованого ремонту охолодження; посилання на польський опис явно позначено. Cryo-Vacuum — ілюстрація обладнання, без заяви про виконаний ремонт. Діоди — існуючий кейс заміни модуля після протікання в Познані, підключений через `scripts/service-cases.json`. Нових кейсів, статей або згенерованих зображень немає.

Існуючі пункти каталогів PL/RU перетворено на посилання без дублювання. Додані пов’язані послуги, прайс, відповідні статті й кейси. Для охолодження використано фактичний каталог послуг, для технічного обслуговування — прайс.

## SEO й AI

Шість унікальних title/description/H1, canonical, взаємні hreflang PL/RU/x-default, OG/Twitter, Service та BreadcrumbList. Provider посилається на існуючий `#organization`; новий LocalBusiness не додавався. Оновлено sitemap (116 URL), Markdown, llms, каталогові Markdown та службові `_headers` штатним генератором. HTML залишається джерелом контенту.

## Перевірки

- Статичний аудит 6 сторінок: HTML-вкладеність, унікальні ID, 48 FAQ, 420 локальних посилань/ресурсів, SEO, sitemap, форма, ідентичні footer та виконувані скрипти еталона — успішно.
- Chrome/Playwright: 36 перевірок нових сторінок на 320, 375, 390, 768, 1024, 1440 px та 6 регресійних перевірок каталогів, діагностики й електроніки на 320 px — без overflow та JS pageerror; зображення завантажуються.
- У всіх 6 мовних сторінках перевірено FAQ клавіатурою, мобільне меню, перемикання мови, CTA до форми, required-поля, honeypot, успіх/помилку з перехопленим webhook, payload і подію `service_lead_submit` у dataLayer. Перевірено FAQ та контактний fallback без JavaScript.
- `build-ai-search.py --check`: 116 сторінок, застарілих ресурсів немає.
- `check-ai-search.py`: issues порожній.
- `check-geo-seo.py`: issues порожній. Його лічильник FAQ стосується schema FAQPage; 48 нових UI-питань перевірено окремо.
- `build-service-cases.py --check`: картки актуальні.
- `git diff --check`: успішно.
- Порівняння SHA256 із початком задачі підтвердило незмінність CSS/JS, зображень, головних сторінок, попередніх посадкових, блогів і реалізацій; видалених файлів немає.

Браузерні артефакти: `/tmp/lts-rf-cryo-diode/browser-results.json`, `functional.cjs`, `static-results.json`, знімки екрана. Фінальну верстку після текстових уточнень перевірено окремо на тих самих шести ширинах; результати в `final-layout.json`.

## Межі перевірки

Зовнішні запити в браузерних тестах блокувалися, webhook замінено тестовою відповіддю. Реальні заявки, отримання лідів у n8n, доставка подій до GA4/GTM, production Lighthouse/CWV та опубліковані URL не перевірялися. Результати стосуються локальної версії. Окремого package/lint build у проєкті немає; використано наявні Python-генератори й валідатори.

## Створені файли

- `ru/uslugi/remont-oborudovaniya-rf/index.html`
- `ru/uslugi/remont-oborudovaniya-rf/index.md`
- `ru/uslugi/servis-oborudovaniya-dlya-krioterapii/index.html`
- `ru/uslugi/servis-oborudovaniya-dlya-krioterapii/index.md`
- `ru/uslugi/zamena-i-kalibrovka-lazernyh-diodov/index.html`
- `ru/uslugi/zamena-i-kalibrovka-lazernyh-diodov/index.md`
- `uslugi/naprawa-urzadzen-rf/index.html`
- `uslugi/naprawa-urzadzen-rf/index.md`
- `uslugi/serwis-urzadzen-do-krioterapii/index.html`
- `uslugi/serwis-urzadzen-do-krioterapii/index.md`
- `uslugi/wymiana-i-kalibracja-diod-laserowych/index.html`
- `uslugi/wymiana-i-kalibracja-diod-laserowych/index.md`
- `docs/rf-cryo-diode-service-report.md`

## Змінені файли

- `_headers`
- `llms-full.txt`
- `llms.txt`
- `ru/uslugi/index.html`
- `ru/uslugi/index.md`
- `scripts/service-cases.json`
- `sitemap.xml`
- `uslugi/index.html`
- `uslugi/index.md`

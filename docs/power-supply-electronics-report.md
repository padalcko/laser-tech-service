# Ремонт блоків живлення та електроніки — звіт

Дата: 2026-10-19. Робота виконана локально; commit, push та deploy не виконувалися.

## Реалізація

Створено дві повноцінні посадкові сторінки на основі локального вихідного коду еталона `/ru/uslugi/diagnostika-diodnyh-lazerov/` і його польської версії. Збережено класи, стилі, порядок основних секцій еталона, навігацію, футер, соціальне меню, FAQ, контактну форму й механізми аналітики.

Маршрути готові до публікації, але ще не опубліковані:

- PL: https://lasertechservice.pl/uslugi/naprawa-zasilaczy-i-elektroniki/
- RU: https://lasertechservice.pl/ru/uslugi/remont-blokov-pitaniya-i-elektroniki/

Секції в порядку сторінки:

1. Hero: назва, опис, ціна від 600 zł, умови діагностики та виїзду, CTA і телефон.
2. Чотири напрямки: заміна блока, відновлення електропроводки/джгутів/з’єднань, компонентний ремонт, оцінка ремонтопридатності.
3. Симптоми: відсутність запуску, вимкнення/перезапуск, помилки живлення, нестабільність електроніки, кабелі/роз’єми, напруга, перегрів/запах. Окрема рекомендація припинити роботу при небезпечних ознаках.
4. Сім етапів від звернення до контрольної перевірки.
5. Пояснення необхідності професійного ремонту.
6. Вартість: від 600 zł; остаточний розрахунок, окреме погодження деталей, діагностика та транспорт.
7. Дві реальні реалізації: 3000 NAIN і RSL.
8. Пов’язані послуги та технічні статті.
9. Вісім FAQ кожною мовою.
10. Завершальний CTA і чинна форма звернення.

Не заявлено фіксовані строки, гарантії, рейтинги чи сертифікації. Ціна від 600 zł не подається як вартість будь-якого нового блока з усіма деталями. Не кожний блок ремонтопридатний; рішення після діагностики.

## Дизайн і фотографії

Глобальні CSS/JS не змінено, нових бібліотек не додано. Використано існуючі main.css, cennik.css, blog.css, service-landing.css і відповідні JS. Hero зберігає оформлення еталона.

Повторно використано наявні оптимізовані WebP без дублювання файлів:

- `img/realizacje/3000-nain/naprawa-elektroniki-3000-nain.webp` — реальна пайка/ремонт електроніки, 900×1600, 119432 байти; також OG/Twitter.
- `img/realizacje/rsl-warszawa/rsl-naprawa-zlacza-manipuly-warszawa.webp` — робота зі з’єднанням; наявні srcset 480/768/941 px.

Для фото в картках задано width/height, lazy loading, decoding і локалізовані alt. Картки формує чинний `scripts/build-service-cases.py` з `scripts/service-cases.json`. RSL явно описаний як косметологічний апарат, не лазер.

## SEO та перелінковка

- Унікальні SEO title/description, H1, логічні H2–H3, canonical, взаємні hreflang PL/RU/x-default, OG/Twitter.
- Service + BreadcrumbList JSON-LD; FAQPage не додано.
- Два URL додано до sitemap, загальна кількість — 106.
- Назва послуги в існуючих каталогах PL/RU стала посиланням. Додано посилання з діагностики, відновлення головок і кейсу 3000 NAIN.
- Нові сторінки посилаються на діагностику, загальний каталог ремонту, техобслуговування, відновлення головок, реалізації та технічні статті.
- Після HTML-змін згенеровано Markdown, llms.txt, llms-full.txt і _headers штатним build-ai-search.py. robots.txt та _redirects не змінено.

## Форма та аналітика

Збережено HTML-контракт і JS чинної форми, required/consent/honeypot, endpoint та обробку успіху/помилки. Ідентифікатори `diagnostic-form`/`diagnostic-title` залишено для сумісності з існуючими селекторами. Назва serviceType — `power-supply-electronics-repair`; source — `pl-power-supply-electronics-repair` або `ru-power-supply-electronics-repair`. Реальні звернення не надсилалися.

## Статичні перевірки

- `python3 scripts/build-service-cases.py --check` — current.
- `python3 scripts/build-ai-search.py --check` — stale = [].
- `python3 scripts/check-ai-search.py` — issues = {}.
- `python3 scripts/check-geo-seo.py` — issues = {}.
- `git diff --check` — без помилок.
- Окремий аудит: дві сторінки, 162 локальні посилання/ресурси, 16 FAQ; HTML nesting, унікальні ID, canonical, hreflang/sitemap, schema, поля форми, скрипти та футер пройшли перевірку.
- Зіставлення SHA-256 з початком цього завдання: глобальні стилі/JS, головні сторінки, robots, redirect і попередні матеріали Пельтьє/ND:YAG збережено; файлів не видалено.
- package.json/pyproject.toml і окремих команд lint/typecheck/build у проєкті немає; виконано штатні генератори та перевірки статичного сайту.

## Браузерні перевірки

Chrome/Playwright: PL/RU на 320, 375, 390, 768, 1024, 1440 px; шість пов’язаних сторінок на 320 px. 18 перевірок без overflow, пошкоджених зображень чи JavaScript pageerror. Вісім FAQ у кожній мові перевірено клавіатурою; без JS відповіді та контактний fallback доступні. CTA прокручує до форми, мовний перемикач і мобільне меню працюють.

Форма в обох мовах: required/consent, honeypot, перехоплена успішна відповідь, перехоплена HTTP-помилка, відновлення кнопки, serviceType/source/language та service_lead_submit перевірені. Реальних заявок: 0.

## Файли

Нові:

- `ru/uslugi/remont-blokov-pitaniya-i-elektroniki/index.html`
- `ru/uslugi/remont-blokov-pitaniya-i-elektroniki/index.md`
- `uslugi/naprawa-zasilaczy-i-elektroniki/index.html`
- `uslugi/naprawa-zasilaczy-i-elektroniki/index.md`
- `docs/power-supply-electronics-report.md`

Змінені в межах цього завдання (попередні незакомічені зміни не входять до списку):

- `_headers`
- `llms-full.txt`
- `llms.txt`
- `realizacje/naprawa-3000-nain-bloku-zasilania/index.html`
- `realizacje/naprawa-3000-nain-bloku-zasilania/index.md`
- `ru/realizacje/naprawa-3000-nain-bloku-zasilania/index.html`
- `ru/realizacje/naprawa-3000-nain-bloku-zasilania/index.md`
- `ru/uslugi/diagnostika-diodnyh-lazerov/index.html`
- `ru/uslugi/diagnostika-diodnyh-lazerov/index.md`
- `ru/uslugi/index.html`
- `ru/uslugi/index.md`
- `ru/uslugi/vosstanovlenie-golovok-i-manipul/index.html`
- `ru/uslugi/vosstanovlenie-golovok-i-manipul/index.md`
- `scripts/service-cases.json`
- `sitemap.xml`
- `uslugi/diagnostyka-laserow-diodowych/index.html`
- `uslugi/diagnostyka-laserow-diodowych/index.md`
- `uslugi/index.html`
- `uslugi/index.md`
- `uslugi/regeneracja-glowic-i-manipulatorow/index.html`
- `uslugi/regeneracja-glowic-i-manipulatorow/index.md`

Тимчасові результати, аудит і скриншоти: `/tmp/lts-electronics/`.

## Обмеження

Локальні перевірки не підтверджують доставку реальної заявки, роботу production-аналітики або production CWV. Публікація не виконувалася.

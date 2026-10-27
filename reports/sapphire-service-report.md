# Sapphire і «Лазери-динозаври» — звіт

Дата підготовки: 27.10.2026. Створено повноцінні версії реалізації та статті PL/RU/EN. За уточненням користувача до початкової PL-реалізації додано RU й EN. З мого боку commit, push і deploy не виконувалися. Публічні URL нижче підготовлені в репозиторії; їхня доступність на production не перевірена.

## Маршрути

| Матеріал | Локальний URL | Підготовлений публічний URL |
|---|---|---|
| Реалізація PL | http://127.0.0.1:8791/realizacje/serwis-lasera-sapphire-wymiana-plynu/ | https://lasertechservice.pl/realizacje/serwis-lasera-sapphire-wymiana-plynu/ |
| Реалізація RU | http://127.0.0.1:8791/ru/realizacje/servis-lasera-sapphire-zamena-zhidkosti/ | https://lasertechservice.pl/ru/realizacje/servis-lasera-sapphire-zamena-zhidkosti/ |
| Реалізація EN | http://127.0.0.1:8791/en/case-studies/sapphire-coolant-replacement-maintenance/ | https://lasertechservice.pl/en/case-studies/sapphire-coolant-replacement-maintenance/ |
| Блог PL | http://127.0.0.1:8791/blog/lasery-dinozaury-wiek-stan-techniczny/ | https://lasertechservice.pl/blog/lasery-dinozaury-wiek-stan-techniczny/ |
| Блог RU | http://127.0.0.1:8791/ru/blog/lazery-dinozavry-vozrast-tehnicheskoe-sostoyanie/ | https://lasertechservice.pl/ru/blog/lazery-dinozavry-vozrast-tehnicheskoe-sostoyanie/ |
| Блог EN | http://127.0.0.1:8791/en/blog/dinosaur-lasers-age-technical-condition/ | https://lasertechservice.pl/en/blog/dinosaur-lasers-age-technical-condition/ |

Реалізація та стаття мають взаємні PL/RU/EN/x-default. Перемикач кожної сторінки відкриває той самий матеріал іншою мовою. Картки додано першими в усі три каталоги реалізацій і блогу; кейси та статті посилаються один на одного відповідною мовою.

## Факти та контент

Реалізація містить тільки надані роботи: виїзд до клієнта, огляд і недостатній рівень рідини, видалення залишків, нова рідина, очищення, запуск і перевірка. Результат — апарат працює. Місто обслуговування — Легниця (Legnica), уточнене користувачем. Його додано в реалізацію, картку, Article JSON-LD та згадки у статтях PL/RU/EN. Не додано причин втрати рідини, заміни деталей, вимірювань потужності чи результатів процедур.

Дата 31.05.2018 перевірена на фото заводської таблички. Це не дата сервісу. Sapphire не названий 15-річним, небезпечним або неефективним. Призначення елемента на IMG_7601 не підтверджене, тому він названий елементом контуру, не фільтром.

У статті збережено критичний тон щодо зношеного обладнання без підтвердженого стану. Розмежовано паспортну довжину хвилі й вік, налаштування дисплея й фактичні вимірювання, догляд/ремонт/регенерацію, контрольований низький флюенс і випадкове падіння потужності. Усі польські ключові фрази використані в реалізації та статті. Фото Sapphire слугують ілюстрацією сервісу, а не доказом клінічної неефективності.

Посилання на первинні джерела розміщено біля відповідних тверджень у всіх трьох статтях:

- [Sony Semiconductor — деградація лазерних діодів](https://www.sony-semicon.com/files/62/Handbook_e_202004.pdf).
- [Newport — фізика лазерного діода та довжина хвилі](https://www.newport.com/n/laser-diode-physics).
- [Ophir — калібрування та умови вимірювань](https://www.ophiropt.com/a/calibration-procedure-and-traceability).
- [Halachmi і Lapidoth — дослідження низького флюенсу](https://pubmed.ncbi.nlm.nih.gov/22129205/).
- [Health Canada — охолодження й безпека](https://www.canada.ca/en/health-canada/services/environmental-workplace-health/reports-publications/radiation/laser-hair-removal-safety-guidelines-facility-owners-operators-health-canada-2011.html).
- [American Academy of Dermatology — чинники результату епіляції](https://www.aad.org/public/cosmetic/hair-removal/laser-hair-removal-faqs).

## Фото

Переглянуто всі 11 HEIC. Відібрано й конвертовано 9 фотографій у 27 WebP. Не використано IMG_7598 і IMG_7607 як близькі дублікати етапів доступу та перевірки. У реалізації — 9 унікальних фото, у кожній статті — 4 спільні компактні ілюстрації. Картки блогу текстові.

Збережено повний кадр і EXIF-орієнтацію. Корекція помірна: яскравість +2%, для двох загальних кадрів +6%; контраст +2%, різкість +6%. Баланс білого не змінено. Деталі не додавалися й не видалялися. AI, ретуш і збільшення вихідних фото не використовувалися. EXIF/XMP видалено.

Головне фото має варіанти 480×853, 768×1365, 1280×2276 px; решта — 480×853, 768×1365, 1152×2048 px. Галерея використовує існуючі компактні прев’ю й відкриває повний кадр. Фото статей мають висоту до 320 px і `object-fit: contain`. Додано локалізовані ALT, srcset/sizes, width/height, eager/high для першого фото та lazy для решти.

Папка: `img/realizacje/sapphire-serwis/`. У таблиці наведені базові назви; адаптивні файли мають суфікси `-480w` і `-768w`.

| Джерело | Базовий WebP | 480w KiB | 768w KiB | Основний KiB |
|---|---|---:|---:|---:|
| IMG_7595.heic | sapphire-serwis-lasera.webp | 42.1 | 86.3 | 195.9 |
| IMG_7596.heic | sapphire-tabliczka-znamionowa.webp | 24.1 | 70.5 | 168.0 |
| IMG_7597.heic | sapphire-demontaz-obudowy.webp | 43.4 | 91.2 | 180.2 |
| IMG_7599.heic | sapphire-wewnetrzne-podzespoly.webp | 82.4 | 176.9 | 355.7 |
| IMG_7600.heic | sapphire-uklad-chlodzenia.webp | 74.4 | 159.1 | 303.0 |
| IMG_7601.heic | sapphire-element-obiegu-chlodzenia.webp | 52.9 | 104.1 | 181.7 |
| IMG_7602.heic | sapphire-wymiana-plynu-chlodzacego.webp | 67.6 | 143.2 | 280.6 |
| IMG_7604.heic | sapphire-obsluga-ukladu-chlodzenia.webp | 91.8 | 193.1 | 366.0 |
| IMG_7606.heic | sapphire-kontrola-po-serwisie.webp | 59.9 | 141.3 | 293.2 |

Загалом **4,125,490 байтів (3.93 MiB)**. Точні розміри, оригінали й параметри корекції — у `image-audit.json`.

## Інтеграція та SEO

- Шість карток: PL/RU/EN-реалізації та PL/RU/EN-блог.
- Взаємні посилання між кейсом і статтею відповідною мовою PL/RU/EN. Посилання на діагностику, охолодження та заміну/калібрування діодів ведуть на відповідну мову.
- Унікальні title/description/H1, логічні H2, canonical без .html, OG/Twitter, Article/BlogPosting і BreadcrumbList. FAQ не створювався, FAQPage відсутній.
- `datePublished`/`dateModified` — 2026-10-27, дата підготовленого матеріалу, не ремонту. Перед пізнішою публікацією дату публікації слід узгодити з фактичним днем.
- Оновлено site-locales.json, sitemap.xml, ai-catalog.json, llms.txt, llms-full.txt, Markdown та _headers штатною збіркою.
- Джерелами контенту залишаються HTML і мовний реєстр. Нової архітектури генерації немає.
- Для Sapphire не змінено CSS/JS дизайну, header/footer, Lazar чи рекламні інтеграції. Шаблонні non-schema скрипти, зокрема GA4 G-6QFRWP5RX5 та Google Ads, звірені без змін.

## Перевірки

- `python3 scripts/build-site.py` — PASS: штатна збірка та загальні перевірки.
- `python3 scripts/check-sapphire.py` — PASS: три локалізовані кейси та статті, SEO, дата таблички, 27 файлів, шість карток, посилання та аналітика.
- `python3 scripts/check-b2b.py` і `build-service-menu.py --check` — PASS після додавання нових сторінок.
- `build-ai-search.py --check` та `build-ai-catalog.py --check` — актуальні результати.
- Загальні SEO/AI-перевірки — 216 canonical сторінок, 72 статті, 75 реалізацій; issues порожній.
- Pillow підтвердив розміри всіх WebP й відсутність EXIF/XMP.
- Chrome/Playwright (`scripts/check-sapphire.cjs`): шість сторінок × 320/375/390/768/1024/1440 px = 36 перевірок; без горизонтального скролу й JS-помилок.
- Фото завантажуються; галерея і Escape, мовний перемикач, Lazar, компактні зображення статей, переходи з шести карток — PASS. Кожен каталог містить одну картку Sapphire відповідною мовою.
- Мобільні знімки переглянуто. Дані браузерної перевірки: `/tmp/lts-sapphire/browser-results.json`, PNG в тій самій папці.
- Footer, основна навігація та всі non-schema скрипти нових сторінок збігаються з мовними еталонами.
- `git diff --check` — PASS.

Невиправлених помилок у проведених перевірках немає. Зовнішні запити браузерних тестів блокувалися. Live-деплой, індексація, реальна аналітика, доставка форм, Lighthouse/CWV та всі зовнішні посилання у production не перевірялися.

## Створені файли

- `ru/realizacje/servis-lasera-sapphire-zamena-zhidkosti/index.html`
- `ru/realizacje/servis-lasera-sapphire-zamena-zhidkosti/index.md`
- `en/case-studies/sapphire-coolant-replacement-maintenance/index.html`
- `en/case-studies/sapphire-coolant-replacement-maintenance/index.md`

- `blog/lasery-dinozaury-wiek-stan-techniczny/index.html`
- `blog/lasery-dinozaury-wiek-stan-techniczny/index.md`
- `en/blog/dinosaur-lasers-age-technical-condition/index.html`
- `en/blog/dinosaur-lasers-age-technical-condition/index.md`
- `img/realizacje/sapphire-serwis/image-audit.json`
- `img/realizacje/sapphire-serwis/sapphire-demontaz-obudowy-480w.webp`
- `img/realizacje/sapphire-serwis/sapphire-demontaz-obudowy-768w.webp`
- `img/realizacje/sapphire-serwis/sapphire-demontaz-obudowy.webp`
- `img/realizacje/sapphire-serwis/sapphire-element-obiegu-chlodzenia-480w.webp`
- `img/realizacje/sapphire-serwis/sapphire-element-obiegu-chlodzenia-768w.webp`
- `img/realizacje/sapphire-serwis/sapphire-element-obiegu-chlodzenia.webp`
- `img/realizacje/sapphire-serwis/sapphire-kontrola-po-serwisie-480w.webp`
- `img/realizacje/sapphire-serwis/sapphire-kontrola-po-serwisie-768w.webp`
- `img/realizacje/sapphire-serwis/sapphire-kontrola-po-serwisie.webp`
- `img/realizacje/sapphire-serwis/sapphire-obsluga-ukladu-chlodzenia-480w.webp`
- `img/realizacje/sapphire-serwis/sapphire-obsluga-ukladu-chlodzenia-768w.webp`
- `img/realizacje/sapphire-serwis/sapphire-obsluga-ukladu-chlodzenia.webp`
- `img/realizacje/sapphire-serwis/sapphire-serwis-lasera-480w.webp`
- `img/realizacje/sapphire-serwis/sapphire-serwis-lasera-768w.webp`
- `img/realizacje/sapphire-serwis/sapphire-serwis-lasera.webp`
- `img/realizacje/sapphire-serwis/sapphire-tabliczka-znamionowa-480w.webp`
- `img/realizacje/sapphire-serwis/sapphire-tabliczka-znamionowa-768w.webp`
- `img/realizacje/sapphire-serwis/sapphire-tabliczka-znamionowa.webp`
- `img/realizacje/sapphire-serwis/sapphire-uklad-chlodzenia-480w.webp`
- `img/realizacje/sapphire-serwis/sapphire-uklad-chlodzenia-768w.webp`
- `img/realizacje/sapphire-serwis/sapphire-uklad-chlodzenia.webp`
- `img/realizacje/sapphire-serwis/sapphire-wewnetrzne-podzespoly-480w.webp`
- `img/realizacje/sapphire-serwis/sapphire-wewnetrzne-podzespoly-768w.webp`
- `img/realizacje/sapphire-serwis/sapphire-wewnetrzne-podzespoly.webp`
- `img/realizacje/sapphire-serwis/sapphire-wymiana-plynu-chlodzacego-480w.webp`
- `img/realizacje/sapphire-serwis/sapphire-wymiana-plynu-chlodzacego-768w.webp`
- `img/realizacje/sapphire-serwis/sapphire-wymiana-plynu-chlodzacego.webp`
- `realizacje/serwis-lasera-sapphire-wymiana-plynu/index.html`
- `realizacje/serwis-lasera-sapphire-wymiana-plynu/index.md`
- `reports/sapphire-service-report.md`
- `ru/blog/lazery-dinozavry-vozrast-tehnicheskoe-sostoyanie/index.html`
- `ru/blog/lazery-dinozavry-vozrast-tehnicheskoe-sostoyanie/index.md`
- `scripts/check-sapphire.cjs`
- `scripts/check-sapphire.py`

## Змінені файли Sapphire

- `ru/realizacje/index.html`
- `ru/realizacje/index.md`
- `en/case-studies/index.html`
- `en/case-studies/index.md`

- `realizacje/index.html`
- `realizacje/index.md`
- `blog/index.html`
- `blog/index.md`
- `ru/blog/index.html`
- `ru/blog/index.md`
- `en/blog/index.html`
- `en/blog/index.md`
- `scripts/site-locales.json`
- `sitemap.xml`
- `ai-catalog.json`
- `llms.txt`
- `llms-full.txt`
- `_headers`

Окремо завершено B2B-перевірки: `scripts/check-b2b.cjs` (уточнено тест клавіатурного фокуса), новий `scripts/check-b2b.py` та `reports/b2b-service-report.md`. Ці файли належать попередньому незавершеному завданню, а не зміні дизайну Sapphire.

Рекомендована назва коміту Sapphire: `feat: add Sapphire service case and multilingual equipment-age guide`.

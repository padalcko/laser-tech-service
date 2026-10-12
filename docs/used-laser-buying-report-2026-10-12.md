# Стаття про купівлю вживаного лазера — 12 жовтня 2026

## Статус

Дві статті підготовлено локально та інтегровано в чинний блог. Commit, push і deploy не виконувалися. Production URL нижче — адреси після публікації, а не підтвердження розгортання.

Попередні локальні SEO/UI-зміни збережено. Порівняння з початковим знімком цього завдання підтвердило: 6 CSS-файлів, 3 JavaScript-файли та 232 файли зображень не змінені. Header, footer, соціальне меню, інтеграції та скрипти запозичені з відповідних мовних шаблонів. Footer і скрипти після main збігаються з шаблонами побайтово. Нова мовна навігація веде на нову відповідну статтю.

## URL та метадані

### PL

- URL: https://lasertechservice.pl/blog/jak-kupic-uzywany-laser-do-depilacji/
- Файл: `blog/jak-kupic-uzywany-laser-do-depilacji/index.html`
- Title: **Używany laser do depilacji – na co uważać przy zakupie?**
- Description: Planujesz zakup używanego lasera do depilacji? Sprawdź stan diody, historię serwisową i koszty napraw. Porady Laser Tech Service i oferty LTS Market.
- H1: Jak prawidłowo kupić używany laser kosmetyczny i nie stracić pieniędzy?
- Час читання: приблизно 11 хвилин, за оцінкою 200 слів/хв.

### RU

- URL: https://lasertechservice.pl/ru/blog/kak-kupit-bu-lazer-dlya-epilyacii/
- Файл: `ru/blog/kak-kupit-bu-lazer-dlya-epilyacii/index.html`
- Title: **Б/у лазер для эпиляции: что проверить перед покупкой?**
- Description: Покупаете б/у лазер в Польше? Узнайте, как проверить диод, охлаждение и историю ремонта, сравнить расходы и заказать диагностику в Laser Tech Service.
- H1: Как правильно купить б/у лазерный аппарат для салона красоты и не потерять деньги?
- Час читання: приблизно 11 хвилин, за оцінкою 200 слів/хв.

Польська основна частина містить близько 2166 слів, російська — 2176 (лічильник `.article-content`, без header/footer). Обидві версії мають 9 FAQ і перелік із 14 пунктів. Умовний приклад правильно дає 37 000 zł для б/у та 60 000 zł для нового з фінансуванням; числа чітко позначені як ілюстрація, а не пропозиція компаній.

Дату підготовки/оновлення `2026-10-12` відображено в HTML, `dateModified`, картках і sitemap. `datePublished` не вигадано: матеріал ще не опубліковано. Фактичну дату першої публікації слід встановити під час дозволеного релізу; за іншої дати переглянути також видиму дату.

## Структура, фотографії й картки

Використано чинні `article-page`, `article-content`, breadcrumbs, `article-faq`, `article-cta` і `article-cta__button--primary`. Останній клас забезпечує читабельний темний текст CTA на фірмовому золотому фоні. Нових глобальних стилів або компонентів не створено. Числовий приклад поданий списком, який читається на телефоні без широкої таблиці.

За останнім уточненням користувача обкладинки прибрано з обох нових карток; вони текстові, як решта блогу. Інші 17 карток кожної мови залишилися в тому самому порядку. Усі 36 карток мають приблизний час читання, узгоджений із поточним обсягом відповідної статті.

Використані реальні фото з уже задокументованих ремонтів, оглянуті перед повторним використанням:

| Фото | Файл у `img/realizacje/` | Розміри | Розміщення |
| --- | --- | --- | --- |
| Технік біля відкритого апарата у Вроцлаві | `wentylatory-wroclaw/technik-serwisu-laserowego-wroclaw.webp` | 941 × 1672 | Hero PL/RU |
| Діодний модуль після залиття в Познані | `wymiana-modulu-diodowego-poznan/uszkodzony-modul-diodowy-poznan.webp` | 1122 × 1402 | Контент PL/RU |

Обидва файли вже оптимізовані у WebP; повторно використано наявні варіанти `-480w.webp` та `-768w.webp`, перевірено фактичні розміри. Нових копій, перейменувань або видалень немає, тому таблиця перейменувань не потрібна. Наявні файли займають: фото техніка 101 000 байтів (варіанти 37 672 і 74 914), модуль 193 356 байтів (варіанти 53 916 і 113 814).

У статтях збережені природні пропорції та обмеження ширини 560 px. Hero має eager/fetchpriority high, контентне фото — lazy. Усі мають srcset, sizes, width/height, decoding async і окремі змістовні ALT PL/RU. Підписи не видають фото ремонту за виконаний передпродажний оптичний тест або конкретний товар каталогу.

## Внутрішні посилання

Крім спільної навігації, у нових статтях є такі контекстні цілі:

### PL

- `/`
- `/blog/`
- `/realizacje/wymiana-modulu-diodowego-lasera-po-zalaniu-poznan/`
- `/realizacje/wymiana-wentylatorow-chlodzenia-lasera-wroclaw/`
- `/blog/czyszczenie-ukladu-chlodzenia-lasera-wentylatory-przegrzanie/`
- `/blog/dlaczego-nie-warto-samodzielnie-wymieniac-uszczelek-w-laserze/`
- `/uslugi/`
- `/kontakt/`
- `/blog/uzywany-laser-diodowy-z-historia-serwisowa/`

### RU

- `/ru/`
- `/ru/blog/`
- `/ru/realizacje/wymiana-modulu-diodowego-lasera-po-zalaniu-poznan/`
- `/ru/realizacje/zamena-ventilyatorov-ohlazhdeniya-lazera-vrotslav/`
- `/ru/blog/ochistka-sistemy-ohlazhdeniya-lazera-ventilyatory-peregrev/`
- `/ru/blog/pochemu-ne-stoit-samostoyatelno-menyat-uplotneniya-v-lazere/`
- `/ru/uslugi/`
- `/ru/kontakt/`
- `/ru/blog/pochemu-vazhno-pokupat-lazer-s-istoriey-servisa/`

Зворотні посилання додано в PL/RU статті про обладнання з сервісною історією. На нові статті також ведуть перші картки індексів блогу. Основна частина PL посилається на PL, RU — на RU.

## LTS Market і редакційні джерела

Фактичний URL знайдено в репозиторії: **https://ltsmarket.pl/**. Прямий HTTP-запит підтвердив 200 і той самий кінцевий URL. Перевірка живої сторінки підтвердила розділи нових і вживаних апаратів та заявлену перевірку вживаних пристроїв Laser Tech Service. У статтях не наведено вигаданих умов фінансування або універсальної гарантії; обсяг сервісної історії та гарантій пропонується уточнювати для конкретного екземпляра.

Використані першоджерела для технічних, правових і фінансових пояснень; посилання розміщені біля відповідних тверджень у статтях:

- [Ophir — вибір датчика потужності/енергії](https://www.ophiropt.com/blog/choosing-the-right-laser-power-or-energy-sensor-easier-said-than-done/).
- [Newport — температурний контроль лазерних діодів](https://www.newport.com/g/laser-diode-temperature-controller-guide).
- [Європейська комісія — CE](https://single-market-economy.ec.europa.eu/single-market/goods/ce-marking_en).
- [EUR-Lex — спільні специфікації, додаток XVI](https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX%3A02022R2346-20230622). HTML-версія іноді показує антибот-перевірку; документ доступний також у PDF.
- [EFL — фінансування обладнання](https://efl.pl/pl/finansowanie-maszyn-i-urzadzen).
- [EFL — лізинг, позика й амортизація](https://media.efl.pl/informacje/kiedy-warto-wziac-leasing-a-kiedy-pozyczke).

## SEO, sitemap і AI Search

- Унікальні title/description/H1, self-canonical, взаємні pl/ru та x-default на PL.
- Open Graph і Twitter Cards із реальним hero-фото, його розмірами й локалізованим ALT.
- `BlogPosting` та `BreadcrumbList`, автор/видавець — наявний `#organization` Laser Tech Service.
- Видимий FAQ реалізовано нативним акордеоном, доступним без JavaScript. Нову `FAQPage`-розмітку не додано: [журнал Google Search Central](https://developers.google.com/search/updates) повідомляє про припинення FAQ rich results. Старі FAQ-схеми інших сторінок цим завданням не змінювались.
- Sitemap зріс із 86 до 88 HTML URL; додано рівно 2 нові адреси та їх мовні альтернативи.
- Штатний `build-ai-search.py` оновив нові Markdown, індекси, дві пов'язані старі статті, `llms.txt`, `llms-full.txt` і `_headers`.
- У sitemap немає Markdown URL. HTML залишається канонічним джерелом; прихований AI-контент не створювався.

## Перевірки

- `PYTHONPATH=/tmp/lts-oct12-tools python3 scripts/check-used-laser-buying.py` — passed: обсяг двох текстів, 18 FAQ, 28 пунктів списків, JSON-LD, canonical/hreflang, 4 розміщення responsive-фото, 36 карток і sitemap.
- `python3 scripts/check-ai-search.py` — passed: 89 HTML-файлів, 88 sitemap URL і Markdown, 9637 перевірок посилань, 221 JSON-LD блок, 880 перевірок правил доступу краулерів; issues порожній.
- `python3 scripts/check-geo-seo.py` — passed: 88 індексованих сторінок, 112 наявних розмічених FAQ, узгоджені NAP; issues порожній.
- `python3 scripts/build-ai-search.py --check` — 88 сторінок, stale порожній.
- `git diff --check` — passed.
- Chrome/Playwright: 6 сторінок × 6 ширин **320, 375, 390, 768, 1024, 1440 px** = 36 перевірок. Нові PL/RU, обидва індекси та дві старі статті зі зворотними посиланнями відповіли HTTP 200; горизонтального переповнення й JS-помилок не виявлено. Перевірено декодування фото, FAQ через Enter і мобільне меню нових сторінок.
- Дві нові статті додатково перевірено при вимкненому JavaScript на 320 px: H1 видимий, нативний FAQ відкривається.
- Після вибору коректного наявного класу CTA повторно перевірено кнопки обох сторінок на 6 ширинах (12 комбінацій): темний текст, відсутність підкреслення та виходу за межі контейнера. Знімки mobile/desktop і картки оглянуто візуально.
- Зовнішні запити під час локальних браузерних тестів блокувались, щоб не надсилати тестові події до production-аналітики. Її роботу ці тести не підтверджують.

Проєкт не має package.json або окремої збірки застосунку: виконано штатну генерацію AI-ресурсів та доступні актуальні загальні перевірки. Старі одноразові сценарії інших публікацій із припущеннями «ця картка перша» / «рівно +4 URL» не використовувалися як критерій цієї публікації; їхні раніше виявлені обмеження описані в `docs/geo-seo-audit-2026-10-12.md`.

## Межі та невирішені питання

- Потрібне окреме підтвердження користувача для commit/push/deploy. Наразі нові production URL, реальна індексація, Google Search Console та AI-цитування не перевірені.
- Фактична дата публікації ще невідома; використано правдиву дату підготовки/оновлення.
- На живому LTS Market сервісна адреса вказана як Rybacka 7, тоді як цей репозиторій LTS містить Piłsudskiego 74 lok. 320. Це може бути розмежування адрес майстерні та реєстрації; без підтвердження не змінювали NAP і не додавали адресу в новий текст. Розбіжність потребує окремого уточнення, якщо оновлювати контакти.
- Гарантія, повнота сервісної книжки, наявність вимірювального оснащення для конкретної моделі та умови фінансування визначаються індивідуально. Стаття прямо передає ці обмеження, не обіцяє універсальні вимірювання чи умови.

## Файли цього завдання

Нижче лише нові або змінені файли від початкового знімка цього завдання, без попередніх локальних правок:

- `_headers`
- `blog/index.html`
- `blog/index.md`
- `blog/jak-kupic-uzywany-laser-do-depilacji/index.html`
- `blog/jak-kupic-uzywany-laser-do-depilacji/index.md`
- `blog/uzywany-laser-diodowy-z-historia-serwisowa/index.html`
- `blog/uzywany-laser-diodowy-z-historia-serwisowa/index.md`
- `docs/used-laser-buying-report-2026-10-12.md`
- `llms-full.txt`
- `llms.txt`
- `ru/blog/index.html`
- `ru/blog/index.md`
- `ru/blog/kak-kupit-bu-lazer-dlya-epilyacii/index.html`
- `ru/blog/kak-kupit-bu-lazer-dlya-epilyacii/index.md`
- `ru/blog/pochemu-vazhno-pokupat-lazer-s-istoriey-servisa/index.html`
- `ru/blog/pochemu-vazhno-pokupat-lazer-s-istoriey-servisa/index.md`
- `scripts/check-used-laser-buying.py`
- `sitemap.xml`

Після видалення обкладинок повторно пройшли `check-used-laser-buying.py`, перевірка актуальності AI-ресурсів та `git diff --check`. Фото всередині статей залишено.

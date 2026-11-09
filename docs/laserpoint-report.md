# LaserPoint і Laser Magic — технічний звіт

Дата: 2026-11-09. Усі зміни локальні; commit, push і deploy не виконувалися.

## LaserPoint

Створено статтю PL/RU/EN у чинному шаблоні блогу. Користувач підтвердив описаний контроль усіх лазерів LTS Market та дату публікації 9 листопада 2026.

- PL: https://lasertechservice.pl/blog/pomiar-mocy-lasera-laserpoint/
- RU: https://lasertechservice.pl/ru/blog/izmerenie-moshchnosti-lazera-laserpoint/
- EN: https://lasertechservice.pl/en/blog/laser-power-measurement-laserpoint/

Це підготовлені маршрути, а не підтвердження їх наявності на production.

### Контент і структура

Усі абзаци, заголовки, порядок та технічні терміни автоматично порівняно з оригінальним вкладенням: PASS у трьох мовах. Контрольні копії: `content/laserpoint/{pl,ru,en}.md`. Видимий текст не переписувався. Модель, точність і діапазони LaserPoint не вигадувалися. Автор/publisher — Laser Tech Service за наявним шаблоном.

Додано природні посилання на LTS Market, відповідні мовні LUMOS, діагностику, техобслуговування та реалізації. Мовні URL LUMOS отримані з live hreflang сторінки RU; усі три сторінки завантажено успішно (PL/EN HTTP 200). Головний LTS Market залишається https://ltsmarket.pl/.

Header, footer, головне меню і соціальне меню відповідають чинним мовним шаблонам. CSS, JS, Lazar, аналітику, мобільну панель, інші статті та партнерів не змінено. Старі картки блогу і решта вмісту трьох індексів залишилися незмінними; додано одну текстову картку на початку кожного індексу.

### Фотографії

Використано три надані PNG. Без AI, ретуші, зміни дисплея чи обрізання. HEIC не використано: він не належить до трьох зазначених фотографій LaserPoint. Збережено пропорції 1199 × 1312, створено 320/480/768/1199 px WebP з якістю 85. Джерела, SHA-256, розміри й вага кожного варіанта — `img/blog/laserpoint/image-audit.json`.

Розміщення: відкритий кейс — перше фото після вступу та OG/Twitter; закритий кейс — перед поясненням LaserPoint; датчик і дисплей — перед розділом про 1200 W. Перший знімок eager/high, інші lazy; усі мають width/height, srcset, sizes і локалізований ALT.

| Основний WebP | Розмір | Вага, байти |
| --- | --- | ---: |
| `laserpoint-laser-power-measurement-case.webp` | 1199 × 1312 | 156262 |
| `laserpoint-professional-laser-measurement-kit.webp` | 1199 × 1312 | 288228 |
| `laserpoint-laser-measurement-sensor-display.webp` | 1199 × 1312 | 338632 |

### SEO та AI

- Self-canonical: PASS для всіх трьох сторінок.
- Взаємні hreflang pl-PL / ru-RU / en / x-default (PL): PASS; перемикач веде на ту саму статтю.
- Sitemap: додано три URL із відповідними alternates.
- Schema.org: BlogPosting та BreadcrumbList; дата 2026-11-09; JSON валідний; фальшивих рейтингів/FAQ немає.
- Open Graph / Twitter: локалізовані заголовки й описи, відкритий кейс, правильні URL/locale.
- robots.txt не змінено; сторінки index, follow. Відповіді HTTP 200 перевірено локально; live-публікацію та індексацію не перевіряли.
- Оновлено похідні Markdown, llms.txt, llms-full.txt, ai-catalog.json та відповідні записи _headers.

### Перевірки

- `python3 scripts/build-site.py`: PASS, exit 0 (включає маршрути, локалі, меню, SEO/GEO, AI, ціни та похідні ресурси).
- `check-site-locales.py`, `check-language-switcher.py`, `check-ai-search.py`, `check-ai-catalog.py`: PASS після додавання внутрішніх посилань.
- `git diff --check`: PASS.
- Lint/typecheck: окремих команд немає; проєкт статичний, package.json відсутній.
- Дослівність текстів, локальні посилання/зображення, JSON-LD, незмінність спільного оформлення та старих карток: PASS.
- Chrome: PL/RU/EN × 320/375/430/768/1024/1440 — 18 макетів. HTTP 200, один H1, три фотографії, мовні посилання, відкриття мобільного меню, відсутність горизонтального overflow і деформації зображень: PASS. Помилок JS і локальних HTTP ≥400 немає. Переглянуто скриншоти мобільного початку та desktop завершення статті.
- Зовнішні запити у браузерному QA блокувалися, щоб не надсилати аналітику; ці показники не є production Core Web Vitals.

| Мова | 320 | 375 | 430 | 768 | 1024 | 1440 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| PL | 0.0000 | 0.0000 | 0.0000 | 0.0077 | 0.2903 | 0.0008 |
| RU | 0.0000 | 0.0000 | 0.0000 | 0.0080 | 0.2813 | 0.0008 |
| EN | 0.0000 | 0.0000 | 0.0000 | 0.0005 | 0.0015 | 0.0008 |

CLS не нульовий на всіх ширинах: при 1024 px у PL зафіксовано 0,2903. Детальний повторний тест показав зміну висоти спільної навігації з 75 до 107 px; чинний шаблон Złota Firma дає ті самі 0,2903. Зміна header виходить за дозволений обсяг. Стверджувати повну відсутність CLS не можна.

## Laser Magic — додано після погодження нового візуалу

Після первинного звіту користувач замовив преміальний візуал на основі IMG_8582.heic та доручив додати партнера з ним. Попередня вимога використовувати виключно Instagram-фото змінена цими подальшими вказівками.

Laser Magic додано першою карткою (priority 100) у `/partnerzy/`, `/ru/partnerzy/`, `/en/partners/`. За подальшим проханням користувача опис PL/RU/EN скорочено до одного речення: Laser Magic — косметичний салон у Зеленій Гурі (відповідною мовою). Адреса, телефон та email збережені за чинним шаблоном. Уся картка веде на https://www.instagram.com/laser_magic_salon/ з target=_blank та rel=noopener noreferrer. Booksy/Facebook не додано.

Зображення: погоджений AI-макет із попереднього повідомлення, а не фотографія з Instagram. Файл `img/partnerzy/laser-magic-zielona-gora-partner.webp`, 1200 × 667, 84 804 байти. Пропорції збережені, object-fit: contain, lazy loading, явні width/height, локалізований ALT. На картці використано чинні розміри зображень без зміни CSS.

Перевірки: build-partners.py, check-partners.py, check-site-locales.py, check-ai-search.py та git diff --check — PASS. Оновлено похідні Markdown/LLM-ресурси. Chrome: 18 макетів PL/RU/EN × 320/375/430/768/1024/1440, усі зображення декодуються, немає overflow/обрізання тексту, 6 мовних переходів і Lazar open/close — PASS, без JS-помилок. Початковий тест під час resize спрацював раніше завершення адаптації меню; після додавання 250 ms очікування перевірки пройшли без зміни сайту.

Інші дев'ять карток та їхній взаємний порядок, HTML поза сіткою партнерів, header/footer, CSS/JS і аналітика збережені. Зміни цієї частини: scripts/partners.json, scripts/check-partners.py, scripts/check-partners.cjs; три HTML та три Markdown сторінок партнерів; llms-full.txt; новий WebP; цей звіт. Commit/push/deploy не виконувалися.

## Файли

Змінені існуючі файли:

- `_headers`
- `ai-catalog.json`
- `blog/index.html`
- `blog/index.md`
- `en/blog/index.html`
- `en/blog/index.md`
- `llms-full.txt`
- `llms.txt`
- `ru/blog/index.html`
- `ru/blog/index.md`
- `scripts/site-locales.json`
- `sitemap.xml`

Створені файли:

- `blog/pomiar-mocy-lasera-laserpoint/index.html`
- `blog/pomiar-mocy-lasera-laserpoint/index.md`
- `content/laserpoint/en.md`
- `content/laserpoint/pl.md`
- `content/laserpoint/routes.json`
- `content/laserpoint/ru.md`
- `en/blog/laser-power-measurement-laserpoint/index.html`
- `en/blog/laser-power-measurement-laserpoint/index.md`
- `img/blog/laserpoint/image-audit.json`
- `img/blog/laserpoint/laserpoint-laser-measurement-sensor-display-320w.webp`
- `img/blog/laserpoint/laserpoint-laser-measurement-sensor-display-480w.webp`
- `img/blog/laserpoint/laserpoint-laser-measurement-sensor-display-768w.webp`
- `img/blog/laserpoint/laserpoint-laser-measurement-sensor-display.webp`
- `img/blog/laserpoint/laserpoint-laser-power-measurement-case-320w.webp`
- `img/blog/laserpoint/laserpoint-laser-power-measurement-case-480w.webp`
- `img/blog/laserpoint/laserpoint-laser-power-measurement-case-768w.webp`
- `img/blog/laserpoint/laserpoint-laser-power-measurement-case.webp`
- `img/blog/laserpoint/laserpoint-professional-laser-measurement-kit-320w.webp`
- `img/blog/laserpoint/laserpoint-professional-laser-measurement-kit-480w.webp`
- `img/blog/laserpoint/laserpoint-professional-laser-measurement-kit-768w.webp`
- `img/blog/laserpoint/laserpoint-professional-laser-measurement-kit.webp`
- `ru/blog/izmerenie-moshchnosti-lazera-laserpoint/index.html`
- `ru/blog/izmerenie-moshchnosti-lazera-laserpoint/index.md`
- `docs/laserpoint-report.md` — цей звіт.

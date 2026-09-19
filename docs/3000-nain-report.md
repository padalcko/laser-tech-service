# 3000 NAIN — звіт про зміни

Дата: 19.09.2026. Зміни виконані локально, без commit і без публікації.

## Нові сторінки, URL та SEO-title

Кожний наведений маршрут реалізовано окремим `index.html`. Повний URL є self-canonical; адреси нижче описують підготовлені маршрути, а не підтверджують їхню публікацію.

| Сторінка | URL / canonical | Title |
|---|---|---|
| case PL | https://lasertechservice.pl/realizacje/naprawa-3000-nain-bloku-zasilania/ | Naprawa 3000 NAIN — blok zasilania | Laser Tech Service |
| case RU | https://lasertechservice.pl/ru/realizacje/naprawa-3000-nain-bloku-zasilania/ | Ремонт 3000 NAIN — блок питания | Laser Tech Service |
| blog PL | https://lasertechservice.pl/blog/3000-nain-laser-historia-konstrukcja-serwis/ | 3000 NAIN — laser starej szkoły i jego serwis | LTS |
| blog RU | https://lasertechservice.pl/ru/blog/3000-nain-lazer-istoriya-konstrukciya-servis/ | 3000 NAIN — лазер старой школы и его сервис | LTS |

## Файли

Створено:

- `realizacje/naprawa-3000-nain-bloku-zasilania/index.html`
- `ru/realizacje/naprawa-3000-nain-bloku-zasilania/index.html`
- `blog/3000-nain-laser-historia-konstrukcja-serwis/index.html`
- `ru/blog/3000-nain-lazer-istoriya-konstrukciya-servis/index.html`
- `img/realizacje/3000-nain/naprawa-3000-nain-laser-tech-service.webp`
- `img/realizacje/3000-nain/urzadzenie-3000-nain-przed-naprawa.webp`
- `img/realizacje/3000-nain/wnetrze-urzadzenia-3000-nain.webp`
- `img/realizacje/3000-nain/blok-zasilania-3000-nain.webp`
- `img/realizacje/3000-nain/panel-sterowania-3000-nain.webp`
- `img/realizacje/3000-nain/naprawa-elektroniki-3000-nain.webp`
- `img/realizacje/3000-nain/montaz-bloku-zasilania-3000-nain.webp`
- `img/realizacje/3000-nain/3000-nain-po-naprawie.webp`
- `img/realizacje/3000-nain/naprawa-3000-nain-laser-tech-service-karta.webp` — зменшена обкладинка для карток.
- `docs/3000-nain-report.md` — цей звіт.

Змінено:

- `realizacje/index.html`
- `ru/realizacje/index.html`
- `blog/index.html`
- `ru/blog/index.html`
- `sitemap.xml`

Усі 8 наданих фотографій використані в кожній мовній версії кейсу. У блозі — 4 вибрані фото та один ролик. Зображення конвертовані у WebP, довга сторона не перевищує 1600 px; окрема карткова версія — 640 px. Оригінали у Downloads не змінені. ALT локалізовані, зображення мають width/height; нижче першого екрана застосовано lazy loading.

Кожний індекс отримав одну нову картку на початку наявного grid. Старі картки перевірено на побайтову тотожність: Realizacje 10 → 11 для кожної мови, Blog 8 → 9. На головних сторінках немає окремого списку таких карток, тому їх редагувати не знадобилося.

## Мови, метадані та schema

- Для кожної пари сторінок задано взаємні `hreflang="pl"`, `hreflang="ru"`; `x-default` вказує на PL.
- Мовні перемикачі ведуть на відповідний матеріал іншою мовою. У шаблоні PL-блогу RU-перемикач вів на `/ru/`; на новій сторінці це виправлено.
- Кожна сторінка має унікальні title/description, self-canonical, Open Graph, Twitter metadata, Article і BreadcrumbList.
- Кейси містять по 5 VideoObject; статті — по 1 VideoObject. Дати uploadDate отримані зі сторінок YouTube, не вигадані.
- Дата публікації статей — 2026-09-19. Автор PL: Aleksandr Padalcko; RU: Александр Падалко. Підпис стоїть після фінального CTA, містить Raccoon SEO Studio з наявним у репозиторії посиланням https://raccoon-studio.com.ua/ та Wrocław / Вроцлав, 2026.
- Кожна стаття посилається на кейс своєї мови в кінці матеріалу; кейс — на статтю та відповідну сторінку послуг.
- Header, footer і неструктуровані глобальні scripts скопійовані з відповідних мовних шаблонів. Автоматичне порівняння підтвердило їхню тотожність, крім потрібних URL мовного перемикача. GA/GTM збережені.
- Глобальні CSS не змінювались. Для відео всередині блогу додано лише локальний клас `nain-article-video` з пропорцією 9:16 і максимальною шириною 420 px. У кейсах застосовано існуючі відеокласи та iframe-механізм.

## Відео: точне розміщення

В обох кейсах ролики розподілені між окремими етапами; порядок визначено за метаданими каналу Laser Tech Service, а не за порядком URL у завданні.

| ID | Розміщення в кейсі PL і RU | Додатково |
|---|---|---|
| `6-ACUofBwsA` | Після початкової діагностики | — |
| `RyLenhbBXGc` | Після демонтажу, як сервісні закулісся | Обидві статті, ближче до кінця |
| `AmVM_ZXMbdo` | Після ремонту електроніки блока живлення | — |
| `YU6aEnaRPmY` | Після повторного монтажу | — |
| `WEfLi9VhYCg` | Після запуску та перевірки | — |

Усі п’ять YouTube watch-сторінок повернули `playabilityStatus.status=OK` і `playableInEmbed=true`. Це підтвердження доступності з боку YouTube на момент перевірки, а не ручна перевірка відтворення у браузері.

Фактичні uploadDate:

- `6-ACUofBwsA`: `2026-09-19T02:33:10-07:00`
- `RyLenhbBXGc`: `2026-09-19T02:31:21-07:00`
- `AmVM_ZXMbdo`: `2026-09-19T02:28:45-07:00`
- `YU6aEnaRPmY`: `2026-09-19T02:27:14-07:00`
- `WEfLi9VhYCg`: `2026-09-19T02:25:39-07:00`

## Джерела research

1. [Власний корпоративний документ Shanghai Dingxin, стор. 27](https://qccdata.qichacha.com/ReportData/PDF/8af2bbd8cb15a533da2f42c161aec471.pdf): 3000NAIN у групі корейського імпорту та співпраця з UTI. PDF завантажено, релевантний текст знайдено пошуком.
2. [Презентація компанії Ugin на yes123](https://www.yes123.com.tw/wk_index/comp_info.asp?p_id=20090511181712_28925046): згадка корейської UTECH і отримання імпортного дозволу 3000NAIN у лютому 2010 року. Це хронологія дистриб’ютора, не встановлений рік початку виробництва.
3. [Картка, опублікована Utech Medical Equipment](https://b2bpakistan.com/12/health_medical-utech_medical_equipment_co_ltd-q_switch_nd_yag_laser_skin_care_machine-18447.html): Nd:YAG Q-Switched, 1064/532 nm, каталогові 105 kg, охолодження та шарнірне оптичне плече. Дані атрибутовані саме описаній версії, не вимірюванню наданого апарата. Поле країни продавця не використане як доказ країни виробництва.
4. [Пропозиція Rescience для UTI 3000NAIN](https://www.rescienceinc.com/product-page/uti-3000nain-dermatology-lasers): знайдена ціна пропозиції 3750 USD. У статті прямо вказано, що одна пропозиція не встановлює ринкової вартості або стану інших апаратів.
5. Власні фото та п’ять відео Laser Tech Service: спостереження за конструкцією та підтверджений користувачем обсяг ремонту.

Не вдалося надійно встановити: точну дату запуску/завершення виробництва, повну юридичну історію назв UTECH/UTI, рік виготовлення цього екземпляра, початкову ціну, ринкову частку/лідерство, актуальну програму постачання заводських запчастин. У текстах ці прогалини позначені; непідтверджені твердження не додані.

Місто цього ремонту, конкретні замінені деталі, первинна причина пошкодження і числові результати вимірювань не встановлені та не приписані кейсу. Згадка Вроцлава у підписі/контексті компанії не є локацією виконання цього ремонту.

## Результат аудиту

Пройдено:

- локальний HTTP 200 для всіх 4 нових сторінок;
- існування внутрішніх URL, images, CSS/scripts нових сторінок;
- один H1, правильний lang, унікальність нових title і description щодо всього репозиторію;
- self-canonical, взаємний hreflang, відповідність sitemap і мовних перемикачів;
- кількість, порядок, title та lazy loading iframe;
- валідний JSON усіх JSON-LD у репозиторії;
- валідний XML sitemap: 50 унікальних URL, 46 попередніх записів збережено, додано 4; усі URL відповідають локальним файлам;
- незмінність старих карток, header/footer і глобальних scripts;
- `git diff --check`.

Обмеження перевірки:

- Browser tool повернув `Browser is not available: iab`, список доступних браузерів порожній. Тому візуальний desktop/tablet/mobile QA, відсутність горизонтального overflow у реальному рендері, роботу мобільного меню та фактичне програвання iframe не підтверджено. Повторно використані наявні responsive CSS; окремий blog iframe обмежений шириною контейнера.
- Не виконувалась публікація. Production HTTP, індексація Google і надходження подій до GA/GTM не перевірялись.

Раніше наявні SEO-проблеми: `uploadDate: "YYYY-MM-DD"` у VideoObject на PL/RU сторінках `serwis-cavi-shape-advanced-wroclaw`, `serwis-hifu-kimed-k1-w1601-gorlitz`, `serwis-lasera-diodowego-wymiana-glowicy-wroclaw` (усього 6 файлів). Їх не змінено в межах додавання нового контенту; для виправлення потрібні фактичні дати відповідних старих відео. Нові VideoObject мають перевірені ISO-дати.

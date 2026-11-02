# Ремонт протікання маніпули — звіт

Дата публікації: 2026-11-02. Реалізація і технічна стаття, кожна PL/RU/EN. Зміни локальні; commit, push та deploy не виконувалися.

## Створені сторінки, URL та SEO

### PL — case-study

- URL: https://lasertechservice.pl/realizacje/naprawa-wycieku-chlodzenia-glowicy-klient-praga/
- Файли: `realizacje/naprawa-wycieku-chlodzenia-glowicy-klient-praga/index.html`, `realizacje/naprawa-wycieku-chlodzenia-glowicy-klient-praga/index.md`
- Title: Naprawa wycieku z głowicy — klient z Pragi | LTS
- Meta description: Klient z Pragi przywiózł aparat z wyciekiem. Wymieniliśmy przewody chłodzenia i osłonę, złożyliśmy głowicę i wykonaliśmy przegląd. Gwarancja 6 miesięcy.

### RU — case-study

- URL: https://lasertechservice.pl/ru/realizacje/remont-protechki-ohlazhdeniya-manipuly-klient-praga/
- Файли: `ru/realizacje/remont-protechki-ohlazhdeniya-manipuly-klient-praga/index.html`, `ru/realizacje/remont-protechki-ohlazhdeniya-manipuly-klient-praga/index.md`
- Title: Ремонт протечки манипулы — клиент из Праги | LTS
- Meta description: Клиент из Праги привёз аппарат с протечкой. Заменили трубки и гофру, собрали манипулу, провели обслуживание. Гарантия на работы 6 месяцев.

### EN — case-study

- URL: https://lasertechservice.pl/en/case-studies/handpiece-cooling-leak-repair-prague-customer/
- Файли: `en/case-studies/handpiece-cooling-leak-repair-prague-customer/index.html`, `en/case-studies/handpiece-cooling-leak-repair-prague-customer/index.md`
- Title: Handpiece Cooling Leak Repair — Prague Customer | LTS
- Meta description: A Prague customer brought a device with a coolant leak. We replaced tubes and the sleeve, reassembled the handpiece and serviced it. Six-month work warranty.

### PL — article

- URL: https://lasertechservice.pl/blog/dlaczego-przewody-chlodzenia-glowicy-przeciekaja/
- Файли: `blog/dlaczego-przewody-chlodzenia-glowicy-przeciekaja/index.html`, `blog/dlaczego-przewody-chlodzenia-glowicy-przeciekaja/index.md`
- Title: Dlaczego przewody chłodzenia głowicy przeciekają? | LTS
- Meta description: Dlaczego rurki chłodzenia tracą szczelność, kiedy wymienić osłonę i co zrobić przy wycieku? Wyjaśnienie na przykładzie naprawy dla klienta z Pragi.

### RU — article

- URL: https://lasertechservice.pl/ru/blog/pochemu-protekayut-trubki-ohlazhdeniya-manipuly/
- Файли: `ru/blog/pochemu-protekayut-trubki-ohlazhdeniya-manipuly/index.html`, `ru/blog/pochemu-protekayut-trubki-ohlazhdeniya-manipuly/index.md`
- Title: Почему протекают трубки охлаждения манипулы? | LTS
- Meta description: Почему стареют трубки охлаждения, достаточно ли заменить гофру и что делать при утечке? Объясняем на примере ремонта для клиента из Праги.

### EN — article

- URL: https://lasertechservice.pl/en/blog/why-handpiece-cooling-tubes-leak/
- Файли: `en/blog/why-handpiece-cooling-tubes-leak/index.html`, `en/blog/why-handpiece-cooling-tubes-leak/index.md`
- Title: Why Do Handpiece Cooling Tubes Leak? | LTS
- Meta description: Why cooling tubes deteriorate, why replacing the sleeve alone may not help, and what to do about a leak. A repair example from Laser Tech Service.

## Фото

10 фото реалізації в порядку показу; фото 3, 5, 6, 9, 10 також використані в блозі. Оригінали в Downloads не змінені. Для кожного створено версії шириною 480, 768 px та повнорозмірну без збільшення. Усі 30 файлів — WebP; ALT окремо PL/RU/EN. Нижче першого екрана застосовано lazy loading, усюди width/height, srcset/sizes.

1. `laser-kosmetyczny-panel-sterowania.webp` — Aparat z ekranem i przyciskiem awaryjnym.
2. `manipula-laserowa-obudowa-boczna.webp` — Boczna obudowa manipuły z przewodem.
3. `uszkodzona-oslona-przewodu-manipuly.webp` — Pęknięcia karbowanej osłony przewodu.
4. `otwarta-manipula-laserowa-modul-i-przewody.webp` — Otwarta manipuła z modułem i przewodami.
5. `wnetrze-manipuly-laserowej-modul-optyczny.webp` — Przezroczyste rurki i metalowy moduł wewnątrz manipuły.
6. `zlacze-manipuly-przewody-i-weze-chlodzenia.webp` — Złącze manipuły z kablami i rurkami chłodzenia.
7. `manipula-laserowa-oznaczenie-serwisowe.webp` — Zamknięta obudowa głowicy z oznaczeniem serwisowym.
8. `serwis-laserow-kontrola-polaczen-elektrycznych.webp` — Kontrola połączeń elektrycznych wewnątrz aparatu.
9. `wnetrze-lasera-zasilacz-i-okablowanie.webp` — Wnętrze aparatu z zasilaczem i okablowaniem.
10. `laser-kosmetyczny-uruchomiony-panel-dotykowy.webp` — Aparat z włączonym panelem dotykowym i manipułą.

Каталог: `img/realizacje/praga-wyciek-chlodzenia/`. `image-audit.json` містить усі 30 шляхів, розміри, вагу, ALT та SHA256 вихідних файлів. Загальна вага варіантів: 2059 KiB. Сторінка завантажує відповідний варіант, а не всі три.

## Інтеграція

- Нові картки першими в PL/RU/EN списках реалізацій і блогу; попередні картки збережені.
- `scripts/site-locales.json`: дві групи, шість локалізованих маршрутів.
- `sitemap.xml`: шість нових URL з alternate мовними посиланнями.
- Генератори оновили `ai-catalog.json`, `llms.txt`, `llms-full.txt`, `_headers`, шість Markdown списків та шість нових Markdown сторінок.
- Взаємні посилання реалізація ↔ блог, ремонт охолодження, відновлення маніпул, післягарантійне обслуговування, контакти, попередній ремонт E808.
- Header, footer, CSS, JS, навігація, форми, Lazar та головна сторінка не змінені.

## Перевірки

- `python3 scripts/build-site.py`: PASS; перевірки локалей, мовного перемикача, AI Search, GEO/SEO та цін. GEO/SEO: 240 сторінок, issues {}.
- `python3 scripts/check-handpiece-leak.py`: PASS — шість сторінок, 30 WebP, ALT/розміри, взаємні посилання, метадані, JSON-LD, спільні компоненти.
- `scripts/check-handpiece-leak.cjs`: PASS — усі шість сторінок на 320/375/430/768/1440 px; без горизонтального прокручування. 45 завантажень фото, діалоги галереї, 12 фактичних мовних переходів, Lazar відкриття/закриття, шість перших карток, без JS-помилок.
- Візуально переглянуто скриншоти PL реалізації 375 px та EN статті 1440 px.
- Canonical, hreflang, Open Graph, Twitter, Article/BlogPosting, BreadcrumbList, наявні дані організації перевірені локальними валідаторами. FAQPage не додавали.
- Три обов’язкові польські ключові фрази присутні в обох PL публікаціях.
- `build-ai-search.py --check`, `build-ai-catalog.py --check`, `check-ai-catalog.py`, `git diff --check`: результати фінального запуску перевірені перед передачею.

## Межі перевірки та фактичні зауваження

- На корпусі в кадрі видно позначення Intense Pulse Light. Точний тип випромінювача, бренд і модель не підтверджені. Збережено загальне формулювання «косметологічний лазер» з наданого тексту; не додано діодний тип, довжину хвилі чи характеристики. У блоці пристрою використано нейтральне «косметологічний апарат».
- Клієнт привіз обладнання із Праги до сервісу; виїзд майстра до Праги в нових матеріалах не заявлений. Географію ремонту не підмінено Прагою у schema.
- Старіння та згинання подані як можливі чинники, а не доведена конкретна причина. Гарантія 6 місяців відповідає завданню.
- ALT кадру з увімкненим екраном описує видимий стан, не видає саме фото за доказ результатів випробувань. Результат ремонту наведено за інформацією користувача.
- Браузерні тести локальні із заблокованими зовнішніми запитами. Роботу зовнішніх сервісів, Google Rich Results, production, PageSpeed та індексацію не перевіряли.
- Нові сторінки ще не опубліковані. Попереднє завдання мобільного LCP не входило в ці зміни; досягнення 2,5 с цим звітом не заявляється.

Додані валідатори: `scripts/check-handpiece-leak.py`, `scripts/check-handpiece-leak.cjs`.

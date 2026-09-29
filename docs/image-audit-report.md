# Фінальний аудит зображень — 2026-09-29

## Статус

Оптимізація та статичні перевірки завершені. OG/social image — PENDING вибору фотографії. Коміт не створено.

Базова точка BEFORE — HEAD до поточної оптимізації; AFTER включає всі responsive-версії та raster favicon/ICO. 1 MB = 1 000 000 байтів.

| Метрика | BEFORE | AFTER |
|---|---:|---:|
| Raster images | 105 | 113 |
| Bytes | 11680323 | 11468431 |
| MB | 11.680323 | 11.468431 |

Saved: 211892 bytes / 0.211892 MB / 1.81%.

- Форматних конвертацій: 0; фото вже були WebP.
- Зменшено 8 наявних зображень; додано 13 responsive-файлів. Під час фіналізації зображення більше не змінювалися.
- Видалено 5 невикористаних старих растрів, включно з парою точних дублікатів.
- Два одноразові CSV видалені з робочої директорії (вони не були tracked).
- Git diff проти HEAD: 47 modified, 5 deleted, 15 added/untracked.

## Sizes

Усі 27 наборів srcset уточнені без зміни CSS або структури HTML. Враховані container padding, grid gap, ширина рамок та media queries.

- Картки: до 650 px — viewport мінус 38 px; до 900 px — min(798 px, viewport мінус 50 px); 901–1200 px — (viewport мінус 110 px) / 3; далі 363.333 px.
- Фото laser: до 900 px приховане CSS, sizes = 0px; 901–1200 px — 45vw мінус 53.1 px; далі 486.9 px.
- Article images усередині article-content: до 650 px — viewport мінус 38 px; до 760 px — viewport мінус 50 px; до 1000 px — viewport мінус 42 px; далі 958 px.
- Article hero поза article-content: до 650 px — viewport мінус 38 px; до 1008 px — viewport мінус 50 px; далі 958 px.
- Width descriptors відповідають реальним розмірам файлів. DPR враховується браузером під час вибору кандидата. Високий DPR не може створити деталі, яких немає у вихідному файлі; джерела не upscale.

Розраховані видимі ширини (контент зображення, без рамки):

| Viewport | Картка | Laser | Article у article-content |
|---|---:|---:|---:|
| 375 | 337 | hidden | 337 |
| 768 | 718 | hidden | 726 |
| 1024 | 304.667 | 407.7 | 958 |
| 1440 | 363.333 | 486.9 | 958 |

## Width/height

Виправлено 15 попередніх невідповідностей intrinsic proportions. Установлені фактичні розміри джерел. CSS width/height, object-fit та aspect-ratio залишені без змін.

| HTML | Source | Було | Стало |
|---|---|---|---|
| `blog/dlaczego-warto-korzystac-z-profesjonalnego-serwisu/index.html` | `/img/blog/profesjonalny-serwis.webp` | 1200×800 | 900×1600 |
| `blog/serwis-glowicy-lasera-diodowego-szczelnosc-optyka/index.html` | `/img/blog/serwis-glowicy-lasera/nieszczelnosc-manipuly-lasera.webp` | 1600×1200 | 1920×1080 |
| `blog/serwis-glowicy-lasera-diodowego-szczelnosc-optyka/index.html` | `/img/blog/serwis-glowicy-lasera/uszkodzona-glowica-lasera.webp` | 1200×1600 | 900×1600 |
| `blog/serwis-glowicy-lasera-diodowego-szczelnosc-optyka/index.html` | `/img/blog/serwis-glowicy-lasera/wnetrze-glowicy-lasera.webp` | 1200×1600 | 900×1600 |
| `blog/serwis-glowicy-lasera-diodowego-szczelnosc-optyka/index.html` | `/img/blog/serwis-glowicy-lasera/zabrudzona-optyka-lasera.webp` | 1200×1600 | 900×1600 |
| `blog/serwis-glowicy-lasera-diodowego-szczelnosc-optyka/index.html` | `/img/blog/serwis-glowicy-lasera/modul-diodowy-lasera.webp` | 1200×1600 | 900×1600 |
| `blog/serwis-glowicy-lasera-diodowego-szczelnosc-optyka/index.html` | `/img/blog/serwis-glowicy-lasera/serwis-glowicy-lasera-na-miejscu.webp` | 1200×1600 | 900×1600 |
| `blog/serwis-glowicy-lasera-diodowego-szczelnosc-optyka/index.html` | `/img/blog/serwis-glowicy-lasera/uszkodzona-glowica-lasera.webp` | 1200×1600 | 900×1600 |
| `ru/blog/obsluzhivanie-manipuly-lazera-germetichnost-optika/index.html` | `/img/blog/serwis-glowicy-lasera/nieszczelnosc-manipuly-lasera.webp` | 1600×1200 | 1920×1080 |
| `ru/blog/obsluzhivanie-manipuly-lazera-germetichnost-optika/index.html` | `/img/blog/serwis-glowicy-lasera/uszkodzona-glowica-lasera.webp` | 1200×1600 | 900×1600 |
| `ru/blog/obsluzhivanie-manipuly-lazera-germetichnost-optika/index.html` | `/img/blog/serwis-glowicy-lasera/wnetrze-glowicy-lasera.webp` | 1200×1600 | 900×1600 |
| `ru/blog/obsluzhivanie-manipuly-lazera-germetichnost-optika/index.html` | `/img/blog/serwis-glowicy-lasera/zabrudzona-optyka-lasera.webp` | 1200×1600 | 900×1600 |
| `ru/blog/obsluzhivanie-manipuly-lazera-germetichnost-optika/index.html` | `/img/blog/serwis-glowicy-lasera/modul-diodowy-lasera.webp` | 1200×1600 | 900×1600 |
| `ru/blog/obsluzhivanie-manipuly-lazera-germetichnost-optika/index.html` | `/img/blog/serwis-glowicy-lasera/serwis-glowicy-lasera-na-miejscu.webp` | 1200×1600 | 900×1600 |
| `ru/blog/pochemu-stoit-polzovatsya-professionalnym-servisom/index.html` | `/img/blog/profesjonalny-serwis.webp` | 1200×800 | 900×1600 |

## Loading та fetchpriority

- Прибрано всі 23 додані високі пріоритети: article hero розташовані після заголовка/вступу; case hero на mobile розташовані після текстової колонки. Глобальний high без вимірювання LCP для них не виправданий.
- Попередні fetchpriority з HEAD не розширювалися. Preload фонового hero двох головних сторінок збережено.
- Hero не переведені в lazy. Немає поєднання high + lazy чи кількох high-priority великих ресурсів на одній сторінці.
- Lazy нижніх секцій збережено. Виявлені раніше eager defaults поза зміненим scope не переписувалися.

## OG/social — PENDING

У шести PL/RU сторінках home/contact/services OG і Twitter тимчасово використовують поточне фонове фото та мають явні HTML-коментарі PENDING. Це не затверджений фінальний social preview. LocalBusiness image також тимчасово збережено. Жодного посилання на нестворений asset немає. Окремий OG-файл не створено.

Кандидати після візуального перегляду наявних фото; усі crop виконуватимуться лише після затвердження:

1. `img/realizacje/multipolar-rf-lublin-1.webp`, 1920×1080 — ремонт електроніки апарата, інструменти й руки майстра. Crop x=0, y=36, w=1920, h=1008; resize до 1200×630 без upscale.
2. `img/blog/serwis-glowicy-lasera/nieszczelnosc-manipuly-lasera.webp`, 1920×1080 — виразний крупний план діагностики лазерної маніпули. Crop x=0, y=36, w=1920, h=1008; resize до 1200×630 без upscale.
3. `img/realizacje/3000-nain/wnetrze-urzadzenia-3000-nain.webp`, 1600×900 — реальний розібраний апарат із видимими вузлами. Crop x=0, y=30, w=1600, h=840; resize до 1200×630 без upscale.

## Redirects та developer utility

Новий непідтверджений image redirect прибрано. Файл `_redirects` байт-у-байт відповідає HEAD; усі попередні redirects збережені. Їхні цільові файли враховані як використані assets.

`scripts/audit-images.py` залишений як developer utility; додано лише коментар, що він не використовується runtime сайту. Потрібні Python 3 та Pillow. Логіка не змінена.

```sh
python3 scripts/audit-images.py
```

Utility та цей Markdown не потрібні runtime. Налаштування deployment не змінювалися; коментар не є механізмом виключення з publish-каталогу.

## Перевірки та межі

- Повторний аудит усіх 51 HTML, PL/RU home, blog, realizacje, kontakt, uslugi та 404: нуль broken local image references, неправильних width/height proportions і invalid srcset descriptors.
- Відсутні посилання на видалені assets; усі наявні растри мають посилання, включно з цілями legacy redirects.
- JSON-LD парситься; збережені schema-поля, крім раніше дозволених image URL. OG/Twitter залишаються явно pending.
- Порівняння HTML з HEAD виключає лише дозволені image attributes, image metadata URLs, preload і невидимі коментарі. Тексти, структура, header/footer, canonical, hreflang не змінені. CSS, JS, sitemap не змінені.
- `git diff --check` пройдено.
- Під час попереднього QA візуально порівняні всі 13 responsive-файлів та 8 зменшених растрів. Crop мініатюр відтворює наявний CSS; часткове відображення апаратів у картках було до оптимізації.
- Браузерний visual QA, LCP/CLS та фактичний currentSrc не виміряні через відсутність підключеного браузера. Sizes перевірені за CSS та розрахунком для mobile/tablet/desktop; це не браузерний замір. Production deployment не перевірявся.

## Змінені HTML

- `404.html`
- `blog/beauty-planet-3d-contour-mozliwosci-serwis/index.html`
- `blog/dlaczego-pala-sie-moduly-diodowe-w-laserach/index.html`
- `blog/dlaczego-warto-korzystac-z-profesjonalnego-serwisu/index.html`
- `blog/hifu-co-to-jest-jak-dziala-zastosowanie-serwis/index.html`
- `blog/planowy-przeglad-lasera-diodowego-dlaczego-to-wazne/index.html`
- `blog/serwis-glowicy-lasera-diodowego-szczelnosc-optyka/index.html`
- `index.html`
- `kontakt/index.html`
- `realizacje/index.html`
- `realizacje/naprawa-alma-accent-gorlitz/index.html`
- `realizacje/naprawa-beauty-planet-3d-contour-wroclaw/index.html`
- `realizacje/naprawa-multipolar-rf-lublin/index.html`
- `realizacje/naprawa-nubway-nbw-vsiii-wroclaw/index.html`
- `realizacje/serwis-cavi-shape-advanced-wroclaw/index.html`
- `realizacje/serwis-glowicy-lasera-diodowego-poznan/index.html`
- `realizacje/serwis-hifu-kimed-k1-w1601-gorlitz/index.html`
- `realizacje/serwis-lasera-diodowego-wymiana-glowicy-wroclaw/index.html`
- `realizacje/serwis-lasera-do-usuwania-tatuazu-wymiana-filtra/index.html`
- `ru/blog/beauty-planet-3d-contour-vozmozhnosti-servis/index.html`
- `ru/blog/hifu-chto-eto-kak-rabotaet-primenenie-servis/index.html`
- `ru/blog/obsluzhivanie-manipuly-lazera-germetichnost-optika/index.html`
- `ru/blog/planovoe-obsluzhivanie-diodnogo-lazera-pochemu-eto-vazhno/index.html`
- `ru/blog/pochemu-sgorayut-diodnye-moduli-v-lazerah/index.html`
- `ru/blog/pochemu-stoit-polzovatsya-professionalnym-servisom/index.html`
- `ru/index.html`
- `ru/kontakt/index.html`
- `ru/realizacje/index.html`
- `ru/realizacje/naprawa-alma-accent-gorlitz/index.html`
- `ru/realizacje/naprawa-beauty-planet-3d-contour-wroclaw/index.html`
- `ru/realizacje/naprawa-multipolar-rf-lublin/index.html`
- `ru/realizacje/naprawa-nubway-nbw-vsiii-wroclaw/index.html`
- `ru/realizacje/serwis-cavi-shape-advanced-wroclaw/index.html`
- `ru/realizacje/serwis-glowicy-lasera-diodowego-poznan/index.html`
- `ru/realizacje/serwis-hifu-kimed-k1-w1601-gorlitz/index.html`
- `ru/realizacje/serwis-lasera-diodowego-wymiana-glowicy-wroclaw/index.html`
- `ru/realizacje/serwis-lasera-do-usuwania-tatuazu-wymiana-filtra/index.html`
- `ru/uslugi/index.html`
- `uslugi/index.html`

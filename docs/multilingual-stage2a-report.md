# Stage 2A — Language Dropdown & EN Runtime Preparation

Дата завершення: 2026-10-22. Зміни локальні, поверх незакоміченого Stage 1. Commit, push і deploy не виконувалися.

## Результат

130 канонічних PL/RU сторінок отримали компактний dropdown у наявній темній/золотистій палітрі. Окремо оновлено компонент у `404.html`: він, як і раніше, веде на мовні головні сторінки, а не на вигадані переклади 404.

Закритий стан — PL ▾ / RU ▾. Відкритий — Polski та Русский; English зараз повністю виключений, оскільки EN planned. Джерело відповідників — `scripts/site-locales.json`, без окремих списків для кожної сторінки. `scripts/build-language-switcher.py` під час збірки замінює тільки один наявний div мовного компонента. Після узгодженої публікації EN HTML, статусу й SEO у Stage 2B наступна збірка додасть English відповідній групі автоматично. Статус published без HTML/сумісного sitemap не обходить перевірки Stage 1.

Компонент використовує нативні details/summary та звичайні посилання: працює без JavaScript. Є Enter, Space через нативний summary, Tab, ArrowUp/ArrowDown, Home/End, Escape з поверненням фокуса, закриття при кліку/переході фокуса поза компонентом. Escape усередині dropdown не закриває burger одночасно. Кнопка та кожне посилання мають ціль не менше 44×44 px. Прапорів немає.

## EN runtime

У всіх п'яти скриптах головне джерело мови — `document.documentElement.lang`. Значення нормалізується до основного коду: en-GB → en, ru-RU → ru. Підтримуються pl, ru, en; невідоме або порожнє значення явно повертається до pl. Для en/en-GB польського fallback немає.

- `js/main.js`: EN підписи burger, клавіатурна поведінка dropdown.
- `js/service-lead-form.js`: EN loading, success, error, submit, required/invalid та consent повідомлення. EN згода й submit отримують словниковий текст; решта HTML полів перекладатиметься в Stage 2B. PL/RU тексти та нативна валідація збережені. `language` у payload тепер походить з HTML lang, тому застарілий hidden input не підмінить EN на PL. Набір payload-полів, source, serviceType, problemDescription, webhook і подія service_lead_submit збережені. Нових полів немає.
- `js/lazar-ai.js`: ASK LAZAR, EN привітання, повідомлення, помилки, контакти; EN контакт `/en/contact/`, payload `language: "en"`. URL створюється лише в EN runtime — на поточних PL/RU сторінках такого посилання немає. Endpoint та створення/збереження session ID не змінювалися. Обробка контактного footer відповіді розширена для EN зі збереженням PL/RU варіантів.
- `js/cennik.js`: EN помилки введення та формат PLN en-GB. Ставка 1,40 PLN, формула і PL/RU форматування не змінені.
- `js/case-gallery.js`: Photo preview / Close × для діалогу фотографій; механіка відкриття/закриття збережена.

## Перевірки

Успішно:

- Повторні `build-site.py`; `build-language-switcher.py --check`, `build-ai-search.py --check`, `build-ai-catalog.py --check`, `build-service-cases.py --check`: стабільний результат, stale відсутні.
- `check-site-locales.py`, `check-language-switcher.py`, `check-ai-search.py`, `check-ai-catalog.py`, `check-geo-seo.py`: published/planned, мовні відповідники, metadata/schema, AI output. 130 канонічних сторінок, 130 Markdown; AI Catalog 15 послуг / 42 статті / 44 кейси, мови pl і ru.
- `check-language-runtime.cjs`: 47 груп. 42 перевірки PL/RU на 320/390/1440 px для home, service-detail, article, case-study, pricing, contact, partners; ще 5 runtime-сценаріїв pl/ru/en/en-GB/xx. Dropdown, реальний перехід на мовний відповідник, відсутність planned-посилань, цілі 44 px, Enter/стрілки/Home/End/Escape, зовнішній клік, burger, відсутність overflow та JS pageerror. Окремо перехід PL → RU без JavaScript.
- EN перевірявся лише підміною атрибута HTML lang у перехопленій відповіді локального браузера. EN HTML-файлів або маршрутів не створювали.
- Runtime-тести: правильні EN підписи/контакти, валідація, consent, form success/error, точний набір payload і serviceType; Lazar 500/invalid JSON/empty/network/success, правильна мова та незмінний session ID між повідомленнями; EN калькулятор і підписи фотодіалогу.
- Чинний `check-lazar-ai.cjs`: 18 груп та storage denial. PL/RU layout, retry/timeout/offline/помилки, payload, аналітичні події, відсутність витоку повідомлень у storage.
- `check-lightsheer-desire.py`, `check-cooling-maintenance.py`, `check-used-laser-buying.py` — PASS.
- `git diff --check` — PASS. Python cache відсутній.

Браузерні тести використовували локальний HTTP, блокування сторонніх запитів і mock webhook. Реальні заявки, повідомлення Лазарю та аналітичні запити не надсилалися. Production/Lighthouse/CWV не перевірялися.

П'ять історичних разових аудитів залишаються з раніше підтвердженими помилками Stage 1: `check-poznan.py` і `check-co2-poznan.py` очікують HEAD + 4 URL; `check-pharaon.py` і `check-gme.py` очікують свій кейс першим; `check-rsl-laser-maintenance.py` очікує старий список карток відносно HEAD. Поточний повторний запуск відтворив ці самі історичні умови. Це не результати PASS; ці аудити не входять до production build, і їхні умови не послаблювалися.

## Межі змін

Порівняння з початком Stage 2A довело: у всіх 131 HTML змінився виключно мовний div. Head, canonical, hreflang, JSON-LD, Open Graph, форми, footer, підключення скриптів і аналітики залишилися побайтово незмінними. Реєстр маршрутів, sitemap, robots, Markdown, llms, `_headers`, ai-catalog.json, ціни та бізнес-дані також незмінні. Нового каталогу en немає.

Stage 2A змінив 138 наявних файлів: 131 HTML, 5 JS, css/main.css та scripts/build-site.py. Зміни скриптів Stage 1 залишено на місці; вони не є додатковими змінами цього етапу.

## Скриншоти

Знімки локального Chrome з відкритим dropdown:

| Мова | Desktop | Mobile | Mobile вузький |
|---|---|---|---|
| PL | [1440 px](qa/stage2a/pl-1440.png) | [390 px](qa/stage2a/pl-390.png) | [320 px](qa/stage2a/pl-320.png) |
| RU | [1440 px](qa/stage2a/ru-1440.png) | [390 px](qa/stage2a/ru-390.png) | [320 px](qa/stage2a/ru-320.png) |

[Результати 47 браузерних груп](qa/stage2a/results.json). Знімки desktop PL, mobile PL 320 та RU 390 також перевірено візуально.

## Ризики та Stage 2B

Frontend готовий до Stage 2B. Перед публікацією потрібні реальні EN HTML, переклад статичних полів/підписів, published статус, reciprocal SEO і повторні тести. `/en/contact/` має бути опублікований до відкриття EN Лазаря користувачам. У поточному PL/RU інтерфейсі EN немає.

Backend n8n НЕ перевірено: серверний workflow/його конфігурація недоступні, експорт workflow у репозиторії не знайдено. За frontend неможливо встановити, чи потрібні серверні зміни. До Stage 2B потрібно перевірити дозволені значення language, prompt/мову відповіді Лазаря, fallback/помилки, обробку заявок і сповіщення. Якщо workflow містить тільки PL/RU гілки, їх слід розширити EN. Окремо потрібно підтвердити зміну мови в межах наявного session ID. Жодних змін серверу на цьому етапі не виконано.

Постійний контроль компонента додано до production build; перевірка опублікованих URL і SEO з Stage 1 залишається обов'язковою. Локальний успіх mock-тестів не підтверджує реальне отримання заявки чи відповідь EN backend.

## Створені файли Stage 2A

- `scripts/build-language-switcher.py`
- `scripts/check-language-switcher.py`
- `scripts/check-language-runtime.cjs`
- `docs/multilingual-stage2a-report.md`
- `docs/qa/stage2a/pl-1440.png`
- `docs/qa/stage2a/pl-390.png`
- `docs/qa/stage2a/pl-320.png`
- `docs/qa/stage2a/ru-1440.png`
- `docs/qa/stage2a/ru-390.png`
- `docs/qa/stage2a/ru-320.png`
- `docs/qa/stage2a/results.json`

## Повний перелік змінених наявних файлів Stage 2A

- `404.html`
- `blog/3000-nain-laser-historia-konstrukcja-serwis/index.html`
- `blog/5-oznak-wymiany-diody-w-laserze/index.html`
- `blog/beauty-planet-3d-contour-mozliwosci-serwis/index.html`
- `blog/czyszczenie-ukladu-chlodzenia-lasera-wentylatory-przegrzanie/index.html`
- `blog/dlaczego-maly-przewod-powoduje-duze-problemy/index.html`
- `blog/dlaczego-nie-warto-samodzielnie-wymieniac-uszczelek-w-laserze/index.html`
- `blog/dlaczego-pala-sie-moduly-diodowe-w-laserach/index.html`
- `blog/dlaczego-warto-korzystac-z-profesjonalnego-serwisu/index.html`
- `blog/hifu-co-to-jest-jak-dziala-zastosowanie-serwis/index.html`
- `blog/index.html`
- `blog/jak-kupic-uzywany-laser-do-depilacji/index.html`
- `blog/laser-co2-nie-reaguje-na-pedal-diagnostyka/index.html`
- `blog/laser-tech-service-zlota-firma-2026/index.html`
- `blog/lightsheer-desire-chlodzenie-niezawodnosc/index.html`
- `blog/modul-peltiera-chlodzenie-glowicy-lasera/index.html`
- `blog/pharaon-1470-historia-technologia-lasera/index.html`
- `blog/planowy-przeglad-lasera-diodowego-dlaczego-to-wazne/index.html`
- `blog/podlaczenie-glowic-przegrzewanie-kalibracja-nd-yag/index.html`
- `blog/serwis-glowicy-lasera-diodowego-szczelnosc-optyka/index.html`
- `blog/uszkodzony-przewod-manipulatora/index.html`
- `blog/uzywany-laser-diodowy-z-historia-serwisowa/index.html`
- `blog/wymiana-wody-w-laserze-do-depilacji/index.html`
- `css/main.css`
- `index.html`
- `js/case-gallery.js`
- `js/cennik.js`
- `js/lazar-ai.js`
- `js/main.js`
- `js/service-lead-form.js`
- `kontakt/index.html`
- `partnerzy/index.html`
- `realizacje/beauty-planet-3d-contour-naprawa-przewodu-wroclaw/index.html`
- `realizacje/index.html`
- `realizacje/naprawa-3000-nain-bloku-zasilania/index.html`
- `realizacje/naprawa-alma-accent-gorlitz/index.html`
- `realizacje/naprawa-beauty-planet-3d-contour-wroclaw/index.html`
- `realizacje/naprawa-lumenis-lightsheer-desire-olesnica/index.html`
- `realizacje/naprawa-multipolar-rf-lublin/index.html`
- `realizacje/naprawa-nubway-nbw-vsiii-wroclaw/index.html`
- `realizacje/naprawa-rsl-masaz-warszawa/index.html`
- `realizacje/pilna-naprawa-lasera-co2-poznan/index.html`
- `realizacje/przeglad-estelase-power-p808l/index.html`
- `realizacje/przeglad-serwis-pharaon-1470-wroclaw/index.html`
- `realizacje/przeglad-techniczny-lasera-do-depilacji/index.html`
- `realizacje/serwis-cavi-shape-advanced-wroclaw/index.html`
- `realizacje/serwis-glowicy-lasera-diodowego-poznan/index.html`
- `realizacje/serwis-gme-exsys-308/index.html`
- `realizacje/serwis-hifu-kimed-k1-w1601-gorlitz/index.html`
- `realizacje/serwis-lasera-diodowego-wymiana-glowicy-wroclaw/index.html`
- `realizacje/serwis-lasera-do-usuwania-tatuazu-wymiana-filtra/index.html`
- `realizacje/wymiana-modulu-diodowego-lasera-po-zalaniu-poznan/index.html`
- `realizacje/wymiana-modulu-peltiera-estetech-poznan/index.html`
- `realizacje/wymiana-peltiera-naprawa-lasera-nd-yag/index.html`
- `realizacje/wymiana-wentylatorow-chlodzenia-lasera-wroclaw/index.html`
- `ru/blog/3000-nain-lazer-istoriya-konstrukciya-servis/index.html`
- `ru/blog/5-priznakov-zameny-dioda-v-lazere/index.html`
- `ru/blog/beauty-planet-3d-contour-vozmozhnosti-servis/index.html`
- `ru/blog/co2-lazer-ne-reagiruet-na-pedal-diagnostika/index.html`
- `ru/blog/hifu-chto-eto-kak-rabotaet-primenenie-servis/index.html`
- `ru/blog/index.html`
- `ru/blog/kak-kupit-bu-lazer-dlya-epilyacii/index.html`
- `ru/blog/laser-tech-service-zlota-firma-2026/index.html`
- `ru/blog/lightsheer-desire-ohlazhdenie-nadezhnost/index.html`
- `ru/blog/modul-pelte-ohlazhdenie-manipuly-lazera/index.html`
- `ru/blog/obsluzhivanie-manipuly-lazera-germetichnost-optika/index.html`
- `ru/blog/ochistka-sistemy-ohlazhdeniya-lazera-ventilyatory-peregrev/index.html`
- `ru/blog/pharaon-1470-istoriya-lazernoy-tehnologii/index.html`
- `ru/blog/planovoe-obsluzhivanie-diodnogo-lazera-pochemu-eto-vazhno/index.html`
- `ru/blog/pochemu-malenkiy-kabel-sozdayot-bolshie-problemy/index.html`
- `ru/blog/pochemu-ne-stoit-samostoyatelno-menyat-uplotneniya-v-lazere/index.html`
- `ru/blog/pochemu-sgorayut-diodnye-moduli-v-lazerah/index.html`
- `ru/blog/pochemu-stoit-polzovatsya-professionalnym-servisom/index.html`
- `ru/blog/pochemu-vazhno-pokupat-lazer-s-istoriey-servisa/index.html`
- `ru/blog/podklyuchenie-manipul-peregrev-kalibrovka-nd-yag/index.html`
- `ru/blog/povrezhdennyj-kabel-manipuly/index.html`
- `ru/blog/zamena-vody-v-lazere-dlya-epilyacii/index.html`
- `ru/index.html`
- `ru/kontakt/index.html`
- `ru/partnerzy/index.html`
- `ru/realizacje/beauty-planet-3d-contour-naprawa-przewodu-wroclaw/index.html`
- `ru/realizacje/index.html`
- `ru/realizacje/naprawa-3000-nain-bloku-zasilania/index.html`
- `ru/realizacje/naprawa-alma-accent-gorlitz/index.html`
- `ru/realizacje/naprawa-beauty-planet-3d-contour-wroclaw/index.html`
- `ru/realizacje/naprawa-multipolar-rf-lublin/index.html`
- `ru/realizacje/naprawa-nubway-nbw-vsiii-wroclaw/index.html`
- `ru/realizacje/naprawa-rsl-masaz-warszawa/index.html`
- `ru/realizacje/pilna-naprawa-lasera-co2-poznan/index.html`
- `ru/realizacje/przeglad-estelase-power-p808l/index.html`
- `ru/realizacje/przeglad-serwis-pharaon-1470-wroclaw/index.html`
- `ru/realizacje/przeglad-techniczny-lasera-do-depilacji/index.html`
- `ru/realizacje/remont-lumenis-lightsheer-desire-olesnica/index.html`
- `ru/realizacje/serwis-cavi-shape-advanced-wroclaw/index.html`
- `ru/realizacje/serwis-glowicy-lasera-diodowego-poznan/index.html`
- `ru/realizacje/serwis-gme-exsys-308/index.html`
- `ru/realizacje/serwis-hifu-kimed-k1-w1601-gorlitz/index.html`
- `ru/realizacje/serwis-lasera-diodowego-wymiana-glowicy-wroclaw/index.html`
- `ru/realizacje/serwis-lasera-do-usuwania-tatuazu-wymiana-filtra/index.html`
- `ru/realizacje/wymiana-modulu-diodowego-lasera-po-zalaniu-poznan/index.html`
- `ru/realizacje/zamena-modulya-pelte-estetech-poznan/index.html`
- `ru/realizacje/zamena-pelte-remont-lazera-nd-yag/index.html`
- `ru/realizacje/zamena-ventilyatorov-ohlazhdeniya-lazera-vrotslav/index.html`
- `ru/uslugi/cennik/index.html`
- `ru/uslugi/diagnostika-diodnyh-lazerov/index.html`
- `ru/uslugi/index.html`
- `ru/uslugi/poslegarantiynoe-obsluzhivanie/index.html`
- `ru/uslugi/remont-blokov-pitaniya-i-elektroniki/index.html`
- `ru/uslugi/remont-oborudovaniya-lpg/index.html`
- `ru/uslugi/remont-oborudovaniya-rf/index.html`
- `ru/uslugi/remont-sensornyh-ekranov/index.html`
- `ru/uslugi/remont-sistem-ohlazhdeniya/index.html`
- `ru/uslugi/servis-ipl/index.html`
- `ru/uslugi/servis-lazerov-co2/index.html`
- `ru/uslugi/servis-lazerov-nd-yag/index.html`
- `ru/uslugi/servis-oborudovaniya-dlya-krioterapii/index.html`
- `ru/uslugi/servis-pikosekundnyh-lazerov/index.html`
- `ru/uslugi/tehnicheskoe-obsluzhivanie-oborudovaniya/index.html`
- `ru/uslugi/vosstanovlenie-golovok-i-manipul/index.html`
- `ru/uslugi/zamena-i-kalibrovka-lazernyh-diodov/index.html`
- `scripts/build-site.py`
- `uslugi/cennik/index.html`
- `uslugi/diagnostyka-laserow-diodowych/index.html`
- `uslugi/index.html`
- `uslugi/konserwacja-urzadzen-kosmetologicznych/index.html`
- `uslugi/naprawa-ekranow-dotykowych/index.html`
- `uslugi/naprawa-ukladow-chlodzenia/index.html`
- `uslugi/naprawa-urzadzen-lpg/index.html`
- `uslugi/naprawa-urzadzen-rf/index.html`
- `uslugi/naprawa-zasilaczy-i-elektroniki/index.html`
- `uslugi/regeneracja-glowic-i-manipulatorow/index.html`
- `uslugi/serwis-ipl/index.html`
- `uslugi/serwis-laserow-co2/index.html`
- `uslugi/serwis-laserow-nd-yag/index.html`
- `uslugi/serwis-laserow-pikosekundowych/index.html`
- `uslugi/serwis-pogwarancyjny/index.html`
- `uslugi/serwis-urzadzen-do-krioterapii/index.html`
- `uslugi/wymiana-i-kalibracja-diod-laserowych/index.html`

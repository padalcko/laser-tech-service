# B2B для салонів і мереж — звіт

Підготовлено 27.10.2026. Сторінки PL/RU/EN реалізовані та перевірені локально. З мого боку commit, push і deploy не виконувалися; live-публікацію не перевірено.

## URL

| Мова | Локальний URL | Підготовлений публічний URL |
|---|---|---|
| PL | http://127.0.0.1:8791/uslugi/serwis-dla-sieci-salonow/ | https://lasertechservice.pl/uslugi/serwis-dla-sieci-salonow/ |
| RU | http://127.0.0.1:8791/ru/uslugi/servis-dlya-setey-salonov/ | https://lasertechservice.pl/ru/uslugi/servis-dlya-setey-salonov/ |
| EN | http://127.0.0.1:8791/en/services/service-for-salon-chains/ | https://lasertechservice.pl/en/services/service-for-salon-chains/ |

## Реалізація

- Еталон: локалізовані посадкові післягарантійного сервісу. Використано наявні hero, breadcrumbs, картки, кроки, FAQ, форму, CTA і footer.
- Збережено надані H1, основний текст, шість переваг та CTA трьома мовами. Додано підтверджені напрямки обладнання, три кроки та шість FAQ.
- Умови: індивідуальні ціни за договором, оплата фактичних робіт, без абонплати, пакетів, мінімальних обсягів і автоматичних списань. Виїзди та їхня вартість — за окремим узгодженням, якщо інше не передбачено договором.
- Меню: новий пункт стоїть безпосередньо після прайсу в існуючому `#servicesSubmenu`. Desktop і mobile використовують цей самий компонент. `scripts/build-service-menu.py` бере маршрути з мовного реєстру, не змінює інші пункти, підтримує `--check` і викликається штатною збіркою. Первинно оновлено 211 меню; після додавання Sapphire перевірено 215 меню.
- На 208 наявних HTML-сторінках перед додаванням Sapphire підтверджено, що єдина зміна — новий пункт меню. Наявні footer, контент і аналітичні скрипти збережено.

## Форма

Використано чинний `js/service-lead-form.js` та чинний n8n endpoint `https://n8n.raccoon-studio.com.ua/webhook/lts-service-lead`. Нового бекенду немає.

| Поле інтерфейсу | Передача у чинному payload |
|---|---|
| Компанія | `salonName` |
| Контактна особа | `fullName` |
| Телефон або email | `phone`, як єдиний контактний рядок |
| Кількість салонів | Локалізований рядок у `problemDescription` |
| Типи обладнання | `deviceName` |
| Необов’язкове повідомлення | Додається до `problemDescription` |
| Тип / джерело | `b2b-service` / `pl-b2b-service`, `ru-b2b-service`, `en-b2b-service` |

Обов’язкові компанія, контактна особа, валідний телефон або email, кількість салонів і згода. Є honeypot, блокування повторного надсилання, timeout чинного механізму, локалізовані помилки й успіх лише після HTTP OK та JSON `success: true`. При помилці дані не стираються. EN-кнопка зберігає наданий B2B-текст.

B2B-логіка вмикається лише через `data-b2b-form`. Чинні форми зберігають попередній формат і подію `service_lead_submit`. Для B2B використано `b2b_cta_click` та `b2b_lead_submit`; остання спрацьовує лише після підтвердження. Персональні дані в аналітику не передаються.

Окремої сторінки політики конфіденційності в репозиторії не виявлено. Збережено точний чинний текст згоди з локалізованих форм, без вигаданого URL або нових юридичних умов. Реальну доставку заявки та інтерпретацію email у полі `phone` downstream-системою не перевірено: тестові запити перехоплювалися локально.

## SEO та дизайн

Унікальні title/description, один H1, canonical, взаємні PL/RU/EN/x-default, OG/Twitter, Service з чинним provider, BreadcrumbList, sitemap та мовний реєстр. AI Catalog містить один B2B-сервіс із трьома локалізаціями; Markdown, llms і Link-заголовки згенеровані штатними скриптами.

Видимий FAQ додано без FAQPage JSON-LD. Google припинив показ FAQ rich results; актуальність перевірена за [офіційним журналом змін Google Search](https://developers.google.com/search/updates#june-2026). Наявні FAQ інших сторінок не змінювалися.

Додано лише вузькі B2B-правила в `css/service-landing.css`: select оформлений як наявні поля, доступний focus, відступи прокручування до форми/полів. Палітра, шрифти, меню та глобальні компоненти не перероблені. Нових бібліотек і зображень немає; використано наявне оформлення шаблону. Lazar збережений, включно з чинним EN-обмеженням надсилання.

## Перевірки

- `scripts/check-b2b.py`: три сторінки, SEO, FAQ, поля, ключові фрази та інтеграції — PASS.
- `scripts/check-b2b.cjs`: 18 комбінацій PL/RU/EN × 320/375/390/768/1024/1440 px — PASS.
- Desktop/mobile меню, активний пункт, клавіатурний фокус, мовний перемикач, FAQ з клавіатури — PASS.
- Поля при прокручуванні до центру екрана доступні та не перекриті Lazar; горизонтального скролу немає.
- Форма: порожні поля, некоректний контакт, відсутня кількість, згода, honeypot, HTTP 500, `success:false`, невалідний JSON, мережева помилка — PASS.
- Відкладене підтвердження: успіх і подія не виникають раніше відповіді; повторний submit блокується — PASS.
- Email і телефон, необов’язкові поля, передача всіх даних, повернення тексту кнопки, події без PII — PASS.
- Регресія чинної форми післягарантійного сервісу PL/RU/EN — PASS.
- Без JavaScript: FAQ читаються, показаний контактний fallback форми — PASS.
- Штатна збірка, SEO/AI, меню `--check`, синтаксис JS, `git diff --check` — PASS.
- Мобільні знімки переглянуто. Докази: `/tmp/lts-b2b/browser-results.json`, PNG у тій самій папці.

Початковий тест фокуса уточнено: `:focus-visible` перевіряється після клавіатурної дії, а не після кліку мишею. Невиправлених помилок у проведених перевірках немає. Реальний n8n, аналітика, заявки, продакшн та Lighthouse/CWV не перевірялися.

## Файли

Створені:

- `uslugi/serwis-dla-sieci-salonow/index.html`
- `uslugi/serwis-dla-sieci-salonow/index.md`
- `ru/uslugi/servis-dlya-setey-salonov/index.html`
- `ru/uslugi/servis-dlya-setey-salonov/index.md`
- `en/services/service-for-salon-chains/index.html`
- `en/services/service-for-salon-chains/index.md`
- `scripts/build-service-menu.py`
- `scripts/check-b2b.py`
- `scripts/check-b2b.cjs`
- `reports/b2b-service-report.md`

Змінені джерела й службові файли: `js/service-lead-form.js`, `js/service-landing.js`, `css/service-landing.css`, `scripts/build-site.py`, `scripts/site-locales.json`, `sitemap.xml`, `_headers`, `ai-catalog.json`, `llms.txt`, `llms-full.txt`; HTML-файли нижче змінені лише для меню.

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
- `blog/laser-po-roku-przestoju-uklad-chlodzenia/index.html`
- `blog/laser-tech-service-zlota-firma-2026/index.html`
- `blog/lightsheer-desire-chlodzenie-niezawodnosc/index.html`
- `blog/modul-peltiera-chlodzenie-glowicy-lasera/index.html`
- `blog/pharaon-1470-historia-technologia-lasera/index.html`
- `blog/planowy-przeglad-lasera-diodowego-dlaczego-to-wazne/index.html`
- `blog/podlaczenie-glowic-przegrzewanie-kalibracja-nd-yag/index.html`
- `blog/serwis-glowicy-lasera-diodowego-szczelnosc-optyka/index.html`
- `blog/spalona-dioda-laserowa-naprawa-glowicy/index.html`
- `blog/uszkodzony-przewod-manipulatora/index.html`
- `blog/uzywany-laser-diodowy-z-historia-serwisowa/index.html`
- `blog/wymiana-wody-w-laserze-do-depilacji/index.html`
- `en/blog/3000-nain-laser-history-design-service/index.html`
- `en/blog/beauty-planet-3d-contour-features-service/index.html`
- `en/blog/burned-out-laser-diode-handpiece-repair/index.html`
- `en/blog/co2-laser-not-responding-to-foot-pedal/index.html`
- `en/blog/damaged-handpiece-cable/index.html`
- `en/blog/diode-laser-handpiece-seals-optics/index.html`
- `en/blog/five-signs-laser-diode-needs-inspection/index.html`
- `en/blog/hair-removal-laser-cooling-water-maintenance/index.html`
- `en/blog/handpiece-connections-overheating-nd-yag-calibration/index.html`
- `en/blog/hifu-technology-applications-service/index.html`
- `en/blog/how-to-buy-a-used-hair-removal-laser/index.html`
- `en/blog/index.html`
- `en/blog/laser-cooling-system-cleaning-overheating/index.html`
- `en/blog/laser-tech-service-zlota-firma-2026/index.html`
- `en/blog/laser-unused-for-a-year-cooling-system/index.html`
- `en/blog/lightsheer-desire-cooling-reliability/index.html`
- `en/blog/peltier-module-laser-handpiece-cooling/index.html`
- `en/blog/pharaon-1470-laser-history-technology/index.html`
- `en/blog/professional-aesthetic-equipment-service/index.html`
- `en/blog/risks-of-replacing-laser-seals-yourself/index.html`
- `en/blog/scheduled-diode-laser-maintenance/index.html`
- `en/blog/used-diode-laser-service-history/index.html`
- `en/blog/why-a-small-cable-causes-big-problems/index.html`
- `en/blog/why-laser-diode-modules-fail/index.html`
- `en/case-studies/3000-nain-power-supply-repair/index.html`
- `en/case-studies/alma-accent-cooling-hose-repair-gorlitz/index.html`
- `en/case-studies/beauty-planet-handpiece-cable-replacement-wroclaw/index.html`
- `en/case-studies/beauty-planet-vacuum-rf-repair-wroclaw/index.html`
- `en/case-studies/burned-out-laser-diode-replacement/index.html`
- `en/case-studies/cavi-shape-advanced-service-wroclaw/index.html`
- `en/case-studies/diode-laser-handpiece-replacement-wroclaw/index.html`
- `en/case-studies/diode-laser-handpiece-service-poznan/index.html`
- `en/case-studies/estelase-power-p808l-maintenance/index.html`
- `en/case-studies/estetech-peltier-module-replacement-poznan/index.html`
- `en/case-studies/flood-damaged-diode-module-replacement-poznan/index.html`
- `en/case-studies/gme-exsys-308-service-inspection/index.html`
- `en/case-studies/hair-removal-laser-maintenance/index.html`
- `en/case-studies/hifu-kimed-k1-w1601-service-gorlitz/index.html`
- `en/case-studies/index.html`
- `en/case-studies/laser-cooling-fan-replacement-wroclaw/index.html`
- `en/case-studies/lightsheer-desire-cooling-tubing-repair-wroclaw/index.html`
- `en/case-studies/lumenis-lightsheer-desire-cooling-repair-olesnica/index.html`
- `en/case-studies/multipolar-rf-repair-lublin/index.html`
- `en/case-studies/nd-yag-tattoo-removal-laser-filter-service/index.html`
- `en/case-studies/nubway-nbw-vsiii-repair-wroclaw/index.html`
- `en/case-studies/peltier-replacement-nd-yag-laser-repair/index.html`
- `en/case-studies/pharaon-1470-maintenance-wroclaw/index.html`
- `en/case-studies/rsl-massage-device-repair-warsaw/index.html`
- `en/case-studies/urgent-co2-laser-repair-poznan/index.html`
- `en/contact/index.html`
- `en/index.html`
- `en/partners/index.html`
- `en/pricing/index.html`
- `en/services/aesthetic-equipment-maintenance/index.html`
- `en/services/co2-laser-service/index.html`
- `en/services/cryotherapy-cryolipolysis-equipment-service/index.html`
- `en/services/diode-laser-diagnostics/index.html`
- `en/services/index.html`
- `en/services/ipl-equipment-service/index.html`
- `en/services/laser-cooling-system-repair/index.html`
- `en/services/laser-diode-replacement-calibration/index.html`
- `en/services/laser-handpiece-repair/index.html`
- `en/services/lpg-endermology-equipment-repair/index.html`
- `en/services/nd-yag-laser-service/index.html`
- `en/services/picosecond-laser-service/index.html`
- `en/services/post-warranty-equipment-service/index.html`
- `en/services/power-supply-electronics-repair/index.html`
- `en/services/rf-equipment-repair/index.html`
- `en/services/touchscreen-control-panel-repair/index.html`
- `index.html`
- `kontakt/index.html`
- `partnerzy/index.html`
- `realizacje/beauty-planet-3d-contour-naprawa-przewodu-wroclaw/index.html`
- `realizacje/index.html`
- `realizacje/naprawa-3000-nain-bloku-zasilania/index.html`
- `realizacje/naprawa-alma-accent-gorlitz/index.html`
- `realizacje/naprawa-beauty-planet-3d-contour-wroclaw/index.html`
- `realizacje/naprawa-chlodzenia-lightsheer-desire-wroclaw/index.html`
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
- `realizacje/wymiana-spalonej-diody-laserowej/index.html`
- `realizacje/wymiana-wentylatorow-chlodzenia-lasera-wroclaw/index.html`
- `ru/blog/3000-nain-lazer-istoriya-konstrukciya-servis/index.html`
- `ru/blog/5-priznakov-zameny-dioda-v-lazere/index.html`
- `ru/blog/beauty-planet-3d-contour-vozmozhnosti-servis/index.html`
- `ru/blog/co2-lazer-ne-reagiruet-na-pedal-diagnostika/index.html`
- `ru/blog/hifu-chto-eto-kak-rabotaet-primenenie-servis/index.html`
- `ru/blog/index.html`
- `ru/blog/kak-kupit-bu-lazer-dlya-epilyacii/index.html`
- `ru/blog/laser-tech-service-zlota-firma-2026/index.html`
- `ru/blog/lazer-posle-goda-prostoya-sistema-ohlazhdeniya/index.html`
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
- `ru/blog/sgorel-lazernyy-diod-remont-manipuly/index.html`
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
- `ru/realizacje/remont-ohlazhdeniya-lightsheer-desire-vrotslav/index.html`
- `ru/realizacje/serwis-cavi-shape-advanced-wroclaw/index.html`
- `ru/realizacje/serwis-glowicy-lasera-diodowego-poznan/index.html`
- `ru/realizacje/serwis-gme-exsys-308/index.html`
- `ru/realizacje/serwis-hifu-kimed-k1-w1601-gorlitz/index.html`
- `ru/realizacje/serwis-lasera-diodowego-wymiana-glowicy-wroclaw/index.html`
- `ru/realizacje/serwis-lasera-do-usuwania-tatuazu-wymiana-filtra/index.html`
- `ru/realizacje/wymiana-modulu-diodowego-lasera-po-zalaniu-poznan/index.html`
- `ru/realizacje/zamena-modulya-pelte-estetech-poznan/index.html`
- `ru/realizacje/zamena-pelte-remont-lazera-nd-yag/index.html`
- `ru/realizacje/zamena-sgorevshego-lazernogo-dioda/index.html`
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

## Рекомендована назва коміту

`feat: add multilingual B2B service pages for salon chains`

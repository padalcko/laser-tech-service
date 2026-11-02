# Pro Beauty Esen — додавання партнера

Додано через `scripts/partners.json`, priority 70. Порядок: Pro Beauty Esen, LTS Market, AnnVi, Magia Kosmetyczna, Cuprum Laser Tech, Cuprum Beauty Lab, LUMINE.

## Сторінки

- `/partnerzy/`
- `/ru/partnerzy/`
- `/en/partners/`

Назва в усіх мовах: **Pro Beauty Esen**.

| Мова | Короткий опис | Адреса |
|---|---|---|
| PL | Depilacja laserowa, manicure, pedicure oraz stylizacja brwi i rzęs. | Svatoplukova 42, Prostějov |
| RU | Лазерная эпиляция, маникюр, педикюр, оформление бровей и ресниц. | Svatoplukova 42, Prostějov |
| EN | Laser hair removal, manicures, pedicures, and brow and lash styling. | Svatoplukova 42, Prostějov |

Вся картка є одним доступним із клавіатури посиланням. Зайві рядки опису «Партнёр Laser Tech Service.» та «Посмотреть Instagram» прибрані в усіх мовах. Стандартний нижній бейдж збережений як в інших картках.

Посилання: https://www.instagram.com/pro_beauty.esen_/ — `target="_blank" rel="noopener noreferrer"`.

## Перевірка джерела

Після невдалої спроби браузера отримано публічний HTML Instagram прямим HTTP-запитом. `og:title` підтверджує laserová epilace/manikúra/pedicure/obočí/řasy/Prostejov; meta description містить 📍PROSTĚJOV Svatoplukova 42. Дані використані для короткого опису та адреси. Маркетингові числа й обіцянки з bio не переносилися.

Фото отримано з `og:image` цього ж профілю, завантажено з CDN Instagram та збережено локально як `img/partnerzy/pro-beauty-esen-instagram.webp`. Джерело 100×100 px; роздільність штучно не збільшувалася. ALT окремо PL/RU/EN. Це фото профілю, а не заявлений офіційний логотип. Placeholder більше не використовується.

## Змінені файли в межах цього завдання

- `scripts/partners.json`
- `partnerzy/index.html`, `ru/partnerzy/index.html`, `en/partners/index.html`
- `partnerzy/index.md`, `ru/partnerzy/index.md`, `en/partners/index.md`
- `llms-full.txt` — перегенеровані тексти трьох сторінок
- `scripts/check-partners.py`, `scripts/check-partners.cjs` — актуальна кількість/порядок та перевірка збереження карток
- `img/partnerzy/pro-beauty-esen-instagram.webp` — фото профілю
- `docs/pro-beauty-esen-report.md` — цей звіт

Попередні незакомічені зміни реалізації/статті про протікання маніпули збережені. Нових маршрутів немає; sitemap, canonical та hreflang не змінювалися в цьому завданні. CSS, header/footer, генератор карток та JS сайту не змінювалися.

## Перевірки

- `python3 scripts/check-partners.py`: PASS. Усі шість попередніх карток і HTML поза сіткою ідентичні базовій версії; JSON-LD читається; генератор актуальний; зміна пріоритету виявляється без запису.
- `scripts/check-partners.cjs`: PASS. 18 комбінацій мов/ширин: 320, 375, 430, 768, 1024, 1440 px. Немає горизонтального прокручування й обрізаного тексту; усі зображення декодуються. Ширини й стилі карток однакові, висота/рядки вирівняні в межах кожного ряду відповідно до чинного дизайну.
- Перша картка отримує фокус із клавіатури. Шість мовних переходів та відкриття/закриття Lazar працюють. JS-помилок немає.
- `build-ai-search.py --check`: 240 сторінок, stale []. `check-ai-search.py`: PASS. `git diff --check`: PASS.
- Візуально переглянуто RU 1440 px.

Браузерні тести локальні, зовнішні запити заблоковані. Не заявляється перевірка live-публікації чи індексації. Commit, push та deploy не виконувалися.

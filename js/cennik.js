/* Indicative billable distance. EN uses the rounded tariff generated at build time. */
(() => {
  const calculator = document.querySelector('[data-travel-calculator]');
  if (!calculator) return;
  const input = calculator.querySelector('#travel-km');
  const result = calculator.querySelector('#travel-result');
  const error = calculator.querySelector('#travel-error');
  // HTML lang is authoritative; normalize regional tags. Unknown/missing values use PL.
  const locale = document.documentElement.lang.trim().toLowerCase().split('-')[0];
  const language = ['pl', 'ru', 'en'].includes(locale) ? locale : 'pl';
  const text = {
    pl: ['Wpisz liczbę od 0 do 10 000 km, maksymalnie z dwoma miejscami po przecinku.', 'Sprawdź liczbę kilometrów.'],
    ru: ['Введите число от 0 до 10 000 км, не более двух знаков после запятой.', 'Проверьте количество километров.'],
    en: ['Enter a number from 0 to 10,000 km, with no more than two decimal places.', 'Check the number of kilometres.'],
  }[language];
  const currency = new Intl.NumberFormat(language === 'en' ? 'en-GB' : 'pl-PL', { style: 'currency', currency: language === 'en' ? 'EUR' : 'PLN' });
  function update() {
    const raw = input.value.trim();
    input.removeAttribute('aria-invalid');
    error.textContent = '';
    if (raw === '') { result.textContent = '—'; return; }
    const km = Number(raw.replace(',', '.'));
    if (!/^\d+(?:[.,]\d{1,2})?$/.test(raw) || !Number.isFinite(km) || km < 0 || km > 10000) {
      input.setAttribute('aria-invalid', 'true');
      error.textContent = text[0];
      result.textContent = text[1];
      return;
    }
    if (language === 'en') {
      // Parse decimal kilometres as integers: no floating-point money calculation.
      const [whole, fraction = ''] = raw.replace(',', '.').split('.');
      const hundredths = BigInt(whole) * 100n + BigInt(fraction.padEnd(2, '0'));
      const tariff = calculator.dataset.eurKm;
      if (!/^\d+$/.test(tariff || '')) { result.textContent = text[1]; return; }
      const euros = (hundredths * BigInt(tariff) + 99n) / 100n;
      result.textContent = currency.format(euros);
      return;
    }
    const grosz = Math.round(km * 140);
    result.textContent = currency.format(grosz / 100);
  }
  input.addEventListener('input', update);
  update();
})();

/* Demonstration only: agreed billable kilometres × 1.40 PLN. */
(() => {
  const calculator = document.querySelector('[data-travel-calculator]');
  if (!calculator) return;
  const input = calculator.querySelector('#travel-km');
  const result = calculator.querySelector('#travel-result');
  const error = calculator.querySelector('#travel-error');
  const ru = document.documentElement.lang === 'ru';
  const currency = new Intl.NumberFormat('pl-PL', { style: 'currency', currency: 'PLN' });
  function update() {
    const raw = input.value.trim();
    input.removeAttribute('aria-invalid');
    error.textContent = '';
    if (raw === '') { result.textContent = '—'; return; }
    const km = Number(raw.replace(',', '.'));
    if (!/^\d+(?:[.,]\d{1,2})?$/.test(raw) || !Number.isFinite(km) || km < 0 || km > 10000) {
      input.setAttribute('aria-invalid', 'true');
      error.textContent = ru
        ? 'Введите число от 0 до 10 000 км, не более двух знаков после запятой.'
        : 'Wpisz liczbę od 0 do 10 000 km, maksymalnie z dwoma miejscami po przecinku.';
      result.textContent = ru ? 'Проверьте количество километров.' : 'Sprawdź liczbę kilometrów.';
      return;
    }
    const grosz = Math.round(km * 140);
    result.textContent = currency.format(grosz / 100);
  }
  input.addEventListener('input', update);
  update();
})();

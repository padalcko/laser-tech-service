/* Local-only tools shared by the three maintenance articles. */
(() => {
  'use strict';
  const checklist = document.querySelector('.lts-maintenance-checklist');
  if (checklist) {
    const key = 'lts-maintenance-checklist-v1';
    const items = [...checklist.querySelectorAll('[data-maintenance-item]')];
    let storageAvailable = true;
    try {
      const saved = JSON.parse(localStorage.getItem(key) || '[]');
      if (Array.isArray(saved)) items.forEach(item => { item.checked = saved.includes(item.dataset.maintenanceItem); });
      localStorage.setItem(key, JSON.stringify(items.filter(item => item.checked).map(item => item.dataset.maintenanceItem)));
    } catch { storageAvailable = false; }
    const update = () => {
      const count = items.filter(item => item.checked).length;
      const percent = items.length ? Math.round(count / items.length * 100) : 0;
      checklist.querySelector('[data-check-progress]').textContent = `${checklist.dataset.done}: ${count}/${items.length} (${percent}%)${count === items.length ? '. ' + checklist.dataset.complete : ''}`;
      checklist.querySelector('progress').value = percent;
      checklist.querySelector('progress').textContent = `${percent}%`;
      checklist.querySelectorAll('.lts-maintenance-group').forEach(group => {
        const boxes = [...group.querySelectorAll('input[type="checkbox"]')];
        const output = group.querySelector('[data-group-progress]');
        output.hidden = false;
        output.textContent = `${checklist.dataset.done}: ${boxes.filter(box => box.checked).length}/${boxes.length}`;
      });
      checklist.querySelector('[data-storage-status]').textContent = storageAvailable ? checklist.dataset.saved : checklist.dataset.unavailable;
    };
    const save = () => {
      try {
        localStorage.setItem(key, JSON.stringify(items.filter(item => item.checked).map(item => item.dataset.maintenanceItem)));
        storageAvailable = true;
      } catch { storageAvailable = false; }
      update();
    };
    checklist.querySelector('[data-check-controls]').hidden = false;
    items.forEach(item => item.addEventListener('change', save));
    checklist.querySelector('[data-check-reset]').addEventListener('click', () => { items.forEach(item => { item.checked = false; }); save(); });
    checklist.querySelector('[data-check-print]').addEventListener('click', () => {
      document.body.classList.add('lts-maintenance-print');
      window.print();
      document.body.classList.remove('lts-maintenance-print');
    });
    window.addEventListener('afterprint', () => document.body.classList.remove('lts-maintenance-print'));
    update();
  }
  const calculator = document.querySelector('.lts-maintenance-calculator');
  if (calculator) {
    const fields = [...calculator.querySelectorAll('[data-calc-input]')];
    const range = calculator.querySelector('input[type="range"]');
    const days = fields.find(field => field.dataset.calcInput === 'days');
    const cost = Number(calculator.dataset.maintenanceCost);
    const currency = new Intl.NumberFormat(calculator.dataset.locale, {style: 'currency', currency: 'PLN'});
    const number = new Intl.NumberFormat(calculator.dataset.locale, {maximumFractionDigits: 2});
    const update = () => {
      let valid = true;
      fields.forEach(field => {
        const value = field.valueAsNumber;
        const ok = field.value.trim() !== '' && Number.isFinite(value) && field.validity.valid;
        field.setAttribute('aria-invalid', String(!ok));
        if (!ok) valid = false;
      });
      const results = calculator.querySelector('[data-calc-results]');
      results.hidden = !valid;
      calculator.querySelector('#maintenance-error').textContent = valid ? '' : calculator.dataset.error;
      calculator.querySelector('[data-days-value]').textContent = days.validity.valid && days.value !== '' ? days.value : '';
      if (!valid) return;
      range.value = days.value;
      const [treatments, price, downtime] = fields.map(field => field.valueAsNumber);
      const daily = treatments * Math.round(price * 100) / 100;
      const revenue = Math.round(daily * 100) * downtime / 100;
      const values = {daily: currency.format(daily), revenue: currency.format(revenue), cost: currency.format(cost), ratio: cost > 0 ? number.format(revenue / cost) + ' ×' : ''};
      for (const [key, value] of Object.entries(values)) calculator.querySelector(`[data-calc-result="${key}"]`).textContent = value;
      const scale = Math.max(revenue, cost, 1);
      calculator.querySelector('[data-bar="revenue"]').style.width = `${revenue / scale * 100}%`;
      calculator.querySelector('[data-bar="cost"]').style.width = `${cost / scale * 100}%`;
    };
    calculator.querySelector('[data-calc-controls]').hidden = false;
    fields.forEach(field => field.addEventListener('input', update));
    range.addEventListener('input', () => { days.value = range.value; update(); });
    calculator.querySelector('[data-calc-reset]').addEventListener('click', () => { fields.forEach(field => { field.value = field.defaultValue; }); update(); });
    update();
  }
})();

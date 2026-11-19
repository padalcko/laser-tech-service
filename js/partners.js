(() => {
  'use strict';
  const grid = document.querySelector('.partners-grid');
  const filters = document.querySelector('.partners-filters');
  const dialog = document.getElementById('partner-dialog');
  if (!grid || !filters || !dialog) return;
  const body = dialog.querySelector('.partner-dialog__body');
  let opener, scrollY, previousStyle;
  grid.addEventListener('click', event => {
    const button = event.target.closest('[data-partner]');
    if (!button) return;
    const template = document.getElementById(`partner-${button.dataset.partner}`);
    if (!template) return;
    opener = button;
    body.replaceChildren(template.content.cloneNode(true));
    body.querySelectorAll('img').forEach(img => { img.loading = 'eager'; });
    body.querySelectorAll('[data-map-address]').forEach(link => {
      link.href = `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(link.dataset.mapAddress)}`;
    });
    scrollY = window.scrollY;
    previousStyle = document.body.getAttribute('style');
    Object.assign(document.body.style, { position: 'fixed', top: `-${scrollY}px`, width: '100%', overflow: 'hidden' });
    dialog.showModal();
    dialog.scrollTop = 0;
  });
  filters.addEventListener('click', event => {
    const button = event.target.closest('[data-filter]');
    if (!button) return;
    filters.querySelectorAll('button').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    grid.querySelectorAll('.partner-card').forEach(card => {
      card.hidden = button.dataset.filter !== 'all' && card.dataset.category !== button.dataset.filter;
    });
  });
  dialog.querySelector('.partner-dialog__close').addEventListener('click', () => dialog.close());
  let backdropDown = false;
  const outside = event => {
    const rect = dialog.getBoundingClientRect();
    return event.target === dialog && (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom);
  };
  dialog.addEventListener('pointerdown', event => { backdropDown = outside(event); });
  dialog.addEventListener('click', event => { if (backdropDown && outside(event)) dialog.close(); });
  dialog.addEventListener('close', () => {
    if (previousStyle === null) document.body.removeAttribute('style');
    else document.body.setAttribute('style', previousStyle);
    window.scrollTo({ top: scrollY, behavior: 'instant' });
    opener?.focus({ preventScroll: true });
  });
})();

(() => {
  const gallery = document.querySelector('main');
  if (!gallery || typeof HTMLDialogElement === 'undefined') return;
  const ru = document.documentElement.lang === 'ru';
  const dialog = document.createElement('dialog');
  dialog.className = 'case-photo-dialog';
  dialog.setAttribute('aria-label', ru ? 'Просмотр фотографии' : 'Podgląd zdjęcia');
  const close = document.createElement('button');
  close.type = 'button';
  close.textContent = ru ? 'Закрыть ×' : 'Zamknij ×';
  const image = document.createElement('img');
  const caption = document.createElement('p');
  dialog.append(close, image, caption);
  document.body.append(dialog);
  let previousOverflow;
  gallery.addEventListener('click', event => {
    const link = event.target.closest('.case-gallery--compact a, .case-photo--compact a');
    if (!link || event.button !== 0 || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    image.src = link.href;
    image.alt = link.querySelector('img').alt;
    caption.textContent = image.alt;
    previousOverflow = document.body.style.overflow;
    dialog.showModal();
    document.body.style.overflow = 'hidden';
  });
  close.addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => {
    const rect = dialog.getBoundingClientRect();
    if (event.target === dialog && (event.clientX < rect.left || event.clientX > rect.right || event.clientY < rect.top || event.clientY > rect.bottom)) dialog.close();
  });
  dialog.addEventListener('close', () => { document.body.style.overflow = previousOverflow; });
})();

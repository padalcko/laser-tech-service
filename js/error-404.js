/* Single-document error localization. Never navigate or persist a language override. */
(() => {
  'use strict';
  const data = JSON.parse(document.getElementById('error-locales').textContent);
  const normalize = value => value.replace(/\s+/g, ' ').trim();
  const texts = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  while (walker.nextNode()) {
    const node = walker.currentNode;
    if (node.parentElement.closest('script, style, .language-switcher')) continue;
    const key = normalize(node.nodeValue);
    if (Object.hasOwn(data.text.pl, key)) texts.push([node, key]);
  }
  const attributes = [];
  document.querySelectorAll('[aria-label], [title], [alt]').forEach(node => {
    if (node.closest('.language-switcher')) return;
    ['aria-label', 'title', 'alt'].forEach(attr => {
      const key = node.getAttribute(attr);
      if (Object.hasOwn(data.text.pl, key)) attributes.push([node, attr, key]);
    });
  });
  const links = [...document.querySelectorAll('a[href^="/"]')].map(node => [node, node.getAttribute('href')]);
  const switcher = document.querySelector('.language-switcher');
  const toggle = document.querySelector('.nav-toggle');
  const menuLabels = {pl: ['Otwórz menu', 'Zamknij menu'], ru: ['Открыть меню', 'Закрыть меню'], en: ['Open menu', 'Close menu']};
  const syncMenuLabel = () => toggle.setAttribute('aria-label', menuLabels[document.documentElement.lang][toggle.getAttribute('aria-expanded') === 'true' ? 1 : 0]);
  new MutationObserver(syncMenuLabel).observe(toggle, {attributes: true, attributeFilter: ['aria-expanded']});
  const descriptions = {
    pl: 'Nie znaleźliśmy tej strony. Wróć na stronę główną Laser Tech Service, sprawdź nasze usługi, realizacje, blog lub skontaktuj się z serwisem.',
    ru: 'Страница не найдена. Вернитесь на главную Laser Tech Service, посмотрите наши услуги, работы и блог или свяжитесь с сервисом.',
    en: 'Page not found. Return to the Laser Tech Service homepage, explore our services, case studies and blog, or contact our team.'
  };
  function apply(language) {
    document.documentElement.lang = language;
    document.body.classList.remove('pl', 'ru', 'en');
    document.body.classList.add(language);
    texts.forEach(([node, key]) => { node.nodeValue = ' ' + data.text[language][key] + ' '; });
    attributes.forEach(([node, attr, key]) => node.setAttribute(attr, data.text[language][key]));
    links.forEach(([node, href]) => node.setAttribute('href', data.routes[language][href] || href));
    document.title = data.text[language]['Błąd 404'] + ' | Laser Tech Service';
    document.querySelector('meta[name="description"]').content = descriptions[language];
    const label = data.text[language]['Wybór języka'];
    switcher.setAttribute('aria-label', label);
    switcher.querySelector('summary > span').textContent = language.toUpperCase();
    switcher.querySelectorAll('a').forEach(link => {
      const active = link.lang === language;
      link.classList.toggle('language-switcher__link--active', active);
      if (active) { link.setAttribute('aria-current', 'page'); switcher.querySelector('summary').setAttribute('aria-label', label + ': ' + link.textContent); }
      else link.removeAttribute('aria-current');
    });
    syncMenuLabel();
    document.dispatchEvent(new Event('error-language-change'));
  }
  switcher.addEventListener('click', event => {
    const link = event.target.closest('a[lang]');
    if (!link) return;
    event.preventDefault();
    apply(link.lang);
  });
  // Keep the approved fixed position; yield space to important page controls.
  let collisionFrame;
  function scheduleCollisionCheck() {
    cancelAnimationFrame(collisionFrame);
    collisionFrame = requestAnimationFrame(() => {
      const launcher = document.querySelector('.lazar-launcher');
      if (!launcher || launcher.hidden) return;
      const box = launcher.getBoundingClientRect();
      const blocked = [...document.querySelectorAll('.error-btn, .error-link-card, .footer__contact-list, #siteNav a, #siteNav button, #siteNav summary')].some(node => {
        const rect = node.getBoundingClientRect();
        return rect.width && rect.height && rect.left < box.right + 6 && rect.right > box.left - 6 && rect.top < box.bottom + 6 && rect.bottom > box.top - 6;
      });
      launcher.style.visibility = blocked ? 'hidden' : '';
    });
  }
  window.addEventListener('scroll', scheduleCollisionCheck, {passive: true});
  window.addEventListener('resize', scheduleCollisionCheck);
  window.addEventListener('load', scheduleCollisionCheck);
  document.addEventListener('click', scheduleCollisionCheck);
  document.addEventListener('keydown', scheduleCollisionCheck);
  document.addEventListener('error-language-change', scheduleCollisionCheck);
  new MutationObserver(scheduleCollisionCheck).observe(document.body, {childList: true, subtree: true});
  new MutationObserver(scheduleCollisionCheck).observe(document.getElementById('siteNav'), {attributes: true, subtree: true, attributeFilter: ['class', 'hidden', 'aria-expanded']});
  document.fonts?.ready.then(scheduleCollisionCheck);
  apply(/^\/(ru|en)(?:\/|$)/.exec(location.pathname)?.[1] || 'pl');
})();

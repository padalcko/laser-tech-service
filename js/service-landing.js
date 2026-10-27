/* Landing interactions use the installed gtag function; never send form values. */
document.addEventListener('DOMContentLoaded', () => {
  const landing = document.querySelector('.service-landing');
  if (!landing) return;
  const serviceType = landing.querySelector('input[name="serviceType"]')?.value;
  if (!serviceType) return;
  document.addEventListener('click', (event) => {
    const link = event.target.closest('a');
    if (!link || typeof window.gtag !== 'function') return;
    const name = link.hasAttribute('data-service-cta') ? (serviceType === 'b2b-service' ? 'b2b_cta_click' : 'service_cta_click')
      : link.getAttribute('href')?.startsWith('tel:') ? 'service_phone_click' : null;
    if (name) window.gtag('event', name, {
      service_type: serviceType,
      language: document.documentElement.lang,
      source: 'service_landing',
    });
  });
});

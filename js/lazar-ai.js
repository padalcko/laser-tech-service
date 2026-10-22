/* Lazar AI: one shared PL/RU/EN client. No conversation content is persisted or logged. */
(() => {
  'use strict';
  if (document.getElementById('lazar-root')) return;
  const config = Object.freeze({
    endpoint: 'https://n8n.raccoon-studio.com.ua/webhook/lazar-ai-chat',
    timeoutMs: 28000,
    maxMessageLength: 2000,
  });
  // HTML lang is authoritative; normalize regional tags. Unknown/missing values use PL.
  const locale = document.documentElement.lang.trim().toLowerCase().split('-')[0];
  const language = ['pl', 'ru', 'en'].includes(locale) ? locale : 'pl';
  // EN backend has not been approved. Keep the public chat hidden until explicitly released.
  if (language === 'en' && document.documentElement.dataset.lazarEnabled !== 'true') return;
  const translations = {
    en: {
      open: 'ASK LAZAR', close: 'Close chat', status: 'AI technical assistant',
      greeting: 'Hello! I am Lazar, the AI technical assistant at Laser Tech Service. Describe the problem with your equipment and I will help you identify possible causes and next steps.',
      placeholder: 'Describe the problem…', input: 'Message to Lazar', send: 'Send', retry: 'Try again',
      call: 'Call us', form: 'Send a service request', log: 'Conversation with Lazar', user: 'You', waiting: 'Lazar is preparing a reply…',
      unavailable: 'Sorry, I am temporarily unavailable. You can call Laser Tech Service or send a service request using the form. Our specialists will help you with the problem.',
      timeout: 'The reply is taking longer than usual. Sorry for the inconvenience. Try again or contact our service team directly.',
      invalid: 'Sorry, I could not prepare a reply. Please ask again or contact our service team.',
      offline: 'You appear to be offline. Check your internet connection and try again.',
      long: 'Your message is too long. Shorten the description and try again.',
      empty: 'Describe the problem before sending a message.',
      repeated: 'I am experiencing temporary technical problems. For faster help, contact Laser Tech Service directly.',
      retryNote: 'The previous request may still be processing. Retrying will send it again.',
      onlineForm: 'The form requires an internet connection.',
    },
    pl: {
      open: 'ZAPYTAJ ŁAZARA', close: 'Zamknij czat', status: 'Asystent techniczny AI',
      greeting: 'Dzień dobry! Jestem Lazar, asystent techniczny AI Laser Tech Service. Opisz problem z urządzeniem, a pomogę Ci ustalić możliwe przyczyny i kolejne kroki.',
      placeholder: 'Opisz problem…', input: 'Wiadomość do Lazara', send: 'Wyślij', retry: 'Spróbuj ponownie',
      call: 'Zadzwoń', form: 'Wyślij zgłoszenie', log: 'Rozmowa z Lazarem', user: 'Ty', waiting: 'Lazar przygotowuje odpowiedź…',
      unavailable: 'Przepraszam, chwilowo jestem niedostępny. Możesz zadzwonić do Laser Tech Service lub wysłać zgłoszenie przez formularz. Nasi specjaliści pomogą Ci rozwiązać problem.',
      timeout: 'Odpowiedź zajmuje więcej czasu niż zwykle. Przepraszam za utrudnienia. Możesz spróbować ponownie albo skontaktować się bezpośrednio z naszym serwisem.',
      invalid: 'Przepraszam, nie udało mi się przygotować odpowiedzi. Spróbuj zadać pytanie ponownie lub skontaktuj się z naszym serwisem.',
      offline: 'Wygląda na to, że nie masz połączenia z internetem. Sprawdź połączenie i spróbuj ponownie.',
      long: 'Wiadomość jest zbyt długa. Skróć opis problemu i spróbuj ponownie.',
      empty: 'Opisz problem przed wysłaniem wiadomości.',
      repeated: 'Wygląda na to, że mam chwilowe problemy techniczne. Najszybciej uzyskasz pomoc, kontaktując się bezpośrednio z Laser Tech Service.',
      retryNote: 'Poprzednie zapytanie może być jeszcze przetwarzane. Ponowna próba wyśle je ponownie.',
      onlineForm: 'Formularz wymaga połączenia z internetem.',
    },
    ru: {
      open: 'СПРОСИТЬ ЛАЗАРЯ', close: 'Закрыть чат', status: 'Технический AI-консультант',
      greeting: 'Здравствуйте! Я Лазар, технический AI-консультант Laser Tech Service. Опишите проблему с оборудованием, и я помогу разобраться в возможных причинах и дальнейших действиях.',
      placeholder: 'Опишите проблему…', input: 'Сообщение Лазарю', send: 'Отправить', retry: 'Попробовать снова',
      call: 'Позвонить', form: 'Оставить заявку', log: 'Разговор с Лазарем', user: 'Вы', waiting: 'Лазар готовит ответ…',
      unavailable: 'Извините, сейчас я временно недоступен. Вы можете позвонить в Laser Tech Service или оставить заявку через форму. Наши специалисты помогут решить вашу проблему.',
      timeout: 'Ответ занимает больше времени, чем обычно. Извините за неудобства. Попробуйте ещё раз или свяжитесь напрямую с нашим сервисом.',
      invalid: 'Извините, мне не удалось подготовить ответ. Попробуйте задать вопрос ещё раз или свяжитесь с нашим сервисом.',
      offline: 'Похоже, отсутствует подключение к интернету. Проверьте соединение и попробуйте ещё раз.',
      long: 'Сообщение слишком длинное. Сократите описание проблемы и попробуйте ещё раз.',
      empty: 'Опишите проблему перед отправкой сообщения.',
      repeated: 'Похоже, у меня временные технические проблемы. Быстрее всего получить помощь можно, связавшись напрямую с Laser Tech Service.',
      retryNote: 'Предыдущий запрос ещё может обрабатываться. Повторная попытка отправит его заново.',
      onlineForm: 'Для формы нужно подключение к интернету.',
    },
  };
  const t = translations[language];
  const track = (event, category) => {
    window.dataLayer = window.dataLayer || [];
    const data = { event, language };
    if (category) data.error_category = category;
    window.dataLayer.push(data);
  };
  const make = (tag, className, text) => {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text) node.textContent = text;
    return node;
  };
  const avatar = () => {
    const img = make('img', 'lazar-avatar');
    img.src = '/img/lazar-ai-avatar.svg'; img.alt = ''; img.width = 38; img.height = 38;
    return img;
  };
  const button = (className, text) => { const node = make('button', className, text); node.type = 'button'; return node; };
  const root = make('div', 'lazar-root'); root.id = 'lazar-root';
  const launcher = button('lazar-launcher');
  const emblem = make('span', 'lazar-launcher-emblem'); emblem.append(avatar());
  launcher.append(emblem, make('span', 'lazar-launcher-label', t.open)); launcher.title = t.open;
  launcher.setAttribute('aria-label', t.open); launcher.setAttribute('aria-expanded', 'false'); launcher.setAttribute('aria-controls', 'lazar-panel');
  const panel = make('section', 'lazar-panel'); panel.id = 'lazar-panel'; panel.hidden = true;
  panel.setAttribute('role', 'dialog'); panel.setAttribute('aria-modal', 'false'); panel.setAttribute('aria-labelledby', 'lazar-title');
  const header = make('div', 'lazar-header');
  const heading = make('div', 'lazar-heading'); const title = make('h2', 'lazar-title', 'Lazar AI'); title.id = 'lazar-title';
  heading.append(title, make('span', 'lazar-brand', 'Laser Tech Service'), make('span', 'lazar-subtitle', t.status));
  const close = button('lazar-close', '×'); close.setAttribute('aria-label', t.close);
  header.append(avatar(), heading, close);
  const log = make('div', 'lazar-log'); log.setAttribute('role', 'log'); log.setAttribute('aria-live', 'polite'); log.setAttribute('aria-relevant', 'additions'); log.setAttribute('aria-label', t.log); log.tabIndex = 0;
  const feedback = make('p', 'lazar-feedback'); feedback.id = 'lazar-feedback'; feedback.setAttribute('role', 'status'); feedback.setAttribute('aria-live', 'polite'); feedback.setAttribute('aria-atomic', 'true');
  const retry = button('lazar-action lazar-retry', t.retry); retry.hidden = true;
  const makeContacts = () => {
    const contacts = make('div', 'lazar-contacts');
    const call = make('a', 'lazar-action', t.call); call.href = 'tel:+48790402597';
    const contact = make('a', 'lazar-action', t.form); contact.href = {pl: '/kontakt/#contactid', ru: '/ru/kontakt/#contactid', en: '/en/contact/'}[language];
    call.addEventListener('click', () => track('lazar_call_click'));
    contact.addEventListener('click', () => track('lazar_form_click'));
    contacts.append(call, contact);
    return contacts;
  };
  const form = make('form', 'lazar-form'); form.setAttribute('aria-label', t.input);
  const input = make('textarea', 'lazar-input'); input.rows = 2; input.placeholder = t.placeholder; input.setAttribute('aria-label', t.input); input.setAttribute('aria-describedby', 'lazar-feedback');
  const send = button('lazar-action lazar-send', t.send); send.type = 'submit';
  form.append(input, send); panel.append(header, log, feedback, retry, form); root.append(launcher, panel); document.body.append(root);
  // Reversible hiding: existing menu markup and handlers remain intact.
  document.querySelectorAll('.menu').forEach(menu => menu.classList.add('lazar-social-hidden'));
  let sessionId;
  const getSessionId = () => {
    if (sessionId) return sessionId;
    try { sessionId = sessionStorage.getItem('lazar-session-id'); } catch (_) { /* Storage may be unavailable. */ }
    if (!sessionId || !/^[a-zA-Z0-9-]{16,100}$/.test(sessionId)) {
      sessionId = crypto.randomUUID ? crypto.randomUUID() : Array.from(crypto.getRandomValues(new Uint32Array(4)), n => n.toString(16).padStart(8, '0')).join('');
      try { sessionStorage.setItem('lazar-session-id', sessionId); } catch (_) { /* Use this page's in-memory ID. */ }
    }
    return sessionId;
  };
  let greeted = false, pending = false, failed = null, failures = 0, errorRow = null;
  // Remove only a recognized trailing contact footer; real links are rendered below.
  const replyText = text => {
    const lines = text.trim().split('\n');
    let end = lines.length, found = false;
    const target = /(?:\+?48[\s-]*790[\s-]*402[\s-]*597|https:\/\/lasertechservice\.pl\/(?:(?:ru\/)?(?:kontakt\/)?|en\/contact\/)#contactid|https:\/\/lasertechservice\.pl\/(?:(?:ru\/)?kontakt|en\/contact)\/?)/i;
    const label = /^(?:\*\*)?(?:Call us|Call|Phone|Send a service request|Service request|Позвонить|Телефон|Оставить заявку|Заявка|Зателефонувати|Залишити заявку|Zadzwoń|Telefon|Wyślij zgłoszenie|Zgłoszenie)(?:\*\*)?\s*:?(?:\*\*)?\s*$/i;
    while (end > 0) {
      const line = lines[end - 1].trim();
      if (!line || label.test(line)) { end--; continue; }
      if (target.test(line) && line.length < 200) { found = true; end--; continue; }
      break;
    }
    const body = found && end > 0 ? lines.slice(0, end).join('\n').trim() : text.trim();
    return body;
  };
  const addMessage = (text, who) => {
    const row = make('div', 'lazar-message' + (who === 'user' ? ' lazar-message--user' : ''));
    row.setAttribute('aria-label', who === 'user' ? t.user : 'Lazar AI');
    if (who !== 'user') row.append(avatar());
    const content = make('div', 'lazar-message-content');
    const bubble = make('p', 'lazar-bubble');
    // A small safe bold renderer: all content remains text nodes, never HTML.
    const parts = (who === 'user' ? text : replyText(text)).split(/(\*\*[^*]+\*\*)/g);
    parts.forEach(part => bubble.append(part.startsWith('**') && part.endsWith('**')
      ? make('strong', '', part.slice(2, -2)) : document.createTextNode(part)));
    content.append(bubble);
    if (who !== 'user') content.append(makeContacts());
    row.append(content); log.append(row); log.scrollTop = log.scrollHeight;
    return row;
  };
  const viewport = () => {
    const vv = window.visualViewport;
    root.style.setProperty('--lazar-vh', (vv ? vv.height : window.innerHeight) + 'px');
    root.style.setProperty('--lazar-top', (vv ? vv.offsetTop : 0) + 'px');
    root.classList.toggle('lazar-root--compact', (vv ? vv.height : innerHeight) < 480);
  };
  window.visualViewport?.addEventListener('resize', viewport);
  window.visualViewport?.addEventListener('scroll', viewport);
  window.addEventListener('resize', viewport); viewport();
  launcher.addEventListener('click', () => {
    panel.hidden = false; launcher.hidden = true; launcher.setAttribute('aria-expanded', 'true');
    if (!greeted) { addMessage(t.greeting, 'assistant'); greeted = true; }
    viewport(); close.focus({ preventScroll: true }); track('lazar_open');
  });
  const hide = (restoreFocus = true) => { panel.hidden = true; launcher.hidden = false; launcher.setAttribute('aria-expanded', 'false'); if (restoreFocus) launcher.focus({ preventScroll: true }); };
  close.addEventListener('click', () => hide());
  panel.addEventListener('keydown', e => { if (e.key === 'Escape') { e.preventDefault(); e.stopPropagation(); hide(); } });
  const busy = value => {
    pending = value; send.disabled = value; retry.disabled = value; input.readOnly = value;
    form.setAttribute('aria-busy', String(value));
  };
  const showFailure = category => {
    failures += 1;
    const copy = { timeout: t.timeout, offline: t.offline, invalid_response: t.invalid };
    let text = failures >= 3 ? t.repeated : (copy[category] || t.unavailable);
    if (category === 'timeout') text += ' ' + t.retryNote;
    if (category === 'offline') text += ' ' + t.onlineForm;
    feedback.textContent = '';
    errorRow = addMessage(text, 'assistant');
    errorRow.querySelector('.lazar-contacts').classList.toggle('lazar-contacts--priority', failures >= 3);
    input.value = failed.message;
    retry.hidden = false; track('lazar_error', category);
  };
  const transmit = async isRetry => {
    if (pending) return;
    const message = isRetry && failed ? failed.message : input.value.trim();
    if (!message) { feedback.textContent = t.empty; input.focus(); return; }
    if (Array.from(message).length > config.maxMessageLength) { feedback.textContent = t.long; track('lazar_error', 'message_too_long'); return; }
    // Clear immediately; keep the failed payload in memory and restore it on failure.
    if (isRetry) track('lazar_retry');
    if (!failed || failed.message !== message) addMessage(message, 'user');
    errorRow?.remove(); errorRow = null;
    failed = { message }; input.value = ''; retry.hidden = true; feedback.textContent = t.waiting; busy(true);
    let timedOut = false;
    const controller = new AbortController();
    const timer = setTimeout(() => { timedOut = true; controller.abort(); }, config.timeoutMs);
    try {
      if (navigator.onLine === false) throw { category: 'offline' };
      track('lazar_message_sent');
      const response = await fetch(config.endpoint, {
        method: 'POST', headers: { 'Content-Type': 'application/json' }, signal: controller.signal,
        credentials: 'omit', referrerPolicy: 'no-referrer',
        body: JSON.stringify({ message, language, page_url: location.origin + location.pathname, session_id: getSessionId() }),
      });
      if (!response.ok) throw { category: 'server_error' };
      let data;
      try { data = await response.json(); } catch (error) {
        if (timedOut) throw error;
        throw { category: 'invalid_response' };
      }
      if (!data || typeof data.reply !== 'string' || !data.reply.trim() || ['undefined', 'null', '[object Object]'].includes(data.reply.trim())) throw { category: 'invalid_response' };
      addMessage(data.reply.trim(), 'assistant');
      input.value = ''; failed = null; failures = 0; feedback.textContent = ''; retry.hidden = true;
    } catch (error) {
      const category = timedOut ? 'timeout' : navigator.onLine === false ? 'offline' : error.category || 'network';
      showFailure(category);
    } finally { clearTimeout(timer); busy(false); }
  };
  form.addEventListener('submit', e => { e.preventDefault(); transmit(false); });
  retry.addEventListener('click', () => transmit(true));
  // Enter sends; Shift+Enter and IME composition retain normal multiline input.
  input.addEventListener('keydown', e => { if (e.key === 'Enter' && !e.shiftKey && !e.isComposing) { e.preventDefault(); transmit(false); } });
})();

/* =========================================================
   LASER TECH SERVICE
   MAIN.JS

   01. Mobile navigation
   02. Restore scroll position
   03. Dark mode
   04. FAQ
   05. Floating social menu
   06. Instagram animation
   07. Scroll animations
   08. Smooth anchor scroll
   09. Jarallax
   10. Legacy social button
   11. Devices carousel
========================================================= */

/* =========================================================
   01. MOBILE NAVIGATION
========================================================= */

document.addEventListener("DOMContentLoaded", () => {
  const nav = document.getElementById("siteNav");

  const toggle = document.querySelector(".nav-toggle");

  const navList = document.getElementById("primaryNavigation");

  if (!nav || !toggle || !navList) {
    return;
  }

  // HTML lang is authoritative; normalize regional tags. Unknown/missing values use PL.
  const locale = document.documentElement.lang.trim().toLowerCase().split('-')[0];
  const language = ['pl', 'ru', 'en'].includes(locale) ? locale : 'pl';
  const labels = {pl: ['Otwórz menu', 'Zamknij menu'], ru: ['Открыть меню', 'Закрыть меню'], en: ['Open menu', 'Close menu']};
  const [openLabel, closeLabel] = labels[language];
  toggle.setAttribute("aria-label", openLabel);

  function openMenu() {
    nav.classList.add("nav--open");

    document.body.classList.add("nav-open");

    toggle.setAttribute("aria-expanded", "true");

    toggle.setAttribute("aria-label", closeLabel);
  }

  function closeMenu() {
    nav.querySelectorAll(".nav-submenu-toggle").forEach((button) => {
      button.setAttribute("aria-expanded", "false");
      const submenu = document.getElementById(button.getAttribute("aria-controls"));
      if (submenu) submenu.hidden = true;
    });
    nav.classList.remove("nav--open");

    document.body.classList.remove("nav-open");

    toggle.setAttribute("aria-expanded", "false");

    toggle.setAttribute("aria-label", openLabel);
  }

  function toggleMenu() {
    const isOpen = nav.classList.contains("nav--open");

    if (isOpen) {
      closeMenu();
    } else {
      openMenu();
    }
  }

  /* BURGER CLICK */

  toggle.addEventListener("click", (event) => {
    event.stopPropagation();

    toggleMenu();
  });

  /* CLOSE AFTER CLICKING NAV LINK */

  navList.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", () => {
      closeMenu();
    });
  });

  /* CLOSE AFTER CLICKING LANGUAGE SWITCHER */

  document.querySelectorAll(".language-switcher__link").forEach((link) => {
    link.addEventListener("click", () => {
      closeMenu();
    });
  });

  /* CLICK OUTSIDE */

  document.addEventListener("click", (event) => {
    if (!nav.classList.contains("nav--open")) {
      return;
    }

    if (nav.contains(event.target)) {
      return;
    }

    closeMenu();
  });

  /* ESC */

  document.addEventListener("keydown", (event) => {
    if (event.key !== "Escape") {
      return;
    }

    if (!nav.classList.contains("nav--open")) {
      return;
    }

    closeMenu();

    toggle.focus();
  });

  /* CLOSE AFTER RESIZE TO DESKTOP */

  window.addEventListener("resize", () => {
    if (window.innerWidth > 760) {
      closeMenu();
    }
  });
});

/* Native disclosure works without JS; enhance keyboard and dismissal behavior. */
document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.language-switcher__dropdown').forEach(dropdown => {
    const toggle = dropdown.querySelector('summary');
    const links = [...dropdown.querySelectorAll('a')];
    const syncExpanded = () => toggle.setAttribute('aria-expanded', String(dropdown.open));
    syncExpanded();
    dropdown.addEventListener('toggle', syncExpanded);
    const close = (focus = false) => { dropdown.open = false; if (focus) toggle.focus(); };
    dropdown.addEventListener('keydown', event => {
      if (event.key === 'Escape' && dropdown.open) {
        event.preventDefault(); event.stopPropagation(); close(true);
      } else if (['ArrowDown', 'ArrowUp', 'Home', 'End'].includes(event.key)) {
        event.preventDefault(); dropdown.open = true;
        const index = links.indexOf(document.activeElement);
        const next = event.key === 'Home' ? 0 : event.key === 'End' ? links.length - 1
          : event.key === 'ArrowDown' ? (index + 1) % links.length : (index < 0 ? links.length - 1 : (index - 1 + links.length) % links.length);
        links[next]?.focus();
      }
    });
    // Safari touch can blur summary before the link receives its click.
    // Dismiss on a real focus transfer; outside taps are handled below.
    dropdown.addEventListener('focusout', event => {
      if (event.relatedTarget && !dropdown.contains(event.relatedTarget)) close();
    });
    links.forEach(link => link.addEventListener('click', () => close()));
    document.addEventListener('click', event => { if (!dropdown.contains(event.target)) close(); });
    document.querySelector('.nav-toggle')?.addEventListener('click', () => close());
  });
});

/* Services disclosure: keep the parent service link independently usable. */
document.addEventListener("DOMContentLoaded", () => {
  document.querySelectorAll(".nav-services").forEach((item) => {
    const button = item.querySelector(".nav-submenu-toggle");
    const submenu = item.querySelector(".nav-submenu");
    if (!button || !submenu) return;
    button.hidden = false;
    function setOpen(open) {
      button.setAttribute("aria-expanded", String(open));
      submenu.hidden = !open;
    }
    button.addEventListener("click", () => setOpen(submenu.hidden));
    if (item.classList.contains('nav-work')) {
      item.querySelector('.nav-list__link').addEventListener('pointerenter', event => {
        if (event.pointerType === 'mouse' && window.innerWidth > 760) setOpen(true);
      });
      item.addEventListener('pointerleave', event => {
        if (event.pointerType === 'mouse' && !item.contains(document.activeElement)) setOpen(false);
      });
    }
    button.addEventListener("keydown", (event) => {
      if (event.key === "ArrowDown") {
        event.preventDefault();
        setOpen(true);
        submenu.querySelector("a")?.focus();
      }
    });
    item.addEventListener("keydown", (event) => {
      if (event.key === "Escape" && !submenu.hidden) {
        event.preventDefault();
        event.stopPropagation();
        setOpen(false);
        button.focus();
      }
    });
    item.addEventListener("focusout", (event) => {
      if (!item.contains(event.relatedTarget)) setOpen(false);
    });
    document.addEventListener("click", (event) => {
      if (!item.contains(event.target)) setOpen(false);
    });
  });
});

/* =========================================================
   02. RESTORE SCROLL POSITION
========================================================= */

window.addEventListener("load", () => {
  const scrollPosition = localStorage.getItem("scrollPosition");

  if (!scrollPosition) {
    return;
  }

  const nav = document.querySelector(".nav");

  const navHeight = nav?.offsetHeight || 0;

  const position = Math.max(0, parseInt(scrollPosition, 10) - navHeight);

  window.scrollTo({
    top: position,

    left: 0,

    behavior: "smooth",
  });

  localStorage.removeItem("scrollPosition");
});

/* =========================================================
   03. DARK MODE

   CIEMNY MOTYW JEST STAŁY
========================================================= */

document.addEventListener("DOMContentLoaded", () => {
  document.body.classList.add("dark");

  localStorage.setItem("darkMode", "dark");
});

/* =========================================================
   04. FAQ
========================================================= */

document.addEventListener("DOMContentLoaded", () => {
  const faqItems = document.querySelectorAll(".faq__item");

  if (!faqItems.length) {
    return;
  }

  function setExpanded(item, expanded) {
    item.classList.toggle("active", expanded);
    item.querySelector(".faq__question")?.setAttribute("aria-expanded", String(expanded));
    item.querySelector(".faq__answer")?.setAttribute("aria-hidden", String(!expanded));
  }

  faqItems.forEach((item) => {
    const button = item.querySelector(".faq__question");

    if (!button) {
      return;
    }

    setExpanded(item, item.classList.contains("active"));

    button.addEventListener("click", () => {
      faqItems.forEach((otherItem) => {
        if (otherItem !== item) {
          setExpanded(otherItem, false);
        }
      });

      setExpanded(item, !item.classList.contains("active"));
    });
  });
});

/* =========================================================
   05. FLOATING SOCIAL MENU
========================================================= */

document.addEventListener("DOMContentLoaded", () => {
  const trigger = document.querySelector("menu > .trigger");

  if (!trigger) {
    return;
  }

  trigger.setAttribute("aria-expanded", String(trigger.parentElement.classList.contains("open")));

  trigger.addEventListener("click", (event) => {
    const menu = event.currentTarget.parentElement;

    if (!menu) {
      return;
    }

    menu.classList.toggle("open");
    trigger.setAttribute("aria-expanded", String(menu.classList.contains("open")));
  });
});

/* =========================================================
   06. INSTAGRAM ANIMATION
========================================================= */

document.addEventListener("DOMContentLoaded", () => {
  const instSection = document.querySelector(".inst__sub");

  if (!instSection) {
    return;
  }

  if (!("IntersectionObserver" in window) || window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    instSection.classList.add("visible");
    return;
  }

  document.body.classList.add("instagram-reveal-ready");
  const observer = new IntersectionObserver((entries, currentObserver) => {
    if (entries.some((entry) => entry.isIntersecting)) {
      instSection.classList.add("visible");
      currentObserver.disconnect();
    }
  }, {
    rootMargin: "0px 0px -100px 0px",
    threshold: 0,
  });
  observer.observe(instSection);
});

/* =========================================================
   07. SCROLL ANIMATIONS
========================================================= */

document.addEventListener("DOMContentLoaded", () => {
  const animatedItems = document.querySelectorAll(".scroll-animate");

  if (!animatedItems.length || !("IntersectionObserver" in window)) {
    return;
  }

  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
  if (prefersReducedMotion.matches) {
    animatedItems.forEach((item) => item.classList.add("visible"));
    return;
  }

  document.body.classList.add("scroll-reveal-ready");
  const observer = new IntersectionObserver((entries, currentObserver) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        currentObserver.unobserve(entry.target);
      }
    });
  }, {
    rootMargin: "0px 0px -80px 0px",
    threshold: 0,
  });
  animatedItems.forEach((item) => observer.observe(item));
});

/* =========================================================
   08. SMOOTH ANCHOR SCROLL
========================================================= */

document.addEventListener("DOMContentLoaded", () => {
  const anchorLinks = document.querySelectorAll('a[href^="#"]');

  anchorLinks.forEach((link) => {
    link.addEventListener("click", function (event) {
      const href = this.getAttribute("href");

      if (!href || href === "#") {
        return;
      }

      const target = document.querySelector(href);

      if (!target) {
        return;
      }

      event.preventDefault();

      const navHeight = document.querySelector(".nav")?.offsetHeight || 0;

      const targetPosition =
        target.getBoundingClientRect().top + window.scrollY - navHeight - 10;

      window.scrollTo({
        top: targetPosition,

        behavior: "smooth",
      });
    });
  });
});

/* =========================================================
   09. JARALLAX
========================================================= */

document.addEventListener("DOMContentLoaded", () => {
  const jarallaxElements = document.querySelectorAll(".jarallax");

  if (!jarallaxElements.length) {
    return;
  }

  const initialize = () => {
    if (typeof window.jarallax === "function") window.jarallax(jarallaxElements);
  };
  if (typeof window.jarallax === "function") initialize();
  else document.querySelector('script[src*="jarallax.min.js"]')?.addEventListener('load', initialize, { once: true });
});

/* =========================================================
   10. LEGACY SOCIAL BUTTON
========================================================= */

document.addEventListener("DOMContentLoaded", () => {
  const mainButton = document.getElementById("main-button");

  if (!mainButton) {
    return;
  }

  mainButton.addEventListener("click", () => {
    const socialButtons = document.querySelector(".social-buttons");

    if (!socialButtons) {
      return;
    }

    socialButtons.classList.toggle("show");
  });
});

/* =========================================================
   11. DEVICES CAROUSEL
========================================================= */

document.addEventListener("DOMContentLoaded", () => {
  const track = document.getElementById("carouselTrack");
  if (!track || track.dataset.carouselReady === "true") return;
  track.dataset.carouselReady = "true";
  const wrapper = track.closest('.carousel-wrapper');
  const mobile = matchMedia('(max-width: 767px)');
  const reducedMotion = matchMedia('(prefers-reduced-motion: reduce)');
  const originals = Array.from(track.children);
  let clones = [], position = 0, frame = null, lastTime = null;
  let visible = false, dragging = false, startX = 0, startPosition = 0;
  const render = () => {
    const length = track.scrollWidth / 2;
    if (length) position = ((position % length) - length) % length;
    track.style.transform = `translateX(${position}px)`;
  };
  const shouldAnimate = () => !mobile.matches && !reducedMotion.matches && visible && !document.hidden && !dragging;
  const stop = () => {
    if (frame !== null) cancelAnimationFrame(frame);
    frame = null; lastTime = null;
  };
  function tick(time) {
    frame = null;
    if (!shouldAnimate()) { lastTime = null; return; }
    if (lastTime !== null) position -= Math.min(time - lastTime, 50) * 0.018;
    lastTime = time;
    render();
    frame = requestAnimationFrame(tick);
  }
  const syncAnimation = () => {
    if (!shouldAnimate()) stop();
    else if (frame === null) frame = requestAnimationFrame(tick);
  };
  const setMode = () => {
    stop(); dragging = false; position = 0;
    if (mobile.matches) {
      clones.forEach(node => node.remove()); clones = [];
      track.style.removeProperty('transform');
    } else {
      wrapper.scrollLeft = 0;
      if (!clones.length) {
        clones = originals.map(node => {
          const clone = node.cloneNode(true);
          clone.setAttribute('aria-hidden', 'true'); clone.inert = true;
          clone.removeAttribute('id'); clone.querySelectorAll('[id]').forEach(child => child.removeAttribute('id'));
          return clone;
        });
        track.append(...clones);
      }
      render();
    }
    syncAnimation();
  };
  new IntersectionObserver(entries => {
    visible = entries[0].isIntersecting;
    syncAnimation();
  }).observe(wrapper);
  mobile.addEventListener('change', setMode);
  reducedMotion.addEventListener('change', syncAnimation);
  document.addEventListener('visibilitychange', syncAnimation);
  setMode();

  const beginDrag = x => {
    if (mobile.matches) return;
    dragging = true; startX = x; startPosition = position; stop();
  };
  const moveDrag = x => {
    if (!dragging || mobile.matches) return;
    position = startPosition + x - startX; render();
  };
  const endDrag = () => { dragging = false; syncAnimation(); };
  track.addEventListener('mousedown', event => beginDrag(event.clientX));
  window.addEventListener('mousemove', event => moveDrag(event.clientX));
  window.addEventListener('mouseup', endDrag);
  track.addEventListener('touchstart', event => {
    if (event.touches.length) beginDrag(event.touches[0].clientX);
  }, {passive: true});
  window.addEventListener('touchmove', event => {
    if (event.touches.length) moveDrag(event.touches[0].clientX);
  }, {passive: true});
  window.addEventListener('touchend', endDrag, {passive: true});
  window.addEventListener('touchcancel', endDrag, {passive: true});
  track.addEventListener('wheel', event => {
    if (mobile.matches) return;
    event.preventDefault(); position -= event.deltaY * 0.5; render();
  }, {passive: false});
});

/* Keep the visible contact controls lightweight until Lazar is requested. */
(() => {
  const language = () => {
    const locale = document.documentElement.lang.trim().toLowerCase().split('-')[0];
    return ['pl', 'ru', 'en'].includes(locale) ? locale : 'pl';
  };
  const labels = {
    en: {
      open: 'Ask Lazar', bar: 'Quick contact', call: 'Call', lazar: 'Lazar',
      loading: 'Loading the assistant…', error: 'The assistant could not be loaded. Press the button to try again.',
    },
    pl: {
      open: 'Zapytaj Łazarza', bar: 'Szybki kontakt', call: 'Zadzwoń', lazar: 'Łazarz',
      loading: 'Ładowanie asystenta…', error: 'Nie udało się załadować asystenta. Naciśnij przycisk, aby spróbować ponownie.',
    },
    ru: {
      open: 'Спросить Лазаря', bar: 'Быстрая связь', call: 'Позвонить', lazar: 'Лазарь',
      loading: 'Загрузка ассистента…', error: 'Не удалось загрузить ассистента. Нажмите кнопку, чтобы попробовать снова.',
    },
  };
  const make = (tag, className, text) => {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text) node.textContent = text;
    return node;
  };
  const getLabels = () => labels[language()];
  let loadPromise;
  let stylePromise;
  let scriptPromise;
  let lazarReady = false;
  const loadResources = () => {
    if (lazarReady) return Promise.resolve();
    if (loadPromise) return loadPromise;

    loadPromise = Promise.all([loadStylesheet(), loadScript()])
      .then(() => {
        if (document.getElementById('lazar-root')?.dataset.lazarReady !== 'true') {
          throw new Error('Lazar did not finish initialization.');
        }
        lazarReady = true;
      })
      .catch((error) => {
        loadPromise = null;
        const script = document.getElementById('lazar-ai-script');
        if (document.getElementById('lazar-root')?.dataset.lazarReady !== 'true') {
          script?.remove();
          document.getElementById('lazar-panel')?.remove();
          scriptPromise = null;
        }
        const style = document.getElementById('lazar-ai-style');
        if (style?.dataset.loadState !== 'loaded') {
          style?.remove();
          stylePromise = null;
        }
        throw error;
      });
      return loadPromise;
  };
  const loadStylesheet = () => {
    if (stylePromise) return stylePromise;
    stylePromise = new Promise((resolve, reject) => {
      let style = document.getElementById('lazar-ai-style');
      if (style?.dataset.loadState === 'loaded') {
        resolve();
        return;
      }
      if (!style) {
        style = document.createElement('link');
        style.id = 'lazar-ai-style';
        style.rel = 'stylesheet';
        style.href = '/css/lazar-ai.css';
      }
      style.dataset.loadState = 'loading';
      style.addEventListener('load', () => {
        style.dataset.loadState = 'loaded';
        resolve();
      }, { once: true });
      style.addEventListener('error', () => reject(new Error('Could not load Lazar styles.')), { once: true });
      if (!style.isConnected) document.head.appendChild(style);
    }).catch((error) => {
      stylePromise = null;
      throw error;
    });
    return stylePromise;
  };
  const loadScript = () => {
    if (scriptPromise) return scriptPromise;
    scriptPromise = new Promise((resolve, reject) => {
      const script = document.createElement('script');
      script.id = 'lazar-ai-script';
      script.src = '/js/lazar-ai.js';
      script.async = true;
      script.addEventListener('load', resolve, { once: true });
      script.addEventListener('error', () => reject(new Error('Could not load Lazar script.')), { once: true });
      document.body.appendChild(script);
    }).catch((error) => {
      scriptPromise = null;
      throw error;
    });
    return scriptPromise;
  };
  const mountShell = () => {
    if (document.getElementById('lazar-root')) return;

    const root = make('div', 'lazar-root');
    root.id = 'lazar-root';
    const routeLanguage = location.pathname.startsWith('/en/') ? 'en' : location.pathname.startsWith('/ru/') ? 'ru' : 'pl';
    const sendingEnabled = document.body.hasAttribute('data-error-localization')
      || (language() === routeLanguage && (language() !== 'en' || document.documentElement.dataset.lazarEnabled === 'true'));
    root.dataset.sendingEnabled = String(sendingEnabled);
    const launcher = make('button', 'lazar-launcher');
    launcher.type = 'button';
    launcher.setAttribute('aria-expanded', 'false');
    launcher.setAttribute('aria-controls', 'lazar-panel');
    const emblem = make('span', 'lazar-launcher-emblem');
    const avatar = make('img', 'lazar-avatar');
    avatar.src = '/img/lazar-ai-avatar.svg';
    avatar.alt = '';
    avatar.width = 38;
    avatar.height = 38;
    emblem.append(avatar);
    launcher.append(emblem, make('span', 'lazar-launcher-label'));

    const status = make('span', 'lazar-loader-status');
    status.setAttribute('role', 'status');
    status.setAttribute('aria-live', 'polite');
    const bar = make('nav', 'mobile-contact-bar');
    const callLabel = make('span');
    const lazarLabel = make('span');
    function makeContact(action, href, icon, label) {
      const control = make(href ? 'a' : 'button', 'mobile-contact-bar__action');
      control.dataset.action = action;
      if (href) {
        control.href = href;
        if (action !== 'phone') {
          control.target = '_blank';
          control.rel = 'noopener noreferrer';
        }
      } else {
        control.type = 'button';
        control.setAttribute('aria-controls', 'lazar-panel');
        control.setAttribute('aria-expanded', 'false');
      }
      const image = make('img');
      image.src = icon;
      image.alt = '';
      image.width = 28;
      image.height = 28;
      const frame = make('span', 'mobile-contact-bar__icon');
      frame.append(image);
      control.append(frame, label);
      control.addEventListener('click', () => {
        if (typeof window.gtag === 'function') window.gtag('event', 'mobile_contact_click', {
          action, placement: 'mobile_bottom_bar', page_path: location.pathname, language: language(),
        });
        if (action === 'lazar') open();
      });
      return control;
    }
    bar.append(
      makeContact('phone', 'tel:+48790402597', '/img/icons/gold-phone.svg', callLabel),
      makeContact('whatsapp', 'https://wa.me/48790402597', '/img/icons/gold-whatsapp.svg', make('span', '', 'WhatsApp')),
      makeContact('instagram', 'https://www.instagram.com/lasertech.service/', '/img/icons/gold-instagram.svg', make('span', '', 'Instagram')),
      makeContact('lazar', null, '/img/lazar-ai-avatar.svg', lazarLabel),
    );
    root.append(launcher, status, bar);
    document.body.append(root);
    document.querySelectorAll('.menu').forEach((menu) => menu.classList.add('lazar-social-hidden'));

    const updateLabels = () => {
      const text = getLabels();
      launcher.setAttribute('aria-label', text.open);
      launcher.title = text.open;
      launcher.querySelector('.lazar-launcher-label').textContent = text.open;
      bar.setAttribute('aria-label', text.bar);
      callLabel.textContent = text.call;
      lazarLabel.textContent = text.lazar;
    };
    const open = async () => {
      if (launcher.getAttribute('aria-busy') === 'true') return;
      launcher.setAttribute('aria-busy', 'true');
      bar.querySelector('[data-action="lazar"]').setAttribute('aria-busy', 'true');
      status.textContent = getLabels().loading;
      try {
        await loadResources();
        status.textContent = '';
        window.dispatchEvent(new Event('lazar:open'));
      } catch (error) {
        console.error('Unable to load Lazar assistant.', error);
        status.textContent = getLabels().error;
      } finally {
        launcher.removeAttribute('aria-busy');
        bar.querySelector('[data-action="lazar"]').removeAttribute('aria-busy');
      }
    };
    launcher.addEventListener('click', open);
    document.addEventListener('error-language-change', updateLabels);
    updateLabels();
  };
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mountShell, { once: true });
  else mountShell();
})();

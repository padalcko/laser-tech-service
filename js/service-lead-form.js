/* =========================================================
   LASER TECH SERVICE
   SERVICE LEAD FORM
   ---------------------------------------------------------
   Obsługa formularzy leadowych:
   - PL / RU / EN
   - walidacja
   - wysyłka do n8n
   - komunikaty success / error
   - blokada wielokrotnego wysłania
   - GA4 event po poprawnym wysłaniu

   Endpoint:
   https://n8n.raccoon-studio.com.ua/webhook/lts-service-lead
========================================================= */

"use strict";

document.addEventListener("DOMContentLoaded", () => {
  /* =======================================================
     CONFIG
  ======================================================= */

  const WEBHOOK_URL =
    "https://n8n.raccoon-studio.com.ua/webhook/lts-service-lead";

  const REQUEST_TIMEOUT_MS = 15000;

  const forms = document.querySelectorAll(".article-service-form__form");

  if (!forms.length) {
    return;
  }

  /* =======================================================
     TRANSLATIONS
  ======================================================= */

  const translations = {
    en: {
      sending: "Sending…", submit: "Send a service request",
      success: "Thank you. We have received your service request and will contact you.",
      error: "The form could not be sent. Please try again or contact us by phone.",
      required: "Please fill in this field.", invalid: "Please enter a valid value.",
      consentRequired: "Please agree to the processing of your data to send this request.",
      consent: "I agree to the processing of my personal data by Laser Tech Service for the purpose of handling my service request.",
    },
    pl: {
      sending: "Wysyłanie...",
      success:
        "Dziękujemy. Otrzymaliśmy Twoje zgłoszenie. Skontaktujemy się z Tobą.",
      error:
        "Nie udało się wysłać formularza. Spróbuj ponownie lub skontaktuj się z nami telefonicznie.",
    },

    ru: {
      sending: "Отправка...",
      success: "Спасибо. Мы получили вашу заявку и свяжемся с вами.",
      error:
        "Не удалось отправить форму. Попробуйте ещё раз или свяжитесь с нами по телефону.",
    },
  };

  /* =======================================================
     HELPERS
  ======================================================= */

  // HTML lang is authoritative; normalize regional tags. Unknown/missing values use PL.
  const locale = document.documentElement.lang.trim().toLowerCase().split('-')[0];
  const language = ['pl', 'ru', 'en'].includes(locale) ? locale : 'pl';

  const getFormValue = (formData, fieldName) => {
    const value = formData.get(fieldName);

    if (typeof value !== "string") {
      return "";
    }

    return value.trim();
  };

  const createMessageElement = (form) => {
    let message = form.querySelector(".article-service-form__message");

    if (message) {
      return message;
    }

    message = document.createElement("p");

    message.className = "article-service-form__message";

    message.setAttribute("role", "status");
    message.setAttribute("aria-live", "polite");

    form.appendChild(message);

    return message;
  };

  const clearMessage = (message) => {
    message.textContent = "";

    message.classList.remove(
      "article-service-form__message--success",
      "article-service-form__message--error",
    );
  };

  const showSuccess = (message, text) => {
    clearMessage(message);

    message.textContent = text;

    message.classList.add("article-service-form__message--success");
  };

  const showError = (message, text) => {
    clearMessage(message);

    message.textContent = text;

    message.classList.add("article-service-form__message--error");
  };

  const sendAnalyticsEvent = (language, source, isB2B) => {
    if (typeof window.gtag !== "function") {
      return;
    }

    window.gtag("event", isB2B ? "b2b_lead_submit" : "service_lead_submit", {
      form_name: isB2B ? "b2b_service_lead" : "service_lead",
      language,
      source,
    });
  };

  /* =======================================================
     FORM INITIALIZATION
  ======================================================= */

  forms.forEach((form) => {
    const submitButton = form.querySelector(".article-service-form__submit");

    if (!submitButton) {
      return;
    }

    const text = translations[language];

    const isB2B = form.hasAttribute('data-b2b-form');
    const b2bText = {
      pl: { required: 'Wypełnij to pole.', invalid: 'Podaj prawidłową wartość.', contact: 'Podaj prawidłowy telefon lub adres email.', consent: 'Wyraź zgodę na przetwarzanie danych, aby wysłać zapytanie.', count: 'Liczba salonów', message: 'Wiadomość' },
      ru: { required: 'Заполните это поле.', invalid: 'Укажите корректное значение.', contact: 'Укажите корректный телефон или email.', consent: 'Подтвердите согласие на обработку данных для отправки заявки.', count: 'Количество салонов', message: 'Сообщение' },
      en: { required: 'Please fill in this field.', invalid: 'Please enter a valid value.', contact: 'Enter a valid phone number or email address.', consent: 'Please agree to data processing to send your enquiry.', count: 'Number of salons', message: 'Message' },
    }[language];

    const message = createMessageElement(form);

    if (language === 'en' || isB2B) {
      if (!isB2B) submitButton.textContent = text.submit;
      const consent = form.querySelector('.consent span');
      if (consent && !isB2B) consent.textContent = text.consent;
      form.addEventListener('invalid', event => {
        const field = event.target;
        if (isB2B && field.name === 'phone' && field.validity.customError) return;
        field.setCustomValidity('');
        field.setCustomValidity(field.validity.valueMissing
          ? (field.name === 'consent' ? (isB2B ? b2bText.consent : text.consentRequired) : (isB2B ? b2bText.required : text.required)) : (isB2B ? b2bText.invalid : text.invalid));
      }, true);
      for (const type of ['input', 'change']) form.addEventListener(type, event => {
        if (typeof event.target.setCustomValidity === 'function') event.target.setCustomValidity('');
      });
      form.addEventListener('reset', () => form.querySelectorAll('input, textarea, select').forEach(field => field.setCustomValidity('')));
    }

    const validateB2BContact = () => {
      if (!isB2B) return;
      const contact = form.elements.namedItem('phone');
      const value = contact.value.trim();
      const validEmail = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
      const validPhone = /^[+\d\s().-]+$/.test(value) && value.replace(/\D/g, '').length >= 7 && value.replace(/\D/g, '').length <= 15;
      contact.setCustomValidity(value && !validEmail && !validPhone ? b2bText.contact : '');
    };
    if (isB2B) {
      form.elements.namedItem('phone').addEventListener('input', () => queueMicrotask(validateB2BContact));
      form.elements.namedItem('phone').addEventListener('change', () => queueMicrotask(validateB2BContact));
    }

    const defaultButtonText = submitButton.textContent.trim();

    let isSubmitting = false;

    /* =====================================================
       SUBMIT
    ===================================================== */

    form.addEventListener("submit", async (event) => {
      event.preventDefault();

      /* -------------------------------------------------
           Prevent double submit
        ------------------------------------------------- */

      if (isSubmitting) {
        return;
      }

      /* -------------------------------------------------
           Native HTML validation
        ------------------------------------------------- */

      validateB2BContact();
      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }

      clearMessage(message);

      const formData = new FormData(form);

      // Optional honeypot on landing forms; existing forms keep their contract.
      if (getFormValue(formData, "companyWebsite")) {
        showError(message, text.error);
        return;
      }

      const payload = {
        fullName: getFormValue(formData, "fullName"),

        phone: getFormValue(formData, "phone"),

        city: getFormValue(formData, "city"),

        salonName: getFormValue(formData, "salonName"),

        deviceName: getFormValue(formData, "deviceName"),

        language,

        source: getFormValue(formData, "source") || "website",

        pageUrl: window.location.href,
      };

      // Send additional fields only when the form provides them.
      for (const field of ["serviceType", "problemDescription"]) {
        if (formData.has(field)) payload[field] = getFormValue(formData, field);
      }

      // Keep the existing n8n payload: company -> salonName; phone/email -> phone;
      // equipment -> deviceName; branch count and optional message -> description.
      if (isB2B) {
        const count = getFormValue(formData, 'salonCount');
        if (!['1', '2-5', '6-10', '10+'].includes(count)) {
          showError(message, text.error);
          return;
        }
        payload.problemDescription = `${b2bText.count}: ${count}`;
        const details = getFormValue(formData, 'problemDescription');
        if (details) payload.problemDescription += `\n${b2bText.message}: ${details}`;
      }

      /* -------------------------------------------------
           UI: sending
        ------------------------------------------------- */

      isSubmitting = true;

      submitButton.disabled = true;

      submitButton.textContent = text.sending;

      form.setAttribute("aria-busy", "true");

      /* -------------------------------------------------
           Request
        ------------------------------------------------- */

      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

      try {
        const response = await fetch(WEBHOOK_URL, {
          method: "POST",

          signal: controller.signal,

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify(payload),
        });

        if (!response.ok) {
          throw new Error(`HTTP error: ${response.status}`);
        }

        const result = await response.json();

        if (result?.success !== true) {
          throw new Error("Webhook returned unsuccessful response");
        }

        /* -----------------------------------------------
             Success
          ----------------------------------------------- */

        form.reset();

        showSuccess(message, text.success);

        sendAnalyticsEvent(payload.language, payload.source, isB2B);
      } catch (error) {
        /* -----------------------------------------------
             Error
          ----------------------------------------------- */

        console.error("Laser Tech Service lead form error:", error);

        showError(message, text.error);
      } finally {
        clearTimeout(timeoutId);

        /* -----------------------------------------------
             Restore form
          ----------------------------------------------- */

        isSubmitting = false;

        submitButton.disabled = false;

        submitButton.textContent = defaultButtonText;

        form.removeAttribute("aria-busy");
      }
    });
  });
});

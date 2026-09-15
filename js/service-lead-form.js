/* =========================================================
   LASER TECH SERVICE
   SERVICE LEAD FORM
   ---------------------------------------------------------
   Obsługa formularzy leadowych:
   - PL / RU
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

  const forms = document.querySelectorAll(".article-service-form__form");

  if (!forms.length) {
    return;
  }

  /* =======================================================
     TRANSLATIONS
  ======================================================= */

  const translations = {
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

  const getLanguage = (form) => {
    const languageInput = form.querySelector('input[name="language"]');

    const language = languageInput?.value?.trim().toLowerCase();

    return translations[language] ? language : "pl";
  };

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

  const sendAnalyticsEvent = (language, source) => {
    if (typeof window.gtag !== "function") {
      return;
    }

    window.gtag("event", "service_lead_submit", {
      form_name: "service_lead",
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

    const language = getLanguage(form);

    const text = translations[language] || translations.pl;

    const message = createMessageElement(form);

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

      if (!form.checkValidity()) {
        form.reportValidity();
        return;
      }

      clearMessage(message);

      const formData = new FormData(form);

      const payload = {
        fullName: getFormValue(formData, "fullName"),

        phone: getFormValue(formData, "phone"),

        city: getFormValue(formData, "city"),

        salonName: getFormValue(formData, "salonName"),

        deviceName: getFormValue(formData, "deviceName"),

        language: getFormValue(formData, "language") || language,

        source: getFormValue(formData, "source") || "website",

        pageUrl: window.location.href,
      };

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

      try {
        const response = await fetch(WEBHOOK_URL, {
          method: "POST",

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

        sendAnalyticsEvent(payload.language, payload.source);
      } catch (error) {
        /* -----------------------------------------------
             Error
          ----------------------------------------------- */

        console.error("Laser Tech Service lead form error:", error);

        showError(message, text.error);
      } finally {
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

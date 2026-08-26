/* =========================================================
   LASER TECH SERVICE
   MAIN.JS

   01. Language switcher
   02. Restore scroll position
   03. Dark mode
   04. FAQ
   05. Floating social menu
   06. Instagram animation
   07. Scroll animations
   08. Smooth anchor scroll
   09. Jarallax
   10. Legacy social button
   11. Contact form
   12. Devices carousel
========================================================= */


/* =========================================================
   01. LANGUAGE SWITCHER
========================================================= */

document.addEventListener("DOMContentLoaded", () => {

  const btnLang = document.querySelector(".dark-mode-btn");

  if (!btnLang) return;


  const path = window.location.pathname;

  const isRussian =
    path === "/ru/" ||
    path.startsWith("/ru/");


  if (isRussian) {
    btnLang.classList.add("dark-mode-btn--active");
  }


  btnLang.addEventListener("click", () => {

    localStorage.setItem(
      "scrollPosition",
      window.scrollY
    );


    let currentPath = window.location.pathname;

    let newPath;


    /* RU -> PL */

    if (isRussian) {

      newPath =
        currentPath.replace(/^\/ru/, "");

      if (
        newPath === "" ||
        newPath === "/index.html"
      ) {
        newPath = "/";
      }

    }

    /* PL -> RU */

    else {

      if (
        currentPath === "/" ||
        currentPath === "/index.html"
      ) {

        newPath = "/ru/";

      } else {

        newPath = "/ru" + currentPath;

      }

    }


    window.location.href =
      newPath +
      window.location.search +
      window.location.hash;

  });

});


/* =========================================================
   02. RESTORE SCROLL POSITION
========================================================= */

window.addEventListener("load", () => {

  const scrollPosition =
    localStorage.getItem("scrollPosition");


  if (!scrollPosition) return;


  const nav =
    document.querySelector(".nav");


  const navHeight =
    nav?.offsetHeight || 0;


  const position =
    Math.max(
      0,
      parseInt(scrollPosition, 10) - navHeight
    );


  window.scrollTo({
    top: position,
    left: 0,
    behavior: "smooth"
  });


  localStorage.removeItem(
    "scrollPosition"
  );

});


/* =========================================================
   03. DARK MODE

   Zostawiamy ciemny motyw włączony na stałe,
   tak jak w poprzedniej wersji.
========================================================= */

document.addEventListener("DOMContentLoaded", () => {

  document.body.classList.add("dark");

  localStorage.setItem(
    "darkMode",
    "dark"
  );

});


/* =========================================================
   04. FAQ
========================================================= */

document.addEventListener("DOMContentLoaded", () => {

  const faqItems =
    document.querySelectorAll(
      ".faq__item"
    );


  if (!faqItems.length) return;


  faqItems.forEach(item => {

    const button =
      item.querySelector(
        ".faq__question"
      );


    if (!button) return;


    button.addEventListener(
      "click",
      () => {

        /* zamykamy pozostałe */

        faqItems.forEach(otherItem => {

          if (otherItem !== item) {

            otherItem.classList.remove(
              "active"
            );

          }

        });


        /* otwieramy / zamykamy aktualny */

        item.classList.toggle(
          "active"
        );

      }
    );

  });

});


/* =========================================================
   05. FLOATING SOCIAL MENU
========================================================= */

document.addEventListener("DOMContentLoaded", () => {

  const trigger =
    document.querySelector(
      "menu > .trigger"
    );


  if (!trigger) return;


  trigger.addEventListener(
    "click",
    event => {

      const menu =
        event.currentTarget.parentElement;


      if (!menu) return;


      menu.classList.toggle(
        "open"
      );

    }
  );

});


/* =========================================================
   06. INSTAGRAM ANIMATION

   WAŻNE:
   Na stronie /uslugi nie ma .inst__sub.
   Dlatego MUSI być sprawdzenie if (instSection).
========================================================= */

document.addEventListener("DOMContentLoaded", () => {

  const instSection =
    document.querySelector(
      ".inst__sub"
    );


  if (!instSection) return;


  function showInstagramOnScroll() {

    const rect =
      instSection.getBoundingClientRect();


    if (
      rect.top <
      window.innerHeight - 100
    ) {

      instSection.classList.add(
        "visible"
      );


      window.removeEventListener(
        "scroll",
        showInstagramOnScroll
      );

    }

  }


  window.addEventListener(
    "scroll",
    showInstagramOnScroll,
    {
      passive: true
    }
  );


  showInstagramOnScroll();

});


/* =========================================================
   07. SCROLL ANIMATIONS
========================================================= */

document.addEventListener("DOMContentLoaded", () => {

  const animatedItems =
    document.querySelectorAll(
      ".scroll-animate"
    );


  if (!animatedItems.length) return;


  function handleScrollAnimation() {

    animatedItems.forEach(item => {

      const rect =
        item.getBoundingClientRect();


      if (
        rect.top <
        window.innerHeight - 80
      ) {

        item.classList.add(
          "visible"
        );

      }

    });

  }


  window.addEventListener(
    "scroll",
    handleScrollAnimation,
    {
      passive: true
    }
  );


  /* bardzo ważne:
     uruchamiamy od razu po załadowaniu strony */

  handleScrollAnimation();

});


/* =========================================================
   08. SMOOTH ANCHOR SCROLL

   Poprawiony selektor:
   było:
   a[href^="#"

   jest:
   a[href^="#"]
========================================================= */

document.addEventListener("DOMContentLoaded", () => {

  const anchorLinks =
    document.querySelectorAll(
      'a[href^="#"]'
    );


  anchorLinks.forEach(link => {

    link.addEventListener(
      "click",
      function(event) {

        const href =
          this.getAttribute("href");


        if (
          !href ||
          href === "#"
        ) {
          return;
        }


        const target =
          document.querySelector(
            href
          );


        if (!target) {
          return;
        }


        event.preventDefault();


        const navHeight =
          document.querySelector(
            ".nav"
          )?.offsetHeight || 0;


        const targetPosition =
          target
            .getBoundingClientRect()
            .top +
          window.scrollY -
          navHeight -
          10;


        window.scrollTo({

          top: targetPosition,

          behavior: "smooth"

        });

      }
    );

  });

});


/* =========================================================
   09. JARALLAX
========================================================= */

document.addEventListener("DOMContentLoaded", () => {

  const jarallaxElements =
    document.querySelectorAll(
      ".jarallax"
    );


  if (!jarallaxElements.length) {
    return;
  }


  if (
    typeof jarallax !==
    "function"
  ) {
    return;
  }


  jarallax(
    jarallaxElements
  );

});


/* =========================================================
   10. LEGACY SOCIAL BUTTON

   Ten blok zostawiamy tylko dla kompatybilności
   ze starym HTML, jeśli gdzieś jeszcze istnieje.
========================================================= */

document.addEventListener("DOMContentLoaded", () => {

  const mainButton =
    document.getElementById(
      "main-button"
    );


  if (!mainButton) return;


  mainButton.addEventListener(
    "click",
    () => {

      const socialButtons =
        document.querySelector(
          ".social-buttons"
        );


      if (!socialButtons) return;


      socialButtons.classList.toggle(
        "show"
      );

    }
  );

});


/* =========================================================
   11. CONTACT FORM
========================================================= */

document.addEventListener("DOMContentLoaded", () => {

  const phoneInput =
    document.getElementById(
      "phone"
    );


  const contactForm =
    document.getElementById(
      "contactForm"
    );


  const customSelect =
    document.getElementById(
      "equipmentSelect"
    );


  /*
     Na stronie bez formularza
     cały blok po prostu się nie uruchamia.
  */

  if (
    !phoneInput ||
    !contactForm ||
    !customSelect
  ) {
    return;
  }


  const selected =
    customSelect.querySelector(
      ".select-selected"
    );


  const items =
    customSelect.querySelector(
      ".select-items"
    );


  const equipmentInput =
    document.getElementById(
      "equipmentInput"
    );


  const successMessage =
    document.getElementById(
      "successMsg"
    );


  /* -----------------------------------------
     PHONE +48
  ----------------------------------------- */

  phoneInput.addEventListener(
    "focus",
    () => {

      if (
        !phoneInput.value.startsWith(
          "+48"
        )
      ) {

        phoneInput.value =
          "+48 ";

      }


      setTimeout(() => {

        const length =
          phoneInput.value.length;


        phoneInput.setSelectionRange(
          length,
          length
        );

      }, 0);

    }
  );


  phoneInput.addEventListener(
    "input",
    () => {

      let value =
        phoneInput.value
          .replace(/\s+/g, "");


      if (
        !value.startsWith(
          "+48"
        )
      ) {

        value = "+48";

      }


      let digits =
        value
          .slice(3)
          .replace(/\D/g, "");


      digits =
        digits.slice(0, 9);


      const formattedDigits =
        digits
          .replace(
            /(\d{3})(?=\d)/g,
            "$1 "
          );


      phoneInput.value =
        "+48 " +
        formattedDigits;

    }
  );


  /* -----------------------------------------
     CUSTOM SELECT
  ----------------------------------------- */

  if (
    selected &&
    items
  ) {

    selected.addEventListener(
      "click",
      event => {

        event.stopPropagation();


        items.classList.toggle(
          "show"
        );


        selected.classList.toggle(
          "active"
        );

      }
    );


    items
      .querySelectorAll("div")
      .forEach(option => {

        option.addEventListener(
          "click",
          event => {

            event.stopPropagation();


            const value =
              option.textContent.trim();


            selected.textContent =
              value;


            if (equipmentInput) {

              equipmentInput.value =
                value;

            }


            items.classList.remove(
              "show"
            );


            selected.classList.remove(
              "active"
            );

          }
        );

      });


    document.addEventListener(
      "click",
      event => {

        if (
          !customSelect.contains(
            event.target
          )
        ) {

          items.classList.remove(
            "show"
          );


          selected.classList.remove(
            "active"
          );

        }

      }
    );

  }


  /* -----------------------------------------
     TELEGRAM SETTINGS

     WSTAW TU SWÓJ TOKEN I CHAT ID
     ZE STAREGO main.js
  ----------------------------------------- */

  const TELEGRAM_BOT_TOKEN =
    "WSTAW_TUTAJ_SWÓJ_TOKEN";


  const TELEGRAM_CHAT_ID =
    "WSTAW_TUTAJ_CHAT_ID";


  /* -----------------------------------------
     FORM SUBMIT
  ----------------------------------------- */

  contactForm.addEventListener(
    "submit",
    async function(event) {

      event.preventDefault();


      const name =
        this.elements.name
          ?.value
          .trim() || "";


      const phone =
        this.elements.phone
          ?.value
          .trim() || "";


      const consent =
        Boolean(
          this.elements.consent
            ?.checked
        );


      let equipment = "";


      if (
        equipmentInput &&
        equipmentInput.value
      ) {

        equipment =
          equipmentInput.value.trim();

      }

      else if (selected) {

        const selectedText =
          selected
            .textContent
            .trim();


        if (
          selectedText !==
          "Wybierz urządzenie"
        ) {

          equipment =
            selectedText;

        }

      }


      /* VALIDATION */

      if (!name) {

        alert(
          "Wpisz imię."
        );

        return;

      }


      if (!phone) {

        alert(
          "Wpisz numer telefonu."
        );

        return;

      }


      if (!equipment) {

        alert(
          "Musisz wybrać urządzenie!"
        );

        return;

      }


      if (!consent) {

        alert(
          "Musisz wyrazić zgodę na przetwarzanie danych!"
        );

        return;

      }


      const now =
        new Date();


      const date =
        now.toLocaleDateString(
          "pl-PL"
        );


      const time =
        now.toLocaleTimeString(
          "pl-PL",
          {
            hour: "2-digit",
            minute: "2-digit"
          }
        );


      const message =
`Nowe zgłoszenie serwisowe

Imię: ${name}
Telefon: ${phone}
Urządzenie: ${equipment}
Data / czas: ${date} ${time}`;


      try {

        const response =
          await fetch(
            `https://api.telegram.org/bot${TELEGRAM_BOT_TOKEN}/sendMessage`,
            {

              method: "POST",

              headers: {
                "Content-Type":
                  "application/json"
              },

              body:
                JSON.stringify({

                  chat_id:
                    TELEGRAM_CHAT_ID,

                  text:
                    message

                })

            }
          );


        const result =
          await response.json();


        if (
          !response.ok ||
          result.ok === false
        ) {

          throw new Error(
            "Telegram API error"
          );

        }


        /* SUCCESS */

        if (successMessage) {

          successMessage.classList.add(
            "show"
          );

        }


        this.reset();


        phoneInput.value =
          "+48 ";


        if (selected) {

          selected.textContent =
            "Wybierz urządzenie";

        }


        if (equipmentInput) {

          equipmentInput.value =
            "";

        }

      }

      catch (error) {

        console.error(
          "Form submit error:",
          error
        );


        alert(
          "Błąd podczas wysyłania formularza. Spróbuj ponownie lub skontaktuj się z nami telefonicznie."
        );

      }

    }
  );

});


/* =========================================================
   12. DEVICES CAROUSEL
========================================================= */

document.addEventListener("DOMContentLoaded", () => {

  const track =
    document.getElementById(
      "carouselTrack"
    );


  /*
     Na /uslugi i /kontakt karuzeli może nie być.
     Jeśli jej nie ma — nic nie robimy.
  */

  if (!track) return;


  /*
     Klonujemy elementy
     dla efektu nieskończonej karuzeli.
  */

  track.innerHTML +=
    track.innerHTML;


  let position = 0;

  const speed = 0.3;


  let isDragging = false;

  let startX = 0;

  let startPosition = 0;


  /* -----------------------------------------
     AUTO MOVEMENT
  ----------------------------------------- */

  function animateCarousel() {

    if (!isDragging) {

      position -= speed;


      if (
        Math.abs(position) >=
        track.scrollWidth / 2
      ) {

        position = 0;

      }

    }


    track.style.transform =
      `translateX(${position}px)`;


    requestAnimationFrame(
      animateCarousel
    );

  }


  animateCarousel();


  /* -----------------------------------------
     MOUSE DRAG
  ----------------------------------------- */

  track.addEventListener(
    "mousedown",
    event => {

      isDragging = true;


      startX =
        event.clientX;


      startPosition =
        position;

    }
  );


  window.addEventListener(
    "mouseup",
    () => {

      isDragging = false;

    }
  );


  window.addEventListener(
    "mousemove",
    event => {

      if (!isDragging) {
        return;
      }


      const distance =
        event.clientX -
        startX;


      position =
        startPosition +
        distance;

    }
  );


  /* -----------------------------------------
     TOUCH
  ----------------------------------------- */

  track.addEventListener(
    "touchstart",
    event => {

      if (
        !event.touches.length
      ) {
        return;
      }


      isDragging = true;


      startX =
        event.touches[0].clientX;


      startPosition =
        position;

    },
    {
      passive: true
    }
  );


  window.addEventListener(
    "touchend",
    () => {

      isDragging = false;

    },
    {
      passive: true
    }
  );


  window.addEventListener(
    "touchmove",
    event => {

      if (
        !isDragging ||
        !event.touches.length
      ) {
        return;
      }


      const distance =
        event.touches[0].clientX -
        startX;


      position =
        startPosition +
        distance;

    },
    {
      passive: true
    }
  );


  /* -----------------------------------------
     MOUSE WHEEL
  ----------------------------------------- */

  track.addEventListener(
    "wheel",
    event => {

      event.preventDefault();


      position -=
        event.deltaY * 0.5;

    },
    {
      passive: false
    }
  );

});
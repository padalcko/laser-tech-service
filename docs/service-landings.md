# Service landing pages

HTML remains canonical. The first pair is `/uslugi/diagnostyka-laserow-diodowych/` and `/ru/uslugi/diagnostika-diodnyh-lazerov/`. Only this service is implemented.

## Reusing the pattern

1. Copy the appropriate locale's diagnostic HTML into the new service route. Keep current localized navigation, footer, social controls, installed analytics and existing form handling. Update the language switcher as well as head alternates.
2. Replace the eight content blocks with approved service facts: hero, scope, symptoms, process, cost, cases, FAQ and request form. Replace all names, titles, descriptions, canonical URLs, breadcrumbs, Service IDs and form serviceType/source. Never inherit diode pricing for an unrelated service. Review the actual service scope and each technical claim.
3. Reuse `main.css`, `cennik.css` and the existing form component in `blog.css`; landing-specific styles live under `.service-landing` in `service-landing.css`. Keep additions scoped. Shared navigation/FAQ/social behavior remains in `main.js`.
4. Add an entry to `scripts/service-cases.json`: locale landing routes, actual locale case URLs, existing image attributes and factual locale title/symptom/cause/result summaries. Source each fact from the referenced case HTML. The cooling-fan example does **not** establish diode technology.
5. Run `python3 scripts/build-service-cases.py`. It updates only the marked case block and Service `subjectOf` relationships. Do not manually edit the generated case cards. Future case additions require one JSON entry, not copied HTML cards. Run `--check` to detect drift.
6. Add the reciprocal pair to `sitemap.xml` and appropriate contextual links in the catalog, price list, relevant cases and articles. Preserve other URL destinations.
7. Run the existing AI build and checks below. Never hand-edit generated Markdown, llms files, discovery links or headers.
8. Validate both locales at narrow mobile and desktop widths, keyboard FAQ/navigation, no-JS text, all links and form requests using a mocked webhook. Review the actual rendered page.

```sh
python3 scripts/build-service-cases.py
python3 scripts/build-service-cases.py --check
python3 scripts/build-ai-search.py
python3 scripts/build-ai-search.py --check
python3 scripts/check-ai-search.py
python3 scripts/check-geo-seo.py
git diff --check
```

## Lead form and analytics

The same `.article-service-form__form` and `js/service-lead-form.js` post to the existing n8n endpoint. Existing payload fields are unchanged. Landing forms optionally add `serviceType` and `problemDescription`; the device model is optional. `source` identifies service and locale. Consent uses the existing contact-page wording and required native checkbox. The optional `companyWebsite` honeypot rejects nonempty submissions locally; it is not a server-side anti-spam guarantee. Existing native validation, request timeout, double-submit protection and translated success/error handling are retained.

`service_lead_submit` remains the existing event and runs only after HTTP success plus JSON `success: true`. `service-landing.js` uses the installed `gtag` function for `service_cta_click` and `service_phone_click`; parameters are fixed service type, locale and source, never form values. Each click is handled once by this script. No new GA/GTM loader was added. The site's existing GA4, Ads and two GTM container configuration is inherited unchanged. Published remote GTM rules and possible overlap within those containers cannot be audited from this repository.

A successful mocked test proves the browser payload and UI behavior. It does not prove downstream n8n field mapping, storage, notifications or production GA delivery. Verify those independently with access to the existing integration before relying on production reporting.

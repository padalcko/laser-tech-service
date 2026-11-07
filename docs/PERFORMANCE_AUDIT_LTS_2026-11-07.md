# Mobile Performance Audit — Laser Tech Service

Date: 2026-11-07  
Scope: repository-wide static inspection plus limited observations of
`https://lasertechservice.pl/` in the integrated browser.  
Change policy: no website code, content, SEO metadata, URLs, analytics, consent
settings, or design were changed. This file is internal documentation.

## Executive summary

The supplied PageSpeed Insights result is poor on mobile: Performance 58,
TBT 3,480 ms, LCP 3.2 s, and Speed Index 5.8 s. The repository does not contain
the PSI JSON, Chrome trace, or an attribution report for that run. Consequently,
the exact function or third-party script responsible for the 3,480 ms TBT
**cannot be established from the supplied score or static source alone**.

The most important evidence is a mismatch between the tracked source and the
live production runtime:

1. The source includes both GTM containers `GTM-PT7BMHKW` and `GTM-MF33VG4R`,
   alongside direct GA4 `G-6QFRWP5RX5` and Google Ads `AW-17614450660`
   initialization on most pages.
2. Neither CookieYes nor GA4 `G-5STE4YVSDH` is present in tracked HTML/JS, but
   the production browser loaded CookieYes and sent requests for `G-5STE4YVSDH`,
   `AW-18029703708`, and `G-B0BZTGSE4X`. This is consistent with remotely
   configured GTM tags, but the container configurations were not accessible
   for inspection.
3. This creates a strong, evidence-based reason to investigate duplicate and
   unnecessary third-party execution first. It does **not** prove that those
   tags account for 3,480 ms or that conversions are duplicated.
4. The shared `main.js` downloads Lazar's 22.7 KB script and 8.9 KB stylesheet
   at `DOMContentLoaded` on every page where `main.js` is present, before the
   user opens the assistant. This is unnecessary pre-interaction work and a
   credible optimization opportunity; its individual TBT contribution has not
   been measured.
5. Montserrat's external stylesheet is a render-blocking stylesheet in the
   `<head>` on all 262 tracked HTML files. The homepage LCP image is correctly
   preloaded and has high fetch priority; the browser identified it as the
   `header.header` background. The sample does not support changing or lazy
   loading that image.

**Conclusion:** the 3,480 ms TBT is not yet attributable to a particular script.
The next step should be a throttled Chrome Performance trace with task
attribution and controlled GTM/CookieYes consent states, before any code or tag
configuration is changed.

## 1. Supplied PageSpeed Insights results

These are user-provided figures; the PSI URL, report JSON, test date, and trace
were not supplied.

| Metric | Supplied mobile result | Target |
|---|---:|---:|
| Performance | 58/100 | 90+ |
| Accessibility | 94/100 | — |
| Best Practices | 100/100 | — |
| SEO | 100/100 | — |
| FCP | 1.7 s | ≤ 1.8 s |
| LCP | 3.2 s | ≤ 2.5 s |
| TBT | 3,480 ms | < 200 ms |
| Speed Index | 5.8 s | — |
| CLS | 0 | ≤ 0.1 |
| INP | Not supplied | ≤ 200 ms field data |

Lab TBT and field INP are different metrics. No CrUX/field INP data was
available in the repository or supplied with the PSI figures.

## 2. Repository and measurement scope

The static scan covered **262 Git-tracked HTML files**, including the 404 page,
all tracked CSS and JavaScript files, script/style references, identifiers,
iframes, and the Netlify build/deploy configuration. It did not treat the
generated, ignored `dist/` copy as a second source tree.

Tracked JavaScript/CSS inventory:

| File | Source size |
|---|---:|
| [`js/main.js`](../js/main.js) | 17,043 B |
| [`js/lazar-ai.js`](../js/lazar-ai.js) | 22,656 B |
| [`js/service-lead-form.js`](../js/service-lead-form.js) | 11,687 B |
| [`js/error-404.js`](../js/error-404.js) | 5,336 B |
| [`js/cennik.js`](../js/cennik.js) | 2,395 B |
| [`js/case-gallery.js`](../js/case-gallery.js) | 1,924 B |
| [`js/service-landing.js`](../js/service-landing.js) | 876 B |
| [`css/main.css`](../css/main.css) | 61,593 B |
| [`css/realizacje.css`](../css/realizacje.css) | 30,327 B |
| [`css/blog.css`](../css/blog.css) | 22,224 B |
| [`css/lazar-ai.css`](../css/lazar-ai.css) | 8,898 B |

Static HTML includes 568 `application/ld+json` blocks, one
`application/json` block, and 1,001 classic inline script blocks. There are no
JavaScript module script tags. JSON-LD blocks are data, not executable
JavaScript; the count is not an estimate of CPU time.

### Limited live browser observations

The integrated browser was used at a 390×844 CSS-pixel viewport, without
configured CPU or network throttling. These are **not Lighthouse results** and
are not directly comparable with the supplied PSI run. The browser context may
reuse network/cache state.

Three homepage navigations exposed the LCP candidate and resource timing:

| Run | TTFB | FCP | LCP | LCP image request start → end | Approx. LCP phase timing |
|---|---:|---:|---:|---:|---|
| 1 | 105 ms | 276 ms | 276 ms | 114 → 156 ms | TTFB 105; resource delay 9; load 42; render delay 120 |
| 2 | 35 ms | 268 ms | 268 ms | 45 → 90 ms | TTFB 35; resource delay 10; load 45; render delay 178 |
| 3 | 37 ms | 216 ms | 216 ms | 48 → 95 ms | TTFB 37; resource delay 11; load 47; render delay 121 |

These rough phases are derived from browser Navigation/Resource Timing and the
observed LCP entry; they are not a PSI trace. In all three samples the LCP
candidate was the `HEADER.header` using
`/img/urzadzenia-laserowe-w-gabinecie.webp`. The browser sample recorded CLS 0.
Homepage DOM size was 674–675 elements.

One non-throttled RU sample reported four Long Tasks of 54, 51, 67, and 76 ms;
one EN sample reported two of 119 and 76 ms. The Long Task API returned no
script/function attribution (`name: unknown`, window container). Three
homepage observations in a separate sample reported Long Tasks of 55, 85, and
65 ms, all before that sample's FCP. These observations neither reproduce the
PSI TBT nor identify a culprit.

## 3. Top 10 findings

| # | Priority | Finding and evidence | Likely metric effect | Status |
|---:|---|---|---|---|
| 1 | P1 | Two GTM containers coexist with direct GA4/Ads setup on most pages; live requests show additional tags and duplicate tag-loader requests. See [production tag evidence](#6-third-party-scripts-analytics-and-ads). | Potentially high TBT and network contention; exact cost unknown. | Confirmed configuration overlap; container purpose and CPU cost unverified. |
| 2 | P1 | Live CookieYes loader and banner are absent from tracked source and appear in production. Google requests were observed with denied-state signals. See [CookieYes](#7-cookieyes-and-consent). | Possible TBT and FCP/LCP network/CPU cost; exact execution cost unknown. | Runtime presence confirmed; container configuration and consent ordering need inspection. |
| 3 | P1 | Lazar JS/CSS is fetched at `DOMContentLoaded`, rather than when the assistant is opened. See [`main.js`](../js/main.js#L540). | Avoidable JS download/parse/execute and style work on initial load; TBT contribution unmeasured. | Confirmed from source and browser request timing. |
| 4 | P1 | Google Fonts stylesheet is render-blocking in `<head>` on all 262 tracked HTML files. See [homepage head](../index.html#L13). | FCP/LCP and Speed Index, particularly on slow connections. | Confirmed source behavior; font-specific delay not isolated. |
| 5 | P1 | Static and image responses use `Cache-Control: public, max-age=0, must-revalidate`; ETags are present but repeated visits still require validation. | Repeat-visit LCP/FCP and transfer latency. | Confirmed on production for HTML, JS, CSS, image, and text samples. |
| 6 | P2 | `main.js` is a classic non-deferred script at the end of 261 pages; the homepage alone has `defer`. | Parser/DOMContentLoaded delay and startup work; likely modest per file, not measured. | Confirmed source placement. |
| 7 | P2 | Scroll animation handler reads every `.scroll-animate` geometry on each scroll event and mutates classes during the same loop. See [`main.js`](../js/main.js#L348). | Scroll-time main-thread work and possible repeated style/layout work; not evidence for initial TBT. | Static risk only. |
| 8 | P2 | Jarallax is loaded from jsDelivr on six localized homepage files, including mobile, although it is used only for the parallax section. | Third-party download/parse and possible scroll/render work. | Confirmed source; no isolated CPU measurement. |
| 9 | P2 | A separate intl-tel-input stylesheet from cdnjs is linked on five pages. | Render-blocking delay on those pages if the CDN is slow. | Confirmed source; no per-page waterfall comparison. |
| 10 | P2 | Several shared styles include blur, backdrop-filter, shadows, and continuous decorative animation; homepage DOM is ~675 elements. | Potential paint/compositing cost, especially on low-end mobile. | Static indicators only; no paint trace or CSS coverage. |

No P0 issue was established. Finding priority is an investigation/implementation
order, not a claim that a particular finding caused a known number of
milliseconds.

## 4. JavaScript execution analysis

### Script-loading frequency

Counts are occurrences across the 262 tracked HTML files, not runtime CPU
measurements.

| Script | Occurrences | Loading mode / notes |
|---|---:|---|
| `/js/main.js` | 262 | 261 classic, non-deferred end-of-body scripts; homepage is deferred. |
| `gtag.js?id=G-6QFRWP5RX5` | 251 | `async` on most pages; homepage inserts it after FCP. |
| `gtag.js?id=AW-17614450660` | 251 | Same pattern as GA4. |
| `/js/service-lead-form.js` | 57 | 49 deferred, 8 classic end-of-body. |
| `/js/service-landing.js` | 48 | Deferred. |
| `/js/case-gallery.js` | 42 | Classic end-of-body. |
| Jarallax CDN script | 6 | Three async and three classic occurrences. |
| `/js/cennik.js` | 3 | Deferred. |
| `/js/error-404.js` | 1 | 404-only. |

The seven local scripts are small compared with the supplied TBT, but source
size alone cannot rule out expensive execution or mobile CPU slowdown. No local
bundler/dependency manifest was found in the tracked top-level project setup.
There is no source-level evidence of a duplicated local library. Duplicate
Google tag initialization is a separate, confirmed configuration concern.

`main.js` has several `DOMContentLoaded` initializers for navigation, FAQ,
dropdowns, scroll effects, and the carousel. Each HTML page loads the script
once; the scan did not establish repeated execution on the same document.
`carouselTrack` has a `data-carousel-ready` guard.

### DOM/layout work

`handleScrollAnimation()` loops over every `.scroll-animate` node on each scroll,
calls `getBoundingClientRect()`, then may add a class before measuring the next
node. This can create repeated style/layout work while scrolling; it is not a
load-time Long Task finding. The Instagram scroll listener measures one
section and removes itself after it becomes visible.

No `MutationObserver` or `ResizeObserver` appears in the shared site scripts.
The only MutationObservers found are in the 404-only [`error-404.js`](../js/error-404.js#L27)
and observe a small menu subtree/attributes. `setInterval` was not found.
Timers in the form and chat scripts are request timeouts, not polling loops.

## 5. Main Thread Blocking Analysis

### What is confirmed

- The supplied 3,480 ms value is an aggregate PSI TBT result. There is no
  trace, task list, or attribution in the repository.
- Production loads multiple third-party tag runtimes after/alongside local
  scripts. Their JavaScript can contribute Long Tasks, but this audit did not
  collect a DevTools trace with URL/function stacks.
- The integrated-browser Long Task API saw several 51–119 ms tasks in one
  RU/EN sample, but reported no owner. The non-throttled homepage sample did
  not show a corresponding post-FCP Long Task. This indicates environment
  sensitivity, not that Lighthouse is wrong.
- `async` external scripts do not block HTML parsing, but their execution still
  uses the main thread. A remote GTM can also load further scripts.

### What is not confirmed

No script/function can responsibly be assigned “3,480 ms” or a specific share
of it from this evidence. In particular, the audit does not claim that
CookieYes, either GTM container, Lazar, or `main.js` alone caused the result.
Long Task durations from an unthrottled browser are not Lighthouse TBT.

### Required trace to establish causality

Capture a Lighthouse mobile trace with the same PSI URL and throttling profile,
then inspect the Main thread from FCP through TTI/TBT for `Evaluate Script`,
`Function Call`, `Compile Script`, and third-party tasks. Repeat with:

1. baseline production with a fresh consent state;
2. baseline after accepting each consent category;
3. a controlled GTM Preview session that identifies tags fired by each
   container;
4. a comparison run with duplicate tags temporarily prevented in an approved
   staging environment, never by disabling production Ads/analytics first.

Keep the trace, PSI JSON, browser/version, network profile, viewport, and
consent-state record with each run.

## 6. Third-party scripts, analytics, and Ads

### Tracked source

| ID / service | In tracked source | Notes |
|---|---|---|
| GA4 `G-6QFRWP5RX5` | 251 HTML files | Direct `gtag.js` and `config` calls. |
| GA4 `G-5STE4YVSDH` | 0 files | Not present in tracked source. |
| Google Ads `AW-17614450660` | 251 HTML files | Direct `gtag.js` and `config` calls. |
| GTM `GTM-PT7BMHKW` | 236 HTML files | Commented as “OLD”; still initialized. |
| GTM `GTM-MF33VG4R` | 258 HTML files | Also initialized on most pages. |

On the homepage the inline wrappers defer the direct GA/Ads loaders and both
GTM bootstraps until after FCP ([`index.html`](../index.html#L254),
[`index.html`](../index.html#L278)). This wrapper is not present in the same
form on the RU/EN homepages and ordinary pages: their GA/Ads scripts are async
in the head and the GTM bootstraps run there
([`ru/index.html`](../ru/index.html#L249),
[`en/index.html`](../en/index.html#L245),
[`uslugi/serwis-dla-sieci-salonow/index.html`](../uslugi/serwis-dla-sieci-salonow/index.html#L86)).
Thus, first-party load behavior is not uniform across locales/routes.

### Live production observation

The production homepage loaded both GTM containers and the direct IDs above.
The browser also observed:

- `G-6QFRWP5RX5` and `AW-17614450660` loader requests with GTM query parameters
  in addition to the direct loader requests;
- GA request/beacon activity for `G-5STE4YVSDH` and `G-B0BZTGSE4X`;
- Ads activity for `AW-18029703708` as well as `AW-17614450660`;
- CookieYes resources from `cdn-cookieyes.com`.

The extra IDs and CookieYes are not in tracked source. A remote GTM container
is a plausible origin, but the actual container contents, firing rules,
ownership, and conversion semantics were not accessible. Do not remove any
identifier or container until a GTM Preview/GA4/Ads audit verifies which
container owns each event. The observed repeated tag loads are not, on their
own, proof of duplicate conversions.

### Other external resources

- Google Fonts stylesheet: all 262 tracked HTML pages.
- intl-tel-input stylesheet from cdnjs: five pages.
- Jarallax 1.12.1 from jsDelivr: six homepage variants.
- Third-party iframes in source: 72 YouTube and six Google Maps frames; all 78
  have `loading="lazy"` in the scan. They were not observed as eager homepage
  startup requests.
- No other social JavaScript SDK was found in tracked HTML. Social destinations
  are links.
- Service lead forms and Lazar contact backend use n8n endpoints only when a
  user submits/sends; do not preload or preconnect to these endpoints without
  separate privacy/behavior review.

## 7. CookieYes and consent

CookieYes has no tracked HTML, JavaScript, or JSON implementation in this
repository. On the sampled production visit:

- The CookieYes consent banner was visible.
- The browser loaded `cdn-cookieyes.com` client/banner/configuration resources
  and `log.cookieyes.com`.
- Google Analytics requests contained `gcs=G100` and `npa=1`, consistent with
  denied consent signals in those observed requests.

This confirms runtime loading and a denied-state signal, not the complete
Consent Mode configuration, category mapping, or absence of all pre-consent
storage. Cross-origin Resource Timing did not expose reliable transfer sizes
or script CPU attribution. The browser session did not run a controlled
accept/reject matrix.

CookieYes must not simply be delayed until a click if it is responsible for
setting the default consent state. First verify the ordering between default
consent, CookieYes initialization, GTM, and each tag. Then, if supported by
the approved consent design, keep the consent bootstrap early and defer
non-essential tag work until the consent signal. Test denied, accepted,
rejected, and returning-user paths, including forms, Ads conversion behavior,
and all locales.

## 8. Lazar assistant

`main.js` appends `/css/lazar-ai.css` and async `/js/lazar-ai.js` at
`DOMContentLoaded` ([`main.js`](../js/main.js#L540)). It does not wait for the
launcher or mobile bottom-bar button to be pressed. In the mobile browser
sample, both local requests began at approximately DOMContentLoaded.

The assistant entry point is shared rather than triplicated by locale. It
selects PL/RU/EN from `document.documentElement.lang`, creates the launcher,
chat panel, quick questions, mobile contact bar, and event handlers. Its API
endpoint is contacted on message send, not during the initial page request.
The current UI therefore has no chat-backend request before interaction, but
does pay the local JS/CSS initialization cost on initial load.

Recommended future design, subject to approval:

1. Keep a lightweight, accessible launcher and mobile bar visible in all
   locales.
2. Load the chat implementation/styles on first open, then mount once.
3. Preserve the existing PL/RU/EN strings, routes, disabled-English page
   behavior, focus handling, keyboard/visual viewport behavior, retry state,
   event names, and phone/WhatsApp links.
4. Verify no CSS/JS/backend request occurs before first assistant interaction
   except the minimum launcher resources that the design explicitly requires.

Potential DOM append and `log.scrollHeight` layout reads in
[`lazar-ai.js`](../js/lazar-ai.js#L223) occur when messages are added. This is
interaction-time work; no trace identified it as an initial-load blocker.

## 9. Carousel, animation, and observers

The devices carousel has a continuous `requestAnimationFrame` loop only while
visible, on a non-mobile viewport, with reduced motion disabled, tab visible,
and no drag in progress. The same loop is stopped when those conditions cease
([`main.js`](../js/main.js#L453)). CSS hides the carousel at `max-width: 767px`
([`main.css`](../css/main.css#L1062)); JavaScript's mobile breakpoint also
prevents the RAF loop. This is not a confirmed mobile auto-scrolling cause.

The main stylesheet has scroll reveal transitions, blurred decorative
backgrounds, `backdrop-filter`, shadows, and a pulse animation. Lazar has a
five-second infinite glow animation. These may add paint/compositing cost on
low-end devices, but no paint trace or CSS coverage was available. Do not
change the animation design without visual and reduced-motion review.

The scroll reveal handler is the clearest local animation-related code
opportunity: replace per-scroll full-list geometry reads with an
`IntersectionObserver` or a scheduled, read-before-write update, while
preserving reveal timing and reduced-motion behavior. The 404 page has
observers, but they are not loaded on ordinary pages.

## 10. LCP and critical rendering path

### LCP element and image

In the three browser observations, LCP was `HEADER.header` backed by
`/img/urzadzenia-laserowe-w-gabinecie.webp`. The image is preloaded with
`fetchpriority="high"` in the homepage head
([`index.html`](../index.html#L12)); CSS uses the same asset as the header
background ([`main.css`](../css/main.css#L832)). The preload is appropriate.
Do **not** lazy-load it.

The production response size reported for this WebP was 66,136 bytes. In the
unthrottled observations the resource started about 9–11 ms after TTFB and took
42–47 ms to complete; the remaining LCP delay varied from 120 to 178 ms in
these samples. This does not explain the supplied 3.2 s mobile LCP; throttled
PSI waterfall/trace data is needed to determine whether production mobile
delay comes from network, server, font/style, tag execution, or paint.

### Render-blocking and first screen

- Montserrat CSS is a stylesheet link in the head on all tracked pages. The
  `display=swap` option and preconnects help, but the external stylesheet still
  participates in the render-blocking CSS path.
- Local reset and main stylesheets are also head-loaded on every page, as
  expected for the current site structure.
- Third-party scripts are `async` or dynamically inserted, not parser-blocking
  classic head scripts. Their execution can still interrupt the main thread.
- No trace isolated cookie-banner layout shift or animation impact. Browser
  sample CLS was 0; this is not field CLS evidence.

## 11. CSS and DOM

Stylesheet usage across tracked HTML:

| Stylesheet | Pages |
|---|---:|
| `css/reset.css` | 262 |
| `css/main.css` | 262 |
| Google Fonts stylesheet | 262 |
| `css/blog.css` | 147 |
| `css/realizacje.css` | 105 |
| `css/cennik.css` | 51 |
| `css/service-landing.css` | 48 |
| `css/case-gallery.css` | 45 |
| `css/about.css` | 3 |
| `css/partnerzy.css` | 3 |
| intl-tel-input stylesheet | 5 |

The two common local CSS files are not minified in the source tree, but
production served `css/main.css` with gzip when requested with compression
support. No CSS coverage or unused-selector report was available; unused CSS
must not be asserted from file size alone.

The live homepage had approximately 674–675 DOM elements. This is measurable,
but not evidence that DOM size alone causes the supplied TBT. Blur and
backdrop-filter effects are candidates for low-end GPU/paint testing, not
confirmed regressions. Use Chrome Rendering/Performance paint profiling and
compare visual output before changing styles.

## 12. Netlify, caching, and publication

The current repository config runs the site build and package step, publishing
`dist` ([`netlify.toml`](../netlify.toml#L1)). The packaging script excludes
`docs/`, `reports/`, `scripts/`, `content/`, and root audit files
([`package-site.py`](../scripts/package-site.py#L9)). This report is under
`docs/` and is outside the configured public bundle. The existing ignored
`dist/` did not contain `docs/` or this report at audit time.

Production checks returned HTTP 200 and ETags for representative HTML, JS,
CSS, image, and `llms.txt` resources. Their sampled cache policy was
`public, max-age=0, must-revalidate`. A compressed request for `css/main.css`
returned `Content-Encoding: gzip`; compression is therefore active for that
sample. There is no evidence here of a Brotli response.

The current max-age policy causes revalidation of static assets on repeat
visits. Since public filenames are not content-hashed, immutable caching must
not be applied blindly. A safe future cache policy should distinguish HTML
from versioned/static assets and include a deployment/cache-busting strategy.
This likely helps repeat visits more than first-visit TBT.

The sampled Netlify response did not reveal a redirect chain for the tested
root/assets. A full crawl of all redirects and route variants was not part of
the browser measurement. Keep redirects and sitemap/canonical behavior
unchanged during any performance-only work.

## 13. Prioritized work table

| Priority | Work item | Expected direction (not a measured promise) | Risk | Verification |
|---|---|---|---|---|
| P1 | Audit both GTM containers and map each GA4/Ads ID/event to one source. Remove nothing until owner approves. | Potentially largest reduction in third-party execution/TBT and network work. Milliseconds unknown. | Lost analytics/conversions if ownership or event dependencies are misunderstood. | GTM Preview, GA4 DebugView, Ads diagnostics, trace before/after, consent matrix. |
| P1 | Verify CookieYes/default-consent ordering and which tags fire before consent. | May reduce pre-consent work while preserving consent; performance gain unquantified. | Consent violation, missing conversions, incorrect banner behavior. | Fresh profile tests: deny/accept/reject/returning, inspect requests/cookies/consent signals. |
| P1 | Load Lazar implementation/styles on first launcher interaction instead of at DOMContentLoaded. | Removes assistant parse/style/DOM startup work from initial page; exact TBT savings unknown. | Broken launcher, language, keyboard, mobile bar, or chat. | PL/RU/EN, mobile and desktop, keyboard/focus, chat success/failure, network panel before/after click. |
| P1 | Measure and optimize Google Fonts critical path while preserving Montserrat appearance. | Potential FCP/LCP improvement on slow networks; no numeric estimate. | Font flash, wrong weights, layout change, text wrapping/CLS. | Font request waterfall, visual screenshots, text metrics and CLS across locales. |
| P1 | Set a deliberate static-asset cache policy with safe cache busting. | Better repeat-visit resource load time; little direct first-visit TBT effect. | Stale CSS/JS/image after deploy. | Verify response headers, deploy two versions, test cache refresh and rollback. |
| P2 | Normalize local scripts to deferred/route-scoped loading where safe. | Smaller parser/startup cost on pages not using a feature; unmeasured. | Initialization order and form/gallery/menu regressions. | Per-route script inventory, existing static/browser tests, all locale route smoke tests. |
| P2 | Replace scroll full-list geometry scan with viewport observation/scheduled reads. | Less scroll-time work and risk of layout thrash. | Reveal timing or hidden-content accessibility changes. | Scroll trace, reduced-motion check, keyboard/no-JS checks. |
| P2 | Load Jarallax only where needed and avoid mobile initialization if design permits. | Less third-party work on mobile and non-visible parallax section. | Parallax visual behavior. | Homepage PL/RU/EN screenshots, mobile scroll, reduced motion. |
| P2 | Review third-party phone-input stylesheet loading on five pages. | Lower render-blocking exposure on those routes. | Broken phone field visuals/interaction. | Contact/form pages in all locales, validation and accessibility checks. |
| P2 | Profile heavy effects/DOM on low-end mobile before altering CSS. | Potential paint/compositing improvement; no change recommended until measured. | Visual regression. | Chrome paint trace, screenshots, device matrix. |

No numeric performance improvement is promised for these items. The current
data cannot support an estimated TBT reduction or a 90+ score prediction.

## 14. Staged implementation plan (approval required before code changes)

1. **Capture a reproducible baseline.** Save three Lighthouse Mobile reports
   and Chrome traces for PL home, a representative service page, contact, and
   RU/EN samples. Record cold/warm state, viewport, throttle, browser, and
   consent state.
2. **Resolve tag ownership/configuration.** Inspect GTM Preview for both
   containers; identify all tags, triggers, duplicate page views, conversions,
   CookieYes ordering, and the observed extra IDs. Get explicit approval before
   any tag is disabled or consolidated.
3. **Run an approved staging comparison.** Compare baseline and one isolated
   change at a time; retain Analytics/Ads conversion checks and consent tests.
4. **Optimize first-party startup.** If approved, lazy-initialize Lazar after
   user intent, then route-scope/defer local scripts and address scroll work.
5. **Tune critical resources and cache policy.** Keep LCP preload/high priority;
   verify fonts and image priority; introduce static caching only with safe
   cache busting.
6. **Regression and rollout.** Test PL/RU/EN, navigation, contact forms, phone,
   WhatsApp, Lazar, galleries, service calculator, consent, canonical/hreflang,
   sitemap, and headers. Compare three Lighthouse runs and field INP/CrUX after
   deployment.

## 15. Risks and regression test matrix

| Surface | Required regression checks |
|---|---|
| Analytics/Ads | One page view per intended property; all approved Ads conversions fire once; correct attribution and consent state. |
| CookieYes | Banner controls, category preferences, returning-user state, denied/accepted network behavior, no tag firing outside approved policy. |
| Lazar | PL/RU/EN launcher, mobile bottom bar, open/close/focus, quick questions, send/retry/offline/timeout, contact links, gated EN pages. |
| Navigation | Mobile menu, language dropdown, service/work submenu, keyboard, focus, back/forward. |
| Forms | Required fields, consent, B2B phone/email validation, successful/error submit, analytics event. |
| LCP/visual | Homepage header background stays eager/preloaded/high priority; no new CLS, font shift, clipping, or contrast regressions. |
| SEO/routing | Canonical/hreflang, sitemap, redirects, 404, Markdown alternates, URL inventory unchanged. |
| Animation | Mobile carousel remains non-animated/hidden as designed; desktop hover/drag; hidden-tab and reduced-motion behavior. |

## 16. Checks not performed / limitations

- Lighthouse Mobile CLI and Chrome executable were not available in the shell
  environment; no formal Lighthouse run was produced.
- No Chrome DevTools Performance trace, task attribution stack, JS CPU profile,
  CSS coverage, or paint/compositing trace was captured.
- The integrated-browser samples used a responsive 390×844 viewport without
  configured CPU/network throttling. They are not equivalent to PSI mobile
  emulation and do not establish the reported TBT cause.
- Three homepage navigations exposed an LCP element and resource timing; this
  does not replace three controlled PSI/Lighthouse runs.
- RU and EN each had only one limited live browser sample.
- No controlled CookieYes deny/accept/reject test was performed, and the
  browser's stored consent state was not modified.
- GTM Preview, GA4 DebugView, Google Ads conversion diagnostics, and remote
  container configuration were unavailable. Dynamic tags cannot be traced to
  a specific container rule from repository source.
- No field INP/CrUX report was supplied or retrieved.
- No code/build changes were made for this audit. The build pipeline had
  passed during the earlier `dist` packaging work; it was not rerun to keep
  this audit read-only apart from this report.

## 17. Final conclusion

The available evidence confirms multiple plausible sources of extra startup
work, especially overlapping Google tag paths and a remotely loaded CookieYes
implementation, plus avoidable eager Lazar initialization. Production browser
observations also show extra analytics/Ads IDs not represented in the tracked
source. These are high-priority items to investigate, but none can yet be
assigned the 3,480 ms PSI TBT.

The LCP candidate is confirmed and already preloaded correctly. The most
important missing artifact is a throttled PSI/Lighthouse trace with
third-party task attribution and recorded consent state. No optimization
should disable analytics, Ads, or consent protections until their ownership
and behavior have been verified.

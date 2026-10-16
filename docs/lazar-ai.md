# Lazar AI integration

## Files and scope

- `js/main.js`: one idempotent loader for widget JS and CSS, after DOM readiness.
- `js/lazar-ai.js`: shared PL/RU interface, request lifecycle, local fallback dictionary and dataLayer events.
- `css/lazar-ai.css`: isolated `lazar-` styles using the site's palette and Montserrat.
- `img/lazar-ai-avatar.svg`: original vector: dark circular surface, central gold lightsaber with a pale blade and symmetric wing-like lines inspired by the Jedi Order emblem. No JavaScript, remote assets or raster images. Used on launcher, header and assistant messages.
- `scripts/check-lazar-ai.cjs`: reproducible browser tests with mocked requests.

All 99 public HTML pages (50 PL, 49 RU, including 404) already load `/js/main.js` exactly once. No HTML, existing navigation/footer/social markup, SEO, JSON-LD, hreflang, Markdown, AI index, n8n workflow or knowledge-base files were changed. The existing service-case/AI generators preserve the shared entry point. New page templates must continue including `main.js` and `main.css`.

## UI and accessibility

The closed launcher is a compact 58 px circle at the former social-menu position, bottom-right, with gold pulse rings. The existing menu remains in HTML with its handlers, but is hidden by the `lazar-social-hidden` class added only when the widget initializes. To restore it, remove that class assignment and its CSS rule, and choose nonoverlapping widget positioning. Nothing is deleted. Reduced-motion users receive static glow rings.

The chat never opens automatically. Width is at most 360 px and normal height at most 500 px, bounded by available viewport. Mobile uses dynamic viewport height, safe areas and visualViewport resize/scroll events, with a compact mode for a keyboard-reduced viewport.

The dialog is non-modal. Opening focuses its close button without automatically summoning the mobile keyboard; Escape/close returns focus to the launcher. There is no keyboard focus trap. A polite log announces messages; a separate status region announces waiting/failure text. Controls have visible focus, localized labels and at least 44 px touch height. Reduced motion disables the brief avatar opening effect. The full site remains usable without JS, but the interactive chat itself requires JS.

Call and form links are part of each assistant message, including the local greeting and fallback messages. There is no fixed contact-button toolbar beside the composer. Previous message links remain available while pending. Form destinations were verified in source: `/kontakt/#contactid` and `/ru/kontakt/#contactid`. Phone: `tel:+48790402597`.

## Request contract

POST `https://n8n.raccoon-studio.com.ua/webhook/lazar-ai-chat`, JSON Content-Type:

```json
{
  "message": "User's message",
  "language": "pl",
  "page_url": "https://lasertechservice.pl/uslugi/",
  "session_id": "random UUID"
}
```

Only an unambiguous, nonempty string `reply` is rendered with text nodes. A controlled renderer supports **bold** text using created strong elements, never innerHTML. A recognized trailing contact footer with the real company phone/form URL is replaced by localized, verified contact buttons below the answer. Arbitrary AI HTML/links are never executed. The URL omits query/fragment to avoid passing tracking or personal query parameters. Request credentials and referrer are omitted. The session identifier is generated on first request, stored in sessionStorage and reused across pages in the tab. If storage is denied, an in-memory ID is used. No conversation or personal data is written to localStorage/sessionStorage; conversation history lives only in the current page's memory and is lost on navigation/reload. No chat contents are logged to console.

Configuration is at the top of `js/lazar-ai.js`: `timeoutMs: 28000`, `maxMessageLength: 2000`, production endpoint. No external AI SDK, secret key, backend or new dependency is installed.

## Failure and retry behavior

Local dictionaries contain the supplied PL/RU messages for network/HTTP failures, timeout, invalid or empty JSON reply, offline state, excessive input and three consecutive technical failures. Empty input is rejected locally. Long input is validated before appending/sending and is not silently truncated. Offline messages explain that the form needs internet; phone/form links remain visible.

Only one request can be pending. Submit/Retry are disabled during a request; the input is temporarily read-only. The input clears immediately after a valid send; its request text stays in memory. On failure the text is restored for editing, and retrying the same text reuses its transcript row. The previous failure bubble is removed on retry to avoid stale errors. A changed message adds a new row. Retries require a user action; no background retries are scheduled. AbortController bounds waiting, including response-body reading. Success clears the failure state, resets the consecutive failure count and restores controls. After three consecutive failures the contact buttons receive priority styling; manual retries remain available. The timeout message explicitly notes that the earlier server execution may still be running. Client-side cancellation cannot guarantee server-side cancellation or exactly-once processing.

## Analytics

The existing `window.dataLayer` receives `lazar_open`, `lazar_message_sent`, `lazar_call_click`, `lazar_form_click`, `lazar_error`, `lazar_retry`. Parameters are locale and, for errors, a category (`timeout`, `network`, `server_error`, `invalid_response`, `offline`, `message_too_long`). No message, contact information, page URL or session ID is sent in these events. No GTM container or GA loader was added. Mapping these custom events to GA4 depends on the existing published GTM configuration; production GA ingestion was not verified.

## Verification — 2026-10-16

- All 99 HTML entry points audited; current template variants keep their metadata untouched.
- Chrome PL/RU: 320, 375, 390, 430, 768, 1024, 1440 px. Closed by default, no request on greeting, one greeting after reopen, no horizontal scroll, avatar decode, contacts and no launcher/social collision: PASS.
- Mocked 500/502/503, network failure, request timeout, malformed JSON, empty/object/null/literal-undefined reply, offline, overlong/empty message: PASS.
- Three consecutive failures, manual retry, unchanged input recovery, no duplicate transcript rows, no concurrent duplicate fetch, reset after success: PASS.
- Safe text rendering of HTML-looking reply, event payload allowlist/no PII, session ID stability within dialogue, blocked browser storage: PASS.
- Escape/focus restoration, social-menu hidden state with original markup retained, reduced motion context and simulated 340 px visualViewport with keyboard controls visible: PASS. Actual iOS/Android keyboard hardware was not tested.
- Additional browser smoke: 30 combinations (15 representative PL/RU routes including home, services, contact, prices, diagnostic landing, article, case and 404; 320/1440 px), with Montserrat confirmed loaded. Widget mounted exactly once; no additional horizontal overflow.
- Syntax checks, SVG XML/no active content, `git diff --check`, `build-ai-search.py --check`, `check-ai-search.py`, `check-geo-seo.py`: PASS. Existing AI resources were not regenerated or changed.

Additional template check found an existing 346 px document width at a 320 px viewport on `/ru/realizacje/serwis-glowicy-lasera-diodowego-poznan/` with Montserrat loaded. Removing the entire widget left the same 346 px width. This unrelated case-page issue was not changed.

Test evidence: `/tmp/lts-lazar/results.json`, `page-audit.json`, screenshots and API probe output. These temporary artifacts are not published assets.

Run a local HTTP server, then (with Playwright available outside the repository if preferred):

```sh
python3 -m http.server 8788 --bind 127.0.0.1
# Separate terminal:
PLAYWRIGHT_MODULE=/path/to/playwright node scripts/check-lazar-ai.cjs
```

Optional environment: `CHROME_PATH`, `LAZAR_TEST_BASE`, `LAZAR_TEST_OUT`. Tests intercept webhook traffic and outbound analytics; the production workflow is never disabled.

## Real API and release limitation

One real OPTIONS request with Origin `https://lasertechservice.pl` returned HTTP 204 and explicitly allowed that origin, POST and content-type. One real browser POST from the loaded production homepage on 2026-10-16 timed out after 28,003 ms. It contained only a clearly identified technical integration test, no customer data or service request. There was no automatic retry. A successful real `reply` was **not** confirmed. The frontend and mocked failure/success handling are verified; end-to-end production readiness remains unconfirmed until the existing backend responds within the agreed timeout.

Before release, the workflow owner should inspect the execution of that test, provider latency and Respond to Webhook behavior, ensuring the agreed `{ "reply": "..." }` JSON response. Do not introduce or alter workflows as part of this frontend task. Keep CORS headers on POST responses and error responses as well as preflight; the timed-out POST could not confirm its response headers. Confirm rate limiting and anti-spam at the existing endpoint/proxy: the public frontend endpoint and input validation are not authentication or server-side abuse prevention. These server controls were not changed or proven present. Idempotency for timeout retries requires backend support; the existing four-field request contract has not been extended.

Response brevity and technical accuracy depend on the already-configured AI agent/knowledge base. The client does not silently cut off technical answers or change prompts. Real assistive-technology testing, physical mobile devices, production analytics reception and deployed widget behavior remain separate checks.

## UI revision — 2026-10-16

The latest requested revision includes compact right-aligned placement, reversible social-menu hiding, a lightsaber avatar, per-message contact buttons, safe bold/contact-footer rendering and immediate composer clearing with failure recovery. The 16 browser layout/scenario groups and storage-denial test were rerun successfully; they now check that contact links are inside messages and no static toolbar exists, plus immediate clearing while a request is pending. The earlier real API probe above was not repeated for this UI revision. AI response language itself is controlled by the existing backend; the frontend continues sending the correct page locale and does not translate responses.

No commit, push or deploy was performed.

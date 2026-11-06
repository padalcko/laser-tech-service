/* Local regression: stalled optional CDN must not block mobile controls. */
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const assert = require('assert').strict;
const base = process.env.LTS_TEST_BASE || 'http://127.0.0.1:8799';
(async () => {
  const browser = await chromium.launch({ channel: 'chrome', headless: true });
  try {
    const context = await browser.newContext({ viewport: { width: 393, height: 852 }, isMobile: true, hasTouch: true });
    let release;
    const stalled = new Promise(resolve => { release = resolve; });
    await context.route('**/*', async route => {
      if (route.request().url().includes('jarallax.min.js')) {
        await stalled;
        return route.abort();
      }
      return route.request().url().startsWith(base + '/') ? route.continue() : route.abort();
    });
    const page = await context.newPage(), errors = [];
    page.on('pageerror', error => errors.push(error.message));
    try {
      for (const path of ['/', '/ru/', '/en/']) {
        await page.goto(base + path, { waitUntil: 'domcontentloaded', timeout: 5000 });
        const bar = page.locator('.mobile-contact-bar');
        await bar.waitFor({ timeout: 5000 });
        for (const y of [1500, 3500, 0]) {
          await page.evaluate(y => scrollTo(0, y), y);
          const box = await bar.boundingBox();
          assert(box && box.y >= 0 && box.y + box.height <= 852);
        }
        await page.locator('.language-switcher__toggle').tap();
        // iOS may emit a blur without relatedTarget before a link's click.
        await page.locator('.language-switcher__toggle').dispatchEvent('focusout', { relatedTarget: null });
        assert(await page.locator('.language-switcher__dropdown').evaluate(e => e.open));
        const target = path === '/en/' ? '/' : '/en/';
        await page.locator(`.language-switcher__options a[href="${target}"]`).tap();
        await page.waitForURL(base + target, { waitUntil: 'domcontentloaded' });
        await bar.waitFor();
        await page.locator('.nav-toggle').tap();
        assert(await bar.isVisible());
        await page.locator('.nav-toggle').tap();
        await page.locator('[data-action=lazar]').tap();
        assert(await bar.isVisible());
        const panelBox = await page.locator('#lazar-panel').boundingBox();
        const barBox = await bar.boundingBox();
        assert(panelBox.y + panelBox.height <= barBox.y);
        await page.locator('.lazar-close').tap();
      }
      assert.deepEqual(errors, []);
      console.log('PASS PL/RU/EN: stalled CDN, mobile bar during scroll/menu/chat, touch language navigation, null-relatedTarget blur, chat clearance, no JS errors');
    } finally { release(); }
  } finally { await browser.close(); }
})().catch(error => { console.error(error); process.exitCode = 1; });

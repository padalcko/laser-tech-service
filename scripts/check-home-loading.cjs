/* Homepage loading contract; no lead or chat messages are sent. */
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const fs=require('fs'),assert=require('assert').strict;
const base=process.env.LTS_TEST_BASE||'http://127.0.0.1:8796';
(async()=>{
 const browser=await chromium.launch({channel:'chrome',headless:true});
 const context=await browser.newContext({viewport:{width:390,height:844},isMobile:true});
 const page=await context.newPage(),errors=[];page.on('pageerror',e=>errors.push(e.message));
 // Real integrations are loaded so injected CookieYes and GTM duplicates remain observable.
 await page.goto(base+'/',{waitUntil:'domcontentloaded'});
 await page.locator('.lazar-launcher').waitFor({state:'visible'});
 await page.waitForFunction(()=>document.querySelectorAll('script[src*="/gtm.js?id="]').length===2);
 await page.waitForFunction(()=>performance.getEntriesByType('resource').filter(e=>e.name.includes('googletagmanager.com/')&&e.initiatorType==='script').length>=4,{},{timeout:45000});
 const timing=await page.evaluate(()=>{
  const fcp=performance.getEntriesByName('first-contentful-paint')[0].startTime;
  const tags=performance.getEntriesByType('resource').filter(e=>e.name.includes('googletagmanager.com/')&&e.initiatorType==='script');
  return {fcp,tags:tags.map(e=>({url:e.name,start:e.startTime})),preloads:[...document.querySelectorAll('link[rel="preload"][as="image"]')].map(e=>e.href)};
 });
 assert(timing.tags.length>=4);assert(timing.tags.every(e=>e.start>=timing.fcp),'Tags must not compete with first paint');
 assert.equal(timing.preloads.length,1);
 assert.equal(await page.locator('script[src*="jarallax-video"],link[href*="intlTelInput"]').count(),0);
 await page.locator('.lazar-launcher').click();await page.locator('#lazar-panel').waitFor({state:'visible'});
 await page.locator('.lazar-close').click();await page.locator('#lazar-panel').waitFor({state:'hidden'});
 await page.locator('.nav-toggle').click();assert.equal(await page.locator('.nav-toggle').getAttribute('aria-expanded'),'true');await page.locator('.nav-toggle').click();
 assert.equal(await page.locator('.language-switcher a').count(),3);
 assert.equal(await page.locator('.article-service-form__form').count(),1);
 assert(await page.evaluate(()=>typeof jarallax==='function'));
 // Wait for the actual CMP, preserving its original GTM ownership.
 await page.locator('.cky-consent-container').waitFor({state:'visible',timeout:45000});
 const cmp=await page.locator('.cky-consent-container').innerText();assert(cmp.length>20);
 for(const width of [320,375,390,768,1440]){
  await page.setViewportSize({width,height:900});assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
 }
 await page.screenshot({path:'/tmp/lts-mobile-lcp/after-desktop.png'});
 await page.setViewportSize({width:390,height:844});await page.screenshot({path:'/tmp/lts-mobile-lcp/after-mobile.png'});
 assert.deepEqual(errors,[]);
 fs.writeFileSync('/tmp/lts-mobile-lcp/functional.json',JSON.stringify({timing,errors,cmpVisible:true,widths:[320,375,390,768,1440]},null,2));
 await browser.close();console.log('PASS: first-paint tag scheduling, CookieYes visible, Lazar/menu/form markup/parallax/languages and five widths; no JS errors');
})().catch(e=>{console.error(e);process.exit(1)});

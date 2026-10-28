/* Run against a local server serving /404.html with status 404 for missing paths. */
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const assert = require('node:assert/strict');
(async () => {
 const browser = await chromium.launch({executablePath: process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', headless:true});
 const base = process.env.TEST_BASE_URL || 'http://127.0.0.1:8789';
 const page = await browser.newPage(); const errors=[]; const payloads=[];
 page.on('pageerror', e => errors.push(e.message));
 await page.route('**/*', route => {
  const url=route.request().url();
  if(url.startsWith(base)) return route.continue();
  if(url.includes('/webhook/lazar-ai-chat')) {payloads.push(route.request().postDataJSON());return route.fulfill({json:{reply:'Test reply'}});}
  return route.abort();
 });
 const paths=['/test-404-check/','/ru/test-404-check/','/en/test-404-check/','/ru/uslugi/nonexistent-page/','/en/services/nonexistent-page/'];
 let checks=0;
 for(const width of [320,390,768,1440]) for(const path of paths) {
  await page.setViewportSize({width,height:900});
  const response=await page.goto(base+path);
  assert.equal(response.status(),404);assert.equal(response.request().redirectedFrom(),null);
  const initial=path.startsWith('/ru/')?'ru':path.startsWith('/en/')?'en':'pl';
  assert.equal(await page.locator('html').getAttribute('lang'),initial);
  await page.locator('#lazar-root').waitFor({state:'attached'});
  for(const lang of ['pl','ru','pl','en','ru','en','pl']) {
   await page.locator('.language-switcher summary').click();
   await page.locator(`.language-switcher a[lang="${lang}"]`).click();
   assert.equal(page.url(),base+path);
   const result=await page.evaluate(lang => {
    const d=JSON.parse(document.querySelector('#error-locales').textContent);
    const text=document.querySelector('main').textContent;
    return {lang:document.documentElement.lang, overflow:document.documentElement.scrollWidth>innerWidth,
     title:document.title, count:document.querySelectorAll('#lazar-root').length,
     hero:text.includes(d.text[lang]['Wróć na stronę główną']),
     links:[...document.querySelectorAll('a[href^="/"]')].map(a=>a.getAttribute('href')),
     footer:document.querySelector('.footer__description').textContent.trim(),
     expectedFooter:d.text[lang][Object.keys(d.text.pl).find(k=>k.startsWith('Profesjonalny serwis'))]};
   },lang);
   assert.equal(result.lang,lang);assert.equal(result.overflow,false,`${width} ${path} ${lang}`);
   assert.equal(result.count,1);assert(result.hero);assert.equal(result.footer,result.expectedFooter);
   assert.equal(await page.locator('.lazar-launcher').getAttribute('aria-label'),{pl:'Zapytaj Łazarza',ru:'Спросить Лазаря',en:'Ask Lazar'}[lang]);
   await page.evaluate(() => scrollTo(0, document.body.scrollHeight));
   await page.locator('.lazar-launcher').click();
   if(lang!=='en') {
    await page.locator('.lazar-input').fill('Test equipment problem');
    await page.locator('.lazar-form').evaluate(form=>form.requestSubmit());
    await page.getByText('Test reply',{exact:true}).waitFor();
    assert.equal(payloads.at(-1).language,lang); assert.equal(payloads.at(-1).page_url,base+path);
   }
   await page.locator('.lazar-close').click();
   for(const href of new Set(result.links)) { const r=await page.request.get(base+href); assert.equal(r.status(),200,href); }
   checks++;
  }
  await page.reload();assert.equal(await page.locator('html').getAttribute('lang'),initial);
  if(path==='/en/test-404-check/')await page.screenshot({path:`/tmp/404-${width}.png`,fullPage:true});
 }
 // Verify collision handling at the previously overlapping mobile CTA.
 await page.setViewportSize({width:320,height:900});
 await page.goto(base+'/en/test-404-check/');
 await page.locator('.lazar-launcher').waitFor({state:'attached'});
 await page.waitForFunction(() => getComputedStyle(document.querySelector('.lazar-launcher')).visibility === 'hidden');
 await page.evaluate(() => scrollTo(0, document.body.scrollHeight));
 await page.locator('.lazar-launcher').waitFor({state:'visible'});
 assert.deepEqual(errors,[]);
 console.log(`PASS: ${checks} locale/layout states; 5 paths; six switch directions; reload; links; mocked Lazar language; no JS errors.`);
 await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});

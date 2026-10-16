/* Run with PLAYWRIGHT_MODULE and CHROME_PATH if Playwright/Chrome are not on defaults.
   All webhook responses are mocked. No real conversations or analytics are sent. */
const { chromium } = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const fs = require('fs');
const assert = require('assert').strict;
const base = process.env.LAZAR_TEST_BASE || 'http://127.0.0.1:8788';
const out = process.env.LAZAR_TEST_OUT || '/tmp/lts-lazar';
fs.mkdirSync(out, { recursive: true });
const results = [];
(async () => {
 const browser = await chromium.launch({ headless: true, executablePath: process.env.CHROME_PATH || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' });
 async function context(width = 390, language = 'pl', timeout = false) {
  const c = await browser.newContext({ viewport: { width, height: 900 }, reducedMotion: 'reduce' });
  let mode = 'success', requests = [];
  await c.route('**/*', async r => {
   const u = r.request().url();
   if (u.includes('/webhook/lazar-ai-chat')) {
    requests.push(r.request().postDataJSON());
    if (mode === 'network') return r.abort();
    if (mode === 'timeout' || mode === 'delayed') await new Promise(resolve => setTimeout(resolve, mode === 'timeout' ? 700 : 100));
    if (/^\d+$/.test(mode)) return r.fulfill({ status: +mode, body: 'private backend error' });
    const body = { success: JSON.stringify({reply:'**Test** <img src=x onerror=alert(1)> reply\n\n**Позвонить:** +48 790 402 597\n**Оставить заявку:**\nhttps://lasertechservice.pl/#contactid'}), invalid:'not json', empty:'{"reply":" "}', object:'{"reply":{}}', null:'{"reply":null}', literal:'{"reply":"undefined"}' }[mode] || '{"reply":"Reply after retry"}';
    return r.fulfill({ status: 200, contentType: 'application/json', body });
   }
   if (timeout && u === base + '/js/lazar-ai.js') return r.fulfill({ contentType: 'application/javascript', body: fs.readFileSync('js/lazar-ai.js','utf8').replace('timeoutMs: 28000', 'timeoutMs: 250') });
   return u.startsWith(base) ? r.continue() : r.abort();
  });
  const p = await c.newPage(); const errors = []; p.on('pageerror', e => errors.push(e.message));
  await p.goto(base + (language === 'ru' ? '/ru/' : '/'));
  await p.locator('.lazar-launcher').waitFor();
  return { c, p, requests, errors, mode: value => mode = value };
 }
 for (const width of [320,375,390,430,768,1024,1440]) for (const language of ['pl','ru']) {
  const x = await context(width, language); const {p,c} = x;
  assert.equal(await p.locator('.lazar-panel').isVisible(), false);
  assert.equal(x.requests.length, 0);
  assert.equal(await p.locator('.menu').isVisible(),false);
  assert(await p.locator('menu > .trigger').count());
  await p.locator('.lazar-launcher').click();
  assert.equal(await p.locator('.lazar-panel > .lazar-contacts').count(),0);
  assert.equal(await p.locator('.lazar-message .lazar-contacts a').count(),2);
  assert.equal(await p.locator('.lazar-message').count(),1); assert.equal(x.requests.length,0);
  await p.locator('.lazar-header img').evaluate(e=>e.decode());
  const geometry=await p.evaluate(()=>{const a=document.querySelector('.lazar-panel').getBoundingClientRect();return {left:a.left,right:a.right,bottom:a.bottom,width:innerWidth,height:innerHeight,overflow:document.documentElement.scrollWidth>innerWidth};});
  assert(geometry.left>=0 && geometry.right<=width && geometry.bottom<=900 && !geometry.overflow);
  assert.equal(await p.locator('.lazar-contacts a').nth(1).getAttribute('href'),(language==='ru'?'/ru':'')+'/kontakt/#contactid');
  await p.keyboard.press('Escape'); assert.equal(await p.locator('.lazar-panel').isVisible(),false);
  assert(await p.locator('.lazar-launcher').evaluate(e=>e===document.activeElement));
  await p.locator('.lazar-launcher').click(); assert.equal(await p.locator('.lazar-message').count(),1);
  if ([390,1440].includes(width)) await p.screenshot({path:`${out}/${language}-${width}.png`});
  await p.locator('.lazar-close').click(); assert.equal(await p.locator('.lazar-panel').isVisible(),false);
  assert.deepEqual(x.errors,[]); results.push({language,width,layout:'PASS'}); await c.close();
 }
 for (const language of ['pl','ru']) {
  const x=await context(390,language,true);const {p,c}=x;
  await p.locator('.lazar-launcher').click();
  await p.locator('.lazar-input').fill('x'.repeat(2001));await p.locator('.lazar-send').click();assert.equal(x.requests.length,0);
  await p.locator('.lazar-input').fill('   ');await p.locator('.lazar-send').click();assert.equal(x.requests.length,0);
  const submit=async(text)=>{await p.locator('.lazar-input').fill(text);await p.locator('.lazar-send').click();};
  const finished=()=>p.waitForFunction(()=>document.querySelector('.lazar-form').getAttribute('aria-busy')==='false');
  for(const mode of ['500','502','503','invalid','empty','object','null','literal','network','timeout']) {
   x.mode(mode);await submit('TEST-'+mode);await finished();assert(await p.locator('.lazar-retry').isVisible());
   assert.equal(await p.locator('.lazar-input').inputValue(),'TEST-'+mode);
   assert.equal(await p.locator('.lazar-message').last().locator('.lazar-contacts a:visible').count(),2);
   const before=await p.locator('.lazar-message--user').count();x.mode('success');await p.locator('.lazar-retry').click();await finished();
   assert.equal(await p.locator('.lazar-message--user').count(),before);assert.equal(await p.locator('.lazar-retry').isVisible(),false);
   assert.equal(await p.locator('.lazar-log img[src="x"]').count(),0);assert(!(await p.locator('.lazar-bubble').last().textContent()).includes('https://lasertechservice.pl'));assert.equal(await p.locator('.lazar-bubble').last().locator('strong').count(),1);assert.equal(await p.locator('.lazar-input').inputValue(),'');
  }
  await c.setOffline(true);await submit('TEST-offline');await finished();assert(await p.locator('.lazar-retry').isVisible());await c.setOffline(false);x.mode('success');await p.locator('.lazar-retry').click();await finished();
  x.mode('500');await submit('TEST-repeat');await finished();for(let i=0;i<2;i++){await p.locator('.lazar-retry').click();await finished();}
  assert(await p.locator('.lazar-contacts--priority').isVisible());
  const before=x.requests.length;await p.waitForTimeout(350);assert.equal(x.requests.length,before);
  x.mode('delayed');await p.locator('.lazar-retry').click();assert.equal(await p.locator('.lazar-input').inputValue(),'');await p.locator('.lazar-form').evaluate(e=>{e.dispatchEvent(new Event('submit',{cancelable:true}));e.dispatchEvent(new Event('submit',{cancelable:true}));});await finished();assert.equal(x.requests.length,before+1);
  assert.equal(await p.locator('.lazar-contacts--priority').count(),0);
  const ids=x.requests.map(r=>r.session_id);assert(ids.every(id=>id===ids[0]));
  assert.deepEqual(Object.keys(x.requests[0]).sort(),['language','message','page_url','session_id']);
  assert.equal(x.requests[0].language,language);
  await p.locator('.lazar-contacts a').evaluateAll(links=>links.forEach(a=>{a.addEventListener('click',e=>e.preventDefault());a.click();}));
  const events=await p.evaluate(()=>dataLayer.filter(e=>e.event?.startsWith('lazar_')));
  for(const name of ['lazar_open','lazar_message_sent','lazar_call_click','lazar_form_click','lazar_error','lazar_retry'])assert(events.some(e=>e.event===name),name);
  assert(!JSON.stringify(events).includes('TEST'));assert(events.every(e=>Object.keys(e).every(k=>['event','language','error_category'].includes(k))));
  const storage=await p.evaluate(()=>({session:{...sessionStorage},local:{...localStorage}}));assert(!JSON.stringify(storage).includes('TEST'));
  // Simulate the visual viewport shrinking independently of layout viewport.
  await p.evaluate(()=>{Object.defineProperty(visualViewport,'height',{configurable:true,value:340});visualViewport.dispatchEvent(new Event('resize'));});
  await p.waitForFunction(()=>document.querySelector('.lazar-input').getBoundingClientRect().bottom<=340);
  const keyboard=await p.evaluate(()=>{const input=document.querySelector('.lazar-input').getBoundingClientRect(),close=document.querySelector('.lazar-close').getBoundingClientRect();return {inputBottom:input.bottom,closeTop:close.top,panel:document.querySelector('.lazar-panel').getBoundingClientRect().toJSON(),classes:document.querySelector('.lazar-root').className};});assert(keyboard.inputBottom<=340&&keyboard.closeTop>=0,JSON.stringify(keyboard));
  results.push({language,fallbacks:'500/502/503/network/timeout/invalid/empty/object/null/literal/offline/long/three-errors',retry:'manual, no duplicate rows/parallel fetch',analytics:'6 events, no PII',keyboardSimulation:'PASS'});
  assert.deepEqual(x.errors,[]);await c.close();
 }
 // Storage denial must not prevent greeting or requests.
 const x=await context();await x.p.addInitScript(()=>{Storage.prototype.getItem=()=>{throw Error('denied')};Storage.prototype.setItem=()=>{throw Error('denied')};});await x.p.reload();await x.p.locator('.lazar-launcher').click();await x.p.locator('.lazar-input').fill('TEST-private');await x.p.locator('.lazar-send').click();await x.p.waitForFunction(()=>document.querySelectorAll('.lazar-message').length===3);assert.equal(x.requests.length,1);await x.c.close();
 await browser.close();fs.writeFileSync(`${out}/results.json`,JSON.stringify(results,null,2));console.log(`PASS ${results.length} layout/scenario groups plus storage denial`);
})().catch(e=>{console.error(e);process.exit(1)});

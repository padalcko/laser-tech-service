/* Local regression only. External requests blocked; webhooks mocked; EN exists only in intercepted HTML. */
const {chromium} = require(process.env.PLAYWRIGHT_MODULE || 'playwright');
const fs = require('fs');
const path = require('path');
const assert = require('assert').strict;
const root = path.resolve(__dirname, '..');
const base = process.env.LTS_TEST_BASE || 'http://127.0.0.1:8788';
const out = process.env.LTS_TEST_OUT || '/tmp/lts-stage2a';
fs.mkdirSync(out, {recursive:true});
const registry = JSON.parse(fs.readFileSync(path.join(__dirname, 'site-locales.json')));
const results = [];
(async () => {
 const browser = await chromium.launch({channel:'chrome', headless:true});
 async function setup(locale, width=390, js=true) {
  const c=await browser.newContext({viewport:{width,height:900},javaScriptEnabled:js,reducedMotion:'reduce'});
  const errors=[], requests=[];let mode='success';
  await c.route('**/*',async r=>{
   const u=r.request().url();
   if(u.includes('/webhook/')){
    requests.push({url:u,body:r.request().postDataJSON()});
    if(mode==='network')return r.abort();
    if(mode==='500')return r.fulfill({status:500,body:'error'});
    if(mode==='invalid')return r.fulfill({body:'invalid JSON'});
    if(mode==='empty')return r.fulfill({json:{reply:''}});
    await new Promise(resolve=>setTimeout(resolve,80));
    return r.fulfill({json:u.includes('lazar-ai-chat')?{reply:'Test reply'}:{success:true}});
   }
   if(!u.startsWith(base+'/'))return r.abort();
   if(locale && r.request().resourceType()==='document'){
    const response=await r.fetch();
    return r.fulfill({response,body:(await response.text()).replace(/<html lang="[^"]+"/,`<html data-lazar-enabled="true" lang="${locale}"`)});
   }
   return r.continue();
  });
  const p=await c.newPage();p.on('pageerror',e=>errors.push(e.message));
  return {p,c,errors,requests,setMode:v=>mode=v};
 }
 const selections=['home','service-detail','article','case-study','pricing','contact','partners'];
 for(const lang of ['pl','ru'])for(const width of [320,390,1440]){
  const x=await setup(null,width);const {p}=x;
  for(const type of selections){
   const group=registry.pages.find(g=>g.type===type);await p.goto(base+group.routes[lang].url);
   const toggle=p.locator('.language-switcher__toggle'),details=p.locator('.language-switcher__dropdown');
   assert.equal((await toggle.innerText()).replace(/\s+/g,' ').trim(),lang.toUpperCase()+' ▾');
   await toggle.focus();await p.keyboard.press('Enter');
   assert(await details.evaluate(e=>e.open));
   const links=await details.locator('a').evaluateAll(a=>a.map(e=>({lang:e.hreflang,url:e.getAttribute('href'),h:e.getBoundingClientRect().height,w:e.getBoundingClientRect().width})));
   assert.deepEqual(links.map(l=>[l.lang,l.url]),Object.entries(group.routes).filter(([,r])=>r.status==='published').map(([l,r])=>[l,r.url]));
   assert(links.every(l=>l.h>=44&&l.w>=44));assert((await toggle.boundingBox()).height>=44);
   await p.keyboard.press('ArrowDown');assert.equal(await p.locator(':focus').getAttribute('hreflang'),'pl');
   await p.keyboard.press('End');assert.equal(await p.locator(':focus').getAttribute('hreflang'),links.at(-1).lang);
   await p.keyboard.press('Home');assert.equal(await p.locator(':focus').getAttribute('hreflang'),'pl');
   await p.keyboard.press('Escape');assert.equal(await details.evaluate(e=>e.open),false);
   assert(await toggle.evaluate(e=>e===document.activeElement));
   await toggle.click();await p.mouse.click(2,800);assert.equal(await details.evaluate(e=>e.open),false);
   if(await p.locator('.nav-toggle').isVisible()){
    await p.locator('.nav-toggle').click();assert.equal(await p.locator('.nav-toggle').getAttribute('aria-expanded'),'true');
    await toggle.click();await p.keyboard.press('Escape');assert.equal(await p.locator('.nav-toggle').getAttribute('aria-expanded'),'true');
    await p.keyboard.press('Escape');assert.equal(await p.locator('.nav-toggle').getAttribute('aria-expanded'),'false');
   }
   await toggle.click();assert(!(await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth)));
   if(type==='home')await p.screenshot({path:path.join(out,`${lang}-${width}.png`)});
   const other=lang==='pl'?'ru':'pl';await details.locator(`[hreflang=${other}]`).click();await p.waitForURL(base+group.routes[other].url);
   results.push({lang,width,type,result:'PASS'});
  }
  assert.deepEqual(x.errors,[]);assert.equal(x.requests.length,0);await x.c.close();
 }
 // Native disclosure and real links remain usable without JavaScript.
 const nojs=await setup(null,320,false);await nojs.p.goto(base+'/');await nojs.p.locator('summary.language-switcher__toggle').click();
 await nojs.p.locator('.language-switcher [hreflang=ru]').click();await nojs.p.waitForURL(base+'/ru/');await nojs.c.close();
 for(const locale of ['pl','ru','en','en-GB','xx']){
  const lang=locale.startsWith('en')?'en':locale==='ru'?'ru':'pl';const x=await setup(locale);const {p}=x;
  await p.goto(base+'/uslugi/diagnostyka-laserow-diodowych/');
  await p.locator('.nav-toggle').click();await p.keyboard.press('Escape');
  assert.equal(await p.locator('.nav-toggle').getAttribute('aria-label'),{pl:'Otwórz menu',ru:'Открыть меню',en:'Open menu'}[lang]);
  await p.locator('.lazar-launcher').waitFor();assert.equal(await p.locator('.lazar-launcher-label').innerText(),{pl:'ZAPYTAJ ŁAZARA',ru:'СПРОСИТЬ ЛАЗАРЯ',en:'ASK LAZAR'}[lang]);
  await p.locator('.lazar-launcher').click();
  assert.equal(await p.locator('.lazar-contacts a').nth(1).getAttribute('href'),{pl:'/kontakt/#contactid',ru:'/ru/kontakt/#contactid',en:'/en/contact/'}[lang]);
  for(const mode of ['500','invalid','empty','network','success']){
   x.setMode(mode);await p.locator('.lazar-input').fill('TEST runtime');await p.locator('.lazar-send').click();
   await p.waitForFunction(()=>document.querySelector('.lazar-form').getAttribute('aria-busy')==='false');
   assert.equal(x.requests.at(-1).body.language,lang);
   if(lang==='en'&&mode!=='success')assert.match(await p.locator('.lazar-message').last().innerText(),/Sorry|temporary technical/);
  }
  const ids=x.requests.map(r=>r.body.session_id);assert(ids.every(id=>id===ids[0]));
  await p.keyboard.press('Escape');
  const form=p.locator('.article-service-form__form');
  if(lang==='en'){
   assert.match(await form.locator('.consent').innerText(),/^I agree/);
   await form.locator('[type=submit]').click();assert.match(await form.locator('[name=fullName]').evaluate(e=>e.validationMessage),/Please/);
  }
  await form.locator('[name=fullName]').fill('TEST');await form.locator('[name=phone]').fill('+48123456789');
  await form.locator('[name=city]').fill('TEST');await form.locator('[name=deviceName]').fill('TEST');
  await form.locator('[name=problemDescription]').fill('TEST');await form.locator('[name=consent]').check();
  for(const mode of ['500','success']){
   x.setMode(mode);await form.locator('[type=submit]').click();
   await p.waitForFunction(()=>!document.querySelector('.article-service-form__form').hasAttribute('aria-busy'));
   const payload=x.requests.at(-1).body;assert.equal(payload.language,lang);assert.equal(payload.serviceType,'diode-laser-diagnostics');
   assert.deepEqual(Object.keys(payload).sort(),['fullName','phone','city','salonName','deviceName','language','source','pageUrl','serviceType','problemDescription'].sort());
   if(lang==='en')assert.match(await form.locator('.article-service-form__message').innerText(),mode==='success'?/Thank you/:/could not be sent/);
  }
  if(lang==='en'){
   await p.goto(base+'/uslugi/cennik/');await p.locator('#travel-km').fill('-1');assert.match(await p.locator('#travel-error').innerText(),/Enter a number/);
   await p.locator('#travel-km').fill('100');assert.match(await p.locator('#travel-result').innerText(),/140/);
   await p.goto(base+'/realizacje/naprawa-lumenis-lightsheer-desire-olesnica/');
   assert.equal(await p.locator('.case-photo-dialog').getAttribute('aria-label'),'Photo preview');
   assert.equal(await p.locator('.case-photo-dialog button').innerText(),'Close ×');
  }
  assert.deepEqual(x.errors,[]);await x.c.close();results.push({locale,runtime:'PASS'});
 }
 await browser.close();fs.writeFileSync(path.join(out,'results.json'),JSON.stringify(results,null,2));console.log(`PASS: ${results.length} groups + no-JS switching`);
})().catch(e=>{console.error(e);process.exit(1)});

/* Stage 3A: local-only browser checks; external requests blocked, leads mocked. */
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const fs=require('fs'),path=require('path'),assert=require('assert').strict;
const registry=JSON.parse(fs.readFileSync(path.join(__dirname,'site-locales.json')));
const groups=registry.pages.filter(g=>g.type==='service-detail'&&g.routes.pl&&g.routes.en?.status==='published');
const base=process.env.LTS_TEST_BASE||'http://127.0.0.1:8788';
const out=process.env.LTS_TEST_OUT||'/tmp/lts-stage3a';fs.mkdirSync(out,{recursive:true});
(async()=>{
 const browser=await chromium.launch({channel:'chrome',headless:true});const results=[];
 const c=await browser.newContext({reducedMotion:'reduce'});let mode='success';const requests=[],errors=[];
 await c.route('**/*',async r=>{
  const url=r.request().url();
  if(url.includes('/webhook/')){
   assert(url.endsWith('/lts-service-lead'),'Unexpected chat request');requests.push(r.request().postDataJSON());
   await new Promise(resolve=>setTimeout(resolve,200));
   return r.fulfill(mode==='error'?{status:500,body:'error'}:{json:{success:true}});
  }
  return url.startsWith(base+'/')?r.continue():r.abort();
 });
 const p=await c.newPage();p.on('pageerror',e=>errors.push(e.message));
 let count=0;for(const g of registry.pages)for(const r of Object.values(g.routes))if(r.status==='published'){
  assert.equal((await c.request.get(base+r.url)).status(),200,r.url);count++;
 }
 assert.equal(count,195);results.push({httpPages:count});
 const selected=['diode-laser-diagnostics','touchscreen-control-panel-repair','co2-laser-service'];
 for(const g of groups)for(const width of [320,390,1440]){
  const route=g.routes.en.url,slug=route.split('/')[3];await p.setViewportSize({width,height:900});await p.goto(base+route);
  await p.waitForTimeout(100);assert.equal(await p.locator('.lazar-root').getAttribute('data-sending-enabled'),'false');
  assert.equal(await p.locator('h1').count(),1);assert.equal(await p.locator('html').getAttribute('lang'),'en');
  const dropdown=p.locator('.language-switcher__dropdown');await dropdown.locator('summary').click();
  assert.deepEqual(await dropdown.locator('a').evaluateAll(es=>es.map(e=>e.hreflang)),['pl','ru','en']);
  const targets=await dropdown.locator('summary,a').evaluateAll(es=>es.map(e=>e.getBoundingClientRect().height));assert(targets.every(h=>h>=44));
  await p.keyboard.press('ArrowDown');assert.equal(await p.locator(':focus').getAttribute('hreflang'),'pl');
  await p.keyboard.press('End');assert.equal(await p.locator(':focus').getAttribute('hreflang'),'en');
  await p.keyboard.press('Escape');assert.equal(await dropdown.evaluate(e=>e.open),false);
  await dropdown.locator('summary').click();await p.mouse.click(8,850);assert.equal(await dropdown.evaluate(e=>e.open),false);
  if(await p.locator('.nav-toggle').isVisible()){
   await p.locator('.nav-toggle').click();assert.equal(await p.locator('.nav-toggle').getAttribute('aria-expanded'),'true');await p.keyboard.press('Escape');
   assert.equal(await p.locator('.nav-toggle').getAttribute('aria-expanded'),'false');
  }
  for(const im of await p.locator('img').all())if(await im.isVisible()){await im.scrollIntoViewIfNeeded();await im.evaluate(e=>e.decode());}
  for(const faq of await p.locator('.faq__question').all()){
   await faq.focus();await p.keyboard.press('Enter');assert.equal(await faq.getAttribute('aria-expanded'),'true');await faq.click();
  }
  assert(!(await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth)),route+' '+width);
  assert.equal(await p.locator('.service-cases-grid:empty, article:empty').count(),0);
  await p.evaluate(()=>scrollTo(0,0));
  if(selected.includes(slug)){
   await p.screenshot({path:path.join(out,slug+'-'+width+'.png')});
   if(width===1440)await p.screenshot({path:path.join(out,slug+'-full.png'),fullPage:true});
  }
  if(width===390){
   await dropdown.locator('summary').click();await dropdown.locator('[hreflang=ru]').click();await p.waitForURL(base+g.routes.ru.url);
   await p.locator('.language-switcher summary').click();await p.locator('.language-switcher [hreflang=en]').click();await p.waitForURL(base+route);
   await p.locator('.language-switcher summary').click();await p.locator('.language-switcher [hreflang=pl]').click();await p.waitForURL(base+g.routes.pl.url);
   await p.locator('.language-switcher summary').click();await p.locator('.language-switcher [hreflang=en]').click();await p.waitForURL(base+route);
   const before=requests.length,form=p.locator('.article-service-form__form');
   await form.locator('[type=submit]').click();assert.equal(requests.length,before);
   assert.match(await form.locator('[name=fullName]').evaluate(e=>e.validationMessage),/Please/);
   for(const name of ['fullName','phone','city','deviceName','problemDescription'])await form.locator(`[name=${name}]`).fill(name==='phone'?'+48123456789':'TEST ONLY');
   await form.locator('[type=submit]').click();assert.equal(requests.length,before);await form.locator('[name=consent]').check();
   const serviceType=await form.locator('[name=serviceType]').inputValue(),source=await form.locator('[name=source]').inputValue();
   for(mode of ['error','success']){
    await form.locator('[type=submit]').click();assert.equal(await form.locator('[type=submit]').innerText(),'Sending…');
    await p.waitForFunction(()=>!document.querySelector('.article-service-form__form').hasAttribute('aria-busy'));
    assert.match(await form.locator('.article-service-form__message').innerText(),mode==='error'?/could not be sent/:/Thank you/);
    const payload=requests.at(-1);assert.equal(payload.language,'en');assert.equal(payload.source,source);assert.equal(payload.serviceType,serviceType);
    assert.equal(payload.pageUrl,base+route);assert.equal(payload.problemDescription,'TEST ONLY');
    assert.deepEqual(Object.keys(payload).sort(),['fullName','phone','city','salonName','deviceName','language','source','pageUrl','serviceType','problemDescription'].sort());
   }
   const events=await p.evaluate(()=>dataLayer.filter(e=>e[0]==='event'&&e[1]==='service_lead_submit').map(e=>e[2]));
   assert.equal(events.length,1);assert.equal(events[0].language,'en');
   results.push({route,form:'PASS: validation, error, success, payload and analytics mocked'});
  }
  results.push({route,width,layout:'PASS',chat:'hidden'});
 }
 assert.deepEqual(errors,[]);await browser.close();fs.writeFileSync(path.join(out,'results.json'),JSON.stringify(results,null,2));
 console.log('PASS: 195 HTTP pages, 45 layouts, 15 mock forms, PL/RU/EN round trips, keyboard, images, gated EN sending');
})().catch(e=>{console.error(e);process.exit(1)});

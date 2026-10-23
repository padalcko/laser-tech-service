/* Stage 2B local browser audit: all external traffic blocked and webhooks mocked. */
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const fs=require('fs'),path=require('path'),assert=require('assert').strict;
const base=process.env.LTS_TEST_BASE||'http://127.0.0.1:8788';
const out=process.env.LTS_TEST_OUT||'/tmp/lts-stage2b';fs.mkdirSync(out,{recursive:true});
const registry=JSON.parse(fs.readFileSync(path.join(__dirname,'site-locales.json')));
(async()=>{
 const browser=await chromium.launch({channel:'chrome',headless:true});const results=[];
 async function setup(width=390,enableChat=false){
  const c=await browser.newContext({viewport:{width,height:900},reducedMotion:'reduce'});
  let mode='success';const requests=[],errors=[],pending=[];
  await c.route('**/*',async r=>{
   const url=r.request().url();
   if(url.includes('/webhook/')){
    requests.push({url,body:r.request().postDataJSON()});
    if(url.includes('lts-service-lead'))await new Promise(resolve=>pending.push(resolve));
    if(mode==='network')return r.abort();
    if(mode==='500')return r.fulfill({status:500,body:'error'});
    await new Promise(resolve=>setTimeout(resolve,250));
    return r.fulfill({json:url.includes('lazar-ai-chat')?{reply:'Test reply in English'}:{success:true}});
   }
   if(!url.startsWith(base+'/'))return r.abort();
   if(enableChat&&r.request().resourceType()==='document'){
    const response=await r.fetch();return r.fulfill({response,body:(await response.text()).replace('data-lazar-enabled="false"','data-lazar-enabled="true"')});
   }
   return r.continue();
  });
  const p=await c.newPage();p.on('pageerror',e=>errors.push(e.message));
  return {p,c,requests,errors,setMode:v=>mode=v,release:()=>pending.splice(0).forEach(resolve=>resolve())};
 }
 const inventory=await setup();let count=0;
 for(const group of registry.pages)for(const r of Object.values(group.routes))if(r.status==='published'){
  const response=await inventory.c.request.get(base+r.url);assert.equal(response.status(),200,r.url);count++;
 }
 assert.equal(count,195);await inventory.c.close();results.push({httpPages:count});
 for(const width of [320,390,1440])for(const route of ['/en/','/en/services/','/en/contact/']){
  const x=await setup(width),p=x.p;await p.goto(base+route);
  await p.locator('#lazar-ai-script').waitFor({state:'attached'});await p.waitForTimeout(150);
  assert.equal(await p.locator('.lazar-root').getAttribute('data-sending-enabled'),'false','EN network sending must remain disabled');assert.equal(x.requests.length,0);
  assert.equal(await p.locator('html').getAttribute('lang'),'en');
  assert.equal(await p.locator('link[rel=canonical]').getAttribute('href'),'https://lasertechservice.pl'+route);
  const group=registry.pages.find(g=>g.routes.en?.url===route);const dropdown=p.locator('.language-switcher__dropdown');
  await dropdown.locator('summary').click();
  assert.deepEqual(await dropdown.locator('a').evaluateAll(es=>es.map(e=>e.hreflang)),['pl','ru','en']);
  await p.keyboard.press('ArrowDown');assert.equal(await p.locator(':focus').getAttribute('hreflang'),'pl');
  await p.keyboard.press('Escape');assert.equal(await dropdown.evaluate(e=>e.open),false);
  if(width<760){await p.locator('.nav-toggle').click();assert.equal(await p.locator('.nav-toggle').getAttribute('aria-expanded'),'true');await p.keyboard.press('Escape');}
  const images=await p.locator('img').count();
  for(let i=0;i<images;i++){const im=p.locator('img').nth(i);if(await im.isVisible()){await im.scrollIntoViewIfNeeded();await im.evaluate(e=>e.decode());}}
  assert(!(await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth)),route+' '+width);
  const publishedEN=registry.pages.filter(g=>g.routes.en?.status==='published').map(g=>g.routes.en.url);
  const bad=await p.locator('a[href^="/en/"]').evaluateAll((es,allowed)=>es.filter(e=>!allowed.includes(new URL(e.href).pathname)).map(e=>e.href),publishedEN);assert.deepEqual(bad,[]);
  const polish=await p.locator('a[href^="/"]').evaluateAll(es=>es.filter(e=>!e.closest('.language-switcher')&&!e.pathname.startsWith('/en/')&&e.pathname.endsWith('/')).map(e=>e.textContent));
  assert(polish.every(t=>t.includes('Polish')),JSON.stringify(polish));
  for(const faq of await p.locator('.faq__question').all()){await faq.click();assert.equal(await faq.getAttribute('aria-expanded'),'true');}
  await p.evaluate(()=>scrollTo(0,0));await p.screenshot({path:path.join(out,route==='/en/'?`home-${width}.png`:`${route.split('/')[2]}-${width}.png`)});
  if(width===1440)await p.screenshot({path:path.join(out,(route==='/en/'?'home':route.split('/')[2])+'-full.png'),fullPage:true});
  await dropdown.locator('summary').click();await dropdown.locator('[hreflang=pl]').click();await p.waitForURL(base+group.routes.pl.url);
  await p.locator('.language-switcher summary').click();await p.locator('.language-switcher [hreflang=en]').click();await p.waitForURL(base+route);
  assert.deepEqual(x.errors,[]);await x.c.close();results.push({route,width,layout:'PASS',chat:'hidden'});
 }
 for(const route of ['/en/','/en/contact/']){
  const x=await setup(),p=x.p;await p.goto(base+route);const form=p.locator('.article-service-form__form');
  await form.locator('[type=submit]').click();assert.equal(x.requests.length,0);
  assert.match(await form.locator('[name=fullName]').evaluate(e=>e.validationMessage),/Please/);
  for(const [name,value] of Object.entries({fullName:'TEST',phone:'+48123456789',city:'TEST',salonName:'TEST',deviceName:'TEST'}))await form.locator(`[name=${name}]`).fill(value);
  await form.locator('[type=submit]').click();assert.equal(x.requests.length,0);
  assert.match(await form.locator('[name=consent]').evaluate(e=>e.validationMessage),/agree/);await form.locator('[name=consent]').check();
  for(const mode of ['500','success']){
   x.setMode(mode);await form.locator('[type=submit]').click();assert.equal(await form.locator('[type=submit]').innerText(),'Sending…');x.release();
   await p.waitForFunction(()=>!document.querySelector('.article-service-form__form').hasAttribute('aria-busy'));
   assert.match(await form.locator('.article-service-form__message').innerText(),mode==='success'?/Thank you/:/could not be sent/);
   assert.deepEqual(Object.keys(x.requests.at(-1).body).sort(),['fullName','phone','city','salonName','deviceName','language','source','pageUrl'].sort());
   assert.equal(x.requests.at(-1).body.language,'en');
   assert.equal(x.requests.at(-1).body.source,route==='/en/'?'en-homepage':'en-contact');
  }
  const analytics=await p.evaluate(()=>dataLayer.filter(e=>e[0]==='event'&&e[1]==='service_lead_submit').map(e=>e[2]));assert.equal(analytics.length,1);assert.equal(analytics[0].language,'en');
  await form.screenshot({path:path.join(out,route==='/en/'?'home-form.png':'contact-form.png')});
  assert.deepEqual(x.errors,[]);await x.c.close();results.push({route,form:'PASS',mockRequests:x.requests.length});
 }
 const chat=await setup(390,true);await chat.p.goto(base+'/en/contact/');await chat.p.locator('.lazar-launcher').waitFor();
 assert.equal(await chat.p.locator('.lazar-launcher-label').innerText(),'Ask Lazar');await chat.p.locator('.lazar-launcher').click();
 assert.equal(await chat.p.locator('.lazar-contacts a').nth(1).getAttribute('href'),'/en/contact/');
 for(const mode of ['500','success']){chat.setMode(mode);await chat.p.locator('.lazar-input').fill('TEST');await chat.p.locator('.lazar-send').click();await chat.p.waitForFunction(()=>document.querySelector('.lazar-form').getAttribute('aria-busy')==='false');assert.equal(chat.requests.at(-1).body.language,'en');}
 assert.equal(chat.requests[0].body.session_id,chat.requests[1].body.session_id);await chat.p.screenshot({path:path.join(out,'lazar-mock-only.png')});
 assert.deepEqual(chat.errors,[]);await chat.c.close();results.push({chat:'EN mock-only PASS'});
 await browser.close();fs.writeFileSync(path.join(out,'results.json'),JSON.stringify(results,null,2));console.log('PASS: 195 HTTP pages; nine layouts; two forms; gated EN chat with mock backend');
})().catch(e=>{console.error(e);process.exit(1)});

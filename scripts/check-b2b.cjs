/* B2B layouts and existing lead-form regression. All webhooks mocked; external traffic blocked. */
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const fs=require('fs'),path=require('path'),assert=require('assert').strict;
const registry=JSON.parse(fs.readFileSync(path.join(__dirname,'site-locales.json')));
const group=registry.pages.find(g=>g.id==='uslugi:serwis-dla-sieci-salonow');
const legacy=registry.pages.find(g=>g.id==='uslugi:serwis-pogwarancyjny');
const base=process.env.LTS_TEST_BASE||'http://127.0.0.1:8791',out=process.env.LTS_TEST_OUT||'/tmp/lts-b2b';fs.mkdirSync(out,{recursive:true});
(async()=>{
 const b=await chromium.launch({channel:'chrome',headless:true});const results=[];
 for(const [lang,route] of Object.entries(group.routes)){
  const c=await b.newContext({viewport:{width:390,height:900},reducedMotion:'reduce'});let mode='success',release;const requests=[],errors=[];
  await c.route('**/*',async r=>{
   const url=r.request().url();
   if(url==='https://n8n.raccoon-studio.com.ua/webhook/lts-service-lead'){
    requests.push(r.request().postDataJSON());
    if(mode==='pending')await new Promise(resolve=>{release=resolve;});
    if(mode==='network')return r.abort();
    if(mode==='500')return r.fulfill({status:500,body:'error'});
    if(mode==='false')return r.fulfill({json:{success:false}});
    if(mode==='json')return r.fulfill({body:'not-json'});
    return r.fulfill({json:{success:true}});
   }
   return url.startsWith(base+'/')?r.continue():r.abort();
  });
  const p=await c.newPage();p.on('pageerror',e=>errors.push(e.message));p.setDefaultTimeout(8000);
  assert.equal((await p.goto(base+route.url)).status(),200);await p.locator('.lazar-launcher').waitFor({state:'visible'});
  assert.equal(await p.locator('h1').count(),1);assert.equal(await p.locator('.lazar-root').getAttribute('data-sending-enabled'),lang==='en'?'false':'true');
  const form=p.locator('[data-b2b-form]'),submit=form.locator('[type=submit]'),message=form.locator('[role=status]');const buttonText=await submit.innerText();
  for(const width of [320,375,390,768,1024,1440]){
   await p.setViewportSize({width,height:900});await p.evaluate(()=>scrollTo(0,0));
   assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),lang+' overflow '+width);
   if(await p.locator('.nav-toggle').isVisible())await p.locator('.nav-toggle').click();
   await p.locator('.nav-submenu-toggle').click();const menu=p.locator('#servicesSubmenu');await menu.waitFor({state:'visible'});
   const entries=menu.locator('a');assert.equal(await entries.count(),2);assert.equal(await entries.nth(1).getAttribute('href'),route.url);
   assert.equal(await entries.nth(1).getAttribute('aria-current'),'page');await p.keyboard.press('Tab');await entries.nth(1).focus();assert.equal(await entries.nth(1).evaluate(e=>getComputedStyle(e).outlineStyle),'solid');
   await p.keyboard.press('Escape');if(await p.locator('.nav-toggle').getAttribute('aria-expanded')==='true')await p.keyboard.press('Escape');
   await p.locator('.language-switcher summary').click();
   for(const [l,r] of Object.entries(group.routes))assert.equal(await p.locator('.language-switcher a[lang="'+l+'"]').getAttribute('href'),r.url);
   await p.keyboard.press('Escape');
   for(const el of await form.locator('input:not([type=hidden]):not([name=companyWebsite]), select, textarea, button').all()){
    await el.evaluate(e=>e.scrollIntoView({block:'center'}));const rect=await el.boundingBox(),widget=await p.locator('.lazar-launcher').boundingBox();
    assert(rect.x>=0&&rect.x+rect.width<=width+1);
    assert(!(rect.x<widget.x+widget.width&&rect.x+rect.width>widget.x&&rect.y<widget.y+widget.height&&rect.y+rect.height>widget.y),'Lazar overlaps centred field '+lang+' '+width);
   }
   if([390,1440].includes(width)){await p.evaluate(()=>scrollTo(0,0));await p.screenshot({path:path.join(out,lang+'-'+width+'.png'),fullPage:true});}
   results.push({lang,width,layout:'PASS',menu:'PASS',lazar:'PASS'});
  }
  await p.setViewportSize({width:390,height:900});
  for(const faq of await p.locator('.faq__question').all()){await faq.focus();await faq.press('Enter');assert.equal(await faq.getAttribute('aria-expanded'),'true');await faq.press('Enter');assert.equal(await faq.getAttribute('aria-expanded'),'false');}
  await submit.evaluate(e=>e.scrollIntoView({block:'center'}));await submit.click();assert.equal(requests.length,0);
  const fill=async(contact='b2b-test@example.com')=>{
   await form.locator('[name=salonName]').fill('TEST COMPANY');await form.locator('[name=fullName]').fill('TEST CONTACT');await form.locator('[name=phone]').fill(contact);await form.locator('[name=salonCount]').selectOption('2-5');await form.locator('[name=consent]').check();
  };
  await fill('invalid');await submit.click();assert.equal(requests.length,0);assert(await form.locator('[name=phone]').evaluate(e=>!e.checkValidity()));
  await fill();await form.locator('[name=salonCount]').selectOption('');await submit.click();assert.equal(requests.length,0);await form.locator('[name=salonCount]').selectOption('2-5');
  await form.locator('[name=consent]').uncheck();await submit.click();assert.equal(requests.length,0);await form.locator('[name=consent]').check();
  await form.locator('[name=companyWebsite]').evaluate(e=>e.value='spam');await submit.click();assert.equal(requests.length,0);await form.locator('[name=companyWebsite]').evaluate(e=>e.value='');
  const eventCount=()=>p.evaluate(()=>dataLayer.filter(e=>e[0]==='event'&&e[1]==='b2b_lead_submit').length);
  for(const failure of ['500','false','json','network']){
   mode=failure;const n=requests.length;await submit.click();await p.waitForFunction(()=>!document.querySelector('[data-b2b-form]').hasAttribute('aria-busy'));
   assert.equal(requests.length,n+1);assert(await message.evaluate(e=>e.classList.contains('article-service-form__message--error')));assert.equal(await eventCount(),0);assert.equal(await form.locator('[name=salonName]').inputValue(),'TEST COMPANY');
  }
  mode='pending';const n=requests.length;await submit.click();await p.waitForFunction(()=>document.querySelector('[data-b2b-form]').hasAttribute('aria-busy'));
  while(!release)await new Promise(r=>setTimeout(r,10));assert(await submit.isDisabled());assert.equal(await message.innerText(),'');assert.equal(await eventCount(),0);
  await form.evaluate(e=>e.dispatchEvent(new Event('submit',{bubbles:true,cancelable:true})));assert.equal(requests.length,n+1);
  release();await p.waitForFunction(()=>!document.querySelector('[data-b2b-form]').hasAttribute('aria-busy'));
  assert(await message.evaluate(e=>e.classList.contains('article-service-form__message--success')));assert.equal(await eventCount(),1);assert.equal(await submit.innerText(),buttonText);
  const payload=requests.at(-1);assert.equal(payload.phone,'b2b-test@example.com');assert.equal(payload.salonName,'TEST COMPANY');assert(payload.problemDescription.includes('2-5'));assert.equal(payload.language,lang);assert.equal(payload.serviceType,'b2b-service');
  assert.deepEqual(Object.keys(payload).sort(),['fullName','phone','city','salonName','deviceName','language','source','pageUrl','serviceType','problemDescription'].sort());
  mode='success';await fill('+48 123 456 789');await form.locator('[name=deviceName]').fill('Diode, IPL');await form.locator('[name=problemDescription]').fill('TEST LOCATIONS');await submit.click();await p.waitForFunction(()=>!document.querySelector('[data-b2b-form]').hasAttribute('aria-busy'));
  assert.equal(requests.at(-1).phone,'+48 123 456 789');assert.equal(requests.at(-1).deviceName,'Diode, IPL');assert(requests.at(-1).problemDescription.includes('TEST LOCATIONS'));
  await p.locator('[data-service-cta]').first().click();const analytics=await p.evaluate(()=>dataLayer.filter(e=>e[0]==='event'&&/^b2b_/.test(e[1])).map(e=>[e[1],e[2]]));assert(analytics.some(e=>e[0]==='b2b_cta_click'));assert(!JSON.stringify(analytics).includes('TEST'));assert.equal(await eventCount(),2);
  // Existing non-B2B service forms keep the original payload and analytics event.
  await p.goto(base+legacy.routes[lang].url);const old=p.locator('.article-service-form__form');
  for(const [name,value] of Object.entries({fullName:'TEST',phone:'+48123456789',city:'TEST',deviceName:'TEST',problemDescription:'TEST'}))await old.locator('[name='+name+']').fill(value);
  await old.locator('[name=consent]').check();await old.locator('[type=submit]').evaluate(e=>e.scrollIntoView({block:'center'}));await old.locator('[type=submit]').click();await p.waitForFunction(()=>!document.querySelector('form.article-service-form__form').hasAttribute('aria-busy'));
  assert.equal(requests.at(-1).problemDescription,'TEST');assert.equal(requests.at(-1).serviceType,'postwarranty-service');assert.equal(await p.evaluate(()=>dataLayer.filter(e=>e[0]==='event'&&e[1]==='service_lead_submit').length),1);
  assert.deepEqual(errors,[]);await c.close();console.log('PASS',lang,'6 layouts, menus, FAQ, validation, honeypot, 4 failures, delayed success, email/phone, analytics, old-form regression');
 }
 const c=await b.newContext({javaScriptEnabled:false});await c.route('**/*',r=>r.request().url().startsWith(base+'/')?r.continue():r.abort());const p=await c.newPage();
 for(const route of Object.values(group.routes)){await p.goto(base+route.url);for(const faq of await p.locator('.faq__answer').all())assert(await faq.isVisible());assert(await p.locator('.article-service-form noscript').isVisible());}
 await c.close();await b.close();fs.writeFileSync(path.join(out,'browser-results.json'),JSON.stringify({results,noJS:'PASS',externalRequests:'blocked',webhook:'mocked'},null,2));
})().catch(e=>{console.error(e);process.exit(1)});

/* Local acceptance; external services blocked and Lazar responses mocked. */
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const fs=require('fs'),path=require('path'),assert=require('assert').strict;
const base=process.env.LTS_TEST_BASE||'http://127.0.0.1:8799';
const out='/tmp/lts-mobile-bar';fs.mkdirSync(out,{recursive:true});
(async()=>{
 const browser=await chromium.launch({channel:'chrome',headless:true});
 const context=await browser.newContext({viewport:{width:375,height:850},reducedMotion:'reduce'});
 let requests=0;const errors=[];
 await context.route('**/*',r=>{
  if(r.request().url().includes('/webhook/lazar-ai-chat')){requests++;return r.fulfill({json:{reply:'Mock response'}})}
  return r.request().url().startsWith(base+'/')?r.continue():r.abort();
 });
 const p=await context.newPage();p.on('pageerror',e=>errors.push(e.message));
 const registry=JSON.parse(fs.readFileSync(path.join(__dirname,'site-locales.json')));
 const routes=registry.pages.flatMap(g=>Object.entries(g.routes).filter(([,r])=>r.status==='published').map(([lang,r])=>({lang,url:r.url})));
 for(const {url,lang} of (process.argv.includes('--layouts-only') ? [] : [...routes,{url:'/404.html',lang:'pl'}])){
  await p.goto(base+url);await p.locator('.mobile-contact-bar').waitFor();
  assert.equal(await p.locator('.mobile-contact-bar').count(),1);
  assert.equal(await p.locator('.mobile-contact-bar__action').count(),4);
  assert.equal(await p.locator('[data-action=phone]').textContent(),{pl:'Zadzwoń',ru:'Позвонить',en:'Call'}[lang]);
 }
 if (!process.argv.includes('--layouts-only')) console.log('PASS all '+(routes.length+1)+' routes');
 for(const lang of ['pl','ru','en'])for(const width of [320,360,375,390,430,767,768,1024,1440]){
  await p.setViewportSize({width,height:850});await p.goto(base+(lang==='pl'?'/':'/'+lang+'/'));await p.waitForSelector('#lazar-root', {state:'attached'});
  const bar=p.locator('.mobile-contact-bar'),mobile=width<768;
  assert.equal(await bar.isVisible(),mobile);assert.equal(await p.locator('.lazar-launcher').isVisible(),!mobile);
  if(mobile){
   assert.equal(await p.locator('[data-action=phone]').getAttribute('href'),'tel:+48790402597');
   assert.equal(await p.locator('[data-action=whatsapp]').getAttribute('href'),'https://wa.me/48790402597');
   assert.equal(await p.locator('[data-action=instagram]').getAttribute('href'),'https://www.instagram.com/lasertech.service/');
   assert.equal(await p.locator('[data-action=instagram]').getAttribute('rel'),'noopener noreferrer');
   const geometry=await bar.evaluate(e=>({rect:e.getBoundingClientRect().toJSON(),controls:[...e.children].map(c=>({w:c.clientWidth,h:c.clientHeight,scroll:c.scrollWidth})),overflow:document.documentElement.scrollWidth>innerWidth}));
   assert(!geometry.overflow);assert(geometry.rect.x>=0&&geometry.rect.right<=width&&geometry.rect.bottom<=850);
   geometry.controls.forEach(c=>assert(c.w>=44&&c.h>=44&&c.scroll<=c.w));
   await p.evaluate(()=>scrollTo(0,document.body.scrollHeight));assert.equal((await bar.boundingBox()).y,geometry.rect.y);
   await p.evaluate(()=>scrollTo(0,0));
   if([375,430].includes(width))await p.screenshot({path:out+'/'+lang+'-'+width+'.png'});
   // Prevent navigation only in the test; retain the real click handlers.
   await bar.evaluate(e=>e.addEventListener('click',ev=>ev.preventDefault()));
   for(const action of ['phone','whatsapp','instagram','lazar'])await p.locator('[data-action='+action+']').click();
   assert(await p.locator('#lazar-panel').isVisible());assert(await bar.isVisible());
   const events=await p.evaluate(()=>dataLayer.filter(e=>e[0]==='event'&&e[1]==='mobile_contact_click').map(e=>e[2]));
   assert.deepEqual(events.map(e=>e.action),['phone','whatsapp','instagram','lazar']);events.forEach(e=>{assert.equal(e.language,lang);assert.equal(e.placement,'mobile_bottom_bar')});
   await p.locator('.lazar-input').fill('Local mocked test');await p.locator('.lazar-send').click();await p.waitForFunction(()=>document.querySelector('.lazar-log').textContent.includes('Mock response'));
   await p.keyboard.press('Escape');assert(await bar.isVisible());assert.equal(await p.evaluate(()=>document.activeElement.dataset.action),'lazar');
   if(width<761){await p.locator('.nav-toggle').click();assert(await bar.isVisible());await p.locator('.nav-toggle').click();assert(await bar.isVisible())}
   await p.evaluate(()=>{const d=document.createElement('dialog');d.id='qa-dialog';document.body.append(d);d.showModal()});assert(await bar.isVisible());await p.evaluate(()=>document.getElementById('qa-dialog').remove());assert(await bar.isVisible());
  }else{await p.locator('.lazar-launcher').click();assert(await p.locator('#lazar-panel').isVisible());await p.locator('.lazar-close').click()}
 }
 // Landscape/keyboard-sized viewport: chat input remains inside visible area.
 for(const size of [{width:667,height:375},{width:375,height:300}]){
  await p.setViewportSize(size);await p.goto(base+'/');await p.locator('[data-action=lazar]').click();
  const r=await p.locator('.lazar-input').boundingBox();assert(r.y>=0&&r.y+r.height<=size.height);
 }
 await p.goto(base+'/404.html');
 for(const lang of ['ru','en','pl']){await p.evaluate(l=>{document.documentElement.lang=l;document.dispatchEvent(new CustomEvent('error-language-change'))},lang);assert.equal(await p.locator('.mobile-contact-bar').count(),1);assert.equal(await p.locator('[data-action=lazar]').textContent(),{pl:'Łazarz',ru:'Лазарь',en:'Lazar'}[lang])}
 assert.deepEqual(errors,[]);await browser.close();
 fs.writeFileSync(out+'/results.json',JSON.stringify({routes:routes.length+1,routeSweep:!process.argv.includes('--layouts-only'),layouts:27,requests,errors,landscape:true,keyboardSizedViewport:true},null,2));
 console.log('PASS 27 layouts, analytics once per click, mock chat, focus, persistent bar with menu/modal, landscape, 404 locales; no JS errors');
})().catch(e=>{console.error(e);process.exit(1)});

/* V2 acceptance: all external traffic blocked, webhook mocked, artifacts outside publish root. */
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const fs=require('fs'),path=require('path'),assert=require('assert').strict;
const base=process.env.LTS_TEST_BASE||'http://127.0.0.1:8788',out=process.env.LAZAR_TEST_OUT||'/tmp/lts-lazar-v2';
fs.mkdirSync(out,{recursive:true});
const registry=JSON.parse(fs.readFileSync(path.join(__dirname,'site-locales.json')));
const home=registry.pages.find(g=>g.type==='home'),contact=registry.pages.find(g=>g.type==='contact');
const routes=registry.pages.flatMap(g=>Object.entries(g.routes).filter(([,r])=>r.status==='published').map(([lang,r])=>({lang,url:r.url})));
(async()=>{
 const browser=await chromium.launch({channel:'chrome',headless:true});const results=[];
 async function setup(approved=false,width=390,mismatch=false){
  const c=await browser.newContext({viewport:{width,height:900},reducedMotion:'reduce'});const requests=[],errors=[];let mode='success';
  await c.route('**/*',async r=>{
   const u=r.request().url();
   if(u.includes('/webhook/')){assert(u.endsWith('/lazar-ai-chat'));requests.push(r.request().postDataJSON());return r.fulfill(mode==='success'?{json:{reply:'MOCK technical response'}}:{status:500,body:'private backend error'});}
   if(!u.startsWith(base+'/'))return r.abort();
   if((approved||mismatch)&&r.request().resourceType()==='document'){
    const response=await r.fetch();let body=await response.text();
    if(approved)body=body.replace('data-lazar-enabled="false"','data-lazar-enabled="true"');
    if(mismatch)body=body.replace('lang="en"','lang="ru"');
    return r.fulfill({response,body});
   }
   return r.continue();
  });
  const p=await c.newPage();p.on('pageerror',e=>errors.push(e.message));return {c,p,requests,errors,mode:v=>mode=v};
 }
 const live=await setup();
 for(const r of routes){
  await live.p.goto(base+r.url);assert.equal(await live.p.locator('.lazar-root').count(),1);
  assert.equal(await live.p.locator('.lazar-root').getAttribute('data-sending-enabled'),String(r.lang!=='en'));
  await live.p.locator('.lazar-launcher').click();assert.equal(await live.p.locator('.lazar-quick-question').count(),3);
  assert.equal(await live.p.locator('.lazar-contacts a').nth(1).getAttribute('href'),contact.routes[r.lang].url+(r.lang==='en'?'':'#contactid'));
  if(r.lang==='en'){
   await live.p.locator('.lazar-quick-question').first().click();const draft=await live.p.locator('.lazar-input').inputValue();
   await live.p.locator('.lazar-send').click();await live.p.locator('.lazar-retry').click();assert.equal(await live.p.locator('.lazar-input').inputValue(),draft);
   assert.equal(await live.p.locator('.lazar-message--system').count(),1);assert.equal(await live.p.locator('.lazar-message--user').count(),0);
  }
 }
 assert.equal(live.requests.length,0);assert.deepEqual(live.errors,[]);results.push({allPublished:routes.length,visible:true,enProductionSending:'blocked',requests:0});await live.c.close();console.log('PASS all published routes and EN gate');
 const geometry={};
 for(const width of [320,390,768,1024,1440,1920])for(const lang of ['pl','ru','en']){
  const x=await setup(true,width),{p}=x;await p.goto(base+home.routes[lang].url);
  if([390,1440].includes(width))await p.screenshot({path:path.join(out,`${lang}-${width}-closed.png`)});
  await p.locator('.lazar-launcher').focus();await p.keyboard.press('Enter');
  const panel=await p.locator('.lazar-panel').boundingBox();const size=[panel.width,panel.height];
  if(geometry[width])assert.deepEqual(size,geometry[width]);else geometry[width]=size;
  assert(panel.x>=0&&panel.x+panel.width<=width&&panel.y>=0&&panel.y+panel.height<=900);
  assert.equal(await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
  for(const b of await p.locator('.lazar-quick-question').all()){
   await b.focus();await p.keyboard.press('Enter');assert((await p.locator('.lazar-input').inputValue()).length>30);assert.equal(x.requests.length,0);assert((await b.boundingBox()).height>=44);
  }
  if([390,1440].includes(width))await p.screenshot({path:path.join(out,`${lang}-${width}-quick.png`)});
  await p.locator('.lazar-input').fill('Edited TEST');await p.locator('.lazar-send').click();await p.waitForFunction(()=>document.querySelector('.lazar-form').getAttribute('aria-busy')==='false');
  assert.equal(x.requests.length,1);assert.equal(x.requests[0].message,'Edited TEST');assert.equal(x.requests[0].language,lang);
  assert.equal(await p.locator('.lazar-quick').isVisible(),false);
  await p.locator('.lazar-input').focus();await p.keyboard.press('Escape');await p.locator('.lazar-launcher').click();assert.equal(await p.locator('.lazar-quick').isVisible(),false);
  x.mode('error');await p.locator('.lazar-input').fill('Failure TEST');await p.locator('.lazar-send').click();await p.waitForFunction(()=>document.querySelector('.lazar-form').getAttribute('aria-busy')==='false');
  assert.equal(await p.locator('.lazar-message--system').count(),1);assert.equal(await p.locator('.lazar-message--system .lazar-avatar').count(),0);
  const lastContact=await p.locator('.lazar-message--system .lazar-contacts').boundingBox(),logBox=await p.locator('.lazar-log').boundingBox();assert(lastContact.y+lastContact.height<=logBox.y+logBox.height+1,'Fallback contacts must be scrolled into view');
  if([390,1440].includes(width))await p.screenshot({path:path.join(out,`${lang}-${width}-error.png`)});
  const events=await p.evaluate(()=>dataLayer.filter(e=>e.event?.startsWith('lazar_')));
  assert.equal(events.filter(e=>e.event==='lazar_message_sent').length,2);assert.equal(events.filter(e=>e.event==='lazar_error').length,1);assert(!JSON.stringify(events).includes('TEST'));
  assert.deepEqual(x.errors,[]);results.push({lang,width,size,result:'PASS'});await x.c.close();
 }
 // Same-language sessions survive navigation; language contexts do not mix.
 const x=await setup(true);const ids={};await x.c.addInitScript(()=>{if(!sessionStorage.getItem('legacy-seeded')){sessionStorage.setItem('lazar-session-id','legacy-session-1234567890');sessionStorage.setItem('legacy-seeded','yes');}});
 for(const lang of ['pl','ru','en','pl']){
  await x.p.goto(base+home.routes[lang].url);await x.p.locator('.lazar-launcher').click();assert(await x.p.locator('.lazar-quick').isVisible());
  await x.p.locator('.lazar-input').fill('Session TEST');await x.p.locator('.lazar-send').click();await x.p.waitForFunction(()=>document.querySelector('.lazar-form').getAttribute('aria-busy')==='false');
  const id=x.requests.at(-1).session_id;if(ids[lang])assert.equal(ids[lang],id);else ids[lang]=id;
 }
 assert.equal(ids.pl,'legacy-session-1234567890');assert.equal(new Set(Object.values(ids)).size,3);assert.deepEqual(x.errors,[]);await x.c.close();results.push({sessionIsolation:'PASS',legacyAdoption:'PASS'});
 const mismatch=await setup(true,390,true);await mismatch.p.goto(base+'/en/');await mismatch.p.locator('.lazar-launcher').click();await mismatch.p.locator('.lazar-input').fill('TEST');await mismatch.p.locator('.lazar-send').click();assert.equal(mismatch.requests.length,0);assert.equal(await mismatch.p.locator('.lazar-root').getAttribute('data-sending-enabled'),'false');await mismatch.c.close();
 const gated=await setup();for(const width of [390,1440]){await gated.p.setViewportSize({width,height:900});await gated.p.goto(base+'/en/');await gated.p.locator('.lazar-launcher').click();await gated.p.screenshot({path:path.join(out,`en-${width}-production-fallback.png`)});}assert.equal(gated.requests.length,0);await gated.c.close();
 await browser.close();fs.writeFileSync(path.join(out,'v2-results.json'),JSON.stringify(results,null,2));console.log('PASS',routes.length,'published routes; 18 layouts; quick questions; EN gate; language sessions; mismatch gate');
})().catch(e=>{console.error(e);process.exit(1)});

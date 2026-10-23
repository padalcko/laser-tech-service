/* All published routes: local browser only; every external request is blocked. */
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const fs=require('fs'),path=require('path'),assert=require('assert').strict;
const registry=JSON.parse(fs.readFileSync(path.join(__dirname,'site-locales.json')));
const routes=registry.pages.flatMap(g=>Object.entries(g.routes).filter(([,r])=>r.status==='published').map(([language,r])=>({url:r.url,language,type:g.type})));
routes.push({url:'/404.html',language:'pl',type:'404'});
const base=process.env.LTS_TEST_BASE||'http://127.0.0.1:8788',out=process.env.LTS_TEST_OUT||'/tmp/lts-final-v1';fs.mkdirSync(out,{recursive:true});
const selected=new Set(['/en/','/en/pricing/','/en/partners/','/en/services/','/en/services/diode-laser-diagnostics/','/en/services/co2-laser-service/','/en/services/laser-handpiece-repair/','/','/ru/','/404.html']);
(async()=>{
 const b=await chromium.launch({channel:'chrome',headless:true});const c=await b.newContext({reducedMotion:'reduce'});const errors=[],issues=[],results=[];
 await c.route('**/*',r=>r.request().url().startsWith(base+'/')?r.continue():r.abort());
 const p=await c.newPage();p.on('pageerror',e=>errors.push({url:p.url(),message:e.message}));p.setDefaultTimeout(7000);
 for(const route of routes){
  try{
   await p.setViewportSize({width:390,height:900});const response=await p.goto(base+route.url,{waitUntil:'load'});assert.equal(response.status(),200);
   assert.equal(await p.locator('html').getAttribute('lang'),route.language);assert.equal(await p.locator('h1').count(),1);
   // Load every lazy image once before the viewport matrix.
   for(const im of await p.locator('img').all())if(await im.isVisible()){await im.evaluate(e=>{e.scrollIntoView({block:'center'});return e.decode();});}
   const gallery=p.locator('.case-gallery--compact a, .case-photo--compact a');
   if(await gallery.count()){await gallery.first().click();await p.locator('.case-photo-dialog').waitFor({state:'visible'});await p.keyboard.press('Escape');await p.locator('.case-photo-dialog').waitFor({state:'hidden'});}
   for(const faq of await p.locator('.faq__question').all()){
    await faq.focus();await p.keyboard.press('Enter');assert.equal(await faq.getAttribute('aria-expanded'),'true');await faq.click();assert.equal(await faq.getAttribute('aria-expanded'),'false');
   }
   if(route.language==='en')assert.equal(await p.locator('.lazar-root').getAttribute('data-sending-enabled'),'false');
   for(const width of [320,390,768,1024,1440,1920]){
    await p.setViewportSize({width,height:900});await p.evaluate(()=>scrollTo(0,0));await p.waitForTimeout(30);
    const overflow=await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth+1);
    if(overflow)issues.push({route:route.url,width,issue:'horizontal overflow'});
    const d=p.locator('.language-switcher__dropdown'),toggle=d.locator('summary');
    assert.equal(await toggle.locator('svg').count(),1);
    if(width===320||width===1440){
     await toggle.click();await p.waitForFunction(()=>document.querySelector('.language-switcher summary').getAttribute('aria-expanded')==='true');
     await p.keyboard.press('ArrowDown');assert(await p.locator(':focus').getAttribute('hreflang'));
     await p.keyboard.press('Escape');assert.equal(await d.evaluate(e=>e.open),false);
     assert((await toggle.boundingBox()).height>=44);
     if(await p.locator('.nav-toggle').isVisible()){await p.locator('.nav-toggle').click();assert.equal(await p.locator('.nav-toggle').getAttribute('aria-expanded'),'true');await p.keyboard.press('Escape');assert.equal(await p.locator('.nav-toggle').getAttribute('aria-expanded'),'false');}
    }
    if(selected.has(route.url)&&[320,390,1440].includes(width)){
     const slug=route.url==='/'?'pl-home':route.url.replace(/^\//,'').replace(/\/$/,'').replaceAll('/','-');
     await p.screenshot({path:path.join(out,slug+'-'+width+'.png')});
     if(width===1440)await p.screenshot({path:path.join(out,slug+'-full.png'),fullPage:true});
    }
    results.push({route:route.url,width,overflow});
   }
   if(route.type==='pricing'){
    const input=p.locator('#travel-km');await input.fill('100');const value=await p.locator('#travel-result').innerText();
    assert(route.language==='en'?/100/.test(value)&&/€|EUR/.test(value):/140/.test(value));
    await input.fill('10001');assert.equal(await input.getAttribute('aria-invalid'),'true');
    await input.fill('0.01');assert.equal(await input.getAttribute('aria-invalid'),null);
   }
   console.log('PASS',route.url);
  }catch(e){issues.push({route:route.url,issue:e.message});console.log('FAIL',route.url,e.message);}
 }
 await b.close();fs.writeFileSync(path.join(out,'results.json'),JSON.stringify({routes:routes.length,layouts:results,issues,errors,externalRequests:'blocked'},null,2));
 assert.deepEqual(issues,[]);assert.deepEqual(errors,[]);console.log('PASS',routes.length,'routes',results.length,'layouts');
})().catch(e=>{console.error(e);process.exit(1)});

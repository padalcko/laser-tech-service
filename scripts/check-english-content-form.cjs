/* Stage 3C article form; external traffic blocked, webhook mocked. */
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const fs=require('fs'),path=require('path'),assert=require('assert').strict;
const base=process.env.LTS_TEST_BASE||'http://127.0.0.1:8788';
const out=process.env.LTS_TEST_OUT||'/tmp/lts-stage3c-form';fs.mkdirSync(out,{recursive:true});
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
 for(const route of ['/en/blog/why-laser-diode-modules-fail/']){
  const x=await setup(),p=x.p;await p.goto(base+route);const form=p.locator('.article-service-form__form');
  await form.locator('[type=submit]').click();assert.equal(x.requests.length,0);
  assert.match(await form.locator('[name=fullName]').evaluate(e=>e.validationMessage),/Please/);
  for(const [name,value] of Object.entries({fullName:'TEST',phone:'+48123456789',city:'TEST',salonName:'TEST',deviceName:'TEST'}))await form.locator(`[name=${name}]`).fill(value);
  for(const mode of ['500','success']){
   x.setMode(mode);await form.locator('[type=submit]').click();assert.equal(await form.locator('[type=submit]').innerText(),'Sending…');x.release();
   await p.waitForFunction(()=>!document.querySelector('.article-service-form__form').hasAttribute('aria-busy'));
   assert.match(await form.locator('.article-service-form__message').innerText(),mode==='success'?/Thank you/:/could not be sent/);
   assert.deepEqual(Object.keys(x.requests.at(-1).body).sort(),['fullName','phone','city','salonName','deviceName','language','source','pageUrl'].sort());
   assert.equal(x.requests.at(-1).body.language,'en');
   assert.equal(x.requests.at(-1).body.source,'blog-dlaczego-pala-sie-moduly-diodowe');
  }
  const analytics=await p.evaluate(()=>dataLayer.filter(e=>e[0]==='event'&&e[1]==='service_lead_submit').map(e=>e[2]));assert.equal(analytics.length,1);assert.equal(analytics[0].language,'en');
  await form.screenshot({path:path.join(out,'article-form.png')});
  assert.deepEqual(x.errors,[]);await x.c.close();results.push({route,form:'PASS',mockRequests:x.requests.length});
 }
 await browser.close();fs.writeFileSync(path.join(out,'results.json'),JSON.stringify(results,null,2));console.log('PASS: EN article form validation, loading, failure/success, exact payload and analytics with mock webhook');
})().catch(e=>{console.error(e);process.exit(1)});

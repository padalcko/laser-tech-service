/* Every published lead form: mock only, no external traffic. */
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const fs=require('fs'),path=require('path'),assert=require('assert').strict;
const root=path.resolve(__dirname,'..'),base=process.env.LTS_TEST_BASE||'http://127.0.0.1:8788',out=process.env.LTS_TEST_OUT||'docs/qa/final-v1';fs.mkdirSync(out,{recursive:true});
const registry=JSON.parse(fs.readFileSync(path.join(__dirname,'site-locales.json')));
const routes=registry.pages.flatMap(g=>Object.entries(g.routes).filter(([,r])=>r.status==='published').map(([language,r])=>({url:r.url,language}))).filter(r=>fs.readFileSync(path.join(root,r.url,'index.html'),'utf8').includes('<form'));
(async()=>{
 const browser=await chromium.launch({channel:'chrome',headless:true}),results=[];
 for(const route of routes){
  const c=await browser.newContext({viewport:{width:390,height:900},reducedMotion:'reduce'});let mode='error',release;const requests=[],errors=[];
  await c.route('**/*',async r=>{
   if(r.request().url().includes('/webhook/')){
    assert(r.request().url().endsWith('/lts-service-lead'));requests.push(r.request().postDataJSON());await new Promise(resolve=>release=resolve);
    return r.fulfill(mode==='error'?{status:500,body:'error'}:{json:{success:true}});
   }
   return r.request().url().startsWith(base+'/')?r.continue():r.abort();
  });
  const p=await c.newPage();p.on('pageerror',e=>errors.push(e.message));await p.goto(base+route.url);const form=p.locator('.article-service-form__form');assert.equal(await form.count(),1);
  await form.locator('[type=submit]').click();assert.equal(requests.length,0);
  const expected=await form.evaluate(f=>Object.fromEntries(new FormData(f)));
  for(const input of await form.locator('input:not([type=hidden]):not([type=checkbox]),textarea').all()){
   if(!(await input.isVisible())||await input.getAttribute('name')==='companyWebsite')continue;
   const name=await input.getAttribute('name');if(!name)continue;await input.fill(name==='phone'?'+48123456789':'TEST ONLY');
  }
  for(const box of await form.locator('[type=checkbox][required]').all())await box.check();
  const fields=await form.evaluate(f=>Object.fromEntries(new FormData(f)));
  for(mode of ['error','success']){
   await form.locator('[type=submit]').click();await p.waitForFunction(()=>document.querySelector('form.article-service-form__form').getAttribute('aria-busy')==='true');
   assert(await form.locator('[type=submit]').isDisabled());
   const count=requests.length;await form.evaluate(f=>f.dispatchEvent(new Event('submit',{bubbles:true,cancelable:true})));await p.waitForTimeout(50);assert.equal(requests.length,count,'double submit');
   assert(release);release();await p.waitForFunction(()=>!document.querySelector('form.article-service-form__form').hasAttribute('aria-busy'));
   assert(await form.locator('.article-service-form__message--'+(mode==='error'?'error':'success')).isVisible());
   const payload=requests.at(-1);assert.equal(payload.language,route.language);assert.equal(payload.source,expected.source||'website');assert.equal(payload.pageUrl,base+route.url);
   for(const name of ['fullName','phone','city','salonName','deviceName','serviceType','problemDescription'])if(name in fields)assert.equal(payload[name],fields[name]);
   assert(!('consent' in payload)&&!('companyWebsite' in payload));
  }
  assert.equal(await p.evaluate(()=>dataLayer.filter(e=>e[0]==='event'&&e[1]==='service_lead_submit').length),1);
  assert.deepEqual(errors,[]);results.push({...route,requests:requests.length,result:'PASS'});console.log('PASS',route.url);await c.close();
 }
 await browser.close();fs.writeFileSync(path.join(out,'forms.json'),JSON.stringify(results,null,2));console.log('PASS',results.length,'forms');
})().catch(e=>{console.error(e);process.exit(1)});

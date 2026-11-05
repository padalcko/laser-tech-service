/* Local QA; third-party requests blocked to avoid analytics and service calls. */
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const fs=require('fs'),path=require('path'),assert=require('assert').strict;
const routes=JSON.parse(fs.readFileSync(path.join(__dirname,'../content/warsaw-808-routes.json')));
const base=process.env.LTS_TEST_BASE||'http://127.0.0.1:8799',out=process.env.LTS_TEST_OUT||'/tmp/lts-warsaw-808';
(async()=>{
const browser=await chromium.launch({channel:'chrome',headless:true});
const ctx=await browser.newContext({reducedMotion:'reduce'});await ctx.route('**/*',r=>r.request().url().startsWith(base+'/')?r.continue():r.abort());
await ctx.addInitScript(()=>{window.qa={cls:0,lcp:0};new PerformanceObserver(l=>{for(const e of l.getEntries())if(!e.hadRecentInput)window.qa.cls+=e.value}).observe({type:'layout-shift',buffered:true});new PerformanceObserver(l=>{for(const e of l.getEntries())window.qa.lcp=e.startTime}).observe({type:'largest-contentful-paint',buffered:true});});
const p=await ctx.newPage(),errors=[],results=[],metrics=[],badResponses=[];p.on('pageerror',e=>errors.push(e.message));p.on('response',r=>{if(r.url().startsWith(base)&&r.status()>=400)badResponses.push([r.status(),r.url()])});
for(const [kind,langs] of Object.entries(routes))for(const [lang,url] of Object.entries(langs)){
 for(const width of [320,375,430,768,1440]){
  await p.setViewportSize({width,height:900});assert.equal((await p.goto(base+url)).status(),200);await p.locator('.lazar-launcher').waitFor({state:'visible'});
  assert.equal(await p.locator('h1').count(),1);assert.equal(await p.locator('main img').count(),kind==='case'?11:4);
  await p.waitForTimeout(350);const initial=await p.evaluate(()=>({...window.qa}));metrics.push({url,width,...initial});
  assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),`Overflow ${url} ${width}`);
  await p.locator('.language-switcher summary').click();for(const [l,u] of Object.entries(langs))assert.equal(await p.locator('.language-switcher a[lang='+l+']').getAttribute('href'),u);await p.keyboard.press('Escape');
  if(width<=430){const burger=p.locator('.nav-toggle');await burger.click();assert.equal(await burger.getAttribute('aria-expanded'),'true');await burger.click();assert.equal(await burger.getAttribute('aria-expanded'),'false');}
  for(const im of await p.locator('main img').all()){await im.evaluate(async e=>{e.scrollIntoView({block:'center'});await e.decode()});assert(await im.evaluate(e=>e.naturalWidth>0 && e.currentSrc.endsWith('.webp')));}
  if(kind==='case'&&width===375){for(const a of await p.locator('.case-photo--compact a,.case-gallery a').all()){await a.click();await p.locator('.case-photo-dialog').waitFor({state:'visible'});await p.locator('.case-photo-dialog img').evaluate(e=>e.decode());await p.keyboard.press('Escape');await p.locator('.case-photo-dialog').waitFor({state:'hidden'});}}
  await p.evaluate(()=>scrollTo(0,0));if([375,1440].includes(width))await p.screenshot({path:path.join(out,kind+'-'+lang+'-'+width+'.png'),fullPage:true});
  results.push({url,width,overflow:false,photos:kind==='case'?11:4});
 }
 console.log('PASS',url);
}
for(const langs of Object.values(routes))for(const [from,url] of Object.entries(langs))for(const [to,peer] of Object.entries(langs)){if(from===to)continue;await p.goto(base+url);await p.locator('.language-switcher summary').click();await p.locator('.language-switcher a[lang='+to+']').click();await p.waitForURL(base+peer);assert.equal(await p.locator('html').getAttribute('lang'),to);}
for(const [kind,langs] of Object.entries(routes))for(const url of Object.values(langs)){const hub=url.split('/').slice(0,-2).join('/')+'/';await p.setViewportSize({width:320,height:900});assert.equal((await p.goto(base+hub)).status(),200);assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));const card=p.locator(kind==='case'?'.realizacja-card':'.blog-card').first();assert.equal(await card.locator('img').count(),kind==='case'?1:0);assert.equal(await card.locator('a').first().getAttribute('href'),url);await card.locator('a').first().click();await p.waitForURL(base+url);}
assert.deepEqual(errors,[]);assert.deepEqual(badResponses,[]);
fs.writeFileSync(path.join(out,'browser-results.json'),JSON.stringify({results,metrics,errors,badResponses,languageTransitions:12,galleryDialogs:33,externalRequests:'blocked'},null,2));await browser.close();console.log('PASS: 30 layouts; 225 photo loads; 33 gallery dialogs; 12 language transitions; 18 mobile menu checks; six catalogue cards; no JS errors or local HTTP errors');
})().catch(e=>{console.error(e);process.exit(1)});

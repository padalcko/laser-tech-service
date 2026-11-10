/* Local browser QA; external services blocked, no forms submitted. */
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const fs=require('fs'),path=require('path'),assert=require('assert').strict;
const routes=JSON.parse(fs.readFileSync(path.join(__dirname,'../content/pure-studio-routes.json')));
const base=process.env.LTS_TEST_BASE||'http://127.0.0.1:8793',out=process.env.LTS_TEST_OUT||'/tmp/lts-pure';
(async()=>{
 const browser=await chromium.launch({channel:'chrome',headless:true});const ctx=await browser.newContext({reducedMotion:'reduce'});
 await ctx.route('**/*',r=>r.request().url().startsWith(base+'/')?r.continue():r.abort());
 await ctx.addInitScript(()=>{window.qa={cls:0,shifts:[]};new PerformanceObserver(l=>{for(const e of l.getEntries())if(!e.hadRecentInput){window.qa.cls+=e.value;window.qa.shifts.push({value:e.value,sources:(e.sources||[]).map(s=>s.node?.className||s.node?.nodeName)})}}).observe({type:'layout-shift',buffered:true})});
 const p=await ctx.newPage(),errors=[],bad=[],results=[];p.on('pageerror',e=>errors.push(e.message));p.on('response',r=>{if(r.url().startsWith(base)&&r.status()>=400)bad.push([r.status(),r.url()])});
 for(const [kind,langs] of Object.entries(routes))for(const [lang,url] of Object.entries(langs)){
  for(const width of [320,360,375,390,430,768,1024,1440]){
   await p.setViewportSize({width,height:900});assert.equal((await p.goto(base+url)).status(),200);await p.locator('#lazar-root').waitFor({state:'attached'});
   assert.equal(await p.locator('h1').count(),1);assert.equal(await p.locator('main img').count(),kind==='case'?4:5);
   assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),`overflow ${url} ${width}`);
   for(const im of await p.locator('main img').all()){await im.evaluate(async e=>{e.scrollIntoView({block:'center'});await e.decode()});assert(await im.evaluate(e=>e.naturalWidth>0&&e.getBoundingClientRect().right<=innerWidth+1));}
   await p.locator('.language-switcher summary').click();for(const [l,u] of Object.entries(langs))assert.equal(await p.locator('.language-switcher a[lang='+l+']').getAttribute('href'),u);await p.locator('.language-switcher summary').click();
   if(width<=430){await p.locator('.nav-toggle').click();assert.equal(await p.locator('.nav-toggle').getAttribute('aria-expanded'),'true');await p.locator('.nav-toggle').click();}
   if(width===375){await p.locator('.mobile-contact-bar [data-action="lazar"]').click();await p.locator('.lazar-panel').waitFor({state:'visible'});await p.keyboard.press('Escape');
    if(kind==='case')for(const a of await p.locator('.case-work-image a').all()){await a.click();await p.locator('.case-photo-dialog').waitFor({state:'visible'});await p.locator('.case-photo-dialog img').evaluate(e=>e.decode());await p.keyboard.press('Escape');}
   }
   await p.locator(kind==='case'?'.realizacje-cta':'.article-cta').scrollIntoViewIfNeeded();assert(await p.locator(kind==='case'?'.realizacje-cta':'.article-cta').isVisible());
   await p.evaluate(()=>scrollTo(0,0));await p.waitForTimeout(150);results.push({kind,lang,width,cls:await p.evaluate(()=>window.qa.cls),shifts:await p.evaluate(()=>window.qa.shifts)});
   if([375,1440].includes(width))await p.screenshot({path:path.join(out,kind+'-'+lang+'-'+width+'.png'),fullPage:true});
  }console.log('PASS',url);
 }
 for(const langs of Object.values(routes))for(const [from,url] of Object.entries(langs))for(const [to,peer] of Object.entries(langs)){if(from===to)continue;await p.goto(base+url);await p.locator('.language-switcher summary').click();await p.locator('.language-switcher a[lang='+to+']').click();await p.waitForURL(base+peer);}
 for(const [lang,url] of Object.entries({pl:'/partnerzy/',ru:'/ru/partnerzy/',en:'/en/partners/'}))for(const width of [320,360,375,390,430,768,1024,1440]){
  await p.setViewportSize({width,height:900});await p.goto(base+url);assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));assert.equal(await p.locator('.partner-card').count(),11);const first=p.locator('.partner-card').first();assert.equal(await first.getAttribute('href'),'https://www.instagram.com/pure.wro/');await first.locator('img').evaluate(e=>e.decode());if([375,1440].includes(width))await p.screenshot({path:path.join(out,'partners-'+lang+'-'+width+'.png'),fullPage:true});
 }
 for(const [kind,langs] of Object.entries(routes))for(const url of Object.values(langs)){await p.goto(base+url.split('/').slice(0,-2).join('/')+'/');const card=p.locator(kind==='case'?'.realizacja-card':'.blog-card').first();assert.equal(await card.locator('a').first().getAttribute('href'),url);await card.locator('a').first().click();await p.waitForURL(base+url);}
 assert.deepEqual(errors,[]);assert.deepEqual(bad,[]);fs.writeFileSync(path.join(out,'browser-results.json'),JSON.stringify({results,errors,bad,languageTransitions:12,partnerLayouts:24,externalRequests:'blocked'},null,2));await browser.close();console.log('PASS 48 content layouts + 24 partner layouts, 12 language transitions, photo dialogs, menu, Lazar, CTA; no JS/local HTTP errors');
})().catch(e=>{console.error(e);process.exit(1)});

/* Local full-catalogue layout QA. External requests are blocked. */
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const fs=require('fs'),path=require('path'),assert=require('assert/strict');
const root=path.resolve(__dirname,'..'),base=process.env.LTS_TEST_BASE||'http://127.0.0.1:8799';
const routes=['realizacje','ru/realizacje','en/case-studies'].flatMap(dir=>fs.readdirSync(path.join(root,dir),{withFileTypes:true}).filter(e=>e.isDirectory()&&fs.existsSync(path.join(root,dir,e.name,'index.html'))).map(e=>'/'+dir+'/'+e.name+'/'));
(async()=>{
 const browser=await chromium.launch({channel:'chrome',headless:true});
 const ctx=await browser.newContext({reducedMotion:'reduce'});
 await ctx.route('**/*',r=>r.request().url().startsWith(base+'/')?r.continue():r.abort());
 const p=await ctx.newPage(),errors=[],failures=[],results=[];
 p.on('pageerror',e=>errors.push(e.message));
 for(const route of routes.filter(r=>!process.env.CASE_ROUTE||new RegExp(process.env.CASE_ROUTE).test(r))){
  for(const width of [320,768,1440]){
   await p.setViewportSize({width,height:900});assert.equal((await p.goto(base+route)).status(),200);
   await p.locator('main img').evaluateAll(async images=>{for(const im of images){im.loading='eager';await im.decode();}});
   const state=await p.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth+1,hero:!!document.querySelector('[data-case-layout="pharaon"] .case-hero__grid'),images:[...document.querySelectorAll('main img')].every(i=>i.naturalWidth>0),grids:[...document.querySelectorAll('.case-work-grid')].map(g=>({columns:getComputedStyle(g).gridTemplateColumns.split(' ').length,imageFirst:g.firstElementChild.classList.contains('case-work-image')}))}));
   if(state.overflow||!state.hero||!state.images||state.grids.some(g=>!g.imageFirst||g.columns!==(width<=900?1:2)))failures.push({route,width,state});
   results.push({route,width});
  }
  console.log('CHECK',route);
 }
 for(const route of ['/realizacje/naprawa-chlodzenia-lightsheer-desire-wroclaw/','/realizacje/nubway-nbw-vsiii-naprawa-zaworu-podcisnienia-wroclaw/','/realizacje/przeglad-serwis-pharaon-1470-wroclaw/']){
  for(const width of [375,1440]){
   await p.setViewportSize({width,height:900});await p.goto(base+route);await p.locator('main img').evaluateAll(async xs=>{for(const i of xs){i.loading='eager';await i.decode()}});
   await p.screenshot({path:'/tmp/case-layout-'+route.split('/')[2]+'-'+width+'.png',fullPage:true});
  }
  if(!route.includes('pharaon')){await p.locator('.case-work-image a').first().click();assert(await p.locator('.case-photo-dialog').isVisible());await p.keyboard.press('Escape');assert(!await p.locator('.case-photo-dialog').isVisible());}
 }
 fs.writeFileSync('/tmp/case-layout-browser.json',JSON.stringify({results,failures,errors},null,2));await browser.close();assert.deepEqual(failures,[]);assert.deepEqual(errors,[]);console.log('PASS',results.length,'layouts; all images decoded; photo dialogs; no overflow or JS errors');
})().catch(e=>{console.error(e);process.exit(1)});

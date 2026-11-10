/* Full blog layout QA; third-party requests and form submissions are not sent. */
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const fs=require('fs'),path=require('path'),assert=require('assert/strict');
const root=path.resolve(__dirname,'..'),base=process.env.LTS_TEST_BASE||'http://127.0.0.1:8800';
const routes=['blog','ru/blog','en/blog'].flatMap(d=>fs.readdirSync(path.join(root,d),{withFileTypes:true}).filter(e=>e.isDirectory()&&fs.existsSync(path.join(root,d,e.name,'index.html'))).map(e=>'/'+d+'/'+e.name+'/'));
(async()=>{
 const browser=await chromium.launch({channel:'chrome',headless:true});const ctx=await browser.newContext({reducedMotion:'reduce'});
 await ctx.route('**/*',r=>r.request().url().startsWith(base+'/')?r.continue():r.abort());
 const p=await ctx.newPage(),errors=[],badResponses=[],results=[],failures=[];
 p.on('pageerror',e=>errors.push(e.message));p.on('response',r=>{if(r.url().startsWith(base)&&r.status()>=400)badResponses.push(r.url())});
 for(const route of routes.filter(r=>!process.env.BLOG_ROUTE||r.includes(process.env.BLOG_ROUTE))){
  for(const width of [320,768,1440]){
   await p.setViewportSize({width,height:900});assert.equal((await p.goto(base+route,{waitUntil:'domcontentloaded'})).status(),200);
   await p.locator('main img').evaluateAll(async xs=>{for(const x of xs){x.loading='eager';await x.decode()}});
   const state=await p.evaluate(()=>{
    const lum=c=>{const xs=c.match(/[\d.]+/g).slice(0,3).map(x=>+x/255).map(x=>x<=.04045?x/12.92:((x+.055)/1.055)**2.4);return .2126*xs[0]+.7152*xs[1]+.0722*xs[2]};
    const sig=[...document.querySelectorAll('.article-signature')];
    return {overflow:document.documentElement.scrollWidth>innerWidth+1,signature:sig.length===1&&sig[0].textContent.replace(/\s+/g,' ').trim()==='Олександр ПадалкоRaccoon Seo StudioWrocław, 2026',lastSignature:sig[0]?.parentElement.lastElementChild===sig[0],photos:[...document.querySelectorAll('main .article-image')].map(f=>({cap:+f.dataset.photoWidth,width:f.getBoundingClientRect().width,images:[...f.querySelectorAll('img')].map(i=>({height:i.getBoundingClientRect().height,cap:+f.dataset.photoHeight,loaded:i.naturalWidth>0}))})),buttons:[...document.querySelectorAll('.article-cta__actions a')].map(a=>{const s=getComputedStyle(a),l1=lum(s.color),l2=lum(s.backgroundColor),r=a.getBoundingClientRect();return {contrast:(Math.max(l1,l2)+.05)/(Math.min(l1,l2)+.05),height:r.height,width:r.width,visible:s.visibility==='visible'&&s.display!=='none',fits:a.scrollWidth<=a.clientWidth+1,href:a.getAttribute('href')}})};
   });
   if(state.overflow||!state.signature||!state.lastSignature||!state.buttons.length||state.buttons.some(b=>b.contrast<4.5||b.height<44||!b.visible||!b.fits)||state.photos.some(f=>f.width>f.cap+1||f.images.some(i=>!i.loaded||i.height>i.cap+1)))failures.push({route,width,state});
   results.push({route,width,photos:state.photos.length,buttons:state.buttons.length,minContrast:Math.min(...state.buttons.map(b=>b.contrast))});
  }
  console.log('CHECK',route);
 }
 for(const route of ['/ru/blog/planovoe-obsluzhivanie-diodnogo-lazera-pochemu-eto-vazhno/','/blog/nubway-nbw-vsiii-dzialanie-serwis/','/en/blog/3000-nain-laser-history-design-service/']){
  if(!routes.includes(route))continue;
  for(const width of [375,1440]){await p.setViewportSize({width,height:900});await p.goto(base+route,{waitUntil:'domcontentloaded'});await p.locator('main img').evaluateAll(async xs=>{for(const i of xs){i.loading='eager';await i.decode()}});await p.screenshot({path:'/tmp/blog-layout-'+route.split('/').filter(Boolean).pop()+'-'+width+'.png',fullPage:true});await p.locator('.article-cta').last().screenshot({path:'/tmp/blog-cta-'+route.split('/').filter(Boolean).pop()+'-'+width+'.png'});}
  for(const button of await p.locator('.article-cta__actions a').all()){
   await button.scrollIntoViewIfNeeded();assert(await button.evaluate(a=>{const r=a.getBoundingClientRect();return a.contains(document.elementFromPoint(r.x+r.width/2,r.y+r.height/2))}),'CTA hit target');await button.focus();assert(await button.evaluate(a=>a===document.activeElement),'CTA keyboard focus');
  }
 }
 fs.writeFileSync('/tmp/blog-layout-browser.json',JSON.stringify({results,failures,errors,badResponses},null,2));await browser.close();assert.deepEqual(failures,[]);assert.deepEqual(errors,[]);assert.deepEqual(badResponses,[]);console.log('PASS',results.length,'layouts; photo bounds; unique author; CTA contrast >= 4.5, focus and hit targets; no overflow, JS or local HTTP errors');
})().catch(e=>{console.error(e);process.exit(1)});

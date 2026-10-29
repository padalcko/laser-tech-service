/* Local browser QA. No external requests or messages are sent. */
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const fs=require('fs'),path=require('path'),assert=require('assert').strict;
const data=JSON.parse(fs.readFileSync(path.join(__dirname,'partners.json')));
const ordered=[...data.partners].sort((a,b)=>b.priority-a.priority);
const base=process.env.LTS_TEST_BASE||'http://127.0.0.1:8794';
const out=process.env.LTS_TEST_OUT||'/tmp/lts-partner-market';
(async()=>{
 const browser=await chromium.launch({channel:'chrome',headless:true});
 const ctx=await browser.newContext({reducedMotion:'reduce'});
 await ctx.route('**/*',r=>r.request().url().startsWith(base+'/')?r.continue():r.abort());
 const page=await ctx.newPage(),errors=[],results=[];
 page.on('pageerror',e=>errors.push(e.message));
 for(const [lang,file] of Object.entries(data.pages)){
  const url='/'+file.replace('index.html','');
  assert.equal((await page.goto(base+url)).status(),200);
  assert.equal(await page.locator('h1').count(),1);
  const cards=page.locator('.partner-card');assert.equal(await cards.count(),6);
  assert.deepEqual(await cards.locator('h2').allTextContents(),ordered.map(p=>p.content[lang].title));
  assert.equal(await cards.first().getAttribute('href'),'https://ltsmarket.pl/');
  assert.equal(await cards.first().locator('img').getAttribute('alt'),ordered[0].content[lang].image_html.match(/alt="([^"]+)"/)[1]);
  await page.locator('.lazar-launcher').click();await page.locator('#lazar-panel').waitFor({state:'visible'});
  await page.locator('.lazar-close').click();await page.locator('#lazar-panel').waitFor({state:'hidden'});
  for(const width of [320,375,430,768,1024,1440]){
   await page.setViewportSize({width,height:900});
   for(const im of await cards.locator('img').all())await im.evaluate(async e=>{e.scrollIntoView();await e.decode()});
   assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
   const dimensions=await cards.evaluateAll(nodes=>nodes.map(e=>{
    const r=e.getBoundingClientRect(),s=getComputedStyle(e),im=e.querySelector('img');
    const blocks=Array.from(e.querySelector('.partner-card__content').children).map(n=>({top:n.getBoundingClientRect().top,bottom:n.getBoundingClientRect().bottom}));
    return {w:r.width,h:r.height,top:r.top,left:r.left,right:r.right,blocks,radius:s.borderRadius,background:s.backgroundColor,fit:getComputedStyle(im).objectFit};
   }));
   for(const d of dimensions){assert(d.left>=-1&&d.right<=width+1);assert(Math.abs(d.w-dimensions[0].w)<1);assert.equal(d.radius,dimensions[0].radius);assert.equal(d.background,dimensions[0].background);assert.equal(d.fit,'contain')}
   for(const d of dimensions){
    const peers=dimensions.filter(x=>Math.abs(x.top-d.top)<1);
    for(const peer of peers){assert(Math.abs(peer.h-d.h)<1);for(let i=0;i<4;i++)assert(Math.abs(peer.blocks[i].top-d.blocks[i].top)<1,'Content rows must align')}
    assert(d.blocks[3].top-d.blocks[2].bottom<=26,'No stretched gap before partner badge');
   }
   assert(await cards.evaluateAll(nodes=>nodes.every(e=>Array.from(e.querySelectorAll('p,h2')).every(n=>n.scrollWidth<=n.clientWidth+1&&n.scrollHeight<=n.clientHeight+1))));
   await page.evaluate(()=>scrollTo(0,0));await page.screenshot({path:path.join(out,lang+'-'+width+'.png'),fullPage:true});
   results.push({lang,width,overflow:false,cards:6});
  }
  for(const [other,target] of Object.entries(data.pages)){
   if(other===lang)continue;
   await page.goto(base+url);await page.locator('.language-switcher summary').click();
   await page.locator('.language-switcher a[lang='+other+']').click();
   await page.waitForURL(base+'/'+target.replace('index.html',''));
   assert.equal(await page.locator('html').getAttribute('lang'),other);
  }
 }
 assert.deepEqual(errors,[]);await browser.close();
 fs.writeFileSync(path.join(out,'browser-results.json'),JSON.stringify({results,errors,languageTransitions:6,lazar:'open/close passed',externalRequests:'blocked'},null,2));
 console.log('PASS: 18 layouts, all logos decoded, aligned content within each row, natural card heights/styles, no text clipping or overflow, six language transitions, Lazar open/close; no JS errors');
})().catch(e=>{console.error(e);process.exit(1)});

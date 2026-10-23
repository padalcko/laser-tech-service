/* Local Stage 3C audit. External traffic is blocked; no real lead/chat submissions. */
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const fs=require('fs'),path=require('path'),assert=require('assert').strict;
const base=process.env.LTS_TEST_BASE||'http://127.0.0.1:8788';
const out=process.env.LTS_TEST_OUT||'/tmp/lts-stage3c';fs.mkdirSync(out,{recursive:true});
const registry=JSON.parse(fs.readFileSync(path.join(__dirname,'site-locales.json')));
const groups=registry.pages.filter(g=>['article','case-study','blog','case-studies'].includes(g.type));
const shots=new Set(['/en/blog/','/en/case-studies/','/en/blog/hifu-technology-applications-service/','/en/blog/lightsheer-desire-cooling-reliability/','/en/blog/why-laser-diode-modules-fail/','/en/case-studies/estetech-peltier-module-replacement-poznan/','/en/case-studies/gme-exsys-308-service-inspection/','/en/case-studies/urgent-co2-laser-repair-poznan/']);
(async()=>{
 const browser=await chromium.launch({channel:'chrome',headless:true});const c=await browser.newContext({reducedMotion:'reduce'});const p=await c.newPage(),errors=[],results=[];
 p.on('pageerror',e=>errors.push(e.message));
 await c.route('**/*',r=>r.request().url().startsWith(base+'/')?r.continue():r.abort());
 for(const g of groups)assert.equal((await c.request.get(base+g.routes.en.url)).status(),200);
 for(const width of [320,390,1440])for(const g of groups){
  const route=g.routes.en.url;await p.setViewportSize({width,height:900});await p.goto(base+route);
  assert.equal(await p.locator('.lazar-root').getAttribute('data-sending-enabled'),'false');
  const dropdown=p.locator('.language-switcher__dropdown');await dropdown.locator('summary').click();
  assert.deepEqual(await dropdown.locator('a').evaluateAll(es=>es.map(e=>e.hreflang)),['pl','ru','en']);
  await p.keyboard.press('ArrowDown');assert.equal(await p.locator(':focus').getAttribute('hreflang'),'pl');
  await p.keyboard.press('End');assert.equal(await p.locator(':focus').getAttribute('hreflang'),'en');
  await p.keyboard.press('Escape');assert.equal(await dropdown.evaluate(e=>e.open),false);
  if(await p.locator('.nav-toggle').isVisible()){
   await p.locator('.nav-toggle').click();assert.equal(await p.locator('.nav-toggle').getAttribute('aria-expanded'),'true');
   assert.equal(await p.locator('#primaryNavigation a[href="/en/blog/"]').count(),1);
   assert.equal(await p.locator('#primaryNavigation a[href="/en/case-studies/"]').count(),1);
   await p.keyboard.press('Escape');
  }
  for(const im of await p.locator('img').all())if(await im.isVisible()){await im.scrollIntoViewIfNeeded();await im.evaluate(e=>e.decode());}
  const gallery=p.locator('.case-gallery--compact a, .case-photo--compact a');
  if(await gallery.count()){
   await gallery.first().click();const dialog=p.locator('.case-photo-dialog');assert(await dialog.isVisible());
   assert.equal(await dialog.getAttribute('aria-label'),'Photo preview');await dialog.locator('img').evaluate(e=>e.decode());
   await p.keyboard.press('Escape');await dialog.waitFor({state:'hidden'});
  }
  const videos=await p.locator('main iframe').evaluateAll(es=>es.map(e=>({src:e.src,loading:e.loading,allow:e.getAttribute('allow')})));
  assert(videos.every(v=>v.src.startsWith('https://www.youtube.com/embed/')),JSON.stringify(videos));
  assert(!(await p.evaluate(()=>document.documentElement.scrollWidth>innerWidth)),route+' '+width);
  if(shots.has(route)){
   await p.evaluate(()=>scrollTo(0,0));const slug=route.split('/').filter(Boolean).slice(1).join('-');
   await p.screenshot({path:path.join(out,slug+'-'+width+'.png')});
   if(width===1440)await p.screenshot({path:path.join(out,slug+'-full.png'),fullPage:true});
  }
  assert.deepEqual(errors,[]);results.push({route,width,status:'PASS',videos:videos.length,gallery:await gallery.count()});
  console.log(width,route,'PASS');
 }
 // Actual language navigation on both indexes and representative content.
 for(const route of shots){const g=groups.find(g=>g.routes.en.url===route);await p.goto(base+route);
  await p.locator('.language-switcher summary').click();await p.locator('.language-switcher [hreflang=ru]').click();await p.waitForURL(base+g.routes.ru.url);
  await p.locator('.language-switcher summary').click();await p.locator('.language-switcher [hreflang=en]').click();await p.waitForURL(base+route);
 }
 await c.close();await browser.close();fs.writeFileSync(path.join(out,'results.json'),JSON.stringify({http:45,layouts:results,roundTrips:shots.size,externalMediaPlayback:'not tested; external requests blocked'},null,2));
 console.log('PASS: 45 HTTP routes, 135 layouts, galleries, dropdown, burger, navigation and source video embeds');
})().catch(e=>{console.error(e);process.exit(1)});

/* Local QA: external services blocked, chat mocked; no real submissions. */
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const assert=require('assert').strict,fs=require('fs');
const base=process.env.LTS_TEST_BASE||'http://127.0.0.1:8807';
const out=process.env.LTS_TEST_OUT||'/tmp/lts-about';fs.mkdirSync(out,{recursive:true});
const axePath=process.env.LTS_AXE_PATH||require.resolve('axe-core');
const registry=JSON.parse(fs.readFileSync(__dirname+'/site-locales.json'));
const group=id=>registry.pages.find(g=>g.id===id);
(async()=>{
 const browser=await chromium.launch({channel:'chrome',headless:true});
 const ctx=await browser.newContext({hasTouch:true,reducedMotion:'reduce'});
 await ctx.route('**/*',r=>r.request().url().includes('/webhook/lazar-ai-chat')?r.fulfill({json:{reply:'Local QA reply'}}):r.request().url().startsWith(base+'/')?r.continue():r.abort());
 const page=await ctx.newPage(),errors=[],failures=[],results=[];
 page.on('pageerror',e=>errors.push(e.message));page.on('response',r=>{if(r.url().startsWith(base+'/')&&r.status()>=400)failures.push(r.url())});
 const routes={pl:'/o-nas/',ru:'/ru/o-nas/',en:'/en/about-us/'};
 for(const [lang,route] of Object.entries(routes))for(const width of [320,375,390,430,768,1024,1440,1920]){
  console.log('Layout',lang,width);
  await page.setViewportSize({width,height:900});await page.goto(base+route);
  await page.locator('#lazar-root').waitFor({state:'attached'});
  assert.equal(await page.locator('main > section').count(),10);
  assert.equal(await page.locator('h1').count(),1);
  assert.equal(await page.locator('html').getAttribute('lang'),lang);
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${lang}/${width} overflow`);
  const photos=page.locator('.about-portrait img');assert.equal(await photos.count(),3);
  for(const img of await page.locator('main img').all()){
   await img.scrollIntoViewIfNeeded();await img.evaluate(e=>e.decode());
   assert(await img.evaluate(e=>e.naturalWidth>0&&Number(e.getAttribute('width'))>0&&Number(e.getAttribute('height'))>0));
  }
  const boxes=await page.locator('.about-person').evaluateAll(es=>es.map(e=>e.getBoundingClientRect().toJSON()));
  if(width<768)assert(boxes.every(b=>b.x===boxes[0].x));
  if(width>=1024)assert(boxes.every(b=>b.y===boxes[0].y));
  assert(await photos.evaluateAll(es=>es.every(e=>getComputedStyle(e).objectFit==='cover')));
  await page.evaluate(()=>scrollTo(0,0));
  const mobile=width<=760;
  if(mobile){await page.locator('.nav-toggle').click();await page.locator('#primaryNavigation').waitFor({state:'visible'});}
  const primary=page.locator('#primaryNavigation');
  const top=await primary.locator(':scope > li').evaluateAll(es=>es.map(e=>e.querySelector('a').getAttribute('href')));
  const partners=group('partnerzy').routes[lang].url,contact=group('kontakt').routes[lang].url;
  assert.equal(top[top.indexOf(partners)+1],route);assert.equal(top[top.indexOf(partners)+2],contact);
  assert(!top.includes(group('blog').routes[lang].url));
  const toggle=page.locator('[aria-controls=workSubmenu]'),menu=page.locator('#workSubmenu');
  await toggle.click();assert.equal(await toggle.getAttribute('aria-expanded'),'true');assert(await menu.isVisible());
  assert.equal(await menu.locator('a').getAttribute('href'),group('blog').routes[lang].url);
  await toggle.click();assert(!await menu.isVisible());
  await toggle.focus();await page.keyboard.press('ArrowDown');assert(await menu.isVisible());
  assert.equal(await page.locator(':focus').getAttribute('href'),group('blog').routes[lang].url);
  await page.keyboard.press('Escape');assert(!await menu.isVisible());
  if(mobile)await page.locator('.nav-toggle').click();
  else {await page.locator('.nav-work .nav-list__link').hover();assert(await menu.isVisible());await page.mouse.move(width-2,850);await page.locator('h1').click();}
  if([390,1440].includes(width)){
   await page.screenshot({path:`${out}/${lang}-${width}.png`,fullPage:true});
   await page.locator('#team').screenshot({path:`${out}/${lang}-team-${width}.png`});
   await page.locator('#hero').scrollIntoViewIfNeeded();
   await page.addScriptTag({path:axePath});
   const axe=await page.evaluate(()=>axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}}));
   results.push({lang,width,accessibility:axe.violations.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.map(n=>n.target)}))});
  }
  const configs=await page.evaluate(()=>dataLayer.filter(x=>x[0]==='config'&&x[1]==='G-6QFRWP5RX5').length);assert.equal(configs,1);
  assert.equal(await page.locator('.mobile-contact-bar').count(),1);
 }
 // Real link clicks and language transitions on touch-enabled mobile.
 await page.setViewportSize({width:390,height:900});
 for(const [lang,route] of Object.entries(routes)){
  await page.goto(base+route);await page.locator('.nav-toggle').tap();
  await page.locator('[aria-controls=workSubmenu]').tap();
  await page.locator('#workSubmenu a').tap();await page.waitForURL(base+group('blog').routes[lang].url);
  await page.goto(base+route);await page.locator('.nav-toggle').tap();
  await page.locator('.nav-work .nav-list__link').tap();await page.waitForURL(base+group('realizacje').routes[lang].url);
  await page.goto(base+route);await page.locator('.language-switcher__toggle').tap();
  const next=lang==='en'?'pl':'en';await page.locator(`.language-switcher__link[lang=${next}]`).tap();await page.waitForURL(base+routes[next]);
  await page.locator('[data-action=lazar]').tap();await page.locator('.lazar-input').fill('Local QA');await page.locator('.lazar-send').tap();
  await page.waitForFunction(()=>document.querySelector('.lazar-log').textContent.includes('Local QA reply'));await page.locator('.lazar-close').tap();
 }
 // Representative existing routes, including services, pricing, articles and local 404 languages.
 for(const lang of ['pl','ru','en'])for(const type of ['home','services','pricing','case-studies','article','partners','contact']){
  const g=registry.pages.find(g=>g.type===type&&g.routes[lang]?.status==='published');
  await page.goto(base+g.routes[lang].url);assert.equal(await page.locator('.nav-work').count(),1);assert.equal(await page.locator('.mobile-contact-bar').count(),1);
 }
 await page.goto(base+'/404.html');
 for(const lang of ['ru','en','pl']){
  await page.locator('.language-switcher__toggle').tap();await page.locator(`.language-switcher__link[lang=${lang}]`).tap();
  assert.equal(await page.locator('html').getAttribute('lang'),lang);
  assert.equal(await page.locator('#primaryNavigation a').filter({hasText:{pl:'O nas',ru:'О нас',en:'About Us'}[lang]}).getAttribute('href'),routes[lang]);
 }
 const inherited=[];
 for(const lang of ['pl','ru','en'])for(const width of [390,1440]){
  await page.setViewportSize({width,height:900});await page.goto(base+group('partnerzy').routes[lang].url);
  await page.addScriptTag({path:axePath});
  const audit=await page.evaluate(()=>axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa']}}));
  inherited.push({lang,width,accessibility:audit.violations.map(v=>({id:v.id,impact:v.impact,nodes:v.nodes.map(n=>n.target)}))});
 }
 const newIssues=results.flatMap(result=>{
  const baseline=inherited.find(r=>r.lang===result.lang&&r.width===result.width);
  return result.accessibility.flatMap(v=>v.nodes.filter(n=>!baseline.accessibility.some(b=>b.id===v.id&&b.nodes.some(t=>JSON.stringify(t)===JSON.stringify(n)))).map(n=>({lang:result.lang,width:result.width,id:v.id,target:n})));
 });
 fs.writeFileSync(out+'/results.json',JSON.stringify({layouts:24,results,inherited,newIssues,errors,failures},null,2));
 assert.deepEqual(errors,[]);assert.deepEqual(failures,[]);
 assert.deepEqual(newIssues,[]);
 await browser.close();console.log('PASS 24 layouts, 6 axe audits with unchanged baseline findings, mobile/desktop/keyboard navigation, PL/RU/EN links, 21 existing routes, 404 locales, mock Lazar and GA4 configuration; no JS/HTTP errors');
})().catch(e=>{console.error(e);process.exit(1)});

/* Local browser QA; external requests blocked. */
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');const fs=require('fs'),path=require('path'),assert=require('assert').strict;
const registry=JSON.parse(fs.readFileSync(path.join(__dirname,'site-locales.json'))),groups=registry.pages.filter(g=>['realizacje:serwis-lasera-sapphire-wymiana-plynu','blog:lasery-dinozaury-wiek-stan-techniczny'].includes(g.id));
const base=process.env.LTS_TEST_BASE||'http://127.0.0.1:8791',out=process.env.LTS_TEST_OUT||'/tmp/lts-sapphire';fs.mkdirSync(out,{recursive:true});
(async()=>{
const b=await chromium.launch({channel:'chrome',headless:true}),c=await b.newContext({reducedMotion:'reduce'});await c.route('**/*',r=>r.request().url().startsWith(base+'/')?r.continue():r.abort());
const p=await c.newPage(),errors=[],results=[];p.on('pageerror',e=>errors.push(e.message));
for(const g of groups)for(const [lang,r] of Object.entries(g.routes)){
const kind=g.type==='case-study'?'case':'blog';await p.setViewportSize({width:390,height:900});assert.equal((await p.goto(base+r.url)).status(),200);await p.locator('.lazar-launcher').waitFor({state:'visible'});
assert.equal(await p.locator('h1').count(),1);assert.equal(await p.locator('main img').count(),kind==='case'?9:4);
for(const im of await p.locator('main img').all()){await im.evaluate(async e=>{e.scrollIntoView({block:'center'});await e.decode()});assert(await im.evaluate(e=>e.naturalWidth>0));}
if(kind==='case'){
for(const sel of ['.case-photo--compact a','.case-gallery a']){await p.locator(sel).first().click();await p.locator('.case-photo-dialog').waitFor({state:'visible'});await p.keyboard.press('Escape');await p.locator('.case-photo-dialog').waitFor({state:'hidden'});}
}
for(const width of [320,375,390,768,1024,1440]){
await p.setViewportSize({width,height:900});await p.evaluate(()=>scrollTo(0,0));assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));
await p.locator('.language-switcher summary').click();assert.equal(await p.locator('.language-switcher a').count(),Object.keys(g.routes).length);
for(const [l,peer] of Object.entries(g.routes))assert.equal(await p.locator('.language-switcher a[lang='+l+']').getAttribute('href'),peer.url);await p.keyboard.press('Escape');
if(kind==='blog')for(const im of await p.locator('main img').all())assert((await im.boundingBox()).height<=321);
if([390,1440].includes(width)){for(const im of await p.locator('main img').all())await im.evaluate(async e=>{e.scrollIntoView({block:'center'});await e.decode()});await p.evaluate(()=>scrollTo(0,0));await p.screenshot({path:path.join(out,kind+'-'+lang+'-'+width+'.png'),fullPage:true});}results.push({url:r.url,width,overflow:false});
}
console.log('PASS',r.url);
}
for(const url of ['/realizacje/','/ru/realizacje/','/en/case-studies/','/blog/','/ru/blog/','/en/blog/']){
await p.setViewportSize({width:320,height:900});assert.equal((await p.goto(base+url)).status(),200);assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1));const card=p.locator(!url.includes('/blog/')?'.realizacja-card':'.blog-card').first();assert.equal(await card.locator('img').count(),!url.includes('/blog/')?1:0);const target=await card.locator('a').first().getAttribute('href');assert(target.includes('sapphire')||target.includes('dino'));await card.locator('a').first().click();await p.waitForURL(base+target);
}
assert.deepEqual(errors,[]);await b.close();fs.writeFileSync(path.join(out,'browser-results.json'),JSON.stringify({results,errors,catalogueChecks:6,externalRequests:'blocked'},null,2));console.log('PASS: 36 layouts, photos, galleries, localized switches, compact article images, six new cards and three-language case');
})().catch(e=>{console.error(e);process.exit(1)});

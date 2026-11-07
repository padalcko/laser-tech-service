/* Scoped corporate-team geometry checks; no external requests or submissions. */
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const fs=require('fs'),assert=require('assert').strict;
const base=process.env.LTS_TEST_BASE||'http://127.0.0.1:8807',out='/tmp/lts-team';
(async()=>{
 const b=await chromium.launch({channel:'chrome',headless:true});
 const c=await b.newContext({reducedMotion:'reduce'});
 await c.route('**/*',r=>r.request().url().startsWith(base+'/')?r.continue():r.abort());
 const p=await c.newPage(),errors=[],failures=[],results=[];
 p.on('pageerror',e=>errors.push(e.message));p.on('response',r=>{if(r.url().startsWith(base+'/')&&r.status()>=400)failures.push(r.url())});
 for(const [lang,route] of Object.entries({pl:'/o-nas/',ru:'/ru/o-nas/',en:'/en/about-us/'}))for(const width of [320,375,390,430,768,1024,1440,1920]){
  await p.setViewportSize({width,height:1000});await p.goto(base+route);
  for(const img of await p.locator('.about-portrait img').all()) {await img.scrollIntoViewIfNeeded();await img.evaluate(e=>e.decode());}
  const cards=await p.locator('.about-person').evaluateAll(es=>es.map(e=>{
   const rect=n=>{const r=n.getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height}};
   const img=e.querySelector('img'),body=e.querySelector('.about-person__body');
   return {person:e.dataset.person,card:rect(e),portrait:rect(e.querySelector('.about-portrait')),image:rect(img),name:rect(body.querySelector('h3')),role:rect(body.querySelector('.about-role')),description:rect(body.querySelector('p:last-child')),fit:getComputedStyle(img).objectFit,src:img.currentSrc,alt:img.alt,loaded:img.naturalWidth>0};
  }));
  assert.deepEqual(cards.map(c=>c.person),['dmytro-zaitsev','oleksandr-padalko','sofiia-shcherbakova']);
  for(const card of cards){
   assert(card.loaded&&card.alt&&card.src.includes(card.person));assert.equal(card.fit,'cover');
   assert(Math.abs(card.portrait.w/card.portrait.h-.8)<.002);
   assert(Math.abs(card.image.w-card.portrait.w)<1&&Math.abs(card.image.h-card.portrait.h)<1);
   assert(Math.abs(card.portrait.w-cards[0].portrait.w)<1&&Math.abs(card.portrait.h-cards[0].portrait.h)<1);
   assert(Math.abs((card.name.y-card.portrait.y-card.portrait.h)-(cards[0].name.y-cards[0].portrait.y-cards[0].portrait.h))<1);
  }
  if(width>=1024)for(const card of cards)for(const key of ['portrait','name','role','description'])assert(Math.abs(card[key].y-cards[0][key].y)<1,`${lang}/${width} ${key}`);
  if(width>=1024)assert(cards.every(card=>Math.abs(card.card.h-cards[0].card.h)<1));
  if(width<768)assert(cards.every(card=>Math.abs(card.card.x-cards[0].card.x)<1));
  assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
  if([390,768,1024,1440].includes(width))await p.locator('#team').screenshot({path:`${out}/${lang}-${width}.png`});
  results.push({lang,width,cards});
 }
 fs.writeFileSync(out+'/results.json',JSON.stringify({results,errors,failures},null,2));
 assert.deepEqual(errors,[]);assert.deepEqual(failures,[]);await b.close();
 console.log('PASS 24 PL/RU/EN layouts: identical 4:5 images, cover, mapping/order, image-to-name gaps, aligned desktop text/card heights; no overflow or JS/HTTP errors');
})().catch(e=>{console.error(e);process.exit(1)});

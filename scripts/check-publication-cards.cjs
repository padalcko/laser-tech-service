/* All public card instances: geometry, complete titles, image decoding and CTA.
   External requests are blocked; no forms or analytics are submitted. */
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const fs=require('fs'),path=require('path');
const root=path.resolve(__dirname,'..'),base=process.env.LTS_TEST_BASE||'http://127.0.0.1:8800';
const skip=new Set(['dist','node_modules','scripts','content','reports','docs','.git']);
function scan(d){return fs.readdirSync(d,{withFileTypes:true}).flatMap(e=>e.name.startsWith('.')||skip.has(e.name)?[]:e.isDirectory()?scan(path.join(d,e.name)):e.name.endsWith('.html')&&fs.readFileSync(path.join(d,e.name),'utf8').includes('lts-card__title')?[path.join(d,e.name)]:[])}
(async()=>{
 const browser=await chromium.launch({channel:'chrome',headless:true});
 const ctx=await browser.newContext({reducedMotion:'reduce'});
 await ctx.route('**/*',r=>(r.request().url().startsWith(base+'/')||/^https:\/\/fonts\.(googleapis|gstatic)\.com\//.test(r.request().url()))?r.continue():r.abort());
 const p=await ctx.newPage(),failures=[],results=[],errors=[];
 p.on('pageerror',e=>errors.push(e.message));
 for(const file of scan(root)){
  const route='/'+path.relative(root,file).replace(/index.html$/,'');
  for(const width of [320,390,768,1024,1440]){
   await p.setViewportSize({width,height:1000});await p.goto(base+route,{waitUntil:'domcontentloaded'});await p.evaluate(()=>document.fonts.ready);
   const state=await p.evaluate(async()=>{
    const cards=[...document.querySelectorAll('.lts-card')];
    const failures=[];const rect=e=>{const r=e.getBoundingClientRect();return {top:r.top,bottom:r.bottom,height:r.height,left:r.left,width:r.width}};
    for(const c of cards){
     const t=c.querySelector('.lts-card__title'),a=c.querySelector('.lts-card__cta'),s=getComputedStyle(t),r=document.createRange();r.selectNodeContents(t);
     const boxes=[...r.getClientRects()].filter(b=>b.width>0);const lines=new Set(boxes.map(b=>Math.round(b.top)));
     if(lines.size>3||Math.max(...boxes.map(b=>b.bottom))>rect(t).bottom+1)failures.push({type:'title',title:t.textContent.trim(),href:a.getAttribute('href'),lines:lines.size});
     if(s.fontSize!=='20px'||Math.abs(rect(t).height-84)>1)failures.push({type:'typography',title:t.textContent.trim(),font:s.fontSize,height:rect(t).height});
     if(!/[\p{L}]/u.test(a.textContent)||rect(a).height<10)failures.push({type:'cta',href:a.getAttribute('href')});
     for(const img of c.querySelectorAll('img')){img.loading='eager';try{await img.decode()}catch{failures.push({type:'image',src:img.src})}}
    }
    for(const grid of document.querySelectorAll('.blog-grid,.realizacje-grid,.about-cases,.service-cases-grid')){
     const rows=new Map();for(const c of [...grid.children].filter(c=>c.matches('.lts-card'))){const top=Math.round(rect(c).top);if(!rows.has(top))rows.set(top,[]);rows.get(top).push(c)}
     for(const row of rows.values())if(row.length>1){
      for(const selector of [null,'.lts-card__title','.lts-card__description','.lts-card__cta','.realizacja-card__meta','.blog-card__category','img']){
       const els=row.map(c=>selector?c.querySelector(selector):c).filter(Boolean);if(els.length<2)continue;
       const vals=els.map(e=>selector==='.lts-card__cta'?rect(e).bottom:selector?rect(e).top:rect(e).height);
       if(Math.max(...vals)-Math.min(...vals)>2)failures.push({type:'alignment',selector,vals});
      }
     }
    }
    if(document.documentElement.scrollWidth>innerWidth+1)failures.push({type:'overflow'});
    return {count:cards.length,failures};
   });
   results.push({route,width,count:state.count});if(state.failures.length)failures.push({route,width,failures:state.failures});
   if(['/blog/','/realizacje/','/ru/blog/','/en/case-studies/'].includes(route)&&[390,768,1440].includes(width)){
    await p.locator('.lts-card').first().scrollIntoViewIfNeeded();await p.screenshot({path:'/tmp/lts-cards/'+route.replaceAll('/','_')+width+'.png'});
   }
  }
  console.log('CHECK',route);
 }
 await browser.close();fs.mkdirSync(path.join(root,'reports'),{recursive:true});fs.writeFileSync(path.join(root,'reports/publication-cards-browser.json'),JSON.stringify({results,failures,errors},null,2));
 console.log(JSON.stringify({layouts:results.length,instances:results.reduce((n,r)=>n+r.count,0),failures:failures.length,errors}));if(failures.length||errors.length)process.exit(1);
})().catch(e=>{console.error(e);process.exit(1)});

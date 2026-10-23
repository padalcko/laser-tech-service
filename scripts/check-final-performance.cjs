/* Local observations only; no field CWV or INP claims. */
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');const fs=require('fs'),path=require('path');
(async()=>{
 const base=process.env.LTS_TEST_BASE||'http://127.0.0.1:8788',out=process.env.LTS_TEST_OUT||'docs/qa/final-v1';fs.mkdirSync(out,{recursive:true});
 const b=await chromium.launch({channel:'chrome',headless:true}),results=[];
 for(const route of ['/','/ru/','/en/','/en/pricing/','/en/partners/','/en/services/','/en/services/diode-laser-diagnostics/'])for(const width of [390,1440]){
  const c=await b.newContext({viewport:{width,height:900},reducedMotion:'reduce'});await c.route('**/*',r=>r.request().url().startsWith(base+'/')?r.continue():r.abort());
  await c.addInitScript(()=>{window.qaMetrics={lcp:null,cls:0};new PerformanceObserver(l=>{for(const e of l.getEntries())window.qaMetrics.lcp=e.startTime;}).observe({type:'largest-contentful-paint',buffered:true});new PerformanceObserver(l=>{for(const e of l.getEntries())if(!e.hadRecentInput)window.qaMetrics.cls+=e.value;}).observe({type:'layout-shift',buffered:true});});
  const p=await c.newPage();await p.goto(base+route);await p.waitForTimeout(1000);
  const sample=await p.evaluate(()=>{
   const rgba=s=>{const m=s.match(/[\d.]+/g);return m&&m.map(Number)};
   const lum=rgb=>rgb.slice(0,3).map(x=>{x/=255;return x<=.04045?x/12.92:((x+.055)/1.055)**2.4}).reduce((s,x,i)=>s+x*[.2126,.7152,.0722][i],0);
   const contrast=[];
   for(const el of [...document.querySelectorAll('main h2, main p, main button, main a, main strong, main span')].slice(0,300)){
    if(![...el.childNodes].some(n=>n.nodeType===3&&n.textContent.trim())||el.getBoundingClientRect().width===0)continue;
    const style=getComputedStyle(el),fg=rgba(style.color);if(!fg||fg[3]===0)continue;
    let ancestor=el,bg=null,unknown=false;
    while(ancestor){const s=getComputedStyle(ancestor);const pseudo=['::before','::after'].map(p=>getComputedStyle(ancestor,p));if(pseudo.some(s=>s.content!=='none'&&s.backgroundImage!=='none')){unknown=true;break;}if(s.backgroundImage!=='none'){unknown=true;break;}const color=rgba(s.backgroundColor);if(color&&color[3]!==0){bg=color;break;}ancestor=ancestor.parentElement;}
    if(!bg||unknown||bg[3]&&bg[3]!==1)continue;
    const text=fg.slice(0,3).map((v,i)=>v*(fg[3]??1)+bg[i]*(1-(fg[3]??1)));
    const ratio=(Math.max(lum(text),lum(bg))+.05)/(Math.min(lum(text),lum(bg))+.05);
    const large=parseFloat(style.fontSize)>=24||(parseFloat(style.fontSize)>=18.66&&parseInt(style.fontWeight)>=700),minimum=large?3:4.5;
    if(ratio<minimum)contrast.push({text:el.textContent.trim().slice(0,65),selector:el.tagName.toLowerCase()+'.'+el.className,backgroundOwner:ancestor?.tagName.toLowerCase()+'.'+ancestor?.className,ratio:+ratio.toFixed(2),minimum,color:style.color,background:bg,font:style.fontSize});
   }
   return {...window.qaMetrics,resources:performance.getEntriesByType('resource').length,contrastSamplesBelowThreshold:contrast};
  });
  results.push({route,width,...sample});await c.close();
 }
 await b.close();fs.writeFileSync(path.join(out,'performance.json'),JSON.stringify({note:'Local Chrome, external scripts blocked, reduced motion; 1 second observation. Not field CWV, not INP or a Lighthouse score. Contrast samples exclude image, gradient and pseudo-element backgrounds; these need visual review.',results},null,2));console.log('Recorded',results.length,'local performance/contrast samples');
 if(results.some(r=>r.contrastSamplesBelowThreshold.length))throw new Error('Readable solid-background text failed the sampled contrast threshold');
})().catch(e=>{console.error(e);process.exit(1)});

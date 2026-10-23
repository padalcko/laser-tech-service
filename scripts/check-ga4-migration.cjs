/* Read-only browser audit: Google and all other external requests are mocked/blocked. */
const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const fs=require('fs'),path=require('path'),assert=require('assert').strict;
const out=process.env.LTS_TEST_OUT||'/tmp/lts-ga4-migration';
const root=path.resolve(__dirname,'..'),base=process.env.LTS_TEST_BASE||'http://127.0.0.1:8788';
const registry=JSON.parse(fs.readFileSync(path.join(__dirname,'site-locales.json')));
const routes=registry.pages.flatMap(g=>Object.values(g.routes).filter(r=>r.status==='published').map(r=>r.url)).concat('/404.html');
(async()=>{
 const b=await chromium.launch({channel:'chrome',headless:true});const results=[];
 for(const route of routes){
  const source=fs.readFileSync(path.join(root,route.endsWith('.html')?route:route+'index.html'),'utf8');
  assert(!source.includes('G-5STE4YVSDH'));
  const c=await b.newContext();const requests=[],errors=[];
  await c.route('**/*',r=>{
   const url=r.request().url();if(url.startsWith(base+'/'))return r.continue();
   requests.push(url);
   if(url.startsWith('https://www.googletagmanager.com/'))return r.fulfill({status:200,contentType:'application/javascript',body:'/* mocked external tag */'});
   return r.abort();
  });
  const p=await c.newPage();p.on('pageerror',e=>errors.push(e.message));await p.goto(base+route);
  const configs=await p.evaluate(()=>(window.dataLayer||[]).filter(x=>x[0]==='config').map(x=>x[1]));
  for(const id of ['G-6QFRWP5RX5','AW-17614450660']){
   const expected=source.includes(id)?1:0;assert.equal(configs.filter(x=>x===id).length,expected,route+' '+id);
   assert.equal(requests.filter(x=>x.includes('/gtag/js?id='+id)).length,expected);
  }
  for(const id of ['GTM-PT7BMHKW','GTM-MF33VG4R'])assert.equal(requests.filter(x=>x.includes('/gtm.js?id='+id)).length,source.includes(id)?1:0);
  assert(!requests.some(x=>x.includes('G-5STE4YVSDH')));
  assert.equal(await p.evaluate(()=>(window.dataLayer||[]).filter(x=>x[0]==='event'&&x[1]==='page_view').length),0);
  assert.deepEqual(errors,[]);results.push({route,configs,result:'PASS'});await c.close();
 }
 await b.close();fs.mkdirSync(out,{recursive:true});
 fs.writeFileSync(path.join(out,'tags.json'),JSON.stringify({mode:'External Google scripts mocked; configuration and requested URLs only, not live collection',results},null,2));
 console.log('PASS',results.length,'routes: GA4/Ads config, GTM loaders, no explicit page_view or JS errors');
})().catch(e=>{console.error(e);process.exit(1)});

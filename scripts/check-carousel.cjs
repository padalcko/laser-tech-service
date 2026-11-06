const {chromium}=require(process.env.PLAYWRIGHT_MODULE||'playwright');
const fs=require('fs'),assert=require('assert').strict;
const base=process.env.LTS_TEST_BASE||'http://127.0.0.1:8799';
(async()=>{
 const browser=await chromium.launch({channel:'chrome',headless:true});
 const ctx=await browser.newContext({hasTouch:true});
 await ctx.route('**/*',r=>r.request().url().startsWith(base+'/')?r.continue():r.abort());
 await ctx.addInitScript(()=>{
  const raf=window.requestAnimationFrame.bind(window),cancel=window.cancelAnimationFrame.bind(window),active=new Set();
  window.carouselFrames={calls:0,max:0,active:()=>active.size};
  window.requestAnimationFrame=fn=>{
   if(!['tick','animateCarousel'].includes(fn.name))return raf(fn);
   let id=raf(t=>{active.delete(id);carouselFrames.calls++;fn(t)});active.add(id);carouselFrames.max=Math.max(carouselFrames.max,active.size);return id;
  };
  window.cancelAnimationFrame=id=>{active.delete(id);cancel(id)};
 });
 const p=await ctx.newPage(),errors=[];p.on('pageerror',e=>errors.push(e.message));
 for(const lang of ['pl','ru','en']){
  await p.setViewportSize({width:375,height:850});await p.goto(base+(lang==='pl'?'/':'/'+lang+'/'));
  const original=await p.locator('#carouselTrack > *').count();
  const assets=await p.locator('#carouselTrack img').evaluateAll(ns=>ns.map(n=>n.outerHTML));
  for(const width of [320,375,430,767,768,1024,1440,375,1024,767,768]){
   await p.setViewportSize({width,height:850});await p.locator('.carousel-wrapper').scrollIntoViewIfNeeded();await p.waitForTimeout(150);
   assert.equal(await p.locator('#carouselTrack > *').count(),original*(width<768?1:2));
   assert(await p.evaluate(()=>document.documentElement.scrollWidth<=innerWidth));
   if(width<768){
    assert.equal(await p.evaluate(()=>carouselFrames.active()),0);
    const before=await p.evaluate(()=>carouselFrames.calls);await p.waitForTimeout(100);assert.equal(await p.evaluate(()=>carouselFrames.calls),before);
    assert.equal(await p.locator('#carouselTrack').evaluate(e=>e.style.transform),'');
    assert.deepEqual(await p.locator('#carouselTrack img').evaluateAll(ns=>ns.map(n=>n.outerHTML)),assets);
    await p.locator('.carousel-wrapper').evaluate(e=>e.scrollLeft=300);await p.waitForTimeout(120);assert(await p.locator('.carousel-wrapper').evaluate(e=>e.scrollLeft>0));
   }else{
    assert.equal(await p.evaluate(()=>carouselFrames.active()),1);
    const x=await p.locator('#carouselTrack').evaluate(e=>e.style.transform);await p.waitForTimeout(100);assert.notEqual(await p.locator('#carouselTrack').evaluate(e=>e.style.transform),x);
    await p.evaluate(()=>scrollTo(0,document.body.scrollHeight));await p.waitForTimeout(100);assert.equal(await p.evaluate(()=>carouselFrames.active()),0);
    await p.locator('.carousel-wrapper').scrollIntoViewIfNeeded();await p.waitForTimeout(100);
    await p.evaluate(()=>{Object.defineProperty(document,'hidden',{configurable:true,value:true});document.dispatchEvent(new Event('visibilitychange'))});assert.equal(await p.evaluate(()=>carouselFrames.active()),0);
    await p.evaluate(()=>{delete document.hidden;document.dispatchEvent(new Event('visibilitychange'))});
    for(let i=0;i<3;i++){await p.emulateMedia({reducedMotion:'reduce'});await p.waitForTimeout(50);assert.equal(await p.evaluate(()=>carouselFrames.active()),0);await p.emulateMedia({reducedMotion:'no-preference'});await p.waitForTimeout(50)}
    assert.equal(await p.evaluate(()=>carouselFrames.active()),1);
   }
   assert((await p.evaluate(()=>carouselFrames.max))<=1);
  }
  // Actual browser touch events exercise native scrolling, not JS drag code.
  await p.setViewportSize({width:375,height:850});await p.locator('.carousel-wrapper').scrollIntoViewIfNeeded();
  await p.locator('.carousel-wrapper').evaluate(e=>e.scrollLeft=0);await p.waitForTimeout(150);
  const box=await p.locator('.carousel-wrapper').boundingBox(),cdp=await ctx.newCDPSession(p),y=box.y+box.height/2;
  await cdp.send('Input.dispatchTouchEvent',{type:'touchStart',touchPoints:[{x:320,y}]});
  for(const x of [280,220,160,100,40]){await cdp.send('Input.dispatchTouchEvent',{type:'touchMove',touchPoints:[{x,y}]});await p.waitForTimeout(20)}
  await cdp.send('Input.dispatchTouchEvent',{type:'touchEnd',touchPoints:[]});await p.waitForTimeout(250);
  assert(await p.locator('.carousel-wrapper').evaluate(e=>e.scrollLeft>0));await cdp.detach();
 }
 assert.deepEqual(errors,[]);await browser.close();console.log('PASS PL/RU/EN: 7 widths, repeated breakpoints, native touch, original assets, desktop animation, offscreen/hidden/reduced-motion pauses, max one RAF, zero mobile RAF; no JS errors');
})().catch(e=>{console.error(e);process.exit(1)});

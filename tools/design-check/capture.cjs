const {chromium}=require('playwright');
const fs=require('fs');
(async()=>{
 const phase=process.argv[2]||'before',base=process.argv[3]||'http://localhost:8080';
 const browser=await chromium.launch({headless:true});
 const out='docs/design/screenshots';fs.mkdirSync(out,{recursive:true});
 const context=await browser.newContext({reducedMotion:'reduce'});
 await context.route('**/api/**',route=>['POST','PUT','PATCH','DELETE'].includes(route.request().method())?route.abort():route.continue());
 const results=[];
 for(const width of ((phase==='before'||process.argv.includes('--quick'))?[1440,375]:[375,430,768,1280,1440,1920])){
  const page=await context.newPage();await page.setViewportSize({width,height:1000});
  let errors=[];page.on('pageerror',e=>errors.push(e.message));
  for(const path of ['/', '/figures', '/figures/6820', '/events', '/search', '/favorites','/login','/purchases','/makers','/franchises','/new','/prices/6820','/chat','/status']){
   await page.goto(base+path);await page.waitForTimeout(650);
   results.push({width,path,errors:[...errors],...await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth,background:getComputedStyle(document.body).backgroundColor}))});
   if(['/', '/figures','/figures/6820','/events','/login'].includes(path)&&[375,1440].includes(width))await page.screenshot({path:`${out}/${phase}-${width}-${path.replaceAll('/','_')||'home'}.png`,fullPage:true});
   errors=[];
  }await page.close();
 }fs.writeFileSync(`docs/design/${phase}-checks.json`,JSON.stringify(results,null,2));await browser.close();
 console.log(JSON.stringify({pages:results.length,overflow:results.filter(r=>r.overflow),errors:results.filter(r=>r.errors.length)}));
})();

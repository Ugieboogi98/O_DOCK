const {chromium}=require('playwright');const assert=require('node:assert/strict');const fs=require('fs');
(async()=>{
 const browser=await chromium.launch();const page=await browser.newPage({viewport:{width:375,height:900},reducedMotion:'reduce'});let checks=[];
 await page.route('**/api/**',async r=>{
  if(r.request().url().includes('/api/compare'))return r.fulfill({json:{items:[]}});
  if(r.request().url().includes('/api/search/korean'))return r.fulfill({json:{items:[],answer:'검색 결과가 없습니다',sources:[]}});
  return ['POST','PUT','PATCH','DELETE'].includes(r.request().method())?r.abort():r.continue();
 });
 await page.goto('http://localhost:8080/');await page.getByRole('button',{name:'메뉴',exact:true}).click();assert.equal(await page.locator('#main-navigation').isVisible(),true);checks.push('mobile menu');
 await page.locator('#main-navigation').getByRole('link',{name:'전체 상품'}).click();await page.locator('.figure-card').first().waitFor();
 await page.locator('.filter-panel select').first().selectOption({index:1});await page.getByRole('button',{name:'필터 적용',exact:true}).click();await page.waitForURL(/manufacturer_id=/);checks.push('filter query');
 await page.getByRole('button',{name:'필터 초기화',exact:true}).click();await page.waitForURL('**/figures');await page.locator('.figure-card').first().waitFor();
 await page.getByRole('button',{name:'비교에 추가',exact:true}).nth(0).click();await page.getByRole('button',{name:'비교에 추가',exact:true}).nth(0).click();await page.getByRole('button',{name:'사양 비교하기',exact:true}).click();await page.getByRole('dialog',{name:'제품 비교'}).waitFor();await page.keyboard.press('Escape');assert.equal(await page.getByRole('dialog').count(),0);checks.push('comparison dialog / escape');
 await page.getByRole('button',{name:'다음',exact:true}).click();await page.waitForURL(/page=2/);checks.push('pagination');
 await page.goto('http://localhost:8080/figures/6820');await page.locator('.domestic-price-table tbody tr').nth(3).waitFor();assert.equal(await page.locator('.domestic-price-table tbody tr').count(),4);assert.equal(await page.locator('.product-secondary-actions a[target="_blank"]').count(),1);checks.push('detail / four retailer rows / source link');
 await page.goto('http://localhost:8080/');await page.getByRole('textbox',{name:'한국어 상품 검색'}).fill('프리렌');await page.locator('.header-search').getByRole('button',{name:'검색',exact:true}).click();await page.waitForURL(/search\?q=/);checks.push('header search / mocked response');
 await page.goto('http://localhost:8080/login');await page.locator('input[autocomplete="username"]').waitFor();checks.push('login fields');
 await page.goto('http://localhost:8080/');await page.keyboard.press('Tab');checks.push('keyboard navigation');
 const contrast=(a,b)=>{let l=h=>{let c=h.match(/\w\w/g).map(x=>parseInt(x,16)/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4);return c[0]*.2126+c[1]*.7152+c[2]*.0722};let x=l(a),y=l(b);return (Math.max(x,y)+.05)/(Math.min(x,y)+.05)};
 const tokens=await page.evaluate(()=>Object.fromEntries(['ink','bg','muted','surface-raised','accent','accent-ink','surface','on-accent'].map(k=>[k,getComputedStyle(document.documentElement).getPropertyValue('--'+k).trim().replace('#','')])));const ratios={body:contrast(tokens.ink,tokens.bg),muted:contrast(tokens.muted,tokens['surface-raised']),accent:contrast(tokens['accent-ink'],tokens.surface),button:contrast(tokens['on-accent'],tokens.accent)};assert(Object.values(ratios).every(n=>n>=4.5));
 fs.writeFileSync('docs/design/interaction-checks.json',JSON.stringify({checks,ratios,postResponsesMocked:true},null,2));console.log({checks,ratios});await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});

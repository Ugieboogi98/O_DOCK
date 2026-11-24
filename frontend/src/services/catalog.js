import {api} from './api'

// The existing API sorts IDs ascending. Read only the tail pages we need.
export async function newestPage(page=1, pageSize=24, request=api) {
 const {total}=await request('/figures?page_size=1')
 const end=Math.max(0,total-(page-1)*pageSize)
 const start=Math.max(0,end-pageSize)
 if (!end) return {items:[],total,page}
 const first=Math.floor(start/pageSize)+1
 const last=Math.ceil(end/pageSize)
 const rows=[]
 for(let n=first;n<=last;n++) {
  const data=await request(`/figures?page_size=${pageSize}&page=${n}`)
  rows.push(...data.items)
 }
 return {items:rows.slice(start-(first-1)*pageSize,end-(first-1)*pageSize).reverse(),total,page}
}

export const primaryMakerNames=['Good Smile Company','MegaHouse','Kotobukiya','Bandai Spirits','FuRyu','SEGA','TAITO']
export function isPrimaryMaker(maker){return primaryMakerNames.includes(maker.name)}

let rateCache=null
async function exchangeRate(){
 if(!rateCache || rateCache.until<Date.now()){
  const promise=api('/exchange-rate').catch(error=>{rateCache=null;throw error})
  rateCache={promise,until:Date.now()+300000}
 }
 return rateCache.promise
}
export function wonPrice(data,exchange=null){
 const prices=data.release_prices||[]
 const korea=prices.find(p=>p.currency==='KRW'&&['korea_official_sale','korea_official_list','official_release','official_list'].includes(p.price_kind))
 if(korea)return {...korea,label:'국내 공식가',estimated:false}
 const japan=data.japan_release_price||prices.find(p=>p.currency==='JPY'&&['official_release','official_list'].includes(p.price_kind))
 const rate=Number(exchange?.rate?.rate)
 if(japan && Number.isFinite(rate) && rate>0)return {price_amount:Math.round(Number(japan.price_amount)*rate),currency:'KRW',label:'원화 환산',estimated:true,rate_date:exchange.rate.rate_date,stale:!!exchange.error}
 return null
}
// Price reads are shared, cached briefly, and limited to two requests at a time.
const prices=new Map(),queue=[]
let running=0
function drain(){
 while(running<2 && queue.length){
  const job=queue.shift();running++
  job().finally(()=>{running--;drain()})
 }
}
export function officialPrice(figure){
 const key=`${figure.id}:${figure.variants?.[0]?.id||''}`
 const cached=prices.get(key)
 if(cached && cached.until>Date.now()) return cached.promise
 const promise=new Promise((resolve,reject)=>{
  queue.push(async()=>{
   try{
    const variant=figure.variants?.[0]?.id
    const data=await api(`/figures/${figure.id}/prices${variant?`?variant_id=${variant}`:''}`)
    const korea=wonPrice(data)
    resolve(korea||wonPrice(data,await exchangeRate()))
   }catch(e){prices.delete(key);reject(e)}
  })
 })
 prices.set(key,{promise,until:Date.now()+300000});drain()
 return promise
}

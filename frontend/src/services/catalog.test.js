import {describe,it,expect,vi} from 'vitest'
import {newestPage,isPrimaryMaker} from './catalog'
function fixture(count){
 const items=Array.from({length:count},(_,i)=>({id:i*3+1})) // IDs may have gaps.
 const request=vi.fn(async path=>{
  const query=new URL('http://local'+path).searchParams
  const size=Number(query.get('page_size')),page=Number(query.get('page')||1)
  return {total:items.length,items:items.slice((page-1)*size,page*size)}
 })
 return {items,request}
}
describe('recent products against the ascending catalog API',()=>{
 it.each([0,1,8,10,11,19,20,21,1387])('returns the newest ten from %i items',async count=>{
  const {items,request}=fixture(count)
  const result=await newestPage(1,10,request)
  expect(result.items).toEqual(items.slice(-10).reverse())
  expect(result.total).toBe(count)
  expect(request.mock.calls.length).toBeLessThanOrEqual(3)
 })
 it('paginates backwards without duplicates or omissions across uneven pages',async()=>{
  const {items,request}=fixture(53),result=[]
  for(let page=1;page<=3;page++)result.push(...(await newestPage(page,24,request)).items)
  expect(result).toEqual([...items].reverse())
  expect((await newestPage(4,24,request)).items).toEqual([])
 })
 it('propagates API failures instead of showing an empty success',async()=>{
  await expect(newestPage(1,10,async()=>{throw new Error('offline')})).rejects.toThrow('offline')
 })
 it('groups Hot Toys and future manufacturers under other',()=>{
  expect(isPrimaryMaker({name:'MegaHouse'})).toBe(true)
  expect(isPrimaryMaker({name:'Hot Toys'})).toBe(false)
  expect(isPrimaryMaker({name:'New Maker'})).toBe(false)
 })
})

import {wonPrice} from './catalog'
describe('won price display',()=>{
 const japan={price_amount:19800,currency:'JPY',price_kind:'official_list'}
 const korea={price_amount:175000,currency:'KRW',price_kind:'korea_official_sale'}
 it('prefers an actual Korean official price to conversion',()=>{
  expect(wonPrice({release_prices:[japan,korea]},{rate:{rate:9.15}})).toMatchObject({price_amount:175000,estimated:false,currency:'KRW'})
 })
 it('labels conversion and retains the rate date',()=>{
  expect(wonPrice({release_prices:[japan]},{rate:{rate:'9.15',rate_date:'2026-10-22'}})).toMatchObject({price_amount:181170,estimated:true,rate_date:'2026-10-22'})
 })
 it('never treats missing or invalid exchange rates as KRW',()=>{
  for(const rate of [undefined,0,-1,'invalid'])expect(wonPrice({release_prices:[japan]},{rate:{rate}})).toBeNull()
 })
})

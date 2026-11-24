import {describe,it,expect} from 'vitest'
import {createSSRApp,h} from 'vue'
import {renderToString} from '@vue/server-renderer'
import DomesticPrices from './DomesticPrices.vue'

const render=props=>renderToString(createSSRApp({render:()=>h(DomesticPrices,props)}))

describe('product detail domestic price table',()=>{
 it('shows the lowest price above three prices and a missing fourth store',async()=>{
  const html=await render({comparison:{lowest_price:140000,retailers:[
   {code:'maniahouse',price:150000,product_url:'https://maniahouse.co.kr/product/1'},
   {code:'figurefarm',price:145000,product_url:'https://www.figurefarm.net/shop/1'},
   {code:'comics_art',price:140000,is_lowest:true,product_url:'https://comics-art.co.kr/product/1'}
  ]}})
  expect(html).toContain('국내 유통 최저가')
  expect(html).toContain('140,000원')
  for(const name of ['매니아하우스','히어로타임','피규어팜','코믹스아트'])expect(html).toContain(name)
  expect(html.match(/가격 없음/g)).toHaveLength(1)
  expect(html).toContain('domestic-price-lowest')
 })
 it('keeps four empty rows and an empty main price when no prices exist',async()=>{
  const html=await render({comparison:{lowest_price:null,retailers:[]}})
  expect(html.match(/가격 없음/g)).toHaveLength(5)
 })
 it('shows loading and failure separately from missing prices',async()=>{
  const loading=await render({loading:true})
  expect(loading).toContain('가격 확인 중')
  expect(loading).not.toContain('가격 없음')
  const failed=await render({error:'일시적인 연결 오류'})
  expect(failed).toContain('가격 조회 실패')
  expect(failed).toContain('다시 확인')
  expect(failed).not.toContain('가격 없음')
 })
})

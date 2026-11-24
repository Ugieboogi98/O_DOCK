import {adminToken} from './admin'

export async function api(path,{method='GET',body,token=adminToken.value,signal}={}) {
 const controller=new AbortController()
 const timeout=setTimeout(()=>controller.abort(),120000)
 try {
  const response=await fetch('/api'+path,{method,headers:{'Content-Type':'application/json',...(token?{'X-Admin-Token':token}:{})},body:body?JSON.stringify(body):undefined,signal:signal||controller.signal})
  const data=await response.json().catch(()=>({detail:'서버 응답을 읽지 못했습니다.'}))
  if(!response.ok)throw new Error(typeof data.detail==='string'?data.detail:`요청 실패 (${response.status})`)
  return data
 } catch(e) {if(e.name==='AbortError')throw new Error('요청 시간이 초과되었습니다. 잠시 후 다시 시도하세요.');throw e}
 finally{clearTimeout(timeout)}
}
export const money=(amount,currency='JPY')=>amount==null?'미확인':new Intl.NumberFormat('ko-KR',{style:'currency',currency,maximumFractionDigits:0}).format(Number(amount))
export const date=(value)=>value?new Intl.DateTimeFormat('ko-KR',{dateStyle:'medium',timeStyle:'short'}).format(new Date(value)):'미확인'
export function safeUrl(value){try{const u=new URL(value);return ['https:','http:'].includes(u.protocol)?u.href:'#'}catch{return '#'}}

export function safeImage(value){return /^\/api\/media\/[a-f0-9]{64}\.(jpg|png|webp)$/.test(value||'')?value:safeUrl(value)}

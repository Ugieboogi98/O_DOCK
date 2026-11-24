import {ref} from 'vue'

// Retain credentials only for this browser tab. Never include them in URLs.
const key='odock-admin-session'
export const adminToken=ref(''),isAdmin=ref(false)

export function disconnectAdmin(){
 adminToken.value='';isAdmin.value=false
 try{sessionStorage.removeItem(key)}catch{}
}

export async function connectAdmin(candidate,request){
 disconnectAdmin()
 const token=candidate.trim()
 if(!token)throw new Error('관리자 토큰을 입력하세요.')
 const result=await request('/admin/session',{token})
 if(result.admin!==true)throw new Error('관리자 인증을 확인하지 못했습니다.')
 adminToken.value=token;isAdmin.value=true
 try{sessionStorage.setItem(key,token)}catch{}
}

export async function restoreAdmin(request){
 let token='';try{token=sessionStorage.getItem(key)||''}catch{}
 if(!token)return false
 try{await connectAdmin(token,request);return true}catch{disconnectAdmin();return false}
}

export async function refreshAsAdmin(request){
 if(!isAdmin.value)return null
 return request('/catalog/refresh',{method:'POST'})
}

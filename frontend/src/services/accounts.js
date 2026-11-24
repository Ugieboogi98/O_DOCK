import {ref} from 'vue'
import {api} from './api'
import {disconnectAdmin} from './admin'

export const currentUser=ref(null),identityVersion=ref(0)
let authRevision=0,identityRequest=0,changing=false
function changed(user){const previous=currentUser.value?.id;currentUser.value=user;if(previous!==user?.id)identityVersion.value++;return user}
export async function loadIdentity(request=api){
 if(changing)return currentUser.value
 const revision=authRevision,ticket=++identityRequest
 const result=await request('/auth/me')
 return revision===authRevision&&ticket===identityRequest?changed(result.user):currentUser.value
}
export async function authenticate(mode,credentials,request=api){
 const revision=++authRevision;changing=true
 disconnectAdmin()
 changed(null)
 try{
  await request('/auth/logout',{method:'POST'})
  if(revision!==authRevision)return currentUser.value
  const result=await request('/auth/'+mode,{method:'POST',body:credentials})
  return revision===authRevision?changed(result):currentUser.value
 }finally{if(revision===authRevision)changing=false}
}
export async function signOut(request=api){
 const revision=++authRevision;changing=true
 try{await request('/auth/logout',{method:'POST'});if(revision===authRevision){disconnectAdmin();changed(null)}}
 finally{if(revision===authRevision)changing=false}
}

import {defineStore} from 'pinia'
import {ref,watch} from 'vue'
import {currentUser,identityVersion} from '../services/accounts'

export const useChats=defineStore('chats',()=>{
 function storageKey(){return currentUser.value?.id===1?'figure-archive-chats':`figure-archive-chats:user:${currentUser.value?.id||'guest'}`}
 function read(){try{return JSON.parse(localStorage.getItem(storageKey())||'{}')}catch{return {}}}
 const conversations=ref(read())
 watch(identityVersion,()=>{conversations.value=read()},{flush:'sync'})
 function messages(key){return conversations.value[key]||[]}
 function add(key,msg,epoch=identityVersion.value){if(epoch!==identityVersion.value)return false;conversations.value[key]=[...messages(key),msg].slice(-40);persist();return true}
 function clear(key){delete conversations.value[key];persist()}
 function persist(){try{localStorage.setItem(storageKey(),JSON.stringify(conversations.value))}catch{}}
 return {messages,add,clear}
})

import {beforeEach,afterEach,describe,it,expect,vi} from 'vitest'
import {createPinia,setActivePinia} from 'pinia'
import {useChats} from './chats'
import {loadIdentity,identityVersion} from '../services/accounts'

let values
beforeEach(()=>{
 setActivePinia(createPinia());values=new Map()
 vi.stubGlobal('localStorage',{getItem:key=>values.get(key)||null,setItem:(key,value)=>values.set(key,value)})
})
afterEach(()=>vi.unstubAllGlobals())
const identity=id=>loadIdentity(async()=>({user:id?{id,username:'user'+id}:null}))

describe('account-bound chat history',()=>{
 it('rejects replies from a previous account and restores each user history',async()=>{
  await identity(101)
  const chats=useChats(),epoch=identityVersion.value
  chats.add('figure:1',{role:'user',text:'account A'},epoch)
  await identity(102)
  expect(chats.messages('figure:1')).toEqual([])
  expect(chats.add('figure:1',{role:'assistant',text:'late A reply'},epoch)).toBe(false)
  chats.add('figure:1',{role:'user',text:'account B'})
  await identity(101)
  expect(chats.messages('figure:1').map(m=>m.text)).toEqual(['account A'])
  expect(values.get('figure-archive-chats:user:102')).not.toContain('late A reply')
 })
 it('loads legacy ownerless history only for the administrator identity',async()=>{
  values.set('figure-archive-chats',JSON.stringify({'figure:1':[{role:'user',text:'legacy'}]}))
  await identity(null)
  const chats=useChats()
  expect(chats.messages('figure:1')).toEqual([])
  await identity(103)
  expect(chats.messages('figure:1')).toEqual([])
  await identity(1)
  expect(chats.messages('figure:1')[0].text).toBe('legacy')
 })
})

import {describe,it,expect,vi,beforeEach} from 'vitest'
import {createPinia,setActivePinia} from 'pinia'
vi.mock('../services/api',()=>({api:vi.fn()}))
import {api} from '../services/api'
import {loadIdentity} from '../services/accounts'
import {useArchive} from './archive'

beforeEach(()=>{setActivePinia(createPinia());vi.resetAllMocks()})
const identity=id=>loadIdentity(async()=>({user:id?{id,username:'user'+id}:null}))

describe('private state across identity changes',()=>{
 it('ignores an old favorites response after switching accounts',async()=>{
  const store=useArchive()
  await identity(11)
  let resolveOld
  api.mockImplementationOnce(()=>new Promise(resolve=>{resolveOld=resolve}))
  const old=store.loadFavorites()
  await identity(12)
  api.mockResolvedValueOnce([{id:2}])
  await store.loadFavorites()
  resolveOld([{id:1}]);await old
  expect(store.isFavorite({id:1,favorite:true})).toBe(false)
  expect(store.isFavorite({id:2})).toBe(true)
  await identity(null)
  expect(store.isFavorite({id:2,favorite:true})).toBe(false)
 })
 it('ignores a previous account favorite toggle that finishes late',async()=>{
  const store=useArchive()
  await identity(21)
  api.mockResolvedValueOnce([])
  await store.loadFavorites()
  let resolveOld
  api.mockImplementationOnce(()=>new Promise(resolve=>{resolveOld=resolve}))
  const toggle=store.toggleFavorite({id:5})
  await identity(22)
  resolveOld({favorite:true})
  expect(await toggle).toBeUndefined()
  expect(store.isFavorite({id:5})).toBe(false)
 })
 it('does not send an old click as the new user after an initial favorites read',async()=>{
  const store=useArchive()
  await identity(31)
  let resolveOld
  api.mockImplementationOnce(()=>new Promise(resolve=>{resolveOld=resolve}))
  const toggle=store.toggleFavorite({id:5})
  await identity(32)
  resolveOld([])
  expect(await toggle).toBeUndefined()
  expect(api).toHaveBeenCalledTimes(1)
 })
 it('can refresh again after a mutation supersedes an in-flight read',async()=>{
  const store=useArchive()
  await identity(41)
  api.mockResolvedValueOnce([])
  await store.loadFavorites()
  let resolveRead
  api.mockImplementationOnce(()=>new Promise(resolve=>{resolveRead=resolve}))
  const background=store.loadFavorites()
  api.mockResolvedValueOnce({favorite:true})
  await store.toggleFavorite({id:7})
  resolveRead([]);await background
  expect(store.isFavorite({id:7})).toBe(true)
  api.mockResolvedValueOnce([{id:7}])
  await store.loadFavorites()
  expect(api).toHaveBeenCalledTimes(4)
 })
})

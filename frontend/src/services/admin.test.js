import {beforeEach,afterEach,describe,it,expect,vi} from 'vitest'
import {adminToken,isAdmin,connectAdmin,disconnectAdmin,restoreAdmin,refreshAsAdmin} from './admin'
import {api} from './api'

let values
beforeEach(()=>{
 values=new Map()
 vi.stubGlobal('sessionStorage',{
  getItem:key=>values.get(key)||null,setItem:(key,value)=>values.set(key,value),removeItem:key=>values.delete(key)
 })
 disconnectAdmin()
})
afterEach(()=>{disconnectAdmin();vi.unstubAllGlobals()})

describe('administrator startup',()=>{
 it('never requests collection for a public visitor',async()=>{
  const request=vi.fn()
  expect(await restoreAdmin(request)).toBe(false)
  expect(await refreshAsAdmin(request)).toBeNull()
  expect(request).not.toHaveBeenCalled()
 })
 it('verifies the token before enabling administrator requests',async()=>{
  const request=vi.fn().mockResolvedValue({admin:true})
  await connectAdmin(' fixture ',request)
  expect(request).toHaveBeenCalledWith('/admin/session',{token:'fixture'})
  expect(isAdmin.value).toBe(true)
  expect(adminToken.value).toBe('fixture')
  await refreshAsAdmin(request)
  expect(request).toHaveBeenLastCalledWith('/catalog/refresh',{method:'POST'})
  disconnectAdmin()
  expect(values.size).toBe(0)
  expect(await refreshAsAdmin(request)).toBeNull()
 })
 it('restores a tab session and clears rejected credentials without collection',async()=>{
  await connectAdmin('fixture',vi.fn().mockResolvedValue({admin:true}))
  adminToken.value='';isAdmin.value=false
  expect(await restoreAdmin(vi.fn().mockResolvedValue({admin:true}))).toBe(true)
  const rejected=vi.fn().mockRejectedValue(new Error('denied'))
  expect(await restoreAdmin(rejected)).toBe(false)
  await refreshAsAdmin(rejected)
  expect(rejected).toHaveBeenCalledTimes(1)
  expect(isAdmin.value).toBe(false)
  expect(adminToken.value).toBe('')
  expect(values.size).toBe(0)
 })
 it('does not promote an unexpected verification response',async()=>{
  await expect(connectAdmin('wrong',vi.fn().mockResolvedValue({admin:false}))).rejects.toThrow()
  expect(isAdmin.value).toBe(false)
  expect(values.size).toBe(0)
 })
 it('sends a verified token as a header and removes it after disconnecting',async()=>{
  await connectAdmin('fixture',vi.fn().mockResolvedValue({admin:true}))
  const fetch=vi.fn().mockResolvedValue({ok:true,json:async()=>({})})
  vi.stubGlobal('fetch',fetch)
  await api('/catalog/refresh',{method:'POST'})
  expect(fetch.mock.calls[0][0]).toBe('/api/catalog/refresh')
  expect(fetch.mock.calls[0][1].headers['X-Admin-Token']).toBe('fixture')
  disconnectAdmin()
  await api('/figures')
  expect(fetch.mock.calls[1][1].headers['X-Admin-Token']).toBeUndefined()
 })
})

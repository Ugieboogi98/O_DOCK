import {describe,it,expect,vi,afterEach} from 'vitest'
import {currentUser,loadIdentity,authenticate,signOut} from './accounts'
import {adminToken,isAdmin,disconnectAdmin} from './admin'

afterEach(()=>{currentUser.value=null;disconnectAdmin()})
describe('account changes',()=>{
 it('revokes the previous browser session before logging into another account',async()=>{
  await loadIdentity(async()=>({user:{id:41,username:'old'}}))
  const request=vi.fn().mockResolvedValueOnce({logged_out:true}).mockResolvedValueOnce({id:42,username:'new'})
  adminToken.value='old-admin';isAdmin.value=true
  await authenticate('login',{username:'new',password:'fixture-password'},request)
  expect(request.mock.calls[0]).toEqual(['/auth/logout',{method:'POST'}])
  expect(request.mock.calls[1][0]).toBe('/auth/login')
  expect(currentUser.value.id).toBe(42)
  expect(isAdmin.value).toBe(false)
 })
 it('does not keep the previous identity when a new login fails',async()=>{
  await loadIdentity(async()=>({user:{id:51,username:'old'}}))
  const request=vi.fn().mockResolvedValueOnce({logged_out:true}).mockRejectedValueOnce(new Error('denied'))
  await expect(authenticate('login',{},request)).rejects.toThrow('denied')
  expect(currentUser.value).toBeNull()
 })
 it('clears the local identity after server logout',async()=>{
  await loadIdentity(async()=>({user:{id:61,username:'user'}}))
  await signOut(vi.fn().mockResolvedValue({logged_out:true}))
  expect(currentUser.value).toBeNull()
 })
 it('does not restore a stale identity response after logout',async()=>{
  let resolveOld
  const pending=loadIdentity(()=>new Promise(resolve=>{resolveOld=resolve}))
  await signOut(vi.fn().mockResolvedValue({logged_out:true}))
  resolveOld({user:{id:71,username:'old'}})
  await pending
  expect(currentUser.value).toBeNull()
 })
})

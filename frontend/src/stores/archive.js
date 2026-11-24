import {defineStore,storeToRefs} from 'pinia'
import {ref,watch} from 'vue'
import {api} from '../services/api'
import {adminToken,isAdmin,connectAdmin,disconnectAdmin,restoreAdmin,refreshAsAdmin} from '../services/admin'
import {identityVersion,loadIdentity} from '../services/accounts'
import {useFavorites} from './favorites'

export const useArchive=defineStore('archive',()=>{
 const status=ref(null),makers=ref([]),comparison=ref([]),error=ref('')
 async function load(){try{const [s,m]=await Promise.all([api('/status'),api('/manufacturers')]);status.value=s;makers.value=m;error.value=''}catch(e){error.value=e.message}}
 function toggle(id){comparison.value=comparison.value.includes(id)?comparison.value.filter(x=>x!==id):comparison.value.length<4?[...comparison.value,id]:comparison.value}
 const favoriteStore=useFavorites()
 const {favorites,favoritesReady,favoriteBusy}=storeToRefs(favoriteStore)
 const {isFavorite,loadFavorites,toggleFavorite}=favoriteStore
 watch(identityVersion,()=>{comparison.value=[]},{flush:'sync'})
 return {status,makers,comparison,adminToken,isAdmin,error,load,toggle,favorites,favoritesReady,favoriteBusy,isFavorite,loadFavorites,toggleFavorite,
  connectAdmin:async token=>{await connectAdmin(token,api);await loadIdentity();await loadFavorites()},
  disconnectAdmin:async()=>{disconnectAdmin();await loadIdentity()},
  restoreAdmin:()=>restoreAdmin(api),refreshCatalog:()=>refreshAsAdmin(api)}
})

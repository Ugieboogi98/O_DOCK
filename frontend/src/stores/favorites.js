import {defineStore} from 'pinia'
import {ref, watch} from 'vue'
import {api} from '../services/api'
import {currentUser, identityVersion} from '../services/accounts'

export const useFavorites = defineStore('favorites', () => {
 const favorites = ref({})
 const favoritesReady = ref(false)
 const favoriteBusy = ref({})
 let favoritesRequest = null
 let revision = 0

 function isFavorite(figure) {
  return !!currentUser.value && (favorites.value[figure.id] ?? false)
 }

 watch(identityVersion, () => {
  revision++
  favorites.value = {}
  favoritesReady.value = false
  favoriteBusy.value = {}
  favoritesRequest = null
 }, {flush: 'sync'})

 function loadFavorites() {
  if (favoritesRequest) return favoritesRequest
  const start = revision
  const request = api('/favorites').then(rows => {
   if (start === revision) {
    favorites.value = Object.fromEntries(rows.map(row => [row.id, true]))
    favoritesReady.value = true
   }
   return rows
  }).finally(() => {
   if (favoritesRequest === request) favoritesRequest = null
  })
  favoritesRequest = request
  return request
 }

 async function toggleFavorite(figure) {
  if (!currentUser.value) throw new Error('로그인 후 관심상품을 등록할 수 있습니다.')
  const id = figure.id
  const epoch = identityVersion.value
  if (favoriteBusy.value[id]) return undefined
  favoriteBusy.value[id] = true
  try {
   if (!favoritesReady.value) await loadFavorites()
   if (epoch !== identityVersion.value) return undefined
   const result = await api('/favorites/' + id, {method: isFavorite(figure) ? 'DELETE' : 'PUT'})
   if (epoch !== identityVersion.value) return undefined
   revision++
   favorites.value[id] = !!result.favorite
   return favorites.value[id]
  } finally {
   if (epoch === identityVersion.value) favoriteBusy.value[id] = false
  }
 }

 return {favorites, favoritesReady, favoriteBusy, isFavorite, loadFavorites, toggleFavorite}
})

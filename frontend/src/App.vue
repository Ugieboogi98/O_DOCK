<script setup>
import {ref,onMounted,onUnmounted} from 'vue';import {ArrowUpRight,Search} from 'lucide-vue-next';import {useArchive} from './stores/archive';import ComparisonPanel from './components/ComparisonPanel.vue'
import {api} from './services/api'
import {currentUser,loadIdentity} from './services/accounts'
import {useRouter} from 'vue-router'
const router=useRouter(),searchText=ref(''),menuOpen=ref(false)
function search(){router.push({path:'/search',query:searchText.value.trim()?{q:searchText.value.trim()}:{}})}
const store=useArchive()
const catalogState=ref(null)
const justAdded=ref(0)
let pollingId=null, lastFinished=null, initialized=false
function syncIdentity(){loadIdentity().then(()=>{if(currentUser.value)store.loadFavorites().catch(()=>{})}).catch(()=>{})}
async function checkCatalog(){
 try {
  const state=await api('/catalog/status')
  const changed=initialized && state.finished_at && lastFinished!==state.finished_at && state.state!=='running'
  if(changed){
   justAdded.value=Number(state.new_products||0)
   await store.load()
   window.dispatchEvent(new Event('catalog-updated'))
  }
  lastFinished=state.finished_at||lastFinished
  initialized=true
  catalogState.value=state
 }catch{/* Main site still works if catalog status is unavailable. */}
}
onMounted(async()=>{
 store.load()
 await checkCatalog() // Establish baseline before triggering refresh.
 await store.restoreAdmin()
 await loadIdentity().catch(()=>{})
 if(currentUser.value)await store.loadFavorites().catch(()=>{})
 try{await store.refreshCatalog()}catch{/* Noncritical administrator task. */}
 await checkCatalog()
 pollingId=setInterval(checkCatalog,7000)
 window.addEventListener('focus',syncIdentity)
})
onUnmounted(()=>{if(pollingId)clearInterval(pollingId);window.removeEventListener('focus',syncIdentity)})
</script>
<template>
 <a class="skip-link" href="#main-content">본문으로 건너뛰기</a><header class="site-header archive-header"><div class="archive-header-top"><RouterLink to="/" class="brand-wordmark" aria-label="O_DOCK 홈">O<span>_</span>DOCK</RouterLink><form class="header-search" action="/search" @submit.prevent="search"><Search :size="17"/><input v-model="searchText" aria-label="한국어 상품 검색" placeholder="어떤 피규어를 찾고 있나요?"><button aria-label="검색"><ArrowUpRight :size="18"/></button></form><button class="mobile-menu-button" aria-controls="main-navigation" :aria-expanded="menuOpen" @click="menuOpen=!menuOpen">{{menuOpen?'닫기':'메뉴'}}</button></div><div id="main-navigation" class="archive-nav-row" :class="{'is-open':menuOpen}" @click="menuOpen=false"><nav aria-label="주요 메뉴"><RouterLink to="/" exact-active-class="home-active">홈</RouterLink><RouterLink to="/figures">전체 상품</RouterLink><RouterLink to="/franchises">작품 목록</RouterLink><RouterLink to="/events">행사</RouterLink><RouterLink to="/favorites">찜 목록</RouterLink><RouterLink to="/purchases">구매 목록</RouterLink><RouterLink to="/login">{{currentUser?currentUser.username+' 님':'로그인'}}</RouterLink></nav></div></header>
 <main id="main-content" tabindex="-1"><div v-if="catalogState?.state==='running'" class="notice" role="status">최신 피규어를 확인 중입니다. 기존 목록은 계속 사용할 수 있습니다.</div><div v-else-if="justAdded>0" class="notice" role="status">새로운 피규어 {{justAdded}}개가 추가되었습니다.</div><div v-if="store.error" class="notice error" role="alert">{{store.error}} <button @click="store.load">다시 연결</button></div><RouterView/></main>
 <footer><div class="footer-top"><span class="logo">O_DOCK</span><p>Our figures DOCK</p><div class="archive-utility"><RouterLink to="/chat">AI 리서치 <ArrowUpRight :size="12"/></RouterLink><RouterLink to="/status">데이터 현황</RouterLink></div></div><div class="footer-bottom"><span>SSAFY AI CORE PROJECT · 2026</span><span>가격은 관측 시점 기준 · 원문 확인 후 구매하세요</span></div></footer><ComparisonPanel/>
</template>

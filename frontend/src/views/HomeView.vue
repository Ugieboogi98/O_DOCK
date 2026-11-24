<script setup>
import {computed,ref,onMounted,onUnmounted} from 'vue'
import {ArrowRight,ChevronLeft,ChevronRight,Pause,Play,Heart,ShoppingBag,UserRound,ImageOff,ArrowUpRight} from 'lucide-vue-next'
import {useArchive} from '../stores/archive'
import {safeImage} from '../services/api'
import {newestPage,primaryMakerNames,isPrimaryMaker} from '../services/catalog'
import FavoriteButton from '../components/FavoriteButton.vue'
import HomeProductCard from '../components/HomeProductCard.vue'
const store=useArchive(),recent=ref([]),loading=ref(true),error=ref(''),active=ref(0),paused=ref(false),hovered=ref(false),focused=ref(false),imageFailed=ref(false)
const slide=computed(()=>recent.value[active.value])
const makers=computed(()=>primaryMakerNames.map(name=>store.makers.find(m=>m.name===name)).filter(Boolean))
const otherCount=computed(()=>store.makers.filter(m=>!isPrimaryMaker(m)).reduce((sum,m)=>sum+Number(m.count||0),0))
let timer,controller,version=0,motion
const reducedMotion=ref(false)
async function load(){
 const current=++version;controller?.abort();controller=new AbortController()
 loading.value=true;error.value=''
 try{
  const {api}=await import('../services/api')
  const data=await newestPage(1,10,path=>api(path,{signal:controller.signal}))
  if(current===version){recent.value=data.items;active.value=0;imageFailed.value=false}
 }catch(e){if(current===version)error.value=e.message}
 finally{if(current===version)loading.value=false}
}
function move(step){active.value=(active.value+step+recent.value.length)%recent.value.length;imageFailed.value=false;restartTimer()}
function restartTimer(){
 clearInterval(timer)
 timer=setInterval(()=>{if(!paused.value&&!hovered.value&&!focused.value&&!reducedMotion.value&&!document.hidden&&recent.value.length>1)move(1)},7000)
}
function updateMotion(){reducedMotion.value=motion.matches}
function focusOut(event){if(!event.currentTarget.contains(event.relatedTarget))focused.value=false}
onMounted(()=>{load();motion=window.matchMedia('(prefers-reduced-motion: reduce)');updateMotion();motion.addEventListener('change',updateMotion);restartTimer();window.addEventListener('catalog-updated',load)})
onUnmounted(()=>{version++;controller?.abort();clearInterval(timer);motion?.removeEventListener('change',updateMotion);window.removeEventListener('catalog-updated',load)})
</script>
<template>
 <div class="archive-home">
  <div class="home-top-grid">
   <section class="home-showcase" aria-label="최근 추가 상품" aria-roledescription="캐러셀" @mouseenter="hovered=true" @mouseleave="hovered=false" @focusin="focused=true" @focusout="focusOut" @keydown.left.prevent="recent.length&&move(-1)" @keydown.right.prevent="recent.length&&move(1)">
    <div v-if="loading" class="home-slide-status" role="status">새로 추가된 상품을 불러오는 중…</div>
    <div v-else-if="error" class="home-slide-status" role="alert"><p>{{error}}</p><button class="button" @click="load">다시 불러오기</button></div>
    <template v-else-if="slide">
     <div class="home-slide" :key="slide.id" role="group" aria-roledescription="슬라이드" :aria-label="`${active+1} / ${recent.length}`">
      <div class="home-slide-copy"><p class="home-slide-maker">{{slide.manufacturer}}</p><h1><RouterLink :to="`/figures/${slide.id}`">{{slide.name_ko||slide.name_original}}</RouterLink></h1><p class="home-slide-line">{{slide.product_line||slide.franchise||'새롭게 아카이브에 담긴 피규어'}}</p><RouterLink :to="`/figures/${slide.id}`" class="home-detail-link">상품 자세히 보기 <ArrowUpRight :size="17"/></RouterLink></div>
      <div class="home-slide-image"><RouterLink :to="`/figures/${slide.id}`" class="home-slide-art" :aria-label="`${slide.name_ko||slide.name_original} 상세 보기`"><img v-if="slide.thumbnail&&!imageFailed" :src="safeImage(slide.thumbnail)" :alt="slide.name_ko||slide.name_original" fetchpriority="high" @error="imageFailed=true"><span v-else class="home-image-empty"><ImageOff :size="48" :stroke-width="1"/>이미지 준비 중</span></RouterLink><FavoriteButton :figure="slide"/></div>
     </div>
     <div class="home-slide-controls"><span class="home-slide-count"><strong>{{String(active+1).padStart(2,'0')}}</strong><span>/ {{String(recent.length).padStart(2,'0')}}</span></span><div class="home-slide-track" aria-hidden="true"><span :style="{width:((active+1)/recent.length*100)+'%'}"></span></div><div class="home-slide-buttons"><button aria-label="이전 상품" :disabled="recent.length<2" @click="move(-1)"><ChevronLeft :size="19"/></button><button v-if="!reducedMotion" :aria-label="paused?'자동 넘김 재생':'자동 넘김 일시정지'" :aria-pressed="paused" @click="paused=!paused"><Play v-if="paused" :size="15"/><Pause v-else :size="15"/></button><button aria-label="다음 상품" :disabled="recent.length<2" @click="move(1)"><ChevronRight :size="19"/></button></div></div>
    </template>
    <div v-else class="home-slide-status">아직 등록된 상품이 없습니다.</div>
   </section>
   <aside class="home-personal" aria-label="나의 컬렉션">
    <div class="home-account"><div class="home-account-top"><span>나의 컬렉션</span><UserRound :size="20" :stroke-width="1.4"/></div><h2>좋아하는 피규어,<br>나의 컬렉션으로</h2><p>좋아하는 상품을 담고,<br>구매한 순간을 기록하세요.</p><RouterLink to="/login" class="home-login-link">내 계정 <ArrowRight :size="16"/></RouterLink><small>관심상품과 구매 기록은 로그인 후 이용할 수 있습니다.</small></div>
    <div class="home-personal-links"><RouterLink to="/favorites"><Heart :size="24" :stroke-width="1.4"/><span>관심 상품</span><ArrowUpRight :size="16"/></RouterLink><RouterLink to="/purchases"><ShoppingBag :size="24" :stroke-width="1.4"/><span>구매 상품</span><ArrowUpRight :size="16"/></RouterLink></div>
   </aside>
  </div>
  <section class="home-section" aria-labelledby="maker-heading"><div class="home-section-heading"><div><h2 id="maker-heading">제조사별 탐색</h2></div><RouterLink to="/makers">모두 보기 <ArrowRight :size="16"/></RouterLink></div>
   <div class="home-maker-grid"><RouterLink v-for="(maker,index) in makers" :key="maker.id" :to="{path:'/figures',query:{manufacturer_id:maker.id}}" class="home-maker" :class="'home-maker-'+index"><strong>{{maker.name}}</strong><span class="home-maker-bottom"><span>{{maker.name_ko||maker.name}}</span><ArrowUpRight :size="16"/></span></RouterLink><RouterLink to="/makers?group=other" class="home-maker home-maker-other"><strong>기타</strong><span class="home-maker-bottom"><span>기타 제조사 · {{otherCount.toLocaleString()}}개</span><ArrowUpRight :size="16"/></span></RouterLink></div>
  </section>
  <section class="home-section" aria-labelledby="new-heading"><div class="home-section-heading"><div><h2 id="new-heading">신규 상품</h2></div><RouterLink to="/new">전체 보기 <ArrowRight :size="16"/></RouterLink></div><p v-if="loading" class="empty" role="status">상품을 불러오는 중…</p><p v-else-if="error" class="error">{{error}}</p><div v-else class="home-product-grid"><HomeProductCard v-for="figure in recent.slice(0,8)" :key="figure.id" :figure="figure"/></div></section>
 </div>
</template>

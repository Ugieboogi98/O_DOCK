<script setup>
import {ref,onMounted,onUnmounted} from 'vue'
import {ArrowUpRight,ImageOff} from 'lucide-vue-next'
import FavoriteButton from './FavoriteButton.vue'
import {safeImage,money} from '../services/api'
import {officialPrice} from '../services/catalog'
const props=defineProps({figure:{type:Object,required:true}})
const root=ref(null),price=ref(null),priceState=ref('waiting'),imageFailed=ref(false)
let observer,disposed=false
async function loadPrice(){
 if(priceState.value!=='waiting')return
 priceState.value='loading'
 try{const value=await officialPrice(props.figure);if(!disposed){price.value=value;priceState.value='ready'}}
 catch{if(!disposed)priceState.value='error'}
}
onMounted(()=>{
 if(!('IntersectionObserver' in window)){loadPrice();return}
 observer=new IntersectionObserver(entries=>{if(entries.some(e=>e.isIntersecting)){observer.disconnect();loadPrice()}},{rootMargin:'120px'})
 observer.observe(root.value)
})
onUnmounted(()=>{disposed=true;observer?.disconnect()})
</script>
<template>
 <article ref="root" class="home-product-card">
  <div class="product-image-wrap"><RouterLink :to="`/figures/${figure.id}`" class="home-product-art" :aria-label="`${figure.name_ko||figure.name_original} 상세 보기`">
   <img v-if="figure.thumbnail&&!imageFailed" :src="safeImage(figure.thumbnail)" :alt="figure.name_ko||figure.name_original" loading="lazy" @error="imageFailed=true">
   <span v-else class="home-image-empty"><ImageOff :size="30" :stroke-width="1"/>이미지 준비 중</span>
  </RouterLink><FavoriteButton :figure="figure"/></div>
  <div class="home-product-maker">{{figure.manufacturer}}</div>
  <h3><RouterLink :to="`/figures/${figure.id}`">{{figure.name_ko||figure.name_original}}</RouterLink></h3>
  <div class="home-product-price"><span>{{price?.label||'가격'}}</span><strong v-if="price">{{price.estimated?'약 ':''}}{{Number(price.price_amount).toLocaleString('ko-KR')}}원</strong><span v-else>{{priceState==='error'?'상세에서 확인':priceState==='ready'?'가격 미확인':'확인 중…'}}</span><small v-if="price?.estimated">{{price.rate_date}} 환율 기준{{price.stale?' · 저장된 환율':''}}</small></div>
 </article>
</template>

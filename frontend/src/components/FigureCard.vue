<script setup>
import {ArrowUpRight,Check,Plus,ImageOff} from 'lucide-vue-next'
import {useArchive} from '../stores/archive'
import FavoriteButton from './FavoriteButton.vue'
import {ref,watch} from 'vue'
import {safeImage} from '../services/api'
const emit=defineEmits(['favorite-changed']);const props=defineProps({figure:Object});const imageFailed=ref(false);watch(()=>props.figure?.thumbnail,()=>imageFailed.value=false);const store=useArchive()
</script>
<template>
 <article class="figure-card">
  <div class="product-image-wrap"><RouterLink :to="`/figures/${figure.id}`" class="card-art" :class="`art-${figure.id%4}`" :aria-label="figure.name_original+' 상세 보기'">
   <span class="card-number">OD—{{ String(figure.id).padStart(4,'0') }}</span>
   <img v-if="figure.thumbnail&&!imageFailed" :src="safeImage(figure.thumbnail)" :alt="figure.name_ko||figure.name_original" class="catalog-image" loading="lazy" @error="imageFailed=true"><div v-else class="card-image-empty"><ImageOff :size="28" :stroke-width="1.5"/><span>이미지 준비 중</span></div>
   <span v-if="false" class="art-label">공식 사진은 원문에서 확인</span><ArrowUpRight class="art-arrow" :size="19"/>
  </RouterLink><FavoriteButton :figure="figure" @changed="v=>emit('favorite-changed',v)"/></div>
  <div class="card-meta"><span>{{ figure.manufacturer }}</span><button class="icon-button" @click="store.toggle(figure.id)" :aria-label="store.comparison.includes(figure.id)?'비교에서 제외':'비교에 추가'" :aria-pressed="store.comparison.includes(figure.id)"><Check v-if="store.comparison.includes(figure.id)" :size="17"/><Plus v-else :size="17"/></button></div>
  <h3><RouterLink :to="`/figures/${figure.id}`">{{ figure.name_ko || figure.name_original }}</RouterLink></h3>
  <p class="card-bottom"><span>{{ figure.product_line || (figure.type==='model_kit'?'조립형 제품':'피규어') }}</span><span>{{ figure.scale || 'NON-SCALE / 미확인' }}</span></p>
 </article>
</template>

<script setup>
import {onMounted,ref,watch} from 'vue';import {useArchive} from '../stores/archive';import FigureCard from '../components/FigureCard.vue'
import {currentUser,identityVersion} from '../services/accounts'
const store=useArchive();const items=ref([]),error=ref(''),loading=ref(true)
async function load(){const epoch=identityVersion.value;items.value=[];if(!currentUser.value){loading.value=false;error.value='로그인 후 관심상품을 확인할 수 있습니다.';return}loading.value=true;error.value='';try{const rows=await store.loadFavorites();if(epoch===identityVersion.value)items.value=rows}catch(e){error.value=e.message}finally{loading.value=false}}
onMounted(load);watch(identityVersion,load)
</script>
<template><section class="section"><p class="eyebrow">MY WISHLIST</p><h1>관심상품</h1><RouterLink v-if="!currentUser" to="/login" class="button">로그인</RouterLink><p>하트로 담아둔 피규어 {{items.length}}개</p><p v-if="error" class="error">{{error}} <button @click="load">다시 시도</button></p><p v-if="loading">불러오는 중…</p><p v-else-if="!items.length" class="empty">아직 관심상품이 없습니다. <RouterLink to="/figures">상품 둘러보기</RouterLink></p><div class="figure-grid"><FigureCard v-for="f in items" :key="f.id" :figure="f" @favorite-changed="active=>{if(!active)items=items.filter(x=>x.id!==f.id)}"/></div></section></template>

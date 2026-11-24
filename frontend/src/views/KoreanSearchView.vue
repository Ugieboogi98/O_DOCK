<script setup>
import {ref,watch,onUnmounted} from 'vue'
import {useRoute,useRouter} from 'vue-router'
import {Search,ArrowRight} from 'lucide-vue-next'
import {api} from '../services/api'
import FigureCard from '../components/FigureCard.vue'
import SourceList from '../components/SourceList.vue'
const route=useRoute(),router=useRouter(),query=ref(''),loading=ref(false),error=ref(''),result=ref(null)
let generation=0,controller
function search(){const q=query.value.trim();if(q)router.push({path:'/search',query:{q}})}
async function load(){
 const current=++generation;controller?.abort();controller=new AbortController()
 query.value=String(route.query.q||'');result.value=null;error.value=''
 if(!query.value.trim()){loading.value=false;return}
 loading.value=true
 try{const value=await api('/search/korean',{method:'POST',body:{query:query.value.trim(),top_k:8},signal:controller.signal});if(current===generation)result.value=value}
 catch(e){if(current===generation)error.value=e.message}
 finally{if(current===generation)loading.value=false}
}
watch(()=>route.query.q,load,{immediate:true})
onUnmounted(()=>{generation++;controller?.abort()})
</script>
<template><section class="page-heading"><h1>한국어로 찾기</h1><p>상품명이나 궁금한 내용을 입력하세요. 저장된 한국어 번역과 제품 정보에서 근거를 찾습니다.</p></section>
<form class="search-bar" @submit.prevent="search"><Search :size="20"/><input v-model="query" maxlength="500" required aria-label="한국어 검색어" placeholder="예: 프리렌 피규어의 재질과 크기 알려줘"><button :disabled="loading">검색 <ArrowRight :size="17"/></button></form>
<p class="fine-print">의미가 유사한 상품을 찾는 검색입니다. 정확한 높이·발매 연도 조건은 <RouterLink to="/figures">전체 상품의 상세 필터</RouterLink>를 이용하세요.</p>
<p v-if="loading" class="notice" role="status">한국어 근거를 검색하고 답변을 준비하고 있습니다…</p>
<div v-else-if="error" class="notice error" role="alert">{{error}} <button @click="load">다시 시도</button></div>
<template v-else-if="result"><p v-for="w in result.warnings||[]" :key="w" class="notice">{{w}}</p>
<section class="personal-panel korean-answer"><h2>{{result.mode==='korean_rag'?'검색 답변':'검색 근거'}}</h2><p class="preserve-lines">{{result.answer}}</p><SourceList :sources="result.sources||[]"/><p class="fine-print">AI 번역을 활용한 결과입니다. 상품명·수치는 연결된 원문과 함께 확인하세요.</p></section>
<section class="section"><div class="section-title"><h2>관련 상품</h2><span>{{result.items?.length||0}}개</span></div><div class="figure-grid"><FigureCard v-for="figure in result.items||[]" :key="figure.id" :figure="figure"/></div><p v-if="!result.items?.length" class="empty">표시할 상품이 없습니다.</p></section></template>
</template>
<style scoped>.korean-answer{margin-top:24px}.korean-answer .preserve-lines{line-height:1.9;overflow-wrap:anywhere}.fine-print a{text-decoration:underline}.search-bar button{display:flex;align-items:center;gap:6px;white-space:nowrap}</style>

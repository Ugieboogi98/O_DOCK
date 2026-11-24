<script setup>
import {ref,computed,onMounted,onUnmounted} from 'vue'
import {api} from '../services/api'
import {ArrowUpRight,Search} from 'lucide-vue-next'
const franchises=ref([]),query=ref(''),loading=ref(false),error=ref(''),scanned=ref(0),total=ref(0),unknown=ref(0)
let controller,version=0
const visible=computed(()=>franchises.value.filter(f=>f.name.toLocaleLowerCase().includes(query.value.toLocaleLowerCase())))
async function load(){
 const current=++version;controller?.abort();controller=new AbortController()
 const signal=controller.signal,groups=new Map(),seen=new Set()
 loading.value=true;error.value='';scanned.value=0;unknown.value=0;franchises.value=[]
 try{
  const data=await api('/franchises',{signal})
  if(current!==version)return
  franchises.value=data.items.sort((a,b)=>a.name.localeCompare(b.name,'ko'))
  unknown.value=data.unknown
  total.value=data.total
  scanned.value=data.total
 }catch(e){if(current===version)error.value=e.message}
 finally{if(current===version)loading.value=false}
}
onMounted(load)
onUnmounted(()=>{version++;controller?.abort()})
</script>
<template><section class="page-heading"><p class="eyebrow">FRANCHISES</p><h1>작품 목록</h1><p>상품 정보에 작품명이 등록된 항목만 표시합니다. 작품명 미확인 상품 {{unknown.toLocaleString()}}개</p></section><form class="search-bar" @submit.prevent><Search :size="18"/><input v-model="query" aria-label="작품명 검색" placeholder="찾고 있는 작품을 입력하세요"></form><p v-if="loading" class="notice" role="status">작품 정보를 모으는 중… {{scanned.toLocaleString()}} / {{total.toLocaleString()}}개 상품</p><p v-if="error" class="error" role="alert">일부 작품을 불러오지 못했습니다. {{error}} <button @click="load">다시 시도</button></p><div class="franchise-grid"><RouterLink v-for="item in visible" :key="item.name" :to="{path:'/figures',query:{franchise:item.name}}"><h2>{{item.name}}</h2><span>{{item.count}}개 상품 <ArrowUpRight :size="16"/></span></RouterLink></div><p v-if="!loading&&!error&&!visible.length" class="empty">표시할 작품이 없습니다.</p></template>

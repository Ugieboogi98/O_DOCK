<script setup>
import {ref,watch,onUnmounted} from 'vue'
import {useRoute,useRouter} from 'vue-router'
import {ArrowLeft,ArrowRight} from 'lucide-vue-next'
import {api} from '../services/api'
import {newestPage} from '../services/catalog'
import HomeProductCard from '../components/HomeProductCard.vue'
const route=useRoute(),router=useRouter(),items=ref([]),total=ref(0),loading=ref(false),error=ref(''),page=ref(1)
let version=0,controller
async function load(){
 const current=++version;controller?.abort();controller=new AbortController()
 const parsed=Number(route.query.page)
 page.value=Number.isSafeInteger(parsed)&&parsed>0?parsed:1;loading.value=true;error.value=''
 try{const result=await newestPage(page.value,24,path=>api(path,{signal:controller.signal}));if(current===version){items.value=result.items;total.value=result.total}}
 catch(e){if(current===version)error.value=e.message}
 finally{if(current===version)loading.value=false}
}
function navigate(value){router.push({path:'/new',query:{page:value}})}
watch(()=>route.query.page,load,{immediate:true})
onUnmounted(()=>{version++;controller?.abort()})
</script>
<template><section class="page-heading"><h1>신규 상품<span class="count">{{total.toLocaleString()}}</span></h1></section><p v-if="loading" class="empty" role="status">상품을 불러오는 중…</p><div v-else-if="error" class="error" role="alert">{{error}} <button @click="load">다시 시도</button></div><div v-else-if="items.length" class="home-product-grid"><HomeProductCard v-for="figure in items" :key="figure.id" :figure="figure"/></div><p v-else class="empty">표시할 상품이 없습니다.</p><div class="pagination"><button :disabled="page<=1||loading" @click="navigate(page-1)"><ArrowLeft :size="16"/> 이전</button><span>{{page}} / {{Math.max(1,Math.ceil(total/24))}}</span><button :disabled="page*24>=total||loading" @click="navigate(page+1)">다음 <ArrowRight :size="16"/></button></div></template>

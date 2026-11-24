<script setup>
import {computed} from 'vue'
import {useRoute} from 'vue-router'
import {ArrowUpRight} from 'lucide-vue-next'
import {useArchive} from '../stores/archive'
import {isPrimaryMaker} from '../services/catalog'
const route=useRoute(),store=useArchive()
const other=computed(()=>route.query.group==='other')
const makers=computed(()=>store.makers.filter(m=>!other.value||!isPrimaryMaker(m)))
</script>
<template><section class="page-heading"><p class="eyebrow">BRANDS</p><h1>{{other?'기타 제조사':'전체 제조사'}}</h1><p>{{other?'Hot Toys를 비롯한 다양한 제조사의 상품을 만나보세요.':'제조사를 선택하면 해당 상품 목록으로 이동합니다.'}}</p></section><div class="home-maker-grid"><RouterLink class="home-maker" v-for="maker in makers" :key="maker.id" :to="{path:'/figures',query:{manufacturer_id:maker.id}}"><span class="home-maker-number">{{maker.count.toLocaleString()}} PRODUCTS</span><strong>{{maker.name}}</strong><span class="home-maker-bottom">{{maker.name_ko}}<ArrowUpRight :size="16"/></span></RouterLink></div><p v-if="!makers.length" class="empty">표시할 제조사가 없습니다.</p></template>

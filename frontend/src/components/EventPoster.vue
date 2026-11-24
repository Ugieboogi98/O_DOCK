<script setup>
import {ref,computed,watch} from 'vue'
import {Image} from 'lucide-vue-next'
const props=defineProps({src:String,alt:String}),failed=ref(false)
const url=computed(()=>{
  const value=props.src||''
  if (/^\/api\/events\/images\/\d+\/\d+$/.test(value)) return value
  try {
    const parsed=new URL(value)
    if (parsed.protocol==='https:'&&!parsed.username&&!parsed.password) return parsed.href
  } catch {}
  return ''
})
watch(()=>props.src,()=>{failed.value=false})
</script>
<template><img v-if="url&&!failed" :src="url" :alt="alt||'Event image'" loading="lazy" referrerpolicy="no-referrer" @error="failed=true"><div v-else class="event-poster-empty"><Image :size="32" :stroke-width="1.1"/><span>O_DOCK EVENTS</span></div></template>

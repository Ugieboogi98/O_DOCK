<script setup>
import {ExternalLink} from 'lucide-vue-next'
import {safeUrl,date} from '../services/api'
defineProps({sources:{type:Array,default:()=>[]}})
</script>
<template><ul class="sources"><li v-for="(s,i) in sources" :key="s.id||i"><a :href="safeUrl(s.url)" target="_blank" rel="noopener noreferrer"><span class="tag">{{ s.number?`근거 ${s.number}`:s.source_type }}</span> {{ s.title }} <ExternalLink :size="13"/></a><small v-if="s.collected_at">{{ date(s.collected_at) }} · {{ s.usage_status }}</small></li></ul></template>

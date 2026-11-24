<script setup>
import {computed,ref} from 'vue'
import {Heart} from 'lucide-vue-next'
import {useArchive} from '../stores/archive'
const props=defineProps({figure:{type:Object,required:true},labeled:Boolean}),emit=defineEmits(['changed']),store=useArchive(),error=ref('')
const active=computed(()=>store.isFavorite(props.figure)),busy=computed(()=>!!store.favoriteBusy[props.figure.id])
async function toggle(){
 error.value=''
 try{const value=await store.toggleFavorite(props.figure);if(value!==undefined)emit('changed',value)}
 catch(e){error.value=e.message}
}
</script>
<template><span class="favorite-control" :class="{'favorite-labeled':labeled}"><button type="button" class="favorite-circle" :class="{hearted:active}" :disabled="busy" :aria-busy="busy" :aria-pressed="active" :aria-label="active?'관심상품 해제':'관심상품 등록'" :title="active?'관심상품 해제':'관심상품 등록'" @click.stop.prevent="toggle"><Heart :size="21" :stroke-width="1.7" :fill="active?'currentColor':'none'"/><span v-if="labeled">{{active?'관심 등록됨':'관심 등록'}}</span></button><small class="favorite-error" role="alert" v-if="error">{{error}}</small></span></template>

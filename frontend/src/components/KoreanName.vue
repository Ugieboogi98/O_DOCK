<script setup>
import {isAdmin} from '../services/admin'
import {ref} from 'vue';import {api} from '../services/api'
const props=defineProps({figure:Object});const emit=defineEmits(['saved']);const name=ref(props.figure.name_ko||''),error=ref(''),busy=ref(false)
async function save(auto=false){busy.value=true;error.value='';try{const r=await api(`/figures/${props.figure.id}/${auto?'translate':'korean-name'}`,{method:auto?'POST':'PUT',body:auto?undefined:{name_ko:name.value}});name.value=r.name_ko;emit('saved',r.name_ko)}catch(e){error.value=e.message}finally{busy.value=false}}
</script>
<template><p v-if="figure.semantic_name_ko&&figure.semantic_name_ko!==figure.name_ko" class="fine-print">새 한국어 번역: {{figure.semantic_name_ko}} · 기존 저장된 이름은 유지됩니다.</p><details v-if="isAdmin"><summary>한국어 이름 번역 / 수정</summary><p class="error" v-if="error">{{error}}</p><form @submit.prevent="save(false)"><input v-model="name" maxlength="500" required aria-label="한국어 상품명"><button v-if="figure.semantic_name_ko&&figure.semantic_name_ko!==name" type="button" class="button ghost" :disabled="busy" @click="name=figure.semantic_name_ko">새 번역을 입력란에 사용</button><button class="button ghost" :disabled="busy">이름 저장</button><button v-if="!figure.name_ko" type="button" class="button ghost" :disabled="busy" @click="save(true)">AI 번역 (API 사용)</button></form></details></template>

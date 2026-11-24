<script setup>
import {ref} from 'vue'
import {useRouter} from 'vue-router'
import {currentUser,authenticate,signOut} from '../services/accounts'
import {useArchive} from '../stores/archive'
const mode=ref('login'),username=ref(''),password=ref(''),error=ref(''),busy=ref(false)
const router=useRouter(),store=useArchive()
async function submit(){
 busy.value=true;error.value=''
 try{await authenticate(mode.value,{username:username.value,password:password.value});password.value='';await store.loadFavorites();router.push('/favorites')}
 catch(e){error.value=e.message}finally{busy.value=false}
}
async function logout(){busy.value=true;error.value='';try{await signOut();password.value=''}catch(e){error.value=e.message}finally{busy.value=false}}
</script>
<template><section class="section"><p class="eyebrow">MY DOCK</p><h1>{{currentUser?'내 계정':mode==='login'?'로그인':'계정 만들기'}}</h1>
 <p v-if="error" class="error" role="alert">{{error}}</p>
 <template v-if="currentUser"><p>{{currentUser.username}} 님의 관심상품과 구매 기록을 사용 중입니다.</p><div class="button-row"><RouterLink to="/favorites" class="button">관심상품</RouterLink><RouterLink to="/purchases" class="button ghost">구매 기록</RouterLink><button class="button ghost" :disabled="busy" @click="logout">로그아웃</button></div></template>
 <form v-else class="personal-panel" @submit.prevent="submit"><label>사용자 이름<input v-model="username" autocomplete="username" minlength="3" maxlength="40" pattern="[A-Za-z0-9][A-Za-z0-9_.-]{2,39}" required></label><p class="fine-print">영문·숫자·밑줄·마침표·하이픈 3–40자. 대소문자를 구분하지 않습니다.</p><label>비밀번호<input type="password" v-model="password" :autocomplete="mode==='login'?'current-password':'new-password'" minlength="12" maxlength="128" required></label><p class="fine-print">비밀번호는 12–128자입니다. 기존 기록은 데이터 현황에서 관리자로 연결하면 확인할 수 있습니다.</p><div class="button-row"><button class="button" :disabled="busy">{{busy?'처리 중…':mode==='login'?'로그인':'계정 만들기'}}</button><button type="button" class="button ghost" :disabled="busy" @click="mode=mode==='login'?'register':'login';error=''">{{mode==='login'?'계정 만들기':'로그인으로 돌아가기'}}</button></div></form>
</section></template>

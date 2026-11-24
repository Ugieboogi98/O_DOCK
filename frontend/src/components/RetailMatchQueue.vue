<script setup>
import {ref} from 'vue'
import {api,safeUrl} from '../services/api'

const items=ref([]),total=ref(0),page=ref(1),error=ref(''),busy=ref(0),done=ref({})
const size=20
const MEDIUM={game:'게임',anime:'애니메이션',manga:'만화',novel:'소설',vtuber:'버튜버'}
async function load(p=page.value){
 error.value=''
 try{const r=await api(`/admin/retail-matches?page=${p}&size=${size}`);items.value=r.items;total.value=r.total;page.value=r.page}
 catch(e){error.value=e.message}
}
async function confirm(item,candidate){
 busy.value=item.listing_id;error.value=''
 try{
  await api(`/admin/retail-matches/${item.listing_id}`,{method:'POST',body:{variant_id:candidate.variant_id}})
  done.value={...done.value,[item.listing_id]:candidate.name_ko||candidate.name_original}
 }catch(e){error.value=e.message}finally{busy.value=0}
}
const pct=v=>v==null?'':`${Math.round(v*100)}%`
defineExpose({load})
</script>

<template>
 <section class="match-queue">
  <div class="section-title"><h2>국내 판매 매칭 검토</h2><button class="button ghost" @click="load(1)">미연결 목록 불러오기</button></div>
  <p class="fine-print">JAN 자동 연결이 안 된 판매 기록입니다. 판매처 상품명과 판본이 같은지 확인한 뒤 연결하세요. 연결하면 가격 비교와 가격 추이에 반영됩니다.</p>
  <p class="error" v-if="error" role="alert">{{error}}</p>
  <p v-if="total" class="fine-print">미연결 {{total}}건 · {{page}} / {{Math.max(1,Math.ceil(total/size))}} 페이지</p>
  <ol class="match-list">
   <li v-for="item in items" :key="item.listing_id">
    <p class="match-title"><a :href="safeUrl(item.url)" target="_blank" rel="noopener noreferrer">{{item.title}}</a></p>
    <p class="fine-print">{{item.source}} · 제조사 {{item.manufacturer||'미표기'}} · JAN {{item.jan_ean||'없음'}} · {{item.match_evidence?.reason||item.match_status}}</p>
    <p v-if="item.recognized" class="fine-print recognized">작품 <strong>{{item.recognized.work}}</strong><span v-if="item.recognized.medium"> ({{MEDIUM[item.recognized.medium]||item.recognized.medium}})</span><span v-if="item.recognized.characters.length"> · 캐릭터 <strong>{{item.recognized.characters.join(', ')}}</strong></span></p>
    <p v-else class="fine-print">작품을 알아보지 못했습니다 — 사전에 없는 작품일 수 있습니다.</p>
    <p v-if="done[item.listing_id]" class="notice">연결됨: {{done[item.listing_id]}}</p>
    <ul v-else-if="item.candidates.length" class="match-candidates">
     <li v-for="c in item.candidates" :key="c.variant_id">
      <span><strong v-if="c.jan_match">JAN 일치 · </strong><strong v-else-if="c.same_character">같은 캐릭터 · </strong><span v-else-if="c.same_work">같은 작품 · </span>{{c.name_ko||c.name_original}}<small v-if="c.edition"> ({{c.edition}})</small><small v-if="c.similarity"> · 유사도 {{pct(c.similarity)}}</small></span>
      <button class="button ghost" :disabled="busy===item.listing_id" @click="confirm(item,c)">이 상품으로 연결</button>
     </li>
    </ul>
    <p v-else class="fine-print">후보 없음 — 카탈로그에 아직 없는 상품입니다. 해당 제조사가 수집 대상이 아닐 수 있습니다.</p>
   </li>
  </ol>
  <div v-if="total>size" class="match-pages">
   <button class="button ghost" :disabled="page<=1" @click="load(page-1)">이전</button>
   <button class="button ghost" :disabled="page*size>=total" @click="load(page+1)">다음</button>
  </div>
 </section>
</template>

<style scoped>
.match-list{display:grid;gap:14px;margin:12px 0 0;padding:0;list-style:none}
.match-list>li{padding:14px 16px;border:1px solid var(--border);border-radius:10px;background:var(--surface)}
.match-title{margin:0;font-weight:600;word-break:break-word}
.match-candidates{display:grid;gap:8px;margin:10px 0 0;padding:0;list-style:none}
.match-candidates li{display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:8px;font-size:13px}
.match-candidates small{color:var(--muted)}
.match-pages{display:flex;gap:8px;margin-top:12px}
</style>

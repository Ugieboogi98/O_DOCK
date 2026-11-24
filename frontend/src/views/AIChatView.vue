<script setup>
import {ref,computed,watch,onMounted,nextTick} from 'vue';import {useRoute,useRouter} from 'vue-router';import {ArrowUp,BookOpen,Trash2,Search} from 'lucide-vue-next';import {useArchive} from '../stores/archive';import {useChats} from '../stores/chats';import {api} from '../services/api';import SourceList from '../components/SourceList.vue'
import {identityVersion} from '../services/accounts'
const route=useRoute(),router=useRouter(),store=useArchive(),chats=useChats(),figures=ref([]),figure=ref(null),variant=ref(''),q=ref(''),question=ref(''),busy=ref(false),error=ref(''),mode=ref('similarity'),topK=ref(5),chatEnd=ref(null),collecting=ref(false)
const key=computed(()=>`${figure.value?.id}:${variant.value}`),messages=computed(()=>chats.messages(key.value))
async function search(){try{figures.value=(await api('/figures?q='+encodeURIComponent(q.value)+'&page_size=30')).items}catch(e){error.value=e.message}}
onMounted(search)
watch(()=>[route.params.id,route.query.variant],async()=>{error.value='';if(!route.params.id){figure.value=null;return}try{figure.value=await api('/figures/'+route.params.id);variant.value=route.query.variant||figure.value.variants[0]?.id}catch(e){error.value=e.message}},{immediate:true})
watch(identityVersion,()=>{question.value='';error.value=''})
async function send(){
 if(!question.value.trim()||!figure.value||busy.value)return
 const epoch=identityVersion.value
 const text=question.value.trim(),targetKey=key.value
 const history=messages.value.slice(-10).map(m=>({role:m.role,content:m.text}))
 const body={figure_id:figure.value.id,variant_id:Number(variant.value),question:text,history,mode:mode.value,top_k:topK.value}
 question.value='';error.value='';busy.value=true
 chats.add(targetKey,{role:'user',text},epoch)
 try{
  const response=await api('/rag/chat',{method:'POST',body})
  chats.add(targetKey,{role:'assistant',text:response.answer,...response},epoch)
 }catch(e){
  if(epoch===identityVersion.value){
   error.value=e.message
   chats.add(targetKey,{role:'assistant',text:'응답을 받지 못했습니다. 다시 질문해 주세요.',warnings:[e.message]},epoch)
  }
 }finally{
  busy.value=false
  if(epoch===identityVersion.value){await nextTick();chatEnd.value?.scrollIntoView({behavior:'smooth',block:'nearest'})}
 }
}
async function collect(){collecting.value=true;error.value='';try{const r=await api(`/figures/${figure.value.id}/documents/refresh?variant_id=${variant.value}`,{method:'POST',token:store.adminToken,body:{query:question.value||figure.value.name_original}});error.value=r.status==='keys_missing'?'LLM_API_KEY와 SEARCH_API_KEY를 먼저 설정하세요.':`문서 ${r.added}건 추가 및 색인 완료`}catch(e){error.value=e.message}finally{collecting.value=false}}
</script>
<template><section class="page-heading compact"><p class="eyebrow">GROUNDED IN SOURCES</p><h1>AI 리서치</h1><p>제품을 고르고 질문하세요. 답변에 사용한 근거를 함께 보여드립니다.</p></section><div class="chat-layout"><aside class="chat-sidebar"><form class="search-bar" @submit.prevent="search"><input v-model="q" aria-label="질문할 제품 검색" placeholder="제품 찾기"><button aria-label="제품 검색"><Search :size="17"/></button></form><div class="chat-products"><button v-for="f in figures" :key="f.id" @click="router.push('/chat/'+f.id)" :class="{selected:figure?.id===f.id}"><small>{{f.manufacturer}}</small>{{f.name_ko||f.name_original}}</button></div><div class="index-status"><BookOpen :size="16"/><div>메타데이터 {{store.status?.index.metadata??0}}건<br>문서 청크 {{store.status?.index.documents??0}}건</div></div></aside><section class="chat-main"><template v-if="figure"><div class="chat-header"><div><small>{{figure.manufacturer}}</small><h3>{{figure.name_ko||figure.name_original}}</h3></div><button class="icon-button" @click="chats.clear(key)" :disabled="busy" aria-label="현재 제품 대화 삭제"><Trash2 :size="18"/></button></div><div class="chat-controls"><label>버전<select v-model="variant"><option v-for="v in figure.variants" :key="v.id" :value="v.id">{{v.edition||v.variant_key}}</option></select></label><label>검색 방식<select v-model="mode"><option value="similarity">유사도</option><option value="mmr">MMR · 다양성</option></select></label><label>문서 Top-k<input type="number" v-model.number="topK" min="1" max="15"></label></div><div class="notice" v-if="!store.status?.llm_ready">API 키가 없어 정형 데이터 조회 모드입니다. 높이·재질·제조사·스케일·발매일을 질문할 수 있습니다.</div><div class="chat-messages"><div v-if="!messages.length" class="chat-welcome"><BookOpen :size="34"/><h2>무엇이 궁금하세요?</h2><p>확인된 정보에서 답을 찾을게요.</p><button v-for="text in ['이 제품의 높이와 재질은 무엇인가요?','제조사와 스케일을 알려줘','공식 발매가가 확인되나요?']" :key="text" @click="question=text">{{text}} ↗</button></div><article v-for="(m,i) in messages" :key="i" class="message" :class="m.role"><small>{{m.role==='user'?'YOU':'O_DOCK'}}</small><p class="message-text">{{m.text}}</p><SourceList v-if="m.sources?.length" :sources="m.sources"/><small v-if="m.role==='assistant'&&!m.sources?.length">인용된 근거 없음</small><p v-for="w in m.warnings||[]" :key="w" class="message-warning">{{w}}</p><small v-if="m.elapsed_ms">{{m.elapsed_ms}} ms · {{m.mode}}</small></article><p v-if="busy" class="notice" role="status">제품 근거 검색 → 답변 작성 중…</p><div ref="chatEnd"></div></div><p v-if="error" class="notice" role="status">{{error}}</p><form @submit.prevent="send" class="chat-input"><textarea v-model="question" :disabled="busy" maxlength="2000" required placeholder="선택한 제품에 대해 질문하세요" aria-label="질문" @keydown.enter.exact.prevent="send"></textarea><button :disabled="busy||!question.trim()" aria-label="질문 전송"><ArrowUp :size="22"/></button></form><details v-if="store.isAdmin" class="collect-control"><summary>외부 문서 추가 검색 · 관리자</summary><button class="button ghost" @click="collect" :disabled="collecting">{{collecting?'문서 검색·수집·색인 중…':'현재 질문의 외부 문서 수집'}}</button><p class="fine-print">검색·LLM 키와 출처별 수집 권한 설정이 필요합니다. 기존 메타데이터 문서는 항상 유지됩니다.</p></details><p v-if="!store.isAdmin" class="fine-print">외부 문서 수집은 <RouterLink to="/status">관리자 연결</RouterLink> 후 사용할 수 있습니다.</p></template><div v-else class="empty chat-empty"><BookOpen :size="44"/><h2>먼저 제품을 선택하세요.</h2><p>대화는 제품과 버전별로 이 브라우저에 저장됩니다.</p></div></section></div></template>

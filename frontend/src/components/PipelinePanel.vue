<script setup>
import {ref,computed,onMounted,onBeforeUnmount} from 'vue'
import {api,date} from '../services/api'

const run=ref(null),error=ref(''),starting=ref(false)
let timer=0
const STATE={pending:'대기',running:'진행 중',completed:'완료',partial:'일부 완료',skipped:'건너뜀',failed:'실패',not_requested:'선택 안 함',never:'실행 기록 없음',interrupted:'중단됨'}
const REASON={OLLAMA_UNREACHABLE:'Ollama 서버에 연결할 수 없습니다',SEMANTIC_WORKER_RUNNING:'번역 워커가 이미 처리 중입니다',META_NOT_CONFIGURED:'Meta API 설정이 없습니다',
 already_running:'이미 실행 중입니다',no_enabled_catalog_sources:'활성화된 수집 출처가 없습니다',ALREADY_RUNNING_ELSEWHERE:'다른 서버 작업자가 실행 중입니다'}
const LABEL={new_products:'신상품',processed_products:'확인한 상품',checked_pages:'확인한 페이지',failed:'실패',index_pending:'색인 대기',committed:'저장',pending_total:'대기열',
 posts:'게시물',ready:'완성',partial:'일부 분류',review:'검토 필요',not_yet_translated:'번역 대기',semantic_queue:'번역 대기열',event_candidates:'행사 후보'}
const running=computed(()=>run.value?.state==='running')
const facts=s=>Object.entries(s).filter(([k,v])=>LABEL[k]&&typeof v==='number').map(([k,v])=>`${LABEL[k]} ${v}`).join(' · ')
const reason=r=>r?(REASON[r]||REASON[String(r).split(':')[0]]||r):''

async function load(){
 try{run.value=await api('/admin/pipeline');error.value=''}catch(e){error.value=e.message}
 clearTimeout(timer);if(running.value)timer=setTimeout(load,3000)
}
async function start(){
 if(!confirm('신상품 수집 → 번역·분류·검증 → 행사 수집 → 결과 점검을 순서대로 실행합니다. 몇 분에서 수십 분 걸릴 수 있습니다. 시작할까요?'))return
 starting.value=true;error.value=''
 try{run.value=await api('/admin/pipeline/run',{method:'POST',body:{}});if(run.value.reason==='already_running')error.value=REASON.already_running}
 catch(e){error.value=e.message}finally{starting.value=false;load()}
}
onMounted(load);onBeforeUnmount(()=>clearTimeout(timer))
</script>

<template>
 <section class="pipeline">
  <div class="section-title"><h2>데이터 갱신</h2>
   <button class="button" :disabled="running||starting" @click="start">{{running?'실행 중…':starting?'시작하는 중…':'한 번에 실행'}}</button>
  </div>
  <p class="fine-print">관리자 전용입니다. 각 단계는 독립적으로 기록되어 한 단계가 실패해도 나머지는 계속 진행합니다. 행사 기간(진행 중·예정·종료)은 수집한 날짜로 조회할 때마다 다시 계산합니다.</p>
  <p class="error" v-if="error" role="alert">{{error}}</p>
  <template v-if="run">
   <p class="fine-print">상태: <strong>{{STATE[run.state]||run.state}}</strong><span v-if="run.started_at"> · 시작 {{date(run.started_at)}}</span><span v-if="run.finished_at"> · 종료 {{date(run.finished_at)}}</span></p>
   <ol class="steps">
    <li v-for="s in run.steps" :key="s.name" :class="s.state">
     <span class="dot" aria-hidden="true"></span>
     <div><strong>{{s.label}}</strong> <small>{{STATE[s.state]||s.state}}</small>
      <p class="fine-print" v-if="facts(s)">{{facts(s)}}</p>
      <p class="fine-print" v-if="s.reason">{{reason(s.reason)}}</p>
      <p class="fine-print" v-if="s.note">{{s.note}}</p>
     </div>
    </li>
   </ol>
  </template>
 </section>
</template>

<style scoped>
.steps{display:grid;gap:10px;margin:12px 0 0;padding:0;list-style:none}
.steps li{display:flex;gap:12px;align-items:flex-start;padding:12px 14px;border:1px solid var(--border);border-radius:10px;background:var(--surface)}
.steps p{margin:4px 0 0}
.steps small{color:var(--muted)}
.dot{flex:none;width:10px;height:10px;margin-top:6px;border-radius:50%;background:var(--border)}
.running .dot{background:var(--accent,#3b82f6);animation:pulse 1s ease-in-out infinite alternate}
.completed .dot{background:#16a34a}
.partial .dot,.skipped .dot{background:#d97706}
.failed .dot{background:#dc2626}
@keyframes pulse{to{opacity:.35}}
@media (prefers-reduced-motion:reduce){.running .dot{animation:none}}
</style>

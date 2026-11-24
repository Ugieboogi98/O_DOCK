<script setup>
import {computed,ref,watch,onUnmounted,nextTick} from 'vue'
import {Search,SlidersHorizontal,MapPin,CalendarDays,ArrowUpRight,ChevronLeft,ChevronRight,X,RotateCcw} from 'lucide-vue-next'
import {api,safeUrl} from '../services/api'
import EventPoster from '../components/EventPoster.vue'
const q=ref(''),category=ref(''),when=ref(''),area=ref(''),sort=ref('latest'),page=ref(1)
const result=ref({items:[],total:0,options:{areas:[]}}),loading=ref(true),error=ref(''),selected=ref(null)
const closeButton=ref(null)
const types=[['','전체'],['POPUP_STORE','팝업스토어'],['EXHIBITION','전시회'],['COLLAB_CAFE','콜라보 카페'],['FAIR','페어'],['FESTIVAL','페스티벌'],['GOODS_EVENT','팬 이벤트']]
const periods=[['','전체 일정'],['ONGOING','진행 중'],['UPCOMING','오픈 예정'],['ENDED','종료'],['CANCELLED','취소'],['POSTPONED','연기'],['SOLD_OUT','매진'],['UNKNOWN','일정 확인 중']]
const periodLabels=Object.fromEntries(periods),typeLabels=Object.fromEntries(types)
const pages=computed(()=>Math.max(1,Math.ceil(result.value.total/12)))
const activeFilters=computed(()=>[category.value,when.value,area.value,q.value].filter(Boolean).length)
const params=computed(()=>new URLSearchParams({q:q.value,category:category.value,when:when.value,area:area.value,sort:sort.value,page:page.value,size:12}).toString())
let timer=null,request=null,generation=0,previousFocus=null,previousOverflow=''
watch([q,category,when,area,sort],()=>{page.value=1})
watch(params,()=>{
 clearTimeout(timer);request?.abort();const n=++generation;loading.value=true;error.value=''
 timer=setTimeout(async()=>{
  request=new AbortController()
  try{
   const data=await api('/events?'+params.value,{signal:request.signal,token:''})
   if(n===generation)result.value=data
  }catch(e){if(n===generation&&!request.signal.aborted)error.value=e.message}
  finally{if(n===generation)loading.value=false}
 },180)
},{immediate:true})
function reset(){q.value='';category.value='';when.value='';area.value='';sort.value='latest';page.value=1}
async function open(item,event){previousFocus=event.currentTarget;selected.value=item;await nextTick();closeButton.value?.focus()}
function close(){selected.value=null;previousFocus?.focus()}
function keydown(event){if(event.key==='Escape')close();if(event.key==='Tab'&&selected.value){const els=document.querySelectorAll('.event-dialog button,.event-dialog a[href]');const first=els[0],last=els[els.length-1];if(event.shiftKey&&document.activeElement===first){event.preventDefault();last?.focus()}else if(!event.shiftKey&&document.activeElement===last){event.preventDefault();first?.focus()}}}
watch(selected,value=>{if(value){previousOverflow=document.body.style.overflow;document.body.style.overflow='hidden';window.addEventListener('keydown',keydown)}else{document.body.style.overflow=previousOverflow;window.removeEventListener('keydown',keydown)}})
onUnmounted(()=>{clearTimeout(timer);request?.abort();window.removeEventListener('keydown',keydown);if(selected.value)document.body.style.overflow=previousOverflow})
function periodLabel(item){return item.period==='UNKNOWN'&&item.period_text?'\uC77C\uC815 \uC548\uB0B4':periodLabels[item.period]||'\uC77C\uC815 \uD655\uC778 \uC911'}
function displayDate(value){return value?value.replaceAll('-','.'):null}
function checkedAt(value){return value?new Intl.DateTimeFormat('ko-KR',{timeZone:'Asia/Seoul',month:'long',day:'numeric',hour:'2-digit',minute:'2-digit'}).format(new Date(value)):''}
function location(item){return item.venue||item.venues?.join(' · ')||'장소 확인 중'}
function range(item){if(item.periods?.length>1)return item.periods.map(p=>`${displayDate(p.start_date)} — ${displayDate(p.end_date)}`).join(' / ');return item.start_date&&item.end_date?`${displayDate(item.start_date)} — ${displayDate(item.end_date)}`:item.period_text|| (item.start_date?`${displayDate(item.start_date)} — 종료일 확인 중`:'기간 확인 중')}
</script>
<template>
 <div class="events-page">
  <header class="events-intro"><div><p class="events-eyebrow">GO BEYOND THE COLLECTION</p><h1>좋아하는 세계를<br class="events-mobile-break"> 직접 만나는 시간<span>.</span></h1><p class="events-subtitle">팝업스토어부터 전시, 콜라보 카페까지.<br>마음에 드는 작품의 다음 만남을 찾아보세요.</p></div><div class="events-intro-mark" aria-hidden="true"><span>O_DOCK</span><strong>OUT<br>OF THE<br>BOX <ArrowUpRight :size="30"/></strong></div></header>
  <div class="events-mode"><span><i></i>서브컬처 행사 아카이브</span><span>공식 공지에서 만나는 새로운 소식</span></div>
  <div class="events-toolbar"><div class="events-type-tabs" role="group" aria-label="행사 유형"><button v-for="[value,label] in types" :key="value" :class="{active:category===value}" :aria-pressed="category===value" @click="category=value">{{label}}</button></div><div class="events-search"><Search :size="17"/><input v-model="q" aria-label="행사 또는 작품 검색" placeholder="작품명, 행사명으로 찾아보세요"><button v-if="q" @click="q=''" aria-label="검색 지우기"><X :size="15"/></button></div></div>
  <div class="events-layout"><aside class="events-filters"><div class="events-filter-heading"><strong><SlidersHorizontal :size="16"/>필터<span v-if="activeFilters">{{activeFilters}}</span></strong><button @click="reset" aria-label="필터 초기화"><RotateCcw :size="14"/>초기화</button></div><fieldset><legend><CalendarDays :size="15"/>일정</legend><label v-for="[value,label] in periods" :key="value"><input type="radio" v-model="when" :value="value" name="event-period">{{label}}</label></fieldset><fieldset><legend><MapPin :size="15"/>장소</legend><select v-model="area" aria-label="행사 장소"><option value="">전체 장소</option><option v-for="place in result.options?.areas||[]" :key="place" :value="place">{{place}}</option></select><p>공식 공지에서 확인한 장소를 기준으로 표시해요.</p></fieldset><div class="events-filter-tip">취향에 맞는 다음 외출.<br><strong>O_DOCK과 함께 찾아요.</strong><ArrowUpRight :size="22"/></div></aside>
   <section class="events-results" aria-label="행사 목록"><div class="events-result-heading"><h2>발견한 행사 <span>{{result.total}}</span></h2><select v-model="sort" aria-label="행사 정렬"><option value="latest">최근 공지순</option><option value="opening">오픈일순</option><option value="ending">종료일순</option></select></div>
    <p v-if="error" class="error" role="alert">{{error}}</p><p v-if="loading" class="events-loading" role="status">행사 정보를 확인하고 있어요…</p>
    <div v-else-if="!result.items.length" class="events-empty"><CalendarDays :size="42" :stroke-width="1"/><h3>{{activeFilters?'조건에 맞는 행사가 없어요':'새로운 만남을 준비하고 있어요'}}</h3><p>필터를 바꾸거나 다음 행사 소식을 확인해 주세요.</p><button v-if="activeFilters" class="button ghost" @click="reset">필터 초기화</button></div>
    <div v-else class="events-grid"><button v-for="item in result.items" :key="item.id" class="event-card" @click="open(item,$event)"><div class="event-card-art"><EventPoster :src="item.images?.[0]" :alt="item.title"/><span class="event-period-pill" :class="item.period.toLowerCase()">{{periodLabel(item)}}</span><span class="event-card-arrow"><ArrowUpRight :size="18"/></span></div><div class="event-card-copy"><p class="event-card-type">{{item.categories.map(v=>typeLabels[v]||v).join(' · ')||'서브컬처 행사'}}</p><h3>{{item.title}}</h3><p class="event-card-dates"><CalendarDays :size="13"/>{{range(item)}}</p><p class="event-card-place"><MapPin :size="13"/>{{location(item)}}</p><div class="event-card-bottom"><span>{{item.franchises.slice(0,2).join(' · ')||'IP 확인 중'}}</span><small v-if="item.sources.length>1">공지 {{item.sources.length}}건</small></div></div></button></div>
    <nav v-if="pages>1&&!loading" class="events-pagination" aria-label="행사 페이지"><button @click="page--" :disabled="page<=1" aria-label="이전 페이지"><ChevronLeft :size="17"/></button><span>{{page}} / {{pages}}</span><button @click="page++" :disabled="page>=pages" aria-label="다음 페이지"><ChevronRight :size="17"/></button></nav>
   </section>
  </div>
  <div v-if="selected" class="event-dialog-backdrop" @click.self="close"><section class="event-dialog" role="dialog" aria-modal="true" aria-labelledby="event-dialog-title"><button ref="closeButton" class="event-dialog-close" @click="close" aria-label="상세 닫기"><X :size="22"/></button><p class="events-eyebrow">EVENT DETAILS</p><h2 id="event-dialog-title">{{selected.title}}</h2><p class="event-dialog-status">{{periodLabel(selected)}}</p><dl><div><dt>작품</dt><dd>{{selected.franchises.join(' · ')||'확인 중'}}</dd></div><div><dt>기간</dt><dd>{{range(selected)}}</dd></div><div><dt>장소</dt><dd>{{location(selected)}}</dd></div></dl><p v-if="selected.year_inferred" class="fine-print">연도는 게시일과 원문 요일을 기준으로 보완했습니다.</p><p class="events-private-note">공식 공지를 바탕으로 수집한 정보입니다. 방문 전 일정·장소를 원문에서 확인해 주세요.</p><p v-if="selected.booking_url"><a :href="safeUrl(selected.booking_url)" target="_blank" rel="noopener noreferrer" class="text-link">예약·예매 안내 <ArrowUpRight :size="14"/></a></p><div class="event-dialog-gallery" v-if="selected.images?.length"><EventPoster v-for="src in selected.images" :key="src" :src="src" :alt="selected.title"/></div><article v-for="(source,index) in selected.sources" :key="index" class="event-source"><h3>공식 공지 · {{source.platform==='website'?source.username:'@'+source.username}}</h3><p v-if="source.last_checked_at">확인 {{checkedAt(source.last_checked_at)}}</p><p v-if="source.caption" class="preserve-lines">{{source.caption}}</p><a :href="safeUrl(source.url)" target="_blank" rel="noopener noreferrer" class="text-link">공식 원문 확인 <ArrowUpRight :size="14"/></a></article></section></div>
 </div>
</template>

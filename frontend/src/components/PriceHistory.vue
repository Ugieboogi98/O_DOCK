<script setup>
import {computed,ref,watch} from 'vue'
import {api} from '../services/api'

const props=defineProps({figureId:[Number,String],variantId:[Number,String]})
const data=ref(null),error=ref(''),loading=ref(false)
const names={maniahouse:'매니아하우스',herotime:'히어로타임',figurefarm:'피규어팜',comics_art:'코믹스아트'}
// Distinct hues that hold up on light and dark surfaces.
const colors={maniahouse:'#2f7fd8',herotime:'#d4553d',figurefarm:'#2f9e6a',comics_art:'#8a5cd6'}

async function load(){
 if(!props.figureId)return
 loading.value=true;error.value=''
 try{
  const q=props.variantId?`&variant_id=${encodeURIComponent(props.variantId)}`:''
  data.value=await api(`/figures/${encodeURIComponent(props.figureId)}/price-history?days=180${q}`)
 }catch(e){error.value=e.message}finally{loading.value=false}
}
watch(()=>[props.figureId,props.variantId],load,{immediate:true})

const W=320,H=120,P=8
const series=computed(()=>(data.value?.series||[]).map(s=>({...s,points:s.points.filter(p=>p.sale_price)})).filter(s=>s.points.length))
const domain=computed(()=>{
 const pts=series.value.flatMap(s=>s.points)
 if(!pts.length)return null
 const t=pts.map(p=>+new Date(p.observed_at)),v=pts.map(p=>p.sale_price)
 const tMin=Math.min(...t),tMax=Math.max(...t),vMin=Math.min(...v),vMax=Math.max(...v)
 return {tMin,tSpan:Math.max(1,tMax-tMin),vMin,vSpan:Math.max(1,vMax-vMin)}
})
const x=p=>P+(+new Date(p.observed_at)-domain.value.tMin)/domain.value.tSpan*(W-2*P)
const y=p=>H-P-(p.sale_price-domain.value.vMin)/domain.value.vSpan*(H-2*P)
const path=s=>s.points.map((p,i)=>`${i?'L':'M'}${x(p).toFixed(1)},${y(p).toFixed(1)}`).join(' ')
const won=v=>`${new Intl.NumberFormat('ko-KR').format(v)}원`
const day=v=>new Intl.DateTimeFormat('ko-KR',{month:'numeric',day:'numeric'}).format(new Date(v))
const summary=s=>{const a=s.points[0],b=s.points[s.points.length-1];return {first:a,last:b,delta:b.sale_price-a.sale_price}}
</script>

<template>
 <section class="price-history" aria-label="국내 가격 추이">
  <h3>가격 추이 <small>최근 180일 · 국내 유통사 관측가</small></h3>
  <p v-if="loading" class="ph-muted">불러오는 중…</p>
  <p v-else-if="error" class="ph-muted" role="alert">{{error}}</p>
  <p v-else-if="!series.length" class="ph-muted">연결된 판매 기록의 가격 이력이 아직 없습니다.</p>
  <template v-else>
   <svg :viewBox="`0 0 ${W} ${H}`" role="img" :aria-label="`최저 관측가 ${won(data.lowest_observed)}`" preserveAspectRatio="none">
    <path v-for="s in series" :key="s.listing_id" :d="path(s)" :stroke="colors[s.source]||'currentColor'" fill="none" stroke-width="2" vector-effect="non-scaling-stroke"/>
    <template v-for="s in series" :key="'p'+s.listing_id">
     <circle v-for="p in s.points" :key="p.observed_at" :cx="x(p)" :cy="y(p)" r="2.5" :fill="colors[s.source]||'currentColor'"><title>{{names[s.source]||s.retailer}} · {{day(p.observed_at)}} · {{won(p.sale_price)}}</title></circle>
    </template>
   </svg>
   <ul class="ph-legend">
    <li v-for="s in series" :key="'l'+s.listing_id">
     <i :style="{background:colors[s.source]||'currentColor'}"></i>{{names[s.source]||s.retailer}}
     <span>{{won(summary(s).last.sale_price)}}</span>
     <em v-if="summary(s).delta" :class="summary(s).delta<0?'down':'up'">{{summary(s).delta<0?'▼':'▲'}} {{won(Math.abs(summary(s).delta))}}</em>
     <small>{{day(summary(s).first.observed_at)}}~{{day(summary(s).last.observed_at)}}</small>
    </li>
   </ul>
   <p class="ph-muted">기간 중 최저 관측가 <strong>{{won(data.lowest_observed)}}</strong> · 배송비 제외</p>
  </template>
 </section>
</template>

<style scoped>
.price-history{margin:0 0 26px;padding:18px 22px;border:1px solid var(--border);border-radius:12px;background:var(--surface)}
h3{margin:0 0 12px;font-size:14px;font-weight:600;color:var(--ink)}
h3 small{margin-left:6px;font-size:11px;font-weight:400;color:var(--muted)}
svg{display:block;width:100%;height:120px;overflow:visible}
.ph-legend{display:grid;gap:6px;margin:12px 0 0;padding:0;list-style:none;font-size:12px;color:var(--ink)}
.ph-legend li{display:flex;flex-wrap:wrap;align-items:center;gap:8px}
.ph-legend i{width:10px;height:10px;border-radius:50%;flex:none}
.ph-legend span{font-weight:600;font-variant-numeric:tabular-nums}
.ph-legend em{font-style:normal;font-size:11px}
.ph-legend em.down{color:#2f9e6a}.ph-legend em.up{color:#d4553d}
.ph-legend small{color:var(--muted);font-size:10px}
.ph-muted{margin:8px 0 0;font-size:11px;color:var(--muted)}
.ph-muted strong{color:var(--ink)}
@media(max-width:480px){.price-history{padding:16px}}
</style>

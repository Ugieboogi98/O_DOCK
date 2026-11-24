<script setup>
import {computed} from 'vue'
import {ArrowUpRight} from 'lucide-vue-next'
import {safeUrl} from '../services/api'

const props=defineProps({comparison:Object,loading:Boolean,error:String})
const emit=defineEmits(['retry'])
const retailers=[
  ['maniahouse','매니아하우스'],['herotime','히어로타임'],
  ['figurefarm','피규어팜'],['comics_art','코믹스아트']
]
const rows=computed(()=>retailers.map(([code,name])=>({
  code,name,...props.comparison?.retailers?.find(row=>row.code===code)
})))
const lowest=computed(()=>props.comparison?.lowest_price)
const winners=computed(()=>rows.value.filter(row=>row.is_lowest).map(row=>row.name).join(' · '))
const price=value=>`${new Intl.NumberFormat('ko-KR').format(value)}원`
const checked=value=>value?new Intl.DateTimeFormat('ko-KR',{month:'numeric',day:'numeric',hour:'2-digit',minute:'2-digit'}).format(new Date(value)):''
const states={IN_STOCK:'판매 중',PREORDER:'예약 판매',SOLD_OUT:'품절',COMING_SOON:'판매 예정',UNKNOWN:'판매 상태 미확인'}
</script>

<template>
 <section class="domestic-prices" aria-label="국내 유통사 가격 비교" :aria-busy="loading">
  <div class="domestic-main-price" aria-live="polite">
   <span class="domestic-price-label">국내 유통 최저가</span>
   <strong v-if="loading" class="domestic-price-pending">가격 확인 중…</strong>
   <strong v-else-if="error" class="domestic-price-pending">가격 조회 실패</strong>
   <strong v-else :class="{'domestic-price-pending':lowest==null}">{{lowest!=null?price(lowest):'가격 없음'}}</strong>
   <p v-if="!loading&&!error&&lowest!=null">{{winners}}<span>배송비 제외</span></p>
  </div>
  <p v-if="error&&!loading" class="domestic-price-error" role="alert">{{error}} <button @click="emit('retry')">다시 확인</button></p>
  <table class="domestic-price-table">
   <caption class="domestic-visually-hidden">유통사별 가격</caption>
   <thead><tr><th scope="col">유통사</th><th scope="col">가격</th></tr></thead>
   <tbody>
    <tr v-for="row in rows" :key="row.code" :class="{'domestic-price-lowest':row.is_lowest&&!loading&&!error}">
     <th scope="row">{{row.name}}<span v-if="row.is_lowest&&!loading&&!error" class="domestic-lowest-label">최저가</span></th>
     <td>
      <span v-if="loading" class="domestic-price-missing">확인 중</span>
      <span v-else-if="error" class="domestic-price-missing">조회 실패</span>
      <template v-else-if="row.price!=null">
       <a :href="safeUrl(row.product_url)" target="_blank" rel="noopener noreferrer">{{price(row.price)}}<ArrowUpRight :size="13"/></a>
       <small>{{row.stale?'이전 확인가':states[row.availability]}}<span v-if="row.observed_at"> · {{checked(row.observed_at)}} 확인</span></small>
      </template>
      <span v-else class="domestic-price-missing">가격 없음</span>
     </td>
    </tr>
   </tbody>
  </table>
 </section>
</template>

<style scoped>
.domestic-prices{margin:22px 0 26px;border:1px solid var(--border);border-radius:12px;overflow:hidden;background:var(--surface)}
.domestic-main-price{padding:22px 24px;background:var(--surface);border-bottom:1px solid var(--border)}
.domestic-price-label{display:block;font-size:12px;font-weight:600;color:var(--muted)}
.domestic-main-price>strong{display:block;margin:7px 0 0;font-size:36px;line-height:1.3;font-weight:500;letter-spacing:-.04em;color:var(--accent-ink);font-variant-numeric:tabular-nums}
.domestic-main-price>strong.domestic-price-pending{font-size:26px;color:var(--ink)}
.domestic-main-price p{display:flex;flex-wrap:wrap;gap:10px;margin:8px 0 0;font-size:11px;color:var(--muted)}
.domestic-main-price p span{color:var(--ink)}
.domestic-price-table{width:100%;border-collapse:collapse;font-size:12px}
.domestic-price-table thead th{padding:10px 18px;font-size:10px;color:var(--ink);font-weight:500;border-bottom:1px solid var(--border)}
.domestic-price-table th{text-align:left}
.domestic-price-table th:first-child{padding-left:24px}
.domestic-price-table td,.domestic-price-table thead th:last-child{text-align:right;padding-right:24px}
.domestic-price-table tbody th,.domestic-price-table td{padding-top:14px;padding-bottom:14px;border-bottom:1px solid var(--border)}
.domestic-price-table tbody tr:last-child th,.domestic-price-table tbody tr:last-child td{border-bottom:0}
.domestic-price-table tbody th{font-weight:550;color:var(--ink);white-space:nowrap}
.domestic-price-table td a{display:inline-flex;align-items:center;gap:5px;font-size:14px;font-weight:600;font-variant-numeric:tabular-nums}
.domestic-price-table small{display:block;margin-top:4px;font-size:9px;font-weight:400;color:var(--ink)}
.domestic-price-missing{font-size:12px;color:var(--ink);font-weight:400}
.domestic-price-lowest{background:var(--surface)}
.domestic-price-lowest td a{color:var(--accent-ink)}
.domestic-lowest-label{display:inline-block;margin-left:7px;font-size:9px;color:var(--muted);font-weight:600}
.domestic-price-error{padding:12px 24px;margin:0;font-size:11px;color:var(--muted);border-bottom:1px solid var(--border)}
.domestic-price-error button{text-decoration:underline;color:inherit}
.domestic-visually-hidden{position:absolute;width:1px;height:1px;overflow:hidden;clip-path:inset(50%);white-space:nowrap}
@media(max-width:480px){.domestic-main-price{padding:20px}.domestic-main-price>strong{font-size:32px}.domestic-price-table th:first-child{padding-left:16px}.domestic-price-table td,.domestic-price-table thead th:last-child{padding-right:16px}.domestic-lowest-label{display:block;margin:3px 0 0}}
</style>

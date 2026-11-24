<script setup>
import {computed,ref,watch} from 'vue'
import {useRoute} from 'vue-router'
import {ArrowUpRight,ArrowDown,Boxes,MessageSquare,Plus,Check,ChevronLeft,ChevronRight} from 'lucide-vue-next'
import {api,money,date,safeUrl,safeImage} from '../services/api'
import {useArchive} from '../stores/archive'
import SourceList from '../components/SourceList.vue'
import FavoriteButton from '../components/FavoriteButton.vue'
import LocalPrices from '../components/LocalPrices.vue'
import DomesticPrices from '../components/DomesticPrices.vue'
import KoreanName from '../components/KoreanName.vue'
import {semanticValue,semanticNotice} from '../services/semantics'
const route=useRoute(),store=useArchive()
const figure=ref(null),prices=ref(null),localPrice=ref(null),sources=ref([]),variant=ref('')
const error=ref(''),loading=ref(false),priceError=ref(''),translationInfo=ref(null),translationError=ref('')
const priceLoading=ref(false)
const description=ref({body:''}),selectedImage=ref(0),imageFailed=ref(false)
let pageGeneration=0,detailGeneration=0
const activeVariant=computed(()=>figure.value?.variants.find(v=>String(v.id)===String(variant.value)))
const images=computed(()=>figure.value?.images||[])
const officialPrice=computed(()=>{
 const yen=(prices.value?.release_prices||[]).filter(p=>p.currency==='JPY')
 return yen.find(p=>p.price_kind==='official_list')||yen.find(p=>p.price_kind==='official_release')||localPrice.value?.japan||null
})
const wonEstimate=computed(()=>officialPrice.value&&localPrice.value?.rate?Math.round(Number(officialPrice.value.price_amount)*Number(localPrice.value.rate.rate)):null)
const franchise=computed(()=>figure.value?semanticValue(figure.value,'franchise_ko',translationInfo.value?.profile?.franchise_ko||figure.value.franchise):null)
const character=computed(()=>figure.value?semanticValue(figure.value,'character_ko',translationInfo.value?.profile?.character_ko||figure.value.character):null)
const formLabel=computed(()=>{
 if(!figure.value)return null
 const f=figure.value,lookup=/るかっぷ|look\s?up|룩업/i
 return lookup.test(`${f.product_line||''} ${f.name_original}`)||(f.figure_form==='chibi_figure'&&lookup.test(description.value.body||''))?'룩업 · 데포르메 피규어':f.figure_form_ko
})
const specs=computed(()=>[
 ['작품명',franchise.value],['캐릭터명',character.value],['피규어 형태',formLabel.value],['발매일',activeVariant.value?.release_date],
 ['크기',[figure.value?.scale?`${figure.value.scale} 스케일`:null,figure.value?.height_mm?`높이 ${figure.value.height_mm} mm`:null].filter(Boolean).join(' · ')],
 ['제조사',figure.value?.manufacturer_ko||figure.value?.manufacturer]
])
const translatedDocuments=computed(()=>(translationInfo.value?.documents||[]).filter(d=>String(d.variant_id)===String(variant.value)&&d.body_ko))
function selectImage(index){selectedImage.value=index;imageFailed.value=false}
function stepImage(delta){if(images.value.length)selectImage((selectedImage.value+delta+images.value.length)%images.value.length)}
async function details(){
 if(!figure.value||!variant.value)return
 const generation=++detailGeneration,id=figure.value.id,v=variant.value
 prices.value=null;localPrice.value=null;sources.value=[];description.value={body:''};priceError.value='';priceLoading.value=true
 const results=await Promise.allSettled([api(`/figures/${id}/prices?variant_id=${v}`),api(`/figures/${id}/sources?variant_id=${v}`),api(`/figures/${id}/description?variant_id=${v}`),api(`/figures/${id}/local-prices?variant_id=${v}`)])
 if(generation!==detailGeneration||id!==figure.value?.id)return
 priceLoading.value=false
 if(results[0].status==='fulfilled')prices.value=results[0].value
 else priceError.value='가격 정보를 불러오지 못했습니다. 잠시 후 다시 시도해 주세요.'
 if(results[1].status==='fulfilled')sources.value=results[1].value
 if(results[2].status==='fulfilled')description.value=results[2].value
 if(results[3].status==='fulfilled')localPrice.value=results[3].value
}
watch(()=>route.params.id,async id=>{
 const generation=++pageGeneration;++detailGeneration
 loading.value=true;error.value='';figure.value=null;translationInfo.value=null;translationError.value='';selectImage(0)
 try{
  const value=await api('/figures/'+id)
  if(generation!==pageGeneration)return
  figure.value=value;variant.value=value.variants[0]?.id||''
  await details()
  try{const value=await api('/figures/'+id+'/korean');if(generation===pageGeneration)translationInfo.value=value}
  catch{if(generation===pageGeneration)translationError.value='한국어 설명을 불러오지 못했습니다.'}
 }catch(e){if(generation===pageGeneration)error.value=e.message}
 finally{if(generation===pageGeneration)loading.value=false}
},{immediate:true})
watch(variant,(value,old)=>{if(old&&value!==old)details()})
</script>
<template>
 <div class="product-detail-page">
  <p class="breadcrumb"><RouterLink to="/">홈</RouterLink><span>/</span><RouterLink to="/figures">전체 상품</RouterLink><span>/</span>상품 상세</p>
  <p v-if="loading" class="empty" role="status">상품을 불러오고 있습니다…</p><p v-if="error" class="error" role="alert">{{error}}</p>
  <template v-if="figure&&!loading">
   <section class="product-overview" aria-label="상품 정보">
    <div class="product-visual">
     <div class="product-main-image" @keydown.left.prevent="stepImage(-1)" @keydown.right.prevent="stepImage(1)" tabindex="0" aria-label="상품 사진. 좌우 화살표로 사진 변경">
      
      <img v-if="images.length&&!imageFailed" :src="safeImage(images[selectedImage]?.image_url)" :alt="`${figure.name_ko||figure.name_original} 상품 사진 ${selectedImage+1}`" @error="imageFailed=true" fetchpriority="high">
      <div v-else class="product-image-empty"><Boxes :size="64" :stroke-width="1"/><p>{{images.length?'이미지를 불러오지 못했습니다.':'등록된 상품 이미지가 없습니다.'}}</p><button v-if="imageFailed" class="text-link" @click="imageFailed=false">다시 불러오기</button></div>
      <div class="product-image-pager" v-if="images.length"><button v-if="images.length>1" @click="stepImage(-1)" aria-label="이전 사진"><ChevronLeft :size="17"/></button><span>{{String(selectedImage+1).padStart(2,'0')}} <i>/</i> {{String(images.length).padStart(2,'0')}}</span><button v-if="images.length>1" @click="stepImage(1)" aria-label="다음 사진"><ChevronRight :size="17"/></button></div>
     </div>
     <div class="product-thumbnails" v-if="images.length>1" aria-label="상품 사진 선택"><button v-for="(img,i) in images" :key="img.id" @click="selectImage(i)" :aria-label="`상품 사진 ${i+1} 선택`" :aria-pressed="selectedImage===i"><img :src="safeImage(img.image_url)" alt="" loading="lazy"></button></div>
     <a v-if="images.length" class="product-all-images" href="#product-gallery">상품 사진 전체 보기 <ArrowDown :size="15"/></a>
    </div>
    <div class="product-summary">
     <p class="product-maker">{{figure.manufacturer_ko||figure.manufacturer}}<span>{{figure.manufacturer}}</span></p>
     <p class="product-line" v-if="figure.product_line">{{figure.product_line}}</p>
     <h1>{{figure.name_ko||figure.name_original}}</h1><p class="product-original" v-if="figure.name_ko">{{figure.name_original}}</p>
     <label class="product-variant" v-if="figure.variants.length>1">상품 버전<select v-model="variant"><option v-for="v in figure.variants" :key="v.id" :value="v.id">{{v.edition||v.variant_key}} {{v.release_date||''}}</option></select></label>
     <DomesticPrices :comparison="prices?.domestic_comparison" :loading="priceLoading" :error="priceError" @retry="details"/>
     <div class="product-primary-actions"><FavoriteButton :figure="figure" labeled/><RouterLink :to="`/purchases?figure=${figure.id}&variant=${variant}`" class="button"><Check :size="18"/>구매 완료 등록</RouterLink></div>
     <div class="product-price-box">
      <div class="product-price-label"><span>일본 공식 표시가</span><a v-if="officialPrice?.source_url" :href="safeUrl(officialPrice.source_url)" target="_blank" rel="noopener noreferrer">출처 <ArrowUpRight :size="13"/></a></div>
      <strong class="product-yen">{{officialPrice?money(officialPrice.price_amount,'JPY'):'등록된 가격 없음'}}</strong>
      <p class="product-price-caption">{{officialPrice?.price_kind==='official_release'?'공식 발매가로 확인된 금액입니다.':'공식 목록에 표시된 가격을 기준으로 합니다.'}}</p>
      <div class="product-converted"><span>환율 환산 참고가</span><strong>{{wonEstimate!==null?money(wonEstimate,'KRW'):'환산 정보 미확인'}}</strong></div>
      <p class="product-rate" v-if="localPrice?.rate">1 JPY = {{Number(localPrice.rate.rate).toFixed(2)}} KRW · {{localPrice.rate.rate_date}} 기준</p>
      <p class="product-price-note">배송비·관부가세·카드 수수료가 포함되지 않은 참고 금액입니다.</p><p v-if="priceError" class="error" role="status">{{priceError}}</p>
     </div>
     <div class="product-market-prices"><div><span>국내 공식 판매가</span><strong>{{localPrice?.korea?money(localPrice.korea.price_amount,'KRW'):'수집 예정'}}</strong><small>{{localPrice?.korea?'등록된 공식 판매처 기준':'가격 수집 후 제공됩니다'}}</small></div><div><span>중고 시세</span><strong>연동 예정</strong><small>확인된 매물 기준으로 제공 예정</small></div></div>
     <div class="product-secondary-actions"><a :href="safeUrl(figure.official_url)" target="_blank" rel="noopener noreferrer">공식 상품 페이지 <ArrowUpRight :size="15"/></a><button @click="store.toggle(figure.id)"><Plus :size="16"/>상품 비교</button><RouterLink :to="`/chat/${figure.id}?variant=${variant}`"><MessageSquare :size="15"/>AI에게 질문</RouterLink></div>
    </div>
   </section>
   <section class="product-specifications" aria-labelledby="spec-heading">
    <div class="product-section-heading"><div><p>THE DETAILS</p><h2 id="spec-heading">상품 정보</h2></div><span>공식 자료를 바탕으로 정리했어요</span></div>
    <dl class="product-spec-grid"><div v-for="[label,value] in specs" :key="label"><dt>{{label}}</dt><dd>{{value||'확인 중'}}</dd></div></dl>
    <p v-if="semanticNotice(figure)" class="product-data-note">{{semanticNotice(figure)}}</p>
    <details class="product-extra-specs"><summary>제품 라인 · 재질 · 제품 번호 더 보기</summary><dl><div v-for="[label,value] in [['제품 라인',figure.product_line],['재질',figure.material],['SKU',activeVariant?.sku]]" :key="label"><dt>{{label}}</dt><dd>{{value||'확인 중'}}</dd></div></dl><KoreanName :key="figure.id" :figure="figure" @saved="v=>figure.name_ko=v"/></details>
   </section>
   <section id="product-gallery" class="product-gallery" v-if="images.length" aria-labelledby="gallery-heading"><div class="product-section-heading"><div><p>A CLOSER LOOK</p><h2 id="gallery-heading">사진으로 더 자세히</h2></div><span>총 {{images.length}}장의 상품 이미지</span></div><div class="product-gallery-images"><figure v-for="(img,i) in images" :key="img.id"><img :src="safeImage(img.image_url)" :alt="`${figure.name_ko||figure.name_original} 상세 사진 ${i+1}`" loading="lazy" decoding="async"><figcaption>{{String(i+1).padStart(2,'0')}} / {{String(images.length).padStart(2,'0')}}</figcaption></figure></div></section>
   <section class="product-editorial" v-if="translatedDocuments.length||description.body||translationError"><div class="product-section-heading"><div><p>ABOUT THIS FIGURE</p><h2>상품 이야기</h2></div></div><p v-if="translationError" class="error">{{translationError}}</p><article v-for="doc in translatedDocuments" :key="doc.id"><p v-if="!doc.complete" class="notice">설명 번역 진행 중 · {{doc.parts_ready}} / {{doc.parts_total}}</p><p class="preserve-lines">{{doc.body_ko}}</p><a :href="safeUrl(doc.url)" target="_blank" rel="noopener noreferrer" class="text-link">원문 확인 <ArrowUpRight :size="14"/></a></article><details v-if="description.body"><summary>공식 상품 설명 원문 보기</summary><p class="preserve-lines">{{description.body}}</p></details></section>
   <section class="product-service-info"><div><span class="product-service-mark">O_DOCK</span><h2>좋아하는 피규어를,<br>더 잘 알아가는 곳.</h2><p>관심 있는 상품을 모으고, 구매한 피규어를 기록하세요.<br>가격과 상품 정보는 확인된 출처와 함께 제공합니다.</p></div><div class="product-service-links"><RouterLink :to="`/prices/${figure.id}?variant=${variant}`">가격 비교 자세히 보기 <ArrowUpRight :size="16"/></RouterLink><details><summary>가격 정보와 환산 기준</summary><LocalPrices :figure="figure" :variant="variant"/></details><details><summary>상품 정보 출처 {{sources.length}}건</summary><SourceList :sources="sources"/><p class="fine-print">수집일 {{date(figure.collected_at)}}</p></details></div></section>
  </template>
 </div>
</template>

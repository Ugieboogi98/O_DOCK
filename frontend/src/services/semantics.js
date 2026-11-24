// A field decision also overrides older translations when the value is withheld.
export function semanticValue(figure, field, legacy=null) {
 if(figure.semantic_field_status?.[field]==='not_applicable') return '해당 없음'
 if (Object.hasOwn(figure.semantic_field_status||{},field)) return figure[field]||null
 return figure[field]||legacy||null
}

const labels={name_ko:'상품명',franchise_ko:'작품',character_ko:'캐릭터',figure_form:'피규어 형태'}
export function semanticNotice(figure) {
 const held=Object.entries(figure.semantic_field_status||{})
  .filter(([,state])=>state==='review').map(([field])=>labels[field]||field)
 if(held.length) return `${held.join('·')} 정보는 검토 중입니다. 확인된 항목만 표시합니다.`
 const states=figure.semantic_field_status||{}
 if(Object.keys(states).length&&!['franchise_ko','character_ko','figure_form'].some(k=>['missing','review','partial'].includes(states[k]))) return ''
 return figure.semantic_status==='partial'?'일부 작품·캐릭터·형태 정보는 아직 미확인입니다.':''
}

import {describe,it,expect} from 'vitest'
import {semanticValue,semanticNotice} from './semantics'

describe('field publication',()=>{
 it('distinguishes confirmed inapplicability from unknown classifications',()=>{
  const f={semantic_status:'partial',semantic_field_status:{name_ko:'missing',franchise_ko:'not_applicable',character_ko:'ready',figure_form:'ready'}}
  expect(semanticValue(f,'franchise_ko','예전 작품')).toBe('해당 없음')
  expect(semanticNotice(f)).toBe('')
 })
 it('does not replace a withheld field with an older translation',()=>{
  const f={semantic_field_status:{franchise_ko:'review'},franchise_ko:null}
  expect(semanticValue(f,'franchise_ko','예전 오역')).toBeNull()
  expect(semanticNotice(f)).toContain('작품 정보는 검토 중')
 })
 it('keeps validated values and supports catalogs without semantic records',()=>{
  expect(semanticValue({character_ko:'페른',semantic_field_status:{character_ko:'ready'}},'character_ko','펀')).toBe('페른')
  expect(semanticValue({},'character_ko','기존 이름')).toBe('기존 이름')
  expect(semanticNotice({semantic_status:'partial'})).toContain('미확인')
  expect(semanticNotice({semantic_status:'ready'})).toBe('')
 })
})

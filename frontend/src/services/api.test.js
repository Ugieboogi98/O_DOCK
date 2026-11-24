import {describe,it,expect} from 'vitest'
import {safeUrl,money} from './api'
describe('source safety and price display',()=>{
 it('rejects script and data URLs',()=>{expect(safeUrl('javascript:alert(1)')).toBe('#');expect(safeUrl('data:text/html,x')).toBe('#')})
 it('preserves unknown values and original currencies',()=>{expect(money(null)).toBe('미확인');expect(money(100,'JPY')).not.toBe(money(100,'KRW'))})
})

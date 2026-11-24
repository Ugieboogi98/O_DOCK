from app.services.local_semantic_lexicon import hints, normalize_result


def entity(original, ko):
    return {'original': original, 'ko': ko, 'evidence_field': 'name_original', 'evidence': original, 'confidence': 1}


def test_bleach_alias_repairs_kanji_title_without_changing_code():
    source = {'name_original': 'BLEACH 黒崎一護 1/7 フィギュア Z50J'}
    raw = {'name_ko': '블리치 黒崎一護 1/7 피규어 Z50J', 'franchise': entity('BLEACH', '블리치'),
           'characters': [entity('黒崎一護', '흑사 일고')], 'figure_form': None}
    value = normalize_result(source, raw)
    assert value['characters'][0]['ko'] == '쿠로사키 이치고'
    assert value['name_ko'] == '블리치 쿠로사키 이치고 1/7 피규어 Z50J'
    assert raw['characters'][0]['ko'] == '흑사 일고'


def test_brand_is_not_work_and_no_unstated_work_is_inferred():
    source = {'name_original': 'TENITOL オリジナル フィギュア', 'product_line': 'TENITOL'}
    raw = {'name_ko': '텐리토 오리지널 피규어', 'franchise': entity('TENITOL', '텐리토'),
           'characters': [], 'figure_form': None}
    assert normalize_result(source, raw)['franchise'] is None
    assert hints({'name_original': '黒崎一護'}) == [{'kind': 'characters', 'original': '黒崎一護', 'ko': '쿠로사키 이치고'}]


def test_long_work_alias_suppresses_short_alias():
    rows = hints({'name_original': 'NARUTO-ナルト- 疾風伝 うちはサスケ'})
    assert [r['ko'] for r in rows if r['kind'] == 'franchises'] == ['나루토 질풍전']


def test_generic_character_label_is_not_a_named_character():
    source = {'name_original': 'TENITOL オリジナルキャラクター フィギュア', 'product_line': 'TENITOL'}
    raw = {'name_ko': '텐리토 원래 캐릭터 피규어', 'franchise': entity('TENITOL', '텐리토'),
           'characters': [entity('オリジナルキャラクター', '원래 캐릭터')], 'figure_form': None}
    result = normalize_result(source, raw)
    assert result['characters'] == []
    assert result['name_ko'].startswith('TENITOL ')

from app.services.local_semantic_grounding import candidates, explicit_form
from app.services.local_semantic_lexicon import grounded_result
from app.services.reference_classifier import resolve
from app.services.semantic_rules import korean


def work(ko, aliases):
    return {'ko': ko, 'aliases': aliases, 'priority': 1,
            'reference': {'url': 'https://example.com/reference', 'evidence': aliases[0], 'checked_at': '2026-11-11'}}


def test_nested_work_alias_does_not_mask_naruto_character_name():
    title = 'NARUTO-ナルト- ニャルト！①うずまきナルト ②うちはサスケ'
    source = {'name_original': title, 'official_url': 'https://example.com/naruto'}
    characters = [
        dict(work('우즈마키 나루토', ['うずまきナルト']), work='나루토'),
        dict(work('우치하 사스케', ['うちはサスケ']), work='나루토'),
    ]
    record = resolve({'source': source, 'figure_id': 1, 'source_hash': 'x'},
                     [work('나루토', ['NARUTO-ナルト-', 'NARUTO', 'ナルト'])], characters, [])
    assert {c['ko'] for c in record['patch']['character_ko']} == {'우즈마키 나루토', '우치하 사스케'}


def test_clothing_one_piece_does_not_override_explicit_frieren_intro():
    source = {'name_original': 'TENITOL フリーレン クラシカルワンピースver.',
              'document_0': '「葬送のフリーレン」より主人公の「フリーレン」が登場。',
              'official_url': 'https://example.com/1', 'type': 'figure'}
    record = resolve({'source': source, 'figure_id': 1, 'source_hash': 'x'},
        [work('원피스', ['ワンピース']), work('장송의 프리렌', ['葬送のフリーレン'])], [], [])
    assert record['patch']['franchise_ko'] == '장송의 프리렌'
    source['document_0'] = None
    record = resolve({'source': source, 'figure_id': 1, 'source_hash': 'x'},
                     [work('원피스', ['ワンピース'])], [], [])
    assert 'franchise_ko' not in record['patch']


def test_unrelated_recommendation_cannot_supply_work():
    source = {'name_original': 'オリジナル フィギュア', 'official_url': 'https://example.com',
              'document_0': 'この商品が登場。おすすめ商品：『ONE PIECE』より別の商品。'}
    result = resolve({'source': source, 'figure_id': 1, 'source_hash': 'x'},
                     [work('원피스', ['ONE PIECE'])], [], [])
    assert 'franchise_ko' not in result['patch']


def test_height_date_and_brand_page_do_not_establish_scale_or_plush():
    assert explicit_form({'name_original': 'フィギュア', 'document_0': '全高110mm。スケール感。'}) is None
    assert explicit_form({'name_original': 'フィギュア', 'document_0': '予約日2025/1/7。'}) is None
    assert explicit_form({'name_original': 'フィギュア',
                          'document_0': '{"official_page_text":"関連商品ぬいぐるみ"}'}) is None


def test_negation_and_related_product_are_not_form_evidence():
    source = {'name_original': 'フィギュア', 'document_0': 'ぬいぐるみではありません。'}
    assert explicit_form(source) is None
    assert candidates(source)['figure_form'] is None
    assert explicit_form({'name_original': 'フィギュア', 'document_0': 'おすすめ商品：アクリルスタンド'}) is None


def test_positive_source_form_and_cyrillic_guard():
    assert explicit_form({'name_original': '超特大ぬいぐるみ'})['code'] == 'plush'
    assert explicit_form({'name_original': 'フィギュア', 'document_0': '1/7スケール。'})['code'] == 'scale_figure'
    assert explicit_form({'name_original': 'フィギュア', 'document_0': '可動フィギュア'})['code'] == 'action_figure'
    assert not korean('텐리토л 프리렌')


def test_source_composition_preserves_brand_and_repairs_known_names():
    source = {'name_original': 'TENITOL TALL フリーレン クラシカルワンピースver.'}
    result = grounded_result(source, {'name_ko': '텐리토л 털 프리렌', 'franchise': None,
                                      'characters': [], 'figure_form': None})
    assert result['name_ko'] == 'TENITOL TALL 프리렌 클래식 원피스 버전'
    assert result['characters'][0]['ko'] == '프리렌'


def test_unfamiliar_model_name_is_a_review_not_a_published_fact():
    source = {'name_original': '未確認キャラクター フィギュア'}
    value = grounded_result(source, {'name_ko': '그럴듯한 이름 피규어',
        'franchise': {'original': '未確認', 'ko': '가공한 작품'},
        'characters': [{'original': '未確認', 'ko': '가공한 이름'}], 'figure_form': None})
    assert value['name_ko'] is None
    assert value['franchise'] is None
    assert value['characters'] == []


def test_miku_series_heading_is_not_an_extra_character_of_len_figure():
    source = {'name_original': '初音ミクシリーズ デフォルメフィギュア 鏡音レン',
              'franchise': '初音ミクシリーズ'}
    from app.services.ollama_semantics import prepare_input
    grounded = prepare_input(source)['_grounded_candidates']
    assert [row['ko'] for row in grounded['characters']] == ['카가미네 렌']


def test_a_name_containing_naruto_does_not_establish_a_work():
    assert candidates({'name_original': 'うずまきナルト フィギュア'})['franchise'] is None


def test_katakana_word_boundary_cannot_turn_scale_into_luffy():
    from app.services.reference_classifier import match
    assert match('ルフィ', '1/7 スケールフィギュア') is None
    assert match('ルフィ', '1/7 スケール フィギュア') is None
    assert match('ルフィ', 'ワンピース ルフィ フィギュア') == 'ルフィ'
    assert match('鬼舞辻無惨', '鬼舞辻󠄀無惨') == '鬼舞辻󠄀無惨'


def test_miku_heading_is_removed_in_final_validation_too():
    from app.services.semantic_rules import validate_result
    source = {'name_original': '初音ミクシリーズ デフォルメフィギュア 鏡音レン',
              'franchise': '初音ミクシリーズ'}
    normalized = grounded_result(source, {'name_ko': '카가미네 렌', 'franchise': None,
                                          'characters': [], 'figure_form': None})
    fields, _ = validate_result(source, normalized)
    assert [c['ko'] for c in fields['characters']] == ['카가미네 렌']


def test_asuka_incarnations_are_distinct_and_numeric_document_scale_is_specific():
    from app.services.reference_classifier import cached_record
    source = {'name_original': '式波・アスカ・ラングレー 1/4 スケールフィギュア', 'official_url': ''}
    patch = cached_record(source, '', 1)['patch']
    assert [c['ko'] for c in patch['character_ko']] == ['시키나미 아스카 랑그레이']
    source = {'name_original': 'フィギュア', 'official_url': '',
              'document_0': '1/8スケール。彩色済み完成品フィギュア'}
    assert cached_record(source, '', 1)['patch']['figure_form'] == 'scale_figure'


def test_movie_heading_is_not_the_subject_of_reze_figure():
    source = {'name_original': '劇場版『チェンソーマン レゼ篇』 フィギュア レゼ',
              'franchise': '劇場版『チェンソーマン レゼ篇』'}
    result = grounded_result(source, {'name_ko': None, 'franchise': None, 'characters': [], 'figure_form': None})
    assert not any(c['original'] == 'チェンソーマン' for c in result['characters'])


def test_roman_season_cannot_disappear_from_published_translation():
    from app.services.semantic_rules import validate_result
    _, issues = validate_result({'name_original': 'デート・ア・ライブⅤ ぬいぐるみ'},
        {'name_ko': '데이트 어 라이브 봉제인형', 'franchise': None, 'characters': [], 'figure_form': None})
    assert 'TITLE_ROMAN_NUMERAL_CHANGED' in issues


def test_clothes_and_vehicle_brand_are_not_the_figure_itself():
    from app.services.reference_classifier import cached_record
    assert explicit_form({'name_original': 'ポンチョ ハイキュー!!'})['code'] == 'figure_parts'
    assert explicit_form({'name_original': '商品', 'document_0': '固定ポーズのプラキットです。'})['code'] == 'model_kit'
    source = {'name_original': 'ハリケーン 栄光の昭和ライダーエディション',
              'franchise': '仮面ライダーV3', 'product_line': 'S.H.Figuarts', 'official_url': ''}
    assert 'figure_form' not in cached_record(source, '', 1)['patch']

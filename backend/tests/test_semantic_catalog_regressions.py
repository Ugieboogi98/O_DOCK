from app.services.semantic_rules import context_candidates, validate_result
from app.services.ko_translation import failure
from types import SimpleNamespace


def test_gms_401_with_empty_balance_is_quota_error():
    assert failure(SimpleNamespace(status_code=401, body={
        'message': '[GMS 에러] This GMS key has no token left', 'statusCode': 401
    })) == ('QUOTA_EXHAUSTED', False)


def source(title, document=None):
    return {'name_original': title, 'manufacturer': 'MegaHouse', 'manufacturer_ko': '메가하우스',
            'product_line': 'Look Up', 'franchise': None, 'character': None,
            'scale': None, 'type': 'figure', 'document_0': document}


def test_japanese_ordinal_preserves_numeric_fact():
    data = source('バディコレ TVアニメ『ダンダダン』第二弾')
    fields, issues = validate_result(data, {'name_ko': '버디콜 TV 애니메이션 단다단 제2탄',
        'franchise': None, 'characters': [], 'figure_form': None})
    assert fields['translation_status'] == 'ready'
    assert 'TITLE_NUMERIC_FACT_CHANGED' not in issues
    _, wrong = validate_result(data, {'name_ko': '버디콜 TV 애니메이션 단다단 제3탄',
        'franchise': None, 'characters': [], 'figure_form': None})
    assert 'TITLE_NUMERIC_FACT_CHANGED' in wrong


def test_product_line_introduction_does_not_reverse_work_and_subject():
    data = source('ウマ娘 プリティーダービー メジロマックイーン',
        '『るかっぷ』より『ウマ娘 プリティーダービー』の「メジロマックイーン」が登場します。')
    candidates = context_candidates(data)
    assert {c['original'] for c in candidates if c['kind'] == 'franchise'} == {'ウマ娘 プリティーダービー'}
    assert {c['original'] for c in candidates if c['kind'] == 'character'} == {'メジロマックイーン'}

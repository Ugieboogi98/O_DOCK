import pytest
from app.services.local_semantic_lexicon import grounded_result
from app.services.local_semantic_subjects import recover,sound_matches
from app.services.semantic_rules import validate_result

def test_middle_dot_is_punctuation_not_an_untranslated_katakana_letter():
    from app.services.semantic_rules import korean
    assert korean('한텐구・조하쿠텐・굣코')
    assert not korean('엠마 フィギュア')
    assert not korean('엠마 物語')
    source={'name_original':'귀멸의 칼날 피규어 EX [한텐구・조하쿠텐・굣코] (A:한텐구)'}
    value=grounded_result(source,{'name_ko':None,'franchise':None,'characters':[],'figure_form':None})
    fields,_=validate_result(source,value)
    assert fields['translation_status']=='ready'

def result(original,ko,title,field='name_original'):
    return {'name_ko':title,'franchise':None,'characters':[{'original':original,'ko':ko,'evidence_field':field,
        'evidence':original,'confidence':1}],'figure_form':None}

@pytest.mark.parametrize('original,ko',[('エマ','엠마'),('マリナ','마리나'),('エリカ','에리카'),('カミラ','카밀라')])
def test_kana_reading_matches_conventional_hangul(original,ko):assert sound_matches(original,ko)

def test_wrong_reading_and_unguessed_kanji_remain_rejected():
    assert not sound_matches('エマ','아스카')
    assert not sound_matches('花子','하나코')
    assert not sound_matches('エマ','엄마')
    assert not sound_matches('キラ・ヤマト','키라 요마토')
    assert not sound_matches('ハマーン・カーン','하마인 카인')
    assert not sound_matches('カカワーシャ','카카와시야')
    assert sound_matches('カカワーシャ','카카와샤')

def test_existing_product_title_corrects_model_reading_without_changing_identity(monkeypatch):
    import app.services.local_semantic_subjects as service
    source={'name_original':'キラ・ヤマト 1/7スケールフィギュア','official_url':'https://example.com/product'}
    monkeypatch.setattr(service,'title_memory',lambda:{service.title_key(source):'키라 야마토 1/7 스케일 피규어'})
    assert service.catalog_reading(source,'キラ・ヤマト','키라 요마토')=='키라 야마토'

def test_a_spaceship_and_a_work_title_cannot_be_recovered_as_characters():
    source={'name_original':'ネェル・アーガマ 1/7スケールフィギュア','document_0':'宇宙戦艦の模型です。'}
    value=grounded_result(source,result('ネェル・アーガマ','네르 아가마','네르 아가마 1/7 스케일 피규어'))
    assert value['characters']==[]

def test_emma_scale_title_is_a_character_with_explicit_nikke_work():
    for title,expected in [('エマ 1/7スケールフィギュア','엠마 1/7 스케일 피규어'),
        ('エマ - オフィスセラピー 1/7スケールフィギュア','엠마 - 오피스 테라피 1/7 스케일 피규어')]:
        source={'name_original':title,'franchise':'勝利の女神:NIKKE','scale':'1/7'}
        value=grounded_result(source,result('エマ','에마','에마 1/7 스케일 피규어'))
        fields,issues=validate_result(source,value)
        assert fields['name_ko']==expected and fields['character_ko']=='엠마'
        assert fields['franchise_ko']=='승리의 여신: 니케' and not issues

@pytest.mark.parametrize('title,work,expected',[
    ('エマ・ブライトネス 1/7スケールフィギュア','俺だけ入れる隠しダンジョン','엠마 브라이트니스'),
    ('The Hidden Dungeon Only I Can Enter 1/7 Emma Brightness Figure','The Hidden Dungeon Only I Can Enter','엠마 브라이트니스'),
    ('約束のネバーランド ひっかけフィギュア エマ','約束のネバーランド','엠마'),
    ('ぬーどるストッパーフィギュア -制服晩餐会 -庭師 エマ・ウッズ-','IdentityV 第五人格','엠마 우즈'),
    ('러브라이브 니지가사키 학원 스쿨 아이돌 동호회 엠마 베르데',None,'엠마 베르데'),
])
def test_emma_names_are_scoped_to_the_actual_work(title,work,expected):
    source={'name_original':title,'franchise':work}
    value=grounded_result(source,{'name_ko':None,'franchise':None,'characters':[],'figure_form':None})
    fields,_=validate_result(source,value)
    assert fields['character_ko']==expected and fields['translation_status']=='ready'
    assert fields['franchise_ko']!='승리의 여신: 니케'

def test_unlisted_kana_subject_uses_title_structure_not_a_global_name_dictionary():
    source={'name_original':'カミラ 1/7スケールフィギュア','franchise':'鬼滅の刃'}
    value=grounded_result(source,result('カミラ','카밀라','카밀라 1/7 스케일 피규어'))
    assert value['characters'][0]['ko']=='카밀라' and value['name_ko']=='카밀라 1/7 스케일 피규어'
    assert value['characters'][0]['method']=='explicit_subject_kana_reading'

def test_named_subject_does_not_invent_a_franchise():
    source={'name_original':'エマ 1/7スケールフィギュア'}
    value=grounded_result(source,result('エマ','엠마','엠마 1/7 스케일 피규어'))
    assert value['franchise'] is None
    assert value['characters'][0]['ko']=='엠마'

def test_existing_korean_product_title_is_not_rejected_for_a_latin_brand():
    source={'name_original':'EXAMPLE BRAND 엠마 1/7 스케일 피규어'}
    value=grounded_result(source,{'name_ko':None,'franchise':None,'characters':[],'figure_form':None})
    assert value['name_ko']==source['name_original']

@pytest.mark.parametrize('title,original,ko',[
    ('1/7 スケールフィギュア','ルフィ','루피'),
    ('オリジナル 1/7スケールフィギュア','オリジナル','오리지널'),
    ('エマ 1/7スケールフィギュア','エマ','아스카'),
    ('鬼滅の刃 1/7スケールフィギュア','鬼滅の刃','귀멸의 칼날'),
])
def test_generic_words_wrong_readings_and_work_names_are_not_subjects(title,original,ko):
    source={'name_original':title,'franchise':'鬼滅の刃'}
    value=grounded_result(source,result(original,ko,'가공한 이름 1/7 스케일 피규어'))
    assert not any(c['ko']==ko for c in value['characters'])

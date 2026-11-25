from app.services.retail_entities import recognize

GROUPS = [
    {'work': '명일방주', 'medium': 'game', 'aliases': ['명일방주', 'アークナイツ', 'Arknights'],
     'characters': {'ラップランド': '라플란드', 'W': 'W', 'チェン': '첸'}},
    {'work': '명일방주: 엔드필드', 'medium': 'game', 'aliases': ['명일방주: 엔드필드', '명일방주 엔드필드', '엔드필드'],
     'characters': {'ジルベルタ': '질베르타'}},
    {'work': '히카루가 죽은 여름', 'medium': 'anime', 'aliases': ['히카루가 죽은 여름', '光が死んだ夏'],
     'characters': {'よしき': '요시키'}},
]


def test_recognizes_work_and_character_in_korean_listing():
    r = recognize('[예약판매] 넨도로이드 1598 명일방주 라플란드 재판', GROUPS)
    assert r == {'work': '명일방주', 'medium': 'game', 'characters': ['라플란드']}
    assert recognize('오렌지루즈 넨도로이드 No.3156 히카루가 죽은 여름 요시키', GROUPS)['characters'] == ['요시키']


def test_more_specific_work_wins():
    r = recognize('[예약판매] 넨도로이드 3152 명일방주 엔드필드 질베르타', GROUPS)
    assert r['work'] == '명일방주: 엔드필드' and r['characters'] == ['질베르타']


def test_latin_names_need_word_boundaries():
    assert recognize('굿스마일아츠상하이 넨도로이드 No.1375 명일방주 W', GROUPS)['characters'] == ['W']
    assert recognize('명일방주 첸 WINTER Ver.', GROUPS)['characters'] == ['첸']


def test_unknown_work_is_none():
    assert recognize('넨도로이드 No.9999 모르는 작품 주인공', GROUPS) is None


def test_work_title_is_not_a_character_mention():
    groups = [{'work': '히카루가 죽은 여름', 'medium': 'anime', 'aliases': ['히카루가 죽은 여름'],
               'characters': {'よしき': '요시키', 'ヒカル': '히카루'}}]
    assert recognize('넨도로이드 No.3156 히카루가 죽은 여름 요시키', groups)['characters'] == ['요시키']
    assert recognize('넨도로이드 히카루가 죽은 여름 히카루', groups)['characters'] == ['히카루']


def test_set_listing_names_both_characters_and_miku_variants_link_to_miku():
    groups = [
        {'work': '헌터×헌터', 'medium': 'anime', 'aliases': ['헌터×헌터', '헌터x헌터'],
         'characters': {'ヒソカ': '히소카', '히소카': '히소카', 'クロロ': '클로로 루실후르', '클로로': '클로로 루실후르'}},
        {'work': '보컬로이드', 'medium': None, 'aliases': ['보컬로이드'], 'characters': {}},
        {'work': '하츠네 미쿠', 'medium': 'music', 'aliases': ['하츠네 미쿠', '하츠네미쿠', '미쿠', '사쿠라미쿠'],
         'characters': {'하츠네미쿠': '하츠네 미쿠', '사쿠라미쿠': '하츠네 미쿠', '하츠네 미쿠': '하츠네 미쿠'}},
    ]
    hit = recognize('메가하우스 룩업 헌터x헌터 히소카 & 클로로 세트', groups)
    assert hit['work'] == '헌터×헌터' and hit['characters'] == ['히소카', '클로로 루실후르']
    hit = recognize('후류 누들스토퍼 보컬로이드 하츠네미쿠 사쿠라미쿠 2027', groups)
    assert hit['work'] == '하츠네 미쿠' and hit['characters'] == ['하츠네 미쿠']


def test_artist_original_is_recognised_only_without_a_known_work():
    groups = [{'work': '원피스', 'medium': None, 'aliases': ['원피스'], 'characters': {}}]
    assert recognize('1/6 키키 illustrated by RST(디럭스판)', groups)['work'] == '오리지널'
    assert recognize('원피스 BWFC 롤로노아 조로 THE ORIGINAL', groups)['work'] == '원피스'


def test_equivalent_miku_works():
    from app.services.retail_entities import same_work
    assert same_work('보컬로이드', '하츠네 미쿠') and same_work('원신', '원신')
    assert not same_work('원신', '하츠네 미쿠') and not same_work(None, '원신')

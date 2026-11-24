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

from app.services.wikidata_groups import merge

CURATED = [{'work': '명일방주', 'aliases': ['アークナイツ'], 'characters': [['ラップランド', '라플란드']]}]
KNOWN = [{'ko': '체인소 맨', 'aliases': ['チェンソーマン']}]


def test_curated_spelling_wins_and_characters_fold_into_curated_work():
    wd = [{'work': '아크나이츠', 'medium': 'game', 'aliases': ['アークナイツ', 'Arknights'],
           'characters': [[['ラップランド', '랩랜드'], '랩랜드'], [['テキサス', '텍사스'], '텍사스']], 'wikidata': ['Q1']}]
    out = merge(CURATED, KNOWN, wd)
    assert [g['work'] for g in out] == ['명일방주']
    assert out[0]['characters'] == [[['テキサス', '텍사스'], '텍사스']]  # 랩랜드 never contradicts 라플란드
    assert out[0]['aliases'] == []  # the curated work keeps its own aliases


def test_verified_work_title_wins():
    wd = [{'work': '체인소맨', 'aliases': ['チェンソーマン'], 'characters': [[['マキマ', '마키마'], '마키마']]}]
    assert merge(CURATED, KNOWN, wd)[0]['work'] == '체인소 맨'


def test_alias_claimed_by_two_wikidata_titles_is_dropped():
    wd = [{'work': '갑', 'aliases': ['同じ', 'Alpha Work'], 'characters': []},
          {'work': '을', 'aliases': ['同じ', 'Beta Work'], 'characters': []}]
    out = {g['work']: g['aliases'] for g in merge([], [], wd)}
    assert out == {'갑': ['Alpha Work'], '을': ['Beta Work']}


def test_new_work_is_kept():
    wd = [{'work': '히카루가 죽은 여름', 'medium': 'manga', 'aliases': ['光が死んだ夏'],
           'characters': [[['ヒカル', '히카루'], '히카루']]}]
    out = merge(CURATED, KNOWN, wd)
    assert out[0]['work'] == '히카루가 죽은 여름' and out[0]['aliases'] == ['光が死んだ夏']

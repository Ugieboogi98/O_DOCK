"""split-semantics-v7: glossary repair, learned aliases, similar products, stale retry, worker lock."""
import json
from types import SimpleNamespace
import pytest
from app.services.kana_hangul import to_hangul, is_kana
from app.services.semantic_neighbors import build_learned, learned_candidates, NgramIndex
from app.services.split_semantics import (Pipeline, residual_spans, resolve_glossary, assemble_glossary,
                                          grounded_dictionary, VERSION)
from app.services.worker_lock import advisory_lock, lock_key


@pytest.mark.parametrize('kana,ko', [
    ('ナツメ タカシ', '나츠메 타카시'), ('うずまきナルト', '우즈마키나루토'), ('ひゅうが', '휴우가'),
    ('せんじゅ', '센쥬'), ('つなで', '츠나데'), ('フェルン', '페룬'), ('チャイナ', '차이나'), ('キッチン', '킷친'),
])
def test_kana_transliteration_matches_dictionary_conventions(kana, ko):
    assert to_hangul(kana) == ko


def test_transliteration_rejects_kanji_and_empty():
    assert to_hangul('夏目') is None and to_hangul('') is None and not is_kana('ABC')


def test_residual_spans_split_katakana_from_kanji():
    assert residual_spans('넨도로이드 夏目貴志&ニャンコ先生コレクション') == ['夏目貴志', 'ニャンコ', '先生', 'コレクション']


def test_glossary_names_are_transliterated_and_terms_validated():
    spans = ['夏目貴志', 'ニャンコ', '先生', 'コレクション', '謎']
    items = [
        {'span': '夏目貴志', 'kind': 'name', 'reading': 'なつめ たかし', 'ko': 'IGNORED'},
        {'span': 'ニャンコ', 'kind': 'name', 'reading': '', 'ko': ''},
        {'span': '先生', 'kind': 'term', 'reading': '', 'ko': '선생'},
        {'span': 'コレクション', 'kind': 'term', 'reading': '', 'ko': '컬렉션'},
        {'span': '謎', 'kind': 'term', 'reading': '', 'ko': '謎'},          # still Japanese -> rejected
        {'span': 'not-a-span', 'kind': 'term', 'reading': '', 'ko': '무시'},
        {'span': '夏目貴志', 'kind': 'name', 'reading': '漢字', 'ko': ''},  # duplicate ignored
    ]
    mapping = resolve_glossary(items, spans)
    assert mapping == {'夏目貴志': '나츠메 타카시', 'ニャンコ': '냔코', '先生': '선생', 'コレクション': '컬렉션'}
    assert assemble_glossary('나츠메 우인장 夏目貴志&ニャンコ先生コレクション', mapping) == '나츠메 우인장 나츠메 타카시 & 냔코 선생 컬렉션'
    assert assemble_glossary('謎 피규어', mapping) is None


class GlossaryClient:
    def __init__(self, retry_ko=None):
        self.calls = []
        self.retry_ko = retry_ko

    def model_digest(self, model):
        return model + '-digest'

    def infer(self, model, prompt, data, schema):
        self.calls.append(schema)
        if 'items' in schema['properties']:
            return {'items': [{'span': s, 'kind': 'name', 'reading': 'なぞ', 'ko': ''} if s.startswith('謎') else
                              {'span': s, 'kind': 'term', 'reading': '', 'ko': '피규어'} for s in data['spans']]}, {'seconds': 1}
        if 'name_ko' in schema['properties'] and len(self.calls) > 2 and self.retry_ko:
            return {'name_ko': self.retry_ko}, {'seconds': 1}
        return {'name_ko': '謎の피규어'}, {'seconds': 1}


def test_failed_translation_is_repaired_from_span_glossary_without_parts(tmp_path):
    c = GlossaryClient()
    p = Pipeline({'fingerprint': 't', 'titles': {}}, c, tmp_path)
    r = p.translate({'name_original': '謎のフィギュア', 'official_url': 'https://e/1', 'manufacturer': 'TAITO', 'type': 'figure'})
    assert r['method'] == 'span_glossary_assembly'
    assert '謎' not in r['name_ko'] and '나조' in r['name_ko']
    assert len(c.calls) == 2  # initial + glossary; no parts/review calls


def test_learned_aliases_require_agreement_and_literal_evidence():
    ready = lambda work_o, work_k, chars: {'classification_status': 'ready', 'franchise_ko': work_k,
        'evidence': {'franchise': {'original': work_o}}, 'characters': [{'original': o, 'ko': k} for o, k in chars]}
    rows = [
        (1, 'ねんどろいど 夏目友人帳 ニャンコ先生', ready('夏目友人帳', '나츠메 우인장', [('ニャンコ先生', '냥코 선생')])),
        (2, 'ぬいぐるみ 夏目友人帳 ニャンコ先生', ready('夏目友人帳', '나츠메 우인장', [('ニャンコ先生', '냥코 선생')])),
        (3, 'フィギュア 単独作品 一人', ready('単独作品', '단독 작품', [('一人', '혼자')])),          # support 1
        (4, 'X 衝突作品', ready('衝突作品', '하나', [])), (5, 'Y 衝突作品', ready('衝突作品', '둘', [])),  # conflict
        (6, 'Z 未確認', {'classification_status': 'review', 'franchise_ko': 'x', 'characters': []}),
    ]
    learned = build_learned(rows)
    originals = {a['original'] for a in learned['aliases']}
    assert originals == {'夏目友人帳', 'ニャンコ先生'}
    hit = learned_candidates({'name_original': 'アクスタ 夏目友人帳 ニャンコ先生 B'}, learned)
    assert hit['franchise']['ko'] == '나츠메 우인장' and hit['franchise']['evidence'] == '夏目友人帳'
    assert [c['ko'] for c in hit['characters']] == ['냥코 선생']
    # A character of a different confirmed work is not attached.
    assert learned_candidates({'name_original': 'ニャンコ先生'}, learned, work_ko='다른 작품')['characters'] == []
    # Grounded result passes the unchanged strict validator.
    from app.services.semantic_rules import validate_result
    source = {'name_original': 'アクスタ 夏目友人帳 ニャンコ先生 B', 'manufacturer': 'M', 'type': 'figure'}
    g = grounded_dictionary(source, {'learned': learned})
    fields, issues = validate_result(source, {'name_ko': '아크릴 스탠드 나츠메 우인장 냥코 선생 B', **g})
    assert fields['franchise_ko'] == '나츠메 우인장' and '냥코 선생' in fields['character_ko']


def test_ngram_index_returns_similar_verified_products():
    idx = NgramIndex([
        {'figure_id': 1, 'name_original': 'ねんどろいど 葬送のフリーレン フェルン', 'franchise_ko': '장송의 프리렌'},
        {'figure_id': 2, 'name_original': 'POP UP PARADE 呪術廻戦 五条悟', 'franchise_ko': '주술회전'},
    ])
    top = idx.similar('ねんどろいど 葬送のフリーレン シュタルク', 1)
    assert top and top[0]['figure_id'] == 1 and 0 < top[0]['similarity'] <= 1
    assert NgramIndex([]).similar('anything') == []


def test_classification_payload_includes_similar_examples(tmp_path):
    class C:
        def __init__(self): self.payloads = []
        def model_digest(self, m): return m
        def infer(self, model, prompt, data, schema):
            self.payloads.append(data)
            return {'franchise': None, 'characters': [], 'figure_form': None}, {'seconds': 0}
    learned = {'aliases': [], 'examples': [{'figure_id': 9, 'name_original': 'ねんどろいど 架空作品 別キャラ',
               'franchise_ko': '장송의 프리렌', 'characters_ko': ['페른'], 'figure_form': 'nendoroid'}]}
    c = C()
    p = Pipeline({'fingerprint': 'x', 'titles': {}, 'learned': learned}, c, tmp_path)
    p.classify({'name_original': 'ねんどろいど 架空作品 新キャラ', 'type': 'figure'}, {'name_ko': '넨도로이드'})
    assert c.payloads[0]['similar_verified_products'][0]['franchise_ko'] == '장송의 프리렌'
    assert 'figure_id' not in c.payloads[0]['similar_verified_products'][0]


@pytest.mark.parametrize('retry_stale,expected', [(False, []), (True, ['1'])])
def test_stale_failures_retry_once_per_pipeline_version(tmp_path, monkeypatch, retry_stale, expected):
    import scripts.split_semantics_worker as worker
    class DB:
        def __enter__(self): return self
        def __exit__(self, *a): pass
        def get(self, model, fid): return SimpleNamespace(id=fid)
    seen = []
    class FakePipeline:
        def __init__(self, *a):
            self.translation_model = 't'; self.classification_model = 'c'; self.digests = {'t': 'a', 'c': 'b'}
        def translate(self, source):
            seen.append(source['name_original']); raise ValueError('still invalid')
    d = tmp_path / 'reference/semantic_dictionary'; d.mkdir(parents=True)
    (d / 'catalog.json').write_text(json.dumps({'fingerprint': 'new'}))
    reports = tmp_path / 'r'; reports.mkdir()
    (reports / 'failures.json').write_text(json.dumps({'1': {'time': 0, 'error': 'X', 'dictionary': 'old', 'pipeline': 'split-semantics-v6'},
                                                     '2': {'time': 0, 'error': 'X', 'dictionary': 'new', 'pipeline': VERSION}}))
    monkeypatch.setattr(worker, 'get_settings', lambda: SimpleNamespace(data_dir=tmp_path))
    monkeypatch.setattr(worker, 'SessionLocal', DB)
    monkeypatch.setattr(worker, 'Pipeline', FakePipeline)
    monkeypatch.setattr(worker, 'pending_jobs', lambda *a: [SimpleNamespace(error_summary=json.dumps({'figure_id': i})) for i in (1, 2)])
    monkeypatch.setattr(worker, 'source_of', lambda f: {'name_original': str(f.id)})
    monkeypatch.setattr(worker, 'source_hash', lambda s: s['name_original'])
    worker.consume(20, reports, client=object(), skip_failed=True, retry_stale=retry_stale)
    assert seen == expected
    if retry_stale:
        # After failing under the current version it is no longer stale, so it is skipped next time.
        seen.clear()
        worker.consume(20, reports, client=object(), skip_failed=True, retry_stale=True)
        assert seen == []


def test_advisory_lock_is_noop_off_postgres_and_key_is_stable():
    engine = SimpleNamespace(dialect=SimpleNamespace(name='sqlite'))
    with advisory_lock('x', engine) as key:
        assert key is None
    assert lock_key('split_semantics_worker') == lock_key('split_semantics_worker') != lock_key('other')


def test_learned_character_inside_work_title_is_not_a_character_mention():
    learned = {'aliases': [
        {'kind': 'franchise', 'original': '葬送のフリーレン', 'ko': '장송의 프리렌', 'work': None, 'support': 5},
        {'kind': 'character', 'original': 'フリーレン', 'ko': '프리렌', 'work': '장송의 프리렌', 'support': 5},
        {'kind': 'character', 'original': 'フェルン', 'ko': '페른', 'work': '장송의 프리렌', 'support': 5}]}
    hit = learned_candidates({'name_original': '葬送のフリーレン Luminasta ‐フェルン‐'}, learned)
    assert [c['ko'] for c in hit['characters']] == ['페른']
    assert [c['ko'] for c in learned_candidates({'name_original': '葬送のフリーレン フリーレン'}, learned)['characters']] == ['프리렌']


def test_explicit_kana_character_is_named_without_model(tmp_path):
    class NoModel:
        def model_digest(self, m): return m
        def infer(self, *a): raise AssertionError('model must not be called for kana names')
    p = Pipeline({'fingerprint': 'k', 'titles': {}}, NoModel(), tmp_path)
    source = {'name_original': 'ねんどろいど ヨツユ', 'document_0': '『架空の物語』より「ヨツユ」がねんどろいどで登場。'}
    ground = {'franchise': {'original': '架空の物語', 'ko': '가공의 이야기', 'evidence_field': 'document_0',
                            'evidence': '『架空の物語』より「ヨツユ」', 'confidence': 1}, 'characters': [], 'figure_form': None}
    p.name_explicit_relations(source, ground, {})
    assert ground['characters'][0]['ko'] == '요츠유' and ground['characters'][0]['method'] == 'explicit_relation_glossary'


def test_rate_limiter_window_and_proxy_header_trust():
    from types import SimpleNamespace
    from app.core import rate_limit
    rate_limit.reset()
    assert all(rate_limit.hit('k', 3, 60, now=t) for t in (0, 1, 2))
    assert not rate_limit.hit('k', 3, 60, now=3)
    assert rate_limit.hit('k', 3, 60, now=61.5)  # oldest attempts expired
    proxied = SimpleNamespace(client=SimpleNamespace(host='172.18.0.5'), headers={'x-real-ip': '203.0.113.7'})
    direct = SimpleNamespace(client=SimpleNamespace(host='8.8.8.8'), headers={'x-real-ip': '1.2.3.4'})
    assert rate_limit.client_ip(proxied) == '203.0.113.7'
    assert rate_limit.client_ip(direct) == '8.8.8.8'  # a public peer cannot spoof its address


def test_same_origin_rejects_cross_site_fetch_metadata(monkeypatch):
    from types import SimpleNamespace
    from fastapi import HTTPException
    from app.core import security
    monkeypatch.setattr(security, 'get_settings', lambda: SimpleNamespace(cors_origins='http://localhost:8080'))
    req = lambda h: SimpleNamespace(headers=h)
    security.require_same_origin(req({'origin': 'http://localhost:8080'}))
    security.require_same_origin(req({}))  # scripts without browser headers
    for headers in ({'origin': 'https://evil.example'}, {'sec-fetch-site': 'cross-site'}):
        with pytest.raises(HTTPException):
            security.require_same_origin(req(headers))


def test_hiragana_long_mark_stays_in_one_span_and_glued_mark_is_residue():
    from app.services.split_semantics import RESIDUE, translation_valid
    assert residual_spans('넨도로이드 파워 私服Ver. べーしっく') == ['私服', 'べーしっく']
    assert RESIDUE.search('누ー도르') and not RESIDUE.search('피규어 ー 하츠네 미쿠 ー')
    assert not translation_valid({'name_original': 'ぬーどる', 'type': 'figure'}, '누ー도르')


def test_term_with_english_fallback_or_long_mark_is_rejected():
    items = [{'span': 'しっく', 'kind': 'term', 'reading': '', 'ko': '시 chick'},
             {'span': 'べ', 'kind': 'term', 'reading': '', 'ko': '베ー'},
             {'span': 'くじ', 'kind': 'term', 'reading': '', 'ko': '쿠지'}]
    assert resolve_glossary(items, ['しっく', 'べ', 'くじ']) == {'くじ': '쿠지'}


def test_span_memory_keeps_one_spelling_across_products(tmp_path):
    class C(GlossaryClient):
        answers = iter(['냥코', '고양이'])
        def infer(self, model, prompt, data, schema):
            self.calls.append(data)
            if 'items' in schema['properties']:
                return {'items': [{'span': s, 'kind': 'term', 'reading': '', 'ko': next(self.answers) if s == 'ニャンコ' else '피규어'}
                                  for s in data['spans']]}, {'seconds': 0}
            return {'name_ko': 'ニャンコ 피규어'}, {'seconds': 0}
    c = C()
    p = Pipeline({'fingerprint': 'm', 'titles': {}}, c, tmp_path)
    first = p.translate({'name_original': 'ニャンコ フィギュア A', 'type': 'figure'})
    second = Pipeline({'fingerprint': 'm', 'titles': {}}, c, tmp_path).translate({'name_original': 'ニャンコ フィギュア B', 'type': 'figure'})
    assert '냥코' in first['name_ko'] and '냥코' in second['name_ko']
    glossary_calls = [d for d in c.calls if 'spans' in d]
    assert len(glossary_calls) == 1  # the second product reuses the remembered spelling


def test_short_or_embedded_kana_alias_does_not_match():
    from app.services.semantic_neighbors import usable_alias, literal_in
    assert not usable_alias('アイ') and usable_alias('アスナ') and usable_alias('猫猫')
    assert not literal_in('アスナ', 'アスナロ物語') and literal_in('アスナ', 'POP UP PARADE アスナ L')
    learned = {'aliases': [{'kind': 'character', 'original': 'アイ', 'ko': '아이', 'work': None, 'support': 9},
                           {'kind': 'character', 'original': 'アスナ', 'ko': '아스나', 'work': None, 'support': 6}]}
    assert learned_candidates({'name_original': 'アイドル衣装 アスナロ'}, learned)['characters'] == []


@pytest.mark.parametrize('known,span,accepted', [
    ('베르세르크', 'ベルセルク', True), ('라인하르트 폰 로엔그람', 'ラインハルト・フォン・ローエングラム', True),
    ('벤티', 'ウェンティ', True), ('포름알데하이드', 'ポムニ', False), ('바니', 'パトラ', False),
])
def test_known_katakana_spelling_is_used_only_when_it_sounds_like_the_reading(known, span, accepted):
    mapping = resolve_glossary([{'span': span, 'kind': 'name', 'reading': '', 'ko': known}], [span])
    assert (mapping[span] == known) is accepted
    assert mapping[span] == known or mapping[span] == to_hangul(span)


def test_rerun_never_downgrades_a_ready_field_but_takes_new_ready_fields():
    from app.services.product_semantics import keep_ready_fields
    old = {'franchise_ko': '원신', 'character_ko': None, 'characters': [], 'figure_form': 'nendoroid', 'figure_form_ko': '넨도로이드',
           'evidence': {'franchise': {'original': '原神'}, 'figure_form': {'code': 'nendoroid'}},
           'field_status': {'name_ko': 'ready', 'franchise_ko': 'ready', 'character_ko': 'missing', 'figure_form': 'ready'},
           'classification_status': 'partial'}
    new = {'name_ko': '넨도로이드 나히다', 'franchise_ko': None, 'character_ko': '나히다', 'characters': [{'original': 'ナヒーダ', 'ko': '나히다'}],
           'figure_form': None, 'figure_form_ko': None, 'evidence': {'characters': [{'original': 'ナヒーダ'}]},
           'field_status': {'name_ko': 'ready', 'franchise_ko': 'review', 'character_ko': 'ready', 'figure_form': 'missing'},
           'field_issues': {'franchise_ko': ['X'], 'figure_form': []}, 'classification_status': 'review'}
    out = keep_ready_fields(new, old)
    assert out['franchise_ko'] == '원신' and out['figure_form'] == 'nendoroid' and out['character_ko'] == '나히다'
    assert out['evidence']['franchise'] == {'original': '原神'} and out['field_issues']['franchise_ko'] == []
    assert out['classification_status'] == 'ready' and set(out['kept_previous_fields']) == {'franchise_ko', 'figure_form'}
    # A manual override is never replaced by the previous automatic value.
    overridden = {**new, 'classification_overrides': {'franchise_ko': {}}}
    assert keep_ready_fields(overridden, old)['franchise_ko'] is None


def test_genre_introduced_work_and_single_title_name_become_relations():
    from app.services.split_semantics import title_relations
    s = {'name_original': '刀剣乱舞ONLINE 山姥切国広', 'manufacturer': 'MegaHouse',
         'document_0': 'るかっぷシリーズよりPCブラウザ・スマホアプリゲーム「刀剣乱舞ONLINE」の山姥切国広が登場です！'}
    assert [(r['kind'], r['original']) for r in title_relations(s)] == [('franchise', '刀剣乱舞ONLINE'), ('character', '山姥切国広')]
    known = {'name_original': '鬼滅の刃 獪岳', 'document_0': 'るかっぷシリーズより「獪岳」が新規造形で登場です！'}
    assert [r['original'] for r in title_relations(known, '鬼滅の刃')] == ['獪岳']
    # Product words and non-name mentions are not characters.
    line = {'name_original': 'バディコレ  SPY×FAMILY', 'document_0': 'TVアニメ「SPY×FAMILY」より「バディコレ」が登場'}
    assert all(r['kind'] != 'character' for r in title_relations(line, stop={'バディコレ'}))
    col = {'name_original': 'コレクション ブルーロック vol.2', 'document_0': 'TVアニメ「ブルーロック」のコレクション第2弾'}
    assert all(r['kind'] != 'character' for r in title_relations(col))


def test_foreign_script_rejected_and_unknown_kanji_names_not_published(tmp_path):
    from app.services.semantic_rules import korean
    assert not korean('냐ัง코 선생님') and not korean('패치ولي 노우ledge') and korean('사이키 쿠스오의 Ψ난 Ⅱ')
    class C:
        def model_digest(self, m): return m
        def infer(self, model, prompt, data, schema):
            return {'franchise': None, 'figure_form': None, 'characters': [
                {'original': '獪岳', 'ko': '카타케이', 'evidence_field': 'name_original', 'evidence': '獪岳', 'confidence': 1},
                {'original': 'テスト', 'ko': '테스토', 'evidence_field': 'name_original', 'evidence': 'テスト', 'confidence': 1}]}, {'seconds': 0}
    p = Pipeline({'fingerprint': 'u', 'titles': {}}, C(), tmp_path)
    out = p.classify({'name_original': 'ねんどろいど 架空 獪岳 テスト', 'type': 'figure'}, {'name_ko': 'x'})
    assert [c['original'] for c in out['result']['characters']] == ['テスト']
    assert [c['original'] for c in out['unverified_characters']] == ['獪岳']
    assert set(out['result']) == {'franchise', 'characters', 'figure_form'}


def test_repair_removes_unknown_kanji_names_and_recomputes_state():
    from scripts.repair_unverified_names import repaired
    fields = {'characters': [{'original': '獪岳', 'ko': '카타케이'}, {'original': 'アスナ', 'ko': '아스나'}],
              'character_ko': '카타케이 · 아스나', 'franchise_ko': 'x', 'figure_form': 'nendoroid',
              'field_status': {'name_ko': 'ready', 'franchise_ko': 'ready', 'character_ko': 'ready', 'figure_form': 'ready'}}
    out, removed = repaired(fields, set())
    assert [c['ko'] for c in removed] == ['카타케이'] and out['character_ko'] == '아스나' and out['classification_status'] == 'ready'
    only, _ = repaired({**fields, 'characters': fields['characters'][:1]}, set())
    assert only['character_ko'] is None and only['field_status']['character_ko'] == 'missing' and only['classification_status'] == 'partial'
    assert repaired(fields, {'獪岳'})[0] is None


def test_normalize_ignores_variation_selectors():
    from app.services.semantic_rules import normalize
    assert normalize('鬼舞辻\U000e0100無惨') == normalize('鬼舞辻無惨')
    assert normalize('葛\ufe00城') == normalize('葛城')


def _title_issues(original, title):
    from app.services.semantic_rules import validate_result
    return validate_result({'name_original': original}, {'name_ko': title, 'franchise': None, 'characters': [], 'figure_form': None})[1]


def test_numeric_guard_accepts_equivalent_forms():
    assert 'TITLE_NUMERIC_FACT_CHANGED' not in _title_issues('映画「五等分の花嫁」 中野一花', '영화 「5등분의 신부」 나카노 이치카')
    assert 'TITLE_NUMERIC_FACT_CHANGED' not in _title_issues('TVアニメ「らんま1/2」 らんま', 'TV 애니메이션 「란마 ½」 란마')
    assert 'TITLE_NUMERIC_FACT_CHANGED' not in _title_issues('TVアニメ『ダンダダン』第二弾', '단다단 두 번째')
    assert 'TITLE_PRODUCT_CODE_CHANGED' not in _title_issues('ニュージャージー IRF2024ver.', '뉴저지 IRF2024 버전')
    assert 'TITLE_PRODUCT_CODE_CHANGED' not in _title_issues('MIRAGE C02-URANUS', '미라주 C02-우라노스')


def test_numeric_guard_still_rejects_changed_numbers():
    assert 'TITLE_NUMERIC_FACT_CHANGED' in _title_issues('1/7スケールフィギュア', '1/8 스케일 피규어')
    assert 'TITLE_NUMERIC_FACT_CHANGED' in _title_issues('TVアニメ『ダンダダン』第二弾', '단다단 세 번째')
    assert 'TITLE_NUMERIC_FACT_CHANGED' in _title_issues('ダンダダン フィギュア', '단다단 피규어 3')
    assert 'TITLE_PRODUCT_CODE_CHANGED' in _title_issues('MIRAGE C02-URANUS', '미라주 우라노스')
    assert 'TITLE_ROMAN_NUMERAL_CHANGED' in _title_issues('デート・ア・ライブⅤ', '데이트 어 라이브')


def test_lone_honorific_is_fixed():
    from app.services.split_semantics import HONORIFICS, assemble_glossary
    assert assemble_glossary('스파이 패밀리 손바닥 요르 さん', {'さん': HONORIFICS['さん']}) == '스파이 패밀리 손바닥 요르 씨'


def test_title_character_keeps_work_korean_title(tmp_path):
    class NoModel:
        def model_digest(self, m): return m
        def infer(self, *a): raise AssertionError('model must not be called')
    p = Pipeline({'fingerprint': 'k', 'titles': {}}, NoModel(), tmp_path)
    source = {'name_original': 'ねんどろいど ブラック・ジャック',
              'document_0': '『ブラック・ジャック』より、主人公「ブラック・ジャック」がねんどろいどに登場です'}
    ground = {'franchise': {'original': 'ブラック・ジャック', 'ko': '블랙 잭', 'evidence_field': 'document_0',
                            'evidence': '『ブラック・ジャック』', 'confidence': 1}, 'characters': [], 'figure_form': None}
    p.name_explicit_relations(source, ground, {})
    assert [c['ko'] for c in ground['characters']] == ['블랙 잭']


def test_version_name_in_title_is_not_a_character():
    from app.services.split_semantics import title_relations
    source = {'name_original': 'ねんどろいど 初音ミク ヴァンパイア Ver.',
              'document_0': 'DECO*27氏による楽曲『ヴァンパイア』MV内に登場する「初音ミク」がねんどろいどで再登場！'}
    assert title_relations(source, '初音ミク') == []
    named = {'name_original': '地獄楽 画眉丸', 'document_0': 'TVアニメ「地獄楽」より「画眉丸」が登場。'}
    assert [r['original'] for r in title_relations(named, '地獄楽') if r['kind'] == 'character'] == ['画眉丸']
    numbered = {'name_original': '呪術廻戦 虎杖悠仁 ver.2', 'document_0': 'TVアニメ『呪術廻戦』より「虎杖悠仁」が登場。'}
    assert [r['original'] for r in title_relations(numbered, '呪術廻戦') if r['kind'] == 'character'] == ['虎杖悠仁']


def test_described_outfit_version_is_not_named_as_character(tmp_path):
    class NoModel:
        def model_digest(self, m): return m
        def infer(self, *a): raise AssertionError('model must not be called')
    p = Pipeline({'fingerprint': 'k', 'titles': {}}, NoModel(), tmp_path)
    source = {'name_original': 'ねんどろいど 木之本桜 CLEAR Ver.',
              'document_0': 'TVアニメ『カードキャプターさくら クリアカード編』より、主人公「木之本桜」がオープニング「CLEAR」の衣装で登場！'}
    sakura = {'original': '木之本桜', 'ko': '키노모토 사쿠라', 'evidence_field': 'name_original', 'evidence': '木之本桜', 'confidence': 1}
    ground = {'franchise': {'original': 'カードキャプターさくら クリアカード編', 'ko': '카드캡터 사쿠라 클리어 카드 편',
                            'evidence_field': 'document_0', 'evidence': '『カードキャプターさくら クリアカード編』', 'confidence': 1},
              'characters': [sakura], 'figure_form': None}
    p.name_explicit_relations(source, ground, {})
    assert [c['ko'] for c in ground['characters']] == ['키노모토 사쿠라']


def test_latin_only_title_is_kept_but_changed_latin_is_not():
    from app.services.semantic_rules import validate_result
    empty = {'franchise': None, 'characters': [], 'figure_form': None}
    for title in ('KAITO', 'C.C.', 'D-STYLE IRONKONG  ［Clear Parts Append］'):
        fields, _ = validate_result({'name_original': title}, {'name_ko': title, **empty})
        assert fields['translation_status'] == 'ready', title
    fields, _ = validate_result({'name_original': 'KAITO'}, {'name_ko': 'KAITO V3', **empty})
    assert fields['translation_status'] != 'ready'
    fields, _ = validate_result({'name_original': 'ねんどろいど KAITO'}, {'name_ko': 'ねんどろいど KAITO', **empty})
    assert fields['translation_status'] != 'ready'


def test_web_proof_must_be_a_word_of_the_title():
    from app.services.verified_classification import standalone
    assert not standalone('ルフィ', '七海千秋 1/7スケールフィギュア')
    assert standalone('ルフィ', 'ONE PIECE モンキー・D・ルフィ')
    assert not standalone('루피', '넨도로이드 네페루피토')
    assert standalone('니케', '넨도로이드 승리의여신니케')
    assert standalone('エミリア', 'フィギュアーエミリア陣営ー')
    assert standalone('初音ミク', '初音ミクシリーズ ふわぷち')
    assert not standalone('ワンピース', 'フリーレン クラシカルワンピースver.')
    assert standalone('ウルトラマン', 'ウルトラマンメビウス', prefix=True)
    assert not standalone('rem', 'Alien Premium Figure')


def test_repair_drops_only_the_unproven_character():
    from scripts.repair_web_proofs import repair
    src = {'name_original': 'ラム&レム 1/7スケールフィギュアセット'}
    proof = lambda m: {'field': 'name_original', 'match': m}
    fields = {'name_ko': '람&렘', 'franchise_ko': None, 'character_ko': '몽키 D. 루피 · 렘 · 람', 'figure_form': None,
              'characters': [], 'evidence': {}, 'field_issues': {},
              'classification_overrides': {'character_ko': {
                  'source_hash': 'h', 'method': 'web_verified', 'value': '몽키 D. 루피 · 렘 · 람',
                  'characters': [{'original': 'ルフィ', 'ko': '몽키 D. 루피'}, {'original': 'レム', 'ko': '렘'}, {'original': 'ラム', 'ko': '람'}],
                  'evidence': {'method': 'web_verified', 'references': [proof('ルフィ'), proof('レム'), proof('ラム')]}}}}
    out, changes = repair(fields, src)
    assert changes[0]['action'] == 'narrowed' and out['character_ko'] == '렘 · 람'


def test_dictionary_groups_ground_wikidata_characters_inside_confirmed_work():
    from app.services.local_semantic_lexicon import title_hints
    groups = [{'work': '원신', 'aliases': ['原神'], 'characters': [['ナヒーダ', '나히다']]},
              {'work': '원신', 'aliases': [], 'provenance': 'wikidata', 'characters': [[['ウェンティ'], '벤티']]},
              {'work': '다른 작품', 'aliases': [], 'provenance': 'wikidata', 'characters': [[['ウェンティ'], '다른 이름']]}]
    ground = {'franchise': {'original': '原神', 'ko': '원신', 'evidence_field': 'franchise', 'evidence': '原神'},
              'characters': [], 'figure_form': None}
    title_hints({'name_original': 'ねんどろいど ウェンティ', 'franchise': '原神'}, ground, groups)
    assert [c['ko'] for c in ground['characters']] == ['벤티']


def test_series_name_and_opening_hero_title_are_not_extra_characters():
    from app.services.local_semantic_lexicon import title_hints
    groups = [{'work': '울트라맨', 'aliases': ['울트라맨'], 'title_is_character': True,
               'characters': [['ウルトラマン|울트라맨', '울트라맨'], ['ゴモラ|고모라', '고모라']]},
              {'work': '괴수 8호', 'aliases': ['怪獣8号', '괴수 8호'], 'title_is_character': True,
               'characters': [['怪獣8号|괴수 8호', '괴수 8호'], ['古橋伊春', '후루하시 이하루']]}]
    def chars(title, work):
        ground = {'franchise': {'original': work, 'ko': work, 'evidence_field': 'name_original', 'evidence': work},
                  'characters': [], 'figure_form': None}
        title_hints({'name_original': title}, ground, groups)
        return [c['ko'] for c in ground['characters']]
    assert chars('울트라맨 시리즈 진좌수 고대괴수 고모라(ver.A)', '울트라맨') == ['고모라']
    assert chars('S.H.피규아트 (진골조제법) 울트라맨', '울트라맨') == ['울트라맨']
    assert chars('怪獣8号 古橋伊春【再販】', '괴수 8호') == ['후루하시 이하루']
    assert chars('괴수 8호 그란디스타 괴수 8호', '괴수 8호') == ['괴수 8호']


def test_box_with_work_needs_no_character_but_single_pick_does():
    from app.services.semantic_rules import assortment_without_character
    def fields():
        return {'franchise_ko': '원피스', 'character_ko': None, 'figure_form': 'prize_figure', 'missing_fields': ['character_ko'],
                'field_status': {'name_ko': 'ready', 'franchise_ko': 'ready', 'character_ko': 'missing', 'figure_form': 'ready'},
                'classification_status': 'partial'}
    box = assortment_without_character({'name_original': 'バディコレ 呪術廻戦【再販】'}, fields())
    assert box['field_status']['character_ko'] == 'not_applicable' and box['classification_status'] == 'ready'
    numbered = assortment_without_character({'name_original': '원피스 DXF 더 그랜드라인 레이디 와노쿠니 VOL.11'}, fields())
    assert numbered['field_status']['character_ko'] == 'missing'  # one figure per number; its character is unknown
    only_work = {**fields(), 'evidence': {'franchise': {'original': 'ONE PIECE'}}}
    assert assortment_without_character({'name_original': 'ONE PIECE【再販】'}, only_work)['classification_status'] == 'ready'
    assert assortment_without_character({'name_original': 'ワンピース 缶バッジコレクション'}, fields())['classification_status'] == 'ready'
    pick = assortment_without_character({'name_original': '귀멸의 칼날 피규어 VOL.27 (B:무라타)'}, fields())
    assert pick['field_status']['character_ko'] == 'missing'
    single = assortment_without_character({'name_original': 'ワンピース ねんどろいど'}, fields())
    assert single['classification_status'] == 'partial'
    no_work = {**fields(), 'franchise_ko': None}
    assert assortment_without_character({'name_original': '缶バッジコレクション'}, no_work)['field_status']['character_ko'] == 'missing'


def test_collection_line_is_not_a_hero_character():
    from app.services.local_semantic_lexicon import title_hints
    groups = [{'work': '체인소 맨', 'aliases': ['체인소 맨'], 'title_is_character': True,
               'characters': [['チェンソーマン|체인소 맨', '체인소 맨']]}]
    ground = {'franchise': {'original': '체인소 맨', 'ko': '체인소 맨', 'evidence_field': 'name_original', 'evidence': '체인소 맨'},
              'characters': [], 'figure_form': None}
    title_hints({'name_original': '체인소 맨 CHAIN SPIRITS VOL.4'}, ground, groups)
    assert ground['characters'] == []


def test_verified_override_survives_source_refresh_only_while_proven():
    from app.services.verified_classification import merge_overrides
    override = {'franchise_ko': {'source_hash': 'old', 'value': '사카모토 데이즈', 'method': 'web_verified',
                                 'evidence': {'method': 'web_verified', 'references': [{'field': 'name_original', 'match': 'SAKAMOTO DAYS'}]}}}
    base = {'name_ko': '사카모토 데이즈 고양이', 'franchise_ko': None, 'character_ko': None, 'characters': [], 'figure_form': None,
            'evidence': {}, 'field_issues': {'franchise_ko': ['DOCUMENT_FRANCHISE_RELATION_NOT_CONFIRMED']}}
    kept = merge_overrides(base, {'classification_overrides': override}, 'new', {'name_original': 'SAKAMOTO DAYS CATS'})
    assert kept['franchise_ko'] == '사카모토 데이즈' and kept['classification_overrides']['franchise_ko']['source_hash'] == 'new'
    gone = merge_overrides(base, {'classification_overrides': override}, 'new', {'name_original': '別の商品'})
    assert gone['franchise_ko'] is None


def test_miku_work_is_its_own_character_unless_another_vocaloid_is_named():
    from app.services.semantic_rules import assortment_without_character
    def fields():
        return {'franchise_ko': '하츠네 미쿠', 'character_ko': None, 'characters': [], 'figure_form': 'scale_figure',
                'missing_fields': ['character_ko'], 'classification_status': 'partial',
                'evidence': {'franchise': {'original': '初音ミク', 'evidence_field': 'franchise', 'evidence': '初音ミク'}},
                'field_status': {'name_ko': 'ready', 'franchise_ko': 'ready', 'character_ko': 'missing', 'figure_form': 'ready'}}
    miku = assortment_without_character({'name_original': '2021春節Ver. 1/7スケールフィギュア'}, fields())
    assert miku['character_ko'] == '하츠네 미쿠' and miku['classification_status'] == 'ready'
    luka = assortment_without_character({'name_original': 'ねんどろいど 巡音ルカ V4X'}, fields())
    assert luka['character_ko'] is None

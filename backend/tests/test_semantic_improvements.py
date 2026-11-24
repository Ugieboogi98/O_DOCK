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

import copy
import json
from types import SimpleNamespace
from decimal import Decimal
import pytest
from sqlalchemy import create_engine, select, func
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from app.models.entities import Base, Manufacturer, Figure, FigureVariant, Favorite, Purchase, User
from app.models.semantics import ProductSemantics
from app.services.product_semantics import (
    source_of, source_hash, validate_result, save_record, current, Extractor, SemanticError)
from app.repositories.figures import list_figures


@pytest.fixture
def semdb():
    e = create_engine('sqlite://', connect_args={'check_same_thread': False}, poolclass=StaticPool)
    Base.metadata.create_all(e)
    with Session(e, expire_on_commit=False) as db:
        db.add(User(id=1, username='admin'))
        maker = Manufacturer(name='FuRyu', name_ko='후류', official_url='https://www.furyu.jp/')
        db.add(maker); db.flush()
        f = Figure(manufacturer_id=maker.id, official_url='https://example.com/itachi',
                   name_original='NARUTO-ナルト- 疾風伝 ぬーどるストッパーフィギュア うちはイタチ', type='figure')
        db.add(f); db.flush()
        v = FigureVariant(figure_id=f.id, variant_key='original')
        db.add(v); db.flush()
        db.add(Favorite(figure_id=f.id, user_id=1))
        db.add(Purchase(variant_id=v.id, user_id=1, amount=Decimal('12345'), purchased_on='2026-11-10', currency='KRW'))
        db.commit()
        yield db, f
    e.dispose()


def result():
    return {'name_ko': '나루토 질풍전 누들 스토퍼 피규어 우치하 이타치',
            'franchise': {'original': 'NARUTO-ナルト- 疾風伝', 'ko': '나루토 질풍전',
                          'evidence_field': 'name_original', 'evidence': 'NARUTO-ナルト- 疾風伝', 'confidence': .99},
            'characters': [{'original': 'うちはイタチ', 'ko': '우치하 이타치',
                            'evidence_field': 'name_original', 'evidence': 'うちはイタチ', 'confidence': .99}],
            'figure_form': None}


def record(f, r=None):
    source = source_of(f)
    return {'figure_id': f.id, 'source': source, 'source_hash': source_hash(source), 'model': 'fixture', 'result': r or result()}


def test_user_example(semdb):
    db, f = semdb
    fields, issues = validate_result(source_of(f), result())
    assert not issues
    assert fields['franchise_ko'] == '나루토 질풍전'
    assert fields['character_ko'] == '우치하 이타치'
    assert fields['figure_form_ko'] == '누들 스토퍼'


def test_unknown_fields_stay_unknown(semdb):
    _, f = semdb
    source = {**source_of(f), 'name_original': 'オリジナル フィギュア'}
    fields, issues = validate_result(source, {'name_ko': '오리지널 피규어', 'franchise': None, 'characters': [], 'figure_form': None})
    assert not issues
    assert fields['franchise_ko'] is None and fields['character_ko'] is None and fields['figure_form'] is None
    assert fields['classification_status'] == 'partial'
    assert fields['translation_status'] == 'ready'


@pytest.mark.parametrize('japanese,translated,expected', [
    ('フリーレン', '프리렌', '프리렌'), ('フェルン', '펀', '페른')])
def test_observed_omissions_recovered_from_curated_dictionary(semdb, japanese, translated, expected):
    _, f = semdb
    source = {**source_of(f), 'name_original': 'TENITOL TALL ' + japanese + ' クラシカルワンピースver.'}
    r = {'name_ko': 'TENITOL TALL ' + translated + ' 클래식 원피스ver.', 'franchise': None, 'characters': [], 'figure_form': None}
    fields, issues = validate_result(source, r)
    assert not issues
    assert fields['character_ko'] == expected
    assert expected in fields['name_ko']
    assert fields['franchise_ko'] == '장송의 프리렌'
    assert fields['figure_form'] is None  # A brand/line or dress does not demonstrate a physical form.
    assert fields['missing_fields'] == ['figure_form']
    assert fields['classification_status'] == 'partial'
    assert fields['evidence']['franchise']['reference_urls']


def test_franchise_title_does_not_add_protagonist_as_character(semdb):
    _, f = semdb
    source = {**source_of(f), 'name_original': '葬送のフリーレン フェルン フィギュア'}
    fields, issues = validate_result(source, {'name_ko': '장송의 프리렌 페른 피규어', 'franchise': None, 'characters': [], 'figure_form': None})
    assert not issues
    assert fields['character_ko'] == '페른'


def test_partial_result_is_stored_searchable_and_honestly_labeled(semdb):
    db, f = semdb
    f.name_original = 'TENITOL TALL フェルン クラシカルワンピースver.'; db.commit()
    r = {'name_ko': 'TENITOL TALL 펀 클래식 원피스ver.', 'franchise': None, 'characters': [], 'figure_form': None}
    assert save_record(db, record(f, r)) == 'partial'
    assert current(db, f).status == 'partial'
    item = list_figures(db, character='페른')['items'][0]
    assert item['semantic_status'] == 'partial'
    assert item['franchise_ko'] == '장송의 프리렌'
    assert '페른' in f.name_ko


@pytest.mark.parametrize('mutation', ['invented', 'low_confidence', 'japanese', 'wrong_form', 'extra_key'])
def test_invalid_output_is_reviewed(semdb, mutation):
    db, f = semdb
    r = result()
    if mutation == 'invented': r['characters'][0]['evidence'] = '架空のキャラクター'
    elif mutation == 'low_confidence': r['franchise']['confidence'] = .3
    elif mutation == 'japanese': r['name_ko'] = '나루토 イタチ'
    elif mutation == 'wrong_form': r['figure_form'] = {'code': 'nendoroid', 'evidence_field': 'name_original', 'evidence': 'うちはイタチ', 'confidence': 1}
    else: r['manufacturer'] = 'Other'
    status = save_record(db, record(f, r))
    if mutation == 'extra_key':
        assert status == 'review'
        assert f.name_ko is None
        assert current(db, f) is None
        return
    rejected = {'invented': 'character_ko', 'low_confidence': 'franchise_ko',
                'japanese': 'name_ko', 'wrong_form': 'figure_form'}[mutation]
    assert status == 'partial'
    p = current(db, f)
    assert p.fields['field_status'][rejected] == 'review'
    assert p.fields[rejected] is None
    assert p.fields['field_issues'][rejected]
    assert (f.name_ko is None) == (rejected == 'name_ko')
    if rejected == 'character_ko':
        assert p.fields['characters'] == []
        assert list_figures(db, character='이타치')['total'] == 0
    elif rejected == 'figure_form':
        assert list_figures(db, figure_form='nendoroid')['total'] == 0
        assert list_figures(db, character='이타치')['total'] == 1


def test_numeric_scale_preservation(semdb):
    _, f = semdb
    source = {**source_of(f), 'name_original': 'テスト １／７ フィギュア ver.2', 'scale': '1/7'}
    r = {'name_ko': '테스트 1/7 피규어 ver.2', 'franchise': None, 'characters': [],
         'figure_form': {'code': 'scale_figure', 'evidence_field': 'scale', 'evidence': '1/7', 'confidence': 1}}
    assert not validate_result(source, r)[1]
    r['name_ko'] = '테스트 1/8 피규어 ver.2'
    assert 'TITLE_NUMERIC_FACT_CHANGED' in validate_result(source, r)[1]


def test_save_preserves_original_personal_and_manual_korean(semdb):
    db, f = semdb
    original = f.name_original
    f.name_ko = '직접 정한 이름'; db.commit()
    item = record(f)
    save_record(db, item); save_record(db, item)
    assert f.name_original == original and f.name_ko == '직접 정한 이름'
    assert f.franchise is None and f.character is None
    from app.repositories.figures import card
    displayed = card(f)
    assert displayed['name_ko'] == '직접 정한 이름'
    assert displayed['semantic_name_ko'] == result()['name_ko']
    assert db.scalar(select(func.count()).select_from(ProductSemantics)) == 1
    assert db.scalar(select(func.count()).select_from(Favorite)) == 1
    assert db.scalar(select(Purchase.amount)) == Decimal('12345')


def test_changed_source_refuses_apply_and_stale_search(semdb):
    db, f = semdb
    item = record(f); save_record(db, item)
    f.name_original = '別の商品'; db.commit()
    assert current(db, f) is None
    assert list_figures(db, franchise='나루토')['total'] == 0
    with pytest.raises(SemanticError, match='SOURCE_CHANGED_RETRY'):
        save_record(db, item)


def test_korean_search_and_form_filter(semdb):
    db, f = semdb
    save_record(db, record(f))
    for filters in ({'q': '나루토 이타치'}, {'franchise': '나루토'}, {'character': '이타치'}, {'figure_form': 'noodle_stopper'}):
        page = list_figures(db, **filters)
        assert page['total'] == 1
        assert page['items'][0]['figure_form_ko'] == '누들 스토퍼'
    assert list_figures(db, figure_form='nendoroid')['total'] == 0
    assert list_figures(db, figure_form='noodle')['total'] == 0
    assert list_figures(db, q='%')['total'] == 0


def test_detail_and_franchise_api(semdb):
    from app.main import app
    from app.core.database import get_db
    db, f = semdb
    save_record(db, record(f))
    app.dependency_overrides[get_db] = lambda: db
    try:
        with TestClient(app) as client:
            detail = client.get('/api/figures/' + str(f.id)).json()
            assert detail['character_ko'] == '우치하 이타치'
            assert detail['manufacturer_ko'] == '후류'
            groups = client.get('/api/franchises').json()
            assert groups['items'] == [{'name': '나루토 질풍전', 'count': 1}]
            assert client.get(f'/api/figures/{f.id}/semantics').json()['status'] == 'ready'
    finally:
        app.dependency_overrides.clear()


def test_field_rejection_is_consistent_in_api_groups_and_legacy_search(semdb):
    from app.main import app
    from app.core.database import get_db
    from app.models.korean import KoreanProfile
    db, f = semdb
    r = result()
    r['franchise']['confidence'] = .1
    save_record(db, record(f, r))
    db.add(KoreanProfile(figure_id=f.id, source_hash='old', model='old',
                         fields={'franchise_ko': '잘못된작품'}))
    db.commit()
    assert list_figures(db, franchise='잘못된작품')['total'] == 0
    assert list_figures(db, q='잘못된작품')['total'] == 0
    assert list_figures(db, character='이타치')['total'] == 1
    app.dependency_overrides[get_db] = lambda: db
    try:
        with TestClient(app) as client:
            data = client.get(f'/api/figures/{f.id}').json()
            assert data['semantic_field_status']['franchise_ko'] == 'review'
            assert data['franchise_ko'] is None
            assert data['character_ko'] == '우치하 이타치'
            assert client.get('/api/franchises').json()['items'] == []
            semantic = client.get(f'/api/figures/{f.id}/semantics').json()
            assert semantic['fields']['field_issues']['franchise_ko']
    finally:
        app.dependency_overrides.clear()


def test_all_fields_rejected_remain_unpublished(semdb):
    db, f = semdb
    r = {'name_ko': '日本語', 'franchise': {'bad': True},
         'characters': None, 'figure_form': {'bad': True}}
    assert save_record(db, record(f, r)) == 'review'
    assert current(db, f) is None
    assert f.name_ko is None


def test_page_cards_batch_reads_without_changing_single_card_output(semdb):
    from sqlalchemy import event
    from app.models.entities import ProductImage
    from app.repositories.figures import card
    db, first = semdb
    figures = [first]
    for i in range(8):
        f = Figure(manufacturer_id=first.manufacturer_id, name_original=f'商品 {i}',
                   official_url=f'https://example.com/batch/{i}')
        db.add(f)
        db.flush()
        db.add(FigureVariant(figure_id=f.id, variant_key='main'))
        figures.append(f)
    db.commit()
    for f in figures:
        db.add(ProductImage(variant_id=f.variants[0].id, image_url='https://example.com/hidden.jpg',
                            source_url='https://example.com/hidden.jpg', usage_status='duplicate_hidden'))
        db.add(ProductImage(variant_id=f.variants[0].id, image_url=f'https://example.com/{f.id}.jpg',
                            source_url=f'https://example.com/{f.id}.jpg', usage_status='authorized'))
    db.commit()
    save_record(db, record(first))
    expected = [card(f, favorite=f.id == first.id) for f in figures]
    statements = []

    def count(conn, cursor, statement, parameters, context, many):
        statements.append(statement)

    event.listen(db.get_bind(), 'before_cursor_execute', count)
    try:
        page = list_figures(db, page_size=24, user_id=1)
    finally:
        event.remove(db.get_bind(), 'before_cursor_execute', count)
    assert page['items'] == expected
    assert len(statements) <= 9
    assert page['items'][0]['favorite'] is True
    assert all(not item['favorite'] for item in page['items'][1:])
    assert all('hidden' not in item['thumbnail'] for item in page['items'])


def fake_extractor(response=None, error=None):
    def request(**kwargs):
        if error:
            raise error
        return SimpleNamespace(choices=[SimpleNamespace(finish_reason='stop', message=SimpleNamespace(content=response))])
    ex = object.__new__(Extractor)
    ex.model, ex.mode, ex.interval, ex.last = 'test', 'chat', 0, 0
    ex.client = SimpleNamespace(chat=SimpleNamespace(completions=SimpleNamespace(create=request)))
    return ex


def test_provider_json_parsing(semdb):
    _, f = semdb
    assert fake_extractor(json.dumps(result()))(source_of(f)) == result()
    with pytest.raises(SemanticError, match='INVALID_MODEL_JSON'):
        fake_extractor('not JSON')(source_of(f))


def test_quota_error_stops_without_retry(semdb):
    _, f = semdb
    e = RuntimeError('hidden provider body')
    e.code = 'insufficient_quota'
    with pytest.raises(SemanticError, match='QUOTA_EXHAUSTED'):
        fake_extractor(error=e)(source_of(f))


def test_cli_preview_apply_and_cached_resume(semdb, tmp_path, monkeypatch):
    import sys
    from sqlalchemy.orm import sessionmaker
    from scripts.product_semantics import main
    import app.core.database as database
    import app.core.config as config
    import app.services.product_semantics as service
    db, f = semdb
    monkeypatch.setattr(database, 'SessionLocal', sessionmaker(db.get_bind(), expire_on_commit=False))
    monkeypatch.setattr(config, 'get_settings', lambda: SimpleNamespace(llm_api_key='fixture', llm_model='fixture', llm_api_mode='chat', media_dir=tmp_path))
    calls = []
    class Fake:
        model = 'fixture'
        def __call__(self, source):
            calls.append(source)
            return result()
    monkeypatch.setattr(service, 'Extractor', Fake)
    path = tmp_path / 'preview.json'
    monkeypatch.setattr(sys, 'argv', ['semantics', 'run', '--limit', '1', '--report', str(path)])
    main()
    db.expire_all()
    assert db.get(ProductSemantics, f.id) is None
    assert len(calls) == 1

    assert json.loads(path.read_text())['summary']['ready'] == 1
    monkeypatch.setattr(sys, 'argv', ['semantics', 'apply', '--report', str(path)])
    main()
    db.expire_all()
    assert db.get(ProductSemantics, f.id).status == 'ready'
    assert len(calls) == 1  # Apply reuses saved output, no second model call.
    monkeypatch.setattr(sys, 'argv', ['semantics', 'run', '--limit', '1', '--report', str(tmp_path/'cached.json')])
    main()
    assert len(calls) == 1


def test_cli_queued_preview_apply_and_resume(semdb, tmp_path, monkeypatch):
    import sys
    from sqlalchemy.orm import sessionmaker
    from scripts.product_semantics import main
    import app.core.database as database
    import app.services.product_semantics as service
    from app.services.semantic_queue import enqueue, pending_jobs
    db, f = semdb
    enqueue(db, f)
    db.add(Figure(manufacturer_id=f.manufacturer_id, name_original='NOT QUEUED',
                  official_url='https://example.com/not-queued'))
    db.commit()
    monkeypatch.setattr(database, 'SessionLocal', sessionmaker(db.get_bind(), expire_on_commit=False))
    calls = []

    class Fake:
        model = 'fixture'
        def __call__(self, source):
            calls.append(source)
            return result()

    monkeypatch.setattr(service, 'Extractor', Fake)
    path = tmp_path / 'queued.json'
    monkeypatch.setattr(sys, 'argv', ['semantics', 'pending', '--limit', '1'])
    main()
    assert not calls
    monkeypatch.setattr(sys, 'argv', ['semantics', 'run', '--queued', '--limit', '1', '--report', str(path)])
    main()
    assert len(calls) == 1
    assert calls[0]['name_original'] == f.name_original
    assert len(pending_jobs(db)) == 1  # Preview does not consume work.
    monkeypatch.setattr(sys, 'argv', ['semantics', 'apply', '--report', str(path)])
    main()
    db.expire_all()
    assert not pending_jobs(db)
    monkeypatch.setattr(sys, 'argv', ['semantics', 'run', '--queued', '--limit', '1', '--report', str(tmp_path / 'empty.json')])
    main()
    assert len(calls) == 1

def test_recheck_reuses_v1_model_output_without_api_or_db_writes(semdb, tmp_path, monkeypatch):
    import sys
    from sqlalchemy.orm import sessionmaker
    from scripts.product_semantics import main
    import app.core.database as database
    import app.services.product_semantics as service
    db, f = semdb
    f.name_original = 'TENITOL TALL フェルン クラシカルワンピースver.'; db.commit()
    source = source_of(f); source['_rules_hash'] = 'previous-version'
    r = {'name_ko': 'TENITOL TALL 펀 클래식 원피스ver.', 'franchise': None, 'characters': [], 'figure_form': None}
    before = {'records': [{'figure_id': f.id, 'source': source, 'source_hash': 'v1hash', 'model': 'saved', 'result': r}]}
    input_path, output_path = tmp_path/'old.json', tmp_path/'new.json'
    input_path.write_text(json.dumps(before), encoding='utf-8')
    monkeypatch.setattr(database, 'SessionLocal', sessionmaker(db.get_bind(), expire_on_commit=False))
    def forbidden():
        raise AssertionError('Recheck must not call the provider')
    monkeypatch.setattr(service, 'Extractor', forbidden)
    monkeypatch.setattr(sys, 'argv', ['semantics', 'recheck', '--report', str(input_path), '--output', str(output_path)])
    main()
    updated = json.loads(output_path.read_text())
    assert updated['paid_api_called'] is False
    assert updated['summary']['partial'] == 1
    assert updated['records'][0]['fields']['character_ko'] == '페른'
    assert json.loads(input_path.read_text()) == before
    assert db.get(ProductSemantics, f.id) is None

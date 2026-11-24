import copy
from types import SimpleNamespace
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from app.models.entities import Base, Figure, Manufacturer
from app.models.semantics import ProductSemantics
from app.services.product_semantics import source_of, source_hash, save_record
from app.services.verified_classification import apply_record, merge_overrides


@pytest.fixture
def catalog():
    engine = create_engine('sqlite://')
    Base.metadata.create_all(engine)
    with Session(engine, expire_on_commit=False) as db:
        maker = Manufacturer(name='Example', name_ko='예시', official_url='https://example.com')
        db.add(maker)
        db.flush()
        f = Figure(manufacturer_id=maker.id, name_original='BLEACH 黒崎一護 1/7',
                   name_ko='사용자 지정 이름', official_url='https://example.com/1', type='figure')
        db.add(f)
        db.commit()
        yield db, f


def record(f):
    return {'figure_id': f.id, 'source_hash': source_hash(source_of(f)), 'approved': True,
        'method': 'web_verified', 'patch': {'franchise_ko': '블리치'},
        'proofs': {'franchise_ko': [{'field': 'name_original', 'match': 'BLEACH',
            'reference_url': 'https://bleach-anime.com/character/', 'reference_evidence': 'BLEACH',
            'checked_at': '2026-11-11T00:00:00Z'}]}}


def test_verified_classification_survives_model_save(catalog):
    db, f = catalog
    web = record(f)
    apply_record(db, web)
    db.commit()
    source = source_of(f)
    save_record(db, {'figure_id': f.id, 'source': source, 'source_hash': source_hash(source), 'model': 'test',
        'result': {'name_ko': '블리치 쿠로사키 이치고 1/7', 'franchise': None, 'characters': [], 'figure_form': None}})
    assert db.get(ProductSemantics, f.id).fields['franchise_ko'] == '블리치'
    assert f.name_ko == '사용자 지정 이름'


def test_source_change_rejects_old_confirmation(catalog):
    db, f = catalog
    web = record(f)
    f.name_original = 'changed'
    db.commit()
    with pytest.raises(RuntimeError, match='SOURCE_CHANGED_RETRY'):
        apply_record(db, web)


def test_web_proof_requires_literal_input_match(catalog):
    db, f = catalog
    web = record(f)
    web['proofs']['franchise_ko'][0]['match'] = 'not in product'
    with pytest.raises(RuntimeError, match='INVALID_WEB_PROOF'):
        apply_record(db, web)


def test_manual_decision_has_priority_over_web(catalog):
    db, f = catalog
    user = record(f)
    user['method'], user['patch']['franchise_ko'] = 'manual_verified', '사용자 확인 작품명'
    apply_record(db, user)
    db.commit()
    apply_record(db, record(f))
    db.commit()
    assert db.get(ProductSemantics, f.id).fields['franchise_ko'] == '사용자 확인 작품명'


def test_not_applicable_is_not_unknown(catalog):
    db, f = catalog
    user = record(f)
    user.update(method='manual_verified', patch={'franchise_ko': None}, not_applicable_fields=['franchise_ko'])
    apply_record(db, user)
    fields = db.get(ProductSemantics, f.id).fields
    assert fields['field_status']['franchise_ko'] == 'not_applicable'
    assert 'franchise_ko' not in fields['missing_fields']


def test_unapproved_input_cannot_publish(catalog):
    db, f = catalog
    user = record(f)
    user['approved'] = False
    with pytest.raises(RuntimeError, match='CLASSIFICATION_APPROVAL_REQUIRED'):
        apply_record(db, user)


def test_cached_reference_enrichment_joins_model_transaction(catalog, monkeypatch):
    db, f = catalog
    import app.core.config as config
    import app.services.reference_classifier as references
    monkeypatch.setattr(config, 'get_settings', lambda: SimpleNamespace(semantic_reference_enrichment=True))
    monkeypatch.setattr(references, 'cached_record', lambda *args: record(f))
    source = source_of(f)
    generated = {'figure_id': f.id, 'source': source, 'source_hash': source_hash(source), 'model': 'test',
        'result': {'name_ko': '블리치 쿠로사키 이치고 1/7', 'franchise': None, 'characters': [], 'figure_form': None}}
    save_record(db, generated)
    assert db.get(ProductSemantics, f.id).fields['franchise_ko'] == '블리치'
    assert generated['reference_enrichment'] is True

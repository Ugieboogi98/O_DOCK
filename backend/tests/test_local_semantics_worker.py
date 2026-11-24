from types import SimpleNamespace
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.models.entities import Base, Manufacturer, Figure
from app.models.semantics import ProductSemantics
from app.services.semantic_queue import enqueue, pending_jobs
from scripts import local_semantics_worker as worker


@pytest.fixture
def queued(monkeypatch, tmp_path):
    engine = create_engine('sqlite://', poolclass=StaticPool, connect_args={'check_same_thread': False})
    Base.metadata.create_all(engine)
    factory = sessionmaker(engine, expire_on_commit=False)
    with factory() as db:
        maker = Manufacturer(name='Example', name_ko='예시', official_url='https://example.com')
        db.add(maker)
        db.flush()
        f = Figure(manufacturer_id=maker.id, name_original='フィギュア 77',
                   official_url='https://example.com/77', type='figure')
        db.add(f)
        db.flush()
        enqueue(db, f)
        db.commit()
        fid = f.id
    monkeypatch.setattr(worker, 'SessionLocal', factory)
    monkeypatch.setattr(worker, 'get_settings', lambda: SimpleNamespace(semantic_provider='ollama'))
    return factory, fid, tmp_path


def test_remote_provider_cannot_consume_queue(monkeypatch, tmp_path):
    monkeypatch.setattr(worker, 'get_settings', lambda: SimpleNamespace(semantic_provider='remote'))
    with pytest.raises(RuntimeError, match='NO_PAID_FALLBACK'):
        worker.consume(1, tmp_path)


def test_local_result_commits_and_finishes_job(queued, monkeypatch):
    factory, fid, root = queued
    class Extractor:
        model = 'ollama:fixture'
        metadata = {'digest': 'fixture'}
        def __call__(self, source):
            return {'name_ko': '피규어 77', 'franchise': None, 'characters': [], 'figure_form': None}
    monkeypatch.setattr(worker, 'Extractor', Extractor)
    assert worker.consume(1, root)['committed'] == 1
    with factory() as db:
        assert not pending_jobs(db)
        assert db.get(Figure, fid).name_ko == '피규어 77'
        assert db.get(ProductSemantics, fid).model == 'ollama:fixture'


def test_source_change_during_inference_cannot_publish_old_result(queued, monkeypatch):
    factory, fid, root = queued
    class Extractor:
        model = 'ollama:fixture'
        metadata = {}
        def __call__(self, source):
            with factory() as db:
                f = db.get(Figure, fid)
                f.name_original = 'フィギュア 78'
                enqueue(db, f)
                db.commit()
            return {'name_ko': '피규어 77', 'franchise': None, 'characters': [], 'figure_form': None}
    monkeypatch.setattr(worker, 'Extractor', Extractor)
    with pytest.raises(RuntimeError, match='SOURCE_CHANGED_RETRY'):
        worker.consume(1, root)
    with factory() as db:
        assert db.get(ProductSemantics, fid) is None
        assert len(pending_jobs(db)) == 1

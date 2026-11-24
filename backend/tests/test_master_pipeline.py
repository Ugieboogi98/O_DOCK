"""One-click pipeline orchestration without network, Ollama or Meta calls."""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import get_settings
from app.core.database import get_db
from app.models.entities import Base, CollectionJob
from app.services import master_pipeline as mp

TOKEN = 'fixture-admin-token-0123456789'


@pytest.fixture
def sessions(monkeypatch):
    engine = create_engine('sqlite://', connect_args={'check_same_thread': False},
                           poolclass=__import__('sqlalchemy.pool', fromlist=['StaticPool']).StaticPool)
    Base.metadata.create_all(engine)
    factory = sessionmaker(bind=engine, expire_on_commit=False)
    monkeypatch.setattr(mp, 'SessionLocal', factory)
    monkeypatch.setattr(mp, '_running', False)
    from contextlib import nullcontext
    from app.services import worker_lock
    monkeypatch.setattr(worker_lock, 'advisory_lock', lambda name, engine=None: nullcontext())
    yield factory
    engine.dispose()


def fake(state, **info):
    return lambda ctx: (state, info)


def test_runs_every_step_in_order_and_records_each(sessions, monkeypatch):
    order = []
    def step(name, state):
        def run(ctx):
            order.append(name)
            return state, {'note': name}
        return run
    monkeypatch.setattr(mp, 'RUNNERS', {'catalog': step('catalog', 'completed'), 'semantics': step('semantics', 'completed'),
                                        'events': step('events', 'skipped'), 'verify': step('verify', 'completed')})
    result = mp.start(background=False)
    assert order == ['catalog', 'semantics', 'events', 'verify']
    assert result['state'] == 'partial'  # one step skipped
    assert [s['state'] for s in result['steps']] == ['completed', 'completed', 'skipped', 'completed']
    assert result['steps'][0]['label'] == '신상품 수집'


def test_failing_step_does_not_stop_the_rest(sessions, monkeypatch):
    def boom(ctx):
        raise RuntimeError('secret detail')
    monkeypatch.setattr(mp, 'RUNNERS', {'catalog': boom, 'semantics': fake('completed'),
                                        'events': fake('completed'), 'verify': fake('completed')})
    result = mp.start(background=False)
    assert result['steps'][0] == {**result['steps'][0], 'state': 'failed', 'reason': 'RuntimeError'}
    assert 'secret detail' not in str(result)
    assert [s['state'] for s in result['steps'][1:]] == ['completed'] * 3


def test_selected_steps_only(sessions, monkeypatch):
    monkeypatch.setattr(mp, 'RUNNERS', {k: fake('completed') for k in mp.STEPS})
    result = mp.start(['events', 'verify'], background=False)
    assert result['state'] == 'completed'
    assert [s['state'] for s in result['steps']] == ['not_requested', 'not_requested', 'completed', 'completed']
    with pytest.raises(ValueError):
        mp.start(['nothing'], background=False)


def test_second_start_while_running_is_refused(sessions, monkeypatch):
    monkeypatch.setattr(mp, '_running', True)
    assert mp.start(background=False)['reason'] == 'already_running'


def test_stale_running_job_is_reported_interrupted(sessions):
    from datetime import datetime, timedelta, timezone
    with sessions() as db:
        db.add(CollectionJob(collector=mp.COLLECTOR, status='running', count=0, error_summary='{}',
                             started_at=datetime.now(timezone.utc) - timedelta(hours=7)))
        db.commit()
    assert mp.status()['state'] == 'interrupted'


def test_semantics_skips_without_ollama(monkeypatch):
    monkeypatch.setattr(mp, 'ollama_ready', lambda *a: 'OLLAMA_UNREACHABLE')
    state, info = mp.step_semantics({})
    assert state == 'skipped' and info['reason'] == 'OLLAMA_UNREACHABLE'


def test_events_skip_without_meta_credentials(monkeypatch):
    from app.integrations.instagram import config
    monkeypatch.setattr(config.InstagramSettings, 'from_local_env', classmethod(lambda cls, path=None: cls(_env_file=None)))
    for key in ('META_ACCESS_TOKEN', 'META_IG_USER_ID'):
        monkeypatch.delenv(key, raising=False)
    assert mp.step_events({}) == ('skipped', {'reason': 'META_NOT_CONFIGURED'})


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(get_settings(), 'admin_token', TOKEN)
    app.dependency_overrides[get_db] = lambda: None
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def test_pipeline_endpoints_are_admin_only(client, monkeypatch):
    calls = []
    monkeypatch.setattr(mp, 'start', lambda steps=None: calls.append(steps) or {'state': 'running'})
    monkeypatch.setattr(mp, 'status', lambda: {'state': 'never'})
    for headers in ({}, {'X-Admin-Token': 'wrong-token-wrong-token-000'}):
        assert client.post('/api/admin/pipeline/run', json={}, headers=headers).status_code == 403
        assert client.get('/api/admin/pipeline', headers=headers).status_code == 403
    assert calls == []
    ok = {'X-Admin-Token': TOKEN}
    assert client.post('/api/admin/pipeline/run', json={'steps': ['events']}, headers=ok).json() == {'state': 'running'}
    assert client.post('/api/admin/pipeline/run', headers=ok).status_code == 200
    assert calls == [['events'], None]
    assert client.post('/api/admin/pipeline/run', json={'steps': ['drop']}, headers=ok).status_code == 422
    assert client.post('/api/admin/pipeline/run', json={}, headers={**ok, 'Origin': 'https://evil.example'}).status_code == 403
    assert client.get('/api/admin/pipeline', headers=ok).json() == {'state': 'never'}

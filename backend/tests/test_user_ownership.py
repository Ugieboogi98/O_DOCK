import hashlib
import importlib.util
from pathlib import Path
from datetime import timedelta
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, event, select
from sqlalchemy.orm import sessionmaker
from alembic.migration import MigrationContext
from alembic.operations import Operations
from app.main import app
from app.core.database import get_db
from app.core.config import get_settings
from app.models.entities import Base, User, UserSession, Manufacturer, Figure, FigureVariant, Purchase, now
from app.services.accounts import COOKIE


@pytest.fixture
def setup(tmp_path, monkeypatch):
    engine = create_engine('sqlite:///' + str(tmp_path / 'users.db'), connect_args={'check_same_thread':False})
    @event.listens_for(engine, 'connect')
    def fk(conn, _):
        conn.execute('PRAGMA foreign_keys=ON')
    Base.metadata.create_all(engine)
    factory = sessionmaker(engine, expire_on_commit=False)
    with factory() as db:
        db.add(User(id=1, username='admin'))
        maker = Manufacturer(name='Maker', name_ko='제작사', official_url='https://example.com')
        db.add(maker); db.flush()
        f = Figure(manufacturer_id=maker.id, name_original='상품', official_url='https://example.com/1')
        db.add(f); db.flush()
        v = FigureVariant(figure_id=f.id, variant_key='main')
        db.add(v); db.commit()
        ids = (f.id, v.id)
    def dependency():
        with factory() as db:
            yield db
    app.dependency_overrides[get_db] = dependency
    monkeypatch.setattr(get_settings(), 'admin_token', 'fixture-admin-token-0123456789')
    yield factory, ids
    app.dependency_overrides.clear()
    engine.dispose()


def register(c, name):
    r = c.post('/api/auth/register', json={'username':name, 'password':'fixture-password-123'})
    assert r.status_code == 200, r.text
    assert 'HttpOnly' in r.headers['set-cookie']
    assert 'SameSite=lax' in r.headers['set-cookie']
    assert 'Path=/api' in r.headers['set-cookie']
    return r.json()


def test_two_users_cannot_read_or_modify_each_others_records(setup):
    factory, (fid, vid) = setup
    with TestClient(app) as a, TestClient(app) as b, TestClient(app) as anon:
        ua, ub = register(a, 'alice'), register(b, 'bob')
        for client in (a,b):
            assert client.put(f'/api/favorites/{fid}').status_code == 200
            assert len(client.get('/api/favorites').json()) == 1
        assert a.delete(f'/api/favorites/{fid}').status_code == 200
        assert a.get('/api/favorites').json() == []
        assert len(b.get('/api/favorites').json()) == 1
        assert a.get(f'/api/figures/{fid}').json()['favorite'] is False
        assert b.get(f'/api/figures/{fid}').json()['favorite'] is True
        assert anon.get(f'/api/figures/{fid}').json()['favorite'] is False
        assert anon.get('/api/favorites').status_code == 401
        assert anon.get('/api/purchases').status_code == 401
        assert anon.put(f'/api/favorites/{fid}').status_code == 401
        body = {'variant_id':vid, 'amount':'1000', 'purchased_on':'2026-01-01'}
        record = a.post('/api/purchases', json=body).json()
        assert b.get('/api/purchases').json() == []
        assert b.put('/api/purchases/'+str(record['id']), json=body).status_code == 404
        assert b.delete('/api/purchases/'+str(record['id'])).status_code == 404
        assert a.get('/api/purchases').json()[0]['id'] == record['id']
        with TestClient(app, headers={'X-Admin-Token':'fixture-admin-token-0123456789'}) as admin:
            # The operator token is not a personal identity.
            assert admin.get('/api/purchases').status_code == 401
            assert admin.delete('/api/purchases/'+str(record['id'])).status_code == 401
            assert admin.get('/api/auth/me').json() == {'user': None}
        assert a.post('/api/purchases', json={**body, 'user_id':ub['id']}).json()['user_id'] == ua['id']
        assert b.post('/api/catalog/refresh').status_code == 403


def test_session_expiry_logout_csrf_and_password_storage(setup):
    factory, _ = setup
    with TestClient(app) as c:
        user = register(c, 'alice')
        token = c.cookies.get(COOKIE)
        with factory() as db:
            row = db.get(User, user['id'])
            assert 'fixture-password-123' not in row.password_hash
            session = db.get(UserSession, hashlib.sha256(token.encode()).hexdigest())
            assert session and session.token_hash != token
        assert c.get('/api/auth/me').json()['user']['id'] == user['id']
        assert c.get('/api/purchases').headers['cache-control'] == 'no-store'
        assert c.post('/api/auth/logout', headers={'Origin':'https://other.example'}).status_code == 403
        assert c.post('/api/auth/logout').status_code == 200
        assert c.get('/api/purchases').status_code == 401
        c.cookies.set(COOKIE, token)
        assert c.get('/api/purchases').status_code == 401  # Server-side revocation.
        c.cookies.clear()
        assert c.post('/api/auth/login', json={'username':'ALICE','password':'fixture-password-123'}).status_code == 200
        token = c.cookies.get(COOKIE)
        with factory() as db:
            session = db.get(UserSession, hashlib.sha256(token.encode()).hexdigest())
            session.expires_at = now()-timedelta(seconds=1)
            db.commit()
        assert c.get('/api/purchases').status_code == 401


def test_registration_cannot_claim_admin_and_password_failures_are_bounded(setup):
    with TestClient(app) as c:
        assert c.post('/api/auth/register',json={'username':'admin','password':'fixture-password-123'}).status_code == 409
        assert c.post('/api/auth/register',json={'username':'alice','password':'fixture-password-123','is_admin':True}).status_code == 422
        register(c,'alice')
        assert c.post('/api/auth/register',json={'username':'Alice','password':'fixture-password-123'}).status_code == 409
        for _ in range(5):
            assert c.post('/api/auth/login',json={'username':'alice','password':'wrong-password-123'}).status_code == 401
        assert c.post('/api/auth/login',json={'username':'alice','password':'fixture-password-123'}).status_code == 429


def test_ownership_migration_preserves_legacy_ids_and_values():
    path = Path(__file__).parents[1]/'alembic/versions/20261110_users.py'
    spec = importlib.util.spec_from_file_location('users_revision',path)
    migration = importlib.util.module_from_spec(spec); spec.loader.exec_module(migration)
    engine = create_engine('sqlite://')
    with engine.begin() as conn:
        conn.exec_driver_sql('CREATE TABLE figures(id INTEGER PRIMARY KEY)')
        conn.exec_driver_sql('INSERT INTO figures VALUES(42)')
        conn.exec_driver_sql('CREATE TABLE favorites(figure_id INTEGER PRIMARY KEY REFERENCES figures(id),created_at DATETIME NOT NULL)')
        conn.exec_driver_sql("INSERT INTO favorites VALUES(42,'2026-01-01')")
        conn.exec_driver_sql('CREATE TABLE purchases(id INTEGER PRIMARY KEY,variant_id INTEGER,amount NUMERIC)')
        conn.exec_driver_sql('INSERT INTO purchases VALUES(77,12,12345)')
        with Operations.context(MigrationContext.configure(conn)):
            migration.upgrade()
        assert tuple(conn.exec_driver_sql('SELECT id,variant_id,amount,user_id FROM purchases').one()) == (77,12,12345,1)
        assert tuple(conn.exec_driver_sql('SELECT figure_id,created_at,user_id FROM favorites').one()) == (42,'2026-01-01',1)
        conn.exec_driver_sql("INSERT INTO users(id,username,failed_attempts,created_at) VALUES(2,'other',0,CURRENT_TIMESTAMP)")
        conn.exec_driver_sql("INSERT INTO favorites VALUES(42,'2026-01-02',2)")
        assert conn.exec_driver_sql('SELECT COUNT(*) FROM favorites').scalar() == 2
    engine.dispose()

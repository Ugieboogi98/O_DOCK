"""Catalog authorization checks without live DB, crawling or provider calls."""
import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException
from app.main import app
from app.core.database import get_db
from app.core.config import get_settings
from app.core.security import require_admin


@pytest.fixture
def client(monkeypatch):
    monkeypatch.setattr(get_settings(), 'admin_token', 'fixture-admin-token-0123456789')
    app.dependency_overrides[get_db] = lambda: None
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.mark.parametrize('method,path', [
    ('post', '/api/catalog/refresh'),
    ('put', '/api/figures/1/korean-name'),
    ('post', '/api/figures/1/translate'),
    ('post', '/api/korea-prices/preview'),
    ('post', '/api/korea-prices'),
    ('delete', '/api/korea-prices/1'),
    ('post', '/api/exchange-rate/refresh'),
    ('post', '/api/figures/1/prices/refresh'),
    ('post', '/api/figures/1/documents/refresh'),
    ('post', '/api/admin/reindex'),
    ('get', '/api/admin/collection-jobs'),
])
def test_catalog_mutations_require_token_before_handler(client, method, path):
    for headers in ({}, {'X-Admin-Token': 'wrong'}):
        assert client.request(method, path, json={}, headers=headers).status_code == 403


def test_verified_admin_can_refresh_and_public_can_read_progress(client, monkeypatch):
    from app.api import catalog_refresh as api
    calls = []
    monkeypatch.setattr(api, 'start_refresh', lambda: calls.append(True) or {'state': 'running'})
    monkeypatch.setattr(api, 'refresh_status', lambda: {'state': 'idle'})
    assert client.get('/api/catalog/status').status_code == 200
    assert not calls
    assert client.get('/api/admin/session').status_code == 403
    headers = {'X-Admin-Token': 'fixture-admin-token-0123456789'}
    assert client.get('/api/admin/session', headers=headers).json() == {'admin': True}
    assert not calls  # Authentication alone has no collection side effects.
    assert client.post('/api/catalog/refresh', headers=headers).json() == {'state': 'running'}
    assert calls == [True]


def test_missing_server_key_fails_closed(client, monkeypatch):
    monkeypatch.setattr(get_settings(), 'admin_token', '')
    assert client.get('/api/admin/session').status_code == 503
    assert client.post('/api/catalog/refresh').status_code == 503


def test_non_ascii_bad_token_is_rejected_without_server_error(monkeypatch):
    monkeypatch.setattr(get_settings(), 'admin_token', 'fixture-admin-token-0123456789')
    with pytest.raises(HTTPException) as error:
        require_admin('잘못된 토큰')
    assert error.value.status_code == 403

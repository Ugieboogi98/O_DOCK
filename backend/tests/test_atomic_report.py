import json
import pytest
from scripts import product_semantics as reports


def test_atomic_report_retries_transient_windows_lock(tmp_path, monkeypatch):
    target = tmp_path / 'progress.json'
    target.write_text('{"state":"old"}')
    replace = reports.os.replace
    calls = []
    def locked(source, destination):
        calls.append(destination)
        if len(calls) < 3:
            assert json.loads(target.read_text()) == {'state': 'old'}
            raise PermissionError('temporary reader lock')
        replace(source, destination)
    monkeypatch.setattr(reports.os, 'replace', locked)
    monkeypatch.setattr(reports.time, 'sleep', lambda _: None)
    reports.atomic_report(target, {'state': 'new'})
    assert len(calls) == 3
    assert json.loads(target.read_text()) == {'state': 'new'}
    assert not list(tmp_path.glob('.semantics-*'))


def test_atomic_report_permanent_lock_keeps_original(tmp_path, monkeypatch):
    target = tmp_path / 'progress.json'
    target.write_text('{"state":"old"}')
    def locked(*args):
        raise PermissionError('permanent lock')
    monkeypatch.setattr(reports.os, 'replace', locked)
    monkeypatch.setattr(reports.time, 'sleep', lambda _: None)
    with pytest.raises(PermissionError):
        reports.atomic_report(target, {'state': 'new'})
    assert json.loads(target.read_text()) == {'state': 'old'}
    assert not list(tmp_path.glob('.semantics-*'))

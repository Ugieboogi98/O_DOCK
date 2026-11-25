import json
import sys
import pytest
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.models.entities import Base, Manufacturer, Figure
from app.models.semantics import ProductSemantics
from app.services.semantic_errors import SemanticError
from scripts import complete_semantics as runner


@pytest.fixture
def catalog(monkeypatch, tmp_path):
    engine = create_engine('sqlite://', poolclass=StaticPool, connect_args={'check_same_thread': False})
    Base.metadata.create_all(engine)
    factory = sessionmaker(engine, expire_on_commit=False)
    with factory() as db:
        maker = Manufacturer(name='Example', name_ko='예시', official_url='https://example.com')
        db.add(maker)
        db.flush()
        db.add(Figure(id=10, manufacturer_id=maker.id, name_original='Example 77',
                      official_url='https://example.com/77', type='figure'))
        db.commit()
    monkeypatch.setattr(runner, 'SessionLocal', factory)
    monkeypatch.setattr(sys, 'argv', ['complete_semantics', '--commit', '--workers', '1', '--report-dir', str(tmp_path)])
    return factory, tmp_path


def test_resume_does_not_repeat_paid_request(catalog, monkeypatch):
    calls = []
    class Extractor:
        model = 'offline-test'
        def __call__(self, source):
            calls.append(source)
            return {'name_ko': '예시 77', 'franchise': None, 'characters': [], 'figure_form': None}
    monkeypatch.setattr(runner, 'Extractor', Extractor)
    runner.main()
    runner.main()
    factory, root = catalog
    assert len(calls) == 1
    with factory() as db:
        assert db.get(Figure, 10).name_ko == '예시 77'
        assert db.get(ProductSemantics, 10).fields['translation_status'] == 'ready'
    assert json.loads((root / 'progress.json').read_text())['counts'] == {'cached': 1}


def test_local_refresh_reprocesses_after_policy_changes(catalog,monkeypatch):
    from types import SimpleNamespace
    from app.core import config
    from app.services import local_semantic_lexicon
    monkeypatch.setattr(config,'get_settings',lambda:SimpleNamespace(semantic_provider='ollama'))
    version=['first'];calls=[]
    monkeypatch.setattr(local_semantic_lexicon,'fingerprint',lambda:version[0])
    class Extractor:
        model='ollama:offline@digest'
        def __call__(self,source):
            calls.append(source)
            return {'name_ko':'예시 77','franchise':None,'characters':[],'figure_form':None}
    monkeypatch.setattr(runner,'Extractor',Extractor)
    sys.argv.append('--refresh-local')
    runner.main();version[0]='second';runner.main()
    assert len(calls)==2
    _,root=catalog
    assert json.loads((root/'10.json').read_text())['processing_fingerprint']=='second'


def test_validation_retry_is_bounded_and_saved(catalog, monkeypatch):
    calls = []
    class Extractor:
        model = 'offline-test'
        def __call__(self, source):
            calls.append(source)
            return {'name_ko': 'Example Seventy-Seven' if len(calls) == 1 else '예시 77',
                    'franchise': None, 'characters': [], 'figure_form': None}
    monkeypatch.setattr(runner, 'Extractor', Extractor)
    runner.main()
    _, root = catalog
    record = json.loads((root / '10.json').read_text())
    assert len(calls) == 2
    assert '_validation_feedback' in calls[1]
    assert record['committed'] is True
    assert record['fields']['name_ko'] == '예시 77'


def test_quota_stops_without_catalog_write(catalog, monkeypatch):
    class Extractor:
        model = 'offline-test'
        def __call__(self, source):
            raise SemanticError('QUOTA_EXHAUSTED')
    monkeypatch.setattr(runner, 'Extractor', Extractor)
    with pytest.raises(SystemExit):
        runner.main()
    factory, root = catalog
    assert json.loads((root / 'progress.json').read_text())['state'] == 'blocked'
    with factory() as db:
        assert db.get(ProductSemantics, 10) is None
        assert db.get(Figure, 10).name_ko is None


def test_local_refresh_preserves_previous_and_resumes_committed_report(catalog, monkeypatch):
    from types import SimpleNamespace
    from app.core import config
    monkeypatch.setattr(config, 'get_settings', lambda: SimpleNamespace(semantic_provider='ollama'))
    calls = []
    class Extractor:
        model = 'ollama:offline@digest'
        metadata = {'provider': 'ollama'}
        def __call__(self, source):
            calls.append(source)
            return {'name_ko': '예시 77', 'franchise': None, 'characters': [], 'figure_form': None}
    monkeypatch.setattr(runner, 'Extractor', Extractor)
    runner.main()
    sys.argv.append('--refresh-local')
    factory, root = catalog
    (root / '10.json').unlink()
    runner.main()
    runner.main()
    record = json.loads((root / '10.json').read_text())
    assert len(calls) == 2
    assert record['previous_publication']['fields']['name_ko'] == '예시 77'
    assert record['paid_api_called'] is False
    assert json.loads((root / 'progress.json').read_text())['counts'] == {'resumed': 1}
    with factory() as db:
        assert db.get(Figure, 10).name_ko == '예시 77'

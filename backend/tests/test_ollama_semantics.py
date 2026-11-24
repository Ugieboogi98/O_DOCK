import json
from types import SimpleNamespace
import httpx
import pytest
from app.services.ollama_semantics import OllamaExtractor
from app.services.semantic_errors import SemanticError


def settings(tmp_path, **changes):
    return SimpleNamespace(semantic_base_url='http://localhost:11434', semantic_model='qwen3:8b',
        semantic_timeout=240, media_dir=tmp_path, **changes)


def install_transport(monkeypatch, *, reason='stop', digest='abc', result=None):
    import app.services.ollama_semantics as service
    calls = []
    actual = httpx.Client
    def handler(request):
        calls.append(request)
        if request.url.path == '/api/tags':
            data = {'models': [{'name': 'qwen3:8b', 'digest': digest[0] if isinstance(digest, list) else digest}]}
        elif request.url.path == '/api/version':
            data = {'version': 'test'}
        else:
            data = {'done': True, 'done_reason': reason, 'message': {'content': json.dumps(result or {
                'name_ko': '나루토 피규어', 'franchise': None, 'characters': [], 'figure_form': None})}}
        return httpx.Response(200, json=data)
    monkeypatch.setattr(service.httpx, 'Client', lambda **kwargs: actual(**kwargs, transport=httpx.MockTransport(handler)))
    return calls


def test_local_cache_and_digest_version(monkeypatch, tmp_path):
    digest = ['abc']
    calls = install_transport(monkeypatch, digest=digest)
    first = OllamaExtractor(settings(tmp_path))
    source = {'name_original': 'NARUTO フィギュア', '_rules_hash': 'v1'}
    assert first(source) == first(source)
    assert sum(r.method == 'POST' for r in calls) == 1
    source['_rules_hash'] = 'v2'
    first(source)
    assert sum(r.method == 'POST' for r in calls) == 2
    digest[0] = 'def'
    second = OllamaExtractor(settings(tmp_path))
    second(source)
    assert sum(r.method == 'POST' for r in calls) == 3
    assert second.model.endswith('@def')
    assert first.metadata['digest'] == 'abc'
    assert first.model.startswith('ollama:')


def test_local_output_truncation_never_cached(monkeypatch, tmp_path):
    install_transport(monkeypatch, reason='length')
    ex = OllamaExtractor(settings(tmp_path))
    with pytest.raises(SemanticError, match='INCOMPLETE_LOCAL_RESPONSE'):
        ex({'name_original': 'test'})
    assert not list(tmp_path.rglob('*.json'))


def test_overlong_input_is_rejected_before_inference(monkeypatch, tmp_path):
    calls = install_transport(monkeypatch)
    ex = OllamaExtractor(settings(tmp_path))
    with pytest.raises(SemanticError, match='LOCAL_INPUT_TOO_LARGE'):
        ex({'name_original': 'test', 'document_0': 'あ' * 9000})
    assert all(request.method == 'GET' for request in calls)


def test_configured_context_is_sent_and_never_silently_truncates(monkeypatch, tmp_path):
    calls = install_transport(monkeypatch)
    ex = OllamaExtractor(settings(tmp_path, semantic_num_ctx=8192))
    ex({'name_original': 'NARUTO'})
    payload = json.loads(next(r.content for r in calls if r.method == 'POST'))
    assert payload['options']['num_ctx'] == 8192
    count = len(calls)
    with pytest.raises(SemanticError, match='LOCAL_INPUT_TOO_LARGE'):
        ex({'name_original': 'test', 'document_0': 'あ' * 3000})
    assert len(calls) == count


def test_no_paid_endpoint_or_cloud_model(tmp_path):
    s = settings(tmp_path)
    s.semantic_base_url = 'https://api.openai.com'
    with pytest.raises(SemanticError, match='LOCAL_OLLAMA_ENDPOINT_REQUIRED'):
        OllamaExtractor(s)
    s.semantic_base_url = 'http://localhost:11434'
    s.semantic_model = 'qwen:cloud'
    with pytest.raises(SemanticError, match='CLOUD_MODEL_NOT_ALLOWED'):
        OllamaExtractor(s)


def test_provider_local_requires_no_remote_api_key(monkeypatch, tmp_path):
    from app.services.semantic_provider import Extractor
    import app.core.config as config
    calls = install_transport(monkeypatch)
    s = settings(tmp_path)
    s.semantic_provider, s.llm_api_key = 'ollama', ''
    monkeypatch.setattr(config, 'get_settings', lambda: s)
    ex = Extractor()
    assert ex({'name_original': 'NARUTO'})['name_ko']
    payload = json.loads(next(r.content for r in calls if r.method == 'POST'))
    assert payload['stream'] is False and payload['think'] is False
    assert payload['format']['type'] == 'object'

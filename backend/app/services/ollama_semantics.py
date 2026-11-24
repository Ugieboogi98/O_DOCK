"""Local-only inference, content-addressed raw cache and model provenance."""
import hashlib
import json
import os
from pathlib import Path
import tempfile
import urllib.parse
import httpx
from app.services.semantic_errors import SemanticError


def prepare_input(source):
    from app.services.local_semantic_grounding import candidates
    from app.services.local_semantic_lexicon import title_hints, translation_input
    grounded = candidates(source)
    aliases = title_hints(source, grounded)
    return {**source, '_canonical_aliases': aliases, '_grounded_candidates': grounded,
            '_translation_input': translation_input(source, aliases)}


def schema():
    from app.services.semantic_rules import FORMS
    fields = ['name_original', 'franchise', 'character', 'document_0', 'document_1', 'document_2']
    entity = {'type': 'object', 'additionalProperties': False, 'properties': {
        'original': {'type': 'string'}, 'ko': {'type': 'string'},
        'evidence_field': {'type': 'string', 'enum': fields}, 'evidence': {'type': 'string'},
        'confidence': {'type': 'number', 'minimum': 0, 'maximum': 1}},
        'required': ['original', 'ko', 'evidence_field', 'evidence', 'confidence']}
    form = {'type': 'object', 'additionalProperties': False, 'properties': {
        'code': {'type': 'string', 'enum': list(FORMS)},
        'evidence_field': {'type': 'string', 'enum': ['name_original', 'product_line', 'scale', 'document_0', 'document_1', 'document_2']},
        'evidence': {'type': 'string'}, 'confidence': {'type': 'number', 'minimum': 0, 'maximum': 1}},
        'required': ['code', 'evidence_field', 'evidence', 'confidence']}
    return {'type': 'object', 'additionalProperties': False, 'properties': {
        'name_ko': {'type': 'string'}, 'franchise': {'anyOf': [entity, {'type': 'null'}]},
        'characters': {'type': 'array', 'maxItems': 20, 'items': entity},
        'figure_form': {'anyOf': [form, {'type': 'null'}]}},
        'required': ['name_ko', 'franchise', 'characters', 'figure_form']}


class OllamaExtractor:
    def __init__(self, settings):
        address = urllib.parse.urlsplit(settings.semantic_base_url)
        if (address.scheme != 'http' or address.hostname not in
                ('localhost', '127.0.0.1', '::1', 'host.docker.internal', 'ollama') or
                address.username or address.password or address.query or address.fragment or address.path not in ('', '/')):
            raise SemanticError('LOCAL_OLLAMA_ENDPOINT_REQUIRED')
        if 'cloud' in settings.semantic_model.lower():
            raise SemanticError('CLOUD_MODEL_NOT_ALLOWED')
        self.tag = settings.semantic_model
        self.num_ctx = max(4096, min(32768, getattr(settings, 'semantic_num_ctx', 32768)))
        self.cache = settings.media_dir / 'local_semantic_cache'
        self.client = httpx.Client(base_url=settings.semantic_base_url.rstrip('/'),
            timeout=settings.semantic_timeout, follow_redirects=False, trust_env=False)
        tags = self.request('/api/tags')
        entry = next((m for m in tags.get('models', []) if self.tag in (m.get('name'), m.get('model'))), None)
        if not entry or not entry.get('digest'):
            raise SemanticError('LOCAL_MODEL_NOT_INSTALLED')
        self.digest = entry['digest']
        self.model = 'ollama:' + self.tag + '@' + self.digest
        self.metadata = {'provider': 'ollama', 'model': self.tag, 'digest': self.digest,
                         'version': self.request('/api/version').get('version')}

    def request(self, endpoint, payload=None):
        try:
            response = self.client.get(endpoint) if payload is None else self.client.post(endpoint, json=payload)
            response.raise_for_status()
            if len(response.content) > 2_000_000:
                raise SemanticError('LOCAL_RESPONSE_TOO_LARGE')
            return response.json()
        except SemanticError:
            raise
        except (httpx.HTTPError, ValueError):
            raise SemanticError('LOCAL_PROVIDER_UNAVAILABLE') from None

    def __call__(self, source):
        from app.services.local_semantic_lexicon import fingerprint, grounded_result, publication_review
        instruction = Path(__file__).with_name('local_semantic_prompt.txt').read_text(encoding='utf-8')
        # The complete evidence-bearing source is retained. Never silently truncate.
        model_input = prepare_input(source)
        encoded_input = json.dumps(model_input, ensure_ascii=False)
        # UTF-8 bytes are a conservative upper bound for this byte-level BPE.
        # Leave room for output and message markers instead of server truncation.
        if len(encoded_input.encode()) + len(instruction.encode()) > self.num_ctx - 2048 - 512:
            raise SemanticError('LOCAL_INPUT_TOO_LARGE', False)
        identity = {'source': source, 'model_input': model_input, 'digest': self.digest, 'prompt': instruction, 'schema': schema(),
                    'alias_hash': fingerprint(),
                    'options': {'temperature': 0, 'num_ctx': self.num_ctx, 'num_predict': 2048}}
        key = hashlib.sha256(json.dumps(identity, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
        self.metadata['cache_key'] = key
        self.metadata['alias_hash'] = identity['alias_hash']
        target = self.cache / (key + '.json')
        self.metadata['cache_hit'] = target.exists()
        if target.exists():
            cached = json.loads(target.read_text(encoding='utf-8'))
            self.metadata['publication_review'] = cached.get('publication_review')
            return cached['result']
        raw = self.request('/api/chat', {'model': self.tag, 'stream': False, 'think': False,
            'keep_alive': '10m', 'format': schema(), 'options': identity['options'],
            'messages': [{'role': 'system', 'content': instruction},
                         {'role': 'user', 'content': encoded_input}]})
        if raw.get('done') is not True or raw.get('done_reason') != 'stop':
            raise SemanticError('INCOMPLETE_LOCAL_RESPONSE', False)
        try:
            result = json.loads(raw['message']['content'])
            if not isinstance(result, dict) or set(result) != {'name_ko', 'franchise', 'characters', 'figure_form'}:
                raise ValueError()
        except (ValueError, KeyError, TypeError):
            raise SemanticError('INVALID_LOCAL_JSON', False) from None
        model_result = result
        result = grounded_result(source, model_result)
        self.metadata['publication_review'] = publication_review(model_result, result)
        self.cache.mkdir(parents=True, exist_ok=True)
        fd, temporary = tempfile.mkstemp(dir=self.cache, prefix='.local-')
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as stream:
                json.dump({'identity': identity, 'result': result, 'model_result': model_result, 'raw': raw,
                           'publication_review': self.metadata['publication_review']}, stream, ensure_ascii=False)
            os.replace(temporary, target)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)
        self.metadata.update({k: raw.get(k) for k in ('prompt_eval_count', 'eval_count', 'total_duration')})
        return result

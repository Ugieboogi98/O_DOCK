"""Explicit web/manual classification publication, separate from model responses."""
import copy
from datetime import datetime, timezone
import re
from urllib.parse import urlsplit
from app.services.semantic_errors import SemanticError
from app.services.semantic_policy import finalize, publication_status

CLASS_FIELDS = ('franchise_ko', 'character_ko', 'figure_form')


def merge_overrides(fields, previous, digest):
    fields = copy.deepcopy(fields)
    overrides = {k: v for k, v in previous.get('classification_overrides', {}).items()
                 if k in CLASS_FIELDS and v.get('source_hash') == digest}
    if not overrides:
        return fields
    fields.setdefault('evidence', {})
    errors = {k: list(fields.get('field_issues', {}).get(k, [])) for k in ('name_ko', *CLASS_FIELDS)}
    na = []
    for key, item in overrides.items():
        errors[key] = []
        fields[key] = item['value']
        if key == 'character_ko':
            fields['characters'] = item.get('characters', [])
        if key == 'figure_form':
            from app.services.semantic_rules import FORMS
            fields['figure_form_ko'] = FORMS.get(item['value'])
        fields['evidence'][{'franchise_ko': 'franchise', 'character_ko': 'characters', 'figure_form': 'figure_form'}[key]] = item['evidence']
        if item.get('not_applicable'):
            na.append(key)
    fields['classification_overrides'] = overrides
    fields = finalize(fields, errors)
    for key in na:
        fields['field_status'][key] = 'not_applicable'
    fields['missing_fields'] = [k for k in CLASS_FIELDS if fields['field_status'].get(k) in ('missing', 'review')]
    states = [fields['field_status'][k] for k in CLASS_FIELDS]
    fields['classification_status'] = 'review' if 'review' in states else 'partial' if 'missing' in states else 'ready'
    return fields


def label(value):
    # Verified Korean-language references may legitimately use Latin titles.
    return isinstance(value, str) and 0 < len(value.strip()) <= 240 and not re.search('[ぁ-ゟ゠-ヿ一-龯]', value)


NAME_SUFFIXES = ('シリーズ', 'ちゃん', 'さん', 'くん', 'さま', 'たん', 'ver', 'Ver', 'VER', '시리즈')
# Form keywords are compound by nature (ぬーどるストッパーフィギュア); only names need word boundaries.
NAME_FIELDS = ('franchise_ko', 'character_ko')


def _script(ch):
    # ー is left out: titles use it as a bracket (フィギュアーエミリアー) as often as a long vowel.
    for name, pattern in (('kana', '[ァ-ヺｦ-ﾟ]'), ('hiragana', '[ぁ-ゖ]'), ('hangul', '[가-힣]'), ('latin', '[A-Za-z0-9]')):
        if re.fullmatch(pattern, ch):
            return name
    return None


def standalone(match, text, prefix=False):
    """The proof term must be a word of the title, not a piece of a longer one:
    ルフィ inside スケールフィギュア, 루피 inside 네페루피토, Black inside Blackjack.

    Katakana and Latin terms may not touch a letter of the same script on either side. Korean
    titles often run words together (승리의여신니케), so a Hangul term is only rejected when it
    sits inside a word with Hangul on both sides. Kanji have no such boundary and are not checked.
    prefix=True also accepts a work name that starts a longer title (ウルトラマン in ウルトラマンメビウス).
    """
    if not isinstance(text, str) or not match:
        return False
    first, last = _script(match[0]), _script(match[-1])
    for m in re.finditer(re.escape(match), text):
        before = _script(text[m.start() - 1]) if m.start() else None
        after = _script(text[m.end()]) if m.end() < len(text) else None
        left = first is not None and before == first
        # 初音ミクシリーズ, リンちゃん: a series word or honorific does not make a longer name.
        right = last is not None and after == last and not text.startswith(NAME_SUFFIXES, m.end())
        inside = (left and right) if 'hangul' in (first, last) else (left or (right and not prefix))
        if not inside:
            return True
    return False


def validate_patch(source, record):
    if record.get('method') not in ('web_verified', 'manual_verified') or record.get('approved') is not True:
        raise SemanticError('CLASSIFICATION_APPROVAL_REQUIRED', False)
    patch = record.get('patch', {})
    if not patch or not set(patch).issubset(CLASS_FIELDS):
        raise SemanticError('INVALID_CLASSIFICATION_PATCH', False)
    proofs = record.get('proofs', {})
    for key, value in patch.items():
        if value is None and key not in record.get('not_applicable_fields', []):
            raise SemanticError('EMPTY_VERIFIED_VALUE', False)
        if key == 'figure_form' and value is not None:
            from app.services.semantic_rules import FORMS
            if value not in FORMS:
                raise SemanticError('INVALID_FIGURE_FORM', False)
        elif key == 'character_ko' and value is not None:
            if not isinstance(value, list) or not value or any(not label(c.get('ko')) for c in value):
                raise SemanticError('INVALID_VERIFIED_CHARACTERS', False)
        elif value is not None and not label(value):
            raise SemanticError('INVALID_VERIFIED_LABEL', False)
        if record['method'] == 'web_verified':
            if not proofs.get(key):
                raise SemanticError('WEB_PROOF_REQUIRED', False)
            for proof in proofs[key]:
                text = source.get(proof.get('field'))
                parsed = urlsplit(proof.get('reference_url', ''))
                if (not isinstance(text, str) or not proof.get('match') or proof['match'] not in text or
                        (key in NAME_FIELDS and not standalone(proof['match'], text, prefix=key == 'franchise_ko')) or
                        parsed.scheme not in ('http', 'https') or not parsed.hostname or
                        not proof.get('reference_evidence') or not proof.get('checked_at')):
                    raise SemanticError('INVALID_WEB_PROOF', False)
    return patch


def apply_record(db, record):
    from app.models.entities import Figure, now
    from app.models.semantics import ProductSemantics
    from app.services.product_semantics import source_of, source_hash
    f = db.get(Figure, record['figure_id'], populate_existing=True, with_for_update=True)
    if f is None:
        raise SemanticError('FIGURE_NOT_FOUND', False)
    db.expire(f, ['manufacturer', 'product_line'])
    source = source_of(f)
    digest = source_hash(source)
    if record.get('source_hash') != digest:
        raise SemanticError('SOURCE_CHANGED_RETRY', False)
    patch = validate_patch(source, record)
    profile = db.get(ProductSemantics, f.id)
    base = copy.deepcopy(profile.fields) if profile and profile.source_hash == digest else {
        'name_ko': f.name_ko, 'franchise_ko': None, 'character_ko': None,
        'characters': [], 'figure_form': None, 'figure_form_ko': None, 'evidence': {}}
    overrides = base.setdefault('classification_overrides', {})
    for key, value in patch.items():
        # An automated web pass never overwrites the user's verified decision.
        if record['method'] == 'web_verified' and overrides.get(key, {}).get('method') == 'manual_verified':
            continue
        item = {'source_hash': digest, 'value': value, 'method': record['method'],
                'not_applicable': key in record.get('not_applicable_fields', []),
                'evidence': {'method': record['method'], 'references': record.get('proofs', {}).get(key, []),
                             'note': record.get('note', ''), 'review_id': record.get('review_id')},
                'checked_at': datetime.now(timezone.utc).isoformat()}
        if key == 'character_ko':
            item['characters'] = value or []
            item['value'] = ' · '.join(c['ko'] for c in value) if value else None
        overrides[key] = item
    fields = merge_overrides(base, base, digest)
    if profile is None:
        profile = ProductSemantics(figure_id=f.id, model='web-classification-v1')
        db.add(profile)
    profile.source, profile.source_hash, profile.fields = source, digest, fields
    profile.status = publication_status(fields, [])
    profile.issues = [error for errors in fields['field_issues'].values() for error in errors]
    profile.updated_at = now()
    db.flush()
    return profile.status

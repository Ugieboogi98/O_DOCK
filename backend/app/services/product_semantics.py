"""Semantic application service: catalog context, cache validity, queries and persistence.

The CLI-facing exports remain stable; pure rules and provider calls live in their
own modules so database work cannot silently introduce paid requests.
"""
from sqlalchemy import select, exists, case, func, or_
from sqlalchemy.orm import object_session
from app.models.entities import Figure, FigureVariant, SourceDocument, Manufacturer, ProductLine, now
from app.models.semantics import ProductSemantics
from app.services.semantic_errors import SemanticError
from app.services.semantic_provider import Extractor, INSTRUCTION
from app.services.semantic_rules import (
    VERSION, FORMS, FORM_ALIASES, normalize, add_documents, context_candidates,
    rules_hash, source_hash, korean, evidence, glossary, canonical,
    classification_status, dictionary_entities, validate_result,
)


def document_query(figure_id):
    return (select(SourceDocument).join(FigureVariant, SourceDocument.variant_id == FigureVariant.id)
            .where(FigureVariant.figure_id == figure_id)
            .order_by(case((SourceDocument.source_type == 'official_detail', 0), else_=1), SourceDocument.id.desc()))


def source_of(f, documents=None):
    source = {'name_original': f.name_original, 'official_url': f.official_url, 'manufacturer': f.manufacturer.name,
            'manufacturer_ko': f.manufacturer.name_ko,
            'product_line': f.product_line.name if f.product_line else None,
            'franchise': f.franchise, 'character': f.character, 'scale': f.scale, 'type': f.type,
            '_rules_hash': rules_hash()}
    if documents is None:
        db = object_session(f)
        documents = list(db.scalars(document_query(f.id).limit(3).execution_options(populate_existing=True))) if db and f.id is not None else []
    return add_documents(source, documents)


def current(db, f):
    p = db.get(ProductSemantics, f.id)
    return p if p and p.status in ('ready', 'partial') and p.source_hash == source_hash(source_of(f)) else None


def current_many(db, figures):
    """Validate one page's profiles using two queries instead of per-card reads."""
    figures = {f.id: f for f in figures}
    if not figures:
        return {}
    profiles = list(db.scalars(select(ProductSemantics).where(
        ProductSemantics.figure_id.in_(figures), ProductSemantics.status.in_(('ready', 'partial')))))
    if not profiles:
        return {}
    ids = [p.figure_id for p in profiles]
    ranked = (select(
        SourceDocument.id.label('document_id'), FigureVariant.figure_id.label('figure_id'),
        func.row_number().over(partition_by=FigureVariant.figure_id,
            order_by=(case((SourceDocument.source_type == 'official_detail', 0), else_=1),
                      SourceDocument.id.desc())).label('position'))
        .join(FigureVariant, SourceDocument.variant_id == FigureVariant.id)
        .where(FigureVariant.figure_id.in_(ids)).subquery())
    documents = {fid: [] for fid in ids}
    for doc, fid in db.execute(select(SourceDocument, ranked.c.figure_id)
            .join(ranked, ranked.c.document_id == SourceDocument.id)
            .where(ranked.c.position <= 3).order_by(ranked.c.figure_id, ranked.c.position)
            .execution_options(populate_existing=True)):
        documents[fid].append(doc)
    return {p.figure_id: p for p in profiles
            if p.source_hash == source_hash(source_of(figures[p.figure_id], documents[p.figure_id]))}


def semantic_match(field, value):
    """Only use validated entities whose source catalog fields still match."""
    expression = ProductSemantics.fields[field].as_string()
    matched = expression == value if field == 'figure_form' else expression.icontains(value, autoescape=True)
    return exists(select(ProductSemantics.figure_id).where(*valid_sql(), matched))


def valid_sql(statuses=('ready', 'partial')):
    maker = select(Manufacturer.name).where(Manufacturer.id == Figure.manufacturer_id).correlate(Figure).scalar_subquery()
    maker_ko = select(Manufacturer.name_ko).where(Manufacturer.id == Figure.manufacturer_id).correlate(Figure).scalar_subquery()
    line = select(ProductLine.name).where(ProductLine.id == Figure.product_line_id).correlate(Figure).scalar_subquery()
    checks = [ProductSemantics.figure_id == Figure.id, ProductSemantics.status.in_(statuses),
            ProductSemantics.source['_rules_hash'].as_string() == rules_hash(),
            ProductSemantics.source['manufacturer'].as_string().is_not_distinct_from(maker),
            ProductSemantics.source['manufacturer_ko'].as_string().is_not_distinct_from(maker_ko),
            ProductSemantics.source['product_line'].as_string().is_not_distinct_from(line),
            *[ProductSemantics.source[k].as_string().is_not_distinct_from(getattr(Figure, k))
              for k in ('name_original', 'official_url', 'franchise', 'character', 'scale', 'type')]]
    for i in range(3):
        stored_id = ProductSemantics.source[f'_document_{i}_id'].as_integer()
        current_id = document_query(Figure.id).with_only_columns(SourceDocument.id).correlate(Figure).offset(i).limit(1).scalar_subquery()
        checks.append(stored_id.is_not_distinct_from(current_id))
        checks.append(or_(stored_id.is_(None), exists(select(SourceDocument.id).where(
            SourceDocument.id == stored_id,
            func.substr(SourceDocument.body, 1, 6000) == ProductSemantics.source[f'document_{i}'].as_string(),
            SourceDocument.url == ProductSemantics.source[f'_document_{i}_url'].as_string(),
            SourceDocument.title == ProductSemantics.source[f'_document_{i}_title'].as_string(),
            SourceDocument.source_type == ProductSemantics.source[f'_document_{i}_source_type'].as_string()))))
    return checks


_FIELD_PARTS = {
    'name_ko': (('name_ko',), None),
    'franchise_ko': (('franchise_ko',), 'franchise'),
    'character_ko': (('character_ko', 'characters'), 'characters'),
    'figure_form': (('figure_form', 'figure_form_ko'), 'figure_form'),
}


def keep_ready_fields(new, old):
    """A re-run never downgrades a field that was already verified for the same source.

    Per field: when the previous result was 'ready' and the new one is not, the previous value,
    its evidence and its state are kept. New fields that became ready are taken as they are.
    """
    import copy
    if not isinstance(old, dict) or not isinstance(new, dict):
        return new
    out = copy.deepcopy(new)
    old_states, new_states = old.get('field_status') or {}, out.setdefault('field_status', {})
    kept = []
    for key, (values, evidence_key) in _FIELD_PARTS.items():
        # A manual override (including not_applicable) already decided this field; never replace it.
        if key in (out.get('classification_overrides') or {}):
            continue
        if old_states.get(key) == 'ready' and new_states.get(key) not in ('ready', 'not_applicable'):
            for name in values:
                out[name] = copy.deepcopy(old.get(name))
            if evidence_key:
                out.setdefault('evidence', {})
                if evidence_key in (old.get('evidence') or {}):
                    out['evidence'][evidence_key] = copy.deepcopy(old['evidence'][evidence_key])
                else:
                    out['evidence'].pop(evidence_key, None)
            new_states[key] = 'ready'
            out.setdefault('field_issues', {})[key] = []
            kept.append(key)
    if kept:
        from app.services.semantic_policy import FIELDS
        out['missing_fields'] = [k for k in FIELDS if k != 'name_ko' and not out.get(k)]
        out['translation_status'] = new_states.get('name_ko')
        classification = [new_states.get(k) for k in FIELDS if k != 'name_ko']
        out['classification_status'] = ('review' if 'review' in classification else
                                         'partial' if 'missing' in classification else 'ready')
        out['kept_previous_fields'] = kept
    return out


def save_record(db, record):
    """Validate imported reports again; never trust a stored model response as authorization."""
    f = db.get(Figure, record['figure_id'], populate_existing=True, with_for_update=True)
    if f:
        db.expire(f, ['manufacturer', 'product_line'])
    if not f or source_hash(source_of(f)) != record['source_hash'] or record['source_hash'] != source_hash(record['source']):
        raise SemanticError('SOURCE_CHANGED_RETRY', False)
    fields, issues = validate_result(record['source'], record['result'])
    p = db.get(ProductSemantics, f.id)
    if p and p.source_hash == record['source_hash']:
        from app.services.verified_classification import merge_overrides
        fields = merge_overrides(fields, p.fields, record['source_hash'])
        fields = keep_ready_fields(fields, p.fields)
        issues = [error for errors in fields.get('field_issues', {}).values() for error in errors]
    if p is None:
        p = ProductSemantics(figure_id=f.id)
        db.add(p)
    p.source_hash, p.source, p.fields = record['source_hash'], record['source'], fields
    p.status, p.model, p.issues, p.updated_at = classification_status(fields, issues), record['model'], issues, now()
    from app.core.config import get_settings
    if getattr(get_settings(), 'semantic_reference_enrichment', False):
        from app.services.reference_classifier import cached_record
        from app.services.verified_classification import apply_record
        db.flush()
        reference = cached_record(record['source'], record['source_hash'], f.id, p.fields)
        if reference and reference.get('patch'):
            apply_record(db, reference)
            record['applied_fields'] = p.fields
            record['reference_enrichment'] = True
    # Existing/manual Korean names, originals and personal lists are preserved.
    if fields.get('translation_status') == 'ready' and not f.name_ko:
        f.name_ko = fields['name_ko']
    from app.services.semantic_queue import finish
    finish(db, f.id, p.source_hash, p.status)
    db.commit()
    return p.status

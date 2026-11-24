"""Bounded, resumable semantic enrichment. No crawling, image writes or model training."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import tempfile
import time


def atomic_report(path, payload):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix='.semantics-', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as stream:
            json.dump(payload, stream, ensure_ascii=False, indent=2)
        # Windows bind mounts can briefly lock the target while an editor or
        # progress reader has it open. Keep the atomic write and retry the lock.
        for attempt in range(20):
            try:
                os.replace(temp, path)
                break
            except PermissionError:
                if attempt == 19:
                    raise
                time.sleep(0.25)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage', choices=['status', 'pending', 'run', 'apply', 'recheck', 'demo'])
    parser.add_argument('--queued', action='store_true', help='For run: process only queued products, within --limit')
    parser.add_argument('--manufacturer')
    parser.add_argument('--limit', type=int, default=5, help='Maximum paid model requests; 1..100 (default 5)')
    parser.add_argument('--figure-id', type=int)
    parser.add_argument('--figure-ids', help='Comma-separated exact figure IDs, e.g. 48,49,50,51,52')
    parser.add_argument('--retry-review', action='store_true')
    parser.add_argument('--refresh-local', action='store_true', help='Locally re-evaluate selected products, preserving previous publication in the report')
    parser.add_argument('--commit', action='store_true', help='For run: save validated results and review records')
    parser.add_argument('--report', type=Path, help='run output or apply input JSON file')
    parser.add_argument('--output', type=Path, help='recheck output; must differ from the input report')
    args = parser.parse_args()
    if not 1 <= args.limit <= 100:
        parser.error('--limit must be 1..100; unbounded paid requests are disabled')
    from app.services.product_semantics import source_of, source_hash, Extractor, SemanticError, validate_result, save_record, classification_status, FORMS
    if args.stage == 'demo':
        source = {'name_original': 'NARUTO-ナルト- 疾風伝 ぬーどるストッパーフィギュア うちはイタチ',
                  'manufacturer': 'FuRyu', 'manufacturer_ko': '후류', 'product_line': None,
                  'franchise': None, 'character': None, 'scale': None, 'type': 'figure'}
        result = {'name_ko': '나루토 질풍전 누들 스토퍼 피규어 우치하 이타치',
                  'franchise': {'original': 'NARUTO-ナルト- 疾風伝', 'ko': '나루토 질풍전', 'evidence_field': 'name_original', 'evidence': 'NARUTO-ナルト- 疾風伝', 'confidence': 1},
                  'characters': [{'original': 'うちはイタチ', 'ko': '우치하 이타치', 'evidence_field': 'name_original', 'evidence': 'うちはイタチ', 'confidence': 1}],
                  'figure_form': None}
        fields, issues = validate_result(source, result)
        print(json.dumps({'manufacturer': '후류', 'fields': fields, 'issues': issues, 'mode': 'OFFLINE_DEMO_NO_API'}, ensure_ascii=False))
        return
    from sqlalchemy import select, inspect, func, exists
    from sqlalchemy.orm import selectinload
    from app.core.config import get_settings
    from app.core.database import SessionLocal
    from app.models.entities import Figure, Manufacturer, CollectionJob
    from app.models.semantics import ProductSemantics
    settings = get_settings()
    if args.refresh_local and getattr(settings, 'semantic_provider', 'remote') != 'ollama':
        parser.error('--refresh-local requires SEMANTIC_PROVIDER=ollama')
    with SessionLocal() as db:
        if not inspect(db.get_bind()).has_table('product_semantics'):
            raise SemanticError('MIGRATION_REQUIRED: alembic upgrade head')
        if args.stage == 'status':
            groups = dict(db.execute(select(ProductSemantics.status, func.count()).group_by(ProductSemantics.status)).all())
            from app.services.semantic_queue import PREFIX
            queued = db.scalar(select(func.count(CollectionJob.id)).where(
                CollectionJob.collector.startswith(PREFIX, autoescape=True), CollectionJob.status == 'pending'))
            local = getattr(settings, 'semantic_provider', 'remote') == 'ollama'
            print(json.dumps({'api_key_set': bool(settings.llm_api_key),
                              'provider': 'ollama' if local else 'remote',
                              'model': settings.semantic_model if local else settings.llm_model,
                              'api_mode': 'ollama' if local else settings.llm_api_mode, 'stored_status_counts': groups,
                              'figures': db.scalar(select(func.count(Figure.id))),
                              'forms': FORMS, 'queued': queued, 'paid_api_called': False}, ensure_ascii=False))
            return
        if args.stage == 'pending':
            from app.services.semantic_queue import pending_jobs
            print(json.dumps({'mode': 'PENDING', 'paid_api_called': False,
                'items': [{'job_id': job.id, **json.loads(job.error_summary)} for job in pending_jobs(db, args.limit)]}, ensure_ascii=False))
            return
        if args.stage == 'recheck':
            if args.report is None or args.output is None or args.report.resolve() == args.output.resolve():
                parser.error('recheck requires --report and a different --output path')
            original = json.loads(args.report.read_text(encoding='utf-8'))
            payload = {'mode': 'RECHECK', 'paid_api_called': False, 'records': [],
                       'summary': {'ready': 0, 'partial': 0, 'review': 0, 'failed': 0}}
            for old in original['records']:
                if 'result' not in old:
                    continue
                f = db.get(Figure, old['figure_id'])
                fresh = source_of(f) if f else None
                core = lambda value: {k: v for k, v in value.items() if k != '_rules_hash'}
                if fresh is None or any(k not in fresh or fresh[k] != v for k, v in core(old['source']).items()):
                    payload['summary']['failed'] += 1
                    print(json.dumps({'figure_id': old['figure_id'], 'error': 'SOURCE_CHANGED_RETRY'}, ensure_ascii=False))
                    continue
                fields, issues = validate_result(fresh, old['result'])
                record = {'figure_id': f.id, 'source': fresh, 'source_hash': source_hash(fresh),
                          'model': old['model'], 'result': old['result'], 'fields': fields,
                          'issues': issues, 'status': classification_status(fields, issues)}
                payload['records'].append(record)
                payload['summary'][record['status']] += 1
                print(json.dumps({'figure_id': f.id, 'status': record['status'], 'fields': fields, 'issues': issues}, ensure_ascii=False), flush=True)
            atomic_report(args.output, payload)
            print(json.dumps({'mode': 'RECHECK', **payload['summary'], 'paid_api_called': False, 'report': str(args.output)}, ensure_ascii=False))
            if payload['summary']['failed']:
                raise SystemExit(1)
            return
        if args.stage == 'apply':
            if args.report is None:
                parser.error('apply requires --report pointing to a previous run report')
            payload = json.loads(args.report.read_text(encoding='utf-8'))
            counts = Counter()
            for record in payload['records']:
                if 'result' not in record:
                    continue
                try:
                    counts[save_record(db, record)] += 1
                except Exception as exc:
                    db.rollback()
                    counts['failed'] += 1
                    print(json.dumps({'figure_id': record.get('figure_id'), 'error': getattr(exc, 'code', type(exc).__name__)}, ensure_ascii=False), flush=True)
            print(json.dumps({'mode': 'APPLY', **counts, 'paid_api_called': False}, ensure_ascii=False))
            if counts['failed']:
                raise SystemExit(1)
            return
        query = select(Figure).options(selectinload(Figure.manufacturer), selectinload(Figure.product_line)).order_by(Figure.id)
        if args.queued:
            from app.services.semantic_queue import queued_match
            query = query.where(queued_match(Figure.id))
        if args.manufacturer:
            query = query.join(Manufacturer).where(Manufacturer.name == args.manufacturer)
        if args.figure_id is not None:
            query = query.where(Figure.id == args.figure_id)
        if args.figure_ids:
            try:
                ids = [int(value) for value in args.figure_ids.split(',')]
                if not ids or len(ids) > 100 or any(value <= 0 for value in ids):
                    raise ValueError()
            except ValueError:
                parser.error('--figure-ids must contain 1..100 positive integer IDs')
            query = query.where(Figure.id.in_(ids))
        selected, previous_profiles = [], {}
        from app.services.product_semantics import valid_sql
        cached_statuses = ('ready',) if args.retry_review else ('ready', 'partial', 'review')
        if not args.refresh_local:
            query = query.where(~exists(select(ProductSemantics.figure_id).where(*valid_sql(cached_statuses))))
        for f in db.scalars(query.limit(args.limit)):
            source = source_of(f)
            p = db.get(ProductSemantics, f.id)
            if not args.refresh_local and p and p.source_hash == source_hash(source) and (p.status == 'ready' or not args.retry_review):
                continue
            if args.refresh_local and p:
                previous_profiles[f.id] = {'source': p.source, 'fields': p.fields, 'issues': p.issues,
                                           'model': p.model, 'status': p.status}
            selected.append((f.id, source))
            if len(selected) == args.limit:
                break
        path = args.report or settings.media_dir / 'semantic_reports' / ('semantics_' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f') + '.json')
        report = {'mode': 'COMMIT' if args.commit else 'PREVIEW', 'records': [], 'summary': {'selected': len(selected), 'ready': 0, 'partial': 0, 'review': 0, 'failed': 0}}
        atomic_report(path, report)  # Test writable before any paid call.
        if not selected:
            print(json.dumps({**report['summary'], 'report': str(path), 'paid_api_called': False}, ensure_ascii=False))
            return
        # No database transaction is held while waiting on the provider.
        db.rollback()
        extractor = Extractor()
        for fid, source in selected:
            record = {'figure_id': fid, 'source': source, 'source_hash': source_hash(source), 'model': extractor.model}
            if fid in previous_profiles:
                record['previous_publication'] = previous_profiles[fid]
            try:
                record['result'] = extractor(source)
                if getattr(extractor, 'metadata', None):
                    record['provider_metadata'] = dict(extractor.metadata)
                fields, issues = validate_result(source, record['result'])
                record.update(fields=fields, issues=issues, status=classification_status(fields, issues))
                report['records'].append(record)
                atomic_report(path, report)  # Preserve model output even if DB saving fails.
                if args.commit:
                    record['status'] = save_record(db, record)
                report['summary'][record['status']] += 1
            except Exception as exc:
                db.rollback()
                record['error'] = getattr(exc, 'code', type(exc).__name__)
                record['status'] = 'failed'
                if not any(x is record for x in report['records']):
                    report['records'].append(record)
                report['summary']['failed'] += 1
                atomic_report(path, report)
                print(json.dumps({'figure_id': fid, 'status': 'failed', 'error': record['error']}, ensure_ascii=False), flush=True)
                if getattr(exc, 'blocked', True):
                    break
                continue
            atomic_report(path, report)
            print(json.dumps({'figure_id': fid, 'status': record['status'], 'fields': record['fields'], 'issues': record['issues']}, ensure_ascii=False), flush=True)
        print(json.dumps({'mode': report['mode'], **report['summary'], 'report': str(path)}, ensure_ascii=False), flush=True)
        if report['summary']['failed']:
            raise SystemExit(1)


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(json.dumps({'failed': 1, 'error': getattr(exc, 'code', type(exc).__name__)}, ensure_ascii=False), flush=True)
        raise SystemExit(1)

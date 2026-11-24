"""Resumable whole-catalog enrichment; explicit --commit authorizes paid calls.

One atomic evidence report per item, isolated DB sessions, bounded concurrency,
one validation retry, and immediate stop on provider authorization/quota failures.
"""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
import json
from pathlib import Path
import threading
from datetime import datetime, timezone

from sqlalchemy import select
from app.core.database import SessionLocal
from app.models.entities import Figure
from app.models.semantics import ProductSemantics
from app.services.product_semantics import (
    source_of, source_hash, Extractor, validate_result, save_record, classification_status)
from scripts.product_semantics import atomic_report


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--commit', action='store_true', required=True)
    p.add_argument('--workers', type=int, choices=range(1, 17), default=4)
    p.add_argument('--limit', type=int, default=0)
    p.add_argument('--report-dir', type=Path, required=True)
    p.add_argument('--refresh-local', action='store_true',
                   help='Reprocess every product with local inference; preserve previous publication in reports')
    args = p.parse_args()
    if args.limit < 0:
        p.error('limit must be nonnegative')
    from app.core.config import get_settings
    local = get_settings().semantic_provider == 'ollama'
    if local:
        from app.services.local_semantic_lexicon import fingerprint
        processing_fingerprint=fingerprint()
    else:processing_fingerprint=None
    if args.refresh_local and not local:
        p.error('--refresh-local requires SEMANTIC_PROVIDER=ollama')
    root = args.report_dir
    root.mkdir(parents=True, exist_ok=True)
    stop = threading.Event()
    counts = Counter()
    with SessionLocal() as db:
        ids = list(db.scalars(select(Figure.id).order_by(Figure.id)))
    if args.limit:
        ids = ids[:args.limit]
    # Test durable storage before any paid calls.
    atomic_report(root / 'progress.json', {'state': 'running', 'total': len(ids), 'counts': {}})

    def process(fid):
        path = root / f'{fid}.json'
        with SessionLocal() as db:
            f = db.get(Figure, fid)
            if f is None:
                return 'deleted'
            source = source_of(f)
            digest = source_hash(source)
            cached = db.get(ProductSemantics, fid)
            # Previous successful runs are free to resume. Retry the original
            # five pilot items once under the corrected English-title prompt.
            if (not args.refresh_local and cached and cached.source_hash == digest and
                    cached.fields.get('translation_status') == 'ready' and
                    (fid > 5 or path.exists())):
                return 'cached'
            previous = ({'source': cached.source, 'source_hash': cached.source_hash,
                         'fields': cached.fields, 'issues': cached.issues, 'model': cached.model,
                         'status': cached.status} if cached else None)
        if stop.is_set():
            return 'not_started'
        record = {'figure_id': fid, 'source': source, 'source_hash': digest}
        if local:record['processing_fingerprint']=processing_fingerprint
        if args.refresh_local:
            record['previous_publication'] = previous
            record['paid_api_called'] = False
        try:
            extractor = Extractor()
            record['model'] = extractor.model
            # Recover paid output if a prior run stopped between report and DB.
            old = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
            if (old.get('source_hash') == digest and old.get('model') == extractor.model and 'result' in old
                    and (not local or old.get('processing_fingerprint')==processing_fingerprint)):
                if args.refresh_local and old.get('committed'):
                    return 'resumed'
                record = old
            else:
                record['result'] = extractor(source)
                if getattr(extractor, 'metadata', None):
                    record['provider_metadata'] = dict(extractor.metadata)
                atomic_report(path, record)
            fields, issues = validate_result(source, record['result'])
            # Local publication is deterministic and abstains on missing dictionary
            # coverage. Repeating the same local proposal cannot repair that coverage.
            if issues and not local and not record.get('validation_retry') and not stop.is_set():
                record['first_result'] = record['result']
                record['first_issues'] = issues
                record['validation_retry'] = True
                atomic_report(path, record)
                corrected = extractor({**source, '_validation_feedback': issues,
                    '_previous_result': record['result'],
                    '_task': 'Correct rejected fields using only original source evidence. Keep all numeric facts and codes.'})
                new_fields, new_issues = validate_result(source, corrected)
                # Do not replace a better initial response with a worse retry.
                score = lambda v: (v.get('translation_status') == 'ready',
                    sum(s == 'ready' for s in v.get('field_status', {}).values()))
                if score(new_fields) > score(fields) or (score(new_fields) == score(fields) and len(new_issues) < len(issues)):
                    record['result'], fields, issues = corrected, new_fields, new_issues
                record['retry_result'] = corrected
            record.update(fields=fields, issues=issues, status=classification_status(fields, issues))
            atomic_report(path, record)
            with SessionLocal() as db:
                record['status'] = save_record(db, record)
            record['committed'] = True
            atomic_report(path, record)
            return record['status']
        except Exception as exc:
            record['error'] = getattr(exc, 'code', type(exc).__name__)
            record['committed'] = False
            atomic_report(path, record)
            if getattr(exc, 'blocked', True):
                stop.set()
            return 'failed'

    def progress(state):
        payload = {'state': state, 'total': len(ids), 'workers': args.workers, 'counts': dict(counts),
                   'finished': sum(counts.values()), 'updated_at': datetime.now(timezone.utc).isoformat()}
        atomic_report(root / 'progress.json', payload)
        print(json.dumps(payload), flush=True)

    iterator = iter(ids)
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        pending = {pool.submit(process, fid) for fid in [next(iterator, None) for _ in range(args.workers)] if fid is not None}
        while pending:
            done, pending = wait(pending, return_when=FIRST_COMPLETED)
            for future in done:
                counts[future.result()] += 1
                if not stop.is_set():
                    fid = next(iterator, None)
                    if fid is not None:
                        pending.add(pool.submit(process, fid))
            progress('stopping' if stop.is_set() else 'running')
    progress('blocked' if stop.is_set() else 'completed')
    if stop.is_set() or counts['failed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()

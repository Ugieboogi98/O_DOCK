"""Sequential local-only consumer for the collection semantic outbox."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import time
from app.core.config import get_settings
from app.core.database import SessionLocal
from app.models.entities import Figure
from app.models.semantics import ProductSemantics
from app.services.product_semantics import Extractor, source_of, source_hash, save_record, validate_result
from app.services.semantic_queue import pending_jobs, finish, enqueue
from scripts.product_semantics import atomic_report


def consume(limit, report_dir):
    settings = get_settings()
    if settings.semantic_provider != 'ollama':
        raise RuntimeError('LOCAL_PROVIDER_REQUIRED_NO_PAID_FALLBACK')
    with SessionLocal() as db:
        ids = [json.loads(job.error_summary)['figure_id'] for job in pending_jobs(db, limit)]
    if not ids:
        return {'selected': 0, 'committed': 0}
    extractor = Extractor()
    counts = {'selected': len(ids), 'committed': 0, 'cached': 0}
    for fid in ids:
        with SessionLocal() as db:
            f = db.get(Figure, fid)
            if f is None:
                raise RuntimeError('QUEUED_FIGURE_NOT_FOUND')
            source = source_of(f)
            digest = source_hash(source)
            previous = db.get(ProductSemantics, fid)
            if previous and previous.source_hash == digest:
                # Reconcile a stale queued source before marking its work complete.
                enqueue(db, f)
                finish(db, fid, digest, previous.status)
                db.commit()
                counts['cached'] += 1
                continue
            prior = ({'source': previous.source, 'fields': previous.fields, 'issues': previous.issues,
                      'model': previous.model, 'status': previous.status} if previous else None)
            enqueue(db, f)
            db.commit()
        stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')
        path = report_dir / f'{fid}_{stamp}.json'
        record = {'figure_id': fid, 'source': source, 'source_hash': digest,
                  'model': extractor.model, 'previous_publication': prior,
                  'mode': 'LOCAL_QUEUE', 'paid_api_called': False}
        atomic_report(path, record)  # Check report storage before inference.
        try:
            record['result'] = extractor(source)
            record['provider_metadata'] = dict(getattr(extractor, 'metadata', {}))
            record['fields'], record['issues'] = validate_result(source, record['result'])
            atomic_report(path, record)
            with SessionLocal() as db:
                record['status'] = save_record(db, record)
            record['committed'] = True
            counts['committed'] += 1
        except Exception as exc:
            record['error'] = getattr(exc, 'code', type(exc).__name__)
            atomic_report(path, record)
            raise
        atomic_report(path, record)
        print(json.dumps({'figure_id': fid, 'status': record['status'], 'paid_api_called': False}), flush=True)
    return counts


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--limit', type=int, choices=range(1, 101), default=5)
    p.add_argument('--watch', action='store_true')
    p.add_argument('--poll-seconds', type=int, choices=range(5, 61), default=15)
    p.add_argument('--report-dir', type=Path)
    args = p.parse_args()
    settings = get_settings()
    while True:
        print(json.dumps(consume(args.limit, args.report_dir or settings.media_dir / 'local_semantic_reports')), flush=True)
        if not args.watch:
            return
        time.sleep(args.poll_seconds)


if __name__ == '__main__':
    main()

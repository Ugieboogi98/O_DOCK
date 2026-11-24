"""Preview/apply explicit researched or user-confirmed classification patches."""
import argparse
import copy
import json
import os
from pathlib import Path
from app.core.database import SessionLocal
from app.models.semantics import ProductSemantics
from app.services.verified_classification import apply_record
from scripts.product_semantics import atomic_report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--commit', action='store_true')
    args = parser.parse_args()
    if args.report.exists():
        parser.error('Use a new audit report path')
    journal = args.report.with_suffix('.journal.jsonl')
    journal.parent.mkdir(parents=True, exist_ok=True)
    journal.open('x', encoding='utf-8').close()
    def append(item):
        with journal.open('a', encoding='utf-8') as stream:
            stream.write(json.dumps(item, ensure_ascii=False) + '\n')
            stream.flush()
            os.fsync(stream.fileno())
    rows = json.loads(args.input.read_text(encoding='utf-8'))['records']
    report = {'mode': 'COMMIT' if args.commit else 'PREVIEW', 'records': [],
              'summary': {'selected': len(rows), 'accepted': 0, 'failed': 0}, 'paid_api_called': False,
              'journal': str(journal)}
    atomic_report(args.report, report)
    for record in rows:
        with SessionLocal() as db:
            previous = db.get(ProductSemantics, record['figure_id'])
            old = None if previous is None else {'source': previous.source, 'source_hash': previous.source_hash,
                'fields': copy.deepcopy(previous.fields), 'model': previous.model, 'issues': previous.issues, 'status': previous.status}
            item = {'figure_id': record['figure_id'], 'previous': old, 'patch': record}
            try:
                item['status'] = apply_record(db, record)
                # Write rollback evidence before changing production rows.
                append(item)
                if args.commit:
                    db.commit()
                else:
                    db.rollback()
                report['summary']['accepted'] += 1
                report['records'].append({'figure_id': item['figure_id'], 'status': item['status']})
            except Exception as exc:
                db.rollback()
                item['error'] = getattr(exc, 'code', type(exc).__name__)
                append(item)
                report['records'].append({'figure_id': item['figure_id'], 'error': item['error']})
                report['summary']['failed'] += 1
            if report['summary']['accepted'] % 100 == 0:
                print(json.dumps(report['summary']), flush=True)
    atomic_report(args.report, report)
    print(json.dumps(report['summary']), flush=True)
    if report['summary']['failed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()

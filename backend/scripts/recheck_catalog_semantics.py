"""Revalidate saved model responses against current rules, with zero API calls."""
import argparse
from collections import Counter
import json
from pathlib import Path
from app.core.database import SessionLocal
from app.models.entities import Figure
from app.services.product_semantics import source_of, source_hash, validate_result, save_record
from scripts.product_semantics import atomic_report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report-dir', type=Path, required=True)
    parser.add_argument('--commit', action='store_true', required=True)
    args = parser.parse_args()
    counts = Counter()
    for path in sorted(args.report_dir.glob('[0-9]*.json'), key=lambda p: int(p.stem)):
        record = json.loads(path.read_text(encoding='utf-8'))
        if 'result' not in record:
            counts['no_response'] += 1
            continue
        try:
            with SessionLocal() as db:
                f = db.get(Figure, record['figure_id'])
                fresh = source_of(f) if f else None
                core = lambda s: {k: v for k, v in s.items() if k not in ('_rules_hash', '_entity_candidates')}
                if fresh is None or core(fresh) != core(record['source']):
                    counts['source_changed'] += 1
                    continue
                candidates = [record[key] for key in ('result', 'first_result', 'retry_result') if key in record]
                def quality(result):
                    values, errors = validate_result(fresh, result)
                    return (values.get('translation_status') == 'ready',
                            sum(s == 'ready' for s in values.get('field_status', {}).values()), -len(errors))
                record['result'] = max(candidates, key=quality)
                fields, issues = validate_result(fresh, record['result'])
                record.setdefault('validation_history', []).append({
                    'source_hash': record['source_hash'], 'issues': record.get('issues'), 'status': record.get('status')})
                record.update(source=fresh, source_hash=source_hash(fresh), fields=fields, issues=issues)
                record['status'] = save_record(db, record)
                record['committed'] = True
                record.pop('error', None)
                atomic_report(path, record)
                counts[record['status']] += 1
        except Exception as exc:
            counts['failed'] += 1
            print(json.dumps({'figure_id': record['figure_id'], 'error': getattr(exc, 'code', type(exc).__name__)}), flush=True)
    atomic_report(args.report_dir / 'recheck.json', {'counts': dict(counts), 'paid_api_called': False})
    print(json.dumps({'counts': dict(counts), 'paid_api_called': False}), flush=True)
    if counts['failed'] or counts['source_changed']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()

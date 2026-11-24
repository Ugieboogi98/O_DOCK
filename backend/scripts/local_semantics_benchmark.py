"""Small contract regression benchmark, not a broad translation quality claim."""
import argparse
import json
from pathlib import Path
import time
from app.core.config import get_settings
from app.services.product_semantics import Extractor, validate_result
from scripts.product_semantics import atomic_report


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--cases', type=Path, required=True)
    p.add_argument('--report', type=Path, required=True)
    args = p.parse_args()
    if get_settings().semantic_provider != 'ollama':
        p.error('Local provider required')
    if args.report.exists():
        p.error('Report exists; use a new filename')
    extractor = Extractor()
    report = {'mode': 'LOCAL_CLASSIFICATION_REGRESSION', 'paid_api_called': False,
              'db_committed': False, 'model': extractor.model, 'records': []}
    atomic_report(args.report, report)
    for line in args.cases.read_text(encoding='utf-8').splitlines():
        if not line.strip():
            continue
        case = json.loads(line)
        record = {'figure_id': case['figure_id'], 'source': case['source'], 'expected': case['expected']}
        started = time.monotonic()
        try:
            record['result'] = extractor(case['source'])
            fields, issues = validate_result(case['source'], record['result'])
            actual = {'franchise_ko': fields.get('franchise_ko'),
                      'characters': sorted(x['ko'] for x in fields.get('characters', [])),
                      'figure_form': fields.get('figure_form')}
            expected = dict(case['expected'], characters=sorted(case['expected']['characters']))
            record.update(fields=fields, issues=issues, actual=actual,
                exact_classification_match=actual == expected,
                translation_valid=fields.get('translation_status') == 'ready')
        except Exception as exc:
            record['error'] = getattr(exc, 'code', type(exc).__name__)
        record['elapsed_seconds'] = round(time.monotonic() - started, 3)
        record['provider_metadata'] = dict(extractor.metadata)
        report['records'].append(record)
        atomic_report(args.report, report)
        print(json.dumps({'id': case['figure_id'], 'match': record.get('exact_classification_match'),
                          'seconds': record['elapsed_seconds'], 'error': record.get('error')}), flush=True)
        if record.get('error'):
            break
    rows = report['records']
    report['summary'] = {'cases': len(rows), 'exact_classification_matches': sum(r.get('exact_classification_match', False) for r in rows),
                         'valid_translations': sum(r.get('translation_valid', False) for r in rows),
                         'failures': sum('error' in r for r in rows)}
    atomic_report(args.report, report)
    print(json.dumps(report['summary']), flush=True)
    if report['summary']['failures']:
        raise SystemExit(1)


if __name__ == '__main__':
    main()

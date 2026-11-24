"""Fresh local inference on a frozen source file, without catalog DB access."""
import argparse
import hashlib
import json
from pathlib import Path
import time
from app.core.config import get_settings
from app.services.semantic_provider import Extractor
from app.services.semantic_rules import validate_result
from app.services.reference_classifier import cached_record
from scripts.product_semantics import atomic_report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sources', type=Path, required=True)
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--resume', action='store_true')
    args = parser.parse_args()
    if get_settings().semantic_provider != 'ollama':
        raise RuntimeError('LOCAL_PROVIDER_REQUIRED')
    if args.report.exists() and not args.resume:
        raise RuntimeError('REPORT_ALREADY_EXISTS')
    sources = json.loads(args.sources.read_text(encoding='utf-8'))['records']
    root = Path(__file__).resolve().parents[1] / 'app/services'
    names = ['ollama_semantics.py', 'local_semantic_prompt.txt', 'local_semantic_lexicon.py',
             'local_semantic_grounding.py', 'local_semantic_tuning_lexicon.json',
             'local_semantic_domain_aliases.json', 'local_semantic_title_terms.json',
             'local_semantic_domain_extension.json',
             'reference_classifier.py', 'classification_knowledge.json', 'classification_wikipedia_anime.json',
             'semantic_rules.py', 'semantic_policy.py']
    extractor = Extractor()
    extractor.local.cache = args.report.parent / (args.report.stem + '_cache')
    report = {'backend': 'ollama_q4_k_m', 'model': extractor.model, 'db_written': False, 'paid_api_called': False,
              'sources_sha256': hashlib.sha256(args.sources.read_bytes()).hexdigest(),
              'implementation_sha256': {name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in names},
              'records': []}
    if args.resume and args.report.exists():
        previous = json.loads(args.report.read_text(encoding='utf-8'))
        if any(previous.get(key) != report[key] for key in ('model', 'sources_sha256', 'implementation_sha256')):
            raise RuntimeError('RESUME_IDENTITY_CHANGED')
        report['previous_failures'] = previous.get('previous_failures', []) + [r for r in previous['records'] if 'error' in r]
        report['records'] = [r for r in previous['records'] if 'error' not in r]
    atomic_report(args.report, report)
    completed_ids = {r['figure_id'] for r in report['records']}
    for row in sources:
        if row['figure_id'] in completed_ids:
            continue
        record = dict(row)
        started = time.monotonic()
        try:
            normalized = extractor(row['source'])
            cache = extractor.local.cache / (extractor.metadata['cache_key'] + '.json')
            raw_cache = json.loads(cache.read_text(encoding='utf-8'))
            raw = raw_cache['model_result']
            fields, issues = validate_result(row['source'], normalized)
            raw_fields, raw_issues = validate_result(row['source'], raw)
            record.update(model_result=raw, raw_fields=raw_fields, raw_issues=raw_issues,
                          model_input=raw_cache['identity']['model_input'], normalized_result=normalized,
                          validated_fields=fields, issues=issues, provider_metadata=dict(extractor.metadata),
                          reference_patch=cached_record(row['source'], '', row['figure_id'], fields))
        except Exception as exc:
            record['error'] = getattr(exc, 'code', type(exc).__name__)
        record['seconds'] = round(time.monotonic() - started, 3)
        report['records'].append(record)
        atomic_report(args.report, report)
        print(json.dumps({'completed': len(report['records']), 'id': row['figure_id'],
                          'seconds': record['seconds'], 'error': record.get('error')}), flush=True)
    report['completed'] = True
    atomic_report(args.report, report)


if __name__ == '__main__':
    main()

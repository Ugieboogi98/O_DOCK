"""Development-only replay of saved raw proposals against changed deterministic rules.

This does NOT rerun the model with updated hints and is never an independent holdout.
"""
import argparse
import hashlib
import json
from pathlib import Path
from app.services.local_semantic_lexicon import grounded_result
from app.services.semantic_rules import validate_result
from app.services.reference_classifier import cached_record


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists():
        raise RuntimeError('REFUSE_OVERWRITE')
    report = json.loads(args.input.read_text(encoding='utf-8'))
    report['evaluation_kind'] = 'development_deterministic_replay_not_new_inference_or_holdout'
    report['original_report_sha256'] = hashlib.sha256(args.input.read_bytes()).hexdigest()
    report['original_inference_implementation_sha256'] = report.pop('implementation_sha256', {})
    root = Path(__file__).resolve().parents[1] / 'app/services'
    report['replay_implementation_sha256'] = {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
        for p in root.iterdir() if p.suffix in ('.py', '.json', '.txt')}
    for row in report['records']:
        if 'model_result' not in row:
            continue
        row['normalized_result'] = grounded_result(row['source'], row['model_result'])
        fields, issues = validate_result(row['source'], row['normalized_result'])
        row.update(validated_fields=fields, issues=issues,
                   reference_patch=cached_record(row['source'], '', row['figure_id'], fields))
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()

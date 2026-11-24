"""Evaluate validated predictions against reviewed held-out labels, offline."""
import argparse
import json
from pathlib import Path


def expected(row):
    if 'expected' in row:
        return row['expected']
    value = row['result']
    return {'franchise_ko': value['franchise']['ko'] if value['franchise'] else None,
            'characters': [c['ko'] for c in value['characters']],
            'figure_form': value['figure_form']['code'] if value['figure_form'] else None}


def score(gold, predictions):
    if not gold:
        raise ValueError('EMPTY_GOLD')
    mapped = {str(row['figure_id']): row for row in predictions}
    if len(mapped) != len(predictions):
        raise ValueError('DUPLICATE_PREDICTION_IDS')
    tp = fp = fn = franchise_correct = form_correct = valid = title_valid = 0
    pairs = []
    for row in gold:
        target = expected(row)
        prediction = mapped.get(str(row['figure_id']), {})
        fields = prediction.get('fields', {})
        got = prediction.get('actual') or {'franchise_ko': fields.get('franchise_ko'),
            'characters': [c['ko'] for c in fields.get('characters', [])], 'figure_form': fields.get('figure_form')}
        valid_row = bool(prediction) and 'error' not in prediction and bool(fields)
        valid += valid_row
        title_valid += valid_row and fields.get('translation_status') == 'ready'
        franchise_correct += valid_row and target['franchise_ko'] == got['franchise_ko']
        form_correct += valid_row and target['figure_form'] == got['figure_form']
        wanted, actual = set(target['characters']), set(got['characters']) if valid_row else set()
        tp += len(wanted & actual)
        fp += len(actual - wanted)
        fn += len(wanted - actual)
        pairs.append((target['figure_form'], got['figure_form'] if valid_row else '__failed__'))
    classes = {value for pair in pairs for value in pair if value not in (None, '__failed__')}
    per_class = {}
    for code in sorted(classes):
        correct = sum(g == code and p == code for g, p in pairs)
        false_positive = sum(g != code and p == code for g, p in pairs)
        false_negative = sum(g == code and p != code for g, p in pairs)
        denominator = 2 * correct + false_positive + false_negative
        per_class[code] = 2 * correct / denominator if denominator else 0
    return {'cases': len(gold), 'validated_prediction_rate': valid / len(gold),
        'translation_validation_rate_not_semantic_accuracy': title_valid / len(gold),
        'franchise_accuracy': franchise_correct / len(gold), 'form_accuracy': form_correct / len(gold),
        'character_precision': tp / (tp + fp) if tp + fp else (1.0 if fn == 0 else 0.0),
        'character_recall': tp / (tp + fn) if tp + fn else 1.0,
        'form_macro_f1_observed_classes': sum(per_class.values()) / len(per_class) if per_class else None,
        'form_f1_by_class': per_class,
        'note': 'Published-field metrics; translation correctness still needs human review. Sanity cases are not held-out performance.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--gold', type=Path, required=True)
    p.add_argument('--predictions', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--sanity', action='store_true')
    args = p.parse_args()
    gold = [json.loads(s) for s in args.gold.read_text(encoding='utf-8').splitlines() if s.strip()]
    if not args.sanity and any(r.get('reviewed') is not True or not r.get('reviewer') for r in gold):
        p.error('Reviewed gold labels required; --sanity is only for regression experiments')
    rows = json.loads(args.predictions.read_text(encoding='utf-8'))['records']
    result = score(gold, rows)
    result['evaluation_kind'] = 'development_sanity' if args.sanity else 'reviewed_holdout'
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()

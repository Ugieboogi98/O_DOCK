"""Score raw, normalized and reference-assisted outputs without conflating them."""
import argparse
import copy
import json
from pathlib import Path
import re
import unicodedata


def key(value):
    return re.sub(r'[\W_]+', '', unicodedata.normalize('NFKC', value or '')).casefold()


def fields(record, stage):
    if stage == 'raw':
        raw = record.get('model_result') or {}
        if not isinstance(raw, dict):
            return {}
        work = raw.get('franchise')
        form = raw.get('figure_form')
        return {'franchise_ko': work.get('ko') if isinstance(work, dict) else None,
                'characters': raw.get('characters') or [],
                'figure_form': form.get('code') if isinstance(form, dict) else None, 'name_ko': raw.get('name_ko')}
    value = copy.deepcopy(record.get('validated_fields') or {})
    if stage == 'reference_assisted':
        patch = (record.get('reference_patch') or {}).get('patch', {})
        if 'franchise_ko' in patch:
            value['franchise_ko'] = patch['franchise_ko']
        if 'character_ko' in patch:
            value['characters'] = patch['character_ko']
        if 'figure_form' in patch:
            value['figure_form'] = patch['figure_form']
    return value


def score(labels, records, stage):
    mapped = {r['figure_id']: r for r in records}
    work_total = work_correct = work_published = char_tp = char_fp = char_fn = 0
    form_total = form_correct = form_published = form_bad_published = form_required = form_required_correct = 0
    failures = []
    for case in labels:
        record = mapped.get(case['id'], {})
        actual = fields(record, stage)
        skip = case.get('skip', [])
        row_errors = []
        if 'work' not in skip:
            work_total += 1
            correct = key(actual.get('franchise_ko')) in {key(x) for x in case['work']}
            work_correct += correct
            work_published += bool(actual.get('franchise_ko'))
            if not correct:
                row_errors.append('work')
        if 'characters' not in skip:
            remaining = [set(map(key, group)) for group in case['characters']]
            for character in actual.get('characters', []):
                name = key(character.get('ko')) if isinstance(character, dict) else key(character)
                index = next((i for i, group in enumerate(remaining) if name in group), None)
                if index is None:
                    char_fp += 1
                    row_errors.append('extra_or_wrong_character:' + name)
                else:
                    char_tp += 1
                    remaining.pop(index)
            char_fn += len(remaining)
            if remaining:
                row_errors.append('missing_character')
        if 'form' not in skip:
            form_total += 1
            chosen = actual.get('figure_form')
            correct = chosen in case['forms']
            form_correct += correct
            form_published += chosen is not None
            form_bad_published += chosen is not None and not correct
            if None not in case['forms']:
                form_required += 1
                form_required_correct += correct
            if not correct:
                row_errors.append('form')
        if row_errors:
            failures.append({'id': case['id'], 'errors': row_errors, 'actual': actual})
    return {
        'work_cases': work_total, 'work_correct': work_correct, 'work_accuracy': work_correct / work_total,
        'work_published_precision': work_correct / work_published if work_published else None,
        'work_publication_coverage': work_published / work_total,
        'character_tp': char_tp, 'character_fp': char_fp, 'character_fn': char_fn,
        'character_precision': char_tp / (char_tp + char_fp) if char_tp + char_fp else None,
        'character_recall': char_tp / (char_tp + char_fn) if char_tp + char_fn else None,
        'form_cases': form_total, 'form_correct_including_supported_abstentions': form_correct,
        'form_accuracy_including_supported_abstentions': form_correct / form_total,
        'form_published': form_published, 'form_wrong_published': form_bad_published,
        'form_published_precision': (form_published - form_bad_published) / form_published if form_published else None,
        'required_form_cases': form_required, 'required_form_correct': form_required_correct,
        'required_form_recall': form_required_correct / form_required if form_required else None,
        'failures': failures,
    }


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--labels', type=Path, required=True)
    p.add_argument('--report', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    gold = json.loads(args.labels.read_text(encoding='utf-8'))
    report = json.loads(args.report.read_text(encoding='utf-8'))
    if len(report['records']) != len(gold['cases']):
        raise RuntimeError('INCOMPLETE_EVALUATION')
    result = {'label_origin': gold['label_origin'], 'cases': len(gold['cases']),
              'generation_errors': sum('error' in r for r in report['records']),
              'translation_semantic_accuracy': 'requires separate source-to-output review',
              'stages': {stage: score(gold['cases'], report['records'], stage)
                         for stage in ('raw', 'normalized', 'reference_assisted')}}
    final = result['stages']['reference_assisted']
    thresholds = {'work_published_precision': .98, 'work_publication_coverage': .90,
                  'character_precision': .98, 'character_recall': .90,
                  'form_published_precision': .98, 'required_form_recall': .95}
    result['classification_gate'] = {
        'thresholds': thresholds, 'passed': all(final[k] is not None and final[k] >= v for k, v in thresholds.items())}
    result['release_allowed'] = False
    result['release_note'] = 'Translation semantics must also be audited; this score alone never approves publication.'
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({stage: {k: v for k, v in value.items() if k != 'failures'} for stage, value in result['stages'].items()}))


if __name__ == '__main__':
    main()

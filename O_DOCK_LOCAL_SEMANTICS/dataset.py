"""Prepare reviewable SFT candidates from saved responses; no API/DB writes."""
import argparse
import copy
from collections import Counter
import hashlib
import json
from pathlib import Path
import re
import sys
import unicodedata

ROOT = Path(__file__).resolve().parent


def family(source):
    # JAN/SKU reissues and minor title variants must not cross data splits.
    title = unicodedata.normalize('NFKC', source['name_original']).casefold()
    title = re.sub(r'【[^】]*(?:再販|再生産)[^】]*】|\([^)]*(?:再販|再生産)[^)]*\)', '', title)
    return re.sub(r'\W+', '', title)


def components(rows):
    """Connected groups by URL/title/duplicated description, across makers too."""
    parent = list(range(len(rows)))
    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    seen = {}
    for i, row in enumerate(rows):
        source = row['source']
        keys = [('title', family(source))]
        if source.get('official_url'):
            keys.append(('url', source['official_url'].split('#')[0].split('?')[0]))
        for n in range(3):
            text = source.get(f'document_{n}') or ''
            if len(text) > 150:
                keys.append(('description', hashlib.sha256(text.encode()).hexdigest()))
        for key in keys:
            if key in seen:
                parent[find(i)] = find(seen[key])
            else:
                seen[key] = i
    groups = {}
    for i, row in enumerate(rows):
        groups.setdefault(find(i), []).append(row)
    return list(groups.values())


def split_rows(rows):
    splits = {'train': [], 'validation': [], 'test': []}
    for group in components(rows):
        token = min(family(r['source']) for r in group)
        bucket = int(hashlib.sha256(token.encode()).hexdigest()[:8], 16) % 100
        part = 'test' if bucket < 10 else 'validation' if bucket < 20 else 'train'
        for row in group:
            splits[part].append(row)
    return splits


def write_jsonl(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8') as stream:
        for row in rows:
            stream.write(json.dumps(row, ensure_ascii=False) + '\n')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--reports', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--backend', type=Path, default=ROOT.parent / 'backend')
    args = p.parse_args()
    if args.output.exists() and any(args.output.iterdir()):
        p.error('Use a new output directory; reviewed datasets must not be overwritten')
    sys.path.insert(0, str(args.backend.resolve()))
    from app.services.semantic_rules import validate_result, rules_hash
    from app.services.semantic_provider import INSTRUCTION
    counts, candidates, review = Counter(), [], []
    for path in sorted(args.reports.glob('[0-9]*.json')):
        record = json.loads(path.read_text(encoding='utf-8'))
        if not record.get('result') or not record.get('source'):
            counts['no_response'] += 1
            continue
        source, result = record['source'], record['result']
        fields, issues = validate_result(source, result)
        item = {'figure_id': record['figure_id'], 'source': source, 'result': result,
                'label_origin': 'teacher_model_unreviewed', 'reviewed': False,
                'teacher_model': record.get('model'), 'source_report': path.name,
                'field_status': fields.get('field_status', {}), 'issues': issues}
        # A review-free, missing entity is not a negative gold label.
        complete = (isinstance(result.get('franchise'), dict) and bool(result.get('characters'))
                    and isinstance(result.get('figure_form'), dict))
        # A field recovered by a dictionary must not leave a null/missing label
        # in the teacher target. Queue such examples for explicit annotation.
        if fields.get('field_status') and all(v == 'ready' for v in fields['field_status'].values()) and complete:
            normalized = copy.deepcopy(result)
            normalized['name_ko'] = fields['name_ko']
            normalized['franchise']['ko'] = fields['franchise_ko']
            by_original = {c['original']: c['ko'] for c in fields['characters']}
            if {c['original'] for c in result['characters']} != set(by_original):
                item['dataset_review_reason'] = 'RECOVERED_CHARACTERS_MISSING_FROM_RAW_TARGET'
                review.append(item)
                continue
            for character in normalized['characters']:
                character['ko'] = by_original[character['original']]
            item['raw_teacher_result'] = result
            item['result'] = normalized
            candidates.append(item)
        else:
            if not complete:
                item['dataset_review_reason'] = 'RAW_TARGET_INCOMPLETE_OR_NEEDS_ANNOTATION'
            review.append(item)
    args.output.mkdir(parents=True, exist_ok=True)
    for part, rows in split_rows(candidates).items():
        write_jsonl(args.output / (part + '.jsonl'), rows)
        counts[part] = len(rows)
    write_jsonl(args.output / 'review_queue.jsonl', review)
    counts['needs_review'] = len(review)
    manifest = {'counts': dict(counts), 'rules_hash': rules_hash(),
                'instruction': INSTRUCTION, 'approved_gold_count': 0,
                'note': 'All teacher labels require review. This is not an accuracy evaluation.'}
    (args.output / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'counts': dict(counts), 'approved_gold_count': 0}, ensure_ascii=False))


if __name__ == '__main__':
    main()

"""Keep changed or unresolved fields only in researched patches."""
import argparse
from collections import Counter
import json
from pathlib import Path


def delta(catalog, resolved):
    old = {r['figure_id']: r for r in catalog['records']}
    counts, new, out = Counter(), Counter(), []
    for row in resolved['records']:
        fields, patch = old[row['figure_id']]['fields'], {}
        for key, value in row['patch'].items():
            if fields.get('classification_overrides', {}).get(key, {}).get('method') == 'manual_verified':
                continue
            previous = fields.get('characters', []) if key == 'character_ko' else fields.get(key)
            same = (sorted(c['ko'] for c in previous) == sorted(c['ko'] for c in value)
                    if key == 'character_ko' else previous == value)
            if not same or fields.get('field_status', {}).get(key) != 'ready':
                patch[key] = value
                counts[key] += 1
                if fields.get('field_status', {}).get(key) != 'ready':
                    new[key] += 1
        if patch:
            out.append(dict(row, patch=patch, proofs={k: v for k, v in row['proofs'].items() if k in patch}))
    return {'records': out, 'changed_fields': dict(counts), 'new_ready': dict(new)}


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    for name in ('catalog', 'resolved', 'output'):
        p.add_argument('--' + name, type=Path, required=True)
    a = p.parse_args()
    result = delta(json.loads(a.catalog.read_text(encoding='utf-8')), json.loads(a.resolved.read_text(encoding='utf-8')))
    if a.output.exists():
        p.error('Use a new output path')
    a.output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'products': len(result['records']), **{k: v for k, v in result.items() if k != 'records'}}))

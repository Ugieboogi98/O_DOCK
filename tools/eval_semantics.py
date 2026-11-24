"""Measure split-semantics quality from existing report items.

offline (default): no model calls. Replays every committed item with the current
deterministic rules (dictionary, learned aliases from the other ready items,
kana transliteration of explicitly stated characters) and compares the
classification status with the recorded one. This is a lower bound: model-backed
steps (glossary repair, kanji names) are skipped.

live: re-runs the given failed items through the full pipeline against the local
Ollama server without writing to the database.

  python tools/eval_semantics.py --items data/private/semantics/split_queue_20261117/items
  python tools/eval_semantics.py --items ... --live --limit 20
"""
import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'backend'))

from app.services.semantic_errors import SemanticError  # noqa: E402
from app.services.semantic_neighbors import build_learned  # noqa: E402
from app.services.semantic_rules import validate_result  # noqa: E402
from app.services.split_semantics import Pipeline, grounded_dictionary, title_hints  # noqa: E402


class Offline:
    def model_digest(self, model):
        return 'offline'

    def infer(self, *args):
        raise SemanticError('OFFLINE_EVALUATION', False)


def load(items_dir):
    rows = []
    for path in sorted(Path(items_dir).glob('*.json'), key=lambda p: int(p.stem) if p.stem.isdigit() else 0):
        rows.append(json.loads(path.read_text(encoding='utf-8')))
    return rows


def offline(records, dictionary, scratch):
    committed = [r for r in records if r.get('status') in ('ready', 'partial', 'review') and r.get('fields')]
    before, after, changes = Counter(), Counter(), Counter()
    examples, changed = [], []
    for record in committed:
        # Leave-one-out: the item's own label never teaches its own alias.
        others = [(r['figure_id'], r['source']['name_original'], r['fields']) for r in committed if r is not record]
        d = {**dictionary, 'learned': build_learned(others)}
        source, name_ko = record['source'], record['fields'].get('name_ko') or record.get('translation', {}).get('name_ko')
        pipe = Pipeline(d, Offline(), scratch)
        ground = grounded_dictionary(source, d)
        title_hints(source, ground)
        pipe.name_explicit_relations(source, ground, record.get('translation') or {})
        fields, _ = validate_result(source, {'name_ko': name_ko, **ground})
        old, new = record['fields'].get('classification_status'), fields.get('classification_status')
        before[old] += 1
        after[new] += 1
        for key in ('franchise_ko', 'character_ko', 'figure_form'):
            if not record['fields'].get(key) and fields.get(key):
                changes['filled_' + key] += 1
            elif record['fields'].get(key) and fields.get(key) and record['fields'][key] != fields[key]:
                changes['changed_' + key] += 1
                if len(changed) < 60:  # label changes are the possible regressions; list them for review
                    changed.append({'figure_id': record['figure_id'], 'field': key, 'title': source['name_original'],
                                    'before': record['fields'][key], 'after': fields[key]})
        if old != new and len(examples) < 15:
            examples.append({'figure_id': record['figure_id'], 'title': source['name_original'], 'before': old, 'after': new,
                             'franchise_ko': fields.get('franchise_ko'), 'character_ko': fields.get('character_ko')})
    return {'mode': 'offline', 'items': len(committed), 'status_before': dict(before), 'status_after': dict(after),
            'field_changes': dict(changes), 'changed_labels': changed, 'examples': examples}


def live(records, dictionary, scratch, limit, base_url):
    from app.services.split_semantics import LocalModel
    failed = [r for r in records if r.get('error')][:limit]
    pipe = Pipeline(dictionary, LocalModel(base_url), scratch)
    outcome, methods, out = Counter(), Counter(), []
    for record in failed:
        try:
            t = pipe.translate(record['source'])
            methods[t['method']] += 1
            c = pipe.classify(record['source'], t)
            fields, _ = validate_result(record['source'], {'name_ko': t['name_ko'], **c['result']})
            outcome[fields['classification_status']] += 1
            out.append({'figure_id': record['figure_id'], 'name_ko': t['name_ko'], 'method': t['method'],
                        'status': fields['classification_status']})
        except SemanticError as exc:
            outcome['failed:' + exc.code] += 1
    return {'mode': 'live', 'items': len(failed), 'outcome': dict(outcome), 'translation_methods': dict(methods), 'results': out}


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--items', type=Path, required=True)
    p.add_argument('--dictionary', type=Path, default=ROOT / 'data/reference/semantic_dictionary/catalog.json')
    p.add_argument('--scratch', type=Path, default=ROOT / 'data/private/semantics/eval_cache')
    p.add_argument('--live', action='store_true')
    p.add_argument('--limit', type=int, default=20)
    p.add_argument('--base-url', default='http://127.0.0.1:11434')
    p.add_argument('--out', type=Path)
    a = p.parse_args()
    dictionary = json.loads(a.dictionary.read_text(encoding='utf-8'))
    records = load(a.items)
    report = live(records, dictionary, a.scratch, a.limit, a.base_url) if a.live else offline(records, dictionary, a.scratch)
    text = json.dumps(report, ensure_ascii=False, indent=2)
    if a.out:
        a.out.parent.mkdir(parents=True, exist_ok=True)
        a.out.write_text(text, encoding='utf-8')
    print(text)


if __name__ == '__main__':
    main()

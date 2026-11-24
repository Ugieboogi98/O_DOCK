"""Remove unverified kanji character names that split-semantics v7/v8 published.

A model's reading of a rare kanji name is often wrong (獪岳 -> 카타케이), so such names are no
longer published (see split_semantics.KANJI). This script applies the same rule to records that
were already saved: the character entries are removed, the field states are recomputed, and the
removed values are written to a report for review. Dry run unless --apply is given.

  python tools/run_split_semantics.py --repair-names --report data/private/semantics/repair_names.json [--apply]
"""
import argparse
import json
from pathlib import Path
from sqlalchemy import select, or_
from app.core.config import get_settings
from app.core.database import SessionLocal
from app.models.semantics import ProductSemantics
from app.models.entities import now
from app.services.semantic_policy import FIELDS, publication_status
from app.services.semantic_rules import normalize
from app.services.split_semantics import KANJI, known_entity_aliases


def labels(dictionary):
    """normalize(original) -> the single curated Korean label, for kanji names only."""
    found = {}
    for group in dictionary.get('domain_groups', []):
        for names, ko in group.get('characters', []):
            for name in (names.split('|') if isinstance(names, str) else names):
                found.setdefault(normalize(name), set()).add(ko)
    return {k: next(iter(v)) for k, v in found.items() if len(v) == 1}


def repaired(fields, known, canonical=None):
    canonical = canonical or {}
    characters = fields.get('characters') or []
    keep, corrected = [], []
    for c in characters:
        original = c.get('original') if isinstance(c, dict) else None
        if isinstance(original, str) and KANJI.search(original):
            label = canonical.get(normalize(original))
            if label and label != c.get('ko'):
                corrected.append({'original': original, 'ko': c.get('ko'), 'corrected_to': label})
                c = {**c, 'ko': label}
            elif not label and normalize(original) not in known:
                continue
        keep.append(c)
    removed = [c for c in characters if isinstance(c, dict) and c.get('original') not in {k.get('original') for k in keep}]
    if not removed and not corrected:
        return None, []
    out = json.loads(json.dumps(fields, ensure_ascii=False))
    out['characters'] = keep
    if corrected:
        out['corrected_characters'] = corrected
    out['character_ko'] = ' · '.join(dict.fromkeys(c['ko'] for c in keep if c.get('ko'))) or None
    states = out.setdefault('field_status', {})
    if states.get('character_ko') != 'not_applicable':
        states['character_ko'] = 'ready' if out['character_ko'] else 'missing'
    out['missing_fields'] = [k for k in FIELDS if k != 'name_ko' and not out.get(k)]
    classification = [states.get(k) for k in FIELDS if k != 'name_ko']
    out['classification_status'] = ('review' if 'review' in classification else
                                    'partial' if 'missing' in classification else 'ready')
    if removed:
        out['removed_unverified_characters'] = removed
    return out, removed + corrected


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--report', type=Path, required=True)
    p.add_argument('--apply', action='store_true')
    a = p.parse_args()
    dictionary = json.loads((get_settings().data_dir / 'reference/semantic_dictionary/catalog.json').read_text(encoding='utf-8'))
    known = known_entity_aliases(dictionary)
    canonical = labels(dictionary)
    changes = []
    with SessionLocal() as db:
        rows = db.scalars(select(ProductSemantics).where(or_(ProductSemantics.model.like('split-semantics-v7%'),
                                                             ProductSemantics.model.like('split-semantics-v8%'))))
        for row in rows:
            fields, touched = repaired(row.fields, known, canonical)
            if fields is None:
                continue
            status = publication_status(fields, row.issues or [])
            changes.append({'figure_id': row.figure_id, 'before': row.status, 'after': status,
                            'removed': [{'original': c.get('original'), 'ko': c.get('ko')} for c in touched if 'corrected_to' not in c],
                            'corrected': [c for c in touched if 'corrected_to' in c]})
            if a.apply:
                row.fields, row.status, row.updated_at = fields, status, now()
        if a.apply:
            db.commit()
    a.report.parent.mkdir(parents=True, exist_ok=True)
    a.report.write_text(json.dumps({'applied': a.apply, 'count': len(changes), 'changes': changes}, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'applied': a.apply, 'count': len(changes)}, ensure_ascii=False))


if __name__ == '__main__':
    main()

"""Read-only coverage audit. Never calls a model or changes catalog rows."""
import argparse
from collections import Counter
import json
from sqlalchemy import select
from app.core.database import SessionLocal
from app.models.entities import Figure, Manufacturer
from app.models.semantics import ProductSemantics
from app.services.product_semantics import source_of, source_hash
from scripts.product_semantics import atomic_report
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    counts, makers, unresolved = Counter(), {}, []
    with SessionLocal() as db:
        for f in db.scalars(select(Figure).order_by(Figure.id)):
            counts['total'] += 1
            maker = f.manufacturer.name
            group = makers.setdefault(maker, Counter())
            group['total'] += 1
            profile = db.get(ProductSemantics, f.id)
            state = 'missing' if profile is None else ('current' if profile.source_hash == source_hash(source_of(f)) else 'stale')
            counts[state] += 1
            group[state] += 1
            states = profile.fields.get('field_status', {}) if state == 'current' else {}
            for field in ('name_ko', 'franchise_ko', 'character_ko', 'figure_form'):
                status = states.get(field, 'missing')
                counts[field + ':' + status] += 1
                group[field + ':' + status] += 1
            if state != 'current' or any(states.get(k) != 'ready' for k in ('name_ko', 'franchise_ko', 'character_ko', 'figure_form')):
                unresolved.append({'figure_id': f.id, 'manufacturer': maker, 'name_original': f.name_original,
                    'profile_state': state, 'field_status': states, 'issues': profile.issues if profile else []})
    payload = {'counts': dict(counts), 'manufacturers': {k: dict(v) for k, v in makers.items()}, 'unresolved': unresolved}
    atomic_report(args.output, payload)
    print(json.dumps({'counts': payload['counts'], 'report': str(args.output)}, ensure_ascii=False))


if __name__ == '__main__':
    main()

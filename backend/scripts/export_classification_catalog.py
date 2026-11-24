"""Read-only research export; excludes user/account/private records."""
import argparse
from collections import Counter
import json
from pathlib import Path
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.core.database import SessionLocal
from app.models.entities import Figure
from app.models.semantics import ProductSemantics
from app.services.product_semantics import source_of, source_hash
from scripts.product_semantics import atomic_report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    records = []
    with SessionLocal() as db:
        profiles = {p.figure_id: p for p in db.scalars(select(ProductSemantics))}
        for f in db.scalars(select(Figure).options(selectinload(Figure.manufacturer), selectinload(Figure.product_line)).order_by(Figure.id)):
            source = source_of(f)
            profile = profiles.get(f.id)
            records.append({'figure_id': f.id, 'name_ko': f.name_ko, 'source': source,
                'source_hash': source_hash(source),
                'fields': profile.fields if profile and profile.source_hash == source_hash(source) else {}})
    atomic_report(args.output, {'records': records})
    print(json.dumps({'exported': len(records), 'types': dict(Counter(r['source']['type'] for r in records)),
                      'franchise_metadata': sum(bool(r['source'].get('franchise')) for r in records)}, ensure_ascii=False))


if __name__ == '__main__':
    main()

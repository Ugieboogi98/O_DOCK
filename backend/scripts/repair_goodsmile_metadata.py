"""Fill missing identifiers/prices from matching official product IDs, with checkpoints."""
import argparse
import hashlib
import json
from pathlib import Path

from sqlalchemy import select

from app.collectors.manufacturers.goodsmile import GoodSmileAdapter
from app.collectors.safe_http import SafeFetcher
from app.core.database import SessionLocal
from app.models.entities import Figure, FigureVariant, SourceDocument, ReleasePrice, CollectionJob
from app.services.import_pipeline import commit_import
from scripts.collect_goodsmile import fetch_detail
from scripts.product_semantics import atomic_report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report-dir', type=Path, required=True)
    args = parser.parse_args()
    progress = json.loads((args.report_dir / 'progress.json').read_text())
    path = args.report_dir / 'metadata_repair.json'
    repaired = json.loads(path.read_text()) if path.exists() else {}
    targets = [r for r in progress['results'].values() if r.get('state') == 'created' and not r.get('jan_code')]
    fetcher, adapter = SafeFetcher(), GoodSmileAdapter()
    for target in targets:
        key = str(target['figure_id'])
        if key in repaired and repaired[key].get('state') == 'completed':
            continue
        html, url = fetch_detail(fetcher, target['url'], target['title'])
        row = adapter.parse(html, url)
        with SessionLocal() as db:
            figure = db.get(Figure, target['figure_id'], with_for_update=True)
            variant = db.get(FigureVariant, target['variant_id'])
            jan = row.get('jan_code')
            conflict = db.scalar(select(FigureVariant.id).where(FigureVariant.jan_code == jan, FigureVariant.id != variant.id)) if jan else None
            if conflict:
                repaired[key] = {'state': 'identifier_conflict', 'other_variant_id': conflict, 'jan': jan}
            else:
                if jan and not variant.jan_code:
                    variant.jan_code = jan
                if row.get('price_amount') and not db.scalar(select(ReleasePrice.id).where(
                    ReleasePrice.variant_id == variant.id, ReleasePrice.source_url == figure.official_url, ReleasePrice.price_kind == 'official_list')):
                    db.add(ReleasePrice(variant_id=variant.id, source_url=figure.official_url, price_amount=row['price_amount'],
                                        currency='JPY', price_kind='official_list', tax_included=True))
                doc = db.scalar(select(SourceDocument).where(SourceDocument.variant_id == variant.id, SourceDocument.url == figure.official_url))
                facts = json.loads(doc.body)
                facts.update(row)
                doc.body = json.dumps(facts, ensure_ascii=False, sort_keys=True)
                doc.content_hash = hashlib.sha256(doc.body.encode()).hexdigest()
                if not db.scalar(select(CollectionJob.id).where(CollectionJob.collector == 'catalog_index', CollectionJob.status == 'pending',
                                                               CollectionJob.error_summary.contains(figure.official_url))):
                    db.add(CollectionJob(collector='catalog_index', status='pending', count=0, error_summary=json.dumps({'url': figure.official_url})))
                commit_import(db, [figure])
                repaired[key] = {'state': 'completed', 'jan': jan, 'price': row.get('price_amount')}
        atomic_report(path, repaired)
        print(json.dumps({'metadata_checked': len(repaired), 'total': len(targets), 'last': repaired[key]}), flush=True)


if __name__ == '__main__':
    main()

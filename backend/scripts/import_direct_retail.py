"""Import reviewed retail detail records with live verification and resumable reports."""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urljoin, urlsplit

from bs4 import BeautifulSoup
from sqlalchemy import select, text

from app.collectors.retailers.preview_sources import SOURCES
from app.collectors.retailers.maniahouse import future_release
from app.core.config import get_settings
from app.core.database import SessionLocal
from app.models.entities import CollectionJob, Figure, FigureVariant, Manufacturer, ProductImage, SourceDocument
from app.models.retail import RetailListing, RetailOffer
from app.services.enrichment import download_image
from app.services.retail_collection import save_offer
from app.services.semantic_queue import enqueue
from scripts.preview_domestic_prices import PreviewFetcher
from scripts.product_semantics import atomic_report


def identity(item):
    return item['retailer_code'] + ':' + str(item['retailer_product_id'])


def verify_source(items, report_dir):
    fetcher = PreviewFetcher(items[0]['retailer_code'])
    for item in items:
        code = item['retailer_code']
        path = report_dir / (identity(item).replace(':', '_') + '.json')
        if path.exists():
            continue
        pid = str(item['retailer_product_id'])
        url = ('https://' + SOURCES[code]['host'] + '/product/detail.html?product_no=' + pid
               if code != 'figurefarm' else 'https://' + SOURCES[code]['host'] + '/shop/detail.php?pno=' + pid)
        record = {'key': identity(item), 'archive': item, 'verified': False}
        try:
            html = fetcher.fetch(url)
            parsed = SOURCES[code]['parse'](html, url)
            parsed.update(observed_at=datetime.now(timezone.utc).isoformat(),
                          source_sha256=hashlib.sha256(html.encode()).hexdigest())
            if parsed.get('jan_ean') and item.get('jan_ean') and parsed['jan_ean'].zfill(14) != item['jan_ean'].zfill(14):
                raise ValueError('LIVE_IDENTIFIER_CHANGED')
            # Preserve checksum-checked archive identifiers when the price parser has no JAN field.
            parsed['jan_ean'] = parsed.get('jan_ean') or item.get('jan_ean')
            parsed['model_code'] = parsed.get('model_code') or item.get('manufacturer_model_code')
            parsed['manufacturer_raw'] = item.get('manufacturer_actual_as_reported') or parsed.get('manufacturer_raw')
            soup = BeautifulSoup(html, 'html.parser')
            images = [item.get('main_image_url'), *item.get('detail_image_urls', [])]
            for node in soup.select('meta[property="og:image"], .keyImg img, .imgArea .thumbnail img'):
                images.append(urljoin(url, node.get('content') or node.get('data-src') or node.get('src') or ''))
            images = list(dict.fromkeys(u for u in images if u and urlsplit(u).scheme == 'https' and urlsplit(u).path not in ('', '/')))
            record.update(verified=True, parsed=parsed, images=images)
        except Exception as exc:
            record['error'] = type(exc).__name__ + ':' + str(exc)[:100]
        atomic_report(path, record)
        print(json.dumps({'verified': record['verified'], 'key': identity(item)}, ensure_ascii=False), flush=True)


def choose_variant(db, item, row, decision):
    listing = db.scalar(select(RetailListing).where(
        RetailListing.source_code == item['retailer_code'],
        RetailListing.external_product_id == str(item['retailer_product_id']), RetailListing.option_key == ''))
    if listing and listing.catalog_variant_id and listing.match_status == 'MATCHED':
        return db.get(FigureVariant, listing.catalog_variant_id), False
    if decision.get('variant_id'):
        variant = db.get(FigureVariant, decision['variant_id'])
        if not variant:
            raise ValueError('REVIEWED_VARIANT_NOT_FOUND')
        if row.get('jan_ean') and variant.jan_code and row['jan_ean'].zfill(14) != variant.jan_code.zfill(14):
            raise ValueError('REVIEWED_VARIANT_JAN_CONFLICT')
        return variant, False
    jan = row.get('jan_ean')
    if jan:
        variants = list(db.scalars(select(FigureVariant).where(FigureVariant.jan_code.in_([jan, jan.zfill(14), jan.lstrip('0')]))))
        if len(variants) > 1:
            raise ValueError('AMBIGUOUS_CATALOG_JAN')
        if variants:
            return variants[0], False
    figure = db.scalar(select(Figure).where(Figure.official_url == row['product_url']))
    if figure:
        return figure.variants[0], False
    maker = db.scalar(select(Manufacturer).where(Manufacturer.name == 'ETC'))
    if maker is None:
        maker = Manufacturer(name='ETC', name_ko='ETC', official_url='')
        db.add(maker)
        db.flush()
    title = item.get('displayed_korean_title') or item['original_title']
    scale = item.get('scale')
    if not scale:
        match = re.search(r'(?<!\d)1\s*/\s*\d+', title)
        scale = re.sub(r'\s+', '', match.group()) if match else None
    figure = Figure(manufacturer_id=maker.id, name_original=item['original_title'], name_ko=title,
                    franchise=item.get('work'), character=item.get('character'), scale=scale,
                    material=item.get('material'), type='figure', quality='retailer_metadata', official_url=row['product_url'])
    db.add(figure)
    db.flush()
    variant = FigureVariant(figure_id=figure.id, variant_key='source-page', jan_code=jan,
                            sku=row.get('model_code'), edition=item.get('edition'),
                            release_date=item.get('release_month'),
                            release_precision='month' if item.get('release_month') else None)
    db.add(variant)
    db.flush()
    return variant, True


def import_record(record, decision, commit):
    item = record['archive']
    if not record['verified']:
        return {'key': identity(item), 'state': 'verification_failed', 'error': record.get('error')}
    row = dict(record['parsed'])
    from app.services.collection_preferences import excluded_retail_product
    if excluded_retail_product(row):
        return {'key': identity(item), 'state': 'excluded', 'reason': 'MANUFACTURER_EXCLUDED'}
    if row['availability'] == 'IN_STOCK' and future_release(item.get('displayed_schedule_text')):
        row['availability'] = 'PREORDER'
        row['availability_basis'] = 'Future release month displayed on the reviewed detail page'
    row['archive_metadata'] = item
    row['match'] = {'status': 'REVIEW_REQUIRED', 'reason': decision['reason']}
    # Refurbished goods remain recorded but do not compete with new-stock prices.
    refurbished = bool(re.search('리퍼|중고', item.get('displayed_korean_title', '')))
    row['conditional_price'] = row.get('conditional_price', False) or refurbished
    row.setdefault('warnings', [])
    if refurbished:
        row['warnings'] = [*row['warnings'], 'REFURBISHED_CONDITION']
    with SessionLocal() as db:
        if db.bind.dialect.name == 'postgresql':
            db.execute(text('SELECT pg_advisory_xact_lock(2026102203)'))
        outcome = save_offer(db, item['retailer_code'], row)
        listing = db.scalar(select(RetailListing).where(
            RetailListing.source_code == item['retailer_code'],
            RetailListing.external_product_id == str(item['retailer_product_id']), RetailListing.option_key == ''))
        if outcome == 'stale':
            return {'key': identity(item), 'state': 'stale_observation'}
        result = {'key': identity(item), 'state': decision['action'], 'offer': outcome}
        if decision['action'] == 'link_or_create':
            variant, created = choose_variant(db, item, row, decision)
            figure = variant.figure
            listing.catalog_variant_id = variant.id
            listing.match_status = 'MATCHED'
            listing.match_evidence = {'method': 'agent_reviewed_archive_and_live_detail',
                                      'reason': decision['reason'], 'jan_ean': row.get('jan_ean')}
            body = json.dumps({'archive': item, 'live': row}, ensure_ascii=False, sort_keys=True)
            doc = db.scalar(select(SourceDocument).where(SourceDocument.variant_id == variant.id, SourceDocument.url == row['product_url']))
            if doc is None:
                doc = SourceDocument(variant_id=variant.id, url=row['product_url'], source_type='retailer_detail',
                                     title=item['displayed_korean_title'], language='ko', body=body,
                                     content_hash=hashlib.sha256(body.encode()).hexdigest())
                db.add(doc)
            image_results = []
            # Import the archive's photos and fill a missing cover from the live page.
            desired = list(dict.fromkeys([item.get('main_image_url'), *item.get('detail_image_urls', [])]))
            desired = [u for u in desired if u]
            if not desired and record['images']:
                desired = record['images'][:1]
            for image_url in desired:
                exists = db.scalar(select(ProductImage.id).where(ProductImage.variant_id == variant.id, ProductImage.source_url == image_url))
                if exists:
                    image_results.append({'state': 'existing', 'url': image_url})
                    continue
                if not commit:
                    continue
                try:
                    local = download_image(image_url, get_settings().media_dir)
                    db.add(ProductImage(variant_id=variant.id, image_url=local, source_url=image_url, usage_status='personal_local'))
                    image_results.append({'state': 'downloaded', 'url': image_url})
                except Exception as exc:
                    image_results.append({'state': 'failed', 'url': image_url, 'error': type(exc).__name__})
            db.flush()
            task = enqueue(db, figure)
            result['semantic_queued'] = task is not None
            if created:
                db.add(CollectionJob(collector='catalog_index', status='pending', count=0,
                                     error_summary=json.dumps({'url': figure.official_url})))
            result.update(state='created' if created else 'linked', figure_id=figure.id, variant_id=variant.id,
                          images=image_results)
        else:
            listing.match_status = 'REJECTED' if decision['action'] == 'excluded' else 'REVIEW_REQUIRED'
            listing.catalog_variant_id = None
            listing.match_evidence = {'reason': decision['reason']}
        if commit:
            db.commit()
        else:
            db.rollback()
        return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--input', required=True, type=Path)
    parser.add_argument('--plan', required=True, type=Path)
    parser.add_argument('--report-dir', required=True, type=Path)
    parser.add_argument('--commit', action='store_true')
    args = parser.parse_args()
    items = json.loads(args.input.read_text(encoding='utf-8'))
    plan = json.loads(args.plan.read_text(encoding='utf-8'))
    keys = [identity(item) for item in items]
    if len(keys) != len(set(keys)) or set(keys) != set(plan):
        raise ValueError('IMPORT_PLAN_MUST_COVER_EVERY_UNIQUE_LISTING')
    args.report_dir.mkdir(parents=True, exist_ok=True)
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(verify_source, [p for p in items if p['retailer_code'] == code], args.report_dir)
                   for code in sorted({p['retailer_code'] for p in items})]
        for future in futures:
            future.result()
    backup = args.report_dir / 'before_import.json'
    if args.commit and not backup.exists():
        with SessionLocal() as db:
            listings = [r for r in db.scalars(select(RetailListing))
                        if r.source_code + ':' + r.external_product_id in plan]
            listing_ids = [r.id for r in listings]
            offers = list(db.scalars(select(RetailOffer).where(RetailOffer.listing_id.in_(listing_ids))))
            saved = {name: [{c.name: getattr(row, c.name) for c in row.__table__.columns} for row in rows]
                     for name, rows in [('listings', listings), ('offers', offers)]}
            atomic_report(backup, json.loads(json.dumps(saved, default=str)))
    results = []
    for item in items:
        path = args.report_dir / (identity(item).replace(':', '_') + '.json')
        record = json.loads(path.read_text(encoding='utf-8'))
        try:
            result = import_record(record, plan[identity(item)], args.commit)
        except Exception as exc:
            result = {'key': identity(item), 'state': 'failed', 'error': type(exc).__name__ + ':' + str(exc)[:120]}
        results.append(result)
        atomic_report(args.report_dir / 'import_results.json', results)
        print(json.dumps(result, ensure_ascii=False), flush=True)
    summary = {'committed': args.commit, 'total': len(items), 'counts': dict(Counter(r['state'] for r in results))}
    atomic_report(args.report_dir / 'summary.json', summary)
    print(json.dumps(summary), flush=True)


if __name__ == '__main__':
    main()

"""Resumable collection from Good Smile Company's public manufacturer-filtered search."""
import argparse
import hashlib
import json
from pathlib import Path
import re
import signal
from urllib.parse import urlencode, urljoin, quote_plus

from bs4 import BeautifulSoup
import httpx
from filelock import FileLock
from sqlalchemy import select, text, or_

from app.collectors.manufacturers.goodsmile import GoodSmileAdapter
from app.collectors.safe_http import SafeFetcher
from app.core.config import get_settings
from app.core.database import SessionLocal
from app.models.entities import CollectionJob, Figure, FigureVariant, Manufacturer, ProductImage, ReleasePrice, SourceDocument, now
from app.services.enrichment import download_image, extract_media
from app.services.import_pipeline import commit_import
from app.services.seed_import import seed
from scripts.product_semantics import atomic_report

HOST = 'https://www.goodsmile.com'
FILTER = {'search_keyword': '', 'search_over18': False,
          'search_category': [1, 15, 59, 63, 57, 51, 61, 21, 64, 20], 'search_maker': [1],
          'search_title': [], 'search_status': '0', 'release_date_from': '', 'release_date_to': '',
          'search_bonus': False, 'search_exclusive': False, 'search_sale': False,
          'search_sales_origin': False, 'tag': []}
ACCESSORIES = re.compile('おようふく|衣装セット|きぐるみ|ボディ|フェイスメーカー|髪型パーツ|アフターパーツ|おでかけポーチ|台座セット|イーゼル|組み立て式プラモデル')


def fetch_detail(fetcher, url, title):
    detail_url = url + '/' + quote_plus(title) if title else url
    try:
        return fetcher.fetch_page(detail_url)
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code != 404:
            raise
    # Slashes in a displayed BOX/reissue title need the site's canonical redirect.
    try:
        return fetcher.fetch_page(url)
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 404:
            raise ValueError('PRODUCT_NO_LONGER_AVAILABLE') from None
        raise


def store(row, cover):
    row.update(source_url=row['official_url'], checked_at=now().isoformat())
    row['source_text'] = json.dumps(row, ensure_ascii=False, sort_keys=True)
    with SessionLocal() as db:
        db.execute(text('SELECT pg_advisory_xact_lock(2026102203)'))
        product_id = re.search(r'/product/(\d+)', row['official_url'])[1]
        aliases = [HOST + '/' + language + '/product/' + product_id for language in ('ja', 'en')]
        figure = db.scalar(select(Figure).where(or_(Figure.official_url.in_(aliases),
            *(Figure.official_url.startswith(alias + '/', autoescape=True) for alias in aliases))))
        variant = None
        if figure:
            variant = figure.variants[0]
        elif row.get('jan_code'):
            matches = list(db.scalars(select(FigureVariant).where(FigureVariant.jan_code == row['jan_code'])))
            if len(matches) > 1:
                raise ValueError('AMBIGUOUS_JAN')
            variant = matches[0] if matches else None
            figure = variant.figure if variant else None
        created = figure is None
        if created:
            seed(db, [row], commit=False)
            figure = db.scalar(select(Figure).where(Figure.official_url == row['official_url']))
            variant = figure.variants[0]
            db.add(CollectionJob(collector='catalog_index', status='pending', count=0,
                                 error_summary=json.dumps({'url': figure.official_url})))
        else:
            for field in ('franchise', 'scale', 'height_mm', 'material'):
                if getattr(figure, field) is None and row.get(field) is not None:
                    setattr(figure, field, row[field])
            if figure.manufacturer.name == 'ETC':
                previous_url = figure.official_url
                figure.manufacturer_id = db.scalar(select(Manufacturer.id).where(Manufacturer.name == 'Good Smile Company'))
                figure.official_url = row['official_url']
                figure.quality = 'official_metadata'
                for job in db.scalars(select(CollectionJob).where(CollectionJob.collector == 'catalog_index', CollectionJob.status == 'pending')):
                    payload = json.loads(job.error_summary)
                    if payload.get('url') == previous_url:
                        job.error_summary = json.dumps({'url': figure.official_url})
            if not db.scalar(select(SourceDocument.id).where(SourceDocument.variant_id == variant.id, SourceDocument.url == row['official_url'])):
                db.add(SourceDocument(variant_id=variant.id, title=row['name_original'], url=row['official_url'],
                                      source_type='official_metadata_extract', language='ja', body=row['source_text'],
                                      content_hash=hashlib.sha256(row['source_text'].encode()).hexdigest()))
            if row.get('price_amount') and not db.scalar(select(ReleasePrice.id).where(
                    ReleasePrice.variant_id == variant.id, ReleasePrice.source_url == row['official_url'], ReleasePrice.price_kind == 'official_list')):
                db.add(ReleasePrice(variant_id=variant.id, price_amount=row['price_amount'], currency='JPY',
                                    price_kind='official_list', tax_included=True, source_url=row['official_url']))
        if cover and not db.scalar(select(ProductImage.id).where(ProductImage.variant_id == variant.id, ProductImage.source_url == cover['source'])):
            db.add(ProductImage(variant_id=variant.id, source_url=cover['source'], image_url=cover['local'], usage_status='personal_local'))
        commit_import(db, [figure])
        return {'state': 'created' if created else 'linked_existing', 'figure_id': figure.id, 'variant_id': variant.id,
                'url': row['official_url'], 'title': row['name_original'], 'jan_code': row.get('jan_code'), 'image_saved': bool(cover)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--limit', type=int, default=500)
    parser.add_argument('--report-dir', required=True, type=Path)
    args = parser.parse_args()
    if args.limit < 1:
        parser.error('--limit must be positive')
    args.report_dir.mkdir(parents=True, exist_ok=True)
    stop = False
    def stopping(*_):
        nonlocal stop
        stop = True
    signal.signal(signal.SIGTERM, stopping)
    signal.signal(signal.SIGINT, stopping)
    with FileLock(str(args.report_dir / 'worker.lock'), timeout=0):
        path = args.report_dir / 'progress.json'
        progress = json.loads(path.read_text(encoding='utf-8')) if path.exists() else {
            'created': 0, 'existing': 0, 'skipped': 0, 'failed': 0, 'offset': 0, 'queue': [], 'results': {}}
        progress.update(state='running', target=args.limit)
        progress.pop('last_error', None)
        fetcher, adapter = SafeFetcher(), GoodSmileAdapter()
        def persist():
            progress['updated_at'] = now().isoformat()
            atomic_report(path, progress)
        persist()
        try:
            while progress['created'] < args.limit and not stop:
                if not progress['queue']:
                    url = HOST + '/ja/search/list?' + urlencode({'filter': json.dumps(FILTER, separators=(',', ':')),
                        'orderBy': 1, 'limit': 60, 'offset': progress['offset'], 'couponId': 'null', 'searchIndex': -1})
                    soup = BeautifulSoup(fetcher.fetch(url), 'html.parser')
                    total = soup.select_one('#search_result_total_count')
                    if total:
                        progress['listing_total'] = int(total.get_text().replace(',', ''))
                    for node in soup.select('a.p-product-list__link[href]'):
                        title = node.select_one('h2')
                        url = urljoin(HOST, node['href'])
                        if adapter.is_product_url(url) and url not in progress['results']:
                            progress['queue'].append({'url': url, 'title': title.get_text(' ', strip=True) if title else ''})
                    progress['offset'] += 60
                    persist()
                    if not progress['queue']:
                        progress['state'] = 'exhausted'
                        break
                item = progress['queue'][0]
                url = item['url']
                progress['active_url'] = url
                persist()
                if ACCESSORIES.search(item['title']):
                    result = {'state': 'excluded_accessory', 'title': item['title']}
                else:
                    # A slug from the displayed title avoids the site's ID-only redirect.
                    try:
                        html, final_url = fetch_detail(fetcher, url, item['title'])
                        row = adapter.parse(html, final_url)
                        if ACCESSORIES.search(row.get('specifications', {}).get('仕様', '')) and 'プラモデル' in row.get('specifications', {}).get('仕様', ''):
                            raise ValueError('MODEL_KIT')
                        cover = None
                        images = extract_media(html, final_url)
                        image_errors = []
                        for image_url in images[:2]:
                            try:
                                host, rule = fetcher.validate(row['official_url'])
                                fetcher._pace(host, rule)
                                cover = {'source': image_url, 'local': download_image(image_url, get_settings().media_dir)}
                                break
                            except Exception as exc:
                                image_errors.append(type(exc).__name__)
                        result = store(row, cover)
                        if not cover:
                            result['image_errors'] = image_errors
                    except ValueError as exc:
                        result = {'state': 'rejected', 'reason': str(exc)[:100]}
                progress['results'][url] = result
                progress['queue'].pop(0)
                key = {'created': 'created', 'linked_existing': 'existing', 'rejected': 'skipped', 'excluded_accessory': 'skipped'}[result['state']]
                progress[key] += 1
                persist()
                print(json.dumps({k: progress[k] for k in ('created', 'existing', 'skipped', 'state')}, ensure_ascii=False), flush=True)
            if progress['created'] >= args.limit:
                progress['state'] = 'completed'
            elif stop:
                progress['state'] = 'interrupted'
        except Exception as exc:
            progress['state'] = 'blocked'
            progress['last_error'] = type(exc).__name__ + ':' + str(exc)[:120]
            raise
        finally:
            persist()


if __name__ == '__main__':
    main()

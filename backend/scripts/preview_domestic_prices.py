"""Explicit, bounded public-price preview. Writes a report and queries catalog identities."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from urllib.parse import urlsplit

import httpx
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.collectors.safe_http import SafeFetcher, CollectionDenied
from app.collectors.retailers.preview_sources import SOURCES
from app.core.database import SessionLocal
from app.models.entities import FigureVariant
from app.search_agents.matching import match_product, norm
from scripts.product_semantics import atomic_report
from app.services.retail_collection import save_offer
from app.services.collection_preferences import excluded_retail_product


class PreviewFetcher(SafeFetcher):
    def __init__(self, source='maniahouse'):
        super().__init__()
        self.source = SOURCES[source]
        self.policy = {self.source['host']: {'enabled': True, 'paths': self.source['paths'], 'delay_seconds': 3}}
        self.requests = 0

    def _request(self, url):
        if not self.allowed_path(url):
            raise CollectionDenied('PREVIEW_PATH_NOT_ALLOWED')
        host, rule = self.validate(url)
        self.check_robots(url, host)
        self._pace(host, rule)
        self.requests += 1
        with httpx.Client(timeout=15, follow_redirects=False, trust_env=False,
                          headers={'User-Agent': self.s.user_agent}) as client:
            with client.stream('GET', url) as response:
                if response.status_code != 200:
                    raise CollectionDenied('HTTP_' + str(response.status_code))
                if 'html' not in response.headers.get('content-type', '').lower():
                    raise CollectionDenied('UNEXPECTED_CONTENT_TYPE')
                body = bytearray()
                for block in response.iter_bytes():
                    body.extend(block)
                    if len(body) > self.source.get('max_html_bytes',3_000_000):
                        raise CollectionDenied('BODY_TOO_LARGE')
        html = body.decode('utf-8', errors='replace')
        if any(marker in html.lower() for marker in ('veritas-hub.cafe24.com/challenge', '<title>captcha', 'request rejected')):
            raise CollectionDenied('ACCESS_CHALLENGE')
        return html, url

    def allowed_path(self, url):
        return url == self.source['url'] or urlsplit(url).path in ('/product/detail.html', '/shop/detail.php')


def matches(db, row):
    if not row['jan_ean']:
        return {'status': 'REVIEW_REQUIRED', 'reason': 'NO_VERIFIED_IDENTIFIER', 'candidates': []}
    candidates = list(db.scalars(select(FigureVariant).where(FigureVariant.jan_code == row['jan_ean'])))
    values = []
    for variant in candidates:
        figure = variant.figure
        target = {'jan_code': variant.jan_code, 'sku': variant.sku,
                  'manufacturer': figure.manufacturer.name, 'edition': variant.edition,
                  'reissue_no': variant.reissue_no, 'scale': figure.scale}
        candidate = {'jan_code': row['jan_ean'], 'manufacturer': row['manufacturer_raw']}
        state = match_product(target, candidate)
        reason = 'JAN_CANDIDATE_REQUIRES_VARIANT_CONFIRMATION'
        if norm(target['manufacturer']) != norm(candidate['manufacturer']):
            state = 'MATCH_REVIEW_REQUIRED'
            reason = 'MANUFACTURER_CONFIRMATION_REQUIRED'
        if row['has_shop_bonus'] or row['conditional_price']:
            state = 'MATCH_REVIEW_REQUIRED'
            reason = 'BONUS_OR_PAYMENT_CONDITION'
        # Raw JAN matches propose candidates, with edition/scale/bonus checked by the reviewer.
        values.append({'variant_id': variant.id, 'title': figure.name_original,
                       'identifier_match': state, 'reason': reason})
    return {'status': 'REVIEW_REQUIRED' if values else 'UNMATCHED',
            'reason': 'CATALOG_CANDIDATES' if values else 'NO_JAN_CANDIDATE', 'candidates': values}


def collect_source(name, limit, report, output, commit=False):
    source = SOURCES[name]
    result = {'name': source['name'], 'state': 'running', 'parsed': 0,
              'items': [], 'errors': [], 'storage': {'inserted': 0, 'updated': 0, 'stale': 0},
              'policy_status': 'REQUIRES_PERMISSION_FOR_SERVICE_REUSE'}
    report['sources'][name] = result
    fetcher = PreviewFetcher(name)
    try:
        urls = source['discover'](fetcher.fetch(source['url']))[:limit]
        result['discovered_sample'] = len(urls)
        if not urls:
            raise CollectionDenied('NO_PRODUCT_LINKS')
        with SessionLocal() as db:
            for url in urls:
                html = fetcher.fetch(url)
                if '/intro/adult_im.html' in html:
                    result['restricted'] = result.get('restricted',0) + 1
                    continue
                try:
                    row = source['parse'](html, url)
                except ValueError as exc:
                    result['errors'].append({'url': url, 'code': str(exc)})
                    atomic_report(output, report)
                    continue
                if excluded_retail_product(row):
                    result['excluded_manufacturer'] = result.get('excluded_manufacturer', 0) + 1
                    continue
                row['retailer_code'] = name
                row['source_sha256'] = hashlib.sha256(html.encode()).hexdigest()
                row['observed_at'] = datetime.now(timezone.utc).isoformat()
                row['match'] = matches(db, row)
                if commit:
                    outcome = save_offer(db, name, row)
                    db.commit()
                    result['storage'][outcome] += 1
                    report['database_written'] = True
                result['items'].append(row)
                report['items'].append(row)
                result['parsed'] = len(result['items'])
                atomic_report(output, report)
        result['state'] = 'completed' if not result['errors'] else 'partial'
    except (CollectionDenied, httpx.HTTPError, SQLAlchemyError, ValueError) as exc:
        result['state'] = 'stopped'
        result['errors'].append({'code': str(exc) if isinstance(exc, CollectionDenied) else type(exc).__name__})
    finally:
        result['page_requests'] = fetcher.requests
        report['errors'].extend(dict(error, source=name) for error in result['errors'])
        atomic_report(output, report)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute', action='store_true', help='Run a one-time public preview')
    parser.add_argument('--limit', type=int, default=5, help='Maximum products per source, 1 to 100')
    parser.add_argument('--commit', action='store_true', help='Save observed listings and current offers')
    parser.add_argument('--sources', nargs='+', choices=list(SOURCES), default=list(SOURCES))
    parser.add_argument('--report-dir', type=Path, required=True)
    args = parser.parse_args()
    if not args.execute:
        parser.error('--execute is required for this one-time preview')
    if not 1 <= args.limit <= 100:
        parser.error('--limit must be between 1 and 100')
    args.report_dir.mkdir(parents=True, exist_ok=False)
    names = list(dict.fromkeys(args.sources))
    report = {'source': names[0] if len(names) == 1 else 'multiple', 'sources': {},
              'dry_run': not args.commit, 'database_written': False,
              'checked_at': datetime.now(timezone.utc).isoformat(), 'items': [], 'errors': [],
              'policy_status': 'REQUIRES_PERMISSION_FOR_SERVICE_REUSE', 'state': 'running'}
    output = args.report_dir / 'preview.json'
    atomic_report(output, report)
    for name in names:
        result = collect_source(name, args.limit, report, output, commit=args.commit)
        print(json.dumps({'source': name, 'state': result['state'], 'parsed': result['parsed'],
                          'storage': result['storage'], 'errors': result['errors']}), flush=True)
    report['state'] = 'completed' if not report['errors'] else 'partial'
    report['product_page_requests'] = sum(s['page_requests'] for s in report['sources'].values())
    report['parsed'] = len(report['items'])
    if len(names) == 1:
        report['discovered_sample'] = report['sources'][names[0]].get('discovered_sample', 0)
    atomic_report(output, report)
    print(json.dumps({'state': report['state'], 'parsed': report['parsed'], 'errors': report['errors']}))
    return 0 if report['state'] == 'completed' else 1


if __name__ == '__main__':
    raise SystemExit(main())

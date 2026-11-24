"""Resumable one-time full domestic catalog collection, one request at a time per store."""
import argparse
from concurrent.futures import ThreadPoolExecutor, wait
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import signal
import threading

import httpx
from filelock import FileLock, Timeout
from sqlalchemy.exc import SQLAlchemyError

from app.collectors.retailers.catalog import canonical_page, canonical_product, discover_page, EXCLUDED_LABEL
from app.collectors.retailers.checkpoint import Checkpoint
from app.collectors.retailers.preview_sources import SOURCES
from app.collectors.safe_http import CollectionDenied
from app.core.database import SessionLocal
from app.services.retail_collection import save_offer
from app.services.collection_preferences import excluded_retail_product
from scripts.preview_domestic_prices import PreviewFetcher, matches
from scripts.product_semantics import atomic_report


class CatalogFetcher(PreviewFetcher):
    def __init__(self, source):
        self.source_code = source
        super().__init__(source)
        self.policy[self.source['host']]['paths'] = ['/']

    def allowed_path(self, url):
        return canonical_page(url, self.source_code) == url or canonical_product(url, self.source_code) == url


def fetch_page(fetcher, url, stop):
    for attempt in range(3):
        try:
            return fetcher.fetch(url)
        except httpx.HTTPError:
            if attempt == 2 or stop.wait(2 ** (attempt + 1)):
                raise


def run_source(name, root, commit, stop):
    folder = root / name
    folder.mkdir(parents=True, exist_ok=True)
    lock = FileLock(str(folder / 'worker.lock'))
    try:
        lock.acquire(timeout=0)
    except Timeout:
        return {'state': 'already_running'}
    queue = Checkpoint(folder / 'checkpoint.sqlite')
    progress_path = folder / 'progress.json'
    progress = json.loads(progress_path.read_text(encoding='utf-8')) if progress_path.exists() else {}
    progress.update(source=name, name=SOURCES[name]['name'], state='running', dry_run=not commit,
                    mode='full_catalog_one_time', last_error=None,
                    process_id=os.getpid(), platform=platform.system())
    storage = progress.setdefault('storage', {'inserted': 0, 'updated': 0, 'stale': 0})
    fetcher = CatalogFetcher(name)
    consecutive_parse_errors = 0

    def persist():
        progress['counts'] = queue.counts()
        progress['updated_at'] = datetime.now(timezone.utc).isoformat()
        atomic_report(progress_path, progress)

    queue.add(pages=['https://' + SOURCES[name]['host'] + '/'])
    persist()
    try:
        while not stop.is_set():
            job = queue.next()
            if not job:
                progress['state'] = 'completed'
                break
            progress['active_url'] = job['url']
            persist()
            try:
                html = fetch_page(fetcher, job['url'], stop)
                if job['kind'] == 'page':
                    pages, products = discover_page(html, job['url'], name)
                    queue.add(pages=pages, products=products)
                    queue.finish(job)
                    persist()
                    continue
                if '/intro/adult_im.html' in html:
                    queue.finish(job, 'restricted', 'AGE_VERIFICATION_REQUIRED')
                    persist()
                    continue
                try:
                    row = SOURCES[name]['parse'](html, job['url'])
                except ValueError as exc:
                    queue.finish(job, 'failed', str(exc)[:100])
                    consecutive_parse_errors += 1
                    if consecutive_parse_errors >= 10:
                        progress.update(state='blocked', last_error='CONSECUTIVE_PRODUCT_PARSE_FAILURES')
                        break
                    persist()
                    continue
                if excluded_retail_product(row):
                    queue.finish(job, 'excluded', 'MANUFACTURER_EXCLUDED')
                    persist()
                    continue
                if EXCLUDED_LABEL.search(row['title_raw']):
                    queue.finish(job, 'excluded', 'NON_CATALOG_PAYMENT_PAGE')
                    persist()
                    continue
                row.update(retailer_code=name, source_sha256=hashlib.sha256(html.encode()).hexdigest(),
                           observed_at=datetime.now(timezone.utc).isoformat())
                with SessionLocal() as db:
                    row['match'] = matches(db, row)
                    if commit:
                        outcome = save_offer(db, name, row)
                        db.commit()
                        storage[outcome] += 1
                queue.finish(job)
                consecutive_parse_errors = 0
                persist()
            except (CollectionDenied, httpx.HTTPError, SQLAlchemyError) as exc:
                code = str(exc) if isinstance(exc, CollectionDenied) else type(exc).__name__
                if code in ('HTTP_404', 'HTTP_410'):
                    queue.finish(job, 'unavailable', code)
                    persist()
                    continue
                queue.finish(job, 'pending', code[:100])
                progress.update(state='blocked', last_error=code[:100])
                break
        if stop.is_set():
            progress['state'] = 'interrupted'
    finally:
        persist()
        queue.close()
        lock.release()
    return progress


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--sources', nargs='+', choices=list(SOURCES), default=list(SOURCES))
    parser.add_argument('--report-dir', required=True, type=Path, help='Existing directory resumes its unfinished frontier')
    parser.add_argument('--commit', action='store_true')
    args = parser.parse_args()
    args.report_dir.mkdir(parents=True, exist_ok=True)
    names = list(dict.fromkeys(args.sources))
    stop = threading.Event()
    signal.signal(signal.SIGTERM, lambda *_: stop.set())
    signal.signal(signal.SIGINT, lambda *_: stop.set())
    unexpected = {}
    with ThreadPoolExecutor(max_workers=len(names)) as executor:
        futures = {executor.submit(run_source, name, args.report_dir, args.commit, stop): name for name in names}
        pending = set(futures)
        while pending:
            finished, pending = wait(pending, timeout=10)
            for future in finished:
                try:
                    future.result()
                except Exception as exc:
                    unexpected[futures[future]] = type(exc).__name__
            sources = {}
            for name in names:
                path = args.report_dir / name / 'progress.json'
                if path.exists():
                    sources[name] = json.loads(path.read_text(encoding='utf-8'))
            state = 'running' if pending else 'completed'
            if not pending and any(source['state'] != 'completed' for source in sources.values()):
                state = 'partial'
            if not pending and unexpected:
                state = 'failed'
            summary = {'state': state, 'sources': sources, 'unexpected_errors': unexpected,
                       'updated_at': datetime.now(timezone.utc).isoformat()}
            atomic_report(args.report_dir / 'progress.json', summary)
            print(json.dumps({'state': state, 'sources': {
                name: {'state': data['state'], 'counts': data.get('counts', {}), 'last_error': data.get('last_error')}
                for name, data in sources.items()}, 'unexpected_errors': unexpected}), flush=True)
    return 1 if unexpected else 0


if __name__ == '__main__':
    raise SystemExit(main())

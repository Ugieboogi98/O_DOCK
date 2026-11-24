"""One bounded, resumable official catalog pass, excluding Good Smile."""
import argparse
import json
from pathlib import Path
from datetime import datetime, timezone
from bs4 import BeautifulSoup
from sqlalchemy import select
from app.core.database import SessionLocal
from app.models.entities import Figure
from app.services.enrichment import enrich_html
from app.services.semantic_queue import enqueue

from app.collectors.safe_http import SafeFetcher
from app.services.catalog_ingest import adapter_for, collect_one, retry_pending_indexes

SOURCES = [
    ('TAITO', 'https://www.taito.co.jp/api/PrizeProduct/?aspMemberID=0000000002&offset=0&limit=120&sortName=TaitoPrizeNew&isDesc=true'),
    ('Bandai Spirits', 'https://tamashiiweb.com/api/site-item/search_item.php?sort=1&per_page=60&current_page=1&area=japan'),
    ('Bandai Spirits', 'https://bsp-prize.jp/search/'),
    ('MegaHouse', 'https://megahobby.jp/products/'),
    ('FuRyu', 'https://furyu-hm.com/collections/scale-figures'),
    ('FuRyu', 'https://furyuprize.com/'),
    ('SEGA', 'https://segaplaza.jp/prize/'),
    ('Kotobukiya', 'https://www.kotobukiya.co.jp/product/'),
]

class CachedFetcher(SafeFetcher):
    """Reuse one detail response for media, respecting the site's crawl interval."""
    def __init__(self):
        super().__init__()
        self.cached = None

    def fetch_page(self, url):
        response = super().fetch_page(url)
        self.cached = (url, response)
        return response

    def fetch(self, url):
        if self.cached and self.cached[0] == url:
            return self.cached[1][0]
        return super().fetch(url)

def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--report-dir', type=Path, required=True)
    p.add_argument('--commit', action='store_true')
    p.add_argument('--max-new', type=int, default=30)
    p.add_argument('--manufacturer', action='append')
    p.add_argument('--source', action='append')
    p.add_argument('--retry-failed', action='store_true')
    p.add_argument('--skip-retail', action='store_true', help='Only for isolated official-source repairs')
    args = p.parse_args()
    if args.max_new < 1:
        p.error('--max-new must be positive')
    args.report_dir.mkdir(parents=True, exist_ok=True)
    path = args.report_dir / 'progress.json'
    state = json.loads(path.read_text()) if path.exists() else {'sources': {}, 'products': {}}
    if args.retry_failed:
        state['products'] = {u:r for u,r in state['products'].items() if r['status'] != 'failed'}
    fetcher = CachedFetcher()
    def save():
        state['updated_at'] = datetime.now(timezone.utc).isoformat()
        tmp = path.with_suffix('.tmp')
        tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding='utf-8')
        tmp.replace(path)
    state['state'] = 'running' if args.commit else 'discovering'
    save()
    for maker, url in SOURCES:
        if args.manufacturer and maker not in args.manufacturer:
            continue
        if args.source and url not in args.source:
            continue
        info = state['sources'].get(url, {'manufacturer': maker})
        if 'urls' not in info:
            try:
                html, final = fetcher.fetch_page(url)
                (args.report_dir / (maker.replace(' ', '_') + '_' + str(SOURCES.index((maker,url))) + '.html')).write_text(html, encoding='utf-8')
                if '/api/PrizeProduct/' in url:
                    rows = json.loads(html)
                    urls = ['https://www.taito.co.jp/taito-prize/' + x['ProductID'] for x in rows if '\u30d5\u30a3\u30ae\u30e5\u30a2' in x['ProductName']]
                elif '/api/site-item/' in url:
                    rows = json.loads(html)['data']
                    urls = ['https://tamashiiweb.com/item/' + x['tamashiiWebId'] + '/' for x in rows if x.get('tamashiiWebId')]
                else:
                    urls = adapter_for(final).discover(html, final)
                    if 'bsp-prize' in url:
                        soup = BeautifulSoup(html, 'html.parser')
                        keep = ('\u30d5\u30a3\u30ae\u30e5\u30a2', 'Grandista', 'ESPRESTO', 'GLITTER', 'MASTERLISE', 'Noir Edge', 'Glasscape')
                        urls = [u for u in urls if any(any(k in a.get_text() for k in keep) for a in soup.select('a[href]') if a['href'].rstrip('/') == u.replace('https://bsp-prize.jp','').rstrip('/') or a['href'].rstrip('/') == u.rstrip('/'))]
                info.update(urls=urls, final_url=final)
            except Exception as exc:
                info['error'] = f'{type(exc).__name__}: {str(exc)[:250]}'
            state['sources'][url] = info
            save()
        print(json.dumps({'source': url, **{k:v for k,v in info.items() if k != 'urls'}, 'discovered': len(info.get('urls', []))}), flush=True)
        if not args.commit:
            continue
        created = sum(v.get('manufacturer') == maker and v.get('status', '').startswith('created') for v in state['products'].values())
        for product in info.get('urls', []):
            if created >= args.max_new:
                break
            if product in state['products']:
                continue
            try:
                status = collect_one(fetcher, product, enrich=False)
                result = {'manufacturer': maker, 'status': status}
                created += status.startswith('created')
                if status.startswith('created'):
                    try:
                        html = fetcher.fetch(product)
                        with SessionLocal() as db:
                            f = db.scalar(select(Figure).where(Figure.official_url == product))
                            result['figure_id'] = f.id
                            result['media'] = [enrich_html(db, f, v, html, product, images=True, max_images=3) for v in f.variants]
                            enqueue(db, f)
                            db.commit()
                    except Exception as exc:
                        result['media_error'] = f'{type(exc).__name__}: {str(exc)[:200]}'
            except Exception as exc:
                result = {'manufacturer': maker, 'status': 'failed', 'error': f'{type(exc).__name__}: {str(exc)[:250]}'}
            state['products'][product] = result
            save()
            print(json.dumps({'url': product, **result}), flush=True)
    if args.commit:
        state['index_retry'] = retry_pending_indexes()
        if not args.skip_retail:
            from app.services.domestic_collection_round import run_round
            state['domestic'] = run_round(args.report_dir / 'retail',20)
    errors = any(r.get('status') == 'failed' for r in state['products'].values()) or any(r.get('error') for r in state['sources'].values())
    state['state'] = ('completed_with_errors' if errors else 'completed') if args.commit else 'discovered'
    save()

if __name__ == '__main__':
    main()

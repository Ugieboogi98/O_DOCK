"""Repair product-specific media for this dated import; preserve prior products."""
import json
import argparse
from pathlib import Path
from sqlalchemy import select
from app.core.database import SessionLocal
from app.models.entities import Figure, Manufacturer
from app.collectors.safe_http import SafeFetcher
from app.services.enrichment import enrich_html
from app.services.semantic_queue import enqueue
from scripts.collect_bandai_with_images import repair_images

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--min-id', type=int, required=True)
    parser.add_argument('--max-id', type=int, required=True)
    parser.add_argument('--manufacturer', action='append')
    parser.add_argument('--report-name', default='image_repair.json')
    args = parser.parse_args()
    if args.min_id > args.max_id:
        parser.error('Invalid bounded product ID range')
    path = Path('/report') / args.report_name
    report = json.loads(path.read_text()) if path.exists() else {}
    fetcher = SafeFetcher()
    with SessionLocal() as db:
        rows = [(f.id, f.official_url, m.name) for f,m in db.execute(select(Figure,Manufacturer).join(Manufacturer).where(Figure.id.between(args.min_id,args.max_id), Manufacturer.name.in_(['Bandai Spirits','Hot Toys'])))]
    for fid, url, maker in rows:
        if args.manufacturer and maker not in args.manufacturer:
            continue
        if str(fid) in report:
            continue
        try:
            html = fetcher.fetch(url)
            if maker == 'Bandai Spirits' and 'tamashiiweb.com' in url:
                result = repair_images(fetcher, fid, html, url, 3)
            else:
                with SessionLocal() as db:
                    figure = db.get(Figure, fid)
                    result = [enrich_html(db,figure,v,html,url,images=True,max_images=3) for v in figure.variants]
                    enqueue(db, figure)
                    db.commit()
            report[str(fid)] = {'url':url,'result':result}
        except Exception as exc:
            report[str(fid)] = {'url':url,'error':str(exc)[:200]}
        temp = path.with_suffix('.tmp')
        temp.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
        temp.replace(path)
        print(fid, json.dumps(report[str(fid)],ensure_ascii=False),flush=True)

if __name__ == '__main__':
    main()

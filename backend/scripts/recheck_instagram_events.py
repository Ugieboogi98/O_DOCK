"""Re-extract already saved posts; no API calls, no product writes."""
import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
from sqlalchemy import create_engine
from app.core.config import get_settings
from app.integrations.instagram.events import extract, default_works
from app.integrations.instagram.store import save_posts
from app.integrations.instagram.review import render
from app.integrations.instagram.event_identity import finalize


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input',type=Path,required=True)
    p.add_argument('--output-dir',type=Path,required=True)
    p.add_argument('--commit',action='store_true')
    args=p.parse_args()
    args.output_dir.mkdir(parents=True,exist_ok=False)
    report=json.loads(args.input.read_text(encoding='utf-8'))
    works=default_works()
    extractor=lambda text:extract(text,works)
    contextual_extractor=lambda row:finalize(extract(row['caption'],works,published_at=row['timestamp']),report['collected_at'])
    for row in report['posts']:row['candidate']=contextual_extractor(row)
    engine=create_engine(get_settings().database_url) if args.commit else None
    try:
        if engine:
            for username in report['sources']:
                rows=[{k:r[k] for k in ('id','caption','permalink','timestamp','media_type')}
                    for r in report['posts'] if r['source_username']==username]
                with engine.begin() as c:
                    report['sources'][username].update(save_posts(c,username,rows,extractor,contextual_extractor))
        from collections import Counter
        report['summary']=dict(Counter(r['candidate']['status'] for r in report['posts']))
        report['rechecked_at']=datetime.now(timezone.utc).isoformat()
        report['recheck_api_requests']=0
        (args.output_dir/'posts.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
        (args.output_dir/'review.html').write_text(render(report),encoding='utf-8')
        print(json.dumps({'summary':report['summary'],'sources':report['sources'],'recheck_api_requests':0},ensure_ascii=False))
    finally:
        if engine:engine.dispose()


if __name__=='__main__':main()

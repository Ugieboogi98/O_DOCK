"""Enrich an existing private event review with official API images, without changing captions or events."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import logging
from pathlib import Path
from app.integrations.instagram.config import InstagramSettings
from app.integrations.instagram.probe import run_probe
from app.integrations.instagram.client import MetaClient,ProbeError
from app.integrations.instagram.images import ImageDownloader,image_assets
from app.integrations.instagram.review import render
from app.integrations.instagram.event_identity import finalize


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--env-file',type=Path)
    p.add_argument('--input',type=Path,required=True)
    p.add_argument('--output-dir',type=Path,required=True)
    args=p.parse_args()
    for name in ('httpx','httpcore'):logging.getLogger(name).disabled=True
    args.output_dir.mkdir(parents=True,exist_ok=False)
    settings=InstagramSettings.from_local_env(args.env_file)
    gate=run_probe(settings,live=True)
    (args.output_dir/'availability.json').write_text(json.dumps(gate,ensure_ascii=False,indent=2),encoding='utf-8')
    if not gate.get('next_phase_eligible'):
        print(json.dumps({'decision':'NO-GO','reason':gate.get('reason')}));return 2
    report=json.loads(args.input.read_text(encoding='utf-8'))
    report['images_collected_at']=datetime.now(timezone.utc).isoformat()
    report['image_source_report_sha256']=hashlib.sha256(args.input.read_bytes()).hexdigest()
    report['image_usage']='PRIVATE_REVIEW_ONLY_NOT_SITE_PUBLICATION'
    report['image_errors']=[]
    client=MetaClient(settings);downloader=ImageDownloader(args.output_dir/'media')
    try:
        for username in report['sources']:
            saved={r['id']:r for r in report['posts'] if r['source_username']==username
                and finalize(r['candidate'],report['collected_at'])['status']!='EXCLUDED_ENDED_BEFORE_COLLECTION'}
            if not saved:continue
            for row in saved.values():row['images']=[];row['image_status']='NOT_IN_CURRENT_API_RESPONSE'
            try:
                payload,_=client.discovery(username,include_images=True)
                discovery=payload.get('business_discovery',{})
                if discovery.get('username','').casefold()!=username:raise ProbeError('DISCOVERY_USERNAME_MISMATCH')
                media=discovery.get('media',{}).get('data',[])
                if not isinstance(media,list) or len(media)>settings.instagram_collection_media_limit:raise ProbeError('MEDIA_LIMIT_OR_SCHEMA_INVALID')
                for post in media:
                    if not isinstance(post,dict) or str(post.get('id')) not in saved:continue
                    row=saved[str(post['id'])]
                    assets=image_assets(post)
                    row['images']=[downloader.download(a) for a in assets]
                    row['image_status']='PROCESSED' if assets else 'API_IMAGE_NOT_PROVIDED'
                    row['image_provenance']={'account':username,'external_post_id':row['id'],'permalink':row['permalink']}
            except ProbeError as exc:
                report['image_errors'].append({'account':username,**exc.safe()})
                if exc.code in ('TOKEN_INVALID_OR_EXPIRED','PERMISSION_DENIED','RATE_LIMITED','RETRY_LATER'):break
    finally:
        downloader.close();client.close()
        images=[v for row in report['posts'] for v in row.get('images',[])]
        report['image_summary']=dict(Counter(v['status'] for v in images))
        report['image_summary']['posts_with_images']=sum(any(i['status']=='DOWNLOADED' for i in row.get('images',[])) for row in report['posts'])
        (args.output_dir/'posts.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
        (args.output_dir/'review.html').write_text(render(report),encoding='utf-8')
    print(json.dumps({'image_summary':report['image_summary'],'errors':report['image_errors'],
        'site_published':False,'db_written':False},ensure_ascii=False))
    return 1 if report['image_errors'] else 0


if __name__=='__main__':raise SystemExit(main())

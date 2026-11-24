"""Collect bounded official website event facts; --commit publishes through the existing event feed."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
from urllib.parse import urljoin
from zoneinfo import ZoneInfo
from app.integrations.event_web import adapters as a
from app.integrations.event_web.client import PublicClient, FetchError
from app.integrations.event_web.sources import SOURCES, DISABLED_SOURCES
from app.integrations.instagram.events import default_works
from app.integrations.instagram.event_identity import finalize

def collect(name,client,works,checked_at,limit=24):
    source=SOURCES[name];documents=[];errors=[]
    def get(url):
        body=client.get(url);documents.append(url);return body
    def attempt(url,parser):
        try:return parser(get(url),url)
        except (FetchError,ValueError,KeyError,TypeError) as exc:
            errors.append({'url':url,'error':str(exc)[:120]});return []
    rows=[]
    if name=='duex':
        for page in ('21','22','21_2','22_2','21_3','22_3'):
            rows.extend(attempt('https://www.duex.co.kr/page/'+page,a.duex))
    elif name=='spacegalleria':
        home=get(source['url'])
        urls={urljoin(source['url'],n['href']).split('?')[0] for n in a.soup(home).select('a[href]') if re.match(r'(?:https://spacegalleria.co.kr)?/exhibition/\d+',n['href'])}
        for url in sorted(urls)[:limit]:rows.extend(attempt(url,a.space))
    elif name=='animate':
        # First page includes upcoming/current announcements; never traverse historical archives.
        listed=a.animate_list(get(source['url']),source['url'])
        for item in listed[:limit]:
            d=finalize(a.candidate(item,works),checked_at)
            if d['status']=='EXCLUDED_ENDED_BEFORE_COLLECTION':rows.append(item);continue
            try:rows.append(a.animate_detail(get(item['url']),item))
            except (FetchError,ValueError) as exc:errors.append({'url':item['url'],'error':str(exc)[:120]})
    elif name=='aniplus':
        get(source['url'])
        payload=json.loads(get('https://api.aniplustv.com:3060/api/v2/offline-collabo?page=1&perPage=30&sort=RECENT'))
        rows=a.aniplus(payload)
        for item in rows:
            if finalize(a.candidate(item,works),checked_at)['status']=='EXCLUDED_ENDED_BEFORE_COLLECTION':continue
            ident=item['url'].split('collaboId=')[-1]
            try:
                detail=json.loads(get('https://api.aniplustv.com:3060/api/v2/offline-collabo/'+ident))
                # Keep only explicit factual location fields, never comments/user profiles.
                places=detail.get('shops') or detail.get('shopList') or detail.get('stores') or []
                if isinstance(places,list):
                    names=[p.get('name') or p.get('shopName') for p in places if isinstance(p,dict)]
                    if names and all(isinstance(n,str) for n in names):item['venue']=' / '.join(names)
            except (FetchError,ValueError,AttributeError) as exc:errors.append({'url':item['url'],'error':str(exc)[:120]})
    elif name=='popcondplay':
        home=get(source['url'])
        urls=list(dict.fromkeys(urljoin(source['url'],n['href']) for n in a.soup(home).select('a[href]') if re.fullmatch(r'/reserve/view/\d+',n['href'])))
        for url in urls[:limit]:rows.extend(attempt(url,a.pop))
    elif name=='daewon':
        home=get(source['url'])
        urls=[urljoin(source['url'],n['href']).split('?')[0] for n in a.soup(home).select('a[href]') if re.search(r'/board/news-event/\d+',n['href']) and re.search(r'팝업|展|특별전|전시|콜라보|페어',a.text(n),re.I)]
        for url in list(dict.fromkeys(urls))[:limit]:rows.extend(attempt(url,a.daewon))
    elif name=='agf':rows=attempt(source['url'],a.agf)
    else:get(source['url'])  # G-STAR remains blocked when robots disallows its details.
    unique={item['url']:item for item in rows}
    result=[]
    for item in unique.values():
        candidate=finalize(a.candidate(item,works),checked_at)
        candidate['last_checked_at']=checked_at
        heading=item['title']
        if re.search(r'(?:행사|전시|개최|운영)\s*(?:전면\s*)?취소|개최\s*중지',heading):candidate['event_status']='CANCELLED'
        elif re.search(r'(?:행사|전시|개최)\s*연기',heading):candidate['event_status']='POSTPONED'
        identity=item['url']+(':'+item['title'] if name=='duex' else '')
        result.append({'id':hashlib.sha256(identity.encode()).hexdigest(),'permalink':item['url'],
            'caption':'', 'timestamp':item.get('published_at') or checked_at,'media_type':'FACTS',
            'facts':item,'candidate':candidate})
    return result,{'documents':len(documents),'document_urls':documents,'parsed':len(result),'errors':errors,
        'summary':dict(Counter(r['candidate']['status'] for r in result)),
        'access_status':'PASS' if documents else 'NO_VERIFIED_DOCUMENT',
        'parse_status':'PASS' if result else 'NO_STRUCTURED_EVENT',
        'reuse_status':'FACTS_AND_LINK_ONLY_NO_BODY_OR_IMAGE_REPUBLICATION',
        'terms_url':source.get('terms_url')}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--report-dir',required=True,type=Path)
    p.add_argument('--cache-dir',required=True,type=Path)
    p.add_argument('--sources',nargs='+',choices=list(SOURCES),default=list(SOURCES))
    p.add_argument('--commit',action='store_true')
    args=p.parse_args();args.report_dir.mkdir(parents=True,exist_ok=False)
    now=datetime.now(timezone.utc).isoformat();works=default_works()
    report={'checked_at':now,'cutoff_date':datetime.now(ZoneInfo('Asia/Seoul')).date().isoformat(),
        'sources':{},'posts':[],'disabled_sources':DISABLED_SOURCES,'paid_api_called':False,'automatic_collection_started':False}
    client=PublicClient(args.cache_dir);engine=None
    if args.commit:
        from sqlalchemy import create_engine
        from app.core.config import get_settings
        engine=create_engine(get_settings().database_url,pool_pre_ping=True)
    def persist():
        (args.report_dir/'events.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    try:
        for name in args.sources:
            try:
                rows,info=collect(name,client,works,now)
                report['sources'][name]=info
                # Excluded old announcements are counted, without keeping source body/image copies.
                report['posts'].extend(dict(row,source_name=name) for row in rows if row['candidate']['status']!='EXCLUDED_ENDED_BEFORE_COLLECTION')
                if engine:
                    from app.integrations.instagram.store import save_posts
                    with engine.begin() as connection:
                        counts=save_posts(connection,SOURCES[name]['name'],rows,lambda _:None,
                            lambda row:row['candidate'],platform='website',source_url=SOURCES[name]['url'])
                    info['storage']=counts
                print(json.dumps({'source':name,**{k:v for k,v in info.items() if k not in ('document_urls','errors')}}),flush=True)
            except (FetchError,ValueError,KeyError,TypeError) as exc:
                report['sources'][name]={'status':'FAILED','error':str(exc)[:160]}
                print(json.dumps({'source':name,**report['sources'][name]}),flush=True)
            persist()
    finally:
        report['http_requests']=client.requests;client.close()
        if engine:engine.dispose()
        persist()
    return 0

if __name__=='__main__':raise SystemExit(main())

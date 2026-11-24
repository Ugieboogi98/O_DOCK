"""Read-only public events and private source candidates. No implicit approvals."""
from datetime import date, datetime
from zoneinfo import ZoneInfo
from functools import lru_cache
import json
from pathlib import Path
import re
from sqlalchemy import select, inspect
from app.integrations.instagram.store import posts, candidates, sources, events, links
from app.integrations.instagram.event_identity import key as event_key
from app.integrations.event_web.images import image_url


def period(start, end, today=None):
    today=today or datetime.now(ZoneInfo('Asia/Seoul')).date()
    try:
        first=date.fromisoformat(start) if start else None
        last=date.fromisoformat(end) if end else None
    except (ValueError,TypeError):return 'UNKNOWN'
    if not first or not last:return 'UNKNOWN'
    if last<first:return 'UNKNOWN'
    if last<today:return 'ENDED'
    if first>today:return 'UPCOMING'
    return 'ONGOING'


@lru_cache(maxsize=16)
def read_image_report(file, modified):
    try:return json.loads(Path(file).read_text(encoding='utf-8'))
    except (OSError,ValueError):return {}


def private_images(data_dir):
    root=(Path(data_dir)/'private/instagram').resolve()
    index={}
    if not root.exists():return index
    for path in sorted(root.glob('*/posts.json'),reverse=True):
        if not path.resolve().is_relative_to(root):continue
        report=read_image_report(str(path),path.stat().st_mtime_ns)
        if not report.get('image_summary'):continue
        for row in report.get('posts',[]):
            key=str(row.get('id',''))
            if key in index:continue
            values=[]
            for item in row.get('images',[]):
                relative=item.get('path','')
                if item.get('status')!='DOWNLOADED' or not re.fullmatch(r'media/[a-f0-9]{64}\.(?:jpg|png|webp)',relative):continue
                image=(path.parent/relative).resolve()
                if image.is_relative_to(root) and image.is_file():values.append(image)
            if values:index[key]={'files':values,'caption':row.get('caption','')}
    return index


def candidate_items(db,data_dir):
    if not inspect(db.get_bind()).has_table('event_candidates'):return []
    images=private_images(data_dir)
    query=(select(candidates.c.id,candidates.c.data,posts.c.id.label('post_id'),posts.c.external_id,
                  posts.c.caption,posts.c.permalink,posts.c.published_at,posts.c.fetched_at,posts.c.platform,sources.c.username)
        .join(posts,posts.c.id==candidates.c.post_id).join(sources,sources.c.id==posts.c.source_id)
        .where(candidates.c.status=='PENDING_REVIEW').order_by(posts.c.published_at.desc(),posts.c.id.desc()))
    groups={}
    for r in db.execute(query).mappings():
        d=r['data'];key=event_key(d) or d.get('duplicate_key') or 'post:'+str(r['post_id'])
        media=images.get(r['external_id'],{}) if r['platform']=='instagram' else {}
        files=media.get('files',[]) if media.get('caption')==r['caption'] else []
        image_urls=[f"/api/admin/event-candidates/images/{r['post_id']}/{i}" for i in range(len(files))]
        if r['platform']=='website':
            image_urls=[url for value in d.get('image_urls',[]) if (url:=image_url(value))]
        source={'username':r['username'],'url':r['permalink'],'caption':r['caption'] if r['platform']=='instagram' else '',
                'platform':r['platform'],'published_at':d.get('published_at') if r['platform']=='website' else r['published_at'].isoformat(),
                'last_checked_at':d.get('last_checked_at') or r['fetched_at'].isoformat(),
                'content_license_status':d.get('content_license_status','API_MEDIA')}
        if key in groups:
            groups[key]['sources'].append(source)
            groups[key]['images'].extend(v for v in image_urls if v not in groups[key]['images'])
            if d.get('booking_url') and not groups[key].get('booking_url'):groups[key]['booking_url']=d['booking_url']
            continue
        groups[key]={'id':r['id'],'title':d.get('title') or '행사 정보 확인 중',
            'categories':d.get('categories',[]),'franchises':d.get('franchises',[]),
            'start_date':d.get('start_date'),'end_date':d.get('end_date'),'venue':d.get('venue'),
            'period_text':d.get('period_text'),'year_inferred':d.get('year_inferred',False),
            'periods':d.get('periods',[]),'venues':d.get('venues',[]),
            'period':schedule_period(d),'verification':'PENDING_REVIEW',
            'images':image_urls,'sources':[source],'warnings':d.get('warnings',[]),
            'evidence':d.get('evidence',[])}
        groups[key].update(booking_url=d.get('booking_url'),address=d.get('address'),last_checked_at=source['last_checked_at'])
    return list(groups.values())


def schedule_period(data,today=None):
    if data.get('event_status') in ('CANCELLED','POSTPONED','SOLD_OUT'):return data['event_status']
    if data.get('start_date') and data.get('end_date'):return period(data['start_date'],data['end_date'],today)
    states=[period(p['start_date'],p['end_date'],today) for p in data.get('periods',[])]
    if 'ONGOING' in states:return 'ONGOING'
    if 'UPCOMING' in states:return 'UPCOMING'
    if states and all(s=='ENDED' for s in states):return 'ENDED'
    return 'UNKNOWN'


def public_items(db):
    if not inspect(db.get_bind()).has_table('events'):return []
    rows=[]
    for r in db.execute(select(events).where(events.c.status=='APPROVED').order_by(events.c.id.desc())).mappings():
        references=db.execute(select(posts.c.permalink,sources.c.username).join(links,links.c.post_id==posts.c.id)
            .join(sources,sources.c.id==posts.c.source_id).where(links.c.event_id==r['id'])).mappings()
        # Images remain private until separate display rights approval is implemented.
        rows.append({'id':r['id'],'title':r['title'],'categories':[],
            'franchises':[r['franchise']] if r['franchise'] else [],'start_date':r['start_date'],
            'end_date':r['end_date'],'venue':r['venue'],'period':period(r['start_date'],r['end_date']),
            'verification':'APPROVED','images':[], 'sources':[{'url':s['permalink'],'username':s['username']} for s in references]})
    return rows


def filtered(items,*,q='',category='',when='',area='',sort='latest',page=1,size=12):
    options={'areas':sorted({place for v in items for place in (v.get('venues') or ([v['venue']] if v.get('venue') else []))}),
             'categories':sorted({c for v in items for c in v.get('categories',[])})}
    q=q.strip().casefold()
    selected=[v for v in items if
        (not q or q in ' '.join([v['title'],v.get('venue') or '',*v.get('franchises',[])]).casefold())
        and (not category or category in v.get('categories',[]))
        and (not when or v['period']==when)
        and (not area or area==(v.get('venue') or '') or area in v.get('venues',[]))]
    def boundary(v,field):
        values=[p[field] for p in v.get('periods',[]) if p.get(field)]
        return v.get(field) or ((min(values) if field=='start_date' else max(values)) if values else '')
    if sort=='opening':selected.sort(key=lambda v:(not boundary(v,'start_date'),boundary(v,'start_date'),-v['id']))
    if sort=='ending':selected.sort(key=lambda v:(not boundary(v,'end_date'),boundary(v,'end_date'),-v['id']))
    return {'items':selected[(page-1)*size:page*size],'total':len(selected),'page':page,'size':size,
            'options':options,'private_preview':any(v['verification']=='PENDING_REVIEW' for v in items)}

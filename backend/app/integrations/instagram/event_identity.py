"""Canonical event identity and initial-collection lifecycle, separate from post IDs."""
from datetime import date, datetime, timezone
from zoneinfo import ZoneInfo
import hashlib
import json
import re
import unicodedata


def venue_key(value):
    text=unicodedata.normalize('NFKC',value or '').casefold()
    text=re.sub(r'덕스\s*\(\s*duex\s*\)|duex\s*\(\s*덕스\s*\)|덕스','duex',text)
    text=re.sub(r'\([^)]*더샵센트럴스타[^)]*\)','',text)
    text=re.sub(r'\([^)]*(?:서울|마포구|주소)[^)]*\)','',text)
    text=text.replace('플라자','plaza').replace('홍대점','홍대')
    text=re.sub(r'(\d+)\s*f\b',r'\1층',text)
    return re.sub(r'[\W_]+','',text)


def key(data):
    venues=data.get('venues') or ([data['venue']] if data.get('venue') else [])
    periods=data.get('periods') or ([{'start_date':data['start_date'],'end_date':data['end_date']}]
        if data.get('start_date') and data.get('end_date') else [])
    identity=sorted(data.get('franchises',[])) or ([data['identity_title'].casefold()] if data.get('identity_title') else [])
    if not periods or not venues or not identity:return None
    signature=[identity,sorted(data.get('categories',[])),
               sorted((p['start_date'],p['end_date']) for p in periods),sorted({venue_key(v) for v in venues})]
    return hashlib.sha256(json.dumps(signature,ensure_ascii=False).encode()).hexdigest()


def finalize(data,first_collected_at):
    """Exclude old announcements on first encounter, retain events that end later."""
    result=dict(data)
    stamp=first_collected_at
    if isinstance(stamp,str):stamp=datetime.fromisoformat(stamp.replace('Z','+00:00'))
    if stamp.tzinfo is None:stamp=stamp.replace(tzinfo=timezone.utc)
    initial_day=stamp.astimezone(ZoneInfo('Asia/Seoul')).date()
    if result['status']=='EXCLUDED_ENDED_BEFORE_COLLECTION' and result.get('is_subculture_relevant') and result.get('categories'):
        result['status']='PENDING_REVIEW'
    end=result.get('end_date')
    if not end and result.get('periods'):end=max(p['end_date'] for p in result['periods'])
    if result['status']=='PENDING_REVIEW' and end and date.fromisoformat(end)<initial_day:
        result['status']='EXCLUDED_ENDED_BEFORE_COLLECTION'
    result['first_collected_at']=stamp.isoformat()
    result['collection_cutoff_date']=initial_day.isoformat()
    result['duplicate_key']=key(result)
    return result

"""Separate event tables. No imports or writes to catalog/product models."""
from datetime import datetime, timezone
from .event_identity import finalize
import hashlib
import json
from sqlalchemy import (MetaData, Table, Column, Integer, String, Text, JSON, DateTime,
                        ForeignKey, UniqueConstraint, Index, select, insert, update)

metadata = MetaData()
sources = Table('event_sources', metadata,
    Column('id', Integer, primary_key=True), Column('platform', String(24), nullable=False),
    Column('username', String(100), nullable=False), Column('url', Text, nullable=False),
    Column('status', String(60), nullable=False), Column('last_success_at', DateTime(timezone=True)),
    UniqueConstraint('platform', 'username'))
posts = Table('source_posts', metadata,
    Column('id', Integer, primary_key=True), Column('source_id', ForeignKey('event_sources.id'), nullable=False),
    Column('platform', String(24), nullable=False), Column('external_id', String(100), nullable=False),
    Column('permalink', Text, nullable=False), Column('caption', Text, nullable=False),
    Column('published_at', DateTime(timezone=True), nullable=False), Column('media_type', String(40)),
    Column('fetched_at', DateTime(timezone=True), nullable=False), Column('content_hash', String(64), nullable=False),
    Column('raw_payload', JSON, nullable=False), UniqueConstraint('platform', 'external_id'))
candidates = Table('event_candidates', metadata,
    Column('id', Integer, primary_key=True), Column('post_id', ForeignKey('source_posts.id'), unique=True, nullable=False),
    Column('status', String(50), nullable=False), Column('data', JSON, nullable=False),
    Column('duplicate_key', String(64)), Column('updated_at', DateTime(timezone=True), nullable=False))
events = Table('events', metadata,
    Column('id', Integer, primary_key=True), Column('status', String(50), nullable=False),
    Column('title', Text, nullable=False), Column('franchise', Text), Column('start_date', String(10)),
    Column('end_date', String(10)), Column('venue', Text), Column('revision_history', JSON, nullable=False))
links = Table('event_source_links', metadata,
    Column('id', Integer, primary_key=True), Column('event_id', ForeignKey('events.id'), nullable=False),
    Column('post_id', ForeignKey('source_posts.id'), nullable=False), UniqueConstraint('event_id', 'post_id'))
Index('ix_source_posts_published_at', posts.c.published_at)
Index('ix_event_candidates_status', candidates.c.status)
Index('ix_event_candidates_duplicate_key', candidates.c.duplicate_key)
Index('ix_events_status_start_date', events.c.status, events.c.start_date)
Index('ix_events_franchise', events.c.franchise)


def save_posts(connection, username, rows, extractor, contextual_extractor=None, *, platform='instagram', source_url=None):
    now = datetime.now(timezone.utc)
    source = connection.execute(select(sources).where(sources.c.platform == platform, sources.c.username == username)).mappings().first()
    if source:
        sid = source['id']
    else:
        sid = connection.execute(insert(sources).values(platform=platform, username=username,
            url=source_url or f'https://www.instagram.com/{username}/', status='DISCOVERY_VERIFIED_NOT_SCHEDULED' if platform=='instagram' else 'PUBLIC_FACTS_COLLECTED')).inserted_primary_key[0]
    counts = {'inserted': 0, 'updated': 0, 'unchanged': 0, 'excluded_ended':0}
    for row in rows:
        content={'facts':row.get('facts'), 'permalink':row['permalink']} if platform=='website' else row
        digest = hashlib.sha256(json.dumps(content, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
        old = connection.execute(select(posts).where(posts.c.platform == platform, posts.c.external_id == row['id'])).mappings().first()
        if old and old['source_id'] != sid:
            raise ValueError('POST_SOURCE_IDENTITY_CHANGED')
        data = contextual_extractor(row) if contextual_extractor else extractor(row['caption'])
        first_seen=(old['raw_payload'].get('first_collected_at') or old['fetched_at']) if old else now
        data=finalize(data,first_seen)
        if data['status']=='EXCLUDED_ENDED_BEFORE_COLLECTION':
            counts['excluded_ended']+=1
            if not old:continue
        raw={**row,'first_collected_at':data['first_collected_at']}
        values = dict(permalink=row['permalink'], caption=row['caption'], media_type=row['media_type'],
            published_at=datetime.fromisoformat(row['timestamp'].replace('Z', '+00:00')),
            fetched_at=now, raw_payload=raw, content_hash=digest)
        if old:
            pid = old['id']
            connection.execute(update(posts).where(posts.c.id == pid).values(**values))
            counts['unchanged' if old['content_hash'] == digest else 'updated'] += 1
        else:
            pid = connection.execute(insert(posts).values(source_id=sid, platform=platform, external_id=row['id'], **values)).inserted_primary_key[0]
            counts['inserted'] += 1
        previous = connection.execute(select(candidates).where(candidates.c.post_id == pid)).mappings().first()
        if platform=='website' and previous:
            history=list(previous['data'].get('change_history',[]))
            tracked=('title','start_date','end_date','venue','categories','event_status')
            before={k:previous['data'].get(k) for k in tracked};after={k:data.get(k) for k in tracked}
            if before!=after:history.append({'checked_at':now.isoformat(),'before':before,'after':after})
            data['change_history']=history[-20:]
        data['last_checked_at']=now.isoformat()
        # Collected candidates feed the public event list; excluded statuses stay hidden.
        state = previous['status'] if previous and old and old['content_hash'] == digest and previous['status'] == 'APPROVED' else data['status']
        cv = dict(status=state, data=data, duplicate_key=data['duplicate_key'], updated_at=now)
        if previous:
            connection.execute(update(candidates).where(candidates.c.id == previous['id']).values(**cv))
        else:
            connection.execute(insert(candidates).values(post_id=pid, **cv))
        if old and old['content_hash'] != digest:
            for event in connection.execute(select(events).join(links, links.c.event_id == events.c.id).where(links.c.post_id == pid)).mappings():
                history = list(event['revision_history'] or []) + [{k: event[k] for k in ('status','title','franchise','start_date','end_date','venue')} | {'reason':'SOURCE_CHANGED', 'at':now.isoformat()}]
                connection.execute(update(events).where(events.c.id == event['id']).values(status='PENDING_REVIEW', revision_history=history))
    connection.execute(update(sources).where(sources.c.id == sid).values(last_success_at=now))
    return counts

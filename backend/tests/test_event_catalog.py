from datetime import date, datetime, timezone
import json
from types import SimpleNamespace
from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine,insert,update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.api.events import router
from app.core.database import get_db
from app.integrations.instagram.store import metadata,sources,posts,candidates,events,links
from app.services.event_catalog import period,filtered


@pytest.fixture
def event_client(tmp_path,monkeypatch):
    from app.core import security
    from app.api import events as event_api
    monkeypatch.setattr(security,'get_settings',lambda:SimpleNamespace(admin_token='test-admin'))
    monkeypatch.setattr(event_api,'get_settings',lambda:SimpleNamespace(data_dir=tmp_path))
    e=create_engine('sqlite://',connect_args={'check_same_thread':False},poolclass=StaticPool)
    metadata.create_all(e);sessions=sessionmaker(e)
    now=datetime.now(timezone.utc)
    with e.begin() as c:
        c.execute(insert(sources).values(id=1,platform='instagram',username='duex.official',url='https://www.instagram.com/duex.official/',status='VERIFIED'))
        for ident in (1,2):
            c.execute(insert(posts).values(id=ident,source_id=1,platform='instagram',external_id=str(100+ident),permalink=f'https://www.instagram.com/p/Post{ident}/',caption='private caption',published_at=now,media_type='IMAGE',fetched_at=now,content_hash='a'*64,raw_payload={}))
            c.execute(insert(candidates).values(post_id=ident,status='PENDING_REVIEW',updated_at=now,data={
                'title':'비공개 팝업','categories':['POPUP_STORE'],'franchises':['원피스'],'venue':'홍대',
                'start_date':'2026-11-15','end_date':'2026-11-25','duplicate_key':'shared'}))
    folder=tmp_path/'private/instagram/20261112_images';(folder/'media').mkdir(parents=True)
    name='a'*64+'.jpg';(folder/'media'/name).write_bytes(b'\xff\xd8\xffPRIVATE_IMAGE')
    (folder/'posts.json').write_text(json.dumps({'image_summary':{'DOWNLOADED':1},'posts':[{
        'id':'102','caption':'private caption','images':[{'status':'DOWNLOADED','path':'media/'+name}]}]}))
    app=FastAPI();app.include_router(router)
    def db():
        with sessions() as session:yield session
    app.dependency_overrides[get_db]=db
    with TestClient(app) as client:yield client,e
    e.dispose()


def test_collected_events_are_visible_without_admin_connection(event_client):
    client,_=event_client
    r=client.get('/api/events');assert r.status_code==200
    assert r.json()['total']==1
    assert r.json()['items'][0]['verification']=='SOURCE_COLLECTED'
    assert '/admin/' not in r.text and 'data/private' not in r.text
    assert client.get('/api/admin/event-candidates').status_code==404


def test_public_grouping_filters_and_images_need_no_token(event_client):
    client,_=event_client
    r=client.get('/api/events?category=POPUP_STORE&q=원피스&area=홍대')
    assert r.status_code==200
    result=r.json();assert result['total']==1
    item=result['items'][0];assert len(item['sources'])==2 and len(item['images'])==1
    assert 'data/private' not in r.text and 'access_token' not in r.text
    image=client.get(item['images'][0])
    assert image.status_code==200 and image.headers['cache-control']=='no-store'
    assert image.content.startswith(b'\xff\xd8\xff')
    assert client.get('/api/events/images/2/-1').status_code==404
    assert client.get('/api/events?category=EXHIBITION').json()['total']==0
    assert client.get('/api/events?size=999').status_code==422


def test_non_event_posts_and_images_are_not_served(event_client):
    client,e=event_client
    with e.begin() as c:
        c.execute(update(candidates).values(status='REJECTED_NOT_EVENT'))
    r=client.get('/api/events')
    assert r.json()['total']==0
    assert client.get('/api/events/images/2/0').status_code==404


@pytest.mark.parametrize('start,end,expected',[('2026-11-01','2026-11-12','ONGOING'),
    ('2026-11-13','2026-12-01','UPCOMING'),('2026-10-01','2026-11-11','ENDED'),
    (None,'2026-12-01','UNKNOWN'),('2026-11-01',None,'UNKNOWN')])
def test_period_boundaries_are_calendar_dates(start,end,expected):
    assert period(start,end,date(2026,11,12))==expected

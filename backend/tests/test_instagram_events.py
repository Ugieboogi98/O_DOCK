from datetime import datetime, timezone
import json
import httpx
import pytest
from sqlalchemy import create_engine, select, func, insert
from app.integrations.instagram.events import extract
from app.integrations.instagram.collector import collect_account, minimal_post
from app.integrations.instagram.client import MetaClient, ProbeError
from app.integrations.instagram.config import InstagramSettings
from app.integrations.instagram.review import render
from app.integrations.instagram.store import metadata, posts, candidates, sources, events, links, save_posts

WORKS=[{'ko':'예시 만화','aliases':['예시 만화','Example Manga']}, {'ko':'원피스','aliases':['원피스']}]


@pytest.mark.parametrize('word,category',[('팝업','POPUP_STORE'),('팝업스토어','POPUP_STORE'),
    ('팝업 스토어','POPUP_STORE'),('전시회','EXHIBITION'),('원화전','EXHIBITION'),
    ('콜라보 카페','COLLAB_CAFE'),('コラボカフェ','COLLAB_CAFE'),('collaboration cafe','COLLAB_CAFE')])
def test_requested_categories_require_ip_and_review(word,category):
    result=extract(f'예시 만화 {word}\n기간: 2026.11.12 ~ 2026.11.20\n장소: 예시 전시장',WORKS)
    assert result['status']=='PENDING_REVIEW' and category in result['categories']
    assert result['start_date']=='2026-11-12' and result['end_date']=='2026-11-20'
    assert result['venue']=='예시 전시장'
    assert result['duplicate_key']
    assert all(e['quote'] in f'예시 만화 {word}\n기간: 2026.11.12 ~ 2026.11.20\n장소: 예시 전시장' for e in result['evidence'])


def test_general_food_fashion_and_non_event_are_excluded():
    assert extract('패션 브랜드 팝업스토어 대규모 할인',WORKS)['status']=='REJECTED_NOT_SUBCULTURE'
    assert extract('커피 브랜드 콜라보 카페 쿠폰',WORKS)['status']=='REJECTED_NOT_SUBCULTURE'
    assert extract('예시 만화 신간 소개',WORKS)['status']=='REJECTED_NOT_EVENT'


def test_dates_never_guess_year_or_choose_reservation_date():
    a=extract('예시 만화 콜라보 카페\n기간: 11/12~11/20',WORKS)
    assert a['start_date'] is None and a['end_date'] is None
    a=extract('예시 만화 전시회\n예약: 2026.11.12\n기간: 미정',WORKS)
    assert a['start_date'] is None and a['explicit_date_mentions']==['2026-11-12']
    assert extract('예시 만화 팝업\n기간: 2026.13.40',WORKS)['start_date'] is None


def test_unlabelled_explicit_period_and_end_year_provenance():
    a=extract('예시 만화 전시회\n2026. 11. 14 (토) ~ 2027. 4. 4(일)\nDUEX(덕스)부산',WORKS)
    assert (a['start_date'],a['end_date'],a['venue'])==('2026-11-14','2027-04-04','DUEX(덕스)부산')
    a=extract('예시 만화 팝업\n2026. 11. 23(월) ~ 12. 6(일)\nAK 플라자 홍대 3층',WORKS)
    assert a['end_date']=='2026-12-06'
    assert any(e['field']=='end_year_inherited_from_explicit_start' for e in a['evidence'])
    a=extract('예시 만화 팝업\n2026.12.20 ~ 1.5',WORKS)
    assert a['start_date'] is None and a['end_date'] is None


def test_multiple_venues_and_periods_are_not_combined_into_one_event():
    a=extract('예시 만화 팝업\n2026.11.1~2026.11.3\n2026.12.1~2026.12.5\n📍서울\n📍부산',WORKS)
    assert a['start_date'] is None and a['venue'] is None and a['duplicate_key'] is None


def test_yearless_range_uses_source_publication_and_checks_weekdays():
    caption='예시 만화 팝업\n🗓️ 11/19(목)~ 12/2(수)\n📍 AK PLAZA 홍대 2F'
    a=extract(caption,WORKS,published_at='2026-11-09T09:53:05+00:00')
    assert (a['start_date'],a['end_date'])==('2026-11-19','2026-12-02')
    assert a['year_inferred'] and a['period_text']=='11/19(목)~ 12/2(수)'
    assert any(e['field']=='period_year_from_publication' for e in a['evidence'])
    b=extract(caption,WORKS,published_at='2025-11-09T09:53:05+00:00')
    assert b['start_date'] is None and b['period_text']
    assert extract(caption,WORKS)['start_date'] is None


def test_partial_date_formats_and_new_year_are_supported_without_today():
    for text in ('11월 19일~12월 2일','11.19 ~ 12.2',r'11/19(목)\~12/2(수)'):
        a=extract('예시 만화 팝업\n'+text,WORKS,published_at='2026-11-09T00:00:00+00:00')
        assert a['start_date']=='2026-11-19' and a['end_date']=='2026-12-02'
    a=extract('예시 만화 팝업\n12/28~1/5',WORKS,published_at='2026-12-20T00:00:00+00:00')
    assert a['start_date']=='2026-12-28' and a['end_date']=='2027-01-05'
    assert extract('예시 만화 팝업 2/30~3/1',WORKS,published_at='2026-02-01T00:00:00+00:00')['start_date'] is None


def test_booking_range_is_not_used_as_event_period_and_raw_multiple_dates_survive():
    a=extract('예시 만화 전시\n예매 기간: 11/1~11/5',WORKS,published_at='2026-10-29T00:00:00+00:00')
    assert a['start_date'] is None
    a=extract('Example Manga pop-up\n📅 Nov 20 – Dec 13, 2026\n📅 Dec 14 – Dec 31, 2026',WORKS)
    assert a['start_date'] is None and 'Nov 20' in a['period_text'] and 'Dec 31' in a['period_text']


def test_exhibition_name_wins_over_incidental_popup_mention():
    from app.integrations.instagram.event_identity import finalize
    works=[{'ko':'진격의 거인','aliases':['진격의 거인']}]
    for name in ('진격의 거인展 FINAL','진격의 거인 전','진격의 거인전 FINAL'):
        a=extract(name+'\n팝업스토어 메뉴 안내\n2026.11.14~2027.4.4\n장소: 부산',works)
        assert a['categories']==['EXHIBITION'] and a['status']=='PENDING_REVIEW'
    assert extract('예시 만화 팝업스토어\n전시장 내 팝업',WORKS)['categories']==['POPUP_STORE']


def test_same_event_identity_across_accounts_and_venue_spelling():
    from app.integrations.instagram.event_identity import key
    a=extract('예시 만화 팝업\n2026.11.19~2026.12.2\n장소: AK PLAZA 홍대점 2층',WORKS)
    b=extract('예시 만화 팝업 굿즈 공지\n2026.11.19~2026.12.2\n📍 AK 플라자 홍대 2F',WORKS)
    assert key(a)==key(b) and key(a)
    b['venue']='AK PLAZA 홍대 3층';b['venues']=[b['venue']]
    assert key(a)!=key(b)


def test_multiple_overseas_schedule_posts_group_without_merging_venues():
    from app.integrations.instagram.event_identity import key
    text='Example Manga pop-up\n📍 Kinokuniya San Francisco\n📅 Nov 20 (Fri) – Dec 13 (Sun), 2026\n📍 Kinokuniya Bookstore San Francisco\n📅 Dec 14 (Mon) – Dec 31 (Thu), 2026'
    a=extract(text,WORKS);b=extract(text+'\nNew goods announcement!',WORKS)
    assert len(a['periods'])==2 and key(a)==key(b) and key(a)
    assert a['start_date'] is None and a['venue'] is None


def test_exclude_only_when_already_ended_at_first_collection():
    from app.integrations.instagram.event_identity import finalize
    from app.services.event_catalog import schedule_period
    a=extract('예시 만화 팝업\n2026.10.24~2026.11.8\n장소: 홍대',WORKS)
    assert finalize(a,'2026-11-12T00:00:00+00:00')['status']=='EXCLUDED_ENDED_BEFORE_COLLECTION'
    kept=finalize(a,'2026-11-01T00:00:00+00:00')
    assert kept['status']=='PENDING_REVIEW'
    from datetime import date
    assert schedule_period(kept,date(2026,11,5))=='ONGOING'
    assert schedule_period(kept,date(2026,11,12))=='ENDED'
    same_day=extract('예시 만화 팝업\n2026.11.1~2026.11.12',WORKS)
    assert finalize(same_day,'2026-11-12T00:00:00+00:00')['status']=='PENDING_REVIEW'
    old=extract('예시 만화 팝업\n📍 홍대\n🗓 10.19 MON — 11.01 SUN',WORKS,published_at='2026-10-19T00:00:00+00:00')
    assert old['end_date']=='2026-11-01' and finalize(old,'2026-11-12T00:00:00+00:00')['status']=='EXCLUDED_ENDED_BEFORE_COLLECTION'


def test_store_skips_old_events_but_preserves_previously_collected_events_after_end(monkeypatch):
    from app.integrations.instagram import store
    class Clock(datetime):
        current=datetime(2026,11,12,tzinfo=timezone.utc)
        @classmethod
        def now(cls,tz=None):return cls.current
    monkeypatch.setattr(store,'datetime',Clock)
    engine=create_engine('sqlite://');metadata.create_all(engine)
    active=row('예시 만화 팝업\n2026.11.1~2026.11.20',ident='111')
    past=row('예시 만화 팝업\n2026.10.24~2026.11.8',ident='222')
    extractor=lambda text:extract(text,WORKS)
    with engine.begin() as c:
        counts=save_posts(c,'duex.official',[active,past],extractor)
        assert counts['inserted']==1 and counts['excluded_ended']==1
        assert c.scalar(select(func.count()).select_from(posts))==1
    Clock.current=datetime(2026,11,21,tzinfo=timezone.utc)
    with engine.begin() as c:
        counts=save_posts(c,'duex.official',[active],extractor)
        assert counts['excluded_ended']==0 and counts['unchanged']==1
        saved=c.execute(select(candidates)).mappings().one()
        assert saved['status']=='PENDING_REVIEW' and saved['data']['collection_cutoff_date']=='2026-11-12'
    engine.dispose()


def row(caption='예시 만화 콜라보 카페', ident='123'):
    return {'id':ident,'caption':caption,'permalink':'https://www.instagram.com/p/Example/',
        'timestamp':'2026-11-12T10:00:00+09:00','media_type':'IMAGE'}


def test_minimal_post_omits_unapproved_media_and_paging():
    original={**row(),'caption':None,'media_url':'https://example.com/image','access_token':'SECRET'}
    saved=minimal_post(original)
    assert saved['caption']=='' and set(saved)=={'id','caption','permalink','timestamp','media_type'}


@pytest.mark.parametrize('url',['http://www.instagram.com/p/Example/','https://evil.example/p/X/',
    'https://www.instagram.com.evil.example/p/X/','javascript:alert(1)'])
def test_untrusted_permalink_rejected(url):
    with pytest.raises(ProbeError):minimal_post({**row(),'permalink':url})


def test_cursor_is_reconstructed_without_following_next_or_duplicate_posts():
    s=InstagramSettings(_env_file=None,meta_ig_user_id='222',meta_access_token='TOKEN',
        meta_graph_api_version='v25.0',instagram_collection_page_limit=2)
    calls=[]
    def handle(request):
        calls.append(request)
        return httpx.Response(200,json={'business_discovery':{'username':'duex.official','media':{
            'data':[row()], 'paging':{'next':'https://evil.example?access_token=SECRET','cursors':{'after':'ABC123'}}}}})
    c=MetaClient(s,transport=httpx.MockTransport(handle))
    result=collect_account(c,'duex.official',s)
    c.close()
    assert len(result)==1 and len(calls)==2
    assert '.after(ABC123)' in calls[1].url.params['fields']
    assert all(r.url.host=='graph.facebook.com' for r in calls)


def test_upsert_rollback_and_changed_source_resets_review():
    engine=create_engine('sqlite://')
    metadata.create_all(engine)
    extractor=lambda caption:extract(caption,WORKS)
    with engine.begin() as c:
        assert save_posts(c,'duex.official',[row()],extractor)['inserted']==1
    with engine.begin() as c:
        assert save_posts(c,'duex.official',[row()],extractor)['unchanged']==1
        assert c.scalar(select(func.count()).select_from(posts))==1
        assert c.scalar(select(func.count()).select_from(candidates))==1
        assert c.scalar(select(func.count()).select_from(events))==0
        pid=c.scalar(select(posts.c.id))
        eid=c.execute(insert(events).values(status='APPROVED',title='old',revision_history=[])).inserted_primary_key[0]
        c.execute(insert(links).values(event_id=eid,post_id=pid))
    with pytest.raises(RuntimeError):
        with engine.begin() as c:
            save_posts(c,'anique.jp',[row(ident='456')],extractor)
            raise RuntimeError('DB interrupted')
    with engine.begin() as c:
        assert c.scalar(select(func.count()).select_from(posts))==1
        assert save_posts(c,'anique.jp',[row(ident='456')],extractor)['inserted']==1
        assert save_posts(c,'duex.official',[row('예시 만화 팝업 변경 안내')],extractor)['updated']==1
        event=c.execute(select(events)).mappings().one()
        assert event['status']=='PENDING_REVIEW' and event['revision_history'][0]['title']=='old'
    engine.dispose()


def test_private_review_html_escapes_caption_and_contains_no_external_images():
    r=row('<script>alert(1)</script> 예시 만화 콜라보 카페')
    r.update(source_username='duex.official',candidate=extract(r['caption'],WORKS))
    html=render({'posts':[r],'collected_at':'2026-11-12'})
    assert '<script>' not in html and '&lt;script&gt;' in html
    assert '<img' not in html and '콜라보 카페' in html
    assert '관리자 검수 전 공개되지 않습니다' in html

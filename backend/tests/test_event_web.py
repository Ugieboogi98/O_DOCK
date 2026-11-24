"""Protocol limits, actual source structures, cross-source identity and lifecycle."""
from datetime import datetime, timezone, date
import gzip
import httpx
import pytest
from sqlalchemy import create_engine, select, func
from app.integrations.event_web.client import PublicClient, FetchError
from app.integrations.event_web import adapters as a
from app.integrations.instagram.events import extract
from app.integrations.instagram.event_identity import finalize, key
from app.integrations.instagram.store import metadata, posts, candidates, save_posts
from app.services.event_catalog import schedule_period

WORKS=[{'ko':'진격의 거인','aliases':['진격의 거인']},{'ko':'주술회전','aliases':['주술회전']},
       {'ko':'죠죠의 기묘한 모험','aliases':['죠죠의 기묘한 모험']}]

@pytest.mark.parametrize('title',['안기고 싶은 남자 1위에게 협박당하고 있습니다.','동방 Project','세포신곡 CELL OF MIRAGE','NU: 카니발'])
def test_official_fair_ips_are_not_dropped_for_missing_anime_aliases(title):
    d=extract(title+' 페어\n행사 기간: 2026.11.12~2026.11.15')
    assert d['is_subculture_relevant'] and 'FAIR' in d['categories']

def test_client_decompresses_once_and_caches_without_network(tmp_path):
    calls=[]
    def respond(r):
        calls.append(str(r.url))
        if r.url.path=='/robots.txt':return httpx.Response(200,text='User-agent: *\nAllow: /')
        return httpx.Response(200,content=gzip.compress('행사 일정'.encode()),headers={'Content-Type':'text/html; charset=utf-8','Content-Encoding':'gzip'})
    c=PublicClient(tmp_path,transport=httpx.MockTransport(respond),delay=0)
    try:
        assert c.get('https://www.duex.co.kr/page/22')=='행사 일정'
        assert c.get('https://www.duex.co.kr/page/22')=='행사 일정'
        assert len(calls)==2
        with pytest.raises(FetchError,match='URL_NOT_ALLOWLISTED'):c.get('https://127.0.0.1/private')
    finally:c.close()

def test_client_honors_robots_and_does_not_follow_offsite_redirects(tmp_path):
    calls=[]
    def respond(r):
        calls.append(r.url.path)
        if r.url.path=='/robots.txt':return httpx.Response(200,text='User-agent: *\nDisallow: /private')
        return httpx.Response(302,headers={'Location':'http://169.254.169.254/latest/meta-data/'})
    c=PublicClient(tmp_path,transport=httpx.MockTransport(respond),delay=0)
    try:
        with pytest.raises(FetchError,match='ROBOTS_DISALLOWED'):c.get('https://www.duex.co.kr/private')
        with pytest.raises(FetchError,match='URL_NOT_ALLOWLISTED'):c.get('https://www.duex.co.kr/page/22')
        assert calls==['/robots.txt','/page/22']
    finally:c.close()

def test_conditional_cache_304_and_retry_are_bounded(tmp_path):
    calls=[]
    def respond(r):
        calls.append(r)
        if r.url.path=='/robots.txt':return httpx.Response(404)
        if r.headers.get('if-none-match'):return httpx.Response(304)
        return httpx.Response(200,text='{}',headers={'Content-Type':'application/json','ETag':'abc'})
    c=PublicClient(tmp_path,transport=httpx.MockTransport(respond),delay=0)
    try:
        url='https://api.aniplustv.com:3060/api/v2/offline-collabo'
        assert c.get(url)=='{}' and c.get(url,ttl=0)=='{}'
        assert calls[-1].headers['if-none-match']=='abc'
    finally:c.close()
    calls=[]
    def limited(r):
        calls.append(r)
        return httpx.Response(404) if r.url.path=='/robots.txt' else httpx.Response(429)
    c=PublicClient(tmp_path/'limited',transport=httpx.MockTransport(limited),delay=0,sleep=lambda _:None)
    try:
        with pytest.raises(FetchError,match='HTTP_429'):c.get('https://www.duex.co.kr/page/22')
        assert len(calls)==4
    finally:c.close()

def test_duex_uses_main_exhibition_dates_and_merges_with_instagram():
    html='''<div class="now"><ul><li class="now--list"><div class="now--title">전시명</div><p class="now--desc">진격의 거인展 FINAL 부산</p></li>
    <li class="now--list"><div class="now--title">전시기간</div><p class="now--desc">2026. 11. 14 (토) ~ 2027. 4. 4 (일)</p></li>
    <li class="now--list"><div class="now--title">전시장소</div><p class="now--desc">덕스(DUEX) 부산 (더샵센트럴스타 B1층)</p></li>
    <li class="now--list"><div class="now--title">관람시간</div><p class="now--desc">2026.11.16~2027.4.4</p></li></ul></div>'''
    item=a.duex(html,'https://www.duex.co.kr/page/22_3')[0];d=a.candidate(item,WORKS)
    ig=extract('진격의 거인展 FINAL\n2026.11.14~2027.4.4\n장소: DUEX(덕스) 부산',WORKS)
    assert d['start_date']=='2026-11-14' and key(d)==key(ig)
    assert a.duex('<p>전시 준비중입니다.</p>','https://www.duex.co.kr/page/21')==[]

def test_space_preserves_main_period_and_official_booking():
    html='''<div><h3>타네무라 아리나 30주년 기념전</h3><p><time>2026.10.03</time> - <time>2026.12.06</time></p>
    <a href="https://ticket.melon.com/performance/index.htm?prodId=213917">국내 Ticket</a></div>
    <dl><dt>전시장소</dt><dd>Space Galleria 서울 홍대</dd><dt>전시소개</dt><dd>작가님의 원화전</dd></dl>'''
    d=a.candidate(a.space(html,'https://spacegalleria.co.kr/exhibition/38')[0],WORKS)
    assert d['status']=='PENDING_REVIEW' and d['end_date']=='2026-12-06'
    assert d['booking_url'].endswith('213917') and d['content_license_status']=='FACTS_AND_LINK_ONLY'

def test_animate_uses_item_dates_and_explicit_offline_locations():
    html='''<div class="event_list"><li><div class="board_tit"><a href="javascript:gd_btn_view('event',520 , 'y')"><strong>죠죠의 기묘한 모험 페어 3탄</strong></a></div>
    <div class="board_event_day">이벤트기간 2026.12.12 00:00 ~ 2026.12.25 23:59</div></li></div>'''
    item=a.animate_list(html,'https://www.animate-onlineshop.co.kr/board/list.php?bdId=event')[0]
    item=a.animate_detail('<div class="board_view_content">○개최장소<br>홍대점/부산점/온라인샵<br>○이벤트 내용</div>',item)
    d=a.candidate(item,WORKS)
    assert d['categories']==['FAIR'] and d['start_date']=='2026-12-12' and d['end_date']=='2026-12-25'
    assert d['venue']=='애니메이트 홍대점/부산점/온라인샵'
    item=a.animate_detail('<div class="board_view_content">○개최장소<br>온라인샵</div>',item)
    assert a.candidate(item,WORKS)['status']=='EXCLUDED_ONLINE_ONLY'

def test_pop_reservation_dates_and_reviews_are_not_event_dates():
    html='''<h1><a href="/"><img alt="logo"></a></h1><meta property="og:title" content="TCG POP-UP STORE"><div class="reserve__infor__list"><div class="editor_content">
    ■ 팝업 운영 기간<br>2026년 11월 12일(목) ~ 12월 12일(토)<br>■ 팝업 입장 예약 기간<br>2026년 11월 12일(목) ~ 11월 18일(수)<br>
    ■ 운영 장소<br>팝콘D스퀘어 성수 5층<br>서울특별시 성동구 연무장길 37-29</div></div><div>Q&amp;A<br>2026.11.1~2026.11.2</div>'''
    item=a.pop(html,'https://www.popcondplay.com/reserve/view/113')[0];d=a.candidate(item,WORKS)
    assert d['status']=='PENDING_REVIEW' and d['end_date']=='2026-12-12' and d['venue']=='팝콘D스퀘어 성수 5층'
    assert 'Q&A' not in str(item) and '2026.11.2' not in str(item)

def test_aniplus_excludes_old_cafes_and_never_infers_locations():
    rows=a.aniplus({'list':[{'id':116,'name':'산나비','startDate':'2026-11-05','endDate':'2026-12-20'},
        {'id':114,'name':'hololive FLOW GLOW','startDate':'2026-09-17','endDate':'2026-11-01'}]})
    results=[finalize(a.candidate(r,WORKS),'2026-11-12T01:00:00+00:00') for r in rows]
    assert results[0]['status']=='PENDING_REVIEW' and results[0]['venue'] is None
    assert results[1]['status']=='EXCLUDED_ENDED_BEFORE_COLLECTION'

def test_agf_uses_event_days_instead_of_past_attendance_year():
    html='''<p>2025년 100,518명 관람</p><ul><li>행사명<p>Anime X Game Festival 2026</p></li><li>일시<p>2026년 12월 4일(금) 09:30 ~ 18:00</p><p>2026년 12월 5일(토) 09:30 ~ 18:00</p><p>2026년 12월 6일(일) 09:30 ~ 18:00</p></li><li>장소<p>KINTEX 제1전시장 1/2/3/4/5홀</p></li></ul>'''
    d=a.candidate(a.agf(html,'https://www.agfkorea.com/event?idx=1')[0],WORKS)
    assert d['categories']==['FESTIVAL'] and d['start_date']=='2026-12-04' and d['end_date']=='2026-12-06'
    assert schedule_period(d,date(2026,12,7))=='ENDED'

def test_website_upsert_is_platform_scoped_and_keeps_change_history():
    engine=create_engine('sqlite://');metadata.create_all(engine)
    stamp=datetime.now(timezone.utc).isoformat()
    raw={'id':'123','caption':'','permalink':'https://www.duex.co.kr/page/22','timestamp':stamp,'media_type':'FACTS'}
    original={'status':'PENDING_REVIEW','is_subculture_relevant':True,'categories':['EXHIBITION'],'title':'주술회전 전시회',
        'franchises':['주술회전'],'venue':'홍대','start_date':'2026-12-04','end_date':'2027-02-28'}
    with engine.begin() as c:
        save_posts(c,'duex.official',[raw],lambda _:original)
        save_posts(c,'DUEX',[raw],lambda _:original,platform='website',source_url='https://www.duex.co.kr/')
        counts=save_posts(c,'DUEX',[raw],lambda _:original,platform='website')
        assert counts['unchanged']==1 and c.scalar(select(func.count()).select_from(posts))==2
        changed=dict(original,end_date='2027-03-01',event_status='CANCELLED')
        save_posts(c,'DUEX',[raw],lambda _:changed,platform='website')
        data=c.execute(select(candidates.c.data).join(posts).where(posts.c.platform=='website')).scalar_one()
        assert len(data['change_history'])==1 and data['change_history'][0]['before']['end_date']=='2027-02-28'
        assert schedule_period(data)=='CANCELLED'
    engine.dispose()

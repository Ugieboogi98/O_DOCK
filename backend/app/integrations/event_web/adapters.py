"""Site-specific facts, never whole-page/nav/footer/visitor-comment extraction."""
from datetime import date, datetime
import json
import re
from urllib.parse import urljoin, urlsplit, urlunsplit
from bs4 import BeautifulSoup
from app.integrations.instagram.events import extract
from app.integrations.event_web.images import poster_images, image_url

def soup(html):return BeautifulSoup(html,'html.parser')
def text(node):return node.get_text(' ',strip=True) if node else ''
def lines(node):return node.get_text('\n',strip=True) if node else ''
def field_rows(root,selector,label,value):
    return {text(row.select_one(label)):text(row.select_one(value)) for row in root.select(selector)}

def canonical(url):
    p=urlsplit(url)
    return urlunsplit((p.scheme,p.netloc,p.path,p.query if '/board/view.php' in p.path or '/collabo-cafe' in p.path or p.path=='/event' else '', ''))

def booking(root,url):
    for a in root.select('a[href]'):
        if re.search(r'ticket|티켓|예매|예약',text(a),re.I):
            link=urljoin(url,a['href'])
            if urlsplit(link).scheme=='https':return link
    return None

def record(url,title,*,period=None,venue=None,published=None,category=None,context='',identity=None,booking_url=None,address=None,image_urls=None):
    return {'url':canonical(url),'title':title,'period_text':period,'venue':venue,'published_at':published,
            'category':category,'context':context,'identity_title':identity,'booking_url':booking_url,'address':address,
            'image_urls':image_urls or []}

def duex(html,url):
    root=soup(html);fields=field_rows(root,'.now--list','.now--title','.now--desc')
    if not fields.get('전시명'):return []
    return [record(url,fields['전시명'],period=fields.get('전시기간'),venue=fields.get('전시장소'),
                   category='EXHIBITION',context=fields.get('전시소개','')[:400],booking_url=booking(root.select_one('.now') or root,url),
                   image_urls=poster_images(root,url,'img[src*="/data/file/"], img[src*="/data/editor/"]'))]

def space(html,url):
    root=soup(html)
    # Scope to the exhibition itself; source navigation also contains old event titles.
    title=root.select_one('h3')
    if not title:return []
    body=title.parent
    while body.parent and not re.search(r'20\d{2}\.\d',text(body)):body=body.parent
    bodytext=text(body)
    m=re.search(r'20\d{2}\.\d{1,2}\.\d{1,2}\s*[-~–]\s*20\d{2}\.\d{1,2}\.\d{1,2}',bodytext)
    full=lines(root)
    venue=re.search(r'전시장소\s*\n([^\n]+)',full)
    description=re.search(r'전시소개\s*\n([^\n]+)',full)
    return [record(url,text(title),period=m.group() if m else None,venue=venue.group(1) if venue else None,
        category='EXHIBITION',context=description.group(1) if description else '',identity=text(title),booking_url=booking(body,url),
        image_urls=poster_images(root,url,'.exhibition-post-hero-image'))]

def animate_list(html,url):
    out=[]
    for li in soup(html).select('.event_list li'):
        title=text(li.select_one('.board_tit strong'));a=li.select_one('.board_tit a[href]')
        m=re.search(r"gd_btn_view\('event',\s*(\d+)",a['href']) if a else None
        if title and m:
            out.append(record(urljoin(url,'view.php?bdId=event&sno='+m.group(1)),title,period=text(li.select_one('.board_event_day')),category='FAIR',
                              image_urls=poster_images(li,url,'img')))
    return out

def animate_detail(html,item):
    root=soup(html)
    body=root.select_one('.board_view_content') or root.select_one('.board_view')
    content=lines(body)
    # Only labeled factual fields, excluding caution paragraphs and visitor comments.
    venue=re.search(r'(?:○\s*)?개최장소\s*\n([^\n]+)',content)
    published=re.search(r'20\d{2}\.\d{2}\.\d{2}\s+\d{2}:\d{2}:\d{2}',text(root.select_one('.view_info_day')))
    result=dict(item)
    result['image_urls']=poster_images(body,item['url'],'img') or item.get('image_urls',[])
    if venue:result['venue']='애니메이트 '+venue.group(1)
    if published:result['published_at']=datetime.strptime(published.group(),'%Y.%m.%d %H:%M:%S').isoformat()+'+09:00'
    # A page explicitly limited to online distribution isn't an offline visit.
    if venue and not re.search(r'홍대|잠실|부산|수원|매장|점/',venue.group(1)):result['online_only']=True
    return result

def pop(html,url):
    root=soup(html)
    # The title and event fields are in the reservation information, above Q&A.
    title=next((node for node in root.select('h1') if text(node)),None)
    if not title:
        meta=root.select_one('meta[property="og:title"]')
        name=meta.get('content','') if meta else ''
    else:name=text(title)
    fields={}
    for dl in root.select('dl'):
        for dt in dl.select('dt'):
            dd=dt.find_next_sibling('dd')
            if dd:fields[text(dt)]=text(dd)
    if not name or re.search(r'매장픽업|예약판매',name):return []
    category='EXHIBITION' if re.search(r'展|특별전|전시',name) else 'POPUP_STORE' if re.search(r'팝업|POP.UP',name,re.I) else None
    if not category:return []
    period=fields.get('기간');venue=fields.get('장소');address=None
    if not period:
        content=lines(root.select_one('.reserve__infor__list .editor_content'))
        m=re.search(r'팝업 운영 기간\s*\n([^\n]+)',content)
        if m:period=m.group(1)
        m=re.search(r'운영 장소\s*\n([^\n]+)(?:\n(서울[^\n]+))?',content)
        if m:venue=m.group(1);address=m.group(2)
    description=root.select_one('meta[property="og:description"]')
    context=description.get('content','') if description else ''
    if 'TCG' in name:context+=' 트레이딩 카드 게임 TCG'
    return [record(url,name,period=period,venue=venue,category=category,context=context,address=address,booking_url=url,
                   image_urls=poster_images(root,url,'meta[property="og:image"]'))]

def daewon(html,url):
    root=soup(html)
    title=root.select_one('.board_view_tit, .view_title, .board-title, .title')
    body=root.select_one('.detail-box .c-text, .board_view_content, .view_content, .board-content, .content_view')
    if not title or not body:return []
    # News often omits the closing date. Keep it excluded until an explicit schedule exists.
    name=text(title);value=lines(body)
    period=re.search(r'20\d{2}[./년-].{0,35}[~～–].{0,40}',value)
    return [record(url,name,period=period.group() if period else None,context=value[:350],
                   image_urls=poster_images(body,url,'img'))]

def agf(html,url):
    root=soup(html);full=lines(root)
    match=re.search(r'행사명\s*\n([^\n]+)\s*\n일시\s*\n(.*?)\n장소\s*\n([^\n]+)',full,re.S)
    if not match:return []
    title,dates,venue=match.groups()
    days=re.findall(r'(20\d{2})년\s*(\d+)월\s*(\d+)일',dates)
    if not days:return []
    values=[date(*map(int,d)).isoformat() for d in days]
    return [record(url,title,period=min(values)+' ~ '+max(values),venue=venue,category='FESTIVAL',
                   identity=title,context='애니메이션 게임 웹툰 라이트노벨 공식 팬 페스티벌',booking_url=urljoin(url,'/ticket'),
                   image_urls=poster_images(root,url,'img[src*="AGF_POSTER"]'))]

def aniplus(payload):
    if not isinstance(payload,dict) or not isinstance(payload.get('list'),list):raise ValueError('ANIPLUS_SCHEMA_CHANGED')
    out=[]
    for row in payload['list']:
        if not all(k in row for k in ('id','name','startDate','endDate')):raise ValueError('ANIPLUS_SCHEMA_CHANGED')
        ident=int(row['id'])
        out.append(record(f'https://shop.aniplustv.com/offline-shop/collabo-cafe?collaboId={ident}',
            row['name']+' 콜라보 카페' if '카페' not in row['name'] else row['name'],
            period=row['startDate']+' ~ '+row['endDate'],category='COLLAB_CAFE',context='공식 IP 콜라보 카페',identity=row['name'],
            image_urls=[url for url in [image_url(row.get('thumbnail'),'https://bc8azosk4j.ecn.cdn.ofs.kr/TShop/collabo/')] if url]))
    return out

def candidate(item,works):
    facts=[item['title']]
    if item.get('period_text'):
        dates=re.sub(r'\s+\d{1,2}:\d{2}(?::\d{2})?','',item['period_text'])
        facts.append('행사 기간: '+dates)
    if item.get('venue'):facts.append('장소: '+item['venue'])
    facts.append(item.get('context',''))
    data=extract('\n'.join(facts),works=works,published_at=item.get('published_at'))
    if item.get('category'):data['categories']=[item['category']]
    # Curated IP-only organizers can verify scope even for titles missing from the product dictionary.
    scoped=item.get('identity_title') and item.get('category') in ('EXHIBITION','COLLAB_CAFE','FESTIVAL')
    if scoped and not data['is_subculture_relevant']:
        data['is_subculture_relevant']=True
        data['evidence'].append({'field':'ip_context','quote':item.get('context') or item['title'],'basis':'official IP-specific source'})
    data['status']='PENDING_REVIEW' if data['categories'] and data['is_subculture_relevant'] else 'REJECTED_NOT_SUBCULTURE'
    if item.get('online_only'):data['status']='EXCLUDED_ONLINE_ONLY'
    if data['status']=='PENDING_REVIEW' and not data['start_date'] and not data.get('periods'):
        data['status']='EXCLUDED_UNCONFIRMED_WEB_SCHEDULE'
    data.update(identity_title=item.get('identity_title'),booking_url=item.get('booking_url'),address=item.get('address'),
                content_license_status='FACTS_AND_LINK_ONLY',source_platform='website',published_at=item.get('published_at'),
                image_urls=item.get('image_urls',[]))
    return data

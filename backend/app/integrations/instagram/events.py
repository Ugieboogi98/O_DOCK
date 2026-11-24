"""Conservative source-bound event candidate extraction; no AI or paid APIs."""
from datetime import date, datetime
from zoneinfo import ZoneInfo
import hashlib
import json
from pathlib import Path
import re
import unicodedata

CATEGORIES = {
    'COLLAB_CAFE': r'콜라보\s*카페|컬래버(?:레이션)?\s*카페|콜라보레이션\s*카페|코라보\s*카페|コラボ\s*カフェ|collab(?:oration)?\s*caf[eé]',
    'POPUP_STORE': r'팝업\s*스토어|팝업\s*숍|팝업|ポップアップ(?:ストア|ショップ)?|pop[\s-]*up(?:\s*store)?',
    'EXHIBITION': r'전시회|전시|특별전|원화전|展覧会|展示会|原画展|exhibition',
    'FAIR': r'페어|온리전|\bfair\b',
    'FESTIVAL': r'페스티벌|\bfestival\b',
    'GOODS_EVENT': r'사인회|굿즈\s*이벤트|팬\s*미팅',
}
IP_CONTEXT = r'애니메이션|アニメ|만화|漫画|웹툰|라이트노벨|ライトノベル|버추얼|VTuber|비디오\s*게임|트레이딩\s*카드\s*게임|캐릭터\s*(?:굿즈|상품)|キャラクターグッズ'


def normalize(text):
    return re.sub(r'\s+', '', unicodedata.normalize('NFKC', text or '')).casefold()


def default_works():
    root = Path(__file__).resolve().parents[2] / 'services'
    rows = []
    for name in ('classification_knowledge.json', 'classification_wikipedia_anime.json'):
        path = root / name
        if path.exists():
            rows.extend(json.loads(path.read_text(encoding='utf-8'))['works'])
    # Explicit aliases useful in event announcements; no inferred work relationships.
    rows += [{'ko': ko, 'aliases': aliases} for ko, aliases in [
        ('포켓몬스터', ['포켓몬', 'ポケモン', 'Pokémon']),
        ('원신', ['원신', '原神', 'Genshin Impact']),
        ('블루 아카이브', ['블루 아카이브', 'ブルーアーカイブ']),
        ('명일방주', ['명일방주', 'アークナイツ']),
        ('앙상블 스타즈', ['앙상블 스타즈', 'あんさんぶるスターズ']),
        ('산리오', ['산리오', 'サンリオ', 'Sanrio'])]]
    rows += [{'ko':ko,'aliases':aliases} for ko,aliases in [
        ('산나비',['산나비','SANABI']),
        ('프로젝트 세카이',['프로젝트 세카이','プロジェクトセカイ','Project SEKAI']),
        ('에일리언 스테이지',['ALIEN STAGE','에일리언 스테이지']),
        ('스튜디오 지브리',['스튜디오 지브리','スタジオジブリ','Studio Ghibli']),
        ('승리의 여신: 니케',['승리의 여신: 니케','NIKKE']),
        ('향기로운 꽃은 늠름하게 핀다',['향기로운 꽃은 늠름하게 핀다']),
        ('안기고 싶은 남자 1위에게 협박당하고 있습니다.',['안기고 싶은 남자 1위에게 협박당하고 있습니다']),
        ('동방 프로젝트',['동방 Project','동방 프로젝트','東方Project','Touhou Project']),
        ('세포신곡',['세포신곡','CELL OF MIRAGE']),
        ('NU: 카니발',['NU: 카니발','NU:카니발','NU: Carnival']),
    ]]
    rows.append({'ko':'야마다 군과 Lv999의 사랑을 하다',
                 'aliases':['야마다 군과 Lv999의 사랑을 하다','야마다군과lv999의 사랑을 한다','山田くんとLv999の恋をする']})
    return rows


def extract(caption, works=None, published_at=None):
    text = caption or ''
    evidence = []
    categories = []
    for category, pattern in CATEGORIES.items():
        hit = re.search(pattern, text, re.I)
        if hit:
            categories.append(category)
            evidence.append({'field': 'category', 'value': category, 'quote': hit.group()})
    hits = {}
    for work in default_works() if works is None else works:
        for alias in sorted(work['aliases'], key=len, reverse=True):
            if len(normalize(alias)) < 3 and alias not in ('원신', '은혼', '原神', '銀魂'):
                continue
            pattern = re.escape(alias).replace(r'\ ', r'\s*')
            if alias.isascii():
                pattern = r'(?<![A-Za-z0-9])' + pattern + r'(?![A-Za-z0-9])'
            hit = re.search(pattern, text, re.I)
            if hit:
                hits.setdefault(work['ko'], hit.group())
                break
    for name, quote in hits.items():
        evidence.append({'field': 'franchise', 'value': name, 'quote': quote})
    heading=next((line.strip() for line in text.splitlines() if line.strip()),'')
    compact=re.sub(r'\s+','',heading)
    named_exhibition=any(re.search(re.escape(re.sub(r'\s+','',name))+r'(?:展|전시회|전시|전)(?![가-힣])',compact,re.I)
        for name in [*hits,*hits.values()])
    # The named event takes precedence over incidental mentions of a shop/menu.
    if re.search(CATEGORIES['COLLAB_CAFE'],heading,re.I):categories=['COLLAB_CAFE']
    elif named_exhibition or re.search(CATEGORIES['EXHIBITION'],heading,re.I):categories=['EXHIBITION']
    elif re.search(CATEGORIES['POPUP_STORE'],heading,re.I):categories=['POPUP_STORE']
    evidence=[e for e in evidence if e['field']!='category' or e['value'] in categories]
    if named_exhibition and not any(e['field']=='category' for e in evidence):
        evidence.append({'field':'category','value':'EXHIBITION','quote':heading})
    cue = re.search(IP_CONTEXT, text, re.I)
    if cue:
        evidence.append({'field': 'ip_context', 'quote': cue.group()})
    relevant = bool(hits or cue)
    state = ('REJECTED_NOT_EVENT' if not categories else
             'REJECTED_NOT_SUBCULTURE' if not relevant else 'PENDING_REVIEW')
    # Parse only fully explicit calendar dates. Partial dates stay in source snippets.
    dates = []
    for match in re.finditer(r'(?<!\d)(20\d{2})\s*[./년\-]\s*(\d{1,2})\s*[./월\-]\s*(\d{1,2})\s*일?', text):
        try:
            value = date(*map(int, match.groups())).isoformat()
        except ValueError:
            continue
        dates.append((value, match.group().strip()))
    distinct = list(dict.fromkeys(v for v, _ in dates))
    # Multiple dates may denote booking and event periods. Do not choose between them.
    start = end = None
    period_line = re.search(r'(?:행사\s*기간|전시\s*기간|개최\s*기간|開催期間|会期|기간)\s*[:：]?([^\n]+)', text)
    if period_line:
        period_dates = [(v, quote) for v, quote in dates if quote in period_line.group()]
        if len(period_dates) in (1, 2):
            start = period_dates[0][0]
            end = period_dates[-1][0] if len(period_dates) == 2 else None
            if end and end < start:
                start = end = None
            else:
                evidence.append({'field': 'period', 'quote': period_line.group()})
    range_pattern = (r'(?<!\d)(20\d{2})\s*[./년\-]\s*(\d{1,2})\s*[./월\-]\s*(\d{1,2})'
                     r'\s*일?\s*(?:\([^\n)]{1,12}\))?\s*[~〜～–—-]\s*'
                     r'(?:(20\d{2})\s*[./년\-]\s*)?(\d{1,2})\s*[./월\-]\s*(\d{1,2})\s*일?')
    ranges = {}
    for line in text.splitlines():
        if re.search(r'예매|예약|판매|reservation|booking|販売', line, re.I):
            continue
        for match in re.finditer(range_pattern, line):
            y, m, d, ey, em, ed = match.groups()
            try:
                first = date(int(y), int(m), int(d))
                last = date(int(ey or y), int(em), int(ed))
            except ValueError:
                continue
            if last < first:
                continue  # Missing year across New Year stays unknown.
            ranges[(first.isoformat(), last.isoformat())] = match.group()
    if len(ranges) == 1:
        (start, end), quote = next(iter(ranges.items()))
        evidence.append({'field':'period','quote':quote})
        if not re.search(r'20\d{2}.*[~〜～–—-]\s*20\d{2}',quote):
            evidence.append({'field':'end_year_inherited_from_explicit_start','quote':quote})
    elif len(ranges) > 1:
        start = end = None
    period_text = next((e['quote'] for e in reversed(evidence) if e['field']=='period'), None)
    year_inferred = False
    if not ranges:
        # Anchor yearless dates to publication time, never today's collector clock.
        partial_pattern = (r'(?<![\d./])(\d{1,2})\s*[./월]\s*(\d{1,2})\s*일?\s*'
            r'(?:\(?([월화수목금토일]|Mon|Tue|Wed|Thu|Fri|Sat|Sun)\)?)?\s*\\?[~〜～–—-]\s*'
            r'(\d{1,2})\s*[./월]\s*(\d{1,2})\s*일?\s*(?:\(?([월화수목금토일]|Mon|Tue|Wed|Thu|Fri|Sat|Sun)\)?)?')
        partials=[]
        for line in text.splitlines():
            if re.search(r'예매|예약|판매|reservation|booking|販売',line,re.I):continue
            partials.extend(re.finditer(partial_pattern,line,re.I))
        if partials:period_text=' / '.join(dict.fromkeys(m.group().strip() for m in partials))
        try:
            anchor=datetime.fromisoformat(str(published_at).replace('Z','+00:00'))
            if anchor.tzinfo is None:raise ValueError()
            anchor=anchor.astimezone(ZoneInfo('Asia/Seoul')).date()
        except (ValueError,TypeError):anchor=None
        resolved={}
        weekdays={'월':0,'화':1,'수':2,'목':3,'금':4,'토':5,'일':6,
                  'mon':0,'tue':1,'wed':2,'thu':3,'fri':4,'sat':5,'sun':6}
        if anchor:
            for m in partials:
                month,day,weekday,end_month,end_day,end_weekday=m.groups()
                choices=[]
                for year in (anchor.year-1,anchor.year,anchor.year+1):
                    try:
                        first=date(year,int(month),int(day))
                        last=date(year+(int(end_month)<int(month)),int(end_month),int(end_day))
                    except ValueError:continue
                    if abs((first-anchor).days)>183 or (last-first).days>183:continue
                    if any(label and label.strip().casefold() in weekdays and value.weekday()!=weekdays[label.strip().casefold()]
                        for label,value in ((weekday,first),(end_weekday,last))):continue
                    choices.append((abs((first-anchor).days),first,last))
                choices.sort()
                if choices and (len(choices)==1 or choices[0][0]!=choices[1][0]):
                    _,first,last=choices[0]
                    resolved[(first.isoformat(),last.isoformat())]=m.group().strip()
            if len(resolved)==1 and len({m.group().strip() for m in partials})==1:
                (start,end),quote=next(iter(resolved.items()))
                year_inferred=True
                evidence.append({'field':'period_year_from_publication','quote':quote,
                    'published_at':str(published_at),'basis':'nearest publication year within 183 days; explicit weekdays checked'})
            elif partials:start=end=None
    if not period_text:
        calendar_lines=[line.strip() for line in text.splitlines()
            if re.match(r'^\s*[📅🗓📆]',line) and re.search(r'\d',line)
            and not re.search(r'예매|예약|판매|reservation|booking|販売',line,re.I)]
        if calendar_lines:period_text=' / '.join(calendar_lines)
    periods=[{'start_date':a,'end_date':b} for a,b in ranges]
    if not periods and start and end:periods=[{'start_date':start,'end_date':end}]
    months={name:i for i,names in enumerate([
        ('jan','january'),('feb','february'),('mar','march'),('apr','april'),('may',),('jun','june'),
        ('jul','july'),('aug','august'),('sep','sept','september'),('oct','october'),('nov','november'),('dec','december')],1) for name in names}
    month_pattern='|'.join(sorted(months,key=len,reverse=True))
    english_pattern=(rf'\b({month_pattern})\s+(\d{{1,2}})\s*(?:\([^)]{{1,12}}\))?\s*[~–—-]\s*'
        rf'({month_pattern})\s+(\d{{1,2}})\s*(?:\([^)]{{1,12}}\))?\s*,?\s*(20\d{{2}})\b')
    for line in text.splitlines():
        if re.search(r'booking|reservation|販売|예매|예약|판매',line,re.I):continue
        for m in re.finditer(english_pattern,line,re.I):
            sm,sd,em,ed,year=m.groups()
            try:first=date(int(year),months[sm.casefold()],int(sd));last=date(int(year),months[em.casefold()],int(ed))
            except ValueError:continue
            if last<first:continue
            item={'start_date':first.isoformat(),'end_date':last.isoformat()}
            if item not in periods:periods.append(item)
            evidence.append({'field':'period','quote':m.group()})
    if len(periods)==1:start,end=periods[0]['start_date'],periods[0]['end_date']
    elif len(periods)>1:start=end=None
    venue_hit = re.search(r'(?:장소|会場|venue)\s*[:：]\s*([^\n]{1,150})', text, re.I)
    venue = venue_hit.group(1).strip() if venue_hit else None
    if venue_hit:
        evidence.append({'field': 'venue', 'quote': venue_hit.group()})
    venues=[venue] if venue else []
    if not venue:
        venue_lines = list(dict.fromkeys(line.strip() for line in text.splitlines()
            if re.match(r'^\s*(?:📍\s*|(?:AK\s*(?:PLAZA|플라자)|DUEX\s*\(덕스\))\s*)',line,re.I)
            and not re.match(r'^\s*📍\s*(?:장소|会場|venue)\s*[:：]',line,re.I)))
        if len(venue_lines) == 1:
            venue = venue_lines[0].removeprefix('📍').strip()
            evidence.append({'field':'venue','quote':venue_lines[0]})
        venues=[line.removeprefix('📍').strip() for line in venue_lines]
    title = next((line.strip()[:240] for line in text.splitlines() if line.strip()), None)
    # Same work/date/venue is only a possible duplicate, never an automatic merge.
    duplicate = hashlib.sha256(json.dumps([sorted(hits), start, end, normalize(venue)], ensure_ascii=False).encode()).hexdigest() if hits and start and end and venue else None
    warnings = []
    if not start: warnings.append('EVENT_PERIOD_UNCONFIRMED')
    if not venue: warnings.append('VENUE_UNCONFIRMED')
    if not hits: warnings.append('IP_NAME_UNCONFIRMED')
    warnings.append('HUMAN_REVIEW_REQUIRED_BEFORE_PUBLICATION')
    return {'status': state, 'categories': categories, 'title': title, 'franchises': list(hits),
            'start_date': start, 'end_date': end, 'venue': venue,
            'period_text':period_text,'year_inferred':year_inferred,'periods':periods,'venues':venues,
            'explicit_date_mentions': distinct, 'evidence': evidence, 'warnings': warnings,
            'duplicate_key': duplicate, 'is_subculture_relevant': relevant}

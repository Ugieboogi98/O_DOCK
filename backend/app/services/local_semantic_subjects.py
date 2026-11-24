"""Recover explicit named subjects without treating every unknown word as a character."""
import re
import unicodedata
from difflib import SequenceMatcher
from functools import lru_cache
import hashlib
import json
from pathlib import Path

KANA=dict(zip(
    'アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポヴ',
    'a i u e o ka ki ku ke ko sa shi su se so ta chi tsu te to na ni nu ne no ha hi fu he ho ma mi mu me mo ya yu yo ra ri ru re ro wa o n ga gi gu ge go za ji zu ze zo da ji zu de do ba bi bu be bo pa pi pu pe po vu'.split()))
INITIAL='g kk n d tt r m b pp s ss _ j jj ch k t p h'.split()
VOWEL='a ae ya yae eo e yeo ye o wa wae oe yo u wo we wi yu eu ui i'.split()
FINAL='_ g kk gs n nj nh d r rg rm rb rs rt rp rh m b bs s ss ng j ch k t p h'.split()

def phonetic(value):
    out=[]
    value=unicodedata.normalize('NFKC',value)
    value=''.join(chr(ord(c)+0x60) if 0x3041<=ord(c)<=0x3096 else c for c in value)
    digraphs={}
    for first,base in [('キ','ky'),('シ','sh'),('チ','ch'),('ニ','ny'),('ヒ','hy'),('ミ','my'),('リ','ry'),('ギ','gy'),('ジ','j'),('ビ','by'),('ピ','py')]:
        for small,vowel in [('ャ','a'),('ュ','u'),('ョ','o')]:digraphs[first+small]=base+vowel
    digraphs.update({'ティ':'ti','ディ':'di','ファ':'fa','フィ':'fi','フェ':'fe','フォ':'fo','ウィ':'wi','ウェ':'we','ウォ':'wo','ヴァ':'va','ヴィ':'vi','ヴェ':'ve','ヴォ':'vo'})
    for pair,reading in digraphs.items():value=value.replace(pair,reading)
    for c in value:
        n=ord(c)
        if 0x3041<=n<=0x3096:c=chr(n+0x60)
        if c in KANA:out.append(KANA[c])
        elif c in 'ァィゥェォャュョ':out.append(dict(zip('ァィゥェォャュョ','a i u e o ya yu yo'.split()))[c])
        elif c in 'ッー':continue
        elif 0xAC00<=n<=0xD7A3:
            x=n-0xAC00;out.append(INITIAL[x//588]+VOWEL[(x%588)//28]+FINAL[x%28])
        elif c.isascii() and c.isalpha():out.append(c.casefold())
        elif c in ' ・·.ー-\t':continue
        else:return None
    text=''.join(out).replace('_','')
    for old,new in [('ae','e'),('eo','o'),('eu','u'),('sh','s'),('ch','t'),('ts','t'),('j','z'),('sy','s'),('ty','t'),('zy','z'),('l','r'),('g','k'),('d','t'),('b','p')]:text=text.replace(old,new)
    return re.sub(r'(.)\1+',r'\1',text)

def sound_matches(original,ko):
    # Kana-only names have a checkable reading. Unknown kanji readings remain withheld.
    if not re.fullmatch(r'[ァ-ヺー・ ぁ-ゖ]+',original) or not re.fullmatch(r'[가-힣 ·]+',ko):return False
    first,second=phonetic(original),phonetic(ko)
    if not first or not second or len(second)<2:return False
    if first[0] in 'aeiou' and second[0]!=first[0]:return False
    return first==second

def title_key(source):
    return hashlib.sha256(json.dumps([source.get('official_url') or '',source.get('name_original') or ''],ensure_ascii=False).encode()).hexdigest()

@lru_cache(maxsize=1)
def title_memory():
    path=Path(__file__).with_name('local_semantic_catalog_titles.json')
    return json.loads(path.read_text(encoding='utf-8')).get('titles',{}) if path.exists() else {}

def catalog_reading(source,original,proposed):
    title=title_memory().get(title_key(source))
    if not title:return None
    # An existing publication is a consistency check, not independent name certification.
    tokens=title.split();choices={}
    for start in range(len(tokens)):
        for end in range(start+1,min(len(tokens),start+6)+1):
            phrase=' '.join(tokens[start:end]).strip('【】[]()（）「」『』-・·')
            if not re.fullmatch(r'[가-힣 ·]+',phrase):continue
            first,second=phonetic(original),phonetic(phrase)
            if not first and re.sub(r'\s+','',phrase)==re.sub(r'\s+','',proposed):return phrase
            if first and second:
                score=SequenceMatcher(None,first,second).ratio()
                if score>=0.9:choices[phrase]=score
    ranked=sorted(choices.items(),key=lambda item:item[1],reverse=True)
    if ranked and (len(ranked)==1 or ranked[0][1]-ranked[1][1]>=0.05):return ranked[0][0]
    return None

def explicit_subject(source,original,grounded):
    from app.services.reference_classifier import match,norm
    from app.services.semantic_rules import context_candidates
    if not original or re.search(r'フィギュア|スケール|シリーズ|オリジナル|プラスチック|ぬいぐるみ|未確認|キャラクター',original):return False
    title=source.get('name_original') or ''
    if not match(original,title):return False
    work=grounded.get('franchise')
    if work and (norm(original)==norm(work['original']) or (original in work['original'] and work['original'] in title)):
        return False
    if norm(original) in {norm(source.get(k)) for k in ('manufacturer','product_line')}:return False
    relations=context_candidates(source)
    if any(c['kind']=='franchise' and norm(c['original'])==norm(original) for c in relations):return False
    for i in range(3):
        body=source.get(f'document_{i}') or ''
        try:body=json.loads(body).get('description','')
        except (ValueError,AttributeError):pass
        if re.search(r'艦船|戦艦|艦艇|宇宙船',body[:700]):return False
    if norm(original)==norm(source.get('character')):return True
    if any(c['kind']=='character' and norm(c['original'])==norm(original)
           and (work or re.search(r'登場人物|キャラクター|ヒロイン|パイロット',c['evidence'])) for c in relations):return True
    # A known work plus "NAME 1/7 scale figure" explicitly names the figure's subject.
    if norm(original)==norm(source.get('franchise')):return False
    scale=re.search(r'(?<!\d)1\s*[/／]\s*\d+\s*(?:スケール|scale)',title,re.I)
    if not scale:return False
    head=title[:scale.start()].strip(' \t【】「」『』[]')
    if work and work['original'] in head:head=head.replace(work['original'],'',1).strip(' \t【】「」『』[]')
    for brand in (source.get('product_line'),source.get('manufacturer')):
        if brand and head.startswith(brand):head=head[len(brand):].strip()
    subject=re.split(r'\s+[-–—]\s+',head,maxsplit=1)[0].strip()
    return norm(subject)==norm(original)

def recover(source,raw,grounded):
    from app.services.semantic_rules import evidence,korean
    found=[]
    for row in raw.get('characters',[]) if isinstance(raw.get('characters'),list) else []:
        if not isinstance(row,dict):continue
        original,ko=row.get('original'),row.get('ko')
        if not isinstance(original,str) or not korean(ko):continue
        if not evidence(row,source,{'name_original','character','document_0','document_1','document_2'}):continue
        if original not in row['evidence'] or row['confidence']<0.95:continue
        if not explicit_subject(source,original,grounded):continue
        existing=catalog_reading(source,original,ko)
        if existing:ko=existing
        elif not sound_matches(original,ko):continue
        if any(c['original']==original for c in grounded['characters']):continue
        found.append({**row,'ko':ko,'method':'explicit_subject_catalog_consistency' if existing else 'explicit_subject_kana_reading'})
    return found

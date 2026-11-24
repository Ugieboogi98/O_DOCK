"""Evidence-backed offline resolution using checked web reference snapshots."""
import argparse
from functools import lru_cache
from collections import Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys
import unicodedata

ROOT = Path(__file__).resolve().parent
GENERIC_SUBJECTS = frozenset(('피규어', '전사'))


@lru_cache(maxsize=60000)
def norm(text):
    return re.sub(r'[\s\U000e0100-\U000e01ef\ufe00-\ufe0f]+', '', unicodedata.normalize('NFKC', text or '')).casefold()


def match(alias, text):
    if not text or not alias:
        return None
    if norm(alias) not in norm(text):
        return None
    pattern = re.escape(alias)
    if alias.isascii():
        pattern = r'(?<![A-Za-z])' + pattern + r'(?![A-Za-z])'
    elif re.fullmatch(r'[가-힣\s.]+', alias):
        pattern = r'(?<![가-힣])' + pattern + r'(?![가-힣])'
    elif re.fullmatch(r'[ァ-ヺー・\s]+', alias):
        pattern = r'(?<![ァ-ヺー])' + pattern + r'(?![ァ-ヺー])'
    found = re.search(pattern, text, re.IGNORECASE)
    if found:
        return found.group()
    needle = norm(alias)
    if len(needle) >= 3 and needle in norm(text):
        normalized, positions = [], []
        for index, character in enumerate(text):
            for value in unicodedata.normalize('NFKC', character).casefold():
                if not value.isspace() and not ('\U000e0100' <= value <= '\U000e01ef' or '\ufe00' <= value <= '\ufe0f'):
                    normalized.append(value)
                    positions.append(index)
        start = ''.join(normalized).find(needle)
        if start >= 0:
            begin, end = positions[start], positions[start + len(needle) - 1] + 1
            if re.fullmatch(r'[가-힣\s.]+', alias) and (
                    begin > 0 and '가' <= text[begin - 1] <= '힣' or
                    end < len(text) and '가' <= text[end] <= '힣'):
                return None
            if re.fullmatch(r'[ァ-ヺー・\s]+', alias) and (
                    begin > 0 and re.fullmatch(r'[ァ-ヺー]', text[begin - 1]) or
                    end < len(text) and re.fullmatch(r'[ァ-ヺー]', text[end])):
                return None
            return text[begin:end]
    return None


def proof(field, term, reference, evidence=None):
    return {'field': field, 'match': term, 'reference_url': reference['url'],
            'reference_evidence': evidence or reference['evidence'],
            'checked_at': reference['checked_at'], 'reference_sha256': reference.get('sha256'),
            'verification': reference.get('verification', 'live_web_reference')}


def knowledge(rules, checked, wiki):
    works, characters, forms = [], [], []
    for row in wiki.get('entries', {}).values():
        categories = ' '.join(row.get('categories', [])).casefold()
        base = {'url': row['url'], 'evidence': row['evidence'], 'checked_at': wiki['checked_at']}
        aliases = list(dict.fromkeys([row['alias'], row['canonical'], row['ko']]))
        # Reject topics such as Ram -> RAM hardware, flowers and list articles.
        is_character = any(key in categories for key in ('登場人物', '架空', 'キャラクター', 'fictional', 'characters', 'vocaloid', 'vtuber', 'バーチャル', '등장인물', '가공의', '캐릭터'))
        if row.get('language') == 'ko':
            alias, canonical = norm(row['alias']), norm(row['ko'])
            # A surname redirect (우치하 -> 우치하 사스케), organization or
            # transformation (초사이어인 -> 사이어인) is not an identity match.
            if alias != canonical and (not canonical.endswith(alias) or alias not in canonical):
                is_character = False
            if any(token in categories for token in ('범죄조직', 'fictional organizations')):
                is_character = False
        if row['ko'] in GENERIC_SUBJECTS or any(token in categories for token in ('캐릭터 디자인', '전형적 등장인물')):
            is_character = False
        if 'character' in row['seed_roles'] and is_character and not any(key in row['ko'] for key in ('등장인물', '목록', '캐릭터 목록')):
            characters.append({'ko': row['ko'], 'aliases': aliases, 'work': None, 'priority': 1, 'reference': base})
        is_work = any(key in categories for key in ('漫画', 'アニメ', '小説', 'ゲーム', '映画', '作品', 'シリーズ', 'ライトノベル', 'anime', 'manga', 'novel', 'video games', 'television', 'comics', 'films', 'vocaloid', 'バーチャル', 'vtuber', '만화', '애니메이션', '소설', '비디오 게임', '영화', '텔레비전 드라마', '텔레비전 프로그램'))
        if 'franchise' in row['seed_roles'] and is_work and not any(key in row['ko'] for key in ('목록', '등장인물')):
            works.append({'ko': row['ko'], 'aliases': aliases, 'priority': 1, 'reference': base})
    for series in rules['series']:
        valid_pages = [url for url in series['urls'] if any(checked.get(url, {}).get('terms', {}).get(a) for a in series['aliases'])]
        if valid_pages:
            url = valid_pages[0]
            ref = dict(url=url, evidence=next(a for a in series['aliases'] if checked[url]['terms'].get(a)),
                verification=checked[url].get('verification', 'live_web_reference'),
                **{k: checked[url][k] for k in ('checked_at', 'sha256')})
            works.append({'ko': series['ko'], 'aliases': series['aliases'] + [series['ko']], 'priority': 2, 'reference': ref})
        for aliases, ko in series['characters']:
            aliases = aliases.split('|')
            for url in series['urls']:
                page = checked.get(url, {})
                actual = next((a for a in aliases if page.get('terms', {}).get(a)), None)
                if actual:
                    short_ko = ko.split()[-1]
                    characters.append({'ko': ko, 'aliases': list(dict.fromkeys(aliases + [ko, short_ko])), 'work': series['ko'], 'priority': 2,
                        'reference': {'url': url, 'evidence': actual, 'checked_at': page['checked_at'], 'sha256': page['sha256']}})
                    break
    for rule in rules['forms']:
        page = checked.get(rule['url'], {})
        if page.get('terms', {}).get(rule['quote']):
            forms.append(dict(rule, reference={'url': rule['url'], 'evidence': rule['quote'],
                'checked_at': page['checked_at'], 'sha256': page['sha256']}))
    return works, characters, forms


def compatible(work, expected):
    return (not expected or not work or norm(work) == norm(expected) or
        len(norm(expected)) >= 3 and norm(work).startswith(norm(expected)) or
        any(root in work and root in expected for root in ('나루토', '드래곤볼')))


def work_match(alias, text):
    found = match(alias, text)
    if found and alias == 'ナルト' and 'うずまきナルト' in text:
        return match(alias, text.replace('うずまきナルト', ' '))
    if found and norm(alias) == norm('ワンピース'):
        # Clothing/version compounds are not a reference to the manga franchise.
        for occurrence in re.finditer(re.escape(found), text):
            before, after = text[:occurrence.start()], text[occurrence.end():]
            if (before and re.search(r'[ァ-ヿー]$', before) or
                    re.match(r'(?:ver\b|バージョン|姿|衣装|ドレス)', after, re.I)):
                continue
            return found
        return None
    return found


def resolve(row, works, characters, forms):
    source, old = row['source'], row.get('fields', {})
    title = source['name_original']
    record = {'figure_id': row['figure_id'], 'source_hash': row['source_hash'],
              'approved': True, 'method': 'web_verified', 'patch': {}, 'proofs': {}}
    work_hits = []
    work_inputs = [('franchise', source.get('franchise') or ''), ('name_original', title), ('product_line', source.get('product_line') or '')]
    for n in range(3):
        field = f'document_{n}'
        body = source.get(field) or ''
        try:
            payload = json.loads(body)
        except (ValueError, TypeError):
            payload = {}
        if isinstance(payload, dict):
            for key in ('franchise', 'series', 'work'):
                value = payload.get(key)
                if isinstance(value, str) and value in body:
                    work_inputs.append((field, value))
        intro = re.split(r'※|別売|関連商品|おすすめ|同時発売', body, maxsplit=1)[0][:2000]
        for value in re.findall(r'[『「]([^』」\n]{2,90})[』」](?:より|から|の)', intro):
            work_inputs.append((field, value))
    for work in works:
        for field, text in work_inputs:
            for alias in work['aliases']:
                if norm(alias) == norm('ディズニー') and norm(text) != norm(alias):
                    continue
                if field != 'franchise' and len(norm(alias)) < 3 and alias not in ('銀魂', '原神'):
                    continue
                found = work_match(alias, text)
                if found:
                    strength = 4 if field == 'franchise' else 3 if field.startswith('document_') else 2 if field == 'name_original' else 1
                    work_hits.append(((strength, work['priority'], len(norm(alias))), work, field, found))
    selected_work = max(work_hits, key=lambda x: x[0]) if work_hits else None
    work_name = selected_work[1]['ko'] if selected_work else old.get('franchise_ko')
    if selected_work:
        _, work, field, found = selected_work
        record['patch']['franchise_ko'] = work_name
        record['proofs']['franchise_ko'] = [proof(field, found, work['reference'])]
    subject_title = re.sub(r'[（(]\s*VS[^)）]*[）)]', lambda m: ' ' * len(m.group()), title, flags=re.IGNORECASE)
    masked = []
    has_opponent = subject_title != title
    for _, work, field, found in sorted(work_hits, key=lambda hit: -len(hit[3])):
        if norm(work['ko']) == norm(work_name) and field == 'name_original':
            subject_brand = norm(work_name) in (norm('하츠네 미쿠'), norm('슈퍼 소니코'))
            series_heading = found.endswith('シリーズ') or found + 'シリーズ' in title
            start = title.find(found)
            end = start + len(found)
            # Nested work aliases refer to the same original heading, even after masking.
            # Searching the shortened title could otherwise erase ナルト inside うずまきナルト.
            if start >= 0 and not any(start < right and end > left for left, right in masked) and (not subject_brand or series_heading):
                subject_title = subject_title[:start] + ' ' * len(found) + subject_title[end:]
                masked.append((start, end))
    char_hits = []
    for character in characters:
        if not compatible(work_name, character['work']):
            continue
        character_inputs = [('name_original', subject_title)]
        if not has_opponent:
            character_inputs.insert(0, ('character', source.get('character') or ''))
        for field, text in character_inputs:
            for alias in sorted(character['aliases'], key=len, reverse=True):
                if len(norm(alias)) < 3 and not character['work'] and norm(text) != norm(alias):
                    continue
                found = match(alias, text)
                if found and found in (source.get(field) or ''):
                    char_hits.append((len(norm(alias)), character, field, found))
                    break
    char_hits.sort(key=lambda x: (x[0], x[1].get('priority', 0)), reverse=True)
    subjects, proofs, covered = [], [], []
    for length, character, field, found in char_hits:
        if any(found != prior and found in prior for prior in covered):
            continue
        if character['ko'] in [item['ko'] for item in subjects]:
            continue
        covered.append(found)
        subjects.append({'original': found, 'ko': character['ko'], 'evidence_field': field,
                         'evidence': found, 'method': 'web_verified'})
        proofs.append(proof(field, found, character['reference']))
    if subjects:
        previous_subjects = {item.get('original') for item in old.get('characters', []) if item.get('ko') not in GENERIC_SUBJECTS}
        new_subjects = {item['original'] for item in subjects}
        # Do not replace a multi-character decision with an incomplete subset.
        if has_opponent or len(previous_subjects) <= 1 or previous_subjects.issubset(new_subjects) or old.get('field_status', {}).get('character_ko') != 'ready':
            record['patch']['character_ko'] = subjects
            record['proofs']['character_ko'] = proofs
    kind = None
    source_ref = {'url': source.get('_document_0_url') or source['official_url'], 'evidence': '',
                  'checked_at': datetime.now(timezone.utc).isoformat(), 'verification': 'stored_catalog_metadata'}
    def literal(code, field, phrase):
        return code, proof(field, phrase, source_ref, phrase)
    # Accessories precede figure brand names. A bonus accessory is not the whole item.
    accessory = re.search(r'(?:専用.*(?:台座|パーツ)|オプションパーツセット|おようふくセット|ディスプレイスタンド|ポンチョ)', title)
    if accessory and not any(token in title for token in ('付属', '付き', 'セット版')):
        kind = literal('figure_parts', 'name_original', accessory.group())
    if (source.get('product_line') or '').startswith('フリューくじ'):
        kind = literal('lottery_goods', 'product_line', source['product_line'])
    for code, pattern in [
        ('plush', r'ぬいぐるみ|plush|봉제인형|봉제 인형'), ('acrylic_stand', r'アクリルスタンド|アクスタ|아크릴 스탠드'),
        ('rubber_mascot', r'ラバーマスコット|ラバーストラップ'),
        ('keychain', r'キーホルダー|アクリルキーチェーン'),
        ('noodle_stopper', r'ぬーどるストッパー|ヌードルストッパー|누들\s?스토퍼'),
        ('nendoroid', r'ねんどろいど|넨도로이드'), ('action_figure', r'アクションフィギュア|可動フィギュア|액션 피규어'),
        ('chibi_figure', r'デフォルメフィギュア'), ('soft_vinyl', r'ソフビ|ソフトビニール'),
        ('mini_figure', r'ミニフィギュア|ミニサイズ|\[mini\]')]:
        found = re.search(pattern, title, re.IGNORECASE)
        if kind is None and found:
            kind = literal(code, 'name_original', found.group())
    for form in forms:
        if kind:
            break
        for field in ('product_line', 'name_original'):
            vehicle_only = (re.search(r'マシン|マシーン|バイク|ビークル', title) or
                title.startswith('ハリケーン') and source.get('franchise') == '仮面ライダーV3') and not re.search(r'セット|[＆&]|フィギュア', title)
            if form['code'] == 'action_figure' and field == 'product_line' and vehicle_only:
                continue
            found = next((match(a, source.get(field) or '') for a in form['aliases'] if match(a, source.get(field) or '')), None)
            if found:
                kind = (form['code'], proof(field, found, form['reference']))
                break
    if kind is None and source.get('type') == 'model_kit':
        kind = literal('model_kit', 'type', 'model_kit')
    if kind is None:
        for field in ('scale', 'name_original'):
            found = re.search(r'\d+\s*/\s*\d+', source.get(field) or '')
            if found:
                kind = literal('scale_figure', field, found.group())
                break
    if kind is None:
        # Restrict free-text description checks to explicit product-type nouns,
        # not related-product advertising or ambiguous pose/size descriptions.
        for n in range(3):
            field = f'document_{n}'
            body = (source.get(field) or '').split('別売', 1)[0].split('※', 1)[0]
            for code, pattern in [('scale_figure', r'(?<![\d/])\d+\s*/\s*\d+\s*スケール'),
                    ('non_scale_figure', r'ノンスケールフィギュア|논스케일 피규어'),
                    ('completed_figure', r'彩色済み完成品フィギュア|塗装済み完成品フィギュア'),
                    ('rubber_mascot', r'ラバーマスコット|ラバーストラップ'),
                    ('static_figure', r'スタチュー|STATUE|非可動フィギュア'),
                    ('plush', r'ぬいぐるみ')]:
                found = re.search(pattern, body, re.IGNORECASE)
                if found:
                    kind = literal(code, field, found.group())
                    break
            if kind:
                break
    if kind is None and (source.get('product_line') or '').startswith('フリューくじ'):
        kind = literal('lottery_goods', 'product_line', source['product_line'])
    # Prize is a confirmed broad category; never pretend its articulation/scale is known.
    if kind is None and any(host in source['official_url'] for host in ('bsp-prize.jp/', 'banpresto.jp/')) and source.get('type') == 'figure':
        kind = literal('prize_figure', 'official_url', source['official_url'])
    if kind:
        record['patch']['figure_form'] = kind[0]
        record['proofs']['figure_form'] = [kind[1]]
    return record



@lru_cache(maxsize=1)
def cached_knowledge():
    file = Path(__file__).with_name('classification_knowledge.json')
    data = json.loads(file.read_text(encoding='utf-8')) if file.exists() else {'works': [], 'characters': [], 'forms': []}
    supplement = file.with_name('classification_wikipedia_anime.json')
    if supplement.exists():
        known = {norm(alias) for work in data['works'] for alias in work['aliases']}
        for work in json.loads(supplement.read_text(encoding='utf-8'))['works']:
            if norm(work['ko']) in known:
                continue
            work['aliases'] = [a for a in work['aliases'] if norm(a) not in known]
            if work['aliases']:
                data['works'].append(work)
    # A shared encyclopedia article about a duo is not an identity mapping for either individual.
    data['characters'] = [row for row in data['characters'] if row['ko'] != '카가미네 린·렌']
    for original, english, ko in [('鏡音リン', 'Kagamine Rin', '카가미네 린'),
                                   ('鏡音レン', 'Kagamine Len', '카가미네 렌')]:
        data['characters'].append({'ko': ko, 'aliases': [original, english, ko], 'work': None, 'priority': 3,
            'reference': {'url': 'https://piapro.net/intl/en_character.html',
                          'evidence': english, 'checked_at': '2026-11-11', 'verification': 'live_web_reference'}})
    # Redirects to a shared article do not prove that different incarnations are identical.
    asuka_aliases = {'式波・アスカ・ラングレー': '시키나미 아스카 랑그레이',
                     '惣流・アスカ・ラングレー': '소류 아스카 랑그레이',
                     'アスカ・ラングレー': '아스카 랑그레이'}
    for character in data['characters']:
        character['aliases'] = [a for a in character['aliases'] if a not in asuka_aliases]
    for original, ko in asuka_aliases.items():
        data['characters'].append({'ko': ko, 'aliases': [original], 'work': None, 'priority': 4,
            'reference': {'url': 'https://www.evangelion.co.jp/', 'evidence': original,
                          'checked_at': '2026-11-11', 'verification': 'agent_curated_identity_distinction'}})
    # A series root cannot imply a particular installment or subtitle.
    for original, ko in [('ゴジラ', '고질라'), ('ソフィーのアトリエ', '소피의 아틀리에')]:
        for work in data['works']:
            work['aliases'] = [a for a in work['aliases'] if norm(a) != norm(original)]
        data['works'].append({'ko': ko, 'aliases': [original], 'priority': 3,
            'reference': {'url': '', 'evidence': original, 'checked_at': '2026-11-11',
                          'verification': 'agent_curated_series_root'}})
    for work in data['works']:
        if any('とある科学の超電磁砲' in a for a in work['aliases']):
            work['ko'] = work['ko'].replace('초전차포', '초전자포').removesuffix(' (애니메이션)')
    return data


def search_title_aliases(query):
    """Expand only an unambiguous complete title, never a substring."""
    hits = [work for work in cached_knowledge()['works']
            if any(norm(query) == norm(alias) for alias in work['aliases'])]
    if len({work['ko'] for work in hits}) != 1:
        return [query]
    return list(dict.fromkeys([query, *hits[0]['aliases']]))


def cached_record(source, digest, figure_id, previous=None):
    data = cached_knowledge()
    if not data:
        return None
    return resolve({'figure_id': figure_id, 'source': source, 'source_hash': digest,
                    'fields': previous or {}}, data['works'], data['characters'], data['forms'])

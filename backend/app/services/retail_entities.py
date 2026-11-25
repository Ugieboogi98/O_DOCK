"""Recognise the work and characters named in a Korean retail listing title.

Retail titles are Korean ("넨도로이드 1598 명일방주 라플란드 재판") while most catalog titles are
Japanese, so character n-grams alone rarely line up. The curated dictionary groups list each
work with its Japanese/Korean/English aliases and its characters, which lets the matcher look for
candidates inside the same work and drop candidates from a different one.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

from app.core.config import get_settings
from app.services.semantic_rules import normalize

_cache = {'key': None, 'groups': []}
# Makers and brands are not works, although bad labels sometimes use them as one (반프레스토).
NOT_WORKS = {'반프레스토', '반다이', '반다이 스피리츠', '굿스마일', '굿스마일 컴퍼니', '메가하우스', '후류', '세가', '타이토', '코토부키야',
             '알터', '맥스팩토리', '프라이즈', '마스코트', '컬렉션', '넨도로이드', '피그마', '봉제인형', '아크릴 스탠드', '피규어'}
LETTER = r'[\w぀-ヿ一-鿿가-힣]'
# Artist originals name no work: "1/6 키키 illustrated by RST", "오리지널 캐릭터: 히타미", "버텍스 오리지널즈".
# Only consulted when no known work is named, so "원피스 … THE ORIGINAL" stays One Piece.
ORIGINAL = re.compile(r'(?i)illustrat(?:ed|ion)\s+by|오리지널|(?<![a-z])originals?(?![a-z])|オリジナル')
ORIGINAL_WORK = '오리지널'


# Catalog labels that name the same product family under different works. Miku figures are filed under
# 보컬로이드 or 하츠네 미쿠 depending on the maker's own franchise field; for matching they are one work.
EQUIVALENT_WORKS = [{'하츠네 미쿠', '보컬로이드', '하츠네 미쿠 GT 프로젝트', '캐릭터 보컬 시리즈'}]


def same_work(a, b):
    if not a or not b:
        return False
    return a == b or any(a in s and b in s for s in EQUIVALENT_WORKS)


def _work_alias(alias):
    n = normalize(alias)
    # Short Latin abbreviations (SEL, IF, C) collide with model codes and brand words.
    if _latin(alias) and len(n) < 4:
        return False
    return len(n) >= 2 and alias.strip() not in NOT_WORKS


def _latin(value):
    return bool(re.fullmatch(r'[A-Za-z0-9 .:-]+', value))


def _contains(text, norm_text, term):
    """Latin terms need word boundaries (W, Lucy); other scripts match as substrings."""
    if not term:
        return False
    if _latin(term):
        return re.search(r'(?<![A-Za-z0-9])' + re.escape(term) + r'(?![A-Za-z0-9])', text, re.I) is not None
    if len(normalize(term)) <= 2:
        # Short names (첸, 제로) only as a separate word, never inside another (첸소맨, 쓰리제로).
        return re.search(r'(?<!' + LETTER + ')' + re.escape(term) + r'(?!' + LETTER + ')', text) is not None
    return normalize(term) in norm_text


def groups(path=None):
    path = Path(path or get_settings().data_dir / 'reference/semantic_dictionary/catalog.json')
    try:
        key = (str(path), path.stat().st_mtime_ns)
    except OSError:
        return []
    if _cache['key'] != key:
        data = json.loads(path.read_text(encoding='utf-8'))
        merged = {}

        def entry(work, aliases=(), medium=None):
            e = merged.setdefault(work, {'work': work, 'medium': medium, 'aliases': [], 'characters': {}})
            e['medium'] = e['medium'] or medium
            e['aliases'] = list(dict.fromkeys([*e['aliases'], work, *(a.strip() for a in aliases if a and a.strip())]))
            return e
        for g in data.get('domain_groups', []):
            if not g.get('work'):
                continue
            e = entry(g['work'], g.get('aliases', []), g.get('medium'))
            for names, ko in g.get('characters', []):
                for name in (names.split('|') if isinstance(names, str) else names):
                    e['characters'].setdefault(name, ko)
        # Verified work names without curated characters still identify the work.
        for w in [*data.get('knowledge', {}).get('works', []), *data.get('aliases', {}).get('franchises', [])]:
            if w.get('ko'):
                entry(w['ko'], w.get('aliases', []))
        for c in data.get('knowledge', {}).get('characters', []):
            if c.get('ko') and c.get('work') in merged:
                for name in c.get('aliases', []):
                    merged[c['work']]['characters'].setdefault(name, c['ko'])
        _cache.update(key=key, groups=list(merged.values()))
    return _cache['groups']


def with_catalog_works(base, catalog):
    """Add Korean work and character labels already validated in the catalog.

    catalog: iterable of (franchise_ko, character_ko) pairs; character_ko may list several (' · ').
    """
    merged = {g['work']: {**g, 'aliases': list(g['aliases']), 'characters': dict(g['characters'])} for g in base}
    for work, characters in catalog:
        if not work or not _work_alias(work):
            continue
        g = merged.setdefault(work, {'work': work, 'medium': None, 'aliases': [work], 'characters': {}})
        for name in (characters or '').split(' · '):
            name = name.strip()
            if name and name != work:
                g['characters'].setdefault(name, name)
    return list(merged.values())


_index_cache = {'groups': None, 'index': None, 'longest': 0}


def _alias_index(dictionary_groups):
    """normalized alias -> [(group, alias)]; thousands of works make a per-group scan too slow."""
    if _index_cache['groups'] is not dictionary_groups:
        index, longest = {}, 0
        for g in dictionary_groups:
            if g['work'] in NOT_WORKS:
                continue
            for alias in g['aliases']:
                if _work_alias(alias):
                    n = normalize(alias)
                    index.setdefault(n, []).append((g, alias))
                    longest = max(longest, len(n))
        _index_cache.update(groups=dictionary_groups, index=index, longest=longest)
    return _index_cache['index'], _index_cache['longest']


def recognize(title, dictionary_groups=None):
    """{'work', 'medium', 'characters': [ko...]} for the most specific work named, else None."""
    text = title or ''
    norm = normalize(text)
    index, longest = _alias_index(dictionary_groups if dictionary_groups is not None else groups())
    best_hit = {}
    for i in range(len(norm)):
        for j in range(i + 2, min(len(norm), i + longest) + 1):
            for g, alias in index.get(norm[i:j], ()):
                # The substring hit is a candidate; boundaries for short and Latin aliases are checked here.
                if _contains(text, norm, alias):
                    best_hit[id(g)] = max(best_hit.get(id(g), (0, g))[0], j - i), g
    found = list(best_hit.values())
    if not found:
        if ORIGINAL.search(text):
            return {'work': ORIGINAL_WORK, 'medium': 'original', 'characters': []}
        return None
    # A work whose characters are named wins (보컬로이드 하츠네미쿠 -> 하츠네 미쿠); among equals the longer
    # alias is the specific work ("명일방주 엔드필드" names both 명일방주 and 명일방주: 엔드필드).
    scored = [(bool(chars), length, g, chars) for length, g in found for chars in [_characters(text, g)]]
    _, _, best, characters = max(scored, key=lambda x: (x[0], x[1]))
    return {'work': best['work'], 'medium': best.get('medium'), 'characters': characters}


def _characters(text, group):
    # The work's own title is not a character mention (히카루 in 히카루가 죽은 여름), unless the work is
    # named after its character (하츠네 미쿠).
    names = {normalize(n) for n in group['characters']} | {normalize(k) for k in group['characters'].values()}
    rest = text
    for alias in sorted(group['aliases'], key=len, reverse=True):
        # 미쿠 is a work alias but also part of 하츠네미쿠; removing it would erase the character.
        if _work_alias(alias) and not any(normalize(alias) in n for n in names):
            rest = re.sub(re.escape(alias), ' ', rest, flags=re.I)
    rest_norm = normalize(rest)
    characters = []
    for original, ko in group['characters'].items():
        if ko not in characters and (_contains(rest, rest_norm, ko) or _contains(rest, rest_norm, original)):
            characters.append(ko)
    return characters

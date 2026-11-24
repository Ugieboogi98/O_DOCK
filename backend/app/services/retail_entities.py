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


def _work_alias(alias):
    n = normalize(alias)
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


def recognize(title, dictionary_groups=None):
    """{'work', 'medium', 'characters': [ko...]} for the most specific work named, else None."""
    text = title or ''
    norm = normalize(text)
    found = []
    for g in dictionary_groups if dictionary_groups is not None else groups():
        if g['work'] in NOT_WORKS:
            continue
        hits = [a for a in g['aliases'] if _work_alias(a) and _contains(text, norm, a)]
        if hits:
            found.append((max(len(normalize(a)) for a in hits), g))
    if not found:
        return None
    # "명일방주 엔드필드" names both 명일방주 and 명일방주: 엔드필드; the longer alias is the specific work.
    best_len, best = max(found, key=lambda x: x[0])
    # The work's own title is not a character mention (히카루 in 히카루가 죽은 여름).
    rest = text
    for alias in sorted(best['aliases'], key=len, reverse=True):
        if _work_alias(alias):
            rest = re.sub(re.escape(alias), ' ', rest, flags=re.I)
    rest_norm = normalize(rest)
    characters = []
    for original, ko in best['characters'].items():
        if ko not in characters and (_contains(rest, rest_norm, ko) or _contains(rest, rest_norm, original)):
            characters.append(ko)
    return {'work': best['work'], 'medium': best.get('medium'), 'characters': characters}

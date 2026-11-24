"""Learned alias memory and similar-product retrieval for classification.

Two complementary signals, both built only from results that already passed
strict validation (``classification_status == 'ready'``):

* ``learned`` aliases: an original-language franchise/character string mapped to
  a Korean label. An alias is kept only when at least ``MIN_SUPPORT`` distinct
  products agree on it and no product disagrees. A matching alias must still
  appear literally in this product's own source field, so the evidence rule is
  unchanged.
* ``NgramIndex``: character n-gram TF-IDF similarity over original titles. It
  works like an embedding index without a model server and is deterministic.
  The nearest verified products are given to the classification model as
  examples. They are hints only, never evidence.
"""
import math
import re
import unicodedata
from collections import Counter, defaultdict

MIN_SUPPORT = 2
MIN_ALIAS_LENGTH = 2


def _norm(value):
    return re.sub(r'\s+', '', unicodedata.normalize('NFKC', value or '')).casefold()


_KATA = 'ァ-ヺー'
_HIRA = 'ぁ-ゖ'
_LATIN = 'A-Za-z0-9'


def usable_alias(original):
    """Short kana aliases (アイ) occur inside unrelated words (アイドル), so kana-only aliases need 3+ chars."""
    text = _norm(original)
    if re.fullmatch(f'[{_KATA}{_HIRA}・]+', text):
        return len(text) >= 3
    return len(text) >= MIN_ALIAS_LENGTH


def literal_in(alias, text):
    """True when ``alias`` occurs as a whole token: not continued by the same script on either side."""
    for match in re.finditer(re.escape(alias), text or ''):
        before = text[match.start() - 1] if match.start() else ''
        after = text[match.end()] if match.end() < len(text) else ''
        glued = False
        for script in (_KATA, _HIRA, _LATIN):
            cls = re.compile(f'[{script}]')
            if (before and cls.match(before) and cls.match(alias[0])) or (after and cls.match(after) and cls.match(alias[-1])):
                glued = True
        if not glued:
            return True
    return False


def observations(name_original, fields):
    """Yield (kind, original, ko, work_ko) facts from one validated profile."""
    if not isinstance(fields, dict) or fields.get('classification_status') != 'ready':
        return []
    out = []
    evidence = fields.get('evidence') or {}
    work = evidence.get('franchise') if isinstance(evidence, dict) else None
    work_ko = fields.get('franchise_ko')
    if isinstance(work, dict) and isinstance(work.get('original'), str) and work_ko:
        out.append(('franchise', work['original'], work_ko, None))
    for item in fields.get('characters') or []:
        if isinstance(item, dict) and isinstance(item.get('original'), str) and item.get('ko'):
            out.append(('character', item['original'], item['ko'], work_ko))
    title = name_original or ''
    return [o for o in out if usable_alias(o[1]) and o[1] in title]


def build_learned(rows):
    """rows: iterable of (figure_id, name_original, fields). Returns a JSON-safe memory."""
    support = defaultdict(set)
    labels = defaultdict(set)
    examples = []
    for figure_id, name_original, fields in rows:
        facts = observations(name_original, fields)
        for kind, original, ko, work in facts:
            key = (kind, original)
            labels[key].add((ko, work))
            support[(kind, original, ko, work)].add(figure_id)
        if facts and fields.get('franchise_ko'):
            examples.append({'figure_id': figure_id, 'name_original': name_original,
                             'franchise_ko': fields.get('franchise_ko'),
                             'characters_ko': [c['ko'] for c in fields.get('characters') or [] if isinstance(c, dict) and c.get('ko')],
                             'figure_form': fields.get('figure_form')})
    aliases = []
    for (kind, original), values in labels.items():
        if kind == 'franchise':
            kos = {ko for ko, _ in values}
            if len(kos) != 1:
                continue
            ko = next(iter(kos))
            count = len(set().union(*(support[(kind, original, ko, w)] for _, w in values)))
            work = None
        else:
            if len(values) != 1:
                continue
            ko, work = next(iter(values))
            count = len(support[(kind, original, ko, work)])
        if count >= MIN_SUPPORT:
            aliases.append({'kind': kind, 'original': original, 'ko': ko, 'work': work, 'support': count})
    aliases.sort(key=lambda a: (a['kind'], a['original']))
    examples.sort(key=lambda e: e['figure_id'])
    return {'version': 'learned-aliases-v1', 'min_support': MIN_SUPPORT, 'aliases': aliases, 'examples': examples}


def learned_candidates(source, learned, work_ko=None, work_original=None):
    """Return {'franchise': item|None, 'characters': [items]} grounded in literal source text."""
    result = {'franchise': None, 'characters': []}
    if not learned:
        return result
    fields = [('name_original', source.get('name_original') or ''), ('franchise', source.get('franchise') or '')]
    aliases = learned.get('aliases', [])
    works = [a for a in aliases if a['kind'] == 'franchise']
    hits = []
    for alias in sorted(works, key=lambda a: -len(a['original'])):
        if not usable_alias(alias['original']):
            continue
        field = next((name for name, value in fields if literal_in(alias['original'], value)), None)
        if field:
            hits.append((alias, field))
    labels = {a['ko'] for a, _ in hits}
    if len(labels) == 1:
        alias, field = hits[0]
        result['franchise'] = {'original': alias['original'], 'ko': alias['ko'], 'evidence_field': field,
                               'evidence': alias['original'], 'confidence': 0.95, 'method': 'learned_verified_alias'}
        work_ko = work_ko or alias['ko']
    # A character name inside a work title (葬送のフリーレン) is not a character mention.
    title = source.get('name_original') or ''
    spans = [a['original'] for a in works] + ([work_original] if work_original else [])
    for span in sorted(set(spans), key=len, reverse=True):
        title = title.replace(span, ' ')
    found = []
    for alias in sorted((a for a in aliases if a['kind'] == 'character'), key=lambda a: -len(a['original'])):
        if not usable_alias(alias['original']) or not literal_in(alias['original'], title):
            continue
        if alias.get('work') and work_ko and _norm(alias['work']) != _norm(work_ko):
            continue
        if any(alias['original'] in f['original'] for f in found):
            continue  # a longer alias already covers this span
        found.append({'original': alias['original'], 'ko': alias['ko'], 'evidence_field': 'name_original',
                      'evidence': alias['original'], 'confidence': 0.95, 'method': 'learned_verified_alias'})
    result['characters'] = found
    return result


def _grams(text, sizes=(2, 3)):
    text = _norm(text)
    return Counter(text[i:i + n] for n in sizes for i in range(max(0, len(text) - n + 1)))


class NgramIndex:
    """Small, dependency-free TF-IDF cosine index over original titles."""

    def __init__(self, examples):
        self.examples = list(examples)
        self.vectors = [_grams(e['name_original']) for e in self.examples]
        df = Counter(g for v in self.vectors for g in v)
        n = max(1, len(self.vectors))
        self.idf = {g: math.log((1 + n) / (1 + c)) + 1 for g, c in df.items()}
        self.weighted = [self._weight(v) for v in self.vectors]

    def _weight(self, vector):
        w = {g: c * self.idf.get(g, 0.0) for g, c in vector.items() if g in self.idf}
        norm = math.sqrt(sum(x * x for x in w.values())) or 1.0
        return {g: x / norm for g, x in w.items()}

    def similar(self, title, k=3, min_score=0.25, exclude_title=True):
        query = self._weight(_grams(title))
        scored = []
        for example, vector in zip(self.examples, self.weighted):
            if exclude_title and example['name_original'] == title:
                continue
            score = sum(x * vector.get(g, 0.0) for g, x in query.items())
            if score >= min_score:
                scored.append((score, example))
        scored.sort(key=lambda s: (-s[0], s[1]['figure_id']))
        return [{**e, 'similarity': round(s, 3)} for s, e in scored[:k]]

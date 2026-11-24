"""Pure evidence, title and entity validation. No SQL or model calls."""
import hashlib
import html
import json
from pathlib import Path
import re
import unicodedata
from app.services.semantic_policy import FIELDS, finalize, publication_status


VERSION = 'ja-ko-semantics-v5-fields'
JAPANESE_TEXT_PATTERN = r'[\u3041-\u3096\u309d-\u309f\u30a1-\u30fa\u30fd-\u30ff\u31f0-\u31ff\u3400-\u4dbf\u4e00-\u9fff々]'


FORMS = {
    'noodle_stopper': '누들 스토퍼', 'scale_figure': '스케일 피규어',
    'action_figure': '액션 피규어', 'chibi_figure': '데포르메 피규어',
    'nendoroid': '넨도로이드', 'soft_vinyl': '소프비',
    'plush': '봉제인형', 'acrylic_stand': '아크릴 스탠드',
    'mini_figure': '미니 피규어',
    'prize_figure': '프라이즈 피규어', 'static_figure': '고정형 피규어',
    'model_kit': '프라모델·조립 모형', 'figure_parts': '피규어 부품·소품',
    'rubber_mascot': '러버 마스코트', 'keychain': '키링·스트랩',
    'lottery_goods': '캐릭터 복권 상품',
    'non_scale_figure': '논스케일 피규어', 'completed_figure': '완성품 피규어',
}


FORM_ALIASES = {
    'noodle_stopper': ['ぬーどるストッパー', 'ヌードルストッパー', 'Noodle Stopper', '누들스토퍼', '누들 스토퍼'],
    'nendoroid': ['ねんどろいど', 'Nendoroid', '넨도로이드'],
    'action_figure': ['アクションフィギュア', '可動フィギュア', 'action figure', '액션 피규어'],
    'chibi_figure': ['デフォルメフィギュア', 'ちびフィギュア', 'Look Up', 'るかっぷ', '데포르메 피규어'],
    'soft_vinyl': ['ソフビ', 'ソフトビニール'],
    'plush': ['ぬいぐるみ', 'plush'], 'acrylic_stand': ['アクリルスタンド', 'アクスタ'],
    'mini_figure': ['ミニフィギュア', 'ミニサイズ', '[mini]'],
    'lottery_goods': ['フリューくじ'],
    'non_scale_figure': ['ノンスケールフィギュア'],
    'completed_figure': ['彩色済み完成品フィギュア', '塗装済み完成品フィギュア'],
}


def normalize(s):
    return re.sub(r'\s+', '', unicodedata.normalize('NFKC', s or '')).casefold()


def same_subject(first, second):
    if normalize(first) == normalize(second):
        return True
    rows = json.loads(Path(__file__).with_name('local_semantic_tuning_lexicon.json').read_text(encoding='utf-8'))['characters']
    return any(normalize(first) in {normalize(a) for a in row['aliases']} and
               normalize(second) in {normalize(a) for a in row['aliases']} for row in rows)


def title_subject(subject, title):
    if subject in title:
        return True
    rows = json.loads(Path(__file__).with_name('local_semantic_tuning_lexicon.json').read_text(encoding='utf-8'))['characters']
    return any(normalize(subject) in {normalize(a) for a in row['aliases']} and
               any(a in title for a in row['aliases']) for row in rows)


def add_documents(source, documents):
    for i in range(3):
        d = documents[i] if i < len(documents) else None
        get = lambda key: (d.get(key) if isinstance(d, dict) else getattr(d, key)) if d else None
        source['document_' + str(i)] = (get('body') or '')[:6000] if d else None
        for key in ('id', 'url', 'title', 'source_type'):
            source[f'_document_{i}_{key}'] = get(key)
    source['_entity_candidates'] = context_candidates(source)
    return source


def context_candidates(source):
    found = []
    for field in ('document_0', 'document_1', 'document_2'):
        body = source.get(field)
        if not isinstance(body, str):
            continue
        # Introductory work/subject relationship, before footnotes and cross-sell recommendations.
        intro = body.split('※', 1)[0].split('\n', 1)[0][:1200]
        # Overlapping introductions: 『るかっぷ』より『WORK』の「SUBJECT」.
        # The product line must not turn WORK into a character.
        pattern = r'(?=([『「]([^』」\n]{1,100})[』」](?:より|から|の)([^\n。！]{1,300})))'
        for match in re.finditer(pattern, intro):
            proof, work, clause = match.groups()
            if normalize(work) in {normalize(source.get('manufacturer')), normalize(source.get('product_line')), 'tenitol', 'fnex', 'るかっぷ'}:
                continue
            subjects = re.findall(r'[「『]([^」』]{1,100})[」』]', clause)
            subjects = [s for s in subjects if title_subject(s, source['name_original']) or s in (source.get('character') or '')]
            if not subjects:
                continue
            found.append({'kind': 'franchise', 'original': work, 'evidence_field': field, 'evidence': proof})
            found.extend({'kind': 'character', 'original': s, 'evidence_field': field, 'evidence': proof} for s in subjects)
    return found


def rules_hash():
    return hashlib.sha256((VERSION + json.dumps(glossary(), ensure_ascii=False, sort_keys=True)).encode()).hexdigest()


def source_hash(source):
    return hashlib.sha256((VERSION + json.dumps(source, ensure_ascii=False, sort_keys=True)
                           + json.dumps(glossary(), ensure_ascii=False, sort_keys=True)).encode()).hexdigest()


_ALLOWED_SCRIPTS = ('HANGUL', 'LATIN', 'FULLWIDTH LATIN', 'GREEK', 'COMBINING', 'DIGIT', 'FULLWIDTH DIGIT',
                    'SUPERSCRIPT', 'SUBSCRIPT', 'ROMAN NUMERAL', 'SMALL ROMAN NUMERAL', 'CIRCLED',
                    # used as a dash between title parts (Figureー初音ミクー)
                    'KATAKANA-HIRAGANA PROLONGED', 'HALFWIDTH KATAKANA-HIRAGANA PROLONGED')


def foreign_letters(value):
    """Letters or marks from scripts a Korean title never needs (Thai in model output, Arabic, ...)."""
    for c in value:
        if unicodedata.category(c)[0] in 'LM' and not unicodedata.name(c, '').startswith(_ALLOWED_SCRIPTS):
            if not re.match(JAPANESE_TEXT_PATTERN, c):
                return True
    return False


def korean(value):
    return (isinstance(value, str) and 0 < len(value.strip()) <= 1500 and bool(re.search('[가-힣]', value))
            and not re.search(JAPANESE_TEXT_PATTERN,value) and not re.search('[\u0400-\u052f]',value)
            and not foreign_letters(value))


def evidence(item, source, allowed):
    if not isinstance(item, dict) or item.get('evidence_field') not in allowed:
        return False
    phrase = item.get('evidence')
    base = source.get(item['evidence_field'])
    confidence = item.get('confidence')
    return (isinstance(phrase, str) and bool(phrase.strip()) and isinstance(base, str)
            and phrase in base and isinstance(confidence, (int, float)) and not isinstance(confidence, bool)
            and 0.85 <= confidence <= 1)


def glossary():
    p = Path(__file__).with_name('product_semantics_glossary.json')
    return json.loads(p.read_text(encoding='utf-8'))


def canonical(original, translated, entries):
    for row in entries:
        if normalize(original) in {normalize(x) for x in row['aliases']}:
            return row['ko']
    return translated.strip()


def classification_status(fields, issues):
    return publication_status(fields, issues)


def dictionary_entities(source, g):
    """Use explicit title terms and curated links, never a model's unsupported world knowledge."""
    title = source.get('name_original') or ''
    # A character whose name is embedded ONLY in a franchise title is not a character mention.
    stripped = title
    for entry in g['characters']:
        for alias in entry['aliases']:
            stripped = re.sub(re.escape(alias) + r'\s*シリーズ', ' ', stripped, flags=re.IGNORECASE)
    for entry in g['franchises']:
        for alias in sorted(entry['aliases'], key=len, reverse=True):
            stripped = re.sub(re.escape(alias) + r'\s*シリーズ', ' ', stripped, flags=re.IGNORECASE)
            stripped = re.sub(r'(?<!\w)' + re.escape(alias) + r'(?!\w)', ' ', stripped, flags=re.IGNORECASE)
    found = []
    for entry in g['characters']:
        for field, value in [('name_original', stripped), ('character', source.get('character') or '')]:
            match = next((re.search(re.escape(alias), value, re.IGNORECASE) for alias in sorted(entry['aliases'], key=len, reverse=True)
                          if re.search(re.escape(alias), value, re.IGNORECASE)), None)
            if match:
                found.append((entry, {'original': match.group(), 'ko': entry['ko'], 'evidence_field': field,
                                      'evidence': match.group(), 'method': 'dictionary'}))
                break
    # Prefer a full-name alias over a contained shorter alias (うちはイタチ vs イタチ).
    return [(entry, item) for entry, item in found if not any(
        item['original'] != other['original'] and item['original'] in other['original']
        for _, other in found)]


def validate_result(source, result):
    issues = []
    field_issues = {key: [] for key in FIELDS}

    def reject(code, field):
        issues.append(code)
        field_issues[field].append(code)

    if not isinstance(result, dict) or set(result) != {'name_ko', 'franchise', 'characters', 'figure_form'}:
        return {}, ['INVALID_RESULT_FIELDS']
    title = result.get('name_ko')
    if not korean(title):
        reject('KOREAN_TITLE_REQUIRED_OR_JAPANESE_REMAINS', 'name_ko')
    elif len(title) > max(200, len(source['name_original']) * 6):
        reject('TITLE_TOO_LONG', 'name_ko')
    else:
        def numbers(s):
            s = unicodedata.normalize('NFKC', html.unescape(s))
            digits = dict(zip('〇零一二三四五六七八九', (0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9)))
            def ordinal(match):
                total, current = 0, 0
                for char in match[1]:
                    if char in digits:
                        current = digits[char]
                    else:
                        total += (current or 1) * {'十': 10, '百': 100, '千': 1000}[char]
                        current = 0
                return '第' + str(total + current)
            s = re.sub(r'第([〇零一二三四五六七八九十百千]+)(?=[弾段期章話巻回版形])', ordinal, s)
            return set(re.findall(r'\d+(?:[.,]\d+)*', s))
        def scales(s):
            return set(re.findall(r'\d+/\d+', re.sub(r'\s+', '', unicodedata.normalize('NFKC', s))))
        if numbers(source['name_original']) != numbers(title) or scales(source['name_original']) != scales(title):
            reject('TITLE_NUMERIC_FACT_CHANGED', 'name_ko')
        # NFKC turns Ⅴ into V, so the decimal guard alone cannot detect a lost season.
        normalized_title = unicodedata.normalize('NFKC', title)
        if any(unicodedata.normalize('NFKC', c) not in normalized_title
               for c in re.findall(r'[Ⅰ-Ⅻⅰ-ⅻ]', source['name_original'])):
            reject('TITLE_ROMAN_NUMERAL_CHANGED', 'name_ko')
        # Protect explicit Latin product/model codes; avoid treating ordinary brand words as codes.
        codes = re.findall(r'\b[A-Za-z]+[A-Za-z0-9-]*\d[A-Za-z0-9-]*\b', source['name_original'])
        if any(normalize(c) not in normalize(title) for c in codes):
            reject('TITLE_PRODUCT_CODE_CHANGED', 'name_ko')
    g = glossary()
    fields = {'name_ko': title.strip() if isinstance(title, str) else None,
              'franchise_ko': None, 'character_ko': None, 'characters': [],
              'figure_form': None, 'figure_form_ko': None, 'evidence': {}}
    franchise = result.get('franchise')

    def entity(item, kind):
        field = 'franchise_ko' if kind == 'franchises' else 'character_ko'
        if (not evidence(item, source, {'name_original', 'franchise', 'character', 'document_0', 'document_1', 'document_2'})
                or not isinstance(item.get('original'), str) or not item['original'].strip()
                or item['original'] not in item['evidence'] or not korean(item.get('ko'))):
            reject('UNGROUNDED_' + kind.upper(), field)
            return None
        if item['evidence_field'].startswith('document_'):
            if item['evidence'] not in source[item['evidence_field']].split('※', 1)[0]:
                reject('RELATED_PRODUCT_EVIDENCE_REJECTED', field)
                return None
            candidates = context_candidates(source)
            if kind == 'characters':
                subjects = [c['original'] for c in candidates if c['kind'] == 'character']
                if not title_subject(item['original'], source['name_original']) and item['original'] not in subjects:
                    reject('RELATED_PRODUCT_CHARACTER_REJECTED', field)
                    return None
            elif kind == 'franchises' and not any(c['kind'] == 'franchise' and c['original'] == item['original'] for c in candidates):
                reject('DOCUMENT_FRANCHISE_RELATION_NOT_CONFIRMED', field)
                return None
        checked = {'original': item['original'], 'ko': canonical(item['original'], item['ko'], g[kind]),
                   'evidence_field': item['evidence_field'], 'evidence': item['evidence']}
        if item['evidence_field'].startswith('document_'):
            checked['source_url'] = source.get('_' + item['evidence_field'] + '_url')
        return checked

    if franchise is not None:
        item = entity(franchise, 'franchises')
        if item:
            fields['franchise_ko'] = item['ko']
            fields['evidence']['franchise'] = item
    characters = result.get('characters')
    if not isinstance(characters, list) or len(characters) > 20:
        reject('INVALID_CHARACTERS', 'character_ko')
    else:
        for c in characters:
            item = entity(c, 'characters')
            if item and item['ko'] not in [x['ko'] for x in fields['characters']]:
                fields['characters'].append(item)
        fields['character_ko'] = ' · '.join(x['ko'] for x in fields['characters']) or None
    form = result.get('figure_form')
    if form is not None:
        if not evidence(form, source, {'name_original', 'product_line', 'scale', 'document_0', 'document_1', 'document_2'}) or not isinstance(form.get('code'), str) or form.get('code') not in FORMS:
            reject('UNGROUNDED_FIGURE_FORM', 'figure_form')
        else:
            code = form['code']
            phrase = form['evidence']
            if form['evidence_field'].startswith('document_') and phrase not in source[form['evidence_field']].split('※', 1)[0]:
                reject('RELATED_PRODUCT_FORM_REJECTED', 'figure_form')
                phrase = ''
            aliases = FORM_ALIASES.get(code, [])
            grounded = any(normalize(a) in normalize(phrase) for a in aliases)
            if code == 'scale_figure':
                grounded = bool(re.search(r'\d+\s*/\s*\d+', unicodedata.normalize('NFKC', phrase)))
            if not grounded:
                reject('FORM_KEYWORD_NOT_SUPPORTED', 'figure_form')
            else:
                fields['figure_form'], fields['figure_form_ko'] = code, FORMS[code]
                fields['evidence']['figure_form'] = form
    # Deterministic form extraction can fill an unknown model form without guessing.
    if fields['figure_form'] is None and not any('FORM' in x for x in issues):
        from app.services.local_semantic_grounding import explicit_form
        determined = explicit_form(source)
        if determined:
            code = determined['code']
            fields['figure_form'], fields['figure_form_ko'] = code, FORMS[code]
            fields['evidence']['figure_form'] = {**determined, 'method': 'dictionary'}
    # Recover omissions from explicit, curated dictionary terms without another API request.
    found = dictionary_entities(source, g)
    for entry, item in found:
        if not any(normalize(c['original']) == normalize(item['original']) for c in fields['characters']):
            fields['characters'].append(item)
        # Correct known model transliteration variants only when the Japanese alias matched this item.
        if fields['name_ko']:
            for bad in entry.get('incorrect_ko', []):
                fields['name_ko'] = re.sub(r'(?<![가-힣])' + re.escape(bad) + r'(?![가-힣])', entry['ko'], fields['name_ko'])
    fields['character_ko'] = ' · '.join(dict.fromkeys(x['ko'] for x in fields['characters'])) or None
    relationships = {entry['franchise']['ko']: entry['franchise'] for entry, item in found if entry.get('franchise')}
    if not fields['franchise_ko'] and len(relationships) == 1:
        relationship = next(iter(relationships.values()))
        fields['franchise_ko'] = relationship['ko']
        fields['evidence']['franchise'] = {'method': 'curated_character_relationship',
            'reference_urls': relationship['reference_urls'], 'character_evidence': [x for _, x in found]}
    elif len(relationships) > 1:
        reject('CONFLICTING_DICTIONARY_FRANCHISES', 'franchise_ko')
    elif fields['franchise_ko'] and relationships and fields['franchise_ko'] not in relationships:
        reject('FRANCHISE_CONFLICTS_WITH_CURATED_CHARACTER', 'franchise_ko')
    # Fill known work translations from an explicit INTRODUCTION relationship, not from character familiarity.
    candidates = context_candidates(source)
    work_candidates = {c['original']: c for c in candidates if c['kind'] == 'franchise'}
    if len(work_candidates) == 1:
        original, proof = next(iter(work_candidates.items()))
        match = next((entry for entry in g['franchises'] if normalize(original) in {normalize(a) for a in entry['aliases']}), None)
        if match:
            if fields['franchise_ko'] not in (None, match['ko']):
                reject('DOCUMENT_FRANCHISE_CONFLICT', 'franchise_ko')
            else:
                fields['franchise_ko'] = match['ko']
                fields['evidence']['franchise'] = {**proof, 'method': 'intro_relationship_dictionary',
                    'source_url': source.get('_' + proof['evidence_field'] + '_url')}
    expected = {c['original'] for c in candidates if c['kind'] == 'character'}
    omitted = {original for original in expected if not any(same_subject(original, c['original']) for c in fields['characters'])}
    if omitted:
        reject('EXPLICIT_MAIN_CHARACTER_OMITTED:' + ','.join(sorted(omitted)), 'character_ko')
    if work_candidates and not fields['franchise_ko']:
        reject('EXPLICIT_DOCUMENT_FRANCHISE_OMITTED', 'franchise_ko')
    return finalize(fields, field_issues), issues

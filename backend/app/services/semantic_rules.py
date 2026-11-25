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


# Variation selectors (e.g. an IVS after a kanji in 鬼舞辻無惨) only pick a glyph; they never change the name.
VARIATION_SELECTORS = re.compile('[\ufe00-\ufe0f\U000e0100-\U000e01ef]')


def normalize(s):
    return re.sub(r'\s+', '', unicodedata.normalize('NFKC', VARIATION_SELECTORS.sub('', s or ''))).casefold()


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


def version_name(name, title):
    """初音ミク ヴァンパイア Ver.: a name right before a bare Ver. is the version (a song, an outfit),
    not a character; Ver.A / ver.2 only number variants of a named character."""
    return re.search(re.escape(name) + r'\s*[-－ー～〜]?\s*ver(?:sion)?\b\.?(?![ \.]*[A-Za-z0-9])', title or '', re.I) is not None


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
            if normalize(work) in {normalize(source.get('manufacturer')), normalize(source.get('product_line')), 'tenitol', 'fnex',
                                   normalize('F:NEX'), 'るかっぷ'}:
                continue
            subjects = re.findall(r'[「『]([^」』]{1,100})[」』]', clause)
            subjects = [s for s in subjects if title_subject(s, source['name_original']) or s in (source.get('character') or '')]
            # 「チアリーディング」初音ミク … 初音ミク チアリーディングVer.: the quoted theme is the version, not a character.
            subjects = [s for s in subjects if not version_name(s, source['name_original'])]
            # 「吉徳×F:NEX カンナ -日本人形- 1/4スケールフィギュア」 quotes the whole product name, not a character.
            subjects = [s for s in subjects if normalize(s) != normalize(source['name_original'])]
            # Brands and lines quoted as subjects (「F:NEX」) are not characters either.
            brands = {normalize(source.get('manufacturer')), normalize(source.get('product_line')), 'tenitol', 'fnex', normalize('F:NEX')}
            subjects = [s for s in subjects if normalize(s) not in brands]
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


def latin_kept(source, title):
    """A Latin-only product name (KAITO, C.C., D-STYLE DEATH SAURER) has nothing to translate;
    keeping it unchanged is the correct title. Only the exact source text qualifies."""
    original = (source or {}).get('name_original') or ''
    return (isinstance(title, str) and title.strip() == original.strip() and bool(re.search('[A-Za-z]', original))
            and re.fullmatch(r'[\x20-\x7e -ÿ -⁯Ⅰ-ⅿ☀-⛿！-～　]+', original.strip()) is not None)


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
    if not (korean(title) or latin_kept(source, title)):
        reject('KOREAN_TITLE_REQUIRED_OR_JAPANESE_REMAINS', 'name_ko')
    elif len(title) > max(200, len(source['name_original']) * 6):
        reject('TITLE_TOO_LONG', 'name_ko')
    else:
        digits = dict(zip('〇零一二三四五六七八九', (0, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9)))
        def kanji_value(run):
            total, current = 0, 0
            for char in run:
                if char in digits:
                    current = digits[char]
                else:
                    total += (current or 1) * {'十': 10, '百': 100, '千': 1000}[char]
                    current = 0
            return total + current
        def plain(s):
            # NFKC turns ½ into 1⁄2 (fraction slash); compare it as 1/2.
            return unicodedata.normalize('NFKC', html.unescape(s)).replace('⁄', '/')
        def numbers(s):
            s = re.sub(r'第([〇零一二三四五六七八九十百千]+)(?=[弾段期章話巻回版形])',
                       lambda m: '第' + str(kanji_value(m[1])), plain(s))
            return set(re.findall(r'\d+(?:[.,]\d+)*', s))
        def scales(s):
            return set(re.findall(r'\d+/\d+', re.sub(r'\s+', '', plain(s))))
        # A kanji numeral may be written as a digit (五等分 -> 5등분), and an ordinal may be written
        # in Korean words (第二弾 -> 두 번째); neither may add or drop a number otherwise.
        native = {1: '첫', 2: '두', 3: '세', 4: '네', 5: '다섯', 6: '여섯', 7: '일곱', 8: '여덟', 9: '아홉', 10: '열'}
        source_numbers, title_numbers = numbers(source['name_original']), numbers(title)
        kanji_numbers = {str(kanji_value(r)) for r in re.findall(r'[〇零一二三四五六七八九十百千]+', plain(source['name_original']))}
        ordinals = {str(kanji_value(r)) for r in re.findall(r'第([〇零一二三四五六七八九十百千]+)', plain(source['name_original']))}
        dropped = {n for n in source_numbers - title_numbers
                   if not (n in ordinals and n.isdigit() and int(n) in native
                           and re.search(native[int(n)] + r'\s*번째', title))}
        if dropped or not title_numbers - source_numbers <= kanji_numbers \
                or scales(source['name_original']) != scales(title):
            reject('TITLE_NUMERIC_FACT_CHANGED', 'name_ko')
        # NFKC turns Ⅴ into V, so the decimal guard alone cannot detect a lost season.
        normalized_title = unicodedata.normalize('NFKC', title)
        if any(unicodedata.normalize('NFKC', c) not in normalized_title
               for c in re.findall(r'[Ⅰ-Ⅻⅰ-ⅻ]', source['name_original'])):
            reject('TITLE_ROMAN_NUMERAL_CHANGED', 'name_ko')
        # Protect explicit Latin product/model codes; avoid treating ordinary brand words as codes.
        codes = re.findall(r'\b[A-Za-z]+[A-Za-z0-9-]*\d[A-Za-z0-9-]*\b', source['name_original'])
        def code_kept(code):
            # IRF2024ver. -> IRF2024 버전, C02-URANUS -> C02-우라노스: the digit-bearing part must survive.
            core = re.sub(r'(?i)ver$', '', code)
            parts = [p for p in core.split('-') if re.search(r'\d', p)]
            return normalize(code) in normalize(title) or all(normalize(p) in normalize(title) for p in parts)
        if not all(code_kept(c) for c in codes):
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
    # 『春夏秋冬代行者 春の舞』 quoted in the description is the work, not a character left out.
    work_names = {normalize(c['original']) for c in candidates if c['kind'] == 'franchise'}
    proof = (fields['evidence'].get('franchise') or {})
    work_names |= {normalize(x) for x in [proof.get('original'), source.get('franchise'),
                                           *(r.get('match') for r in proof.get('references') or [])] if x}
    work_names = {w for w in work_names if len(w) >= 3}
    omitted = {o for o in omitted if not any(normalize(o) in w or w in normalize(o) for w in work_names)}
    # 「ルピー：ウィンターショッパー」, 「小鳥遊ホシノ（臨戦）」: the named character plus its outfit or form.
    omitted = {o for o in omitted if not any(o.startswith(c['original']) and o[len(c['original']):len(c['original']) + 1] in '：:・･ -‐（(〈〔［[～~'
                                             for c in fields['characters'] if c.get('original'))}
    if omitted:
        reject('EXPLICIT_MAIN_CHARACTER_OMITTED:' + ','.join(sorted(omitted)), 'character_ko')
    if work_candidates and not fields['franchise_ko']:
        reject('EXPLICIT_DOCUMENT_FRANCHISE_OMITTED', 'franchise_ko')
    return assortment_without_character(source, finalize(fields, field_issues)), issues


# Boxes, blind assortments, sets and numbered lines hold several characters (or none in the title);
# for them the work is the classification and a missing character is not a gap.
ASSORTMENT = re.compile(r'(?i)(?<![a-z])box(?![a-z])|ボックス|박스|全\s*\d+\s*種|\d+\s*종|アソート|아소트|assort|コレクション|컬렉션|'
                        r'トレーディング|트레이딩|ブラインド|블라인드|ガチャ|가챠|(?<![a-z])set(?![a-z])|セット|세트|'
                        # VOL.n and "Collection Figure #2" number single figures; they are not boxes.
                        r'第\S{1,3}弾|\d+\s*個入|くじ|쿠지|'
                        # Blind-box lines and mascot assortments sold by the box.
                        r'バディコレ|マスコット|とびマス|ぬいっぽ|ニャンコ|ニャルト|にゃんこ|ニャン[！!]|ニャンダム|にゃん魂|CATS|'
                        r'さぷらいず|ぴたきゅーと|プチラマ|LOGBOX|MEGA ?CAT|カラころ|もぐもぐ|ちびコレ|'
                        # Unnamed rank-and-file figures (ジオン公国軍一般兵士01).
                        r'一般兵士|専用バイク|専用バギー')


def _title_is_only_the_work(title, fields):
    """ONE PIECE, 呪術廻戦【再販】, TVアニメ『ダンダダン』: the title names the work and nothing else."""
    evidence = (fields.get('evidence') or {}).get('franchise') or {}
    # Verified overrides keep the matched title text in their references instead of "original".
    names = {evidence.get('original') or '', fields.get('franchise_ko') or '',
             *(r.get('match') or '' for r in evidence.get('references') or [])} - {''}
    core = re.sub(r'【[^】]*】|\[[^\]]*\]|^(?:TV)?アニメ|^劇場版|^映画|[『』「」]', '', title).strip(' 　')
    return bool(core) and normalize(core) in {normalize(n) for n in names}
# "(B:무라타)" picks one figure of the line; that one names a character the dictionary should know.
SINGLE_PICK = re.compile(r'[(（]\s*[A-Z]\s*[:：.]')


# Works that are their own character: a Miku product with no other character named is a Miku figure.
WORK_IS_CHARACTER = {'하츠네 미쿠': '하츠네 미쿠', '하츠네 미쿠 GT 프로젝트': '하츠네 미쿠'}
OTHER_VOCALOIDS = re.compile(r'鏡音|巡音|KAITO|MEIKO|重音|カイト|메이코|카가미네|메구리네')


def _work_as_character(source, fields):
    ko = WORK_IS_CHARACTER.get(fields.get('franchise_ko'))
    title = (source or {}).get('name_original') or ''
    evidence = (fields.get('evidence') or {}).get('franchise') or {}
    field = evidence.get('evidence_field') or ('name_original' if '初音ミク' in title or '미쿠' in title else None)
    if not ko or fields.get('character_ko') or OTHER_VOCALOIDS.search(title):
        return False
    original = evidence.get('original') or next((r.get('match') for r in evidence.get('references') or [] if r.get('match')), None)
    fields['characters'] = [{'original': original or fields['franchise_ko'], 'ko': ko, 'evidence_field': field or 'franchise',
                             'evidence': evidence.get('evidence') or original or fields['franchise_ko'], 'method': 'work_is_character'}]
    fields['character_ko'] = ko
    return True


def assortment_without_character(source, fields):
    title = (source or {}).get('name_original') or ''
    states = fields.get('field_status') or {}
    if fields.get('franchise_ko') and states.get('character_ko') == 'missing' and _work_as_character(source, fields):
        states['character_ko'] = 'ready'
        fields['missing_fields'] = [k for k in fields.get('missing_fields', []) if k != 'character_ko']
        classification = [states[k] for k in ('franchise_ko', 'character_ko', 'figure_form')]
        fields['classification_status'] = ('review' if 'review' in classification else
                                           'partial' if 'missing' in classification else 'ready')
        return fields
    if (fields.get('franchise_ko') and states.get('character_ko') == 'missing' and not fields.get('character_ko')
            and (ASSORTMENT.search(title) or _title_is_only_the_work(title, fields)) and not SINGLE_PICK.search(title)):
        states['character_ko'] = 'not_applicable'
        fields['missing_fields'] = [k for k in fields.get('missing_fields', []) if k != 'character_ko']
        classification = [states[k] for k in ('franchise_ko', 'character_ko', 'figure_form')]
        fields['classification_status'] = ('review' if 'review' in classification else
                                           'partial' if 'missing' in classification else 'ready')
    return fields

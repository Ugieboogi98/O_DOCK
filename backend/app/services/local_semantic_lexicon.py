"""Exact-source alias assistance; no inference of unstated work relationships."""
import copy
import hashlib
import html
import json
from pathlib import Path
import re
import unicodedata

# フィギュアー名前ー / フィギュア―名前― (noodle stoppers, prize lines): dashes around the character name.
BRACKETED_NAME = re.compile(r'(フィギュア)[ー―－](.+?)[ー―－](?=\s|$|[（(【\[])')


def load():
    data = json.loads(Path(__file__).with_name('local_semantic_aliases.json').read_text(encoding='utf-8'))
    from app.services.semantic_rules import glossary
    for kind, rows in glossary().items():
        if kind not in ('franchises', 'characters'):
            continue
        for row in rows:
            if not any(row['ko'] == other['ko'] and set(row['aliases']) == set(other['aliases']) for other in data[kind]):
                data[kind].append(row)
    return data


def fingerprint():
    return hashlib.sha256(Path(__file__).read_bytes() + Path(__file__).with_name('local_semantic_tuning_lexicon.json').read_bytes()
                          + Path(__file__).with_name('local_semantic_domain_aliases.json').read_bytes()
                          + Path(__file__).with_name('local_semantic_domain_extension.json').read_bytes()
                          + Path(__file__).with_name('local_semantic_title_terms.json').read_bytes()
                          + Path(__file__).with_name('local_semantic_subjects.py').read_bytes()
                          + Path(__file__).with_name('local_semantic_prompt.txt').read_bytes()
                          + Path(__file__).with_name('local_semantic_grounding.py').read_bytes()
                          + Path(__file__).with_name('semantic_rules.py').read_bytes()
                          + (Path(__file__).with_name('local_semantic_catalog_titles.json').read_bytes()
                             if Path(__file__).with_name('local_semantic_catalog_titles.json').exists() else b'')
                          + json.dumps(load(), ensure_ascii=False, sort_keys=True).encode()).hexdigest()


def tuning_lexicon():
    return json.loads(Path(__file__).with_name('local_semantic_tuning_lexicon.json').read_text(encoding='utf-8'))


def _loose(label):
    return re.sub(r'[\s.·・･]', '', label or '')


def title_hints(source, grounded, groups=None):
    """groups: the dictionary's domain groups, which add verified Wikidata characters to the curated files."""
    from app.services.reference_classifier import match, norm
    rows = hints(source)
    title = source.get('name_original') or ''
    data = tuning_lexicon()
    for row in data['characters']:
        if row.get('required_work_aliases') and not any(a in title for a in row['required_work_aliases']):
            continue
        for alias in sorted(row['aliases'], key=len, reverse=True):
            if alias in title:
                rows.append({'kind': 'characters', 'original': alias, 'ko': row['ko']})
                if not any(c['original'] == alias for c in grounded['characters']):
                    grounded['characters'].append({'original': alias, 'ko': row['ko'], 'evidence_field': 'name_original',
                                                  'evidence': alias, 'confidence': 1})
                break
    for kind, values in [('franchises', [grounded['franchise']]), ('characters', grounded['characters'])]:
        rows.extend({'kind': kind, 'original': row['original'], 'ko': row['ko']} for row in values if row)
    if groups is None:
        domains = json.loads(Path(__file__).with_name('local_semantic_domain_aliases.json').read_text(encoding='utf-8'))
        domains['groups'] += json.loads(Path(__file__).with_name('local_semantic_domain_extension.json').read_text(encoding='utf-8'))['groups']
    else:
        domains = {'groups': groups}
    context = ' '.join([title, source.get('franchise') or '', (grounded['franchise'] or {}).get('ko', '')])
    subject = title
    work = grounded['franchise']
    if work and work['original'] in title:
        singer = work['ko'] in ('하츠네 미쿠', '슈퍼 소니코')
        if not singer or work['original'] + 'シリーズ' in title:
            subject = subject.replace(work['original'], ' ', 1)
    # ぬーどるストッパーフィギュアーブランー: the long-vowel marks bracket the name, they do not lengthen it.
    subject = BRACKETED_NAME.sub(r'\1 \2 ', subject)
    korean_title = re.search('[가-힣]', title) is not None
    for group in domains['groups']:
        if group.get('provenance') == 'wikidata':
            # Wikidata characters only inside the work already confirmed for this product.
            if not (work and norm(group['work']) == norm(work.get('ko') or '')):
                continue
        elif not (any(norm(alias) in norm(context) for alias in group['aliases']) or group['work'] in context):
            continue
        self_title = group.get('title_is_character') and (not work or
            any(norm(a) == norm(work['original']) for a in group['aliases']))
        group_subject = BRACKETED_NAME.sub(r'\1 \2 ', title) if self_title else subject
        for aliases, ko in group['characters']:
            names = aliases.split('|') if isinstance(aliases, str) else list(aliases)
            if korean_title:
                # Korean retail-style titles (승리의 여신 NIKKE 아니스) name the character by its Korean label.
                names.append(ko)
            original = next((found for a in sorted(names, key=len, reverse=True)
                             if (found := match(a, group_subject))), None)
            if not original:
                continue
            if original == '初音ミク' and original + 'シリーズ' in title:
                continue
            if group.get('provenance') == 'wikidata' and any(
                    original in c['original'] or c['original'] in original or _loose(c['ko']) == _loose(ko)
                    for c in grounded['characters']):
                # Wikidata only fills a gap; it never relabels a name a curated source already read.
                continue
            if any(_loose(ko) in _loose(c['ko']) and c['original'] != original for c in grounded['characters']):
                continue  # 몽키 D 루피 and 몽키 D. 루피, or 호시노 next to 타카나시 호시노, are one character
            # The full name replaces a given name read earlier (타카나시 호시노 over 호시노).
            shorter = {c['original'] for c in grounded['characters'] if _loose(c['ko']) in _loose(ko)}
            grounded['characters'] = [c for c in grounded['characters'] if c['original'] not in shorter]
            rows = [r for r in rows if not (r['kind'] == 'characters' and r['original'] in shorter)]
            rows = [r for r in rows if not (r['kind'] == 'characters' and r['original'] == original)]
            rows.append({'kind': 'characters', 'original': original, 'ko': ko})
            grounded['characters'] = [c for c in grounded['characters'] if c['original'] != original]
            grounded['characters'].append({'original': original, 'ko': ko, 'evidence_field': 'name_original',
                                           'evidence': original, 'confidence': 1})
    return list({(r['kind'], r['original'], r['ko']): r for r in rows}.values())


def translation_input(source, rows):
    title = html.unescape(source.get('name_original') or '')
    terms = [(r['original'], r['ko']) for r in rows] + [tuple(r) for r in tuning_lexicon()['title_terms']]
    terms += [tuple(r) for r in json.loads(Path(__file__).with_name('local_semantic_title_terms.json').read_text(encoding='utf-8'))]
    mapping = dict(terms)
    mapping.update((r['original'], r['ko']) for r in rows)
    # Collectors normalize full-width punctuation and Roman numerals with NFKC.
    # Retain both spellings so a long work title wins over its shorter alias.
    for original, ko in list(mapping.items()):
        mapping.setdefault(unicodedata.normalize('NFKC', original), ko)
    for original, ko in list(mapping.items()):
        # Encyclopedia disambiguators describe the article, not this product.
        ko = re.sub(r'\s*\((?:비디오 게임|애니메이션|만화)\)$', '', ko)
        if original.endswith('シリーズ') and not ko.endswith('시리즈'):
            ko += ' 시리즈'
        mapping[original] = ko
    terms = sorted(mapping.items(), key=lambda r: (-len(r[0]), r[0]))
    output, cursor = [], 0
    while cursor < len(title):
        hit = next(((a, ko) for a, ko in terms if title.startswith(a, cursor)), None)
        if hit:
            output.append(' ' + hit[1] + ' ')
            cursor += len(hit[0])
        else:
            output.append(title[cursor])
            cursor += 1
    composed = re.sub(r'\s+', ' ', ''.join(output)).strip()
    composed = re.sub(r'([【〈「『（(])\s+', r'\1', composed)
    return re.sub(r'\s+([】〉」』）)])', r'\1', composed)


def normalized(value):
    return re.sub(r'\s+', '', unicodedata.normalize('NFKC', value or '')).casefold()


def hints(source):
    title = source.get('name_original') or ''
    found = []
    data = load()
    for kind in ('franchises', 'characters'):
        for row in data[kind]:
            for alias in sorted(row['aliases'], key=len, reverse=True):
                pattern = r'(?<![A-Za-z])' + re.escape(alias) + r'(?![A-Za-z])' if alias.isascii() else re.escape(alias)
                match = re.search(pattern, title, re.IGNORECASE)
                if match:
                    found.append({'kind': kind, 'original': match.group(), 'ko': row['ko']})
                    break
    unique = list({(row['kind'], row['original'], row['ko']): row for row in found}.values())
    return [row for row in unique if not any(row['kind'] == other['kind'] and
            row['original'] != other['original'] and row['original'] in other['original'] for other in found)]


def normalize_result(source, result):
    result = copy.deepcopy(result)
    data = load()
    entities = [('franchises', result.get('franchise'))]
    characters = result.get('characters')
    if isinstance(characters, list):
        excluded = {normalized(term) for term in data['non_entity_terms']}
        characters = [item for item in characters if not isinstance(item, dict) or normalized(item.get('original')) not in excluded]
        result['characters'] = characters
        entities += [('characters', item) for item in characters]
    for kind, entity in entities:
        if not isinstance(entity, dict):
            continue
        original = entity.get('original')
        proof = entity.get('evidence')
        field = entity.get('evidence_field')
        if not isinstance(original, str) or not isinstance(proof, str):
            continue
        source_field = source.get(field) if isinstance(field, str) else None
        if not isinstance(source_field, str) or proof not in source_field or original not in proof:
            continue
        row = next((r for r in data[kind] if normalized(original) in {normalized(a) for a in r['aliases']}), None)
        if row is None:
            continue
        previous = entity.get('ko')
        entity['ko'] = row['ko']
        title = result.get('name_ko')
        # Repair only a named entity also explicit in this product title.
        if isinstance(title, str) and original in (source.get('name_original') or ''):
            title = title.replace(original, row['ko'])
            if row['ko'] not in title and isinstance(previous, str) and previous.strip() and previous != row['ko']:
                title = title.replace(previous, row['ko'])
            result['name_ko'] = title
    work = result.get('franchise')
    known_works = {normalized(a) for row in data['franchises'] for a in row['aliases']}
    if (isinstance(work, dict) and normalized(work.get('original')) not in known_works and
            normalized(work.get('original')) in {
            normalized(source.get('manufacturer')), normalized(source.get('product_line'))}):
        if isinstance(work.get('ko'), str) and isinstance(result.get('name_ko'), str):
            result['name_ko'] = result['name_ko'].replace(work['ko'], work.get('original') or '')
        result['franchise'] = None
    return result


def grounded_result(source, result):
    """Apply explicit source-bound candidates, preserving raw output in the cache."""
    from app.services.ollama_semantics import prepare_input
    prepared = prepare_input(source)
    result = normalize_result(source, result)
    grounded = prepared['_grounded_candidates']
    from app.services.local_semantic_subjects import recover
    recovered=recover(source,result,grounded)
    grounded['characters'].extend(recovered)
    if recovered:
        prepared['_canonical_aliases'].extend({'kind':'characters','original':c['original'],'ko':c['ko']} for c in recovered)
        prepared['_translation_input']=translation_input(source,prepared['_canonical_aliases'])
    result['franchise'] = copy.deepcopy(grounded['franchise'])
    # Unknown model spellings remain visible in model_result, never silently become searchable facts.
    # A missing field means review is required; it is not a verified negative label.
    result['characters'] = copy.deepcopy(grounded['characters'])
    # Local publication uses explicit type evidence; the model-only proposal remains in model_result.
    result['figure_form'] = copy.deepcopy(grounded['figure_form'])
    composed = prepared['_translation_input']
    # Only use the lexical composition when every Japanese term was covered.
    # Unknown Japanese still goes through the model and normal validation.
    protected = tuning_lexicon()['protected_brands'] + ['TV', source.get('product_line') or '']
    remainder = composed
    for row in prepared['_canonical_aliases']:
        remainder = remainder.replace(row['ko'], '')
    for brand in sorted(protected, key=len, reverse=True):
        remainder = remainder.replace(brand, '')
    unknown_latin = [token for token in re.findall(r'[A-Za-z][A-Za-z0-9-]*', remainder) if not re.search(r'\d', token)]
    japanese_input = bool(re.search('[ぁ-ゟ゠-ヿ一-龯]', source.get('name_original') or ''))
    from app.services.semantic_rules import korean
    if korean(source.get('name_original')):
        result['name_ko']=source['name_original']
    elif (not unknown_latin or japanese_input) and korean(composed):
        result['name_ko'] = composed
    else:
        # Dictionary coverage is an explicit automatic-publication boundary.
        # A plausible Korean-only string is not proof that an unfamiliar name was translated correctly.
        result['name_ko'] = None
    return result


def publication_review(raw, normalized_result):
    """Expose abstentions and deterministic corrections alongside the raw model result."""
    return {
        'policy': 'source_lexicon_and_explicit_subject_reading_v2',
        'automatic_title_covered': normalized_result.get('name_ko') is not None,
        'changed_fields': [key for key in ('name_ko', 'franchise', 'characters', 'figure_form')
                           if raw.get(key) != normalized_result.get(key)],
        'unknown_fields_require_review': [key for key in ('name_ko', 'franchise', 'characters', 'figure_form')
                                          if not normalized_result.get(key)],
        'note': 'Missing is review/unknown, never a verified not-applicable decision.'}

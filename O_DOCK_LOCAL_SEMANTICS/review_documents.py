"""Generate grouped editable Markdown; turn explicitly approved blocks into patches."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import sys
import unicodedata

ROOT = Path(__file__).resolve().parent
FIELDS = {'franchise_ko': '작품명', 'character_ko': '캐릭터·대상', 'figure_form': '피규어 종류'}


def normalize(value):
    return re.sub(r'\s+', '', unicodedata.normalize('NFKC', value or '')).casefold()


def candidate(row, field):
    source, fields = row['source'], row.get('fields', {})
    if field == 'franchise_ko' and source.get('franchise'):
        return source['franchise']
    if field == 'character_ko' and source.get('character'):
        return source['character']
    if field == 'figure_form' and source.get('product_line'):
        return source['product_line']
    title = source['name_original']
    for text in (fields.get('franchise_ko'), source.get('franchise'), source.get('product_line')):
        if text:
            title = title.replace(text, ' ', 1)
    title = re.sub(r'【[^】]*(?:再販|再生産|予約)[^】]*】', '', title)
    title = re.sub(r'(?:\d+\s*/\s*\d+\s*(?:スケール|스케일))|フィギュア|피규어', ' ', title)
    return re.sub(r'\s+', ' ', title).strip(' -_') or source['name_original']


def generate(catalog, output):
    if (output / 'manifest.json').exists():
        raise ValueError('REVIEW_DOCUMENT_EXISTS: use a new directory to preserve user edits')
    output.mkdir(parents=True, exist_ok=True)
    sys.path.insert(0, str(ROOT.parent / 'backend'))
    from app.services.semantic_rules import FORMS
    groups, counts = defaultdict(list), Counter()
    rows = catalog['records']
    for row in rows:
        states = row.get('fields', {}).get('field_status', {})
        for field in FIELDS:
            if states.get(field) in ('ready', 'not_applicable'):
                continue
            value = candidate(row, field)
            scope = row.get('fields', {}).get('franchise_ko') or row['source'].get('franchise') or ''
            # Do not combine ambiguous character names from different works.
            key = (field, normalize(scope) if field == 'character_ko' else '', normalize(value))
            groups[key].append(row)
            counts[field] += 1
    manifest = {'version': 1, 'groups': {}, 'counts': dict(counts), 'products': len(rows)}
    files = {field: ['# ' + label + ' 확인 문서', '',
        '값을 기입하고 해당 그룹의 모든 상품에 맞는지 확인한 뒤 `approved`를 `true`로 바꿉니다.',
        '확정할 수 없으면 null/false를 유지합니다. 해당 없음이 확실하면 value=null, not_applicable=true로 적습니다.',
        '캐릭터 value는 `["이름1", "이름2"]`, 작품명은 문자열, 종류는 아래 코드 문자열입니다.',
        '인터넷에 정보가 없다는 판정이 아니라 현재까지 확정하지 못한 항목입니다.', ''] for field, label in FIELDS.items()}
    files['figure_form'] += ['사용 가능한 코드:', '', *[f'- `{code}`: {name}' for code, name in FORMS.items()], '']
    for number, (key, members) in enumerate(sorted(groups.items(), key=lambda pair: (-len(pair[1]), pair[0])), 1):
        field = key[0]
        review_id = f'R{number:04d}'
        name = candidate(members[0], field)
        manifest['groups'][review_id] = {'field': field, 'candidate': name,
            'members': [{'figure_id': r['figure_id'], 'source_hash': r['source_hash']} for r in members]}
        lines = files[field]
        lines += [f'## {review_id} — {name.replace(chr(10), " ")} ({len(members)}개)', '',
                  '상품 ID: ' + ', '.join(str(r['figure_id']) for r in members), '']
        for row in members[:3]:
            label = row['source']['name_original'].replace('[', '(').replace(']', ')').replace('\n', ' ')
            lines.append(f"- [{label}]({row['source']['official_url']})")
        lines += ['', '```json', json.dumps({'review_id': review_id, 'approved': False,
            'value': None, 'not_applicable': False, 'note': ''}, ensure_ascii=False, indent=2), '```', '']
    names = {'franchise_ko': '01_WORKS.md', 'character_ko': '02_CHARACTERS.md', 'figure_form': '03_FIGURE_TYPES.md'}
    for field, lines in files.items():
        (output / names[field]).write_text('\n'.join(lines), encoding='utf-8')
    manifest['group_count'] = len(groups)
    (output / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    index = ['# 직접 확인할 미확정 분류', '',
        f'전체 {len(rows):,}개 상품에서 미확정 필드를 {len(groups):,}개 확인 그룹으로 묶었습니다.', '',
        '| 문서 | 미확정 상품·필드 건수 |', '|---|---:|']
    index += [f'| [{FIELDS[field]}]({names[field]}) | {counts[field]:,} |' for field in FIELDS]
    index += ['', '같은 그룹의 모든 상품에 해당하는 값만 승인하세요. 세트·복수 구성은 캐릭터를 배열로 적습니다.',
        '원문과 근거가 바뀐 상품에는 이전 문서의 결정을 강제로 적용하지 않습니다.', '',
        '작성 후 프로젝트 루트에서 검토용 패치를 만듭니다. 이 단계는 DB에 쓰지 않습니다.', '', '```powershell',
        f'python O_DOCK_LOCAL_SEMANTICS/review_documents.py import --directory "{output.as_posix()}" --output O_DOCK_LOCAL_SEMANTICS/data/manual_classifications.json',
        '```', '', '생성한 패치는 `scripts.apply_verified_classifications`의 preview 후 commit으로 반영할 수 있습니다.', '']
    (output / 'README.md').write_text('\n'.join(index), encoding='utf-8')
    return manifest


def import_documents(directory):
    manifest = json.loads((directory / 'manifest.json').read_text(encoding='utf-8'))
    records, seen = {}, set()
    for path in sorted(directory.glob('0*.md')):
        for block in re.findall(r'```json\s*\n(.*?)\n```', path.read_text(encoding='utf-8-sig'), re.DOTALL):
            decision = json.loads(block)
            if decision.get('approved') is not True:
                continue
            review_id = decision['review_id']
            if review_id in seen:
                raise ValueError('DUPLICATE_APPROVED_REVIEW_ID')
            seen.add(review_id)
            group = manifest['groups'][review_id]
            field, value = group['field'], decision.get('value')
            if value is None and decision.get('not_applicable') is not True:
                raise ValueError('APPROVED_VALUE_REQUIRED')
            if field == 'character_ko' and value is not None:
                if not isinstance(value, list) or any(not isinstance(v, str) or not v.strip() for v in value):
                    raise ValueError('CHARACTERS_REQUIRE_NAME_ARRAY')
                value = [{'original': None, 'ko': name.strip(), 'method': 'manual_verified'} for name in value]
            for member in group['members']:
                fid = member['figure_id']
                row = records.setdefault(fid, {'figure_id': fid, 'source_hash': member['source_hash'],
                    'approved': True, 'method': 'manual_verified', 'patch': {}, 'proofs': {},
                    'not_applicable_fields': [], 'review_id': [], 'note': ''})
                if row['source_hash'] != member['source_hash']:
                    raise ValueError('CONFLICTING_SOURCE_HASH')
                row['patch'][field] = value
                row['review_id'].append(review_id)
                row['note'] += decision.get('note', '') + '\n'
                if decision.get('not_applicable'):
                    row['not_applicable_fields'].append(field)
    return {'records': list(records.values()), 'approved_groups': len(seen)}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='mode', required=True)
    create = sub.add_parser('generate')
    create.add_argument('--catalog', type=Path, required=True)
    create.add_argument('--directory', type=Path, required=True)
    load = sub.add_parser('import')
    load.add_argument('--directory', type=Path, required=True)
    load.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    if args.mode == 'generate':
        manifest = generate(json.loads(args.catalog.read_text(encoding='utf-8')), args.directory)
        print(json.dumps({'groups': manifest['group_count'], 'counts': manifest['counts']}))
    else:
        payload = import_documents(args.directory)
        if args.output.exists():
            p.error('Use a new patch output filename')
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps({'approved_groups': payload['approved_groups'], 'products': len(payload['records'])}))


if __name__ == '__main__':
    main()

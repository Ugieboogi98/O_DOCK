"""Compile checked references and prepare evidence-backed catalog patches."""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / 'backend'))
from app.services.reference_classifier import norm, match, knowledge, resolve


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--directory', type=Path, required=True)
    p.add_argument('--catalog', type=Path, help='Fresh read-only DB export; defaults to directory/catalog.json')
    p.add_argument('--rules', type=Path, default=ROOT.parent / 'backend/app/services/classification_reference_rules.json')
    args = p.parse_args()
    directory = args.directory
    catalog = json.loads((args.catalog or directory / 'catalog.json').read_text(encoding='utf-8'))
    rules = json.loads(args.rules.read_text(encoding='utf-8'))
    extra_path = args.rules.with_name('classification_extra_reference_rules.json')
    if extra_path.exists():
        extra = json.loads(extra_path.read_text(encoding='utf-8'))
        for key in ('series', 'forms'):
            rules[key].extend(extra[key])
    anime_path = args.rules.with_name('classification_anime_reference_rules.json')
    if anime_path.exists():
        extra = json.loads(anime_path.read_text(encoding='utf-8'))
        for key in ('series', 'forms'):
            rules[key].extend(extra[key])
    checked = json.loads((directory / 'official_reference_checks.json').read_text(encoding='utf-8'))
    furyu_rules = args.rules.with_name('classification_furyu_reference_rules.json')
    if furyu_rules.exists():
        extra = json.loads(furyu_rules.read_text(encoding='utf-8'))
        for key in ('series', 'forms'):
            rules[key].extend(extra[key])
        checked.update(json.loads(args.rules.with_name('classification_furyu_reference_checks.json').read_text(encoding='utf-8')))
    wiki = json.loads((directory / 'wiki_entities.json').read_text(encoding='utf-8'))
    ko_path = directory / 'wiki_ko_entities.json'
    if ko_path.exists():
        wiki['entries'].update(json.loads(ko_path.read_text(encoding='utf-8'))['entries'])
    works, characters, forms = knowledge(rules, checked, wiki)
    (args.rules.parent / 'classification_knowledge.json').write_text(json.dumps({'works': works, 'characters': characters, 'forms': forms}, ensure_ascii=False, indent=2), encoding='utf-8')
    records = []
    for index, row in enumerate(catalog['records'], 1):
        records.append(resolve(row, works, characters, forms))
        if index % 1000 == 0:
            print(json.dumps({'processed': index}), flush=True)
    records = [row for row in records if row['patch']]
    counts = Counter(key for row in records for key in row['patch'])
    payload = {'records': records, 'summary': dict(counts),
        'knowledge': {'works': len(works), 'characters': len(characters), 'forms': len(forms)}}
    (directory / 'resolved.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'products': len(records), 'fields': dict(counts), 'knowledge': payload['knowledge']}, ensure_ascii=False))


if __name__ == '__main__':
    main()

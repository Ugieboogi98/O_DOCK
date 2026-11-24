"""Freeze a deterministic real-product evaluation sample without model calls."""
import json
import random
import argparse
import re
import hashlib
import unicodedata
from pathlib import Path
from collections import Counter
from sqlalchemy import select
from app.core.database import SessionLocal
from app.models.entities import Figure
from app.services.product_semantics import source_of

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--count', type=int, default=60)
parser.add_argument('--seed', type=int, default=20261111)
parser.add_argument('--output', type=Path, default=Path('/evaluation/holdout_sources_20261111.json'))
parser.add_argument('--exclude', type=Path)
parser.add_argument('--exclude-dataset', type=Path, action='append', default=[])
args = parser.parse_args()


def family(source):
    title = unicodedata.normalize('NFKC', source['name_original']).casefold()
    title = re.sub(r'【[^】]*(?:再販|再生産)[^】]*】|\([^)]*(?:再販|再生産)[^)]*\)', '', title)
    return re.sub(r'\W+', '', title)


excluded_sources = []
if args.exclude:
    excluded_sources.extend(r['source'] for r in json.loads(args.exclude.read_text(encoding='utf-8'))['records'])
for directory in args.exclude_dataset:
    for path in directory.glob('*.jsonl'):
        excluded_sources.extend(json.loads(line)['source'] for line in path.read_text(encoding='utf-8').splitlines() if line.strip())
excluded_families = {family(s) for s in excluded_sources}
excluded_urls = {s.get('official_url') for s in excluded_sources if s.get('official_url')}
excluded_bodies = {hashlib.sha256(s[f'document_{n}'].encode()).hexdigest() for s in excluded_sources for n in range(3)
                   if len(s.get(f'document_{n}') or '') > 150}
with SessionLocal() as db:
    figures = list(db.scalars(select(Figure).order_by(Figure.id)))
    random.Random(args.seed).shuffle(figures)
    counts, chosen = Counter(), []
    excluded = {37, 39, 51, 378, 1283, 115, 4806, 817, 233, 234}
    for f in figures:
        if f.id in excluded or counts[f.manufacturer_id] >= max(15, args.count // 4):
            continue
        if not re.search('[ぁ-ゟァ-ヺ一-龯]', f.name_original):
            continue
        source = source_of(f)
        if family(source) in excluded_families or source.get('official_url') in excluded_urls:
            continue
        if any(hashlib.sha256((source.get(f'document_{n}') or '').encode()).hexdigest() in excluded_bodies for n in range(3)):
            continue
        chosen.append({'figure_id': f.id, 'source': source})
        excluded_families.add(family(source))
        counts[f.manufacturer_id] += 1
        if len(chosen) >= args.count:
            break
    target = args.output
    if target.exists():
        raise RuntimeError('FROZEN_SAMPLE_ALREADY_EXISTS')
    target.write_text(json.dumps({'seed': args.seed, 'records': chosen}, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'cases': len(chosen), 'makers': dict(counts)}))

"""Task adaptation with scoped names, missing hints and title-only translation.

The former real holdout has now informed vocabulary curation and is development
data. A new, untouched real sample is required for a release decision.
"""
import hashlib
import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT.parent / 'backend'))
from app.services.ollama_semantics import prepare_input
from app.services.local_semantic_lexicon import translation_input
from dataset import components, family, write_jsonl


def ent(original, ko, field='name_original'):
    return {'original': original, 'ko': ko, 'evidence_field': field, 'evidence': original, 'confidence': 1}


def main():
    target = ROOT / 'data/domain_tuning_20261111_v2'
    if target.exists():
        raise RuntimeError('DATASET_ALREADY_EXISTS')
    services = ROOT.parent / 'backend/app/services'
    domains = json.loads((services / 'local_semantic_domain_aliases.json').read_text(encoding='utf-8'))['groups']
    rows = []
    for group in domains:
        work = group['aliases'][0]
        for aliases, ko in group['characters']:
            original = aliases.split('|')[0]
            for variant in range(2):
                name = (f'{work} {original} 1/7スケールフィギュア【再販】' if variant == 0
                        else f'TENITOL {original} クラシカルワンピースver.')
                source = {'name_original': name, 'manufacturer': 'Example', 'manufacturer_ko': '예시',
                          'product_line': 'TENITOL' if variant else None, 'franchise': work,
                          'character': None, 'scale': '1/7' if variant == 0 else None, 'type': 'figure',
                          'official_url': f'https://example.invalid/domain/{len(rows)}',
                          'document_0': None}
                prepared = prepare_input(source)
                work_ko = (prepared['_grounded_candidates']['franchise'] or {}).get('ko', group['work'])
                result = {'name_ko': (f'{work_ko} {ko} 1/7 스케일 피규어【재판】' if variant == 0
                                     else f'TENITOL {ko} 클래식 원피스 버전'),
                          'franchise': ent(work, work_ko, 'franchise'), 'characters': [ent(original, ko)],
                          'figure_form': {'code': 'scale_figure', 'evidence_field': 'scale',
                                          'evidence': '1/7', 'confidence': 1} if variant == 0 else None}
                # Half of the examples teach translation without a name answer in the hints.
                if len(rows) % 4 < 2:
                    prepared['_canonical_aliases'] = [r for r in prepared['_canonical_aliases'] if r['kind'] != 'characters']
                    prepared['_grounded_candidates']['characters'] = []
                    prepared['_translation_input'] = translation_input(source, prepared['_canonical_aliases'])
                rows.append({'figure_id': f'domain-{len(rows)}', 'source': prepared, 'result': result,
                             'reviewed': True, 'reviewer': 'Codex agent: scoped translation template audit',
                             'label_origin': 'agent_curated_synthetic_not_human_gold'})
    parts = {'train': [], 'validation': [], 'test': []}
    for group in components(rows):
        bucket = int(hashlib.sha256(min(family(r['source']) for r in group).encode()).hexdigest()[:8], 16) % 20
        part = 'test' if bucket == 0 else 'validation' if bucket == 1 else 'train'
        parts[part].extend(group)
    for part, values in parts.items():
        write_jsonl(target / (part + '.jsonl'), values)
    manifest = {'instruction': (services / 'local_semantic_prompt.txt').read_text(encoding='utf-8'),
                'counts': {k: len(v) for k, v in parts.items()}, 'human_reviewed_gold_count': 0,
                'note': 'Former real holdout used for development vocabulary; never present it as untouched release data.'}
    (target / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(manifest['counts']))


if __name__ == '__main__':
    main()

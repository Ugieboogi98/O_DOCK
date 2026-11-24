"""Read-only live local-model sample evaluation; reports are not DB patches."""
import argparse
import json
import time
from pathlib import Path
from datetime import datetime, timezone
from sqlalchemy import select
from app.core.config import get_settings
from app.core.database import SessionLocal
from app.models.entities import Figure
from app.services.product_semantics import source_of, source_hash, validate_result
from app.services.semantic_provider import Extractor
from app.services.reference_classifier import cached_record, norm
from scripts.product_semantics import atomic_report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--report', type=Path, required=True)
    args = parser.parse_args()
    if get_settings().semantic_provider != 'ollama':
        raise RuntimeError('LOCAL_PROVIDER_REQUIRED')
    ids = [37, 39, 51, 378, 1283, 115, 4806, 817]
    with SessionLocal() as db:
        figures = list(db.scalars(select(Figure).order_by(Figure.id)))
        # Add up to two real titles covered by new references, not old rules.
        root = Path(__file__).resolve().parents[1] / 'app/services'
        old = json.loads((root / 'classification_knowledge.json').read_text(encoding='utf-8'))
        known = {norm(a) for w in old['works'] for a in w['aliases']}
        supplement = json.loads((root / 'classification_wikipedia_anime.json').read_text(encoding='utf-8'))
        extra = [w for w in supplement['works'] if norm(w['ko']) not in known]
        for f in figures:
            if f.id not in ids and any(len(a) >= 4 and a in f.name_original for w in extra for a in w['aliases'][1:]):
                ids.append(f.id)
                if len(ids) == 10:
                    break
        sources = [(fid, source_of(db.get(Figure, fid))) for fid in ids]
    report = {'started_at': datetime.now(timezone.utc).isoformat(), 'mode': 'READ_ONLY_LIVE_LOCAL_MODEL',
              'db_written': False, 'paid_api_called': False, 'records': []}
    atomic_report(args.report, report)
    extractor = Extractor()
    # Separate empty cache guarantees these are new model calls for this evaluation.
    extractor.local.cache = args.report.parent / (args.report.stem + '_cache')
    for fid, source in sources:
        start = time.monotonic()
        record = {'figure_id': fid, 'source': source, 'source_hash': source_hash(source)}
        try:
            result = extractor(source)
            fields, issues = validate_result(source, result)
            reference = cached_record(source, source_hash(source), fid, fields)
            cache = extractor.local.cache / (extractor.metadata['cache_key'] + '.json')
            raw = json.loads(cache.read_text(encoding='utf-8'))
            record.update(model_result=raw['model_result'], normalized_result=result,
                          validated_fields=fields, issues=issues,
                          reference_patch=reference, provider_metadata=dict(extractor.metadata))
        except Exception as exc:
            record['error'] = getattr(exc, 'code', type(exc).__name__)
        record['seconds'] = round(time.monotonic() - start, 2)
        report['records'].append(record)
        atomic_report(args.report, report)
        print(json.dumps({'figure_id': fid, 'seconds': record['seconds'], 'error': record.get('error'),
                          'name_ko': record.get('validated_fields', {}).get('name_ko')}), flush=True)
    report['finished_at'] = datetime.now(timezone.utc).isoformat()
    atomic_report(args.report, report)


if __name__ == '__main__':
    main()

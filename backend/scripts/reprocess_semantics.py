"""Re-run existing partial/review profiles through the current split pipeline, resumably.

Fields that were already 'ready' for the same source are never downgraded (see
product_semantics.keep_ready_fields). Progress is stored in the report directory, so an
interrupted run continues where it stopped.

  python tools/run_split_semantics.py --reprocess --status partial --report-dir data/private/semantics/reprocess_20261124
"""
import argparse
import json
import time
from datetime import datetime, timezone
from pathlib import Path
from sqlalchemy import select
from app.core.database import SessionLocal
from app.core.config import get_settings
from app.models.semantics import ProductSemantics
from app.services.split_semantics import VERSION
from app.services.worker_lock import advisory_lock
from scripts.product_semantics import atomic_report
from scripts.split_semantics_worker import consume


def targets(statuses, stale_only=False):
    """stale_only keeps rows not yet on VERSION: the ones a previous run failed and left untouched."""
    q = select(ProductSemantics.figure_id).where(ProductSemantics.status.in_(statuses))
    if stale_only:
        q = q.where(ProductSemantics.model.notlike(f'{VERSION}%'))
    with SessionLocal() as db:
        return list(db.scalars(q.order_by(ProductSemantics.figure_id)))


def before_states(ids):
    with SessionLocal() as db:
        return {p.figure_id: p.status for p in db.scalars(select(ProductSemantics).where(ProductSemantics.figure_id.in_(ids)))}


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--status', nargs='+', default=['partial'], choices=['partial', 'review', 'ready'])
    p.add_argument('--batch', type=int, default=50)
    p.add_argument('--max', type=int, default=0, help='Stop after this many items (0 = all).')
    p.add_argument('--report-dir', type=Path, required=True)
    p.add_argument('--translation-model', default=get_settings().semantic_translation_model)
    p.add_argument('--classification-model', default=get_settings().semantic_classification_model)
    p.add_argument('--retry-failed', action='store_true',
                   help='Re-run only rows still on an older pipeline (failed earlier), even if marked done.')
    p.add_argument('--ids-file', type=Path, help='JSON list of figure ids to re-run, whatever their status.')
    a = p.parse_args()
    if not 1 <= a.batch <= 100:
        p.error('batch must be 1..100')
    root = a.report_dir
    root.mkdir(parents=True, exist_ok=True)
    state_path = root / ('retry_progress.json' if a.retry_failed else 'reprocess_progress.json')
    state = json.loads(state_path.read_text(encoding='utf-8')) if state_path.exists() else {}
    if state.get('pipeline') != VERSION:
        state = {'pipeline': VERSION, 'done': [], 'transitions': {}, 'failed': 0}
    with advisory_lock('split_semantics_worker'):
        done = set(state['done'])
        wanted = json.loads(a.ids_file.read_text(encoding='utf-8')) if a.ids_file else targets(a.status, a.retry_failed)
        todo = [fid for fid in sorted(set(wanted)) if fid not in done]
        if a.max:
            todo = todo[:a.max]
        state.update(statuses=a.status, total=len(done) + len(todo), started_at=state.get('started_at') or datetime.now(timezone.utc).isoformat())
        started = time.monotonic()
        for i in range(0, len(todo), a.batch):
            batch = todo[i:i + a.batch]
            before = before_states(batch)
            result = consume(len(batch), root, ids=batch, translation_model=a.translation_model,
                             classification_model=a.classification_model)
            after = before_states(batch)
            for fid in batch:
                key = f'{before.get(fid)}->{after.get(fid)}'
                state['transitions'][key] = state['transitions'].get(key, 0) + 1
            state['failed'] += result['failed']
            state['done'] += batch
            elapsed = time.monotonic() - started
            remaining = len(todo) - (i + len(batch))
            state.update(updated_at=datetime.now(timezone.utc).isoformat(),
                         eta_minutes=round(elapsed / (i + len(batch)) * remaining / 60, 1))
            atomic_report(state_path, state)
            print(json.dumps({'done': len(state['done']), 'total': state['total'], 'transitions': state['transitions'],
                              'failed': state['failed'], 'eta_minutes': state['eta_minutes']}, ensure_ascii=False), flush=True)
    state['finished_at'] = datetime.now(timezone.utc).isoformat()
    atomic_report(state_path, state)


if __name__ == '__main__':
    main()

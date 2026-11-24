"""One administrator action that runs every data step in order.

  1. catalog   – collect new products from the approved manufacturer sources
  2. semantics – translate and classify the queued products with the local Ollama models
  3. events    – collect official Instagram posts (Meta Graph API) and extract event dates
  4. verify    – summarise what this run added and what still needs review

Each step records its own state, so a failed or skipped step never hides the others. The
run is kept in collection_jobs (collector 'master_pipeline'), which the admin page polls.
Only one run can be active (PostgreSQL advisory lock across workers, a flag within one).
"""
from __future__ import annotations

import json
import logging
import threading
from datetime import datetime, timedelta, timezone

import httpx
from sqlalchemy import func, select

from app.core.config import get_settings
from app.core.database import SessionLocal
from app.models.entities import CollectionJob, Figure, now

LOG = logging.getLogger(__name__)
COLLECTOR = 'master_pipeline'
STEPS = ('catalog', 'semantics', 'events', 'verify')
LABELS = {'catalog': '신상품 수집', 'semantics': '번역·분류·검증', 'events': '행사 수집·날짜 정리', 'verify': '결과 점검'}
SEMANTIC_BATCH = 20
SEMANTIC_MAX_ITEMS = 300   # one click stays bounded; the rest waits for the next run or the worker
STALE_AFTER = timedelta(hours=6)
_gate = threading.Lock()
_running = False


def _stamp():
    return datetime.now(timezone.utc).isoformat()


def _load(job):
    try:
        detail = json.loads(job.error_summary or '{}')
    except (TypeError, ValueError):
        detail = {}
    return detail if isinstance(detail, dict) else {}


def _view(job):
    if job is None:
        return {'state': 'never', 'steps': [{'name': s, 'label': LABELS[s], 'state': 'pending'} for s in STEPS]}
    detail = _load(job)
    steps = detail.get('steps') or {}
    state = job.status
    started = job.started_at.replace(tzinfo=job.started_at.tzinfo or timezone.utc) if job.started_at else None
    # A server restart kills the thread without a final write; do not show it as running forever.
    if state == 'running' and started and datetime.now(timezone.utc) - started > STALE_AFTER:
        state = 'interrupted'
    return {'state': state, 'job_id': job.id,
            'started_at': job.started_at.isoformat() if job.started_at else None,
            'finished_at': job.ended_at.isoformat() if job.ended_at else None,
            'current': detail.get('current'),
            'steps': [{'name': s, 'label': LABELS[s], **steps.get(s, {'state': 'pending'})} for s in STEPS]}


def status():
    with SessionLocal() as db:
        job = db.scalar(select(CollectionJob).where(CollectionJob.collector == COLLECTOR)
                        .order_by(CollectionJob.id.desc()).limit(1))
        return _view(job)


def _save(job_id, detail, state=None):
    with SessionLocal() as db:
        job = db.get(CollectionJob, job_id)
        if job is None:
            return
        job.error_summary = json.dumps(detail, ensure_ascii=False, default=str)
        if state:
            job.status = state
            job.ended_at = now()
        db.commit()


# --- steps -------------------------------------------------------------------------------

def step_catalog(ctx):
    from app.services.catalog_refresh import run_now
    result = run_now()
    state = {'completed': 'completed', 'partial': 'partial', 'skipped': 'skipped',
             'not_configured': 'skipped'}.get(result.get('state'), 'failed')
    keep = ('new_products', 'processed_products', 'checked_pages', 'failed', 'index_pending', 'reason')
    return state, {k: result[k] for k in keep if k in result}


def ollama_ready(base_url, models):
    try:
        r = httpx.get(base_url.rstrip('/') + '/api/tags', timeout=5)
        r.raise_for_status()
        names = {m.get('name') for m in r.json().get('models', [])}
    except (httpx.HTTPError, ValueError):
        return 'OLLAMA_UNREACHABLE'
    missing = [m for m in models if m not in names]
    return 'MODEL_MISSING:' + ','.join(missing) if missing else None


def step_semantics(ctx):
    from app.services.worker_lock import WorkerAlreadyRunning, advisory_lock
    from scripts.split_semantics_worker import consume
    settings = get_settings()
    models = (settings.semantic_translation_model, settings.semantic_classification_model)
    problem = ollama_ready(settings.semantic_base_url, models)
    if problem:
        return 'skipped', {'reason': problem, 'note': '상품은 저장됐고 번역 대기열에 남아 있습니다. Ollama를 켠 뒤 다시 실행하세요.'}
    root = settings.semantic_report_dir  # same failure history as the semantic worker
    totals = {'committed': 0, 'failed': 0, 'pending_total': 0, 'rounds': 0}
    try:
        with advisory_lock('split_semantics_worker'):
            while totals['committed'] + totals['failed'] < SEMANTIC_MAX_ITEMS:
                r = consume(SEMANTIC_BATCH, root, translation_model=models[0], classification_model=models[1],
                            skip_failed=True, retry_stale=True)
                totals['rounds'] += 1
                totals['committed'] += r['committed']
                totals['failed'] += r['failed']
                totals['pending_total'] = r['pending_total']
                ctx['progress']({'semantics': dict(totals)})
                if not r['selected']:
                    break
    except WorkerAlreadyRunning:
        return 'skipped', {'reason': 'SEMANTIC_WORKER_RUNNING', 'note': '번역 워커가 이미 같은 대기열을 처리하고 있습니다.'}
    except httpx.HTTPError as exc:
        return 'failed', {**totals, 'reason': 'OLLAMA_' + type(exc).__name__}
    return ('partial' if totals['failed'] else 'completed'), totals


def step_events(ctx):
    from app.integrations.instagram.config import InstagramSettings
    from scripts.collect_instagram_events import collect
    settings = InstagramSettings.from_local_env()
    if not (settings.meta_access_token.get_secret_value() and settings.meta_ig_user_id):
        return 'skipped', {'reason': 'META_NOT_CONFIGURED'}
    report_dir = get_settings().private_dir / 'events' / datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S')
    code, summary = collect(report_dir, commit=True)
    error = summary.get('error')
    reason = summary.get('reason') or (error.get('reason') if isinstance(error, dict) else error)
    if summary.get('decision') == 'NO-GO':
        reason = 'META_GATE_NO_GO:' + str(reason)
    detail = {'posts': summary.get('posts', 0), 'by_status': summary.get('summary') or {}}
    if reason:
        detail['reason'] = reason
    # Event dates are extracted from each caption at collection time; ongoing/upcoming/ended is
    # computed from those dates on every read (event_catalog.period), so nothing goes stale.
    return ('completed' if code == 0 else 'failed' if code == 1 else 'skipped'), detail


def step_verify(ctx):
    from app.models.semantics import ProductSemantics
    from app.services.semantic_queue import pending_jobs
    first_new = ctx['max_figure_id'] + 1
    with SessionLocal() as db:
        new_ids = list(db.scalars(select(Figure.id).where(Figure.id >= first_new)))
        by_status = dict(db.execute(select(ProductSemantics.status, func.count())
                                    .where(ProductSemantics.figure_id >= first_new)
                                    .group_by(ProductSemantics.status)).all())
        queue = len(pending_jobs(db, 100000))
    untranslated = len(new_ids) - sum(by_status.values())
    detail = {'new_products': len(new_ids), 'ready': by_status.get('ready', 0),
              'partial': by_status.get('partial', 0), 'review': by_status.get('review', 0),
              'not_yet_translated': max(0, untranslated), 'semantic_queue': queue}
    events = ctx['steps'].get('events', {})
    if events.get('by_status'):
        detail['event_candidates'] = events['by_status'].get('PENDING_REVIEW', 0)
    return ('partial' if detail['review'] or detail['not_yet_translated'] else 'completed'), detail


RUNNERS = {'catalog': step_catalog, 'semantics': step_semantics, 'events': step_events, 'verify': step_verify}


def _steps(job_id, steps, detail):
    with SessionLocal() as db:
        ctx = {'max_figure_id': db.scalar(select(func.max(Figure.id))) or 0, 'steps': detail['steps']}

    def progress(extra):
        detail['steps'][detail['current']].update(extra.get(detail['current'], {}))
        _save(job_id, detail)
    ctx['progress'] = progress
    for name in STEPS:
        if name not in steps:
            detail['steps'][name] = {'state': 'not_requested'}
            continue
        detail['current'] = name
        detail['steps'][name] = {'state': 'running', 'started_at': _stamp()}
        _save(job_id, detail)
        try:
            state, info = RUNNERS[name](ctx)
        except Exception as exc:  # one step's failure must not stop the others
            LOG.exception('master_pipeline_step_failed step=%s', name)
            state, info = 'failed', {'reason': type(exc).__name__}
        detail['steps'][name] = {**detail['steps'][name], **info, 'state': state, 'finished_at': _stamp()}
        _save(job_id, detail)
    detail['current'] = None
    states = [detail['steps'][s]['state'] for s in steps]
    return ('completed' if all(s == 'completed' for s in states) else
            'failed' if all(s == 'failed' for s in states) else 'partial')


def _run(job_id, steps):
    global _running
    from app.services.worker_lock import WorkerAlreadyRunning, advisory_lock
    detail = {'steps': {}, 'requested': list(steps)}
    final = 'failed'
    try:
        with advisory_lock(COLLECTOR):
            final = _steps(job_id, steps, detail)
    except WorkerAlreadyRunning:
        detail['reason'] = 'ALREADY_RUNNING_ELSEWHERE'
        final = 'skipped'
    except Exception as exc:
        LOG.exception('master_pipeline_failed')
        detail['reason'] = type(exc).__name__
    finally:
        _save(job_id, detail, final)
        with _gate:
            _running = False


def start(steps=None, background=True):
    """Start a run; returns the status view. steps defaults to every step."""
    global _running
    steps = [s for s in STEPS if s in (steps or STEPS)]
    if not steps:
        raise ValueError('NO_STEPS')
    with _gate:
        if _running:
            return {**status(), 'reason': 'already_running'}
        with SessionLocal() as db:
            job = CollectionJob(collector=COLLECTOR, status='running', count=0,
                                error_summary=json.dumps({'steps': {}, 'requested': steps}))
            db.add(job)
            db.commit()
            job_id = job.id
        _running = True
    if background:
        try:
            threading.Thread(target=_run, args=(job_id, steps), name='master-pipeline', daemon=True).start()
        except Exception:
            with _gate:
                _running = False
            raise
    else:
        _run(job_id, steps)
    return {**status(), 'reason': 'started'}

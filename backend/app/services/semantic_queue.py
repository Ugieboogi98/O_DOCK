"""Durable, source-versioned semantic work. Enqueueing never calls a provider."""
import json
from sqlalchemy import select, text, exists, cast, String
from app.models.entities import CollectionJob, now
from app.models.semantics import ProductSemantics

PREFIX = 'catalog_semantics:'


def task_name(figure_id):
    return PREFIX + str(figure_id)


def pending_jobs(db, limit=100):
    return list(db.scalars(select(CollectionJob).where(
        CollectionJob.collector.startswith(PREFIX, autoescape=True), CollectionJob.status == 'pending'
    ).order_by(CollectionJob.id).limit(limit)))


def queued_match(figure_id):
    return exists(select(CollectionJob.id).where(
        CollectionJob.collector == PREFIX + cast(figure_id, String),
        CollectionJob.status == 'pending'))


def enqueue(db, figure):
    """Join the caller's transaction; serialize same-product writers on PostgreSQL."""
    from app.services.product_semantics import source_of, source_hash
    if db.bind.dialect.name == 'postgresql':
        db.execute(text('SELECT pg_advisory_xact_lock(20261110, :id)'), {'id': figure.id})
    digest = source_hash(source_of(figure))
    cached = db.get(ProductSemantics, figure.id)
    job = db.scalar(select(CollectionJob).where(
        CollectionJob.collector == task_name(figure.id), CollectionJob.status == 'pending'
    ).order_by(CollectionJob.id).limit(1))
    if cached and cached.source_hash == digest:
        if job:
            job.status = 'review' if cached.status == 'review' else 'completed'
            job.ended_at = now()
        return None
    payload = {'figure_id': figure.id, 'source_hash': digest, 'url': figure.official_url}
    if job is None:
        job = CollectionJob(collector=task_name(figure.id), status='pending', count=0)
        db.add(job)
    job.error_summary = json.dumps(payload)
    return job


def finish(db, figure_id, digest, status):
    """A report for an older source must never consume newer queued work."""
    jobs = db.scalars(select(CollectionJob).where(
        CollectionJob.collector == task_name(figure_id), CollectionJob.status == 'pending'))
    for job in jobs:
        if json.loads(job.error_summary)['source_hash'] == digest:
            job.status = 'review' if status == 'review' else 'completed'
            job.ended_at = now()
            job.count = 1

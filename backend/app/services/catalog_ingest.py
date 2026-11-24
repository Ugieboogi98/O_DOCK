"""Append-only official metadata ingestion with a durable indexing outbox.

seed commits the pending CollectionJob and the product in the same transaction.
All callers of this service serialize identity checks using a transaction lock.
Optional derivative jobs reuse the detail response; failures remain retryable.
"""

import json
from urllib.parse import urldefrag, urlparse
from sqlalchemy import select, text, or_
from app.collectors.manufacturers import ADAPTERS
from app.core.database import SessionLocal
from app.models.entities import CollectionJob, Figure, FigureVariant, Manufacturer, now
from app.services.seed_import import seed
from app.services.semantic_queue import enqueue as enqueue_semantics

INDEX_JOB = "catalog_index"
INGEST_LOCK = 2026102203


def adapter_for(url):
    host = (urlparse(url).hostname or "").lower()
    return next((a for a in ADAPTERS if host in a.domains), None)


def _index(db, figure, job):
    try:
        from app.rag.store import index_variant

        for variant in figure.variants:
            index_variant(db, figure, variant)
    except Exception as exc:
        # PostgreSQL already committed: keep a retryable outbox, never undo product data.
        db.rollback()
        job = db.get(CollectionJob, job.id)
        payload = json.loads(job.error_summary)
        payload["error"] = type(exc).__name__
        job.error_summary = json.dumps(payload)
        job.status = "pending"
        db.commit()
        return False
    job.status = "completed"
    job.ended_at = now()
    job.count = len(figure.variants)
    db.commit()
    return True


def retry_pending_indexes(limit=500):
    summary = {"indexed": 0, "failed": 0}
    with SessionLocal() as db:
        jobs = list(
            db.scalars(
                select(CollectionJob)
                .where(
                    CollectionJob.collector == INDEX_JOB,
                    CollectionJob.status == "pending",
                )
                .order_by(CollectionJob.id)
                .limit(limit)
            )
        )
        for job in jobs:
            url = json.loads(job.error_summary)["url"]
            figure = db.scalar(select(Figure).where(Figure.official_url == url))
            if figure is None:
                summary["failed"] += 1
                continue
            summary["indexed" if _index(db, figure, job) else "failed"] += 1
    return summary


def collect_one(fetcher, url, *, enrich=False):
    url = urldefrag(url.strip())[0]
    adapter = adapter_for(url)
    if adapter is None or not adapter.is_product_url(url):
        raise ValueError("NOT_A_PRODUCT_URL")
    from app.services.collection_preferences import excluded_manufacturer
    if excluded_manufacturer(adapter.manufacturer):
        raise ValueError('MANUFACTURER_EXCLUDED')
    # Validate even saved URLs; configuration may have changed since discovery.
    fetcher.validate(url)
    with SessionLocal() as db:
        existing = db.scalar(select(Figure).where(Figure.official_url == url))
        if existing is not None:
            enqueue_semantics(db, existing)
            pending = db.scalar(
                select(CollectionJob.id)
                .where(
                    CollectionJob.collector == INDEX_JOB,
                    CollectionJob.status == "pending",
                    CollectionJob.error_summary.contains(url),
                )
                .limit(1)
            )
            db.commit()
            return "existing_index_pending" if pending else "existing"
    html, final_url = (
        fetcher.fetch_page(url)
        if hasattr(fetcher, "fetch_page")
        else (fetcher.fetch(url), url)
    )
    if adapter_for(final_url) is not adapter or not adapter.is_product_url(final_url):
        raise ValueError("REDIRECT_NOT_A_PRODUCT")
    row = adapter.parse(html, final_url)
    if (
        row.get("manufacturer") != adapter.manufacturer
        or not row.get("name_original", "").strip()
    ):
        raise ValueError("INVALID_PRODUCT_IDENTITY")
    row.update(
        source_url=final_url,
        checked_at=now().isoformat(),
        source_text=json.dumps(row, ensure_ascii=False),
    )
    with SessionLocal() as db:
        if db.bind.dialect.name == "postgresql":
            db.execute(text("SELECT pg_advisory_xact_lock(:key)"), {"key": INGEST_LOCK})
        if (
            db.scalar(
                select(Figure.id).where(
                    Figure.official_url.in_([url, row["official_url"]])
                )
            )
            is not None
        ):
            return "existing"
        identifiers = []
        if row.get("jan_code"):
            identifiers.append(FigureVariant.jan_code == row["jan_code"])
        if row.get("sku"):
            identifiers.append(FigureVariant.sku == row["sku"])
        if identifiers:
            duplicate = db.scalar(
                select(Figure.id)
                .join(FigureVariant)
                .join(Manufacturer, Manufacturer.id == Figure.manufacturer_id)
                .where(Manufacturer.name == row["manufacturer"], or_(*identifiers))
                .limit(1)
            )
            if duplicate is not None:
                return "existing"
        job = CollectionJob(
            collector=INDEX_JOB,
            status="pending",
            count=0,
            error_summary=json.dumps({"url": row["official_url"]}),
        )
        db.add(job)
        created = seed(db, [row], refresh=False, commit=False)
        figure = db.scalar(
            select(Figure).where(Figure.official_url == row["official_url"])
        )
        enqueue_semantics(db, figure)
        db.commit()  # Product, index outbox and semantic work are durable together.
        if enrich:
            derivative = CollectionJob(
                collector="catalog_enrichment",
                status="pending",
                count=0,
                error_summary=json.dumps({"url": final_url}),
            )
            db.add(derivative)
            db.commit()
            _enrich(db, figure, derivative, html, final_url)
        indexed = _index(db, figure, job)
        return (
            ("created" if indexed else "created_index_pending")
            if created
            else "existing"
        )


def _enrich(db, figure, job, html, url):
    from app.services.enrichment import enrich_html

    try:
        for variant in figure.variants:
            result = enrich_html(db, figure, variant, html, url, images=True)
            if result.get("image_failures"):
                raise ValueError("IMAGE_DOWNLOAD_INCOMPLETE")
        semantic_task = enqueue_semantics(db, figure)
        job.status = "completed"
        job.ended_at = now()
        job.error_summary = json.dumps(
            {"url": url, "translation": "queued_for_validation" if semantic_task else "cached_validation"}
        )
        db.commit()
        return True
    except Exception as exc:
        db.rollback()
        # Media enrichment may already have committed part of the source text.
        enqueue_semantics(db, figure)
        job.error_summary = json.dumps({"url": url, "error": type(exc).__name__})
        job.status = "pending"
        db.commit()
        return False


def retry_pending_enrichment(fetcher, limit=3):
    summary = {"completed": 0, "failed": 0}
    with SessionLocal() as db:
        jobs = list(
            db.scalars(
                select(CollectionJob)
                .where(
                    CollectionJob.collector == "catalog_enrichment",
                    CollectionJob.status == "pending",
                )
                .order_by(CollectionJob.id)
                .limit(limit)
            )
        )
        for job in jobs:
            try:
                url = json.loads(job.error_summary)["url"]
                figure = db.scalar(select(Figure).where(Figure.official_url == url))
                if figure is None:
                    raise ValueError("MISSING_FIGURE")
                html = fetcher.fetch(url)
                ok = _enrich(db, figure, job, html, url)
                summary["completed" if ok else "failed"] += 1
                if ok:
                    index_job = CollectionJob(
                        collector=INDEX_JOB,
                        status="pending",
                        count=0,
                        error_summary=json.dumps({"url": url}),
                    )
                    db.add(index_job)
                    db.commit()
            except Exception:
                db.rollback()
                summary["failed"] += 1
    return summary

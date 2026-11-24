"""Bounded, opt-in catalog discovery and ingestion on a site visit.

The source allowlist and robots rules are still enforced by SafeFetcher.
DB CollectionJob records are used for progress and cooldown (no new tables).
"""

from __future__ import annotations

import json
import logging
import threading
from collections import deque
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urldefrag, urlparse

from sqlalchemy import select, text, or_

from app.collectors.safe_http import SafeFetcher
from app.collectors.manufacturers import ADAPTERS
from app.core.config import get_settings
from app.core.database import SessionLocal
from app.models.entities import CollectionJob, Figure, FigureVariant, Manufacturer, now

LOG = logging.getLogger(__name__)
COLLECTOR = "auto_catalog_refresh"
LOCK_KEY = 2026102102
_gate = threading.Lock()
# Guarded by _gate, within one ASGI worker. PostgreSQL handles cross-worker locking.
_pending = False


def _utc(value):
    if value is None:
        return None
    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc)


def _latest(db):
    return db.scalar(
        select(CollectionJob)
        .where(CollectionJob.collector == COLLECTOR)
        .order_by(CollectionJob.id.desc())
        .limit(1)
    )


def _result(job):
    if job is None:
        return {
            "state": "never",
            "new_products": 0,
            "processed_products": 0,
            "checked_pages": 0,
            "finished_at": None,
        }
    try:
        detail = json.loads(job.error_summary or "{}")
        if not isinstance(detail, dict):
            detail = {}
    except (ValueError, TypeError):
        detail = {}
    return {
        "state": job.status,
        "job_id": job.id,
        "new_products": detail.get("new_products", job.count or 0),
        "processed_products": detail.get("processed_products", 0),
        "checked_pages": detail.get("checked_pages", 0),
        "failed": detail.get("failed", 0),
        "index_pending": detail.get("index_pending", 0),
        "sources": detail.get("sources", []),
        "finished_at": job.ended_at.isoformat() if job.ended_at else None,
        "started_at": job.started_at.isoformat() if job.started_at else None,
    }


def refresh_status():
    with SessionLocal() as db:
        return _result(_latest(db))


def _config():
    path = Path(get_settings().data_dir) / "catalog_sources.json"
    if not path.is_file():
        return {
            "sources": [],
            "max_pages_per_source": 3,
            "max_new_products_per_run": 30,
        }
    settings = json.loads(path.read_text(encoding="utf-8-sig"))
    settings["max_pages_per_source"] = max(
        1, min(int(settings.get("max_pages_per_source", 3)), 10)
    )
    settings["max_new_products_per_run"] = max(
        1, min(int(settings.get("max_new_products_per_run", 30)), 100)
    )
    settings["max_products_per_source"] = max(
        1, min(int(settings.get("max_products_per_source", 20)), 100)
    )
    return settings


def _adapter(url):
    host = urlparse(url).hostname
    return next((adapter for adapter in ADAPTERS if host in adapter.domains), None)


def _canonical(url):
    return urldefrag(url.strip())[0]


def _next_pages(html, base_url, start_url):
    # Reuse the separately supplied discovery script's pagination detection.
    from app.collectors.pagination import pagination_links

    base = urlparse(start_url)
    for link in pagination_links(html, base_url):
        parsed = urlparse(link)
        # Follow only the approved source's catalog path, never off-site links.
        if (
            parsed.hostname == base.hostname
            and parsed.path.startswith(base.path.rstrip("/") + "/")
            or (parsed.hostname == base.hostname and parsed.path == base.path)
        ):
            yield link


# Backwards-compatible entry point for manual and automatic catalog collection.
from app.services.catalog_ingest import collect_one as _collect_one


def _execute(job_id):
    global _pending
    stats = {
        "new_products": 0,
        "processed_products": 0,
        "checked_pages": 0,
        "failed": 0,
        "index_pending": 0,
        "sources": [],
    }
    lock_session = None
    locked = False
    final_state = "failed"
    try:
        # Dedicated connection: session-level advisory lock prevents concurrent
        # collectors across Uvicorn workers. Never return it to the pool locked.
        lock_session = SessionLocal()
        locked = bool(
            lock_session.execute(
                text("SELECT pg_try_advisory_lock(:key)"), {"key": LOCK_KEY}
            ).scalar()
        )
        if not locked:
            final_state = "skipped"
            return
        config = _config()
        from app.services.catalog_ingest import retry_pending_indexes

        retried = retry_pending_indexes()
        stats["failed"] += retried["failed"]
        fetcher = SafeFetcher()
        from app.services.catalog_ingest import retry_pending_enrichment

        derivatives = retry_pending_enrichment(fetcher)
        stats["failed"] += derivatives["failed"]
        attempted_urls = set()
        limit = config["max_new_products_per_run"]
        from app.services.collection_preferences import excluded_manufacturer
        sources = [x for x in config.get("sources", []) if x.get("auto_enabled") and not excluded_manufacturer(x.get('manufacturer'))]
        if sources:
            offset = job_id % len(sources)
            sources = sources[offset:] + sources[:offset]
        # Fair share per source: a large maker cannot consume the whole run.
        per_source = max(1, limit // max(1, len(sources)))
        for source in sources:
            source_budget = min(per_source, max(0, limit - stats["new_products"]))
            source_new = 0
            source_processed = 0
            before_failed = stats["failed"]
            report = {
                "manufacturer": source.get("manufacturer"),
                "url": source.get("start_url"),
                "state": "running",
            }
            stats["sources"].append(report)
            if source_budget == 0:
                report["state"] = "budget_deferred"
                continue
            if source.get("driver") == "bnkr":
                try:
                    from app.services.bnkr_catalog import refresh_source

                    result = refresh_source(
                        source, config["max_pages_per_source"], source_budget
                    )
                    for key in (
                        "new_products",
                        "processed_products",
                        "failed",
                        "checked_pages",
                    ):
                        stats[key] += result[key]
                    report.update(result)
                    if result["state"] == "busy":
                        stats["failed"] += 1
                except Exception as exc:
                    stats["failed"] += 1
                    report.update(state="failed", error=type(exc).__name__)
                continue
            start = _canonical(source["start_url"])
            adapter = _adapter(start)
            if adapter is None or adapter.manufacturer != source.get("manufacturer"):
                stats["failed"] += 1
                report["state"] = "adapter_mismatch"
                continue
            # Fail closed for disabled paths / disallowed hosts.
            try:
                fetcher.validate(start)
            except Exception:
                stats["failed"] += 1
                report["state"] = "source_unavailable"
                continue
            queue = deque([start])
            visited = set()
            while (
                queue
                and len(visited) < config["max_pages_per_source"]
                and source_new < source_budget
                and source_processed < config.get("max_products_per_source", 20)
            ):
                page_url = queue.popleft()
                if page_url in visited:
                    continue
                visited.add(page_url)
                try:
                    html = fetcher.fetch(page_url)
                    stats["checked_pages"] += 1
                    urls = adapter.discover(html, page_url)
                    if not urls:
                        raise ValueError("NO_PRODUCT_LINKS_REVIEW_HTML_OR_JS")
                    for product in urls:
                        url = _canonical(product)
                        if not adapter.is_product_url(url):
                            continue
                        if url in attempted_urls or _adapter(url) is not adapter:
                            continue
                        attempted_urls.add(url)
                        try:
                            fetcher.validate(url)
                            result = _collect_one(fetcher, url, enrich=True)
                            stats["processed_products"] += 1
                            if not result.startswith("existing"):
                                source_processed += 1
                            if result in ("created", "created_index_pending"):
                                stats["new_products"] += 1
                                source_new += 1
                            if result in (
                                "created_index_pending",
                                "existing_index_pending",
                            ):
                                stats["index_pending"] += 1
                                stats["failed"] += 1
                        except Exception as exc:
                            source_processed += 1
                            stats["failed"] += 1
                            LOG.warning(
                                "product_collection_failed type=%s", type(exc).__name__
                            )
                        if (
                            source_new >= source_budget
                            or source_processed
                            >= config.get("max_products_per_source", 20)
                        ):
                            break
                    if source_new < source_budget:
                        for nxt in _next_pages(html, page_url, start):
                            if nxt not in visited and nxt not in queue:
                                try:
                                    fetcher.validate(nxt)
                                    queue.append(nxt)
                                except Exception:
                                    continue
                except Exception as exc:
                    stats["failed"] += 1
                    LOG.warning("catalog_collection_failed type=%s", type(exc).__name__)
            report.update(
                state="partial" if stats["failed"] > before_failed else "completed",
                new_products=source_new,
                processed_products=source_processed,
            )
            with SessionLocal() as progress_db:
                progress = progress_db.get(CollectionJob, job_id)
                if progress:
                    progress.error_summary = json.dumps(stats, ensure_ascii=False)
                    progress_db.commit()
        if config.get('domestic_enabled'):
            from app.services.domestic_collection_round import run_round
            stats['domestic'] = run_round(get_settings().media_dir / 'domestic_rounds' / str(job_id),
                                          max(1,min(100,int(config.get('domestic_max_products_per_source',20)))))
            if stats['domestic']['state'] != 'completed':
                stats['failed'] += 1
        final_state = "partial" if stats["failed"] else "completed"
    except Exception as exc:
        stats["failed"] += 1
        LOG.error("catalog_refresh_failed type=%s", type(exc).__name__)
        final_state = "failed"
    finally:
        if lock_session is not None:
            try:
                if locked:
                    lock_session.execute(
                        text("SELECT pg_advisory_unlock(:key)"), {"key": LOCK_KEY}
                    )
            finally:
                lock_session.close()
        try:
            with SessionLocal() as db:
                job = db.get(CollectionJob, job_id)
                if job:
                    job.status = final_state
                    job.count = stats["new_products"]
                    job.ended_at = now()
                    job.error_summary = json.dumps(stats, ensure_ascii=False)
                    db.commit()
        except Exception:
            LOG.exception("catalog_job_record_failed")
        with _gate:
            _pending = False


def start_refresh():
    """At most one local pending job, + persisted cooldown across server restarts."""
    global _pending
    with _gate:
        if _pending:
            return {"state": "running", "reason": "already_running"}
        with SessionLocal() as db:
            if db.bind.dialect.name == "postgresql":
                db.execute(
                    text("SELECT pg_advisory_xact_lock(:key)"), {"key": LOCK_KEY + 1}
                )
            last = _latest(db)
            # Failed attempts retry only after an hour; successful after 24 hours.
            if last:
                stamp = _utc(last.started_at or last.ended_at)
                if stamp:
                    elapsed = datetime.now(timezone.utc) - stamp
                    cooldown = timedelta(hours=24 if last.status == "completed" else 1)
                    if elapsed < cooldown:
                        return {**_result(last), "reason": "cooldown"}
            try:
                config = _config()
                if not any(x.get("auto_enabled") for x in config.get("sources", [])):
                    return {
                        "state": "not_configured",
                        "reason": "no_enabled_catalog_sources",
                    }
            except (ValueError, OSError, TypeError, KeyError):
                return {"state": "not_configured", "reason": "invalid_catalog_sources"}
            job = CollectionJob(
                collector=COLLECTOR,
                status="running",
                count=0,
                error_summary=json.dumps(
                    {
                        "new_products": 0,
                        "processed_products": 0,
                        "checked_pages": 0,
                        "failed": 0,
                        "index_pending": 0,
                    }
                ),
            )
            db.add(job)
            db.commit()
            job_id = job.id
        _pending = True
        try:
            threading.Thread(
                target=_execute, args=(job_id,), name="catalog-refresh", daemon=True
            ).start()
        except Exception:
            _pending = False
            raise
        return {"state": "running", "job_id": job_id, "reason": "started"}

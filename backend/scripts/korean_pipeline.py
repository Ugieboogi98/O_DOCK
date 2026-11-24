"""Translate existing DB records and build a separate Korean RAG index."""

import argparse, json, sys, fcntl
from sqlalchemy import select
from app.core.database import SessionLocal
from app.core.config import get_settings
from app.models.entities import Figure, SourceDocument, Manufacturer
from app.services.ko_translation import (
    Translator,
    TranslationError,
    translate_figure,
    current_profile,
    current_chunks,
    parts,
    failure,
)


def output(**data):
    print(json.dumps(data, ensure_ascii=False), flush=True)


def run(args):
    from app.rag.ko_rag import index_figure, index_name, config, embedder

    stats = {
        "processed": 0,
        "saved_units": 0,
        "indexed": 0,
        "failed": 0,
        "blocked": None,
        "interrupted": False,
        "last_figure_id": None,
    }
    translator = None
    with SessionLocal() as db:
        query = select(Figure.id).where(Figure.id > args.after_id).order_by(Figure.id)
        if args.figure_id:
            query = query.where(Figure.id == args.figure_id)
        if args.manufacturer:
            query = query.join(Manufacturer).where(
                Manufacturer.name == args.manufacturer
            )
        ids = list(db.scalars(query))
        ids = ids[: args.limit] if args.limit else ids
        if args.stage == "audit":
            profiles = docs = translated = chunks_total = chunks_ready = 0
            for fid in ids:
                f = db.get(Figure, fid)
                profiles += int(current_profile(db, f) is not None)
                for v in f.variants:
                    for d in db.scalars(
                        select(SourceDocument).where(SourceDocument.variant_id == v.id)
                    ):
                        n = len(parts(d.body))
                        ready = len(current_chunks(db, d))
                        docs += 1
                        translated += int(n == ready)
                        chunks_total += n
                        chunks_ready += ready
            from app.rag.ko_rag import collection, records

            index_audit = {"expected_records": 0, "matching_records": 0, "error": None}
            try:
                saved = collection().get(include=["metadatas"])
                indexed = {
                    rid: m.get("fingerprint")
                    for rid, m in zip(saved["ids"], saved["metadatas"])
                }
                for fid in ids:
                    f = db.get(Figure, fid)
                    for v in f.variants:
                        for row in records(db, f, v):
                            index_audit["expected_records"] += 1
                            index_audit["matching_records"] += int(
                                indexed.get(row["id"]) == row["metadata"]["fingerprint"]
                            )
                index_audit["missing_or_stale"] = (
                    index_audit["expected_records"] - index_audit["matching_records"]
                )
            except Exception as exc:
                index_audit["error"] = type(exc).__name__
            return {
                "figures": len(ids),
                "profiles_ready": profiles,
                "profiles_missing": len(ids) - profiles,
                "documents": docs,
                "documents_complete": translated,
                "chunks_ready": chunks_ready,
                "chunks_total": chunks_total,
                "korean_embedding_provider": config()["provider"],
                "index_collection": index_name(),
                "index": index_audit,
            }, 0
        try:
            if args.stage in ("translate", "all"):
                translator = Translator(args.interval, args.retries)
            if args.stage in ("index", "all"):
                embedder()  # Check required key before starting paid translation.
            for fid in ids:
                f = db.get(Figure, fid)
                stats["processed"] += 1
                stats["last_figure_id"] = fid
                output(
                    figure_id=fid,
                    progress=f'{stats["processed"]}/{len(ids)}',
                    stage=args.stage,
                )
                try:
                    if translator:

                        def saved(**event):
                            stats["saved_units"] += 1
                            output(**event)

                        translate_figure(db, f, translator, saved)
                    if args.stage in ("index", "all"):
                        result = index_figure(db, f)
                        output(figure_id=fid, **result)
                        if result["state"] == "indexed":
                            stats["indexed"] += 1
                        else:
                            stats["failed"] += 1
                except TranslationError as exc:
                    db.rollback()
                    stats["failed"] += 1
                    output(figure_id=fid, error=exc.code)
                    if exc.blocked:
                        stats["blocked"] = exc.code
                        break
                except Exception as exc:
                    db.rollback()
                    stats["failed"] += 1
                    # Stop on provider failures rather than repeating paid/failed calls for the whole catalogue.
                    code, retry = failure(exc)
                    output(figure_id=fid, error=type(exc).__name__, code=code)
                    stats["blocked"] = code
                    break
        except TranslationError as exc:
            stats["blocked"] = exc.code
        except KeyboardInterrupt:
            db.rollback()
            stats["interrupted"] = True
        except Exception as exc:
            stats["blocked"] = (
                str(exc)
                if isinstance(exc, ValueError)
                and str(exc)
                in ("EMBEDDING_API_KEY_REQUIRED", "KOREAN_EMBEDDING_PROVIDER_INVALID")
                else type(exc).__name__
            )
    return stats, (
        130 if stats["interrupted"] else 1 if stats["failed"] or stats["blocked"] else 0
    )


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--stage", choices=["audit", "translate", "index", "all"], default="audit"
    )
    p.add_argument(
        "--limit", type=int, default=0, help="Maximum selected products; 0 means all"
    )
    p.add_argument("--after-id", type=int, default=0)
    p.add_argument("--figure-id", type=int)
    p.add_argument("--manufacturer")
    p.add_argument("--interval", type=float, default=2)
    p.add_argument("--retries", type=int, default=2)
    args = p.parse_args()
    if (
        args.limit < 0
        or args.after_id < 0
        or not 1 <= args.interval <= 60
        or not 0 <= args.retries <= 5
    ):
        p.error("Invalid limit, ID, interval or retries")
    if args.stage == "audit":
        result, code = run(args)
    else:
        folder = get_settings().media_dir / ".locks"
        folder.mkdir(parents=True, exist_ok=True)
        with (folder / "korean-pipeline.lock").open("a") as lock:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                output(state="busy")
                return 1
            result, code = run(args)
    print(json.dumps(result, ensure_ascii=False, indent=2), flush=True)
    return code


if __name__ == "__main__":
    sys.exit(main())

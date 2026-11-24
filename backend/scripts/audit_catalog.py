"""Read-only inventory and completeness report. Never reindexes or calls an LLM."""

import json
from sqlalchemy import select, func
from app.core.database import SessionLocal
from app.models.entities import (
    Figure,
    FigureVariant,
    Manufacturer,
    ReleasePrice,
    SourceDocument,
    CollectionJob,
)
from app.core.config import get_settings


def audit(db):
    result = {
        "figures": db.scalar(select(func.count(Figure.id))),
        "variants": db.scalar(select(func.count(FigureVariant.id))),
        "source_documents": db.scalar(select(func.count(SourceDocument.id))),
        "embedding_provider": get_settings().embedding_provider,
        "pending_index_jobs": db.scalar(
            select(func.count(CollectionJob.id)).where(
                CollectionJob.collector == "catalog_index",
                CollectionJob.status == "pending",
            )
        ),
        "manufacturers": [],
    }
    for maker in db.scalars(select(Manufacturer).order_by(Manufacturer.id)):
        fs = list(db.scalars(select(Figure).where(Figure.manufacturer_id == maker.id)))
        vs = [v for f in fs for v in f.variants]
        entry = {"manufacturer": maker.name, "figures": len(fs), "missing": {}}
        for field in (
            "name_original",
            "name_ko",
            "franchise",
            "scale",
            "height_mm",
            "material",
        ):
            entry["missing"][field] = sum(getattr(f, field) in (None, "") for f in fs)
        for field in ("sku", "jan_code", "release_date"):
            entry["missing"][field] = sum(getattr(v, field) in (None, "") for v in vs)
        vids = [v.id for v in vs]
        priced = set(
            db.scalars(
                select(ReleasePrice.variant_id).where(ReleasePrice.variant_id.in_(vids))
            )
        )
        entry["missing"]["official_price"] = sum(v.id not in priced for v in vs)
        from app.services.enrichment import image_count

        entry["missing"]["product_images"] = sum(
            image_count(db, [v.id for v in f.variants]) == 0 for f in fs
        )
        entry["variant_count"] = len(vs)
        result["manufacturers"].append(entry)
    try:
        from app.rag.store import collection

        result["index"] = {
            k: collection(n).count()
            for k, n in [
                ("metadata", "figure_metadata"),
                ("documents", "figure_documents"),
            ]
        }
        result["metadata_count_matches"] = (
            result["index"]["metadata"] == result["variants"]
        )
    except Exception as exc:
        result["index_error"] = type(exc).__name__
    return result


if __name__ == "__main__":
    with SessionLocal() as db:
        print(json.dumps(audit(db), ensure_ascii=False, indent=2))

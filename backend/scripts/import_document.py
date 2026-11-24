import argparse, hashlib
from pathlib import Path
from sqlalchemy import select
from pypdf import PdfReader
from app.core.database import SessionLocal
from app.models.entities import SourceDocument
from app.repositories.figures import get_figure, choose_variant
from app.rag.store import index_variant

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--figure-id", type=int, required=True)
    p.add_argument("--variant-id", type=int)
    p.add_argument("--file", required=True)
    p.add_argument("--source-url", required=True)
    p.add_argument("--rights-note", required=True)
    args = p.parse_args()
    path = Path(args.file)
    pages = (
        [
            (i + 1, page.extract_text() or "")
            for i, page in enumerate(PdfReader(path).pages)
        ]
        if path.suffix.lower() == ".pdf"
        else [(None, path.read_text(encoding="utf-8"))]
    )
    with SessionLocal() as db:
        f = get_figure(db, args.figure_id)
        v = choose_variant(f, args.variant_id)
        for page, body in pages:
            if not body.strip():
                continue
            url = args.source_url + (f"#page={page}" if page else "")
            d = db.scalar(
                select(SourceDocument).where(
                    SourceDocument.variant_id == v.id, SourceDocument.url == url
                )
            ) or SourceDocument(variant_id=v.id, url=url)
            d.title = path.name + (f" p.{page}" if page else "")
            d.body = body
            d.source_type = "pdf" if page else "text"
            d.language = "und"
            d.usage_status = args.rights_note
            d.content_hash = hashlib.sha256(body.encode()).hexdigest()
            db.add(d)
        db.commit()
        print({"indexed_chunks": index_variant(db, f, v)})

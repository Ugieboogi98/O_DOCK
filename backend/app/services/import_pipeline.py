"""Atomic publication staging for offline importers. Never calls a provider."""
from app.services.semantic_queue import enqueue


def commit_import(db, figures):
    """Commit imported source records and versioned semantic work together.

    Callers choose the transaction boundary (a product or an entire bundle).
    Flushing first also supports importers that disable SQLAlchemy autoflush.
    """
    db.flush()
    metrics = {'semantic_pending': 0, 'semantic_cached': 0}
    seen = set()
    for figure in figures:
        if figure.id in seen:
            continue
        seen.add(figure.id)
        # A previously loaded relationship may describe the pre-import source.
        db.expire(figure, ['manufacturer', 'product_line'])
        job = enqueue(db, figure)
        metrics['semantic_pending' if job is not None else 'semantic_cached'] += 1
    db.commit()
    return metrics

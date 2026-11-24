"""Single-consumer guarantee shared by host and Docker workers.

A file lock only protects processes that see the same file system, so a host
worker and a container worker could both consume one queue. A PostgreSQL
session-level advisory lock is held on one connection for the worker's
lifetime. Every process that uses the same database sees it, and it is released
automatically when that connection closes or the process dies.
"""
import hashlib
from contextlib import contextmanager
from sqlalchemy import text


class WorkerAlreadyRunning(RuntimeError):
    pass


def lock_key(name):
    return int.from_bytes(hashlib.sha256(name.encode()).digest()[:8], 'big', signed=True)


@contextmanager
def advisory_lock(name, engine=None):
    if engine is None:
        from app.core.database import engine
    if engine.dialect.name != 'postgresql':
        yield None  # SQLite tests and tools: no cross-process queue to protect.
        return
    key = lock_key(name)
    with engine.connect() as conn:
        if not conn.execute(text('SELECT pg_try_advisory_lock(:k)'), {'k': key}).scalar():
            raise WorkerAlreadyRunning('WORKER_ALREADY_RUNNING:' + name)
        try:
            yield key
        finally:
            conn.execute(text('SELECT pg_advisory_unlock(:k)'), {'k': key})

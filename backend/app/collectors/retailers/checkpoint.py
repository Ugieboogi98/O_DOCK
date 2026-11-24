"""Disk-backed crawl frontier. Product commits are safe to replay after interruption."""
import sqlite3
from pathlib import Path


class Checkpoint:
    def __init__(self, path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.connection = sqlite3.connect(path)
        self.connection.execute('PRAGMA journal_mode=WAL')
        self.connection.executescript('''
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY,
                url TEXT NOT NULL UNIQUE,
                kind TEXT NOT NULL,
                state TEXT NOT NULL DEFAULT 'pending',
                error TEXT
            );
            CREATE INDEX IF NOT EXISTS jobs_pending ON jobs(state,kind,id);
        ''')
        self.connection.commit()

    def close(self):
        self.connection.close()

    def add(self, pages=(), products=()):
        with self.connection:
            self.connection.executemany('INSERT OR IGNORE INTO jobs(url,kind) VALUES (?,?)',
                                        [(url, 'page') for url in pages] + [(url, 'product') for url in products])

    def next(self):
        for kind in ('product', 'page'):
            row = self.connection.execute(
                "SELECT id,url,kind FROM jobs WHERE state='pending' AND kind=? ORDER BY id LIMIT 1", (kind,)).fetchone()
            if row:
                return {'id': row[0], 'url': row[1], 'kind': row[2]}
        return None

    def finish(self, job, state='done', error=None):
        with self.connection:
            self.connection.execute('UPDATE jobs SET state=?,error=? WHERE id=?', (state, error, job['id']))

    def counts(self):
        return {kind + '_' + state: count for kind, state, count in self.connection.execute(
            'SELECT kind,state,COUNT(*) FROM jobs GROUP BY kind,state')}

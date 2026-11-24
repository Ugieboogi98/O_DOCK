"""Run the retail collector on the host against the existing Compose database.

Pass the normal collect_domestic_catalog arguments, including --report-dir.
"""
import os
from pathlib import Path
import runpy
import sys

from dotenv import dotenv_values
from sqlalchemy.engine import URL


def main():
    root = Path(__file__).resolve().parents[1]
    values = dotenv_values(root / '.env')
    # Match Compose's PostgreSQL service credentials, without exposing them in logs.
    def value(key, default):
        return os.environ.get(key) or values.get(key) or default

    url = URL.create(
        'postgresql+psycopg',
        username=value('POSTGRES_USER', 'figure'),
        password=value('POSTGRES_PASSWORD', 'figure_local'),
        host='127.0.0.1', port=5432,
        database=value('POSTGRES_DB', 'figure_archive'),
    )
    os.environ['DATABASE_URL'] = url.render_as_string(hide_password=False)
    os.environ['DATA_DIR'] = str(root / 'data')
    os.environ['MEDIA_DIR'] = str(root / 'media')
    sys.path.insert(0, str(root / 'backend'))
    latest = '--latest' in sys.argv
    if latest:
        sys.argv.remove('--latest')
    runpy.run_module('scripts.collect_domestic_round' if latest else 'scripts.collect_domestic_catalog', run_name='__main__')


if __name__ == '__main__':
    main()

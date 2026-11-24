"""Run the semantic queue consumer with host-local PostgreSQL and Ollama access."""
import os
from pathlib import Path
import runpy
import sys

from dotenv import dotenv_values
from sqlalchemy.engine import URL

root = Path(__file__).resolve().parents[1]
values = dotenv_values(root / '.env')
url = URL.create('postgresql+psycopg', username=values.get('POSTGRES_USER') or 'figure',
                 password=values.get('POSTGRES_PASSWORD') or 'figure_local', host='127.0.0.1', port=5432,
                 database=values.get('POSTGRES_DB') or 'figure_archive')
os.environ['DATABASE_URL'] = url.render_as_string(hide_password=False)
os.environ['DATA_DIR'] = str(root / 'data')
os.environ['MEDIA_DIR'] = str(root / 'media')
os.environ['SEMANTIC_PROVIDER'] = 'ollama'
os.environ['SEMANTIC_BASE_URL'] = 'http://127.0.0.1:11434'
os.environ.setdefault('SEMANTIC_TIMEOUT', '600')
os.environ.setdefault('SEMANTIC_NUM_CTX', '16384')
sys.path.insert(0, str(root / 'backend'))
runpy.run_module('scripts.split_semantics_worker', run_name='__main__')

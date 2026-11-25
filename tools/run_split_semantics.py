"""Host launcher; credentials stay in the environment, never in command output."""
import os,sys,runpy
from pathlib import Path
from dotenv import dotenv_values
from sqlalchemy.engine import URL

root=Path(__file__).resolve().parents[1]
v=dotenv_values(root/'.env')
url=URL.create('postgresql+psycopg',username=v.get('POSTGRES_USER') or 'figure',password=v.get('POSTGRES_PASSWORD') or 'figure_local',host='127.0.0.1',port=5432,database=v.get('POSTGRES_DB') or 'figure_archive')
os.environ['DATABASE_URL']=url.render_as_string(hide_password=False)
os.environ['DATA_DIR']=str(root/'data');os.environ['MEDIA_DIR']=str(root/'media')
os.environ['SEMANTIC_PROVIDER']='ollama'
os.environ['SEMANTIC_BASE_URL']='http://127.0.0.1:11434'
sys.path.insert(0,str(root/'backend'))
module='scripts.split_semantics_worker'
if '--build-dictionary' in sys.argv:
    sys.argv.remove('--build-dictionary');module='scripts.build_semantic_dictionary'
if '--repair-names' in sys.argv:
    sys.argv.remove('--repair-names');module='scripts.repair_unverified_names'
if '--reprocess' in sys.argv:
    sys.argv.remove('--reprocess');module='scripts.reprocess_semantics'
if '--repair-web-proofs' in sys.argv:
    sys.argv.remove('--repair-web-proofs');module='scripts.repair_web_proofs'
if '--recover-classifications' in sys.argv:
    sys.argv.remove('--recover-classifications');module='scripts.recover_dictionary_classifications'
runpy.run_module(module,run_name='__main__')

"""Local staged queue: translation batch -> classification -> existing validation."""
import argparse,json,time
from pathlib import Path
from datetime import datetime,timezone
from filelock import FileLock
from app.core.config import get_settings
from app.core.database import SessionLocal
from app.models.entities import Figure
from app.services.product_semantics import source_of,source_hash,save_record,validate_result
from app.services.semantic_queue import pending_jobs
from app.services.split_semantics import Pipeline,LocalModel,VERSION
from app.services.semantic_errors import SemanticError
import httpx
from scripts.product_semantics import atomic_report

def consume(limit,root,ids=None,client=None,translation_model='qwen3:8b',classification_model='qwen3:1.7b',skip_failed=False):
    settings=get_settings();root=Path(root);root.mkdir(parents=True,exist_ok=True)
    dictionary=json.loads((settings.data_dir/'reference/semantic_dictionary/catalog.json').read_text(encoding='utf-8'))
    pipeline=Pipeline(dictionary,client or LocalModel(settings.semantic_base_url,settings.semantic_timeout),root/'stages',translation_model,classification_model)
    failures_path=root/'failures.json'
    failures=json.loads(failures_path.read_text()) if failures_path.exists() else {}
    explicit=ids is not None
    with SessionLocal() as db:
        if ids is None:ids=[json.loads(j.error_summary)['figure_id'] for j in pending_jobs(db,10000)]
    selected=[]
    deferred=0
    skipped={str(fid):failures[str(fid)] for fid in dict.fromkeys(ids) if str(fid) in failures} if skip_failed and not explicit else {}
    if skip_failed:
        atomic_report(root/'skipped_failures.json',{'policy':'skip_failed','updated_at':datetime.now(timezone.utc).isoformat(),'count':len(skipped),'items':skipped})
    for fid in dict.fromkeys(ids):
        if str(fid) in skipped:
            continue
        failure=failures.get(str(fid),{})
        if not explicit and failure.get('pipeline')==VERSION and failure.get('dictionary')==dictionary['fingerprint'] and time.time()-failure.get('time',0)<3600:
            deferred+=1
            continue
        selected.append(fid)
        if len(selected)>=limit:break
    report={'pipeline':VERSION,'selected':len(selected),'pending_total':len(ids),'skipped_failed':len(skipped),'retry_policy':'skip_failed' if skip_failed else 'cooldown','cooldown_deferred':deferred,'committed':0,'failed':0,'items':[],'dictionary':dictionary['fingerprint']}
    def progress(stage):
        atomic_report(root/'progress.json',{k:v for k,v in report.items() if k!='items'}|{'stage':stage,'updated_at':datetime.now(timezone.utc).isoformat()})
    progress('translation')
    staged=[]
    def fail(record,exc,stage):
        record.update(error=getattr(exc,'code',type(exc).__name__),failed_stage=stage)
        if getattr(exc,'details',None):record['rejected_proposal']=exc.details
        failures[str(record['figure_id'])]={'time':time.time(),'stage':stage,'error':record['error'],'dictionary':dictionary['fingerprint'],'pipeline':VERSION}
        atomic_report(failures_path,failures)
        atomic_report(root/'items'/f"{record['figure_id']}.json",record)
        report['failed']+=1;report['items'].append(record)
    # A stage batch avoids loading and unloading the two models for every product.
    for fid in selected:
        record={'figure_id':fid,'pipeline':VERSION,'paid_api_called':False}
        try:
            with SessionLocal() as db:
                f=db.get(Figure,fid)
                if f is None:raise ValueError('FIGURE_NOT_FOUND')
                source=source_of(f)
            record.update(source=source,source_hash=source_hash(source))
            record['translation']=pipeline.translate(source)
            atomic_report(root/'items'/f'{fid}.json',record)
            staged.append(record)
        except httpx.HTTPError:raise
        except Exception as exc:fail(record,exc,'translation')
        progress('translation')
    progress('classification')
    for record in staged:
        try:
            record['classification']=pipeline.classify(record['source'],record['translation'])
            record['result']={'name_ko':record['translation']['name_ko'],**record['classification']['result']}
            record['fields'],record['issues']=validate_result(record['source'],record['result'])
            record['model']=VERSION+';translation='+pipeline.translation_model+'@'+pipeline.digests[pipeline.translation_model]+';classification='+pipeline.classification_model+'@'+pipeline.digests[pipeline.classification_model]
            atomic_report(root/'items'/f"{record['figure_id']}.json",record)
            with SessionLocal() as db:record['status']=save_record(db,record)
            record['committed']=True;report['committed']+=1
            failures.pop(str(record['figure_id']),None)
            atomic_report(root/'items'/f"{record['figure_id']}.json",record)
            report['items'].append(record)
            print(json.dumps({k:record[k] for k in ('figure_id','status')},ensure_ascii=False),flush=True)
        except httpx.HTTPError:raise
        except Exception as exc:fail(record,exc,'classification_or_validation')
        progress('classification_and_validation')
    atomic_report(failures_path,failures)
    report['finished_at']=datetime.now(timezone.utc).isoformat()
    report['state']='completed_batch' if selected else ('paused_failed' if skipped and len(skipped)==len(set(ids)) else ('waiting_retry' if ids else 'idle'))
    stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')
    atomic_report(root/'batches'/(stamp+'.json'),report)
    atomic_report(root/'progress.json',{k:v for k,v in report.items() if k!='items'})
    return {k:v for k,v in report.items() if k!='items'}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--limit',type=int,default=20)
    p.add_argument('--ids',type=int,nargs='+')
    p.add_argument('--watch',action='store_true')
    p.add_argument('--skip-failed',action='store_true',help='Preserve failed jobs but skip their automatic retries; explicit --ids can retry them.')
    p.add_argument('--translation-model',default=get_settings().semantic_translation_model)
    p.add_argument('--classification-model',default=get_settings().semantic_classification_model)
    p.add_argument('--report-dir',type=Path,required=True)
    a=p.parse_args()
    if not 1<=a.limit<=100:p.error('limit must be 1..100')
    a.report_dir.mkdir(parents=True,exist_ok=True)
    with FileLock(str(get_settings().media_dir/'split_semantics_worker.lock'),timeout=0):
        while True:
            try:
                print(json.dumps(consume(a.limit,a.report_dir,a.ids,translation_model=a.translation_model,classification_model=a.classification_model,skip_failed=a.skip_failed)),flush=True)
            except (httpx.HTTPError,SemanticError) as exc:
                if not a.watch:raise
                print(json.dumps({'state':'waiting_for_local_provider','error':getattr(exc,'code',type(exc).__name__)}),flush=True)
                time.sleep(30)
                continue
            if not a.watch or a.ids:return
            time.sleep(15)

if __name__=='__main__':main()

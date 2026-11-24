"""Resumable local-only remaining-title batch. Existing classifications are preserved."""
import argparse
from collections import Counter
from datetime import datetime,timezone
import json
from pathlib import Path
import time
from sqlalchemy import select,or_,func
from app.core.config import get_settings
from app.core.database import SessionLocal
from app.models.entities import Figure
from app.services.product_semantics import source_of,source_hash
from app.services.local_title_translation import LocalTitleTranslator,apply_title,apply_classification
from scripts.product_semantics import atomic_report

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--report-dir',type=Path,required=True);p.add_argument('--limit',type=int)
    p.add_argument('--ids',type=int,nargs='+',help='Process these specific figure IDs in a new report directory')
    p.add_argument('--classify',action='store_true',help='Refresh missing classification fields with the same local model')
    p.add_argument('--commit',action='store_true');p.add_argument('--attempts',type=int,choices=(1,2),default=2)
    args=p.parse_args()
    settings=get_settings()
    if settings.semantic_provider!='ollama':p.error('SEMANTIC_PROVIDER=ollama required; remote APIs are never used')
    root=args.report_dir;root.mkdir(parents=True,exist_ok=True)
    targets=root/'targets.json'
    with SessionLocal() as db:
        if targets.exists():ids=json.loads(targets.read_text(encoding='utf-8'))
        else:
            query=select(Figure.id).order_by(Figure.id)
            query=query.where(Figure.id.in_(args.ids)) if args.ids else query.where(or_(Figure.name_ko.is_(None),Figure.name_ko==''))
            ids=list(db.scalars(query))
            if args.limit:ids=ids[:args.limit]
            atomic_report(targets,ids)
    translator=LocalTitleTranslator(settings);counts=Counter();classification_counts=Counter();started=time.monotonic();failures=0
    def progress(state,active=None):
        atomic_report(root/'progress.json',{'state':state,'total':len(ids),'finished':sum(counts.values()),'counts':dict(counts),
            'classification_counts':dict(classification_counts),'classify':args.classify,
            'active_figure_id':active,'local_model':translator.model,'title_inference_calls_this_run':translator.calls,
            'paid_api_called':False,'committed':args.commit,'elapsed_seconds':round(time.monotonic()-started,1),
            'updated_at':datetime.now(timezone.utc).isoformat()})
    try:
        progress('running')
        for fid in ids:
            path=root/(str(fid)+'.json')
            with SessionLocal() as db:
                f=db.get(Figure,fid)
                if not f:counts['deleted']+=1;continue
                already_translated=bool(f.name_ko and f.name_ko.strip())
                if already_translated and not args.classify:counts['already_translated']+=1;progress('running');continue
                source=source_of(f);digest=source_hash(source)
            progress('running',fid)
            record={'figure_id':fid,'source':source,'source_hash':digest,'committed':False,'paid_api_called':False}
            try:
                old=json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}
                if already_translated:
                    result={'name_ko':f.name_ko}
                elif (old.get('source_hash')==digest and old.get('result',{}).get('processing_fingerprint')==translator.fingerprint
                        and old.get('result',{}).get('model')==translator.model):
                    result=old['result']
                else:result=translator.translate(source,max_attempts=args.attempts)
                record['result']=result;atomic_report(path,record)
                if args.classify:
                    try:
                        classified=translator.extractor(source)
                        record['classification_result']=classified
                        if args.commit:
                            with SessionLocal() as db:
                                filled=apply_classification(db,fid,source,digest,classified,translator.model)
                            record['classification_filled']=filled
                            classification_counts['updated' if filled else 'unchanged']+=1
                        else:classification_counts['preview']+=1
                    except Exception as exc:
                        record['classification_error']=getattr(exc,'code',type(exc).__name__)
                        classification_counts['failed']+=1
                    atomic_report(path,record)
                if already_translated:
                    state='already_translated'
                elif result['name_ko']:
                    if args.commit:
                        with SessionLocal() as db:state=apply_title(db,fid,source,digest,result)
                        record['committed']=True
                    else:state='preview_translated'
                else:state='review'
                record['state']=state;counts[state]+=1;failures=0
            except Exception as exc:
                record['error']=getattr(exc,'code',type(exc).__name__);counts['failed']+=1;failures+=1
            atomic_report(path,record);progress('running')
            print(json.dumps({'id':fid,'state':record.get('state','failed'),'counts':dict(counts)},ensure_ascii=False),flush=True)
            if failures>=3:progress('blocked');return 2
        progress('completed_with_review' if counts['review'] or counts['failed'] or classification_counts['failed'] else 'completed');return 0
    finally:translator.close()

if __name__=='__main__':raise SystemExit(main())

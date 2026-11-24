"""Reapply improved local policy to original cached model output, without inference or paid calls."""
import argparse
from collections import Counter
from datetime import datetime,timezone
import json
from pathlib import Path
from app.core.database import SessionLocal
from app.core.config import get_settings
from app.models.entities import Figure
from app.models.semantics import ProductSemantics
from app.services.product_semantics import source_of,source_hash,validate_result,save_record
from app.services.local_semantic_lexicon import grounded_result
from app.services.verified_classification import merge_overrides
from scripts.product_semantics import atomic_report

def core(source):return {k:v for k,v in source.items() if k not in ('_rules_hash','_entity_candidates')}
def summary(fields):return {k:fields.get(k) for k in ('name_ko','franchise_ko','character_ko','figure_form','field_status')}

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--input-dir',type=Path,required=True);p.add_argument('--report-dir',type=Path,required=True)
    p.add_argument('--commit',action='store_true');p.add_argument('--ids',nargs='*',type=int);p.add_argument('--limit',type=int)
    p.add_argument('--ids-file',type=Path)
    args=p.parse_args();args.report_dir.mkdir(parents=True,exist_ok=True)
    counts=Counter();examples=[];root=args.report_dir;cache=get_settings().media_dir/'local_semantic_cache'
    paths=sorted(args.input_dir.glob('[0-9]*.json'),key=lambda path:int(path.stem))
    if args.ids_file:args.ids=json.loads(args.ids_file.read_text(encoding='utf-8'))
    if args.ids:paths=[path for path in paths if int(path.stem) in args.ids]
    if args.limit:paths=paths[:args.limit]
    def progress(state):
        data={'state':state,'total':len(paths),'counts':dict(counts),'changed_examples':examples[:100],
            'model_inference_calls':0,'paid_api_calls':0,'committed':args.commit,'updated_at':datetime.now(timezone.utc).isoformat()}
        atomic_report(root/'progress.json',data)
        print(json.dumps({k:v for k,v in data.items() if k!='changed_examples'}),flush=True)
    progress('running')
    for index,path in enumerate(paths,1):
        saved=json.loads(path.read_text(encoding='utf-8'));fid=int(path.stem)
        with SessionLocal() as db:
            f=db.get(Figure,fid);previous=db.get(ProductSemantics,fid)
            if not f:counts['deleted']+=1;continue
            was_title_missing=not f.name_ko
            source=source_of(f)
            if core(source)!=core(saved.get('source',{})):
                counts['source_changed']+=1;continue
            key=saved.get('provider_metadata',{}).get('cache_key','')
            raw_path=cache/(key+'.json')
            raw=None
            if key and raw_path.is_file():
                payload=json.loads(raw_path.read_text(encoding='utf-8'))
                if core(payload.get('identity',{}).get('source',{}))==core(source):raw=payload.get('model_result')
            if not isinstance(raw,dict):raw=saved.get('result')
            if not isinstance(raw,dict):
                from app.services.semantic_rules import korean
                if korean(source['name_original']):
                    raw={'name_ko':source['name_original'],'franchise':None,'characters':[],'figure_form':None}
                    counts['existing_korean_source_without_model']+=1
                else:counts['missing_model_response']+=1;continue
            result=grounded_result(source,raw)
            fields,issues=validate_result(source,result);digest=source_hash(source)
            if previous and previous.source_hash==digest:fields=merge_overrides(fields,previous.fields,digest)
            before=summary(previous.fields) if previous else {}
            after=summary(fields)
            if before==after and previous.source_hash==digest:
                counts['unchanged']+=1;continue
            # Never replace a successfully published field with an empty/rejected one.
            lost=[k for k in ('name_ko','franchise_ko','character_ko','figure_form')
                  if before.get(k) and not after.get(k)]
            if lost:
                counts['regression_blocked']+=1
                atomic_report(root/(str(fid)+'.json'),{'figure_id':fid,'before':before,'after':after,'lost_fields':lost,'committed':False})
                continue
            record={'figure_id':fid,'source':source,'source_hash':digest,'result':result,
                'model':saved.get('model','local-cached')+'+subject-policy-v2',
                'before':before,'after':after,'previous_publication':{'fields':previous.fields,'status':previous.status,
                    'model':previous.model,'issues':previous.issues,'source_hash':previous.source_hash} if previous else None,
                'raw_cache_key':key,'paid_api_called':False,'model_inference_called':False,'committed':False}
            atomic_report(root/(str(fid)+'.json'),record)
            if args.commit:
                record['status']=save_record(db,record);record['committed']=True
                atomic_report(root/(str(fid)+'.json'),record)
            counts['changed']+=1
            if not before.get('name_ko') and after.get('name_ko'):counts['recovered_titles']+=1
            if not before.get('character_ko') and after.get('character_ko'):counts['recovered_characters']+=1
            if was_title_missing and after.get('name_ko'):counts['filled_catalog_titles']+=1
            examples.append({'figure_id':fid,'original':source['name_original'],'before':before,'after':after})
        if index%50==0:progress('running')
    progress('completed')

if __name__=='__main__':main()

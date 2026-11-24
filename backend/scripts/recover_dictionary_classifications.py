"""Apply only additional validated dictionary fields; no model calls or weakened rules."""
import argparse,copy,json
from pathlib import Path
from app.core.config import get_settings
from app.core.database import SessionLocal
from app.models.entities import Figure
from app.models.semantics import ProductSemantics
from app.services.product_semantics import source_of,source_hash,save_record,validate_result
from app.services.split_semantics import grounded_dictionary
from app.services.local_semantic_lexicon import title_hints
from scripts.product_semantics import atomic_report

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--report-dir',type=Path,required=True);p.add_argument('--commit',action='store_true');a=p.parse_args()
    dictionary=json.loads((get_settings().data_dir/'reference/semantic_dictionary/catalog.json').read_text(encoding='utf-8'))
    summary={'examined':0,'improved':0,'skipped':0,'items':[],'dictionary':dictionary['fingerprint']}
    for path in sorted((a.report_dir/'items').glob('*.json')):
        old=json.loads(path.read_text(encoding='utf-8'))
        if not old.get('committed') or not old.get('result'):continue
        with SessionLocal() as db:
            f=db.get(Figure,old['figure_id']);profile=db.get(ProductSemantics,old['figure_id'])
            if not f or not profile:continue
            source=source_of(f);h=source_hash(source)
            if h!=old['source_hash'] or profile.source_hash!=h:continue
            summary['examined']+=1
            ground=grounded_dictionary(source,dictionary);title_hints(source,ground)
            proposed=copy.deepcopy(old['result'])
            for key in ('franchise','figure_form'):
                if ground[key]:proposed[key]=ground[key]
            originals={c['original'] for c in ground['characters']}
            proposed['characters']=ground['characters']+[c for c in proposed['characters'] if c['original'] not in originals and c.get('ko') not in {g['ko'] for g in ground['characters']}]
            fields,issues=validate_result(source,proposed)
            keys=('franchise_ko','character_ko','figure_form')
            prior=profile.fields
            protected=[k for k in keys if prior.get('field_status',{}).get(k)=='ready']
            improved=[k for k in keys if fields.get('field_status',{}).get(k)=='ready' and prior.get('field_status',{}).get(k)!='ready']
            if not improved or any(fields.get(k)!=prior.get(k) for k in protected):summary['skipped']+=1;continue
            record={**old,'source':source,'source_hash':h,'result':proposed,'fields':fields,'issues':issues,
                    'previous_model':old['model'],'model':'split-semantics-v6;dictionary-recovery='+dictionary['fingerprint']}
            entry={'figure_id':f.id,'improved':improved,'before':prior.get('classification_status')}
            if a.commit:
                atomic_report(a.report_dir/'dictionary_recovery'/(str(f.id)+'_before.json'),{'fields':prior,'model':profile.model})
                entry['status']=save_record(db,record)
                record['status']=entry['status'];atomic_report(path,record)
            entry['after']=fields.get('classification_status');summary['items'].append(entry);summary['improved']+=1
    atomic_report(a.report_dir/'dictionary_recovery_summary.json',summary)
    print(json.dumps({k:v for k,v in summary.items() if k!='items'}),flush=True)

if __name__=='__main__':main()

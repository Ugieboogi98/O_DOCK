"""Export existing curated dictionaries and currently validated exact title translations."""
import hashlib
import json
from pathlib import Path
from sqlalchemy import select
from app.core.config import get_settings
from app.core.database import SessionLocal
from app.models.entities import Figure
from app.models.semantics import ProductSemantics
from app.services.product_semantics import source_of,source_hash
from app.services.semantic_rules import glossary,FORMS
from app.services.local_semantic_lexicon import load
from scripts.product_semantics import atomic_report

def build():
    root=Path(__file__).resolve().parents[1]/'app/services'
    files=sorted(set(root.glob('*reference*.json'))|set(root.glob('local_semantic_*.json'))|{root/'classification_knowledge.json',root/'classification_wikipedia_anime.json',root/'product_semantics_glossary.json'})
    files+= [root/name for name in ('local_semantic_lexicon.py','reference_classifier.py','local_semantic_grounding.py','semantic_rules.py')]
    files.append(root/'semantic_recovery_dictionary.json')
    sources=[{'file':p.name,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]
    aliases=load()
    from app.services.reference_classifier import cached_knowledge
    knowledge=cached_knowledge()
    groups=[]
    for name in ('local_semantic_domain_aliases.json','local_semantic_domain_extension.json','semantic_recovery_dictionary.json'):
        groups+=json.loads((root/name).read_text(encoding='utf-8')).get('groups',[])
    path=get_settings().data_dir/'reference/semantic_dictionary/catalog.json'
    previous_titles=json.loads(path.read_text(encoding='utf-8')).get('titles',{}) if path.exists() else {}
    titles={};quarantined=0
    with SessionLocal() as db:
        figures=list(db.scalars(select(Figure)))
        profiles={p.figure_id:p for p in db.scalars(select(ProductSemantics))}
        for f in figures:
            p=profiles.get(f.id)
            context={'manufacturer':f.manufacturer.name,'franchise':f.franchise,'product_line':f.product_line.name if f.product_line else None}
            previous_title=previous_titles.get(f.name_original,{})
            retained=p and previous_title.get('ko')==p.fields.get('name_ko') and previous_title.get('context')==context
            if p and (not (p.model or '').startswith('split-semantics-') or retained) and p.fields.get('translation_status')=='ready' and p.source_hash==source_hash(source_of(f)) and p.fields.get('name_ko'):
                title=p.fields['name_ko']
                previous=titles.get(f.name_original)
                if previous and (previous.get('conflict') or previous.get('ko')!=title or previous.get('context')!=context):
                    titles[f.name_original]={'conflict':True}
                elif not titles.get(f.name_original,{}).get('conflict'):
                    titles[f.name_original]={'ko':title,'figure_id':f.id,'context':context,'provenance':'source_current_validated_profile'}
            elif f.name_ko:
                quarantined+=1
        makers=[{'original':f.manufacturer.name,'ko':f.manufacturer.name_ko} for f in figures]
    titles={k:v for k,v in titles.items() if not v.get('conflict')}
    data={'version':'split-dictionary-v2','sources':sources,'aliases':aliases,'knowledge':knowledge,'domain_groups':groups,'forms':FORMS,
          'manufacturers':list({m['original']:m for m in makers}.values()),'titles':titles,
          'unverified_catalog_titles_excluded':quarantined,
          'policy':'No automatic promotion of new model guesses. Character scope stays in source rules.'}
    data['fingerprint']=hashlib.sha256(json.dumps(data,sort_keys=True,ensure_ascii=False).encode()).hexdigest()
    path=get_settings().data_dir/'reference/semantic_dictionary/catalog.json'
    atomic_report(path.parent/'versions'/(data['fingerprint']+'.json'),data)
    atomic_report(path,data)
    print(json.dumps({'path':str(path),'source_files':len(files),'exact_titles':len(titles),'works':len(knowledge['works']),
                      'characters':len(knowledge['characters']),'unverified_excluded':quarantined}),flush=True)
    return data

if __name__=='__main__':build()

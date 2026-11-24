"""Freeze existing Korean catalog titles for name-spelling consistency; never claims human gold."""
import argparse,json
from pathlib import Path
from sqlalchemy import select
from app.core.database import SessionLocal
from app.models.entities import Figure
from app.services.semantic_rules import korean,validate_result
from app.services.local_semantic_subjects import title_key

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    titles={}
    with SessionLocal() as db:
        for title,translated,url in db.execute(select(Figure.name_original,Figure.name_ko,Figure.official_url).where(Figure.name_ko.is_not(None))):
            if not korean(translated):continue
            source={'name_original':title,'official_url':url}
            fields,_=validate_result(source,{'name_ko':translated,'franchise':None,'characters':[],'figure_form':None})
            if fields.get('translation_status')=='ready':titles[title_key(source)]=translated
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps({'provenance':'existing_catalog_publication_consistency_not_independent_gold','titles':titles},ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'title_pairs':len(titles),'db_written':False}))

if __name__=='__main__':main()

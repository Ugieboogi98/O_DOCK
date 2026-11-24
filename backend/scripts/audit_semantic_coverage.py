"""Read-only live coverage audit; no model/API calls and no secret configuration output."""
from collections import Counter
import json
from sqlalchemy import select,func,or_
from app.core.database import SessionLocal
from app.models.entities import Figure
from app.models.semantics import ProductSemantics
from app.services.product_semantics import current,source_of
from app.services.semantic_rules import rules_hash

def main():
    import argparse
    from pathlib import Path
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path);args=parser.parse_args()
    with SessionLocal() as db:
        total=db.scalar(select(func.count()).select_from(Figure))
        profiles=list(db.scalars(select(ProductSemantics)))
        stats={'total_products':total,'profiles':len(profiles),'record_status':dict(Counter(p.status for p in profiles)),
            'translation_status':dict(Counter(p.fields.get('translation_status','unknown') for p in profiles)),
            'has_validated_title':sum(bool(p.fields.get('name_ko')) for p in profiles),
            'has_character':sum(bool(p.fields.get('character_ko')) for p in profiles),
            'has_franchise':sum(bool(p.fields.get('franchise_ko')) for p in profiles),
            'outdated_rules':sum(p.source.get('_rules_hash')!=rules_hash() for p in profiles),
            'catalog_has_name_ko':db.scalar(select(func.count()).select_from(Figure).where(Figure.name_ko.is_not(None),Figure.name_ko!=''))}
        examples=[]
        for f in db.scalars(select(Figure).where(or_(Figure.name_original.contains('エマ'),Figure.name_original.contains('エンマ'),Figure.name_original.icontains('emma'),Figure.name_ko.contains('엠마')))):
            p=db.get(ProductSemantics,f.id)
            examples.append({'id':f.id,'name_original':f.name_original,'name_ko':f.name_ko,'official_url':f.official_url,
                'franchise':f.franchise,'character':f.character,'source':source_of(f),
                'profile_fields':p.fields if p else None,'issues':p.issues if p else None,'currently_visible':bool(current(db,f))})
        report={'coverage':stats,'emma_examples':examples}
        if args.output:
            args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
        print(json.dumps({'coverage':stats,'emma_examples':[{'id':r['id'],'original':r['name_original'],'display_title':r['name_ko'],
            'franchise':r['franchise'],'character':(r['profile_fields'] or {}).get('character_ko'),'visible':r['currently_visible']} for r in examples]},ensure_ascii=False,indent=2))

if __name__=='__main__':main()

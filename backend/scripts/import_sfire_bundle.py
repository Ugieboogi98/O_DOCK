"""Offline O_DOCK import. Default: preview. Run after other collection/translation jobs finish."""
import argparse, hashlib, json, re, shutil
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from app.core.paths import import_bundle_path

def valid_jan(j):
    return bool(re.fullmatch(r'\d{13}',j)) and sum(int(c)*(1 if i%2==0 else 3) for i,c in enumerate(j))%10==0

def validate(root):
    ps=json.loads((root/'products.json').read_text(encoding='utf-8'));seen=set()
    for p in ps:
        j=p['jan_code']
        if j in seen or not valid_jan(j):raise ValueError('duplicate or invalid JAN: '+j)
        seen.add(j)
        if p['official_url']!='https://s-fire.net/products/'+j:raise ValueError('source URL mismatch')
        for im in p['images']:
            f=(root/im['file']).resolve()
            if not f.is_relative_to(root) or not f.is_file():raise ValueError('missing or unsafe image path')
            if hashlib.sha256(f.read_bytes()).hexdigest()!=im['sha256']:raise ValueError('image hash mismatch: '+im['file'])
        if not (root/'documents'/f'{j}.txt').is_file():raise ValueError('missing document')
    return ps

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--bundle',type=Path,default=import_bundle_path('s_fire'))
    ap.add_argument('--report',type=Path,help='Write a commit report outside the read-only input bundle')
    ap.add_argument('--commit',action='store_true');ap.add_argument('--validate-only',action='store_true')
    ap.add_argument('--limit',type=int,default=0,help='0 = all products')
    a=ap.parse_args()
    if a.limit<0:ap.error('--limit must be >= 0')
    root=a.bundle.resolve();ps=validate(root)
    if a.validate_only:
        print(json.dumps({'validated_products':len(ps),'validated_images':sum(len(p['images']) for p in ps),'database_accessed':False}));return
    from sqlalchemy import select,text
    from app.core.database import SessionLocal
    from app.core.config import get_settings
    from app.services.import_pipeline import commit_import
    from app.models.entities import Manufacturer,ProductLine,Figure,FigureVariant,ProductImage,SourceDocument,ReleasePrice
    observed=datetime.fromisoformat(json.loads((root/'summary.json').read_text())['collected_at_utc'])
    summary={'mode':'COMMIT' if a.commit else 'PREVIEW','new_candidates':0,'matched':0,'saved':0,'review':0,'failed':0,'indexed':False,'translated':False}
    logs=[];lockdb=SessionLocal();locked=False
    try:
        if a.commit and lockdb.bind.dialect.name=='postgresql':
            locked=lockdb.scalar(text('SELECT pg_try_advisory_lock(74102881)'))
            if not locked:raise RuntimeError('another S-FIRE import is running')
        for p in ps[:a.limit or None]:
            j=p['jan_code'];url=p['official_url'];db=SessionLocal()
            try:
                matches=db.scalars(select(FigureVariant).where(FigureVariant.jan_code==j)).all()
                urls=db.scalars(select(Figure).where(Figure.official_url==url)).all()
                docs=db.scalars(select(SourceDocument).where(SourceDocument.url==url)).all()
                docvars=[db.get(FigureVariant,d.variant_id) for d in docs]
                ids={v.figure_id for v in matches+docvars if v is not None}|{f.id for f in urls}
                if len(ids)>1 or len(matches)>1:raise ValueError('REVIEW: ambiguous JAN/source match')
                f=db.get(Figure,next(iter(ids))) if ids else None;v=None
                if f:
                    if f.manufacturer.name!='SEGA':raise ValueError('REVIEW: manufacturer mismatch')
                    vs=db.scalars(select(FigureVariant).where(FigureVariant.figure_id==f.id)).all()
                    eligible=[v for v in vs if v.jan_code==j]
                    if len(eligible)==1:v=eligible[0]
                    elif len(vs)==1 and not vs[0].jan_code:v=vs[0]
                    else:raise ValueError('REVIEW: ambiguous variant')
                    summary['matched']+=1
                else:summary['new_candidates']+=1
                result={'jan':j,'action':'match' if f else 'create','figure_id':f.id if f else None,'name':p['name_original']}
                if a.commit:
                    if not f:
                        maker=db.scalar(select(Manufacturer).where(Manufacturer.name=='SEGA'))
                        if maker is None:
                            maker=Manufacturer(name='SEGA',name_ko='세가',official_url='https://s-fire.net/');db.add(maker);db.flush()
                        line=db.scalar(select(ProductLine).where(ProductLine.manufacturer_id==maker.id,ProductLine.name=='S-FIRE'))
                        if line is None:
                            line=ProductLine(manufacturer_id=maker.id,name='S-FIRE');db.add(line);db.flush()
                        spec=p['specifications'];mat=spec.get('specMaterial','');scale=re.search(r'\b1/\d+\b',mat);height=re.search(r'全高\s*約?\s*(\d+)\s*mm',spec.get('specSize',''))
                        f=Figure(manufacturer_id=maker.id,product_line_id=line.id,name_original=p['name_original'],name_ko=None,franchise=p['franchise'] or None,type='figure',scale=scale.group() if scale else None,height_mm=int(height.group(1)) if height else None,material=mat[:200] or None,official_url=url,quality='official_metadata',collected_at=observed)
                        db.add(f);db.flush();v=FigureVariant(figure_id=f.id,variant_key='source-page',jan_code=j);db.add(v);db.flush()
                    elif not v.jan_code:v.jan_code=j
                    known={im.source_url for im in db.scalars(select(ProductImage).where(ProductImage.variant_id==v.id))}
                    media=Path(get_settings().media_dir);media.mkdir(parents=True,exist_ok=True);added=0
                    for im in p['images']:
                        if im['source_url'] in known:continue
                        src=root/im['file'];name=im['sha256']+src.suffix.lower();dest=media/name
                        if dest.exists():
                            if hashlib.sha256(dest.read_bytes()).hexdigest()!=im['sha256']:raise ValueError('existing media hash mismatch')
                        else:shutil.copyfile(src,dest)
                        db.add(ProductImage(variant_id=v.id,image_url='/api/media/'+name,source_url=im['source_url'],usage_status='personal_local',license_evidence=None,checked_at=observed));known.add(im['source_url']);added+=1
                    if db.scalar(select(SourceDocument).where(SourceDocument.variant_id==v.id,SourceDocument.url==url)) is None:
                        body=(root/'documents'/f'{j}.txt').read_text(encoding='utf-8')
                        db.add(SourceDocument(variant_id=v.id,title=p['name_original'],url=url,source_type='official',language='ja',body=body,usage_status='factual_metadata_only',content_hash=hashlib.sha256(body.encode()).hexdigest(),collected_at=observed))
                    if p['price_amount'] is not None and db.scalar(select(ReleasePrice).where(ReleasePrice.variant_id==v.id,ReleasePrice.source_url==url,ReleasePrice.price_kind=='official_list')) is None:
                        db.add(ReleasePrice(variant_id=v.id,source_url=url,price_kind='official_list',currency='JPY',price_amount=Decimal(str(p['price_amount'])),tax_included=p['tax_included'],checked_at=observed))
                    staging=commit_import(db,[f])
                    for key,value in staging.items():summary[key]=summary.get(key,0)+value
                    summary['saved']+=1;result.update(figure_id=f.id,images_added=added)
                logs.append(result);print(json.dumps(result,ensure_ascii=False))
            except Exception as e:
                db.rollback();summary['review' if str(e).startswith('REVIEW:') else 'failed']+=1
                result={'jan':j,'error':str(e)};logs.append(result);print(json.dumps(result,ensure_ascii=False))
            finally:db.close()
    finally:
        if locked:lockdb.execute(text('SELECT pg_advisory_unlock(74102881)'))
        lockdb.close()
    if a.commit:
        stamp=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S_%fZ')
        report=a.report or get_settings().media_dir/'import_reports'/f'sfire_{stamp}.json'
        report.parent.mkdir(parents=True,exist_ok=True)
        report.write_text(json.dumps({'summary':summary,'results':logs},ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(summary))
    if summary['failed']:raise SystemExit(1)
if __name__=='__main__':main()

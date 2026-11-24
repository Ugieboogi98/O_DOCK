"""Offline TAITO import. Preview by default; --commit writes only local data."""
import argparse,hashlib,json,shutil,tempfile,os,re
from pathlib import Path
from decimal import Decimal
from datetime import datetime, timezone
from app.core.paths import import_bundle_path

ROOT=import_bundle_path('taito')

def load_validate(root):
    rows=json.loads((root/'products.json').read_text(encoding='utf-8'))
    urls=set();checked=set()
    for row in rows:
        url=row['source_url']
        if not re.fullmatch(r'https://taito-goods\.jp/shop/(?:[a-z0-9_-]+/)?g/g[\w-]+/',url) or url in urls:raise ValueError('INVALID_OR_DUPLICATE_URL')
        urls.add(url)
        if not row['name_original'].strip() or row['manufacturer']!='TAITO':raise ValueError('INVALID_IDENTITY')
        if row['currency']!='JPY':raise ValueError('UNEXPECTED_CURRENCY')
        if row['price_amount'] is not None and row['price_amount']<=0:raise ValueError('INVALID_PRICE')
        for image in row['images']:
            if 'path' not in image:continue
            path=(root/image['path']).resolve()
            if not path.is_relative_to(root.resolve()):raise ValueError('IMAGE_PATH_ESCAPE')
            if path in checked:continue
            if hashlib.sha256(path.read_bytes()).hexdigest()!=image['sha256']:raise ValueError('IMAGE_HASH_MISMATCH')
            checked.add(path)
    return rows,len(checked)

def import_rows(db, rows, root, media, commit):
    from app.services.import_pipeline import commit_import
    from sqlalchemy import select,text
    from app.models.entities import Manufacturer,Figure,FigureVariant,SourceDocument,ProductImage,ReleasePrice,ProductLine
    stats=dict(selected=len(rows),created=0,existing=0,review=0,failed=0,images_added=0,mode='COMMIT' if commit else 'PREVIEW')
    for n,row in enumerate(rows,1):
        try:
            if commit and db.bind.dialect.name=='postgresql':db.execute(text('SELECT pg_advisory_xact_lock(2026102203)'))
            maker=db.scalar(select(Manufacturer).where(Manufacturer.name=='TAITO'))
            f=db.scalar(select(Figure).where(Figure.official_url==row['source_url']))
            if f and (not maker or f.manufacturer_id!=maker.id):raise ValueError('MANUFACTURER_CONFLICT')
            if not f and maker:
                possible=db.scalar(select(Figure.id).outerjoin(FigureVariant).where(Figure.manufacturer_id==maker.id, (Figure.name_original==row['name_original']) | (FigureVariant.sku==row['sku'])).limit(1))
                if possible:
                    stats['review']+=1;db.rollback();print(json.dumps({'sku':row['sku'],'state':'review','existing_figure_id':possible}),flush=True);continue
            observed_at=datetime.fromisoformat(row['collected_at']) if row.get('collected_at') else datetime.now(timezone.utc)
            state='existing' if f else 'created'
            if not commit:
                stats[state]+=1;db.rollback();continue
            if maker is None:
                maker=Manufacturer(name='TAITO',name_ko='타이토',official_url='https://www.taito.co.jp/');db.add(maker);db.flush()
            if f is None:
                kind=row.get('type','goods')
                line=None
                if row.get('product_line'):
                    line=db.scalar(select(ProductLine).where(ProductLine.manufacturer_id==maker.id,ProductLine.name==row['product_line']))
                    if line is None:
                        line=ProductLine(manufacturer_id=maker.id,name=row['product_line']);db.add(line);db.flush()
                f=Figure(manufacturer_id=maker.id,name_original=row['name_original'],official_url=row['source_url'],type=kind,quality='official_metadata',collected_at=observed_at,franchise=row.get('franchise'),height_mm=row.get('height_mm'),scale=row.get('scale'),product_line_id=line.id if line else None);db.add(f);db.flush()
            variants=list(db.scalars(select(FigureVariant).where(FigureVariant.figure_id==f.id)))
            if len(variants)>1:raise ValueError('MULTIPLE_VARIANTS_REVIEW')
            v=variants[0] if variants else FigureVariant(figure_id=f.id,variant_key='source-page',sku=row['sku'],release_date=row.get('release_date'),release_precision='month' if row.get('release_date') else None)
            if not variants:db.add(v);db.flush()
            if v.sku and v.sku!=row['sku']:raise ValueError('SKU_CONFLICT')
            body=json.dumps({'name_original':row['name_original'],'categories':row.get('categories',{}),'specifications':row.get('specifications',{}),'description':row.get('description_original','')},ensure_ascii=False,indent=2)
            doc=db.scalar(select(SourceDocument).where(SourceDocument.variant_id==v.id,SourceDocument.url==row['source_url']))
            if doc is None:
                db.add(SourceDocument(variant_id=v.id,url=row['source_url'],title=row['name_original'],language='ja',source_type='official_detail',body=body,content_hash=hashlib.sha256(body.encode()).hexdigest(),usage_status='personal_local',collected_at=observed_at))
            price=db.scalar(select(ReleasePrice).where(ReleasePrice.variant_id==v.id,ReleasePrice.source_url==row['source_url'],ReleasePrice.price_kind=='official_list'))
            if price is None and row['price_amount'] is not None:db.add(ReleasePrice(variant_id=v.id,source_url=row['source_url'],price_kind='official_list',currency='JPY',price_amount=Decimal(row['price_amount']),checked_at=observed_at))
            added=0
            for image in row['images']:
                if 'path' not in image:continue
                img=db.scalar(select(ProductImage).where(ProductImage.variant_id==v.id,ProductImage.source_url==image['source_url']))
                if img is not None and img.usage_status=='duplicate_hidden':continue
                source=root/image['path'];target=media/source.name;media.mkdir(parents=True,exist_ok=True)
                if not target.exists() or hashlib.sha256(target.read_bytes()).hexdigest()!=image['sha256']:
                    fd,tmp=tempfile.mkstemp(dir=media,suffix='.tmp');os.close(fd)
                    try:shutil.copyfile(source,tmp);os.replace(tmp,target)
                    finally:Path(tmp).unlink(missing_ok=True)
                if img is None:
                    db.add(ProductImage(variant_id=v.id,source_url=image['source_url'],image_url='/api/media/'+target.name,usage_status='personal_local'));added+=1
                else:img.image_url='/api/media/'+target.name;img.usage_status='personal_local'
            staging=commit_import(db,[f])
            for key,value in staging.items():stats[key]=stats.get(key,0)+value
            stats[state]+=1;stats['images_added']+=added
            print(json.dumps({'progress':f'{n}/{len(rows)}','sku':row['sku'],'state':state,'figure_id':f.id,'images_added':added}),flush=True)
        except Exception as exc:
            db.rollback();stats['failed']+=1;print(json.dumps({'sku':row.get('sku'),'error':type(exc).__name__,'reason':str(exc)[:150] if isinstance(exc,ValueError) else 'DB or file error'}),flush=True)
    return stats

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--commit',action='store_true');p.add_argument('--validate-only',action='store_true')
    p.add_argument('--bundle',type=Path,default=ROOT)
    a=p.parse_args();root=a.bundle.resolve()
    rows,count=load_validate(root)
    print(json.dumps({'validated_products':len(rows),'validated_image_files':count,'database_accessed':False}),flush=True)
    if a.validate_only:return
    from app.core.database import SessionLocal
    from app.core.config import get_settings
    with SessionLocal() as db:result=import_rows(db,rows,root,get_settings().media_dir,a.commit)
    print(json.dumps(result),flush=True)
    # stdout only: never require write permission to the input bundle.
    if result['failed']:raise SystemExit(1)
if __name__=='__main__':main()

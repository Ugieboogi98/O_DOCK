"""Verify the bounded November 17 manufacturer import and its served detail data."""
import json
from pathlib import Path
from collections import Counter
import httpx
from sqlalchemy import select,func
from app.core.database import SessionLocal
from app.models.entities import Figure,FigureVariant,ProductImage,Manufacturer,CollectionJob,now
from app.rag.store import index_variant

def main():
    out = Path('/report/final_verification.json')
    report = {'baseline_total':6722,'baseline_max_id':6819,'manufacturers':{},'missing_images':[],'api_failures':[],'image_failures':[],'index_failures':[]}
    with SessionLocal() as db, httpx.Client(base_url='http://backend:8000',timeout=20) as client:
        figures = list(db.scalars(select(Figure).where(Figure.id>=6820).order_by(Figure.id)))
        report['new_products'] = len(figures)
        report['total_products'] = db.scalar(select(func.count(Figure.id)))
        report['goodsmile_total'] = db.scalar(select(func.count(Figure.id)).where(Figure.manufacturer_id==4))
        report['manufacturers'] = dict(Counter(f.manufacturer.name for f in figures))
        report['figure_ids'] = [f.id for f in figures]
        report['translated'] = sum(bool(f.name_ko) for f in figures)
        report['image_rows'] = 0
        for f in figures:
            r = client.get(f'/api/figures/{f.id}')
            if r.status_code != 200:
                report['api_failures'].append(f.id)
            images = list(db.scalars(select(ProductImage).where(ProductImage.variant_id.in_([v.id for v in f.variants]))))
            report['image_rows'] += len(images)
            if not images:
                report['missing_images'].append({'id':f.id,'manufacturer':f.manufacturer.name,'url':f.official_url})
            else:
                primary = client.get(images[0].image_url)
                if primary.status_code != 200 or not primary.headers.get('content-type','').startswith('image/'):
                    report['image_failures'].append(f.id)
            try:
                for variant in f.variants:
                    index_variant(db,f,variant)
            except Exception as exc:
                report['index_failures'].append({'id':f.id,'error':str(exc)[:150]})
        report['semantic_pending'] = db.scalar(select(func.count(CollectionJob.id)).where(CollectionJob.collector.in_(['catalog_semantics:'+str(f.id) for f in figures]),CollectionJob.status=='pending'))
        report['header_image_rows'] = db.scalar(select(func.count(ProductImage.id)).join(FigureVariant,ProductImage.variant_id==FigureVariant.id).where(FigureVariant.figure_id>=6820,ProductImage.source_url.startswith('https://tamashiiweb.com/assets/img/header/')))
        job = db.scalar(select(CollectionJob).where(CollectionJob.collector=='manual_manufacturer_pass:20261117').order_by(CollectionJob.id.desc()).limit(1))
        if job is None:
            job = CollectionJob(collector='manual_manufacturer_pass:20261117')
            db.add(job)
        job.status = 'completed'
        job.ended_at = now()
        job.count = len(figures)
        job.error_summary = json.dumps(report,ensure_ascii=False)
        db.commit()
    out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({k:v for k,v in report.items() if k not in ('figure_ids','missing_images')},ensure_ascii=False),flush=True)

if __name__ == '__main__':
    main()

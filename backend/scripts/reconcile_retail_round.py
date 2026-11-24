"""Reapply a collected round through current identity rules without another crawl."""
import argparse
import json
from pathlib import Path
from collections import Counter
from sqlalchemy import select
from app.core.database import SessionLocal
from app.models.retail import RetailListing
from app.services.retail_collection import save_offer
from app.services.collection_preferences import excluded_retail_product

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--report',type=Path,required=True)
    args=p.parse_args()
    report=json.loads(args.report.read_text(encoding='utf-8'))
    if report['state']!='completed':
        p.error('Collection must complete before reconciliation')
    counts=Counter()
    linked=Counter()
    with SessionLocal() as db:
        for row in report['items']:
            if excluded_retail_product(row):
                raise ValueError('EXCLUDED_MANUFACTURER_IN_ROUND')
            save_offer(db,row['retailer_code'],row)
            db.flush()
            listing=db.scalar(select(RetailListing).where(RetailListing.source_code==row['retailer_code'],RetailListing.external_product_id==row['external_product_id'],RetailListing.option_key==''))
            counts[row['retailer_code']]+=1
            linked[row['retailer_code']]+=int(listing.match_status=='MATCHED' and listing.catalog_variant_id is not None)
        db.commit()
    result={'state':'completed','observations':sum(counts.values()),'sources':dict(counts),'linked':dict(linked),'excluded_manufacturer_rows':0}
    args.report.with_name('verification.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False))

if __name__=='__main__':
    main()

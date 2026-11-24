import argparse
import json
from pathlib import Path
from app.services.domestic_collection_round import run_round

def main():
    p=argparse.ArgumentParser(description='Collect current product and price facts from all four retailers, excluding Hot Toys.')
    p.add_argument('--report-dir',type=Path,required=True)
    p.add_argument('--limit',type=int,default=20)
    p.add_argument('--commit',action='store_true')
    args=p.parse_args()
    if not 1<=args.limit<=100:
        p.error('--limit must be between 1 and 100')
    result=run_round(args.report_dir,args.limit,args.commit)
    print(json.dumps(result,ensure_ascii=False),flush=True)
    return 0 if result['state']=='completed' else 1

if __name__=='__main__':
    raise SystemExit(main())

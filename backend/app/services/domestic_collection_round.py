"""Collect a bounded current listing sample from all four requested retailers."""
from datetime import datetime, timezone
from pathlib import Path
import json
from app.services.collection_preferences import DOMESTIC_SOURCES

def run_round(report_dir, limit=20, commit=True):
    from scripts.preview_domestic_prices import collect_source
    from scripts.product_semantics import atomic_report
    report_dir = Path(report_dir)
    report_dir.mkdir(parents=True, exist_ok=True)
    output = report_dir / 'preview.json'
    report = {'state':'running','sources':{},'items':[],'errors':[],
              'dry_run':not commit,'database_written':False,
              'checked_at':datetime.now(timezone.utc).isoformat(),
              'excluded_manufacturers':['Hot Toys']}
    if output.exists():
        report = json.loads(output.read_text(encoding='utf-8'))
        report['state'] = 'running'
    atomic_report(output,report)
    for name in DOMESTIC_SOURCES:
        if report['sources'].get(name,{}).get('state') == 'completed':
            continue
        report['errors'] = [e for e in report['errors'] if e.get('source') != name]
        report['items'] = [r for r in report['items'] if r.get('retailer_code') != name]
        collect_source(name,limit,report,output,commit=commit)
    report['state'] = 'partial' if report['errors'] else 'completed'
    report['parsed'] = len(report['items'])
    atomic_report(output,report)
    return {'state':report['state'],'parsed':report['parsed'],
            'sources':{name:{key:data.get(key) for key in ('state','parsed','storage','excluded_manufacturer','errors')} for name,data in report['sources'].items()},
            'report_path':str(output)}

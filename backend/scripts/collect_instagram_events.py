"""Manual, gated official Instagram collection into isolated event review tables."""
import argparse
from collections import Counter
from datetime import datetime, timezone
import json
import logging
from pathlib import Path
from app.integrations.instagram.config import InstagramSettings
from app.integrations.instagram.probe import run_probe, TARGETS
from app.integrations.instagram.client import MetaClient, ProbeError
from app.integrations.instagram.collector import collect_account
from app.integrations.instagram.events import extract, default_works
from app.integrations.instagram.review import render
from app.integrations.instagram.event_identity import finalize


def collect(report_dir, commit=False, env_file=None):
    """Run one gated collection; returns (exit_code, summary). report_dir must not exist yet."""
    report_dir = Path(report_dir)
    for name in ('httpx','httpcore'):logging.getLogger(name).disabled = True
    report_dir.mkdir(parents=True, exist_ok=False)
    try:
        settings = InstagramSettings.from_local_env(env_file)
        gate = run_probe(settings, live=True)
    except Exception:
        return 2, {'error':'INVALID_CONFIGURATION_OR_GATE_REDACTED'}
    (report_dir/'availability.json').write_text(json.dumps(gate,ensure_ascii=False,indent=2),encoding='utf-8')
    if not gate.get('next_phase_eligible'):
        return 2, {'decision':'NO-GO','reason':gate.get('reason'),'posts_saved':0}
    engine = None
    if commit:
        from sqlalchemy import create_engine, inspect
        from app.core.config import get_settings
        from app.integrations.instagram.store import metadata
        engine = create_engine(get_settings().database_url, pool_pre_ping=True)
        if not all(inspect(engine).has_table(t) for t in metadata.tables):
            engine.dispose()
            return 2, {'error':'EVENT_MIGRATION_REQUIRED_NO_POSTS_COLLECTED'}
    client = MetaClient(settings)
    works = default_works()
    extractor = lambda text: extract(text, works=works)
    contextual_extractor = lambda row: finalize(extract(row['caption'],works=works,published_at=row['timestamp']),datetime.now(timezone.utc))
    report = {'collected_at':datetime.now(timezone.utc).isoformat(),'source_platform':'instagram',
        'mode':'MANUAL_COMMIT' if commit else 'PRIVATE_PREVIEW', 'paid_api_called':False,
        'automatic_collection_started':False, 'posts':[], 'sources':{}, 'error':None}
    def persist():
        (report_dir/'posts.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
        (report_dir/'review.html').write_text(render(report),encoding='utf-8')
    try:
        for username in TARGETS:
            if gate['targets'][username]['status'] != 'PASS':continue
            rows = collect_account(client,username,settings)
            fetched=len(rows)
            rows=[row for row in rows if contextual_extractor(row)['status']!='EXCLUDED_ENDED_BEFORE_COLLECTION']
            report['sources'][username]={'fetched':fetched,'excluded_ended':fetched-len(rows),'committed':False}
            report['posts'].extend({**row,'source_username':username,'candidate':contextual_extractor(row)} for row in rows)
            persist()  # Recoverable source snapshot before DB transaction.
            if engine is not None:
                from app.integrations.instagram.store import save_posts
                with engine.begin() as connection:
                    counts = save_posts(connection,username,rows,extractor,contextual_extractor)
                report['sources'][username].update(counts,committed=True)
                report['sources'][username]['excluded_ended']+=fetched-len(rows)
            persist()
    except ProbeError as exc:
        report['error']=exc.safe()
    except Exception:
        report['error']={'reason':'COLLECTION_OR_DB_FAILED_REDACTED','note':'Account transaction rolled back; retry using a new report directory.'}
    finally:
        report['collection_api_requests']=client.request_count
        client.close()
        if engine is not None:engine.dispose()
        report['summary']=dict(Counter(row['candidate']['status'] for row in report['posts']))
        persist()
    return (1 if report['error'] else 0), {'posts':len(report['posts']),'summary':report['summary'],
        'sources':report['sources'],'error':report['error'],'automatic_collection_started':False}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--env-file', type=Path)
    p.add_argument('--report-dir', type=Path, required=True, help='Private directory; not public web assets')
    p.add_argument('--commit', action='store_true', help='Explicit one-shot DB write; never enables scheduler')
    args = p.parse_args()
    code, summary = collect(args.report_dir, args.commit, args.env_file)
    print(json.dumps(summary, ensure_ascii=False))
    return code


if __name__=='__main__':
    raise SystemExit(main())

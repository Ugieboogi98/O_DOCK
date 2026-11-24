"""Read-only official API preflight/probe. No DB access or automatic collection."""
import argparse
import json
import logging
from pathlib import Path
from app.integrations.instagram.config import InstagramSettings
from app.integrations.instagram.probe import run_probe


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--env-file', type=Path, help='Local secret environment file; never pass secrets as CLI arguments')
    parser.add_argument('--report', type=Path, required=True)
    parser.add_argument('--live', action='store_true', help='Explicitly allow a few read-only Meta requests')
    args = parser.parse_args()
    if args.report.exists():
        parser.error('Use a new report file; previous evidence is never overwritten')
    # debug_token requires input_token as a query parameter. Never enable HTTP URL logging.
    for name in ('httpx', 'httpcore'):
        logging.getLogger(name).disabled = True
    try:
        settings = InstagramSettings.from_local_env(args.env_file)
    except Exception:
        print(json.dumps({'decision': 'NO-GO', 'reason': 'INVALID_CONFIGURATION_VALUES_REDACTED'}))
        return 2
    args.report.parent.mkdir(parents=True, exist_ok=True)
    # Verify storage before any external request without using the production report path.
    with args.report.open('x', encoding='utf-8') as stream:
        stream.write('{}')
    try:
        report = run_probe(settings, live=args.live)
    except Exception:
        # No traceback: provider URLs and third-party text can contain credentials.
        report = {'decision': 'NO-GO', 'reason': 'UNEXPECTED_PROBE_FAILURE_REDACTED', 'poc_success': False}
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False))
    return 0 if report.get('next_phase_eligible') else 2


if __name__ == '__main__':
    raise SystemExit(main())

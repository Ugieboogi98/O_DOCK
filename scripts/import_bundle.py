"""Uniform offline imports. Validation by default; no crawling or model calls."""
import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
COMPOSE = ['docker', 'compose', '-p', 'figure-archive-ai']


@dataclass(frozen=True)
class Bundle:
    manufacturer: str
    directory: str
    module: str
    root_option: str


BUNDLES = {name: Bundle(**entry) for name, entry in
           json.loads((ROOT / 'data/imports/registry.json').read_text(encoding='utf-8')).items()}


def command_for(name, mode, stamp, root=ROOT):
    bundle = BUNDLES[name]
    if mode == 'commit-missing' and name != 'furyu':
        raise ValueError('commit-missing is supported only for furyu')
    reports = root / 'backups/imports' / name
    command = COMPOSE + ['run', '--rm', '--no-deps', '-v', f'{reports.as_posix()}:/reports',
                         'backend', 'python', '-m', 'scripts.' + bundle.module,
                         bundle.root_option, '/data/imports/' + bundle.directory]
    if mode == 'validate':
        command += ['--validate-only']
    elif mode.startswith('commit'):
        command += ['--commit']
    if mode == 'commit-missing':
        command += ['--allow-missing-images']
    if name in ('furyu', 's_fire'):
        command += ['--report', f'/reports/{mode}_{stamp}.json']
    return command


def execute(command, **kwargs):
    subprocess.run(command, check=True, cwd=ROOT, **kwargs)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('manufacturer', choices=BUNDLES)
    parser.add_argument('mode', nargs='?', default='validate',
                        choices=('validate', 'preview', 'commit', 'commit-missing'))
    parser.add_argument('--dry-run', action='store_true', help='Print the command without creating files or invoking Docker')
    args = parser.parse_args()
    bundle = (ROOT / 'data/imports' / BUNDLES[args.manufacturer].directory).resolve()
    if not bundle.is_relative_to((ROOT / 'data/imports').resolve()):
        parser.error('Input bundle must stay within data/imports')
    if not bundle.is_dir():
        parser.error('Input bundle missing: ' + str(bundle))
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%f')
    try:
        command = command_for(args.manufacturer, args.mode, stamp)
    except ValueError as error:
        parser.error(str(error))
    if args.dry_run:
        print(json.dumps(command, ensure_ascii=False))
        return
    reports = ROOT / 'backups/imports' / args.manufacturer
    reports.mkdir(parents=True, exist_ok=True)
    if args.mode.startswith('commit'):
        execute(COMPOSE + ['stop', 'catalog-worker'])
        backup = f'/tmp/before_import_{stamp}.dump'
        execute(COMPOSE + ['exec', '-T', 'postgres', 'sh', '-c',
                          'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc -f ' + backup])
        execute(COMPOSE + ['exec', '-T', 'postgres', 'pg_restore', '--list', backup], stdout=subprocess.DEVNULL)
        execute(COMPOSE + ['cp', 'postgres:' + backup, str(reports / f'before_{stamp}.dump')])
    # Keep stdout as evidence even for importers that do not write their own report.
    with (reports / f'{args.mode}_{stamp}.log').open('w', encoding='utf-8') as log:
        process = subprocess.Popen(command, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                   text=True, encoding='utf-8', errors='replace')
        for line in process.stdout:
            print(line, end='')
            log.write(line)
            log.flush()
        if process.wait():
            raise SystemExit(process.returncode)


if __name__ == '__main__':
    main()

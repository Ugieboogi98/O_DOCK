"""Check active source imports, docs links and repository placement without DB access."""
import ast
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def check():
    errors = []
    for path in ROOT.iterdir():
        if path.is_dir() and re.fullmatch(r'[A-Z_]+_\d{8}', path.name):
            errors.append(f'Manufacturer bundle at root: {path.name}')
    for name in ('O_DOCK_IMAGE_DEDUP', 'migration_backup', 'korean_patch_backups', 'furyu_sample_sources.json', 'WORK_REPORT_20261110.md'):
        if (ROOT / name).exists():
            errors.append('Obsolete root path: ' + name)
    registry = json.loads((ROOT / 'data/imports/registry.json').read_text(encoding='utf-8'))
    for name, entry in registry.items():
        bundle = (ROOT / 'data/imports' / entry['directory']).resolve()
        if not bundle.is_relative_to((ROOT / 'data/imports').resolve()):
            errors.append('Bundle escapes input root: ' + name)
        if not (ROOT / 'backend/scripts' / (entry['module'] + '.py')).is_file():
            errors.append('Missing canonical importer: ' + name)
    python_files = list((ROOT / 'backend/app').rglob('*.py')) + list((ROOT / 'backend/scripts').rglob('*.py')) + list((ROOT / 'scripts').rglob('*.py'))
    for path in python_files:
        tree = ast.parse(path.read_text(encoding='utf-8-sig'))
        for node in ast.walk(tree):
            modules = ([node.module] if isinstance(node, ast.ImportFrom) and node.level == 0 else
                       [alias.name for alias in node.names] if isinstance(node, ast.Import) else [])
            for module in modules:
                if module and module.startswith(('app.', 'scripts.')):
                    target = ROOT / 'backend' / module.replace('.', '/')
                    if not target.with_suffix('.py').is_file() and not (target / '__init__.py').is_file():
                        errors.append(f'{path.relative_to(ROOT)}: missing {module}')
    front_files = [p for p in (ROOT / 'frontend/src').rglob('*') if p.suffix in ('.js', '.vue')]
    for path in front_files:
        for match in re.finditer(r'''(?:from\s*|import\s*\(\s*)['"](\.[^'"]+)['"]''', path.read_text(encoding='utf-8-sig')):
            target = (path.parent / match[1]).resolve()
            choices = (target, Path(str(target)+'.js'), Path(str(target)+'.vue'), Path(str(target)+'.json'), target/'index.js')
            if not any(candidate.is_file() for candidate in choices):
                errors.append(f'{path.relative_to(ROOT)}: missing {match[1]}')
    for relative in ('README.md', 'docs/PROJECT_STRUCTURE.md', 'data/imports/README.md', 'docs/reports/WORK_REPORT_20261110.md'):
        path = ROOT / relative
        if not path.is_file():
            errors.append('Missing entry document: ' + relative)
            continue
        for target in re.findall(r'\]\(([^)]+)\)', path.read_text(encoding='utf-8')):
            if not target.startswith(('http:', 'https:', '#')) and not (path.parent / target.split('#')[0]).exists():
                errors.append(f'{relative}: broken link {target}')
    tool = ROOT / 'tools/image_dedup'
    for line in (tool / 'SHA256SUMS.txt').read_text().splitlines():
        digest, name = line.split('  ', 1)
        if hashlib.sha256((tool / name).read_bytes()).hexdigest() != digest:
            errors.append('Image tool checksum mismatch: ' + name)
    return {'python_sources': len(python_files), 'frontend_sources': len(front_files), 'errors': errors}


if __name__ == '__main__':
    result = check()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(bool(result['errors']))

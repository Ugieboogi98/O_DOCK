"""Resolve external input locations from the shared, read-only bundle registry."""
import json
from app.core.config import get_settings


def import_bundle_path(name):
    root = (get_settings().data_dir / 'imports').resolve()
    registry = json.loads((root / 'registry.json').read_text(encoding='utf-8'))
    path = (root / registry[name]['directory']).resolve()
    if not path.is_relative_to(root) or path == root:
        raise ValueError('BUNDLE_PATH_OUTSIDE_IMPORTS')
    return path

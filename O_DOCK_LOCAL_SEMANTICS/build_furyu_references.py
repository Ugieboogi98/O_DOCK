"""Compile manually checked official directory names; no invented page checks."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SERVICES = ROOT / 'backend/app/services'


def build():
    observations = json.loads((SERVICES / 'furyu_directory_observations.json').read_text(encoding='utf-8'))
    labels = json.loads((SERVICES / 'classification_furyu_titles.json').read_text(encoding='utf-8'))
    series, checked = [], {}
    for row in observations['rows']:
        # Navigation/footer links are not licensed properties.
        entries = [e for e in row['entries'] if e['label'] not in ('クレーンゲーム景品について',) and '†' not in e['label']]
        row['entries'] = entries
        observed = {e['label'] for e in entries}
        mapped = set()
        for item in labels[row['kana']]:
            original, ko, *extra = item
            if original not in observed:
                raise ValueError('UNOBSERVED_DIRECTORY_TITLE: ' + original)
            aliases = [original] + (extra[0].split('|') if extra else [])
            series.append({'ko': ko, 'aliases': aliases, 'urls': [row['url']], 'characters': []})
            mapped.add(original)
        if observed != mapped:
            raise ValueError('UNMAPPED_DIRECTORY_TITLES: ' + repr(observed - mapped))
        checked[row['url']] = {'checked_at': observations['checked_at'],
            'sha256': hashlib.sha256('\n'.join(sorted(observed)).encode()).hexdigest(),
            'hash_scope': 'observed_directory_names_not_raw_html',
            'verification': 'web_tool_reference', 'terms': {name: True for name in observed}}
    (SERVICES / 'furyu_directory_observations.json').write_text(json.dumps(observations, ensure_ascii=False, indent=2), encoding='utf-8')
    (SERVICES / 'classification_furyu_reference_rules.json').write_text(json.dumps({'series': series, 'forms': []}, ensure_ascii=False, indent=2), encoding='utf-8')
    (SERVICES / 'classification_furyu_reference_checks.json').write_text(json.dumps(checked, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps({'rows': len(observations['rows']), 'directory_entries': len(series)}))


if __name__ == '__main__':
    build()

"""Read public Wikipedia language links; keep provenance and reject disambiguation."""
import argparse
from collections import defaultdict, Counter
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import time
import urllib.parse
import urllib.request


def request(language, params):
    url = f'https://{language}.wikipedia.org/w/api.php?' + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={'User-Agent': 'ODockClassificationResearch/1.0 (local catalog verification)'})
    with urllib.request.urlopen(req, timeout=40) as response:
        return json.load(response)


def seed_names(rows):
    seeds = defaultdict(set)
    for row in rows:
        source = row['source']
        for kind in ('franchise', 'character'):
            text = source.get(kind)
            if text and len(text) <= 120:
                seeds[text].add(kind)
        # Explicit work/subject introductions are candidates, not automatic labels.
        for n in range(3):
            text = (source.get(f'document_{n}') or '').split('※', 1)[0][:2000]
            for title in re.findall(r'[『「]([^』」\n]{2,90})[』」](?:より|から)', text):
                seeds[title].add('franchise')
        for title in re.findall(r'『([^』\n]{2,90})』', source['name_original']):
            seeds[title].add('franchise')
    return seeds


def fetch_batch(language, names):
    data = request(language, {'action': 'query', 'format': 'json', 'redirects': 1,
        'prop': 'langlinks|pageprops|info|categories', 'inprop': 'url', 'ppprop': 'disambiguation|wikibase_item',
        'lllang': 'ko', 'lllimit': 'max', 'cllimit': 'max', 'titles': '|'.join(names)})
    query = data.get('query', {})
    renamed = {r['from']: r['to'] for key in ('normalized', 'redirects') for r in query.get(key, [])}
    pages = {p['title']: p for p in query.get('pages', {}).values()}
    found = {}
    for name in names:
        title, visited = name, set()
        while title in renamed and title not in visited:
            visited.add(title)
            title = renamed[title]
        page = pages.get(title)
        if not page or 'missing' in page or 'disambiguation' in page.get('pageprops', {}):
            continue
        linked = page['title'] if language == 'ko' else next((p['*'] for p in page.get('langlinks', []) if p['lang'] == 'ko'), None)
        if not linked:
            continue
        found[name] = {'alias': name, 'canonical': page['title'], 'ko': linked,
            'language': language, 'url': page.get('fullurl'), 'wikidata': page.get('pageprops', {}).get('wikibase_item'),
            'categories': [r['title'] for r in page.get('categories', [])],
            'evidence': f"{page['title']} → {linked}", 'method': 'wikipedia_interlanguage_link'}
    return found


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalog', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--korean-titles', action='store_true')
    args = parser.parse_args()
    rows = json.loads(args.catalog.read_text(encoding='utf-8'))['records']
    seeds = seed_names(rows)
    if args.korean_titles:
        words = Counter(word for row in rows for word in re.findall(r'[가-힣]{2,15}', row['source']['name_original']))
        seeds = {name: {'franchise', 'character'} for name, frequency in words.most_common(300) if frequency >= 2}
    frequency = Counter(row['source'].get(field) for row in rows for field in ('franchise', 'character'))
    existing = json.loads(args.output.read_text(encoding='utf-8')) if args.output.exists() else {'entries': {}}
    entries = existing['entries']
    for language in (('ko',) if args.korean_titles else ('ja', 'en')):
        completed = set(existing.setdefault('checked', {}).get(language, []))
        names = sorted((name for name in seeds if name not in entries and name not in completed), key=lambda name: (-frequency[name], name))
        if language == 'en':
            names = [name for name in names if not re.search(r'[ぁ-ヿ一-龯가-힣]', name)]
        for index in range(0, len(names), 20):
            batch = names[index:index + 20]
            try:
                found = fetch_batch(language, batch)
            except Exception as exc:
                print(json.dumps({'language': language, 'batch': index, 'error': type(exc).__name__, 'http_status': getattr(exc, 'code', None)}), flush=True)
                if getattr(exc, 'code', None) in (429, 403):
                    raise SystemExit('Wikipedia request limit reached; preserve cache and resume later')
                continue
            for name, value in found.items():
                value['seed_roles'] = sorted(seeds[name])
                entries[name] = value
            completed.update(batch)
            existing['checked'][language] = sorted(completed)
            existing.update(entries=entries, seed_count=len(seeds), checked_at=datetime.now(timezone.utc).isoformat())
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding='utf-8')
            print(json.dumps({'language': language, 'batch': index, 'resolved_names': len(entries), 'seed_count': len(seeds)}), flush=True)
            time.sleep(5)


if __name__ == '__main__':
    main()

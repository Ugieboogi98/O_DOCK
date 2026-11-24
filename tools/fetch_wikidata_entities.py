"""Fetch anime/manga/game works and their characters with Korean and Japanese labels from Wikidata.

Writes backend/app/services/local_semantic_domain_wikidata.json in the dictionary "groups" format;
rebuild the dictionary afterwards (tools/run_split_semantics.py --build-dictionary).

Only public labels are requested. Wikimedia requires a contact in the User-Agent, so the project's
repository URL is sent (no personal data). Queries are small, sequential and paced.

  python tools/fetch_wikidata_entities.py [--max-works 0]
"""
import argparse
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'backend/app/services/local_semantic_domain_wikidata.json'
ENDPOINT = 'https://query.wikidata.org/sparql'
AGENT = 'O_DOCK-dictionary-builder/1.0 (https://github.com/Ugieboogi98/O_DOCK)'
# Direct instance-of types (no subclass paths: those time out on the public endpoint).
TYPES = {
    'Q63952888': 'anime',  # anime television series
    'Q1107': 'anime',      # anime
    'Q20650540': 'anime',  # anime film
    'Q21198342': 'manga',  # manga series
    'Q747381': 'novel',    # light novel
    'Q7889': 'game',       # video game
    'Q7058673': 'game',    # video game series
    'Q196600': None,       # media franchise
}
HANGUL = re.compile('[가-힣]')
JAPANESE_OR_LATIN = re.compile('[぀-ヿ一-鿿A-Za-z]')


def sparql(client, query, attempts=4):
    for attempt in range(attempts):
        r = client.get(ENDPOINT, params={'query': query, 'format': 'json'})
        if r.status_code == 200:
            time.sleep(1)  # pace requests
            return r.json()['results']['bindings']
        if r.status_code in (429, 500, 502, 503, 504):
            wait = int(r.headers.get('Retry-After', 0) or 0) or 10 * (attempt + 1)
            print(f'  retry in {wait}s (HTTP {r.status_code})', flush=True)
            time.sleep(wait)
            continue
        r.raise_for_status()
    raise RuntimeError('WIKIDATA_UNAVAILABLE')


def value(row, key):
    return (row.get(key) or {}).get('value')


def works_of_type(client, qid):
    q = f"""SELECT ?work ?ko ?ja ?en (GROUP_CONCAT(DISTINCT ?alt; separator='|') AS ?alts) WHERE {{
      ?work wdt:P31 wd:{qid} .
      ?work rdfs:label ?ko . FILTER(LANG(?ko)='ko')
      ?work rdfs:label ?ja . FILTER(LANG(?ja)='ja')
      OPTIONAL {{ ?work rdfs:label ?en . FILTER(LANG(?en)='en') }}
      OPTIONAL {{ ?work skos:altLabel ?alt . FILTER(LANG(?alt) IN ('ja','ko')) }}
    }} GROUP BY ?work ?ko ?ja ?en"""
    return sparql(client, q)


def characters_of(client, work_ids):
    values = ' '.join('wd:' + w for w in work_ids)
    q = f"""SELECT ?work ?char ?ko ?ja WHERE {{
      VALUES ?work {{ {values} }}
      ?char wdt:P1441 ?work .
      ?char rdfs:label ?ko . FILTER(LANG(?ko)='ko')
      ?char rdfs:label ?ja . FILTER(LANG(?ja)='ja')
    }}"""
    return sparql(client, q)


def usable(name, needs_hangul=False):
    if not name or name.startswith('Q') and name[1:].isdigit():
        return False
    if needs_hangul and not HANGUL.search(name):
        return False
    if not needs_hangul and not JAPANESE_OR_LATIN.search(name):
        return False
    return len(re.sub(r'\s+', '', name)) >= 2 or bool(re.fullmatch(r'[A-Za-z0-9]+', name))


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('--max-works', type=int, default=0, help='Limit works (testing); 0 = all')
    p.add_argument('--batch', type=int, default=150)
    a = p.parse_args()
    works = {}
    with httpx.Client(headers={'User-Agent': AGENT, 'Accept': 'application/sparql-results+json'}, timeout=90) as client:
        for qid, medium in TYPES.items():
            try:
                rows = works_of_type(client, qid)
            except Exception as exc:
                print(f'type {qid}: skipped ({type(exc).__name__})', flush=True)
                continue
            for row in rows:
                wid = value(row, 'work').rsplit('/', 1)[-1]
                ko, ja = value(row, 'ko'), value(row, 'ja')
                if not usable(ko, True) or not usable(ja):
                    continue
                w = works.setdefault(wid, {'qid': wid, 'work': ko, 'medium': medium, 'aliases': set()})
                w['medium'] = w['medium'] or medium
                w['aliases'] |= {x for x in [ja, value(row, 'en'), *((value(row, 'alts') or '').split('|'))] if x and usable(x)}
            print(f'type {qid}: {len(rows)} rows, {len(works)} works so far', flush=True)
        ids = list(works)[:a.max_works or None]
        chars = {}
        for i in range(0, len(ids), a.batch):
            batch = ids[i:i + a.batch]
            try:
                rows = characters_of(client, batch)
            except Exception as exc:
                print(f'characters {i}: skipped ({type(exc).__name__})', flush=True)
                continue
            for row in rows:
                wid = value(row, 'work').rsplit('/', 1)[-1]
                ko, ja = value(row, 'ko'), value(row, 'ja')
                if usable(ko, True) and usable(ja):
                    chars.setdefault(wid, {})[ja] = ko
            print(f'characters {i + len(batch)}/{len(ids)}: {sum(map(len, chars.values()))} so far', flush=True)
    # Works that share a Korean title (anime + manga + game of one franchise) become one group.
    groups = {}
    for wid in ids:
        w = works[wid]
        g = groups.setdefault(w['work'], {'work': w['work'], 'medium': w['medium'], 'aliases': set(), 'characters': {}, 'qids': []})
        g['medium'] = g['medium'] or w['medium']
        g['aliases'] |= w['aliases']
        g['qids'].append(wid)
        for ja, ko in chars.get(wid, {}).items():
            g['characters'].setdefault(ja, ko)
    # A Korean label shared by two characters of one work is ambiguous; keep both only if distinct.
    out = []
    for g in sorted(groups.values(), key=lambda x: x['work']):
        out.append({'work': g['work'], 'medium': g['medium'], 'aliases': sorted(g['aliases']),
                    'characters': [[[ja, ko], ko] for ja, ko in sorted(g['characters'].items())],
                    'wikidata': sorted(g['qids'])})
    stamp = datetime.now(timezone.utc).isoformat()
    OUT.write_text(json.dumps({'status': 'wikidata_labels', 'retrieved_at': stamp,
                               'provenance': 'Wikidata labels (CC0). Korean labels are community-maintained; curated groups win on conflict.',
                               'groups': out}, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    print(json.dumps({'works': len(out), 'with_characters': sum(1 for g in out if g['characters']),
                      'characters': sum(len(g['characters']) for g in out), 'path': str(OUT)}, ensure_ascii=False))


if __name__ == '__main__':
    sys.exit(main())

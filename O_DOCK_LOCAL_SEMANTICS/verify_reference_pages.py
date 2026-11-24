"""Verify reference terms on official pages; retain only hashes/short facts."""
import argparse
from datetime import datetime, timezone
import hashlib
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import time
import unicodedata
import urllib.request


def normalize(value):
    return re.sub(r'\s+', '', unicodedata.normalize('NFKC', value)).casefold()


class Text(HTMLParser):
    def __init__(self):
        super().__init__()
        self.parts = []
        self.ignore = 0
    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'):
            self.ignore += 1
        if not self.ignore:
            self.parts.extend(value for key, value in attrs if key in ('alt', 'title') and value)
    def handle_endtag(self, tag):
        if tag in ('script', 'style'):
            self.ignore = max(0, self.ignore - 1)
    def handle_data(self, value):
        if not self.ignore:
            self.parts.append(value)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--rules', type=Path, required=True)
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    rules = json.loads(args.rules.read_text(encoding='utf-8'))
    extra_path = args.rules.with_name('classification_extra_reference_rules.json')
    if extra_path.exists():
        extra = json.loads(extra_path.read_text(encoding='utf-8'))
        for key in ('series', 'forms'):
            rules[key].extend(extra[key])
    targets = {}
    anime_path = args.rules.with_name('classification_anime_reference_rules.json')
    if anime_path.exists():
        extra = json.loads(anime_path.read_text(encoding='utf-8'))
        for key in ('series', 'forms'):
            rules[key].extend(extra[key])
    for series in rules['series']:
        terms = list(series['aliases']) + [alias for aliases, _ in series['characters'] for alias in aliases.split('|')]
        for url in series['urls']:
            targets.setdefault(url, set()).update(terms)
    for form in rules['forms']:
        targets.setdefault(form['url'], set()).add(form['quote'])
    cache = json.loads(args.output.read_text(encoding='utf-8')) if args.output.exists() else {}
    for url, terms in targets.items():
        if url in cache and cache[url].get('encoding') and set(terms).issubset(cache[url].get('terms', {})):
            continue
        if cache.get(url, {}).get('http_status') in (403, 404):
            continue
        try:
            request = urllib.request.Request(url, headers={'User-Agent': 'ODockCatalogVerification/1.0'})
            with urllib.request.urlopen(request, timeout=30) as response:
                raw = response.read(4_000_000)
                charset = response.headers.get_content_charset() or 'utf-8'
            candidates = []
            for encoding in dict.fromkeys((charset, 'utf-8', 'shift_jis', 'euc_jp')):
                parser = Text()
                try:
                    parser.feed(raw.decode(encoding, errors='replace'))
                except LookupError:
                    continue
                text = normalize(html.unescape(' '.join(parser.parts)))
                candidates.append((sum(normalize(term) in text for term in terms), encoding, text))
            _, charset, text = max(candidates, key=lambda row: row[0])
            cache[url] = {'checked_at': datetime.now(timezone.utc).isoformat(),
                'sha256': hashlib.sha256(raw).hexdigest(), 'encoding': charset,
                'terms': {term: normalize(term) in text for term in sorted(terms)}}
            print(json.dumps({'url': url, 'verified_terms': sum(cache[url]['terms'].values())}), flush=True)
        except Exception as exc:
            cache[url] = {'error': type(exc).__name__, 'http_status': getattr(exc, 'code', None), 'terms': {}}
            print(json.dumps({'url': url, 'error': cache[url]['error']}), flush=True)
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(cache, ensure_ascii=False, indent=2), encoding='utf-8')
        time.sleep(1)


if __name__ == '__main__':
    main()

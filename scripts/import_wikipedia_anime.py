"""Refresh the attributed TV anime reference supplement (no database writes)."""
import hashlib
import argparse
import json
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
import re
import unicodedata
import time
from urllib.error import HTTPError
from urllib.parse import urlencode, quote, unquote
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
BASE = '일본의_텔레비전_애니메이션_목록'
OUT = ROOT / 'data/reference/wikipedia_anime'


def api(**params):
    url = 'https://ko.wikipedia.org/w/api.php?' + urlencode(dict(format='json', **params))
    for attempt in range(6):
        time.sleep(2)
        try:
            with urlopen(Request(url, headers={'User-Agent': 'ODockCatalog/1.0 (reference import)'}), timeout=60) as response:
                result = json.load(response)
            break
        except HTTPError as error:
            if error.code not in (429, 502, 503) or attempt == 5:
                raise
            time.sleep(10)
    if 'error' in result:
        raise RuntimeError(result['error'])
    return result


class Titles(HTMLParser):
    def __init__(self):
        super().__init__()
        self.rows, self.items = [], []
        self.started = True
        self.table = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'h2':
            self.started = True
        if tag == 'table':
            self.table += 1
        if self.table or not self.started:
            return
        if tag == 'li':
            self.items.append({'text': '', 'target': None})
        if tag == 'a' and self.items and not self.items[-1]['target']:
            if attrs.get('href', '').startswith('/wiki/') and 'new' not in attrs.get('class', '').split():
                self.items[-1]['target'] = attrs.get('title')

    def handle_data(self, data):
        if self.items and not self.table:
            self.items[-1]['text'] += data

    def handle_endtag(self, tag):
        if tag == 'table':
            self.table -= 1
        if tag == 'li' and self.items and not self.table:
            self.rows.append(self.items.pop())


def key(text):
    return re.sub(r'\s+', '', unicodedata.normalize('NFKC', text)).casefold()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--refresh', action='store_true', help='Download current pages instead of reusing snapshots')
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    checked = datetime.now(timezone.utc).isoformat()
    previous = json.loads((OUT / 'catalog.json').read_text(encoding='utf-8')) if not args.refresh and (OUT / 'catalog.json').exists() else {}
    old_pages = {p['title']: p for p in previous.get('pages', [])}
    records, pages = {}, []
    names = [BASE + '/' + c for c in 'ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎ'] + [BASE + '/알파벳']
    for index, name in enumerate(names):
        snapshot = OUT / f'{index:02d}.html'
        if name in old_pages and snapshot.exists():
            page = {'revid': old_pages[name]['revision']}
            html = snapshot.read_text(encoding='utf-8')
        else:
            page = api(action='parse', page=name, prop='text|revid', redirects=1)['parse']
            html = page['text']['*']
        (OUT / f'{index:02d}.html').write_text(html, encoding='utf-8')
        url = 'https://ko.wikipedia.org/w/index.php?' + urlencode({'oldid': page['revid']})
        parser = Titles()
        parser.feed(html)
        count = 0
        for row in parser.rows:
            title = re.sub(r'\[\d+\]', '', row['text']).strip()
            if not title or title == '없음' or '목록' in title or '내용을 추가' in title:
                continue
            if key(title) not in records:
                records[key(title)] = {'ko': title, 'aliases': [title], 'priority': 0,
                    'reference': {'url': url, 'evidence': title, 'checked_at': checked,
                                  'sha256': hashlib.sha256(html.encode()).hexdigest(),
                                  'verification': 'wikipedia_list_snapshot'},
                    'article': row['target']}
            count += 1
        pages.append({'title': name, 'url': url, 'revision': page['revid'], 'items': count})
        print(f'page {index + 1}/15: {count}', flush=True)
    # Only use explicit language links; never guess Japanese translations.
    targets = list(dict.fromkeys(r['article'] for r in records.values() if r['article']))
    japanese = {unquote(r['reference']['language_link_url'].split('/wiki/', 1)[1]).replace('_', ' '): r['aliases'][1]
                for r in previous.get('works', []) if r['reference'].get('language_link_url')}
    targets = [t for t in targets if t not in japanese]
    for offset in range(0, len(targets), 50):
        result = api(action='query', titles='|'.join(targets[offset:offset + 50]),
                     prop='langlinks', lllang='ja', lllimit='max', redirects=1)['query']
        mappings = {r['from']: r['to'] for r in result.get('normalized', []) + result.get('redirects', [])}
        by_title = {p['title']: p for p in result['pages'].values()}
        for title in targets[offset:offset + 50]:
            resolved, seen = title, set()
            while resolved in mappings and resolved not in seen:
                seen.add(resolved)
                resolved = mappings[resolved]
            links = by_title.get(resolved, {}).get('langlinks', [])
            if links:
                japanese[title] = links[0]['*']
        print(f'language links {min(offset + 50, len(targets))}/{len(targets)}', flush=True)
    for record in records.values():
        target = record.pop('article')
        if target in japanese:
            record['aliases'].append(japanese[target])
            record['reference']['language_link_url'] = 'https://ko.wikipedia.org/wiki/' + quote(target.replace(' ', '_'))
    payload = {'source': 'https://ko.wikipedia.org/wiki/' + BASE, 'checked_at': checked,
               'license': 'CC-BY-SA-4.0', 'pages': pages, 'works': list(records.values())}
    (OUT / 'catalog.json').write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (ROOT / 'backend/app/services/classification_wikipedia_anime.json').write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'works': len(records), 'japanese_aliases': sum(len(r['aliases']) > 1 for r in records.values())}))


if __name__ == '__main__':
    main()

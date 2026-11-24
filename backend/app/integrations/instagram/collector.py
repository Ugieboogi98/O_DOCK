"""Bounded manual collection after a fresh official API availability gate."""
from datetime import datetime
import re
from urllib.parse import urlsplit
from .client import ProbeError


def minimal_post(value):
    if not isinstance(value, dict) or not re.fullmatch(r'\d{1,100}', str(value.get('id', ''))):
        raise ProbeError('INVALID_POST_ID')
    caption = value.get('caption')
    if caption is not None and (not isinstance(caption, str) or len(caption) > 30000):
        raise ProbeError('INVALID_CAPTION')
    url = value.get('permalink', '')
    if not isinstance(url, str):
        raise ProbeError('INVALID_POST_URL')
    parsed = urlsplit(url)
    if (parsed.scheme != 'https' or parsed.hostname not in ('www.instagram.com', 'instagram.com')
        or parsed.username or parsed.password or parsed.port not in (None, 443)
        or not re.fullmatch(r'/(?:p|reel|tv)/[A-Za-z0-9_-]+/?', parsed.path)):
        raise ProbeError('INVALID_POST_URL')
    stamp = value.get('timestamp')
    try:
        published = datetime.fromisoformat(stamp.replace('Z', '+00:00'))
        if published.tzinfo is None:
            raise ValueError()
    except (TypeError, ValueError, AttributeError):
        raise ProbeError('INVALID_PUBLISHED_AT') from None
    media_type = value.get('media_type')
    if media_type not in ('IMAGE', 'VIDEO', 'CAROUSEL_ALBUM'):
        raise ProbeError('INVALID_MEDIA_TYPE')
    return {'id': str(value['id']), 'caption': caption or '',
            'permalink': 'https://www.instagram.com' + parsed.path,
            'timestamp': published.isoformat(), 'media_type': media_type}


def collect_account(client, username, settings):
    rows, seen, cursors, after = [], set(), set(), None
    for _ in range(settings.instagram_collection_page_limit):
        payload, _status = client.discovery(username, after=after)
        discovery = payload.get('business_discovery')
        if not isinstance(discovery, dict) or discovery.get('username', '').casefold() != username:
            raise ProbeError('DISCOVERY_SCHEMA_OR_USERNAME_MISMATCH')
        media = discovery.get('media', {})
        items = media.get('data') if isinstance(media, dict) else None
        if not isinstance(items, list) or len(items) > settings.instagram_collection_media_limit:
            raise ProbeError('MEDIA_LIMIT_OR_SCHEMA_INVALID')
        for item in items:
            row = minimal_post(item)
            if row['id'] not in seen:
                rows.append(row)
                seen.add(row['id'])
        paging = media.get('paging', {})
        # Never fetch paging.next: it may contain a token or an untrusted host.
        cursor = paging.get('cursors', {}).get('after') if isinstance(paging, dict) else None
        if not items or not paging.get('next') or not cursor or cursor in cursors:
            break
        if not isinstance(cursor, str) or not re.fullmatch(r'[A-Za-z0-9_+=/\-]{1,1500}', cursor):
            raise ProbeError('UNSAFE_PAGING_CURSOR')
        cursors.add(cursor)
        after = cursor
    return rows

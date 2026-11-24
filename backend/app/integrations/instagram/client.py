"""Strictly allowlisted Meta GETs. Never return exception URLs or error messages."""
import re
import time
import httpx


class ProbeError(Exception):
    def __init__(self, code, status=None, meta_code=None, meta_subcode=None):
        super().__init__(code)
        self.code, self.status = code, status
        self.meta_code, self.meta_subcode = meta_code, meta_subcode

    def safe(self):
        return {'status': 'FAIL', 'reason': self.code, 'http_status': self.status,
                'meta_code': self.meta_code, 'meta_subcode': self.meta_subcode}


class MetaClient:
    def __init__(self, settings, *, transport=None, sleep=time.sleep):
        # Business Discovery is probed only on the documented Facebook Graph route.
        # Do not guess that Unified Login / Instagram Login has the same capabilities.
        if settings.meta_graph_base_url.rstrip('/') != 'https://graph.facebook.com':
            raise ProbeError('LOGIN_HOST_ROUTE_UNVERIFIED')
        if not re.fullmatch(r'v\d{1,2}\.\d+', settings.meta_graph_api_version):
            raise ProbeError('EXPLICIT_SUPPORTED_API_VERSION_REQUIRED')
        self.settings, self.sleep = settings, sleep
        self.request_count = 0
        self.http = httpx.Client(base_url=settings.meta_graph_base_url.rstrip('/'),
            transport=transport, timeout=20, follow_redirects=False, trust_env=False)

    def close(self):
        self.http.close()

    def get(self, resource, params, token=None):
        if resource != 'debug_token' and resource != self.settings.meta_ig_user_id:
            raise ProbeError('RESOURCE_NOT_ALLOWED')
        if resource != 'debug_token' and not re.fullmatch(r'\d+', resource):
            raise ProbeError('NUMERIC_SELF_ACCOUNT_ID_REQUIRED')
        bearer = token or self.settings.meta_access_token.get_secret_value()
        if not bearer:
            raise ProbeError('ACCESS_TOKEN_REQUIRED')
        for attempt in range(3):
            try:
                self.request_count += 1
                with self.http.stream('GET', f'/{self.settings.meta_graph_api_version}/{resource}',
                    params=params, headers={'Authorization': 'Bearer ' + bearer}) as response:
                    status = response.status_code
                    raw = bytearray()
                    for chunk in response.iter_bytes():
                        raw.extend(chunk)
                        if len(raw) > 2_000_000:
                            raise ProbeError('RESPONSE_TOO_LARGE', status)
                    import json
                    try:
                        data = json.loads(raw)
                    except (ValueError, UnicodeError):
                        data = None
                    if status == 429 or 500 <= status < 600:
                        if attempt < 2:
                            delay = 2 ** attempt
                            try:
                                delay = max(delay, float(response.headers.get('Retry-After', 0)))
                            except ValueError:
                                pass
                            if delay > 30:
                                raise ProbeError('RETRY_LATER', status)
                            self.sleep(delay)
                            continue
                    if not isinstance(data, dict):
                        raise ProbeError('INVALID_RESPONSE_SCHEMA', status)
                    error = data.get('error')
                    if status != 200 or error:
                        error = error if isinstance(error, dict) else {}
                        code = error.get('code') if type(error.get('code')) is int else None
                        subcode = error.get('error_subcode') if type(error.get('error_subcode')) is int else None
                        reason = ('TOKEN_INVALID_OR_EXPIRED' if code == 190 or status == 401 else
                                  'PERMISSION_DENIED' if status == 403 or code in (10, 200) else
                                  'DISCOVERY_FIELD_OR_OBJECT_UNAVAILABLE' if code == 100 else
                                  'RATE_LIMITED' if status == 429 else 'META_REQUEST_FAILED')
                        raise ProbeError(reason, status, code, subcode)
                    return data, status
            except httpx.HTTPError:
                if attempt < 2:
                    self.sleep(2 ** attempt)
                    continue
                raise ProbeError('NETWORK_OR_TIMEOUT') from None
        raise ProbeError('RETRIES_EXHAUSTED')

    def debug_token(self):
        s = self.settings
        return self.get('debug_token', {'input_token': s.meta_access_token.get_secret_value()},
                        token=s.meta_app_id + '|' + s.meta_app_secret.get_secret_value())

    def own_account(self):
        return self.get(self.settings.meta_ig_user_id, {'fields': 'id,username'})

    def discovery(self, username, after=None, include_images=False):
        if username not in ('duex.official', 'anique.jp', 'akplaza_hongdae'):
            raise ProbeError('TARGET_NOT_ALLOWLISTED')
        if after is not None and not re.fullmatch(r'[A-Za-z0-9_+=/\-]{1,1500}', after):
            raise ProbeError('UNSAFE_PAGING_CURSOR')
        paging = ('.after(' + after + ')') if after else ''
        image_fields = ',media_url,thumbnail_url,children.limit(20){id,media_type,media_url,thumbnail_url}' if include_images else ''
        fields = ('business_discovery.username(' + username + '){id,username,media_count,media.limit('
                  + str(self.settings.instagram_collection_media_limit) + ')' + paging
                  + '{id,caption,timestamp,permalink,media_type' + image_fields + '}}')
        return self.get(self.settings.meta_ig_user_id, {'fields': fields})

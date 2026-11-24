"""No DB imports, persistence, schedulers, model calls or media downloads."""
import re
import time
from datetime import datetime, timezone
from .client import MetaClient, ProbeError

TARGETS = ('duex.official', 'anique.jp', 'akplaza_hongdae')


def run_probe(settings, *, live=False, client_factory=MetaClient, now=time.time):
    report = {'checked_at': datetime.now(timezone.utc).isoformat(),
        'phase': 'AVAILABILITY_POC', 'mode': 'LIVE_READ_ONLY' if live else 'PREFLIGHT_NO_NETWORK',
        'login_path': 'Unified Login (user reported; console not independently verified)',
        'app_created': 'USER_REPORTED',
        'config_created': 'PRESENT_UNVERIFIED' if settings.meta_ig_login_config_id else 'UNKNOWN',
        'token_valid': 'UNKNOWN', 'self_account': {'status': 'NOT_RUN'},
        'discovery_supported': 'UNKNOWN', 'poc_success': False, 'decision': 'NO-GO',
        'db_written': False, 'paid_api_called': False, 'api_requests': 0,
        'automatic_collection_started': False,
        'targets': {u: {'status': 'UNKNOWN', 'source_status': 'MANUAL_LINK_ONLY',
                        'url': f'https://www.instagram.com/{u}/'} for u in TARGETS}}
    required = ('meta_app_id', 'meta_app_secret', 'meta_access_token', 'meta_ig_user_id', 'meta_graph_api_version')
    def present(name):
        value = getattr(settings, name)
        return bool(value.get_secret_value() if hasattr(value, 'get_secret_value') else value)
    missing = [name.upper() for name in required if not present(name)]
    report['missing_configuration'] = missing
    if missing:
        report['reason'] = 'CONFIGURATION_INCOMPLETE_NO_REQUEST_SENT'
        return report
    if not re.fullmatch(r'\d+', settings.meta_app_id) or not re.fullmatch(r'\d+', settings.meta_ig_user_id):
        report['reason'] = 'NUMERIC_APP_AND_SELF_ACCOUNT_IDS_REQUIRED'
        return report
    if settings.meta_access_token.get_secret_value() == settings.meta_ig_login_config_id:
        report['reason'] = 'CONFIGURATION_ID_IS_NOT_ACCESS_TOKEN'
        return report
    try:
        client = client_factory(settings)
    except ProbeError as exc:
        report['reason'] = exc.code
        return report
    try:
        if not live:
            report['reason'] = 'LIVE_FLAG_REQUIRED_FOR_NETWORK_PROBE'
            return report
        report['api_requests'] += 1
        payload, status = client.debug_token()
        debug = payload.get('data')
        if not isinstance(debug, dict):
            raise ProbeError('INVALID_TOKEN_DEBUG_SCHEMA', status)
        safe = {k: debug[k] for k in ('is_valid', 'type', 'issued_at', 'expires_at', 'data_access_expires_at')
                if type(debug.get(k)) in (bool, int) or k == 'type' and debug.get(k) in ('USER', 'PAGE', 'SYSTEM_USER')}
        scopes = debug.get('scopes')
        safe['scopes'] = [s for s in scopes if isinstance(s, str) and re.fullmatch(r'[a-z_]+', s)] if isinstance(scopes, list) else []
        safe['http_status'] = status
        safe['app_id_matches'] = str(debug.get('app_id')) == settings.meta_app_id
        report['token_check'] = safe
        if debug.get('is_valid') is not True or not safe['app_id_matches']:
            raise ProbeError('TOKEN_INVALID_OR_WRONG_APP', status)
        if debug.get('type') not in ('USER', 'PAGE', 'SYSTEM_USER'):
            raise ProbeError('TOKEN_TYPE_UNVERIFIED', status)
        if not isinstance(scopes, list) or not scopes:
            raise ProbeError('TOKEN_PERMISSIONS_UNVERIFIED', status)
        for key in ('expires_at', 'data_access_expires_at'):
            value = debug.get(key)
            if type(value) is not int or value < 0:
                raise ProbeError('TOKEN_EXPIRY_UNVERIFIED', status)
            if value and value <= now():
                raise ProbeError('TOKEN_EXPIRED', status)
        report['token_valid'] = 'PASS_DEBUG_ONLY'
        report['api_requests'] += 1
        own, status = client.own_account()
        if str(own.get('id')) != settings.meta_ig_user_id or not isinstance(own.get('username'), str):
            raise ProbeError('SELF_ACCOUNT_SCHEMA_OR_ID_MISMATCH', status)
        report['self_account'] = {'status': 'PASS', 'http_status': status, 'fields': ['id', 'username']}
        report['token_valid'] = 'PASS'
        blocked = False
        for username in TARGETS:
            try:
                report['api_requests'] += 1
                payload, status = client.discovery(username)
                discovery = payload.get('business_discovery')
                if (not isinstance(discovery, dict) or str(discovery.get('username', '')).casefold() != username
                        or not re.fullmatch(r'\d+', str(discovery.get('id', '')))):
                    raise ProbeError('DISCOVERY_SCHEMA_OR_USERNAME_MISMATCH', status)
                if str(discovery.get('id')) == settings.meta_ig_user_id:
                    raise ProbeError('TARGET_IS_SELF_NOT_THIRD_PARTY', status)
                media = discovery.get('media', {'data': []})
                if not isinstance(media, dict) or not isinstance(media.get('data'), list):
                    raise ProbeError('MEDIA_SCHEMA_INVALID', status)
                posts = media['data']
                if any(not isinstance(p, dict) or not isinstance(p.get('id'), str) for p in posts):
                    raise ProbeError('POST_SCHEMA_INVALID', status)
                report['targets'][username].update(status='PASS', source_status='DISCOVERY_VERIFIED_NOT_SCHEDULED',
                    http_status=status, fields=sorted(k for k in discovery if k in ('id','username','media_count','media')),
                    media_count_in_response=len(posts),
                    post_fields=sorted({k for p in posts for k in p if k in ('id','caption','timestamp','permalink','media_type')}))
            except ProbeError as exc:
                report['targets'][username].update(exc.safe())
                if exc.code in ('TOKEN_INVALID_OR_EXPIRED', 'PERMISSION_DENIED', 'RATE_LIMITED', 'RETRY_LATER'):
                    blocked = True
                    break
        success = [v for v in report['targets'].values() if v['status'] == 'PASS']
        report['discovery_supported'] = 'PASS' if success else 'FAIL_OR_UNVERIFIED'
        report['next_phase_eligible'] = not blocked and any(v['media_count_in_response'] > 0 for v in success)
        report['reason'] = ('DISCOVERY_PASS_STORAGE_AND_EVENT_REVIEW_NOT_IMPLEMENTED'
            if report['next_phase_eligible'] else 'NO_VERIFIED_THIRD_PARTY_POSTS')
        # Availability alone is not POC_SUCCESS (which also requires safe storage/classification).
        report['decision'] = 'GO_NEXT_PHASE_ONLY' if report['next_phase_eligible'] else 'NO-GO'
    except ProbeError as exc:
        report['failure'] = exc.safe()
        report['reason'] = exc.code
    finally:
        report['api_requests'] = client.request_count
        client.close()
    return report

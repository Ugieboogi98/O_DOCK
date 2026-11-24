import logging
import secrets
from fastapi import Header, HTTPException, Request
from app.core.config import get_settings

audit = logging.getLogger('odock.audit')
MIN_ADMIN_TOKEN_LENGTH = 24


def require_same_origin(request: Request):
    origin = request.headers.get('origin')
    if origin and origin not in [o.strip() for o in get_settings().cors_origins.split(',')]:
        raise HTTPException(403, '허용되지 않은 요청 출처입니다.')
    # Browsers that omit Origin still send Fetch Metadata. Reject explicit cross-site requests;
    # non-browser clients (scripts, curl) send neither header and are unaffected.
    if not origin and request.headers.get('sec-fetch-site') == 'cross-site':
        raise HTTPException(403, '허용되지 않은 요청 출처입니다.')


def require_admin(x_admin_token: str = Header(default=""), request: Request = None):
    token = get_settings().admin_token
    if not token:
        raise HTTPException(
            503, "관리 기능을 사용하려면 서버의 ADMIN_TOKEN을 설정하세요."
        )
    if len(token) < MIN_ADMIN_TOKEN_LENGTH:
        raise HTTPException(
            503, f"ADMIN_TOKEN이 너무 짧습니다. {MIN_ADMIN_TOKEN_LENGTH}자 이상의 무작위 값으로 바꾸세요."
        )
    client = request.client.host if request is not None and request.client else 'unknown'
    if not secrets.compare_digest(token.encode('utf-8'), x_admin_token.encode('utf-8')):
        if x_admin_token:
            audit.warning('admin_denied method=%s path=%s client=%s', getattr(request, 'method', '-'), getattr(getattr(request, 'url', None), 'path', '-'), client)
        raise HTTPException(403, "관리자 인증이 필요합니다.")
    audit.info('admin_ok method=%s path=%s client=%s', getattr(request, 'method', '-'), getattr(getattr(request, 'url', None), 'path', '-'), client)

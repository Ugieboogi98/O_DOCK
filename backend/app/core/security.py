import secrets
from fastapi import Header, HTTPException, Request
from app.core.config import get_settings


def require_same_origin(request: Request):
    origin = request.headers.get('origin')
    if origin and origin not in get_settings().cors_origins.split(','):
        raise HTTPException(403, '허용되지 않은 요청 출처입니다.')


def require_admin(x_admin_token: str = Header(default="")):
    token = get_settings().admin_token
    if not token:
        raise HTTPException(
            503, "관리 기능을 사용하려면 서버의 ADMIN_TOKEN을 설정하세요."
        )
    if not secrets.compare_digest(token.encode('utf-8'), x_admin_token.encode('utf-8')):
        raise HTTPException(403, "관리자 인증이 필요합니다.")

"""Password hashing, server sessions and authenticated ownership dependencies."""
import hashlib
import secrets
from datetime import timedelta, timezone
from fastapi import Depends, HTTPException, Request
from sqlalchemy import delete
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.config import get_settings
from app.models.entities import User, UserSession, now
COOKIE = 'odock_session'
LIFETIME = 7 * 86400


def password_hash(password, salt=None):
    salt = salt or secrets.token_hex(16)
    digest = hashlib.scrypt(password.encode(), salt=bytes.fromhex(salt), n=16384, r=8, p=1, maxmem=64*1024*1024)
    return salt + ':' + digest.hex()


def verify_password(password, stored):
    candidate = password_hash(password, stored.split(':')[0] if stored else '00'*16)
    return bool(stored) and secrets.compare_digest(candidate, stored)


def utc(value):
    return value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value


def optional_user(request: Request, db: Session = Depends(get_db)):
    configured = get_settings().admin_token
    supplied = request.headers.get('x-admin-token', '')
    if configured and secrets.compare_digest(configured.encode(), supplied.encode()):
        return db.get(User, 1)
    token = request.cookies.get(COOKIE)
    if not token or len(token) > 200:
        return None
    session = db.get(UserSession, hashlib.sha256(token.encode()).hexdigest())
    return db.get(User, session.user_id) if session and utc(session.expires_at) > now() else None


def require_user(user=Depends(optional_user)):
    if user is None:
        raise HTTPException(401, '로그인이 필요합니다.')
    return user


def identity(user):
    return {'id': user.id, 'username': user.username}


def issue_session(db, user, response, request):
    old = request.cookies.get(COOKIE)
    if old:
        db.execute(delete(UserSession).where(UserSession.token_hash == hashlib.sha256(old.encode()).hexdigest()))
    db.execute(delete(UserSession).where(UserSession.expires_at <= now()))
    token = secrets.token_urlsafe(48)
    db.add(UserSession(token_hash=hashlib.sha256(token.encode()).hexdigest(), user_id=user.id,
                       expires_at=now() + timedelta(seconds=LIFETIME)))
    db.commit()
    response.set_cookie(COOKIE, token, max_age=LIFETIME, httponly=True, samesite='lax',
                        secure=get_settings().auth_cookie_secure, path='/api')
    return identity(user)

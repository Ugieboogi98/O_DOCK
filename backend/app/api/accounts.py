"""Account registration, login, logout and current-identity endpoints."""
import hashlib
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from pydantic import BaseModel, Field, ConfigDict
from sqlalchemy import select, delete
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.core.database import get_db
from app.core.config import get_settings
from app.core.security import require_same_origin
from app.core.rate_limit import limiter

# Per client IP, on top of the per-account lockout below.
login_limit = limiter('login', 20, 300)
register_limit = limiter('register', 10, 3600)
from app.models.entities import User, UserSession, now
from app.services.accounts import COOKIE, identity, issue_session, optional_user, password_hash, utc, verify_password
router = APIRouter(prefix='/api/auth', tags=['accounts'])


class Credentials(BaseModel):
    model_config = ConfigDict(extra='forbid')
    username: str = Field(pattern=r'^[a-zA-Z0-9][a-zA-Z0-9_.-]{2,39}$')
    password: str = Field(min_length=12, max_length=128)


@router.post('/register', dependencies=[Depends(require_same_origin), Depends(register_limit)])
def register(data: Credentials, request: Request, response: Response, db: Session = Depends(get_db)):
    username = data.username.lower()
    if username == 'admin':
        raise HTTPException(409, '사용할 수 없는 사용자 이름입니다.')
    user = User(username=username, password_hash=password_hash(data.password))
    db.add(user)
    try:
        db.flush()
    except IntegrityError:
        db.rollback()
        raise HTTPException(409, '사용할 수 없는 사용자 이름입니다.') from None
    return issue_session(db, user, response, request)


@router.post('/login', dependencies=[Depends(require_same_origin), Depends(login_limit)])
def login(data: Credentials, request: Request, response: Response, db: Session = Depends(get_db)):
    user = db.scalar(select(User).where(User.username == data.username.lower()).with_for_update())
    if user and user.locked_until and utc(user.locked_until) > now():
        raise HTTPException(429, '로그인 시도가 많습니다. 15분 뒤 다시 시도하세요.')
    if not verify_password(data.password, user.password_hash if user else None):
        if user and user.password_hash:
            user.failed_attempts += 1
            if user.failed_attempts >= 5:
                user.locked_until = now() + timedelta(minutes=15)
            db.commit()
        raise HTTPException(401, '사용자 이름 또는 비밀번호를 확인하세요.')
    user.failed_attempts = 0
    user.locked_until = None
    return issue_session(db, user, response, request)


@router.get('/me')
def me(user=Depends(optional_user)):
    return {'user': identity(user) if user else None}


@router.post('/logout', dependencies=[Depends(require_same_origin)])
def logout(request: Request, response: Response, db: Session = Depends(get_db)):
    token = request.cookies.get(COOKIE)
    if token:
        db.execute(delete(UserSession).where(UserSession.token_hash == hashlib.sha256(token.encode()).hexdigest()))
        db.commit()
    response.delete_cookie(COOKIE, path='/api', httponly=True, samesite='lax', secure=get_settings().auth_cookie_secure)
    return {'logged_out': True}

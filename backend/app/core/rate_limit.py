"""Small in-process sliding-window limiter for authentication endpoints.

Per-account lockout already stops guessing one password. This limiter also
covers password spraying across many accounts from one client, and mass
registration. It keeps state in memory, which is enough for the single
backend process this project runs.
"""
import ipaddress
import threading
import time
from collections import defaultdict, deque
from fastapi import HTTPException, Request

_lock = threading.Lock()
_hits = defaultdict(deque)


def client_ip(request: Request) -> str:
    peer = request.client.host if request.client else 'unknown'
    try:
        private = ipaddress.ip_address(peer).is_private or ipaddress.ip_address(peer).is_loopback
    except ValueError:
        private = False
    # Only trust the proxy header when the direct peer is our own reverse proxy (private network).
    forwarded = request.headers.get('x-real-ip') if private else None
    return (forwarded or peer).strip()[:64]


def hit(key: str, limit: int, window: float, now=None) -> bool:
    """Record one attempt; return False when the key exceeded ``limit`` within ``window`` seconds."""
    now = time.monotonic() if now is None else now
    with _lock:
        q = _hits[key]
        while q and now - q[0] > window:
            q.popleft()
        if len(q) >= limit:
            return False
        q.append(now)
        if len(_hits) > 10000:  # bound memory under a flood of distinct keys
            for stale in [k for k, v in _hits.items() if not v or now - v[-1] > window][:5000]:
                _hits.pop(stale, None)
        return True


def reset():
    with _lock:
        _hits.clear()


def limiter(name: str, limit: int, window: float):
    def dependency(request: Request):
        if not hit(f'{name}:{client_ip(request)}', limit, window):
            raise HTTPException(429, '요청이 너무 많습니다. 잠시 뒤 다시 시도하세요.', headers={'Retry-After': str(int(window))})
    return dependency

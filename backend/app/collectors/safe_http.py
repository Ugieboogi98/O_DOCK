"""Public HTTPS allowlist, fail-closed robots, bounded bodies and paced retries."""

import ipaddress
import socket
import time
import json
import re
from email.utils import parsedate_to_datetime
from datetime import datetime, timezone
from urllib.parse import urlparse, urljoin, unquote
import httpx
from app.core.config import get_settings


class CollectionDenied(ValueError):
    pass


def robots_rules(body, user_agent):
    """Select most specific agent group; merge equally specific groups."""
    groups = []
    agents, rules = [], []
    directives = False
    for line in body.splitlines() + ["User-agent: __end__"]:
        line = line.split("#", 1)[0].strip()
        if ":" not in line:
            continue
        key, value = (x.strip() for x in line.split(":", 1))
        key = key.lower()
        if key == "user-agent":
            if directives:
                groups.append((agents, rules))
                agents, rules, directives = [], [], False
            agents.append(value.lower())
        elif agents:
            directives = True
            rules.append((key, value))
    ua = user_agent.lower()
    ranked = [
        (
            max(
                (0 if a == "*" else len(a) for a in agents if a == "*" or a in ua),
                default=-1,
            ),
            rules,
        )
        for agents, rules in groups
    ]
    best = max((rank for rank, _ in ranked), default=-1)
    return [
        rule for rank, rules in ranked if rank == best and rank >= 0 for rule in rules
    ]


def robots_allowed(rules, url):
    p = urlparse(url)
    target = unquote(p.path or "/") + ("?" + p.query if p.query else "")
    matches = []
    for kind, value in rules:
        if kind not in ("allow", "disallow") or not value:
            continue
        terminal = value.endswith("$")
        raw = unquote(value[:-1] if terminal else value)
        pattern = (
            "^"
            + ".*".join(re.escape(x) for x in raw.split("*"))
            + ("$" if terminal else "")
        )
        if re.search(pattern, target):
            matches.append((len(raw.replace("*", "")), kind == "allow"))
    return max(matches, default=(0, True))[1]


class SafeFetcher:
    def __init__(self):
        self.s = get_settings()
        self.policy = json.loads(
            (self.s.data_dir / "source_policy.json").read_text(encoding="utf-8-sig")
        )
        self.robots, self.last = {}, {}

    def validate(self, url):
        parsed = urlparse(url)
        host = (parsed.hostname or "").lower()
        if (
            parsed.scheme != "https"
            or parsed.username
            or parsed.password
            or parsed.port not in (None, 443)
        ):
            raise CollectionDenied("HTTPS_PUBLIC_SOURCE_REQUIRED")
        rule = self.policy.get(host, {})
        if not rule.get("enabled"):
            raise CollectionDenied("SOURCE_DISABLED")
        # Decode before policy matching; encoded traversal must not escape the subtree.
        path = unquote(parsed.path)
        if "\\" in path or any(x in (".", "..") for x in path.split("/")):
            raise CollectionDenied("UNSAFE_PATH")
        if not any(path.startswith(p) for p in rule.get("paths", [])):
            raise CollectionDenied("PATH_NOT_ALLOWED")
        addresses = socket.getaddrinfo(host, 443, type=socket.SOCK_STREAM)
        if not addresses or any(
            not ipaddress.ip_address(x[4][0]).is_global for x in addresses
        ):
            raise CollectionDenied("PRIVATE_NETWORK_BLOCKED")
        return host, rule

    def check_robots(self, url, host):
        if host not in self.robots:
            with httpx.Client(
                timeout=self.s.request_timeout,
                follow_redirects=False,
                headers={"User-Agent": self.s.user_agent},
            ) as client:
                with client.stream(
                    "GET", "https://" + host + "/robots.txt"
                ) as response:
                    if response.status_code not in (200, 404):
                        raise CollectionDenied("ROBOTS_UNAVAILABLE")
                    body = bytearray()
                    for block in response.iter_bytes():
                        body.extend(block)
                        if len(body) > 500_000:
                            raise CollectionDenied("ROBOTS_TOO_LARGE")
                    # An HTML challenge is not an empty robots permission.
                    decoded = body.decode("utf-8", errors="replace")
                    if response.status_code == 200 and "<html" in decoded.lower():
                        raise CollectionDenied("ROBOTS_INVALID")
                    rules = (
                        robots_rules(decoded, self.s.user_agent)
                        if response.status_code == 200
                        else []
                    )
                    self.robots[host] = rules
        if not robots_allowed(self.robots[host], url):
            raise CollectionDenied("ROBOTS_DENIED")

    def _pace(self, host, rule):
        delays = [self.s.collection_delay_seconds, float(rule.get("delay_seconds", 2))]
        for kind, value in self.robots.get(host, []):
            if kind == "crawl-delay":
                try:
                    delays.append(float(value))
                except ValueError:
                    raise CollectionDenied("INVALID_CRAWL_DELAY")
            if kind == "request-rate":
                try:
                    count, seconds = map(float, value.split("/"))
                    delays.append(seconds / count)
                except (ValueError, ZeroDivisionError):
                    raise CollectionDenied("INVALID_REQUEST_RATE")
        delay = max(delays)
        if delay > 60:
            raise CollectionDenied("CRAWL_DELAY_REQUIRES_SCHEDULING")
        time.sleep(max(0, delay - (time.monotonic() - self.last.get(host, 0))))
        self.last[host] = time.monotonic()

    def _request(self, url):
        for _ in range(4):
            host, rule = self.validate(url)
            self.check_robots(url, host)
            for attempt in range(3):
                self._pace(host, rule)
                with httpx.Client(
                    timeout=self.s.request_timeout,
                    follow_redirects=False,
                    headers={"User-Agent": self.s.user_agent},
                ) as client:
                    with client.stream("GET", url) as response:
                        if response.status_code in (429, 500, 502, 503, 504):
                            if attempt == 2:
                                response.raise_for_status()
                            value = response.headers.get("Retry-After", "")
                            try:
                                seconds = float(value)
                            except ValueError:
                                try:
                                    seconds = (
                                        parsedate_to_datetime(value)
                                        - datetime.now(timezone.utc)
                                    ).total_seconds()
                                except (ValueError, TypeError, OverflowError):
                                    seconds = 0
                            if seconds > 60:
                                raise CollectionDenied("RETRY_AFTER_REQUIRES_LATER_RUN")
                            time.sleep(max(0, seconds, 2**attempt))
                            continue
                        if response.is_redirect:
                            location = response.headers.get("location")
                            if not location:
                                raise CollectionDenied("REDIRECT_WITHOUT_LOCATION")
                            url = urljoin(url, location)
                            break
                        response.raise_for_status()
                        data = bytearray()
                        for block in response.iter_bytes():
                            data.extend(block)
                            if len(data) > 3_000_000:
                                raise CollectionDenied("BODY_TOO_LARGE")
                        return data.decode("utf-8", errors="replace"), url
        raise CollectionDenied("TOO_MANY_REDIRECTS")

    def fetch_page(self, url):
        return self._request(url)

    def fetch(self, url):
        return self._request(url)[0]

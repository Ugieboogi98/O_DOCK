"""Allowlisted, robots-aware GET client with persistent conditional cache."""
import hashlib
import json
from pathlib import Path
import time
from urllib.parse import urljoin, urlsplit
from urllib.robotparser import RobotFileParser
import httpx

AGENT='O_DOCK-EventCollector/1.0'
ORIGINS={
 'https://www.duex.co.kr','https://spacegalleria.co.kr',
 'https://www.animate-onlineshop.co.kr','https://shop.aniplustv.com',
 'https://api.aniplustv.com:3060','https://www.popcondplay.com',
 'https://daewonmedia.com','https://www.agfkorea.com','https://www.gstar.or.kr',
}

class FetchError(Exception):
    pass

class PublicClient:
    def __init__(self,cache,*,transport=None,delay=1.0,sleep=time.sleep):
        self.cache=Path(cache);self.cache.mkdir(parents=True,exist_ok=True)
        self.http=httpx.Client(timeout=25,transport=transport,follow_redirects=False,headers={'User-Agent':AGENT})
        self.delay=delay;self.sleep=sleep;self.last={};self.robots={};self.requests=0

    def close(self):self.http.close()

    def origin(self,url):
        p=urlsplit(url)
        origin=f'{p.scheme}://{p.netloc}'
        if origin not in ORIGINS or p.username or p.password:raise FetchError('URL_NOT_ALLOWLISTED')
        return origin

    def _get(self,url,headers=None):
        origin=self.origin(url)
        pause=self.delay-(time.monotonic()-self.last.get(origin,0))
        if pause>0:self.sleep(pause)
        for attempt in range(3):
            self.requests+=1;self.last[origin]=time.monotonic()
            try:
                with self.http.stream('GET',url,headers=headers or {}) as r:
                    body=bytearray()
                    for chunk in r.iter_bytes():
                        body.extend(chunk)
                        if len(body)>5_000_000:raise FetchError('RESPONSE_TOO_LARGE')
                    # iter_bytes() already decompresses gzip/br; don't decode it a second time.
                    response=httpx.Response(r.status_code,headers={k:v for k,v in r.headers.items()
                        if k.lower() not in ('content-encoding','content-length')},content=bytes(body),request=r.request)
            except httpx.HTTPError as exc:
                if attempt==2:raise FetchError(type(exc).__name__) from None
                self.sleep(2**(attempt+1));continue
            if response.status_code in (429,500,502,503,504) and attempt<2:
                retry=response.headers.get('retry-after','')
                if retry.isdigit() and int(retry)>30:raise FetchError('RATE_LIMITED_RETRY_LATER')
                self.sleep(max(2**(attempt+1),int(retry) if retry.isdigit() else 0));continue
            return response

    def allowed(self,url):
        origin=self.origin(url)
        if origin not in self.robots:
            r=self._get(origin+'/robots.txt')
            if r.status_code==200:
                parser=RobotFileParser();parser.parse(r.text.splitlines());self.robots[origin]=parser
                (self.cache/(hashlib.sha256(origin.encode()).hexdigest()+'.robots.txt')).write_text(r.text,encoding='utf-8')
            elif r.status_code in (404,410):self.robots[origin]=True
            else:raise FetchError('ROBOTS_UNAVAILABLE')
        policy=self.robots[origin]
        if policy is not True:
            if not policy.can_fetch(AGENT,url):raise FetchError('ROBOTS_DISALLOWED')
            self.delay=max(self.delay,policy.crawl_delay(AGENT) or policy.crawl_delay('*') or 0)
        return True

    def get(self,url,*,ttl=3600):
        for _ in range(4):
            self.allowed(url)
            path=self.cache/(hashlib.sha256(url.encode()).hexdigest()+'.json')
            old=json.loads(path.read_text(encoding='utf-8')) if path.exists() else None
            if old and time.time()-old['checked_at']<ttl:return old['body']
            headers={}
            if old:
                if old.get('etag'):headers['If-None-Match']=old['etag']
                if old.get('modified'):headers['If-Modified-Since']=old['modified']
            r=self._get(url,headers)
            if r.status_code in (301,302,303,307,308):
                url=urljoin(url,r.headers.get('location',''));self.origin(url);continue
            if r.status_code==304 and old:
                old['checked_at']=time.time();path.write_text(json.dumps(old),encoding='utf-8');return old['body']
            if r.status_code!=200:raise FetchError(f'HTTP_{r.status_code}')
            if not any(t in r.headers.get('content-type','').lower() for t in ('html','json','javascript','text/')):
                raise FetchError('UNEXPECTED_CONTENT_TYPE')
            data={'url':url,'checked_at':time.time(),'body':r.text,'etag':r.headers.get('etag'),'modified':r.headers.get('last-modified')}
            path.write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8')
            return data['body']
        raise FetchError('TOO_MANY_REDIRECTS')

"""Download only API-returned Meta CDN images for private review; never fetch video."""
from datetime import datetime, timezone
import hashlib
import ipaddress
from pathlib import Path
import re
import socket
from urllib.parse import urlsplit, parse_qs
import httpx


class ImageError(Exception):
    pass


def check_cdn(url, resolve=socket.getaddrinfo):
    if not isinstance(url,str):raise ImageError('INVALID_IMAGE_URL')
    try:
        parsed=urlsplit(url)
        host=parsed.hostname or ''
        valid=(parsed.scheme=='https' and not parsed.username and not parsed.password and
            parsed.port in (None,443) and not parsed.fragment and
            any(host==suffix or host.endswith('.'+suffix) for suffix in ('cdninstagram.com','fbcdn.net')))
        if not valid or any(k.lower() in ('access_token','token') for k in parse_qs(parsed.query)):
            raise ImageError('NON_META_IMAGE_URL_OR_TOKEN_QUERY')
        addresses=resolve(host,443,type=socket.SOCK_STREAM)
        if not addresses or any(not ipaddress.ip_address(a[4][0]).is_global for a in addresses):
            raise ImageError('NON_PUBLIC_CDN_ADDRESS')
    except (ValueError,OSError):
        raise ImageError('INVALID_OR_UNRESOLVABLE_CDN') from None
    return host


def image_assets(post):
    if not isinstance(post,dict):return []
    values=post.get('children',{}).get('data',[]) if isinstance(post.get('children'),dict) else []
    if post.get('media_type')!='CAROUSEL_ALBUM':values=[post]
    if not isinstance(values,list):return []
    assets=[]
    for value in values[:20]:
        if not isinstance(value,dict) or not re.fullmatch(r'\d{1,100}',str(value.get('id',''))):continue
        kind=value.get('media_type')
        url=value.get('media_url') if kind=='IMAGE' else value.get('thumbnail_url') if kind=='VIDEO' else None
        if url:
            assets.append({'external_media_id':str(value['id']), 'role':'VIDEO_THUMBNAIL' if kind=='VIDEO' else 'IMAGE', 'url':url})
    return assets


class ImageDownloader:
    def __init__(self, folder, *, transport=None, resolve=socket.getaddrinfo, max_bytes=10*1024**2,total_bytes=150*1024**2):
        self.folder=Path(folder);self.folder.mkdir(parents=True,exist_ok=True)
        self.resolve,self.max_bytes,self.remaining=resolve,max_bytes,total_bytes
        # Never send the Graph API bearer token to a CDN. No redirects or ambient proxies.
        self.client=httpx.Client(timeout=25,follow_redirects=False,trust_env=False,transport=transport)

    def close(self):self.client.close()

    def download(self,asset):
        try:
            host=check_cdn(asset['url'],self.resolve)
            if self.remaining<=0:raise ImageError('RUN_IMAGE_BUDGET_EXCEEDED')
            with self.client.stream('GET',asset['url'],headers={'Accept':'image/jpeg,image/png,image/webp'}) as response:
                if response.status_code!=200:raise ImageError('CDN_IMAGE_UNAVAILABLE')
                data=bytearray()
                for chunk in response.iter_bytes():
                    data.extend(chunk)
                    if len(data)>min(self.max_bytes,self.remaining):raise ImageError('IMAGE_SIZE_LIMIT_EXCEEDED')
                if data.startswith(b'\xff\xd8\xff'):ext='jpg'
                elif data.startswith(b'\x89PNG\r\n\x1a\n'):ext='png'
                elif data[:4]==b'RIFF' and data[8:12]==b'WEBP':ext='webp'
                else:raise ImageError('UNSUPPORTED_IMAGE_BYTES')
                if response.headers.get('content-type','').split(';')[0].lower() not in ('image/jpeg','image/png','image/webp'):
                    raise ImageError('NON_IMAGE_CONTENT_TYPE')
            digest=hashlib.sha256(data).hexdigest()
            file=self.folder/(digest+'.'+ext)
            if not file.exists():file.write_bytes(data)
            self.remaining-=len(data)
            return {'external_media_id':asset['external_media_id'],'role':asset['role'],'status':'DOWNLOADED',
                'path':'media/'+file.name,'sha256':digest,'bytes':len(data),'cdn_host':host,
                'downloaded_at':datetime.now(timezone.utc).isoformat(),
                'usage':'PRIVATE_REVIEW_ONLY_RIGHTS_NOT_VERIFIED_FOR_REPUBLICATION'}
        except ImageError as exc:
            return {'external_media_id':asset['external_media_id'],'role':asset['role'],'status':'UNAVAILABLE','reason':str(exc)}
        except (httpx.HTTPError,OSError):
            return {'external_media_id':asset['external_media_id'],'role':asset['role'],'status':'UNAVAILABLE','reason':'IMAGE_NETWORK_OR_STORAGE_FAILED'}

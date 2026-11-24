import socket
import httpx
import pytest
from app.integrations.instagram.images import ImageDownloader,ImageError,check_cdn,image_assets
from app.integrations.instagram.review import render


def resolve(*args,**kwargs):return [(socket.AF_INET,socket.SOCK_STREAM,6,'',('8.8.8.8',443))]


@pytest.mark.parametrize('url',['http://s.cdninstagram.com/img','https://cdninstagram.com.evil.example/img',
    'https://evil.example/img','https://s.fbcdn.net:8443/img','https://user:pass@s.fbcdn.net/img',
    'https://s.fbcdn.net/img?access_token=SECRET'])
def test_image_urls_cannot_leave_official_cdn(url):
    with pytest.raises(ImageError):check_cdn(url,resolve)


def test_private_dns_is_blocked():
    def private(*args,**kwargs):return [(socket.AF_INET,socket.SOCK_STREAM,6,'',('127.0.0.1',443))]
    with pytest.raises(ImageError):check_cdn('https://s.fbcdn.net/image',private)


def test_carousel_preserves_order_and_never_downloads_video():
    assets=image_assets({'id':'1','media_type':'CAROUSEL_ALBUM','children':{'data':[
        {'id':'2','media_type':'IMAGE','media_url':'https://a.cdninstagram.com/img'},
        {'id':'3','media_type':'VIDEO','media_url':'https://a.cdninstagram.com/video','thumbnail_url':'https://a.cdninstagram.com/thumb'},
        {'id':'4','media_type':'VIDEO','media_url':'https://a.cdninstagram.com/video'}]}})
    assert [v['external_media_id'] for v in assets]==['2','3']
    assert assets[1]['role']=='VIDEO_THUMBNAIL' and assets[1]['url'].endswith('/thumb')


def test_download_hash_dedup_no_bearer_and_no_signed_url_in_report(tmp_path):
    calls=[]
    def handler(request):
        calls.append(request)
        assert 'Authorization' not in request.headers
        return httpx.Response(200,headers={'Content-Type':'image/jpeg'},content=b'\xff\xd8\xffIMAGE')
    d=ImageDownloader(tmp_path,transport=httpx.MockTransport(handler),resolve=resolve)
    asset={'external_media_id':'123','role':'IMAGE','url':'https://s.fbcdn.net/image?sig=PRIVATE'}
    a=d.download(asset);b=d.download(asset);d.close()
    assert a['status']=='DOWNLOADED' and a['sha256']==b['sha256']
    assert len(list(tmp_path.iterdir()))==1 and 'url' not in a


@pytest.mark.parametrize('status,content,kind',[(302,b'','image/jpeg'),(403,b'','image/jpeg'),
    (200,b'<svg onload=alert(1)>','image/svg+xml'),(200,b'\xff\xd8\xffoops','text/html')])
def test_unavailable_redirect_or_active_content_is_not_saved(tmp_path,status,content,kind):
    d=ImageDownloader(tmp_path,transport=httpx.MockTransport(lambda _:httpx.Response(status,headers={'Content-Type':kind,'Location':'https://evil.example'},content=content)),resolve=resolve)
    result=d.download({'external_media_id':'1','role':'IMAGE','url':'https://s.fbcdn.net/img'})
    d.close()
    assert result['status']=='UNAVAILABLE' and not list(tmp_path.iterdir())


def test_image_size_and_run_budget_are_bounded(tmp_path):
    d=ImageDownloader(tmp_path,transport=httpx.MockTransport(lambda _:httpx.Response(200,headers={'Content-Type':'image/jpeg'},content=b'\xff\xd8\xff'+b'A'*100)),resolve=resolve,max_bytes=10)
    result=d.download({'external_media_id':'1','role':'IMAGE','url':'https://s.fbcdn.net/img'})
    d.close()
    assert result['reason']=='IMAGE_SIZE_LIMIT_EXCEEDED' and not list(tmp_path.iterdir())


def test_review_uses_only_local_hash_paths():
    from app.integrations.instagram.events import extract
    row={'source_username':'duex.official','timestamp':'2026-11-12','caption':'테스트',
        'permalink':'https://www.instagram.com/p/example/', 'candidate':extract('테스트',[]),
        'images':[{'status':'DOWNLOADED','path':'media/'+'a'*64+'.jpg','role':'IMAGE'},
                  {'status':'DOWNLOADED','path':'../../secret.jpg'},
                  {'status':'DOWNLOADED','path':'https://evil.example/image.jpg'}]}
    html=render({'posts':[row],'collected_at':'2026-11-12','image_summary':{'DOWNLOADED':1}})
    assert html.count('<img ')==1 and '../../secret' not in html and 'evil.example' not in html

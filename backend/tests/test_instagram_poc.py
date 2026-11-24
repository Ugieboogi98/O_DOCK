import json
import httpx
import pytest
import os
from app.integrations.instagram.config import InstagramSettings
from app.integrations.instagram.client import MetaClient, ProbeError
from app.integrations.instagram.probe import run_probe, TARGETS


@pytest.fixture(autouse=True)
def isolated_instagram_environment(monkeypatch):
    # Compose injects the real .env. Tests must never inherit production credentials.
    for key in list(os.environ):
        if key.startswith(('META_', 'INSTAGRAM_')):
            monkeypatch.delenv(key)


def settings(**changes):
    return InstagramSettings(_env_file=None, meta_app_id='111', meta_app_secret='APP_SECRET_SENTINEL',
        meta_access_token='TOKEN_SENTINEL', meta_ig_user_id='222', meta_graph_api_version='v25.0', **changes)


def client(handler, delays=None):
    return lambda s: MetaClient(s, transport=httpx.MockTransport(handler), sleep=(delays.append if delays is not None else lambda _: None))


def debug(**changes):
    return {'data': {'is_valid': True, 'app_id': '111', 'type': 'USER',
        'scopes': ['instagram_basic'], 'expires_at': 9999999999,
        'data_access_expires_at': 9999999999, **changes}}


def test_missing_config_never_issues_network_and_config_id_is_not_token():
    def forbidden(*args):
        raise AssertionError('network forbidden')
    result = run_probe(InstagramSettings(_env_file=None, meta_ig_login_config_id='123'), live=True, client_factory=forbidden)
    assert result['decision'] == 'NO-GO' and result['api_requests'] == 0
    assert result['config_created'] == 'PRESENT_UNVERIFIED'
    s = settings(meta_ig_login_config_id='TOKEN_SENTINEL')
    assert run_probe(s, live=True, client_factory=forbidden)['reason'] == 'CONFIGURATION_ID_IS_NOT_ACCESS_TOKEN'


def test_preflight_does_not_send_requests():
    result = run_probe(settings(), client_factory=client(lambda _: pytest.fail('request forbidden')))
    assert result['api_requests'] == 0 and result['decision'] == 'NO-GO'


@pytest.mark.parametrize('base', ['https://evil.example','http://graph.facebook.com','https://graph.facebook.com.evil.example','https://graph.instagram.com'])
def test_unknown_host_or_login_route_is_rejected(base):
    result = run_probe(settings(meta_graph_base_url=base), live=True)
    assert result['reason'] == 'LOGIN_HOST_ROUTE_UNVERIFIED'


@pytest.mark.parametrize('change,reason', [({'is_valid':False},'TOKEN_INVALID_OR_WRONG_APP'),
    ({'app_id':'333'},'TOKEN_INVALID_OR_WRONG_APP'), ({'expires_at':1},'TOKEN_EXPIRED'),
    ({'type':'APP'},'TOKEN_TYPE_UNVERIFIED'), ({'scopes':[]},'TOKEN_PERMISSIONS_UNVERIFIED'),
    ({'expires_at':None},'TOKEN_EXPIRY_UNVERIFIED')])
def test_failed_auth_stops_before_self_or_discovery(change, reason):
    requests = []
    def handler(request):
        requests.append(request)
        return httpx.Response(200, json=debug(**change))
    result = run_probe(settings(), live=True, client_factory=client(handler))
    assert result['reason'] == reason and len(requests) == 1
    assert all(v['status'] == 'UNKNOWN' for v in result['targets'].values())


def test_successful_discovery_is_not_storage_or_event_poc_success():
    requests = []
    def handler(request):
        requests.append(request)
        assert request.method == 'GET'
        assert 'access_token' not in request.url.params
        if request.url.path.endswith('/debug_token'):
            return httpx.Response(200, json=debug())
        if request.url.params['fields']=='id,username':
            return httpx.Response(200, json={'id':'222','username':'owner'})
        username = next(u for u in TARGETS if u in request.url.params['fields'])
        return httpx.Response(200, json={'business_discovery': {'id':'555','username':username,
            'media': {'data':[{'id':'123','caption':None,'permalink':'https://www.instagram.com/p/example/',
                             'timestamp':None,'media_type':'IMAGE'}],
                      'paging':{'next':'https://evil.example/?access_token=TOKEN_SENTINEL'}}}})
    result = run_probe(settings(), live=True, client_factory=client(handler))
    assert len(requests)==5
    assert result['token_valid']=='PASS' and result['discovery_supported']=='PASS'
    assert result['decision']=='GO_NEXT_PHASE_ONLY' and not result['poc_success']
    assert not result['db_written'] and not result['automatic_collection_started']
    encoded=json.dumps(result)
    assert 'TOKEN_SENTINEL' not in encoded and 'APP_SECRET_SENTINEL' not in encoded
    assert 'paging' not in encoded and 'caption' in encoded


@pytest.mark.parametrize('status,code,expected', [(401,190,'TOKEN_INVALID_OR_EXPIRED'),(403,10,'PERMISSION_DENIED'),(400,100,'DISCOVERY_FIELD_OR_OBJECT_UNAVAILABLE')])
def test_errors_are_redacted_and_not_retried(status,code,expected):
    calls=[]
    def handler(request):
        calls.append(request)
        return httpx.Response(status,json={'error':{'code':code,'message':'TOKEN_SENTINEL APP_SECRET_SENTINEL'}})
    c=client(handler)(settings())
    with pytest.raises(ProbeError) as error:
        c.own_account()
    c.close()
    assert error.value.code==expected and len(calls)==1
    assert 'SENTINEL' not in json.dumps(error.value.safe())


@pytest.mark.parametrize('status', [429,500,503])
def test_temporary_errors_have_bounded_backoff(status):
    calls=[];delays=[]
    def handler(request):
        calls.append(request)
        return httpx.Response(status,json={'error':{'code':1}})
    c=client(handler,delays)(settings())
    with pytest.raises(ProbeError):c.own_account()
    c.close()
    assert len(calls)==3 and delays==[1,2]


def test_large_retry_after_and_redirect_are_not_followed():
    c=client(lambda _:httpx.Response(429,headers={'Retry-After':'600'},json={})) (settings())
    with pytest.raises(ProbeError,match='RETRY_LATER'):c.own_account()
    c.close()
    c=client(lambda _:httpx.Response(302,headers={'Location':'https://evil.example'},json={})) (settings())
    with pytest.raises(ProbeError):c.own_account()
    c.close()


def test_permission_failure_stops_remaining_targets():
    calls=[]
    def handler(request):
        calls.append(request)
        if request.url.path.endswith('debug_token'):return httpx.Response(200,json=debug())
        if request.url.params['fields']=='id,username':return httpx.Response(200,json={'id':'222','username':'self'})
        return httpx.Response(403,json={'error':{'code':10,'message':'TOKEN_SENTINEL'}})
    result=run_probe(settings(),live=True,client_factory=client(handler))
    assert len(calls)==3 and result['targets']['duex.official']['status']=='FAIL'
    assert result['targets']['anique.jp']['status']=='UNKNOWN'
    assert all(v['source_status']=='MANUAL_LINK_ONLY' for v in result['targets'].values())


def test_empty_media_supports_discovery_but_does_not_pass_post_gate():
    def handler(request):
        if request.url.path.endswith('debug_token'):return httpx.Response(200,json=debug())
        if request.url.params['fields']=='id,username':return httpx.Response(200,json={'id':'222','username':'self'})
        username=next(u for u in TARGETS if u in request.url.params['fields'])
        return httpx.Response(200,json={'business_discovery':{'id':'555','username':username,'media':{'data':[]}}})
    result=run_probe(settings(),live=True,client_factory=client(handler))
    assert result['discovery_supported']=='PASS' and not result['next_phase_eligible']
    assert result['decision']=='NO-GO'


def test_revoked_token_after_one_target_cannot_authorize_next_phase():
    calls=[]
    def handler(request):
        calls.append(request)
        if request.url.path.endswith('debug_token'):return httpx.Response(200,json=debug())
        if request.url.params['fields']=='id,username':return httpx.Response(200,json={'id':'222','username':'self'})
        if 'duex.official' in request.url.params['fields']:
            return httpx.Response(200,json={'business_discovery':{'id':'555','username':'duex.official','media':{'data':[{'id':'789'}]}}})
        return httpx.Response(401,json={'error':{'code':190}})
    result=run_probe(settings(),live=True,client_factory=client(handler))
    assert len(calls)==4 and not result['next_phase_eligible'] and result['decision']=='NO-GO'


@pytest.mark.parametrize('payload', [[], {'business_discovery':None},
    {'business_discovery':{'id':'555','username':'wrong'}},
    {'business_discovery':{'username':'duex.official'}},
    {'business_discovery':{'id':'555','username':'duex.official','media':{'data':None}}}])
def test_malformed_response_never_passes_discovery(payload):
    def handler(request):
        if request.url.path.endswith('debug_token'):return httpx.Response(200,json=debug())
        if request.url.params['fields']=='id,username':return httpx.Response(200,json={'id':'222','username':'self'})
        return httpx.Response(200,json=payload)
    result=run_probe(settings(),live=True,client_factory=client(handler))
    assert not result.get('next_phase_eligible') and result['decision']=='NO-GO'

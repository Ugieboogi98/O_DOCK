from types import SimpleNamespace
import json
import pytest
from app.services.collection_preferences import excluded_manufacturer, excluded_retail_product, DOMESTIC_SOURCES
from app.services import domestic_collection_round as rounds

@pytest.mark.parametrize('value',['Hot Toys','HOTTOYS','핫토이','ホットトイズ','[예약] 핫 토이 아이언맨'])
def test_hottoys_aliases_are_excluded(value):
    assert excluded_manufacturer(value)
    assert excluded_retail_product({'title_raw':value})

def test_other_makers_remain_available():
    assert not excluded_manufacturer('TAITO')
    assert len(DOMESTIC_SOURCES)==4

def test_joint_round_collects_all_four_and_resumes_only_failed(tmp_path,monkeypatch):
    import scripts.preview_domestic_prices as preview
    calls=[]
    def collect(name,limit,report,output,commit):
        calls.append(name)
        report['sources'][name]={'state':'completed','parsed':1,'storage':{'inserted':1},'errors':[]}
        report['items'].append({'retailer_code':name})
    monkeypatch.setattr(preview,'collect_source',collect)
    assert rounds.run_round(tmp_path)['parsed']==4
    assert tuple(calls)==DOMESTIC_SOURCES
    calls.clear()
    assert rounds.run_round(tmp_path)['parsed']==4
    assert calls==[]


def test_retail_age_verification_is_skipped_without_parse_or_save(tmp_path,monkeypatch):
    from contextlib import nullcontext
    import scripts.preview_domestic_prices as preview
    class Fetcher:
        requests=2
        def fetch(self,url):
            return 'listing' if 'detail.html' not in url else '<script>location.replace("/intro/adult_im.html");</script>'
    source=dict(preview.SOURCES['herotime'],discover=lambda html:['https://www.herotime.co.kr/product/detail.html?product_no=77990'])
    monkeypatch.setitem(preview.SOURCES,'herotime',source)
    monkeypatch.setattr(preview,'PreviewFetcher',lambda name:Fetcher())
    monkeypatch.setattr(preview,'SessionLocal',lambda:nullcontext(None))
    report={'sources':{},'items':[],'errors':[]}
    result=preview.collect_source('herotime',20,report,tmp_path/'preview.json',commit=True)
    assert result['state']=='completed'
    assert result['restricted']==1 and result['parsed']==0

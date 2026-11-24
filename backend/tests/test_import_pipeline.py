"""Offline import staging regressions. No live DB, provider or website calls."""
import json
import sys
import os
import uuid
from types import SimpleNamespace
from decimal import Decimal
import pytest
from sqlalchemy import create_engine, event, select, func, text
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker
from app.core import database
from app.core.config import get_settings
from app.models.entities import (Base, Manufacturer, Figure, FigureVariant, SourceDocument,
                                CollectionJob, User, Favorite, Purchase, ProductImage)
from app.services import product_semantics as sem, import_pipeline
from app.services.semantic_queue import pending_jobs
from scripts import import_furyu_bundle as furyu, import_sfire_bundle as sfire, import_taito_bundle as taito


@pytest.fixture
def workspace(tmp_path, monkeypatch):
    test_url=os.environ.get('TEST_DATABASE_URL')
    control=None
    if test_url:
        target,live=make_url(test_url),make_url(get_settings().database_url)
        assert (target.host,target.port,target.database)!=(live.host,live.port,live.database), 'Dedicated test database required'
        schema='import_test_'+uuid.uuid4().hex
        control=create_engine(test_url)
        with control.begin() as conn:conn.execute(text(f'CREATE SCHEMA "{schema}"'))
        engine=create_engine(test_url,connect_args={'options':'-csearch_path='+schema,'prepare_threshold':None})
    else:
        engine=create_engine('sqlite:///'+str(tmp_path/'imports.db'))
        @event.listens_for(engine,'connect')
        def foreign_keys(conn,_):
            conn.execute('PRAGMA foreign_keys=ON')
    Base.metadata.create_all(engine)
    factory=sessionmaker(engine,expire_on_commit=False)
    monkeypatch.setattr(database,'SessionLocal',factory)
    monkeypatch.setattr(get_settings(),'media_dir',tmp_path/'media')
    def forbidden(*args,**kwargs):
        pytest.fail('Offline import must not call a provider')
    monkeypatch.setattr(sem,'Extractor',forbidden)
    with factory() as db:
        db.add(User(id=1,username='admin'))
        for name,ko in [('FuRyu','후류'),('SEGA','세가'),('TAITO','타이토'),('Bandai Spirits','반다이')]:
            db.add(Manufacturer(name=name,name_ko=ko,official_url='https://example.com/'+name))
        db.commit()
    yield factory,tmp_path
    engine.dispose()
    if control:
        with control.begin() as conn:conn.execute(text(f'DROP SCHEMA "{schema}" CASCADE'))
        control.dispose()


def run_import(maker,workspace,monkeypatch,commit,specs=None):
    factory,root=workspace
    title='テスト商品'
    if maker=='bandai':
        from app.services.bnkr_catalog import store_product
        row={'name_ko':'테스트 상품','url':'https://www.bnkrmall.co.kr/goods/detail.do?gno=111',
             'jan_code':'4900000000016','specifications':specs or {},'price_krw':None,'images':[]}
        return store_product(row,SimpleNamespace(commit=commit,create_new=True,max_images=0),SimpleNamespace())
    if maker=='furyu':
        url='https://furyu-hm.com/products/test-import'
        data={key:[] for key in furyu.TABLES}
        data['figures']=[{'official_url':url,'name_original':title,'type':'figure','quality':'official_metadata'}]
        data['figure_variants']=[{'figure_official_url':url,'variant_key':'main','sku':'F-TEST'}]
        data['source_documents']=[{'figure_official_url':url,'variant_key':'main','url':url,
            'title':title,'body':'公式の説明','source_type':'official_detail'}]
        return furyu.import_db(data,{},root/'media',commit,{})['summary']
    if maker=='taito':
        rows=[{'source_url':'https://taito-goods.jp/shop/g/gtest-import/',
               'name_original':title,'sku':'T-TEST','type':'goods','price_amount':None,'images':[]}]
        with factory() as db:
            return taito.import_rows(db,rows,root,root/'media',commit)
    jan='4900000000016'
    assert sfire.valid_jan(jan)
    bundle=root/'sfire'
    (bundle/'documents').mkdir(parents=True,exist_ok=True)
    (bundle/'documents'/f'{jan}.txt').write_text('公式の説明',encoding='utf-8')
    (bundle/'summary.json').write_text(json.dumps({'collected_at_utc':'2026-11-10T00:00:00+00:00'}))
    (bundle/'products.json').write_text(json.dumps([{'jan_code':jan,'official_url':'https://s-fire.net/products/'+jan,
        'name_original':title,'franchise':'','specifications':{},'price_amount':None,'images':[]}]))
    argv=['sfire','--bundle',str(bundle),'--report',str(root/'sfire-report.json')]
    if commit:argv.append('--commit')
    monkeypatch.setattr(sys,'argv',argv)
    sfire.main()
    return {}


@pytest.mark.parametrize('maker',['furyu','s_fire','taito','bandai'])
def test_preview_does_not_create_products_or_work(maker,workspace,monkeypatch):
    run_import(maker,workspace,monkeypatch,False)
    factory,_=workspace
    with factory() as db:
        assert db.scalar(select(func.count(Figure.id)))==0
        assert db.scalar(select(func.count(CollectionJob.id)))==0


@pytest.mark.parametrize('maker',['furyu','s_fire','taito'])
def test_commit_repeat_and_validated_cache_preserve_personal_records(maker,workspace,monkeypatch):
    factory,_=workspace
    run_import(maker,workspace,monkeypatch,True)
    with factory() as db:
        f=db.scalar(select(Figure));v=db.scalar(select(FigureVariant))
        fid,vid=f.id,v.id
        assert len(pending_jobs(db))==1
        first_job=pending_jobs(db)[0].id
        assert json.loads(pending_jobs(db)[0].error_summary)['source_hash']==sem.source_hash(sem.source_of(f))
        db.add(Favorite(figure_id=fid,user_id=1))
        purchase=Purchase(user_id=1,variant_id=vid,amount=Decimal('12345'),currency='KRW',purchased_on='2026-01-01')
        db.add(purchase);db.commit();pid=purchase.id
    run_import(maker,workspace,monkeypatch,True)
    with factory() as db:
        f=db.get(Figure,fid)
        assert [job.id for job in pending_jobs(db)]==[first_job]
        source=sem.source_of(f)
        response={'name_ko':'테스트 상품','franchise':None,'characters':[],'figure_form':None}
        assert sem.save_record(db,{'figure_id':fid,'source':source,'source_hash':sem.source_hash(source),
            'model':'fixture','result':response})=='partial'
        assert not pending_jobs(db)
        f.name_ko='사용자가 정한 이름';db.commit()
    run_import(maker,workspace,monkeypatch,True)
    with factory() as db:
        assert not pending_jobs(db)
        assert db.get(Figure,fid).name_ko=='사용자가 정한 이름'
        assert db.get(Favorite,(fid,1)) is not None
        assert db.get(Purchase,pid).amount==Decimal('12345')
        assert db.scalar(select(func.count(Figure.id)))==1
        assert db.scalar(select(func.count(FigureVariant.id)))==1
        # Requeue changed source without overwriting its content or calling a model.
        doc=db.scalar(select(SourceDocument));doc.body+=' 追加情報';db.commit()
    run_import(maker,workspace,monkeypatch,True)
    with factory() as db:
        f=db.get(Figure,fid)
        assert len(pending_jobs(db))==1
        assert pending_jobs(db)[0].id!=first_job
        assert json.loads(pending_jobs(db)[0].error_summary)['source_hash']==sem.source_hash(sem.source_of(f))


@pytest.mark.parametrize('maker',['furyu','s_fire','taito','bandai'])
def test_queue_failure_rolls_back_imported_source(maker,workspace,monkeypatch):
    def unavailable(*args):
        raise RuntimeError('QUEUE_UNAVAILABLE')
    monkeypatch.setattr(import_pipeline,'enqueue',unavailable)
    if maker in ('furyu','bandai'):
        with pytest.raises(RuntimeError,match='QUEUE_UNAVAILABLE'):
            run_import(maker,workspace,monkeypatch,True)
    elif maker=='s_fire':
        with pytest.raises(SystemExit) as error:
            run_import(maker,workspace,monkeypatch,True)
        assert error.value.code==1
    else:
        assert run_import(maker,workspace,monkeypatch,True)['failed']==1
    factory,_=workspace
    with factory() as db:
        assert db.scalar(select(func.count(Figure.id)))==0
        assert db.scalar(select(func.count(SourceDocument.id)))==0
        assert db.scalar(select(func.count(CollectionJob.id)))==0


def test_taito_reimport_does_not_restore_hidden_images(workspace,monkeypatch):
    factory,root=workspace
    run_import('taito',workspace,monkeypatch,True)
    source='https://example.com/image.jpg'
    with factory() as db:
        f=db.scalar(select(Figure));v=db.scalar(select(FigureVariant))
        db.add(ProductImage(variant_id=v.id,source_url=source,image_url='/api/media/original.jpg',usage_status='duplicate_hidden'))
        db.commit()
        row={'source_url':f.official_url,'name_original':f.name_original,'sku':'T-TEST','price_amount':None,
             'images':[{'source_url':source,'path':'missing-original.jpg','sha256':'0'*64}]}
        result=taito.import_rows(db,[row],root,root/'media',True)
        assert result['failed']==0
        image=db.scalar(select(ProductImage))
        assert image.usage_status=='duplicate_hidden'
        assert image.image_url=='/api/media/original.jpg'


def test_bandai_stages_updated_source_and_reuses_valid_results(workspace,monkeypatch):
    factory,_=workspace
    assert run_import('bandai',workspace,monkeypatch,True)['semantic_pending']==1
    with factory() as db:
        original_job=pending_jobs(db)[0].id
    run_import('bandai',workspace,monkeypatch,True)
    with factory() as db:
        assert [job.id for job in pending_jobs(db)]==[original_job]
        f=db.scalar(select(Figure));source=sem.source_of(f)
        sem.save_record(db,{'figure_id':f.id,'source':source,'source_hash':sem.source_hash(source),
            'model':'fixture','result':{'name_ko':'테스트 상품','franchise':None,'characters':[],'figure_form':None}})
    assert run_import('bandai',workspace,monkeypatch,True)['semantic_cached']==1
    with factory() as db:
        assert not pending_jobs(db)
    assert run_import('bandai',workspace,monkeypatch,True,specs={'색상':'검정'})['semantic_pending']==1
    with factory() as db:
        f=db.scalar(select(Figure))
        assert len(pending_jobs(db))==1
        assert pending_jobs(db)[0].id!=original_job
        assert json.loads(pending_jobs(db)[0].error_summary)['source_hash']==sem.source_hash(sem.source_of(f))

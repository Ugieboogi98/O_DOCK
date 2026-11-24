from datetime import datetime, timezone

from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session

from app.models.entities import Base, CollectionJob, Figure, FigureVariant, Manufacturer
from app.models.retail import RetailListing, RetailOffer
from scripts import import_direct_retail as importer


def record(source, product_id):
    url = 'https://' + importer.SOURCES[source]['host'] + '/product/detail.html?product_no=' + product_id
    return {
        'verified': True, 'images': [],
        'archive': {'retailer_code': source, 'retailer_product_id': product_id,
                    'original_title': '피규어 예시', 'displayed_korean_title': '피규어 예시'},
        'parsed': {'external_product_id': product_id, 'product_url': url, 'title_raw': '피규어 예시',
                   'manufacturer_raw': 'Maker', 'jan_ean': '4573102742414', 'model_code': None,
                   'observed_at': datetime.now(timezone.utc).isoformat(), 'currency': 'KRW',
                   'sale_price': 10000, 'list_price': None, 'availability': 'IN_STOCK',
                   'conditional_price': False, 'has_shop_bonus': False, 'payment_options': [], 'warnings': []},
    }


def test_import_replay_and_second_retailer_share_one_etc_figure(tmp_path, monkeypatch):
    engine = create_engine('sqlite:///' + str(tmp_path / 'catalog.sqlite'))
    Base.metadata.create_all(engine)
    monkeypatch.setattr(importer, 'SessionLocal', lambda: Session(engine, expire_on_commit=False))
    decision = {'action': 'link_or_create', 'reason': 'test reviewed identity'}
    first = importer.import_record(record('maniahouse', '123'), decision, True)
    second = importer.import_record(record('herotime', '456'), decision, True)
    replay = importer.import_record(record('maniahouse', '123'), decision, True)
    assert first['state'] == 'created'
    assert second['state'] == replay['state'] == 'linked'
    assert first['variant_id'] == second['variant_id'] == replay['variant_id']
    with Session(engine) as db:
        assert db.scalar(select(func.count()).select_from(Figure)) == 1
        assert db.scalar(select(func.count()).select_from(FigureVariant)) == 1
        assert db.scalar(select(Manufacturer.name)) == 'ETC'
        assert db.scalar(select(func.count()).select_from(RetailListing)) == 2
        assert db.scalar(select(func.count()).select_from(RetailOffer)) == 2
        assert db.scalar(select(func.count()).select_from(CollectionJob).where(CollectionJob.collector.like('catalog_semantics:%'))) == 1


def test_refurbished_offer_is_conditional_and_excluded_goods_create_no_figure(tmp_path, monkeypatch):
    engine = create_engine('sqlite:///' + str(tmp_path / 'catalog.sqlite'))
    Base.metadata.create_all(engine)
    monkeypatch.setattr(importer, 'SessionLocal', lambda: Session(engine, expire_on_commit=False))
    row = record('maniahouse', '123')
    row['archive']['displayed_korean_title'] = '(리퍼상품) 피규어 예시'
    row['archive']['displayed_schedule_text'] = '99년 5월'
    importer.import_record(row, {'action': 'link_or_create', 'reason': 'test'}, True)
    importer.import_record(record('herotime', '456'), {'action': 'excluded', 'reason': 'not a figure'}, True)
    with Session(engine) as db:
        assert db.scalar(select(RetailOffer.conditions).join(RetailListing).where(RetailListing.source_code == 'maniahouse'))['conditional_price'] is True
        assert db.scalar(select(RetailOffer.availability).join(RetailListing).where(RetailListing.source_code == 'maniahouse')) == 'PREORDER'
        assert db.scalar(select(func.count()).select_from(Figure)) == 1
        listing = db.scalar(select(RetailListing).where(RetailListing.source_code == 'herotime'))
        assert listing.match_status == 'REJECTED' and listing.catalog_variant_id is None

from datetime import datetime, timedelta, timezone
import importlib.util
from pathlib import Path

from alembic.migration import MigrationContext
from alembic.operations import Operations
from fastapi import FastAPI
from fastapi.testclient import TestClient
import pytest
from sqlalchemy import create_engine, func, inspect, select
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from app.api.retail_offers import router
from app.core.database import get_db
from app.models.entities import Base, Retailer, Manufacturer, Figure, FigureVariant
from app.services.domestic_prices import domestic_comparison
from app.models.retail import RetailListing, RetailOffer
from app.services.retail_collection import save_offer


@pytest.fixture
def session():
    engine = create_engine('sqlite://', poolclass=StaticPool, connect_args={'check_same_thread': False})
    Base.metadata.create_all(engine)
    with Session(engine) as db:
        yield db
    engine.dispose()


def observation():
    return {'external_product_id': '123', 'product_url': 'https://maniahouse.co.kr/product/detail.html?product_no=123',
            'title_raw': '예약상품', 'manufacturer_raw': 'Maker', 'jan_ean': None, 'model_code': None,
            'currency': 'KRW', 'sale_price': 10000, 'list_price': 12000, 'availability': 'PREORDER',
            'observed_at': (datetime.now(timezone.utc) - timedelta(minutes=1)).isoformat(), 'has_shop_bonus': False,
            'conditional_price': False, 'payment_options': [], 'warnings': [],
            'match': {'status': 'UNMATCHED', 'reason': 'NO_JAN_CANDIDATE', 'candidates': []}}


def test_repeat_update_and_older_observation_keep_one_current_offer(session):
    row = observation()
    assert save_offer(session, 'maniahouse', row) == 'inserted'
    session.commit()
    assert save_offer(session, 'maniahouse', row) == 'updated'
    session.commit()
    newer = {**row, 'sale_price': 9000, 'observed_at': (datetime.fromisoformat(row['observed_at']) + timedelta(seconds=1)).isoformat()}
    assert save_offer(session, 'maniahouse', newer) == 'updated'
    session.commit()
    assert save_offer(session, 'maniahouse', row) == 'stale'
    session.commit()
    assert session.scalar(select(func.count()).select_from(RetailListing)) == 1
    assert session.scalar(select(func.count()).select_from(RetailOffer)) == 1
    assert session.scalar(select(RetailOffer.sale_price)) == 9000
    assert session.scalar(select(RetailListing.catalog_variant_id)) is None


def test_price_validation_precedes_database_writes(session):
    with pytest.raises(ValueError, match='INVALID_PRICE'):
        save_offer(session, 'maniahouse', {**observation(), 'sale_price': -1})
    assert session.scalar(select(func.count()).select_from(Retailer)) == 0
    assert session.scalar(select(func.count()).select_from(RetailListing)) == 0


def test_excluded_maker_is_never_saved(session):
    with pytest.raises(ValueError,match='MANUFACTURER_EXCLUDED'):
        save_offer(session,'maniahouse',{**observation(),'manufacturer_raw':'핫토이'})
    assert session.scalar(select(func.count()).select_from(RetailListing))==0


def test_unique_jan_and_maker_link_but_scale_conflicts_do_not(session):
    maker=Manufacturer(name='Kotobukiya',name_ko='코토부키야',official_url='https://example.com')
    session.add(maker);session.flush()
    figure=Figure(manufacturer_id=maker.id,name_original='Figure',official_url='https://example.com/product',scale='1/7')
    session.add(figure);session.flush()
    variant=FigureVariant(figure_id=figure.id,variant_key='standard',jan_code='4904810931098')
    # Use a checksum-valid JAN as the sole identity evidence.
    from app.collectors.retailers.maniahouse import valid_jan
    base='490481093109'
    variant.jan_code=base+str((-sum(int(n)*(1 if i%2==0 else 3) for i,n in enumerate(base)))%10)
    assert valid_jan(variant.jan_code)
    session.add(variant);session.commit()
    row={**observation(),'manufacturer_raw':'코토부키야','jan_ean':variant.jan_code,'title_raw':'Figure 1/7'}
    save_offer(session,'maniahouse',row);session.commit()
    assert session.scalar(select(RetailListing)).catalog_variant_id==variant.id
    conflict={**row,'title_raw':'Figure 1/6','observed_at':datetime.now(timezone.utc).isoformat()}
    save_offer(session,'maniahouse',conflict);session.commit()
    assert session.scalar(select(RetailListing)).catalog_variant_id is None


def test_null_price_and_existing_seller_are_preserved(session):
    session.add(Retailer(name='매니아하우스', site_url='https://www.maniahouse.co.kr', seller_type='unverified'))
    session.commit()
    save_offer(session, 'maniahouse', {**observation(), 'sale_price': None})
    session.commit()
    assert session.scalar(select(func.count()).select_from(Retailer)) == 1
    assert session.scalar(select(RetailOffer.sale_price)) is None


def test_offer_api_exposes_unmatched_with_filters(session):
    save_offer(session, 'maniahouse', observation())
    session.commit()
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_db] = lambda: session
    with TestClient(app) as client:
        response = client.get('/api/retail-offers?source=maniahouse&availability=PREORDER')
        assert response.status_code == 200
        data = response.json()
        assert data['total'] == 1 and data['items'][0]['sale_price'] == 10000
        assert data['items'][0]['catalog_variant_id'] is None
        assert client.get('/api/retail-offers?source=figurefarm').json()['total'] == 0


def test_retail_migration_upgrade_and_downgrade_only_target_new_tables():
    engine = create_engine('sqlite://')
    path = Path(__file__).resolve().parents[1] / 'alembic/versions/20261116_retail_offers.py'
    spec = importlib.util.spec_from_file_location('retail_migration', path)
    migration = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(migration)
    with engine.begin() as connection:
        context = MigrationContext.configure(connection)
        Retailer.__table__.create(connection)
        with Operations.context(context):
            migration.upgrade()
            assert {'retailer_listings', 'retailer_offers'} <= set(inspect(connection).get_table_names())
            migration.downgrade()
            assert 'retailer_listings' not in inspect(connection).get_table_names()
            assert 'retailers' in inspect(connection).get_table_names()
    engine.dispose()


def test_confirmed_variant_prices_and_match_survive_price_refresh(session):
    maker = Manufacturer(name='Maker', name_ko='제조사', official_url='https://maker.example')
    session.add(maker)
    session.flush()
    figure = Figure(manufacturer_id=maker.id, name_original='Figure', official_url='https://maker.example/1')
    session.add(figure)
    session.flush()
    variant = FigureVariant(figure_id=figure.id, variant_key='standard')
    session.add(variant)
    session.flush()
    row = observation()
    save_offer(session, 'maniahouse', row)
    session.commit()
    # Unlinked observations must not appear on an arbitrary product detail.
    assert domestic_comparison(session, variant.id, [])['lowest_price'] is None
    listing = session.scalar(select(RetailListing))
    listing.catalog_variant_id = variant.id
    listing.match_status = 'MATCHED'
    session.commit()
    assert domestic_comparison(session, variant.id, [])['lowest_price'] == 10000
    newer = {**row, 'sale_price': 9000, 'observed_at': (datetime.fromisoformat(row['observed_at']) + timedelta(seconds=1)).isoformat()}
    save_offer(session, 'maniahouse', newer)
    session.commit()
    assert domestic_comparison(session, variant.id, [])['lowest_price'] == 9000
    changed_identity = {**newer, 'title_raw': 'Different edition', 'observed_at': datetime.now(timezone.utc).isoformat()}
    save_offer(session, 'maniahouse', changed_identity)
    session.commit()
    assert domestic_comparison(session, variant.id, [])['lowest_price'] is None


def _catalog(session):
    maker = Manufacturer(name='Kotobukiya', name_ko='코토부키야', official_url='https://example.com')
    session.add(maker); session.flush()
    figure = Figure(manufacturer_id=maker.id, name_original='ARTFX J 架空キャラ', name_ko='ARTFX J 가공 캐릭터',
                    official_url='https://example.com/p', scale='1/8')
    session.add(figure); session.flush()
    variant = FigureVariant(figure_id=figure.id, variant_key='standard', jan_code=None)
    session.add(variant); session.commit()
    return figure, variant


def _app(session, monkeypatch):
    from app.core.config import get_settings
    monkeypatch.setattr(get_settings(), 'admin_token', 'fixture-admin-token-0123456789')
    app = FastAPI(); app.include_router(router)
    app.dependency_overrides[get_db] = lambda: session
    return TestClient(app)


def test_history_keeps_every_observation_and_manual_match_survives_reobservation(session, monkeypatch):
    from app.models.retail import RetailOfferHistory
    figure, variant = _catalog(session)
    row = {**observation(), 'title_raw': 'ARTFX J 가공 캐릭터 1/8', 'observed_at': '2026-11-01T00:00:00+00:00'}
    save_offer(session, 'maniahouse', row); session.commit()
    save_offer(session, 'maniahouse', {**row, 'sale_price': 8000, 'observed_at': '2026-11-02T00:00:00+00:00'}); session.commit()
    save_offer(session, 'maniahouse', row); session.commit()  # stale re-delivery adds nothing
    assert [h.sale_price for h in session.scalars(select(RetailOfferHistory).order_by(RetailOfferHistory.observed_at))] == [10000, 8000]
    c = _app(session, monkeypatch)
    admin = {'X-Admin-Token': 'fixture-admin-token-0123456789'}
    assert c.get('/api/admin/retail-matches').status_code == 403
    queue = c.get('/api/admin/retail-matches', headers=admin).json()
    assert queue['total'] == 1 and queue['items'][0]['candidates'][0]['variant_id'] == variant.id
    listing_id = queue['items'][0]['listing_id']
    assert c.post(f'/api/admin/retail-matches/{listing_id}', json={'variant_id': variant.id}).status_code == 403
    assert c.post(f'/api/admin/retail-matches/{listing_id}', json={'variant_id': variant.id}, headers=admin).status_code == 200
    # A later observation of the same listing keeps the confirmed link.
    save_offer(session, 'maniahouse', {**row, 'sale_price': 7000, 'observed_at': '2026-11-03T00:00:00+00:00'}); session.commit()
    assert session.get(RetailListing, listing_id).catalog_variant_id == variant.id
    history = c.get(f'/api/figures/{figure.id}/price-history?days=730').json()
    assert [p['sale_price'] for p in history['series'][0]['points']] == [10000, 8000, 7000]
    assert history['lowest_observed'] == 7000
    assert c.get('/api/admin/retail-matches', headers=admin).json()['total'] == 0
    assert c.delete(f'/api/admin/retail-matches/{listing_id}', headers=admin).json()['catalog_variant_id'] is None

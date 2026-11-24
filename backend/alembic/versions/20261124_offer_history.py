"""Add append-only domestic price history and seed it from the latest offers."""
from alembic import op
from sqlalchemy import text

from app.models.retail import RetailOfferHistory


revision = '20261124_offer_history'
down_revision = '20261116_retail_offers'
branch_labels = depends_on = None


def upgrade():
    RetailOfferHistory.__table__.create(op.get_bind(), checkfirst=True)
    # Keep the observations collected so far as the first history point.
    op.get_bind().execute(text(
        'INSERT INTO retailer_offer_history (listing_id, observed_at, list_price, sale_price, availability) '
        'SELECT listing_id, observed_at, list_price, sale_price, availability FROM retailer_offers '
        'ON CONFLICT (listing_id, observed_at) DO NOTHING'))


def downgrade():
    RetailOfferHistory.__table__.drop(op.get_bind(), checkfirst=True)

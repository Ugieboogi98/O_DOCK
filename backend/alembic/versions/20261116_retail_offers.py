"""Add domestic listings and latest offers without changing catalog records."""
from alembic import op

from app.models.retail import RetailListing, RetailOffer


revision = '20261116_retail_offers'
down_revision = '20261112_instagram_events'
branch_labels = depends_on = None


def upgrade():
    RetailListing.__table__.create(op.get_bind(), checkfirst=True)
    RetailOffer.__table__.create(op.get_bind(), checkfirst=True)


def downgrade():
    RetailOffer.__table__.drop(op.get_bind(), checkfirst=True)
    RetailListing.__table__.drop(op.get_bind(), checkfirst=True)

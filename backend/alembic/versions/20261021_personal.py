"""Personal collection tables; preserves existing products."""
from alembic import op
import sqlalchemy as sa
revision='20261021_personal'
down_revision='cac17c89def2'
branch_labels=None
depends_on=None

def upgrade():
    op.create_table('favorites',sa.Column('figure_id',sa.Integer(),sa.ForeignKey('figures.id'),primary_key=True),sa.Column('created_at',sa.DateTime(timezone=True),nullable=False))
    op.create_table('purchases',sa.Column('id',sa.Integer(),primary_key=True),sa.Column('variant_id',sa.Integer(),sa.ForeignKey('figure_variants.id'),nullable=False),sa.Column('amount',sa.Numeric(14,2),nullable=False),sa.Column('currency',sa.String(3),nullable=False),sa.Column('purchased_on',sa.String(10),nullable=False),sa.Column('delivery_status',sa.String(20),nullable=False),sa.Column('shop',sa.String(200),nullable=False),sa.Column('memo',sa.Text(),nullable=False),sa.Column('created_at',sa.DateTime(timezone=True),nullable=False),sa.CheckConstraint('amount >= 0'))
    op.create_index('ix_purchases_variant_id','purchases',['variant_id'])
    op.create_table('exchange_rates',sa.Column('pair',sa.String(10),primary_key=True),sa.Column('rate',sa.Numeric(18,8),nullable=False),sa.Column('rate_date',sa.String(10),nullable=False),sa.Column('source_url',sa.Text(),nullable=False),sa.Column('checked_at',sa.DateTime(timezone=True),nullable=False))

def downgrade():
    op.drop_table('exchange_rates');op.drop_table('purchases');op.drop_table('favorites')

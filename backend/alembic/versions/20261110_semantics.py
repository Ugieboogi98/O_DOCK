"""Add derived Japanese/Korean product semantics; preserve catalog and personal data."""
from alembic import op
import sqlalchemy as sa
revision = '20261110_semantics'
down_revision = '20261023_korean'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('product_semantics',
        sa.Column('figure_id', sa.Integer(), sa.ForeignKey('figures.id', ondelete='CASCADE'), primary_key=True),
        sa.Column('source_hash', sa.String(64), nullable=False),
        sa.Column('source', sa.JSON(), nullable=False),
        sa.Column('fields', sa.JSON(), nullable=False),
        sa.Column('status', sa.String(20), nullable=False),
        sa.Column('model', sa.String(200), nullable=False),
        sa.Column('issues', sa.JSON(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False))
    op.create_index('ix_product_semantics_status', 'product_semantics', ['status'])


def downgrade():
    op.drop_table('product_semantics')

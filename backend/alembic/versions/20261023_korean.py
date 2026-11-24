"""Add resumable Korean translations; no original data is altered."""
from alembic import op
import sqlalchemy as sa
revision='20261023_korean'
down_revision='20261021_personal'
branch_labels=None
depends_on=None

def upgrade():
    op.create_table('korean_profiles',
        sa.Column('figure_id',sa.Integer(),sa.ForeignKey('figures.id',ondelete='CASCADE'),primary_key=True),
        sa.Column('source_hash',sa.String(64),nullable=False),sa.Column('fields',sa.JSON(),nullable=False),
        sa.Column('model',sa.String(200),nullable=False),sa.Column('translated_at',sa.DateTime(timezone=True),nullable=False))
    op.create_table('korean_chunks',
        sa.Column('document_id',sa.Integer(),sa.ForeignKey('source_documents.id',ondelete='CASCADE'),primary_key=True),
        sa.Column('part',sa.Integer(),primary_key=True),sa.Column('source_hash',sa.String(64),nullable=False),
        sa.Column('body_ko',sa.Text(),nullable=False),sa.Column('model',sa.String(200),nullable=False),
        sa.Column('translated_at',sa.DateTime(timezone=True),nullable=False))

def downgrade():
    op.drop_table('korean_chunks')
    op.drop_table('korean_profiles')

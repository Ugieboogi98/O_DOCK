"""Isolated Instagram event review tables; no catalog data changes."""
from alembic import op
from app.integrations.instagram.store import metadata

revision = '20261112_instagram_events'
down_revision = '20261110_users'
branch_labels = depends_on = None


def upgrade():
    metadata.create_all(op.get_bind(), checkfirst=True)


def downgrade():
    metadata.drop_all(op.get_bind(), checkfirst=True)

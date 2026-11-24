"""Adopt legacy personal records into the administrator's account without changing IDs."""
from alembic import op
import sqlalchemy as sa
from datetime import datetime, timezone

revision = '20261110_users'
down_revision = '20261110_semantics'
branch_labels = depends_on = None


def upgrade():
    users = op.create_table('users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('username', sa.String(40), nullable=False, unique=True),
        sa.Column('password_hash', sa.Text(), nullable=True),
        sa.Column('failed_attempts', sa.Integer(), nullable=False),
        sa.Column('locked_until', sa.DateTime(timezone=True)),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False))
    op.bulk_insert(users, [{'id': 1, 'username': 'admin', 'password_hash': None,
                           'failed_attempts': 0, 'created_at': datetime.now(timezone.utc)}])
    if op.get_bind().dialect.name == 'postgresql':
        op.execute("SELECT setval(pg_get_serial_sequence('users','id'), 1)")
    op.create_table('user_sessions',
        sa.Column('token_hash', sa.String(64), primary_key=True),
        sa.Column('user_id', sa.Integer(), sa.ForeignKey('users.id', ondelete='CASCADE'), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False))
    op.create_index('ix_user_sessions_user_id', 'user_sessions', ['user_id'])
    for table in ('favorites', 'purchases'):
        with op.batch_alter_table(table) as batch:
            batch.add_column(sa.Column('user_id', sa.Integer(), nullable=False, server_default='1'))
        with op.batch_alter_table(table, naming_convention={'pk': '%(table_name)s_pkey'}) as batch:
            batch.alter_column('user_id', existing_type=sa.Integer(), server_default=None)
            batch.create_foreign_key(f'fk_{table}_user_id', 'users', ['user_id'], ['id'])
            if table == 'favorites':
                batch.drop_constraint('favorites_pkey', type_='primary')
                batch.create_primary_key('favorites_pkey', ['figure_id', 'user_id'])
            else:
                batch.create_index('ix_purchases_user_id', ['user_id'])


def downgrade():
    # A single-owner schema cannot preserve overlapping multi-user favorites.
    # Require an explicit export/merge plan instead of silently discarding data.
    raise RuntimeError('USER_DATA_EXPORT_REQUIRED: ownership migration cannot be safely downgraded')

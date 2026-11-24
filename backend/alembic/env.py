from app.models import semantics  # register derived entity table
from app.models import korean  # register translation tables
from app.models import retail  # register domestic store listings and offers
from alembic import context
from sqlalchemy import create_engine,pool
from app.core.config import get_settings
from app.models.entities import Base
from app.integrations.instagram.store import metadata as event_metadata
config=context.config
target_metadata=[Base.metadata, event_metadata]
def offline():
    context.configure(url=get_settings().database_url,target_metadata=target_metadata,literal_binds=True,dialect_opts={'paramstyle':'named'})
    with context.begin_transaction():context.run_migrations()
def online():
    engine=create_engine(get_settings().database_url,poolclass=pool.NullPool, connect_args={"prepare_threshold": None})
    with engine.connect() as connection:
        context.configure(connection=connection,target_metadata=target_metadata)
        with context.begin_transaction():context.run_migrations()
if context.is_offline_mode():offline()
else:online()

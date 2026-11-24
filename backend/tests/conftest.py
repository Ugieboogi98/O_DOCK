import os, json
from pathlib import Path
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.database import get_db
from app.core.config import get_settings
from app.models.entities import Base
from app.main import app
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def engine():
    url = os.environ.get("TEST_DATABASE_URL")
    if not url:
        pytest.skip("Set TEST_DATABASE_URL to a dedicated PostgreSQL test database")
    e = create_engine(
        url, connect_args={"prepare_threshold": None}, pool_size=1, max_overflow=0
    )
    Base.metadata.create_all(e)
    yield e
    e.dispose()


@pytest.fixture
def db(engine):
    from scripts.seed import seed

    with engine.connect() as conn:
        outer = conn.begin()
        s = sessionmaker(
            bind=conn, join_transaction_mode="create_savepoint", expire_on_commit=False
        )()
        seed(s, json.loads((get_settings().data_dir / "figures.json").read_text()))
        yield s
        s.close()
        outer.rollback()


@pytest.fixture
def client(db):
    app.dependency_overrides[get_db] = lambda: db
    with TestClient(app, raise_server_exceptions=False) as c:
        yield c
    app.dependency_overrides.clear()

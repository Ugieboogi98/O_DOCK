import importlib.util
from pathlib import Path
from sqlalchemy import create_engine, inspect
from alembic.migration import MigrationContext
from alembic.operations import Operations


def test_migration_adds_and_removes_only_derived_table():
    migration = Path(__file__).parents[1] / 'alembic/versions/20261110_semantics.py'
    spec = importlib.util.spec_from_file_location('semantics_revision', migration)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    engine = create_engine('sqlite://')
    with engine.begin() as conn:
        conn.exec_driver_sql('CREATE TABLE figures (id INTEGER PRIMARY KEY)')
        conn.exec_driver_sql('INSERT INTO figures VALUES (42)')
        with Operations.context(MigrationContext.configure(conn)):
            module.upgrade()
            assert inspect(conn).has_table('product_semantics')
            assert conn.exec_driver_sql('SELECT id FROM figures').scalar() == 42
            module.downgrade()
            assert not inspect(conn).has_table('product_semantics')
            assert conn.exec_driver_sql('SELECT id FROM figures').scalar() == 42

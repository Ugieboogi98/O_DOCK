"""Portable PostgreSQL schema + data snapshot. Restore into an empty database."""

import argparse, json
from datetime import date, datetime
from decimal import Decimal
from pathlib import Path
from sqlalchemy import select, text
from sqlalchemy.schema import CreateTable, CreateIndex
from sqlalchemy.dialects import postgresql
from app.core.database import engine
from app.models.entities import Base


def literal(v):
    if v is None:
        return "NULL"
    if isinstance(v, bool):
        return "TRUE" if v else "FALSE"
    if isinstance(v, (int, float, Decimal)):
        return str(v)
    if isinstance(v, (dict, list)):
        v = json.dumps(v, ensure_ascii=False)
    if isinstance(v, (date, datetime)):
        v = v.isoformat()
    return "'" + str(v).replace("'", "''") + "'"


def export(path):
    dialect = postgresql.dialect()
    lines = [
        "-- Figure Archive AI: restore into a new empty PostgreSQL database.",
        "BEGIN;",
        "SET standard_conforming_strings = on;",
    ]
    with engine.connect() as conn:
        for table in Base.metadata.sorted_tables:
            lines.append(str(CreateTable(table).compile(dialect=dialect)) + ";")
            for idx in table.indexes:
                lines.append(str(CreateIndex(idx).compile(dialect=dialect)) + ";")
            columns = ",".join('"' + c.name + '"' for c in table.columns)
            rows = conn.execute(select(table).order_by(table.c.id)).all()
            for row in rows:
                lines.append(
                    f'INSERT INTO "{table.name}" ({columns}) VALUES ('
                    + ",".join(literal(v) for v in row)
                    + ");"
                )
            if rows:
                lines.append(
                    f"SELECT setval(pg_get_serial_sequence('{table.name}','id'), (SELECT MAX(id) FROM {table.name}), true);"
                )
        revision = conn.execute(
            text("SELECT version_num FROM alembic_version")
        ).scalar()
        lines.extend(
            [
                "CREATE TABLE alembic_version (version_num VARCHAR(32) PRIMARY KEY);",
                f"INSERT INTO alembic_version VALUES ({literal(revision)});",
                "COMMIT;",
            ]
        )
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")
    return len(lines)


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--out", default="../data/database.sql")
    args = p.parse_args()
    print({"sql_statements": export(args.out)})

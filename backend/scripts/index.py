import argparse
from app.core.database import SessionLocal
from app.rag.store import index_all

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument(
        "--reset",
        action="store_true",
        help="Explicitly delete both collections before reindexing after embedding model changes",
    )
    a = p.parse_args()
    with SessionLocal() as db:
        print(index_all(db, reset=a.reset))

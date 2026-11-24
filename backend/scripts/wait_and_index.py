import time
from app.rag.store import client, index_all
from app.core.database import SessionLocal

if __name__ == "__main__":
    for attempt in range(30):
        try:
            client().heartbeat()
            break
        except Exception:
            if attempt == 29:
                raise RuntimeError("Chroma readiness timeout") from None
            time.sleep(2)
    with SessionLocal() as db:
        print(index_all(db))

"""Optional Compose worker. PostgreSQL-backed cooldown governs every tick."""

import argparse
import json
import signal
import threading
from app.services.catalog_refresh import start_refresh


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--interval",
        type=int,
        default=3600,
        help="Seconds between cooldown checks (minimum 60)",
    )
    a = p.parse_args()
    if a.interval < 60:
        p.error("--interval must be >= 60")
    stop = threading.Event()
    for sig in (signal.SIGTERM, signal.SIGINT):
        signal.signal(sig, lambda *_: stop.set())
    while not stop.is_set():
        try:
            print(json.dumps(start_refresh(), ensure_ascii=False), flush=True)
        except Exception as exc:
            print(
                json.dumps({"state": "failed", "error": type(exc).__name__}), flush=True
            )
        stop.wait(a.interval)


if __name__ == "__main__":
    main()

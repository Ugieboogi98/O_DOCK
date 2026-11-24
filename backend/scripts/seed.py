"""Compatibility CLI for idempotent seed import."""

from app.services.seed_import import *

if __name__ == "__main__":
    with SessionLocal() as db:
        print(
            {
                "new_figures": seed(
                    db,
                    json.loads((get_settings().data_dir / "figures.json").read_text()),
                )
            }
        )

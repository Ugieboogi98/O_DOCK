"""Compatibility CLI; shared BNKR pipeline lives in app.services."""

from app.services.bnkr_catalog import *

if __name__ == "__main__":
    raise SystemExit(main())

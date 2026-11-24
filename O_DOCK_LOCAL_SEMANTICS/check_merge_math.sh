#!/usr/bin/env bash
set -euo pipefail
python -m pip install 'pytest>=8,<9'
python -m pytest -q -p no:cacheprovider /work/tests/test_streaming_merge.py

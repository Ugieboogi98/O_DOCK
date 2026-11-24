#!/usr/bin/env sh
set -eu
cd "$(dirname "$0")/.."
[ -f .env ] || { printf '%s\n' 'Create .env from .env.example and configure it before startup.' >&2; exit 1; }
docker compose -p figure-archive-ai up -d postgres chroma
docker compose -p figure-archive-ai stop backend frontend
docker compose -p figure-archive-ai build backend frontend
docker compose -p figure-archive-ai run --rm --no-deps backend alembic upgrade head
docker compose -p figure-archive-ai up -d --no-deps backend frontend
printf '%s\n' 'Ready: http://localhost:8080 (no seed or catalog worker started)'

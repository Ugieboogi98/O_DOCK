#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../.."
mode="${1:-audit}"
if [[ "$mode" != audit && "$mode" != apply && "$mode" != restore ]]; then
  echo 'Usage: bash tools/image_dedup/run.sh audit|apply|restore [extra options]'; exit 1
fi
if [[ $# -gt 0 ]]; then shift; fi
export MSYS_NO_PATHCONV=1
mkdir -p backups/migrations/image_dedup
docker compose -p figure-archive-ai exec -T backend mkdir -p /app/media/tools
docker compose -p figure-archive-ai cp ./tools/image_dedup backend:/app/media/tools/
if ! docker compose -p figure-archive-ai exec -T -e PYTHONPATH=/tmp/odock_image_libs:/app backend python -c 'import PIL' >/dev/null 2>&1; then
  docker compose -p figure-archive-ai exec -T backend python -m pip install --target /tmp/odock_image_libs -r /app/media/tools/image_dedup/requirements.txt
fi
report='/app/media/image_dedup_reports/audit.json'
if [[ "$mode" == audit ]]; then
  docker compose -p figure-archive-ai stop catalog-worker
  docker compose -p figure-archive-ai exec -T -e PYTHONPATH=/tmp/odock_image_libs:/app backend python /app/media/tools/image_dedup/image_dedup.py audit --report "$report" "$@"
  docker compose -p figure-archive-ai cp backend:/app/media/image_dedup_reports/audit.json ./backups/migrations/image_dedup/audit.json
  docker compose -p figure-archive-ai cp backend:/app/media/image_dedup_reports/audit.html ./backups/migrations/image_dedup/audit.html
  echo 'Open backups/migrations/image_dedup/audit.html to compare candidates.'
elif [[ "$mode" == apply ]]; then
  docker compose -p figure-archive-ai stop catalog-worker
  stamp="$(date +%Y%m%d_%H%M%S)_$$"
  backup="backups/migrations/image_dedup/before_${stamp}.dump"
  docker compose -p figure-archive-ai exec -T postgres sh -c 'pg_dump -U "$POSTGRES_USER" -d "$POSTGRES_DB" -Fc' > "$backup"
  test -s "$backup"
  docker compose -p figure-archive-ai exec -T postgres pg_restore --list < "$backup" > /dev/null
  journal="/app/media/image_dedup_reports/apply_${stamp}.json"
  docker compose -p figure-archive-ai exec -T -e PYTHONPATH=/tmp/odock_image_libs:/app backend python /app/media/tools/image_dedup/image_dedup.py apply --report "$report" --journal "$journal" "$@"
  docker compose -p figure-archive-ai cp "backend:$journal" ./backups/migrations/image_dedup/
  echo "Restore command: bash tools/image_dedup/run.sh restore --report $journal"
else
  if [[ $# -eq 0 ]]; then echo 'restore requires --report /app/media/image_dedup_reports/apply_....json'; exit 1; fi
  docker compose -p figure-archive-ai stop catalog-worker
  docker compose -p figure-archive-ai exec -T -e PYTHONPATH=/tmp/odock_image_libs:/app backend python /app/media/tools/image_dedup/image_dedup.py restore "$@"
fi

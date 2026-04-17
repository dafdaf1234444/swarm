#!/usr/bin/env bash
set -Eeuo pipefail

COUNT=$(ls tasks/lanes/lane-*.md 2>/dev/null | wc -l)

if [ "$COUNT" -lt 5 ]; then
  ID=$(date +%s)
  cat > "tasks/lanes/lane-$ID.md" <<EOL
# lane-$ID

status=READY
owner=
created_at=$(date -u +%Y-%m-%dT%H:%M:%SZ)
updated_at=$(date -u +%Y-%m-%dT%H:%M:%SZ)
focus=Auto-generated task
allowed_paths=tasks/lanes/,memory/logs/,runtime/
next_step=Do something small and log it
EOL

  echo "created lane-$ID"
fi

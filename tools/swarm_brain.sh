#!/usr/bin/env bash
set -Eeuo pipefail

MAX_LANES=6
DIR="tasks/lanes"
mkdir -p "$DIR"

COUNT=$(ls $DIR/*.md 2>/dev/null | grep -v TEMPLATE | wc -l || true)

if [ "$COUNT" -lt "$MAX_LANES" ]; then
  ID=$(date +%s)
  cat > "$DIR/lane-$ID.md" <<EOL
# lane-$ID

status=READY
owner=
created_at=$(date -u +%Y-%m-%dT%H:%M:%SZ)
updated_at=$(date -u +%Y-%m-%dT%H:%M:%SZ)
focus=Auto expanding swarm
allowed_paths=tasks/lanes/,memory/logs/,runtime/
next_step=Append log + small mutation
proof_of_novelty=Do something slightly different
EOL
  echo "created lane-$ID"
fi

FILE=$(ls $DIR/*.md 2>/dev/null | shuf | head -n1 || true)
if [ -n "$FILE" ]; then
  echo "- $(date -u +%T) evolve-$RANDOM" >> "$FILE"
fi

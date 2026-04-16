#!/usr/bin/env bash
set -euo pipefail

SEEN_FILE=".loop_seen"
touch "$SEEN_FILE"

while true; do
  ID="$(
    python3 tools/orient.py |
    grep -o 'L-[0-9]\+' |
    grep -vxFf "$SEEN_FILE" |
    head -n 1 || true
  )"

  if [ -z "$ID" ]; then
    echo "No unseen IDs left. Resetting..."
    : > "$SEEN_FILE"
    sleep 2
    continue
  fi

  echo "$ID" >> "$SEEN_FILE"
  echo "Running $ID"
  ./tools/resolve_one.sh "$ID"

  sleep 1
done

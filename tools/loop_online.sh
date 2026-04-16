#!/usr/bin/env bash
set -euo pipefail

BRANCH="$(git branch --show-current)"
SEEN_FILE=".loop_seen"
touch "$SEEN_FILE"

while true; do
  echo "=== GODDING SYNC DOWN ==="
  git add .
  git commit -m "auto: checkpoint before sync" || true
  git pull --no-rebase origin "$BRANCH" || true

  echo "=== STATE SYNC ==="
  python3 tools/sync_state.py || true
  python3 tools/validate_beliefs.py || true
  bash tools/check.sh --quick || true

  echo "=== PICK NEXT ==="
  ID="$(
    python3 tools/orient.py |
    grep -o 'L-[0-9]\+' |
    grep -vxFf "$SEEN_FILE" |
    head -n 1 || true
  )"

  if [ -z "$ID" ]; then
    echo "No unseen IDs left. Resetting seen list."
    : > "$SEEN_FILE"
    sleep 5
    continue
  fi

  echo "$ID" >> "$SEEN_FILE"
  echo "processing $ID"

  ./tools/resolve_one.sh "$ID" || true

  echo "=== WRITEBACK ==="
  python3 tools/sync_state.py || true
  python3 tools/validate_beliefs.py || true
  git add .
  git commit -m "auto: processed $ID" || true

  echo "=== GODDING SYNC UP ==="
  git push -u origin "$BRANCH" || true

  sleep 2
done

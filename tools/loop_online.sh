#!/usr/bin/env bash
set -euo pipefail

BRANCH="$(git branch --show-current)"
SEEN_FILE=".loop_seen"
touch "$SEEN_FILE"

while true; do
  git fetch origin
  git pull --rebase origin "$BRANCH" || true

  ID="$(
    python3 tools/orient.py |
    grep -o 'L-[0-9]\+' |
    grep -vxFf "$SEEN_FILE" |
    head -n 1 || true
  )"

  if [ -z "$ID" ]; then
    : > "$SEEN_FILE"
    sleep 5
    continue
  fi

  echo "$ID" >> "$SEEN_FILE"
  ./tools/resolve_one.sh "$ID" || true

  git push origin "$BRANCH" || true

  sleep 2
done

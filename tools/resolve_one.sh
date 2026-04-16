#!/usr/bin/env bash
set -euo pipefail

ID="${1:?usage: ./tools/resolve_one.sh L-1234}"

echo "=== ORIENT ==="
python3 tools/orient.py | grep -C 2 "$ID" || true
echo ""
echo "=== AUTO DECIDE ==="

action="$(python3 tools/decide_one.py "$ID" || echo s)"
echo "auto=$action for $ID"
read -t 3 -p "override? (k/d/s, wait=auto): " manual || true
if [ -n "${manual:-}" ]; then
  action="$manual"
fi

if [ "$action" = "d" ]; then
  echo "Edit/delete manually for $ID, then press Enter"
  read
  git add .
  git commit -m "resolve $ID" || true
elif [ "$action" = "k" ]; then
  git commit --allow-empty -m "acknowledge $ID" || true
else
  echo "Skipped $ID"
fi

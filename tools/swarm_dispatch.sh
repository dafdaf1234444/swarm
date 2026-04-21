#!/data/data/com.termux/files/usr/bin/bash
while true; do
  echo "=============================="
  echo "SWARM DISPATCH CYCLE"
  echo "=============================="

  python3 tools/orient.py 2>/dev/null || true
  bash tools/check.sh --quick 2>/dev/null || true
  python3 tools/sync_state.py 2>/dev/null || true
  python3 tools/validate_beliefs.py 2>/dev/null || true

  git add -A
  git commit -m "swarm: auto cycle" || true
  git pull --rebase || true
  git push || true

  echo "sleeping 30s"
  sleep 30
done

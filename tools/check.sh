#!/bin/bash
# Universal swarm validation — call from any tool at session start/end.
# Replaces tool-specific hooks for non-Claude tools.
# Usage: bash tools/check.sh [--quick]
set -e
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

QUICK=""
[ "$1" = "--quick" ] && QUICK="--quick"

echo "=== SWARM CHECK ==="

# 1. Belief integrity (critical)
if python3 tools/validate_beliefs.py $QUICK 2>/dev/null | grep -q "RESULT: FAIL"; then
    echo "FAIL: Belief validation failed. Fix before committing."
    python3 tools/validate_beliefs.py --quick
    exit 1
fi
echo "  Beliefs: PASS"

# 2. Maintenance (informational)
python3 tools/maintenance.py 2>/dev/null
echo ""

# 3. Proxy K (if not quick)
if [ -z "$QUICK" ]; then
    python3 tools/proxy_k.py 2>/dev/null
fi

echo "=== CHECK COMPLETE ==="

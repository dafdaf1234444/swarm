#!/bin/bash
# Universal swarm validation — call from any tool at session start/end.
# Replaces tool-specific hooks for non-Claude tools.
# Usage: bash tools/check.sh [--quick]
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

QUICK=""
if [ "${1:-}" = "--quick" ]; then
    QUICK="--quick"
fi

echo "=== SWARM CHECK ==="

# 1. Belief integrity (critical)
if python3 tools/validate_beliefs.py $QUICK 2>/dev/null | grep -q "RESULT: FAIL"; then
    echo "FAIL: Belief validation failed. Fix before committing."
    python3 tools/validate_beliefs.py --quick
    exit 1
fi
echo "  Beliefs: PASS"

# 2. Maintenance (informational)
python3 tools/maintenance.py $QUICK 2>/dev/null
echo ""

# 3. Bulletin regression suite (if not quick)
if [ -z "$QUICK" ] && [ -f "tools/test_bulletin.py" ]; then
    if ! python3 tools/test_bulletin.py >/dev/null 2>&1; then
        echo "FAIL: Bulletin regression suite failed."
        python3 tools/test_bulletin.py
        exit 1
    fi
    echo "  Bulletin regression: PASS"
fi

# 4. Proxy K (if not quick)
if [ -z "$QUICK" ]; then
    python3 tools/proxy_k.py 2>/dev/null
fi

echo "=== CHECK COMPLETE ==="

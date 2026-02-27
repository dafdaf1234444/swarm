#!/bin/bash
# Universal swarm validation — call from any tool at session start/end.
# Replaces tool-specific hooks for non-Claude tools.
# Usage: bash tools/check.sh [--quick]
set -euo pipefail
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$REPO_ROOT"

choose_python() {
    if command -v python3 >/dev/null 2>&1 && python3 -c "import sys" >/dev/null 2>&1; then
        PYTHON_CMD=(python3)
        return 0
    fi
    if command -v python >/dev/null 2>&1 && python -c "import sys" >/dev/null 2>&1; then
        PYTHON_CMD=(python)
        return 0
    fi
    # Windows launcher fallback for shells where python/python3 are not on PATH.
    if command -v py >/dev/null 2>&1 && py -3 -c "import sys" >/dev/null 2>&1; then
        PYTHON_CMD=(py -3)
        return 0
    fi
    return 1
}

declare -a PYTHON_CMD=()
if ! choose_python; then
    echo "FAIL: No runnable python interpreter found (python3/python/py -3)."
    exit 1
fi

ARGS=()
if [ "${1:-}" = "--quick" ]; then
    ARGS+=(--quick)
fi

echo "=== SWARM CHECK ==="

# 1. Belief integrity (critical)
if "${PYTHON_CMD[@]}" tools/validate_beliefs.py "${ARGS[@]}" 2>/dev/null | grep -q "RESULT: FAIL"; then
    echo "FAIL: Belief validation failed. Fix before committing."
    "${PYTHON_CMD[@]}" tools/validate_beliefs.py --quick
    exit 1
fi
echo "  Beliefs: PASS"

# 2. Maintenance (informational)
if ! "${PYTHON_CMD[@]}" tools/maintenance.py "${ARGS[@]}"; then
    echo "FAIL: maintenance check failed."
    exit 1
fi
echo ""

# 3. Bulletin regression suite (if not quick)
if [ "${#ARGS[@]}" -eq 0 ] && [ -f "tools/test_bulletin.py" ]; then
    if ! "${PYTHON_CMD[@]}" tools/test_bulletin.py >/dev/null 2>&1; then
        echo "FAIL: Bulletin regression suite failed."
        "${PYTHON_CMD[@]}" tools/test_bulletin.py
        exit 1
    fi
    echo "  Bulletin regression: PASS"
fi

# 4. Wiki swarm regression suite (if not quick)
if [ "${#ARGS[@]}" -eq 0 ] && [ -f "tools/test_wiki_swarm.py" ]; then
    if ! "${PYTHON_CMD[@]}" tools/test_wiki_swarm.py >/dev/null 2>&1; then
        echo "FAIL: Wiki swarm regression suite failed."
        "${PYTHON_CMD[@]}" tools/test_wiki_swarm.py
        exit 1
    fi
    echo "  Wiki swarm regression: PASS"
fi

# 5. Swarm parse regression suite (if not quick)
if [ "${#ARGS[@]}" -eq 0 ] && [ -f "tools/test_swarm_parse.py" ]; then
    if ! "${PYTHON_CMD[@]}" tools/test_swarm_parse.py >/dev/null 2>&1; then
        echo "FAIL: Swarm parse regression suite failed."
        "${PYTHON_CMD[@]}" tools/test_swarm_parse.py
        exit 1
    fi
    echo "  Swarm parse regression: PASS"
fi

# 6. Colony regression suite (if not quick)
if [ "${#ARGS[@]}" -eq 0 ] && [ -f "tools/test_colony.py" ]; then
    if ! "${PYTHON_CMD[@]}" tools/test_colony.py >/dev/null 2>&1; then
        echo "FAIL: Colony regression suite failed."
        "${PYTHON_CMD[@]}" tools/test_colony.py
        exit 1
    fi
    echo "  Colony regression: PASS"
fi

# 7. Proxy K (if not quick)
if [ "${#ARGS[@]}" -eq 0 ]; then
    "${PYTHON_CMD[@]}" tools/proxy_k.py 2>/dev/null
fi

echo "=== CHECK COMPLETE ==="

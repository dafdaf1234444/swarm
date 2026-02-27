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

run_suite() {
    local label="$1"
    local path="$2"
    if [ ! -f "$path" ]; then
        return 0
    fi
    if ! "${PYTHON_CMD[@]}" "$path" >/dev/null 2>&1; then
        echo "FAIL: ${label} failed."
        "${PYTHON_CMD[@]}" "$path"
        exit 1
    fi
    echo "  ${label}: PASS"
}

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
    run_suite "Bulletin regression" "tools/test_bulletin.py"
fi

# 4. Wiki swarm regression suite (if not quick)
if [ "${#ARGS[@]}" -eq 0 ] && [ -f "tools/test_wiki_swarm.py" ]; then
    run_suite "Wiki swarm regression" "tools/test_wiki_swarm.py"
fi

# 5. Swarm parse regression suite (if not quick)
if [ "${#ARGS[@]}" -eq 0 ] && [ -f "tools/test_swarm_parse.py" ]; then
    run_suite "Swarm parse regression" "tools/test_swarm_parse.py"
fi

# 6. Colony regression suite (if not quick)
if [ "${#ARGS[@]}" -eq 0 ] && [ -f "tools/test_colony.py" ]; then
    run_suite "Colony regression" "tools/test_colony.py"
fi

# 7. PR intake regression suite (if not quick)
if [ "${#ARGS[@]}" -eq 0 ] && [ -f "tools/test_swarm_pr.py" ]; then
    run_suite "Swarm PR regression" "tools/test_swarm_pr.py"
fi

# 8. Swarm lanes regression suite (if not quick)
if [ "${#ARGS[@]}" -eq 0 ] && [ -f "tools/test_swarm_lanes.py" ]; then
    run_suite "Swarm lanes regression" "tools/test_swarm_lanes.py"
fi

# 9. Mission constraints regression suite (if not quick)
if [ "${#ARGS[@]}" -eq 0 ] && [ -f "tools/test_mission_constraints.py" ]; then
    run_suite "Mission constraints regression" "tools/test_mission_constraints.py"
fi

# 10. Repair regression suite (if not quick)
if [ "${#ARGS[@]}" -eq 0 ] && [ -f "tools/test_repair.py" ]; then
    run_suite "Repair regression" "tools/test_repair.py"
fi

# 11. NK analyze regression suite (if not quick)
if [ "${#ARGS[@]}" -eq 0 ] && [ -f "tools/test_nk_analyze.py" ]; then
    run_suite "NK analyze regression" "tools/test_nk_analyze.py"
fi

# 12. Additional tool regressions auto-discovery (if not quick)
if [ "${#ARGS[@]}" -eq 0 ]; then
    CORE_TESTS=(
        "tools/test_bulletin.py"
        "tools/test_wiki_swarm.py"
        "tools/test_swarm_parse.py"
        "tools/test_colony.py"
        "tools/test_swarm_pr.py"
        "tools/test_swarm_lanes.py"
        "tools/test_mission_constraints.py"
        "tools/test_repair.py"
        "tools/test_nk_analyze.py"
    )
    EXTRA_COUNT=0
    while IFS= read -r test_path; do
        SKIP=0
        for core in "${CORE_TESTS[@]}"; do
            if [ "$test_path" = "$core" ]; then
                SKIP=1
                break
            fi
        done
        if [ "$SKIP" -eq 1 ]; then
            continue
        fi
        test_name="$(basename "$test_path" .py)"
        run_suite "Additional regression (${test_name})" "$test_path"
        EXTRA_COUNT=$((EXTRA_COUNT + 1))
    done < <(find tools -maxdepth 1 -type f -name 'test_*.py' | sort)
    if [ "$EXTRA_COUNT" -gt 0 ]; then
        echo "  Additional tool regressions: PASS (${EXTRA_COUNT} suites)"
    fi
fi

# 13. Orient.py smoke test (if not quick)
if [ "${#ARGS[@]}" -eq 0 ] && [ -f "tools/orient.py" ]; then
    ORIENT_OUT=$("${PYTHON_CMD[@]}" tools/orient.py --brief 2>&1)
    if echo "$ORIENT_OUT" | grep -q "=== ORIENT"; then
        echo "  Orient smoke test: PASS"
    else
        echo "FAIL: orient.py produced unexpected output."
        echo "$ORIENT_OUT"
        exit 1
    fi
fi

# 14. Proxy K (if not quick)
if [ "${#ARGS[@]}" -eq 0 ]; then
    "${PYTHON_CMD[@]}" tools/proxy_k.py 2>/dev/null
fi

echo "=== CHECK COMPLETE ==="

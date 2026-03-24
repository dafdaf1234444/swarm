#!/bin/bash
# Document consistency: detect stale cross-references to changed PHIL claims.
# Stigmergic enforcement — makes drift visible every session.
# NOTICE only in quick mode; blocks in full mode if HIGH issues found.
if [ -f "tools/consistency_check.py" ]; then
    CC_ARGS=()
    if [ "$GUARD_MODE" = "quick" ]; then
        CC_ARGS+=(--quick)
    fi
    CC_OUT=$("${PYTHON_CMD[@]}" tools/consistency_check.py "${CC_ARGS[@]}" --json 2>&1) || true
    if [ -n "$CC_OUT" ]; then
        HIGH_COUNT=$(echo "$CC_OUT" | "${PYTHON_CMD[@]}" -c "
import json, sys
try: d = json.load(sys.stdin); print(d.get('high', 0))
except: print(0)
" 2>/dev/null || echo 0)
        TOTAL=$(echo "$CC_OUT" | "${PYTHON_CMD[@]}" -c "
import json, sys
try: d = json.load(sys.stdin); print(d.get('total_issues', 0))
except: print(0)
" 2>/dev/null || echo 0)
        if [ "${HIGH_COUNT}" -gt 0 ]; then
            echo "  Consistency: ${TOTAL} issues (${HIGH_COUNT} HIGH) — run: python3 tools/consistency_check.py"
        elif [ "${TOTAL}" -gt 0 ]; then
            echo "  Consistency: ${TOTAL} issues (0 HIGH)"
        fi
    fi
fi

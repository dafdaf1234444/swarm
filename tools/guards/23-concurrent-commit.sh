#!/bin/bash
# L-1528/L-1534: Concurrent-commit stampede guard.
# Detects N>2 git processes and warns. At N>4, blocks commit to prevent index corruption.
# L-1534: When concurrent, require GIT_INDEX_FILE to avoid shared .git/index corruption.
# WSL/NTFS cannot handle multiple concurrent git index writes — they cascade into corruption.
GIT_PROCS=$(ps aux 2>/dev/null | grep -E "git (commit|reset|add|read-tree|write-tree)" | grep -v grep | wc -l)
if [ "${GIT_PROCS:-0}" -gt 4 ]; then
    echo "FAIL: Concurrent-commit stampede detected (${GIT_PROCS} git processes)."
    echo "  L-1528: At N>4, index corruption is near-certain on WSL/NTFS."
    echo "  Wait for other sessions to finish, then retry."
    if [ "${ALLOW_STAMPEDE:-0}" != "1" ]; then
        exit 1
    fi
    echo "  ALLOW_STAMPEDE=1 set — bypassing guard."
elif [ "${GIT_PROCS:-0}" -gt 2 ]; then
    echo "  L-1528 NOTICE: ${GIT_PROCS} concurrent git processes — elevated corruption risk."
    # L-1534: Concurrent sessions must isolate index writes.
    if [ -z "${GIT_INDEX_FILE:-}" ]; then
        echo "FAIL: L-1534 concurrent sessions require GIT_INDEX_FILE=<tmpfile>."
        echo "  Retry with an isolated index or use python3 tools/safe_commit.py."
        if [ "${ALLOW_STAMPEDE:-0}" != "1" ]; then
            exit 1
        fi
        echo "  ALLOW_STAMPEDE=1 set — bypassing temp-index requirement."
    else
        echo "  L-1534 OK: isolated index detected (${GIT_INDEX_FILE})."
    fi
fi

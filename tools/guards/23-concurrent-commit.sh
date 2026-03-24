#!/bin/bash
# L-1528: Concurrent-commit stampede guard.
# Detects N>2 git processes and warns. At N>4, blocks commit to prevent index corruption.
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
fi

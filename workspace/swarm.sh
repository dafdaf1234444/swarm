#!/usr/bin/env bash
# swarm — CLI for managing the swarm knowledge base
# Usage: ./workspace/swarm.sh <command>

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

cmd_status() {
    echo "=== Swarm Status ==="
    echo ""

    # Session count
    local sessions
    sessions=$(grep -oP 'Sessions completed: \K\d+' "$REPO_ROOT/memory/INDEX.md" 2>/dev/null || echo "?")
    echo "Sessions completed: $sessions"

    # Lesson count
    local lessons
    lessons=$(find "$REPO_ROOT/memory/lessons" -name "L-*.md" 2>/dev/null | wc -l)
    echo "Lessons: $lessons"

    # Task count
    local done total
    done=$(grep -rl 'Status: DONE' "$REPO_ROOT/tasks/" 2>/dev/null | wc -l)
    total=$(find "$REPO_ROOT/tasks" -name "TASK-*.md" 2>/dev/null | wc -l)
    echo "Tasks: $done/$total done"

    # Belief count
    local beliefs
    beliefs=$(grep -c '^### B' "$REPO_ROOT/beliefs/DEPS.md" 2>/dev/null || echo "0")
    echo "Beliefs tracked: $beliefs"

    # Frontier
    local open resolved
    open=$(grep -c '^\- \*\*F' "$REPO_ROOT/tasks/FRONTIER.md" 2>/dev/null || echo "0")
    resolved=$(grep -c '^| F' "$REPO_ROOT/tasks/FRONTIER.md" 2>/dev/null || echo "0")
    echo "Frontier: $open open, $resolved resolved"
}

cmd_health() {
    echo "=== Health Check ==="
    echo ""

    # 1. Knowledge growth
    local lessons
    lessons=$(find "$REPO_ROOT/memory/lessons" -name "L-*.md" 2>/dev/null | wc -l)
    echo "1. Knowledge: $lessons lessons"

    # 2. Confidence ratio
    local verified assumed
    verified=$(grep -r 'Confidence: Verified' "$REPO_ROOT/memory/lessons/" 2>/dev/null | wc -l)
    assumed=$(grep -r 'Confidence: Assumed' "$REPO_ROOT/memory/lessons/" 2>/dev/null | wc -l)
    local total_conf=$((verified + assumed))
    if [ "$total_conf" -gt 0 ]; then
        local pct=$((verified * 100 / total_conf))
        echo "2. Accuracy: ${pct}% verified ($verified/$total_conf)"
    else
        echo "2. Accuracy: no data"
    fi

    # 3. Compactness
    local long_lessons
    long_lessons=$(find "$REPO_ROOT/memory/lessons" -name "L-*.md" -exec sh -c 'wc -l < "$1"' _ {} \; 2>/dev/null | awk '$1 > 20' | wc -l)
    local index_lines
    index_lines=$(wc -l < "$REPO_ROOT/memory/INDEX.md" 2>/dev/null)
    echo "3. Compactness: $long_lessons lessons over 20 lines, INDEX is $index_lines lines"

    # 4. Belief evolution
    local belief_commits
    belief_commits=$(git -C "$REPO_ROOT" log --oneline beliefs/DEPS.md 2>/dev/null | wc -l)
    echo "4. Belief evolution: $belief_commits commits to DEPS.md"

    # 5. Task throughput
    local done total
    done=$(grep -rl 'Status: DONE' "$REPO_ROOT/tasks/" 2>/dev/null | wc -l)
    total=$(find "$REPO_ROOT/tasks" -name "TASK-*.md" 2>/dev/null | wc -l)
    if [ "$total" -gt 0 ]; then
        local pct=$((done * 100 / total))
        echo "5. Throughput: ${pct}% tasks done ($done/$total)"
    else
        echo "5. Throughput: no tasks"
    fi
}

cmd_frontier() {
    echo "=== Open Frontier Questions ==="
    echo ""
    grep '^\- \*\*F' "$REPO_ROOT/tasks/FRONTIER.md" 2>/dev/null | while read -r line; do
        echo "  $line"
    done
}

cmd_lessons() {
    echo "=== Lessons ==="
    echo ""
    grep '^\- \*\*L-' "$REPO_ROOT/memory/INDEX.md" 2>/dev/null | while read -r line; do
        echo "  $line"
    done
}

cmd_next() {
    echo "=== Suggested Next Session ==="
    echo ""

    # Check for in-progress tasks
    local in_progress
    in_progress=$(grep -rl 'Status: IN PROGRESS' "$REPO_ROOT/tasks/" 2>/dev/null | head -1 || true)
    if [ -n "$in_progress" ]; then
        echo "CONTINUE: $(basename "$in_progress") is still in progress"
        head -1 "$in_progress" | sed 's/^# /  /'
        return
    fi

    # Show critical frontier questions first
    echo "Critical open questions:"
    grep '^\- \*\*F' "$REPO_ROOT/tasks/FRONTIER.md" 2>/dev/null | head -3 | while read -r line; do
        echo "  $line"
    done
    echo ""

    # Health check suggestion
    local sessions
    sessions=$(grep -oP 'Sessions completed: \K\d+' "$REPO_ROOT/memory/INDEX.md" 2>/dev/null || echo "0")
    if [ $((sessions % 5)) -eq 0 ] && [ "$sessions" -gt 0 ]; then
        echo "NOTE: Session $sessions — time for a health check (run: swarm.sh health)"
    fi
}

cmd_log() {
    echo "=== Recent Activity ==="
    echo ""
    git -C "$REPO_ROOT" log --oneline -10 2>/dev/null
}

cmd_help() {
    echo "swarm — CLI for the swarm knowledge base"
    echo ""
    echo "Commands:"
    echo "  status    Show system overview"
    echo "  health    Run health check"
    echo "  frontier  List open frontier questions"
    echo "  lessons   List all lessons"
    echo "  next      Suggest what to work on next"
    echo "  log       Show recent git activity"
    echo "  help      Show this help"
}

case "${1:-help}" in
    status)   cmd_status ;;
    health)   cmd_health ;;
    frontier) cmd_frontier ;;
    lessons)  cmd_lessons ;;
    next)     cmd_next ;;
    log)      cmd_log ;;
    help)     cmd_help ;;
    *)        echo "Unknown command: $1"; cmd_help; exit 1 ;;
esac

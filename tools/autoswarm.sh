#!/usr/bin/env bash
# autoswarm.sh — Autonomous cross-session swarm initiator (F-CC1)
# Implements the F134 automation path: external trigger → claude --print → headless swarm session
#
# Usage:
#   bash tools/autoswarm.sh              # manual invocation
#   bash tools/autoswarm.sh --dry-run    # print what would run, don't execute
#
# Cron example (run every 30 minutes):
#   */30 * * * * cd /path/to/swarm && bash tools/autoswarm.sh >> workspace/autoswarm-logs/cron.log 2>&1
#
# Filesystem watcher example (inotifywait on Linux):
#   inotifywait -m -e create workspace/autoswarm-trigger | while read; do
#     bash tools/autoswarm.sh
#   done
#
# The Stop hook writes workspace/autoswarm-trigger to signal session completion.
# This script is the consumer of that trigger file.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SWARM_CMD="$REPO_ROOT/.claude/commands/swarm.md"
LOG_DIR="$REPO_ROOT/workspace/autoswarm-logs"
TRIGGER_FILE="$REPO_ROOT/workspace/autoswarm-trigger"
LOCKFILE="$REPO_ROOT/workspace/autoswarm.lock"

DRY_RUN=false
if [[ "${1:-}" == "--dry-run" ]]; then
    DRY_RUN=true
fi

# Ensure log directory exists
mkdir -p "$LOG_DIR"

# Timestamped log file
TIMESTAMP="$(date +%Y-%m-%d-%H-%M)"
LOGFILE="$LOG_DIR/$TIMESTAMP.log"

log() {
    echo "[$(date '+%Y-%m-%dT%H:%M:%S')] $*" | tee -a "$LOGFILE"
}

# Prevent concurrent autoswarm runs
if [[ -f "$LOCKFILE" ]]; then
    LOCK_PID="$(cat "$LOCKFILE" 2>/dev/null || echo 0)"
    if kill -0 "$LOCK_PID" 2>/dev/null; then
        log "SKIP: autoswarm already running (pid=$LOCK_PID)"
        exit 0
    else
        log "WARN: stale lockfile found (pid=$LOCK_PID), removing"
        rm -f "$LOCKFILE"
    fi
fi

# Check that swarm command file exists
if [[ ! -f "$SWARM_CMD" ]]; then
    log "ERROR: swarm command not found at $SWARM_CMD"
    log "Fix: git checkout HEAD -- .claude/commands/swarm.md"
    exit 1
fi

# Check that claude CLI is available
if ! command -v claude &>/dev/null; then
    log "ERROR: claude CLI not found in PATH"
    log "Install: npm install -g @anthropic-ai/claude-code"
    exit 1
fi

# Remove trigger file if present (consume the trigger)
if [[ -f "$TRIGGER_FILE" ]]; then
    log "INFO: consumed trigger file $TRIGGER_FILE"
    rm -f "$TRIGGER_FILE"
fi

if [[ "$DRY_RUN" == true ]]; then
    log "DRY-RUN: would invoke: claude --print \"\$(cat $SWARM_CMD)\" --dangerously-skip-permissions --max-budget-usd 2"
    log "DRY-RUN: log would be written to $LOGFILE"
    exit 0
fi

# Write lockfile
echo "$$" > "$LOCKFILE"

log "START: autoswarm session initiated"
log "INFO: repo=$REPO_ROOT"
log "INFO: logfile=$LOGFILE"

# Invoke headless swarm session
EXIT_CODE=0
(
    cd "$REPO_ROOT"
    SWARM_PROMPT="$(cat "$SWARM_CMD")"
    claude --print "$SWARM_PROMPT" \
        --dangerously-skip-permissions \
        --max-budget-usd 2 \
        2>&1
) | tee -a "$LOGFILE" || EXIT_CODE=$?

rm -f "$LOCKFILE"

if [[ $EXIT_CODE -eq 0 ]]; then
    log "DONE: autoswarm session completed successfully"
else
    log "WARN: autoswarm session exited with code $EXIT_CODE"
fi

# Write new trigger file so next scheduled run can detect this session ended
touch "$TRIGGER_FILE"
log "INFO: wrote trigger file $TRIGGER_FILE for next cycle"

exit $EXIT_CODE

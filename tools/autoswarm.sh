#!/usr/bin/env bash
# autoswarm.sh — Autonomous cross-session swarm initiator (F-CC1)
# Implements the F134 automation path: external trigger → claude --print → headless swarm session
#
# Usage:
#   bash tools/autoswarm.sh                       # manual invocation
#   bash tools/autoswarm.sh --dry-run             # print what would run, don't execute
#   bash tools/autoswarm.sh --anxiety-cadence 3   # run anxiety trigger every 3 autoswarm runs
#   bash tools/autoswarm.sh --no-anxiety          # disable anxiety trigger
#   ANXIETY_ENABLED=false bash tools/autoswarm.sh # disable anxiety trigger via env
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
ANXIETY_TRIGGER="$REPO_ROOT/tools/anxiety_trigger.py"
ANXIETY_STATE_FILE="$REPO_ROOT/workspace/anxiety-dispatch.state"

DRY_RUN=false
ANXIETY_ENABLED="${ANXIETY_ENABLED:-true}"
ANXIETY_CADENCE="${ANXIETY_CADENCE:-1}"
while [[ $# -gt 0 ]]; do
    case "$1" in
        --dry-run)
            DRY_RUN=true
            ;;
        --anxiety-cadence)
            ANXIETY_CADENCE="${2:-1}"
            shift
            ;;
        --no-anxiety)
            ANXIETY_ENABLED=false
            ;;
        *)
            ;;
    esac
    shift
done

# Ensure log directory exists
mkdir -p "$LOG_DIR"

# Timestamped log file
TIMESTAMP="$(date +%Y-%m-%d-%H-%M)"
LOGFILE="$LOG_DIR/$TIMESTAMP.log"

log() {
    echo "[$(date '+%Y-%m-%dT%H:%M:%S')] $*" | tee -a "$LOGFILE"
}

# Validate cadence
if ! [[ "$ANXIETY_CADENCE" =~ ^[0-9]+$ ]] || [[ "$ANXIETY_CADENCE" -lt 1 ]]; then
    log "WARN: invalid ANXIETY_CADENCE '$ANXIETY_CADENCE' — defaulting to 1"
    ANXIETY_CADENCE=1
fi

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

# Anxiety-zone gate (F-ISG1)
ANXIETY_STATUS=""
ANXIETY_FRONTIER=""
ANXIETY_PROMPT=""
PROMPT_SOURCE="swarm_cmd"
PYTHON_BIN=""
ANXIETY_RUN=false
ANXIETY_NEXT_COUNT=0
ANXIETY_SKIP_REASON=""

if [[ "$ANXIETY_ENABLED" == "true" ]]; then
    COUNT=0
    if [[ -f "$ANXIETY_STATE_FILE" ]]; then
        COUNT="$(cat "$ANXIETY_STATE_FILE" 2>/dev/null || echo 0)"
    fi
    if ! [[ "$COUNT" =~ ^[0-9]+$ ]]; then
        COUNT=0
    fi
    ANXIETY_NEXT_COUNT=$((COUNT + 1))
    if (( ANXIETY_NEXT_COUNT % ANXIETY_CADENCE == 0 )); then
        ANXIETY_RUN=true
    else
        ANXIETY_SKIP_REASON="cadence"
    fi
    if [[ "$DRY_RUN" != true ]]; then
        echo "$ANXIETY_NEXT_COUNT" > "$ANXIETY_STATE_FILE"
    fi
else
    ANXIETY_SKIP_REASON="disabled"
fi

if [[ "$ANXIETY_ENABLED" == "true" && "$ANXIETY_SKIP_REASON" == "cadence" ]]; then
    log "SKIP: anxiety gate closed by cadence (count=$ANXIETY_NEXT_COUNT cadence=$ANXIETY_CADENCE)"
    exit 0
fi

if command -v python3 &>/dev/null; then
    PYTHON_BIN="python3"
elif command -v python &>/dev/null; then
    PYTHON_BIN="python"
fi

if [[ "$ANXIETY_ENABLED" == "true" ]]; then
    if [[ -z "$PYTHON_BIN" ]]; then
        log "ERROR: anxiety gate requires python (python3 or python not found)"
        exit 1
    fi
    if [[ ! -f "$ANXIETY_TRIGGER" ]]; then
        log "ERROR: anxiety gate missing $ANXIETY_TRIGGER"
        exit 1
    fi
    ANXIETY_JSON="$("$PYTHON_BIN" "$ANXIETY_TRIGGER" --json 2>/dev/null || true)"
    if [[ -z "$ANXIETY_JSON" ]]; then
        log "ERROR: anxiety gate produced empty JSON"
        exit 1
    fi
    ANXIETY_PARSED="$(ANXIETY_JSON="$ANXIETY_JSON" "$PYTHON_BIN" - <<'PY'
import json
import os
import shlex
import sys

raw = os.environ.get("ANXIETY_JSON", "").strip()
if not raw:
    sys.exit(0)
try:
    data = json.loads(raw)
except Exception:
    sys.exit(0)

status = data.get("status", "")
top = (data.get("top_frontier") or {})
frontier = top.get("id", "")
desc = top.get("desc", "")
age = top.get("age", "")
last = top.get("last_session", "")
prompt = ""
cmd = data.get("dispatch_command", "")
if cmd:
    try:
        parts = shlex.split(cmd)
        if "--print" in parts:
            idx = parts.index("--print") + 1
            if idx < len(parts):
                prompt = parts[idx]
    except Exception:
        pass

print(status)
print(frontier)
print(prompt)
print(desc)
print(age)
print(last)
PY
)"

    if [[ -n "$ANXIETY_PARSED" ]]; then
        IFS=$'\n' read -r ANXIETY_STATUS ANXIETY_FRONTIER ANXIETY_PROMPT ANXIETY_DESC ANXIETY_AGE ANXIETY_LAST <<<"$ANXIETY_PARSED"
    fi
else
    log "INFO: anxiety_gate disabled (set ANXIETY_ENABLED=true)"
fi

SELECTED_PROMPT="$(cat "$SWARM_CMD")"
if [[ "$ANXIETY_ENABLED" == "true" ]]; then
    if [[ -z "$ANXIETY_STATUS" ]]; then
        log "ERROR: anxiety gate produced empty status"
        exit 1
    fi
    if [[ "$ANXIETY_STATUS" == "no_anxiety_zones" ]]; then
        log "SKIP: anxiety gate found no anxiety zones"
        exit 0
    fi
    if [[ "$ANXIETY_STATUS" != "anxiety_zone_found" ]]; then
        log "ERROR: anxiety gate unexpected status=$ANXIETY_STATUS"
        exit 1
    fi
    if [[ -z "$ANXIETY_FRONTIER" ]]; then
        log "ERROR: anxiety gate missing frontier id"
        exit 1
    fi
    PROMPT_SOURCE="anxiety_gate"
    FOCUS_NOTE="AUTOSWARM GATE (F-ISG1): Focus on ${ANXIETY_FRONTIER}"
    if [[ -n "$ANXIETY_AGE" ]]; then
        FOCUS_NOTE="$FOCUS_NOTE (+${ANXIETY_AGE} sessions)"
    fi
    if [[ -n "$ANXIETY_LAST" ]]; then
        FOCUS_NOTE="$FOCUS_NOTE; last active S${ANXIETY_LAST}"
    fi
    FOCUS_NOTE="$FOCUS_NOTE."
    if [[ -n "$ANXIETY_DESC" ]]; then
        FOCUS_NOTE="$FOCUS_NOTE $ANXIETY_DESC"
    fi
    SELECTED_PROMPT="$SELECTED_PROMPT"$'\n\n'"$FOCUS_NOTE"
    log "INFO: anxiety_gate selected frontier=$ANXIETY_FRONTIER"
else
    log "INFO: anxiety_gate disabled; using swarm command"
fi

if [[ "$DRY_RUN" == true ]]; then
    log "DRY-RUN: prompt_source=$PROMPT_SOURCE"
    if [[ "$PROMPT_SOURCE" == "anxiety_gate" ]]; then
        log "DRY-RUN: frontier=$ANXIETY_FRONTIER"
    fi
    log "DRY-RUN: would invoke: claude --print \"$SELECTED_PROMPT\" --dangerously-skip-permissions --max-budget-usd 2"
    log "DRY-RUN: log would be written to $LOGFILE"
    exit 0
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

# Write lockfile
echo "$$" > "$LOCKFILE"

log "START: autoswarm session initiated"
log "INFO: repo=$REPO_ROOT"
log "INFO: logfile=$LOGFILE"
log "INFO: prompt_source=$PROMPT_SOURCE"
if [[ "$PROMPT_SOURCE" == "anxiety_gate" ]]; then
    log "INFO: frontier=$ANXIETY_FRONTIER"
fi

# Invoke headless swarm session
EXIT_CODE=0
(
    cd "$REPO_ROOT"
    SESSION_PROMPT="$SELECTED_PROMPT"
    claude --print "$SESSION_PROMPT" \
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

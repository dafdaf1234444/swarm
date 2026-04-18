#!/usr/bin/env bash
set -u

REMOTE="${REMOTE:-origin}"
BRANCH="${BRANCH:-$(git branch --show-current 2>/dev/null || echo main)}"
SLEEP_SECONDS="${SLEEP_SECONDS:-30}"
MIN_COMMIT_AGE_SECONDS="${MIN_COMMIT_AGE_SECONDS:-90}"
REQUIRE_NEXT_FILE="${REQUIRE_NEXT_FILE:-1}"
NEXT_FILE="${NEXT_FILE:-tasks/NEXT.md}"
SESSION_LOG="${SESSION_LOG:-memory/SESSION-LOG.md}"
KILL_FILE="${KILL_FILE:-tasks/KILL-SWITCH.md}"
LOCK_FILE="${LOCK_FILE:-.swarm_loop.lock}"
LOG_DIR="${LOG_DIR:-logs/swarm}"
WORKER_CMD="${WORKER_CMD:-swarm}"
AUTO_PUSH="${AUTO_PUSH:-1}"
AUTO_COMMIT="${AUTO_COMMIT:-1}"
AUTO_STASH_PREFIX="swarm-auto-stash"
mkdir -p "$LOG_DIR"

log() {
  printf '[%s] %s\n' "$(date '+%F %T')" "$*" | tee -a "$LOG_DIR/loop-v7.log"
}

run_cmd() {
  log "RUN: $*"
  bash -lc "$*" 2>&1 | tee -a "$LOG_DIR/loop-v7.log"
  return ${PIPESTATUS[0]}
}

have_changes() {
  ! git diff --quiet || ! git diff --cached --quiet || [[ -n "$(git ls-files --others --exclude-standard)" ]]
}

checkpoint_commit() {
  [[ "$AUTO_COMMIT" == "1" ]] || return 0
  git add -A
  if have_changes; then
    git commit -m "swarm: auto checkpoint $(date '+%F %T')" || true
  fi
}

recover_rebase_state() {
  if [[ -d .git/rebase-merge || -d .git/rebase-apply ]]; then
    log "rebase detected"
    git add -A || true
    git rebase --continue && return 0
    log "rebase continue failed -> aborting"
    git rebase --abort || true
  fi
  return 0
}

safe_pull_rebase() {
  git fetch "$REMOTE" || return 1

  if have_changes; then
    log "dirty tree detected -> checkpoint"
    checkpoint_commit
  fi

  git pull --rebase "$REMOTE" "$BRANCH" && return 0

  log "pull --rebase failed -> abort/stash/retry"
  git rebase --abort || true
  git stash push -u -m "$AUTO_STASH_PREFIX-$(date +%s)" || true
  git pull --rebase "$REMOTE" "$BRANCH" || return 1
  git stash pop || true
  return 0
}

maybe_push() {
  [[ "$AUTO_PUSH" == "1" ]] || return 0
  git push "$REMOTE" "$BRANCH" || true
}

kill_switch_triggered() {
  [[ "${SWARM_STOP:-0}" == "1" ]] && return 0
  if [[ -f "$KILL_FILE" ]]; then
    grep -qiE 'stop|halt|kill|abort' "$KILL_FILE" 2>/dev/null && return 0
  fi
  return 1
}

require_next_ready() {
  [[ "$REQUIRE_NEXT_FILE" == "1" ]] || return 0
  [[ -f "$NEXT_FILE" ]] || {
    log "missing $NEXT_FILE"
    return 1
  }

  grep -qiE 'next|ready|todo|dispatch|active|focus' "$NEXT_FILE" 2>/dev/null && return 0

  log "$NEXT_FILE exists but no obvious actionable markers found"
  return 1
}

recent_commit_too_fresh() {
  local now last age
  now="$(date +%s)"
  last="$(git log -1 --format=%ct 2>/dev/null || echo 0)"
  age=$(( now - last ))
  if (( age < MIN_COMMIT_AGE_SECONDS )); then
    log "novelty gate: last commit only ${age}s ago (< ${MIN_COMMIT_AGE_SECONDS}s)"
    return 0
  fi
  return 1
}

same_head_as_last_cycle() {
  local head_file head prev
  head_file="$LOG_DIR/last_head.txt"
  head="$(git rev-parse HEAD 2>/dev/null || echo nohead)"
  prev="$(cat "$head_file" 2>/dev/null || echo none)"
  echo "$head" > "$head_file"
  [[ "$head" == "$prev" ]]
}

recent_session_log_too_fresh() {
  [[ -f "$SESSION_LOG" ]] || return 1
  local now mtime age
  now="$(date +%s)"
  mtime="$(stat -c %Y "$SESSION_LOG" 2>/dev/null || echo 0)"
  age=$(( now - mtime ))
  if (( age < MIN_COMMIT_AGE_SECONDS )); then
    log "session log updated ${age}s ago (< ${MIN_COMMIT_AGE_SECONDS}s)"
    return 0
  fi
  return 1
}

novelty_gate() {
  recent_commit_too_fresh && return 1
  recent_session_log_too_fresh && return 1

  if same_head_as_last_cycle; then
    log "HEAD unchanged since last cycle"
  fi

  return 0
}

write_cycle_note() {
  mkdir -p "$(dirname "$SESSION_LOG")"
  {
    echo ""
    echo "## auto-loop $(date '+%F %T')"
    echo "- branch: $BRANCH"
    echo "- head: $(git rev-parse --short HEAD 2>/dev/null || echo unknown)"
    echo "- worker: $WORKER_CMD"
  } >> "$SESSION_LOG"
}

acquire_lock() {
  if [[ -f "$LOCK_FILE" ]]; then
    local old_pid
    old_pid="$(cat "$LOCK_FILE" 2>/dev/null || echo '')"
    if [[ -n "$old_pid" ]] && kill -0 "$old_pid" 2>/dev/null; then
      log "another loop already running with pid=$old_pid"
      exit 1
    fi
  fi
  echo "$$" > "$LOCK_FILE"
}

cleanup() {
  rm -f "$LOCK_FILE"
}
trap cleanup EXIT INT TERM

run_worker() {
  log "worker cycle start"
  run_cmd "$WORKER_CMD"
  local rc=$?
  log "worker cycle end rc=$rc"
  return 0
}

main_cycle() {
  log "=== cycle start branch=$BRANCH remote=$REMOTE ==="

  if kill_switch_triggered; then
    log "kill switch triggered -> exit"
    exit 0
  fi

  recover_rebase_state
  safe_pull_rebase || log "pre-worker sync failed"

  if kill_switch_triggered; then
    log "kill switch triggered after sync -> exit"
    exit 0
  fi

  require_next_ready || {
    log "no actionable NEXT state -> skip cycle"
    return 0
  }

  novelty_gate || {
    log "novelty gate blocked cycle"
    return 0
  }

  write_cycle_note
  run_worker

  if kill_switch_triggered; then
    log "kill switch triggered after worker -> exit"
    exit 0
  fi

  checkpoint_commit
  safe_pull_rebase || log "post-worker sync failed"
  maybe_push

  log "=== cycle end ==="
}

acquire_lock

while true; do
  main_cycle
  log "sleep ${SLEEP_SECONDS}s"
  sleep "$SLEEP_SECONDS"
done

#!/usr/bin/env bash
set -u

SLEEP_SECS="${SLEEP_SECS:-20}"
LOG_FILE="${LOG_FILE:-swarm-loop.log}"

log() {
  printf "[%s] %s\n" "$(date "+%Y-%m-%d %H:%M:%S")" "$*" | tee -a "$LOG_FILE"
}

run_quiet() {
  "$@" >>"$LOG_FILE" 2>&1
  return $?
}

run_shell_quiet() {
  bash -lc "$1" >>"$LOG_FILE" 2>&1
  return $?
}

git_has_changes() {
  ! git diff --quiet --ignore-submodules -- 2>/dev/null || \
  ! git diff --cached --quiet --ignore-submodules -- 2>/dev/null
}

ensure_repo() {
  git rev-parse --show-toplevel >/dev/null 2>&1 || {
    echo "Not inside a git repo"
    exit 1
  }
  cd "$(git rev-parse --show-toplevel)" || exit 1
}

stop_requested() {
  [ "${SWARM_STOP:-0}" = "1" ] && return 0
  [ -f .swarm-stop ] && return 0
  return 1
}

safe_pull() {
  git remote get-url origin >/dev/null 2>&1 || return 0
  run_quiet git fetch origin || return 0
  run_quiet git pull --rebase --autostash || {
    log "pull/rebase failed, continuing"
    return 0
  }
}

run_if_exists() {
  local label="$1"
  local cmd="$2"
  if [ -f "$3" ]; then
    log "run: $label"
    run_shell_quiet "$cmd" || log "failed: $label"
    return 0
  fi
  return 1
}

heartbeat_fallback() {
  mkdir -p memory tasks 2>/dev/null || true

  {
    echo
    echo "## Swarm loop heartbeat $(date "+%Y-%m-%d %H:%M:%S")"
    echo "- branch: $(git branch --show-current 2>/dev/null || echo unknown)"
    echo "- head: $(git rev-parse --short HEAD 2>/dev/null || echo none)"
    echo "- status:"
    git status --short 2>/dev/null | sed "s/^/  - /"
  } >> tasks/NEXT.md 2>/dev/null || true

  {
    echo
    echo "### $(date "+%Y-%m-%d %H:%M:%S")"
    echo "- autonomous heartbeat"
    echo "- branch: $(git branch --show-current 2>/dev/null || echo unknown)"
    echo "- head: $(git rev-parse --short HEAD 2>/dev/null || echo none)"
  } >> memory/SESSION-LOG.md 2>/dev/null || true
}

commit_and_push() {
  git add -A >>"$LOG_FILE" 2>&1 || true

  if git diff --cached --quiet --ignore-submodules -- 2>/dev/null; then
    log "no staged changes"
    return 0
  fi

  local msg="swarm: loop $(date "+%Y-%m-%d %H:%M:%S")"
  if run_quiet git commit -m "$msg"; then
    log "committed"
    git remote get-url origin >/dev/null 2>&1 && {
      run_quiet git push || log "push failed"
    }
  else
    log "commit failed"
  fi
}

main() {
  ensure_repo
  touch "$LOG_FILE"
  log "swarm loop started"

  while true; do
    if stop_requested; then
      log "stop requested"
      exit 0
    fi

    log "tick"

    safe_pull

    run_if_exists "orient" "python3 tools/orient.py" "tools/orient.py" || true
    run_if_exists "check" "bash tools/check.sh --quick" "tools/check.sh" || true
    run_if_exists "sync_state" "python3 tools/sync_state.py" "tools/sync_state.py" || true
    run_if_exists "validate_beliefs" "python3 tools/validate_beliefs.py" "tools/validate_beliefs.py" || true

    DID_WORK=0

    run_if_exists "swarm runner" "python3 tools/swarm.py" "tools/swarm.py" && DID_WORK=1
    run_if_exists "dispatch" "python3 tools/dispatch.py" "tools/dispatch.py" && DID_WORK=1
    run_if_exists "domain priority" "python3 tools/f_ops2_domain_priority.py" "tools/f_ops2_domain_priority.py" && DID_WORK=1
    run_if_exists "periodics" "python3 tools/run_periodics.py" "tools/run_periodics.py" && DID_WORK=1
    run_if_exists "periodics alt" "python3 tools/periodics.py" "tools/periodics.py" && DID_WORK=1

    run_if_exists "post-sync_state" "python3 tools/sync_state.py" "tools/sync_state.py" || true
    run_if_exists "post-validate_beliefs" "python3 tools/validate_beliefs.py" "tools/validate_beliefs.py" || true

    if [ "$DID_WORK" -eq 0 ]; then
      log "no inner runner found; writing heartbeat"
      heartbeat_fallback
    fi

    if git_has_changes; then
      commit_and_push
    else
      log "no repo changes"
    fi

    sleep "$SLEEP_SECS"
  done
}

main

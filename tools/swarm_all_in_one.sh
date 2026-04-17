#!/usr/bin/env bash
set -euo pipefail

ROOT="$(pwd)"
LOCK_FILE="$ROOT/runtime/swarm.lock"
SEEN_FILE="$ROOT/runtime/swarm.seen"
LOG_FILE="$ROOT/runtime/swarm.log"
STATUS_FILE="$ROOT/runtime/status.txt"
SUMMARY_FILE="$ROOT/runtime/summary.txt"
CLAIM_DIR="$ROOT/runtime/claims"

MAX_BATCH="${MAX_BATCH:-3}"
SLEEP_SECS="${SLEEP_SECS:-4}"
SCREENSHOT_EVERY="${SCREENSHOT_EVERY:-0}"

mkdir -p "$ROOT/runtime" "$CLAIM_DIR" "$ROOT/tasks" "$ROOT/tools" "$ROOT/memory"
touch "$SEEN_FILE" "$LOG_FILE" "$STATUS_FILE" "$SUMMARY_FILE" "$ROOT/tasks/NEXT.md"

exec 9>"$LOCK_FILE"
flock -n 9 || { echo "already running"; exit 1; }

log() {
  printf '[%s] %s\n' "$(date '+%F %T')" "$*" | tee -a "$LOG_FILE"
}

DEFAULT_BRANCH="$(git remote show origin 2>/dev/null | sed -n '/HEAD branch/s/.*: //p')"
[ -z "${DEFAULT_BRANCH:-}" ] && DEFAULT_BRANCH="$(git branch --show-current 2>/dev/null || echo master)"

LAST_BATCH="none"
LAST_ID="none"
LAST_ACTION="none"
LAST_RESULT="idle"

write_status() {
  cat > "$STATUS_FILE" <<STATUS
time: $(date '+%F %T')
root: $ROOT
branch: $DEFAULT_BRANCH
max_batch: $MAX_BATCH
last_batch: $LAST_BATCH
last_id: $LAST_ID
last_action: $LAST_ACTION
last_result: $LAST_RESULT
seen_count: $(wc -l < "$SEEN_FILE" 2>/dev/null || echo 0)
log_file: $LOG_FILE
summary_file: $SUMMARY_FILE
STATUS
}

write_summary() {
  {
    echo "=== SWARM SUMMARY ==="
    echo "time: $(date '+%F %T')"
    echo "branch: $DEFAULT_BRANCH"
    echo "last_batch: $LAST_BATCH"
    echo "last_id: $LAST_ID"
    echo "last_action: $LAST_ACTION"
    echo "last_result: $LAST_RESULT"
    echo
    echo "=== RECENT LOG ==="
    tail -n 40 "$LOG_FILE" 2>/dev/null || true
  } > "$SUMMARY_FILE"
}

maybe_screenshot() {
  if [ "$SCREENSHOT_EVERY" -gt 0 ] && command -v termux-screenshot >/dev/null 2>&1; then
    mkdir -p "$ROOT/runtime/screens"
    termux-screenshot -p "$ROOT/runtime/screens/shot_$(date +%F_%H-%M-%S).png" >/dev/null 2>&1 || true
  fi
}

sync_down() {
  log "SYNC DOWN"
  git fetch origin "$DEFAULT_BRANCH" || true
  git reset --hard "origin/$DEFAULT_BRANCH" || true
}

sync_up() {
  log "SYNC UP"
  git add . || true
  git commit -m "swarm: batch $(date +%H:%M:%S)" || true
  git push origin HEAD:"$DEFAULT_BRANCH" || true
}

claim() {
  local id="$1"
  local file="$CLAIM_DIR/$id.claim"
  ( set -o noclobber; echo "$$" > "$file" ) 2>/dev/null
}

release() {
  rm -f "$CLAIM_DIR/$1.claim" 2>/dev/null || true
}

pick_batch() {
python3 - "$ROOT" "$SEEN_FILE" "$MAX_BATCH" << 'PY'
import re, sys, pathlib, subprocess

root = pathlib.Path(sys.argv[1])
seen_path = pathlib.Path(sys.argv[2])
max_batch = int(sys.argv[3])

def read(p):
    try:
        return p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return ""

seen = set()
if seen_path.exists():
    seen = {x.strip() for x in read(seen_path).splitlines() if x.strip()}

text_next = read(root / "tasks" / "NEXT.md")
text_lanes = read(root / "tasks" / "SWARM-LANES.md")
text_log = read(root / "memory" / "SESSION-LOG.md")

scores = {}

def add(id_, score):
    if re.fullmatch(r"L-\d+", id_):
        scores[id_] = scores.get(id_, 0) + score

for m in re.finditer(r"L-\d+", text_next):
    add(m.group(0), 80)

for line in text_lanes.splitlines():
    ids = re.findall(r"L-\d+", line)
    if not ids:
        continue
    U = line.upper()
    L = line.lower()
    base = 0
    if "ACTIVE" in U: base += 120
    if "READY" in U: base += 100
    if "BLOCKED" in U: base -= 80
    if "ABANDONED" in U or "MERGED" in U: base -= 120
    if "next_step=" in L: base += 10
    if "focus=" in L: base += 8
    if "available=" in L: base += 5
    if "human_open_item=" in L: base -= 25
    for i in ids:
        add(i, base)

for line in text_log.lower().splitlines()[-300:]:
    for i in re.findall(r"l-\d+", line):
        i = i.upper()
        if "duplicate" in line or "near-duplicate" in line:
            add(i, -20)
        if "stale" in line or "obsolete" in line:
            add(i, -15)
        if "working" in line or "resolved" in line or "done" in line:
            add(i, 5)

try:
    out = subprocess.check_output(
        ["python3", str(root / "tools" / "orient.py")],
        stderr=subprocess.DEVNULL,
        text=True,
    )
    for n, i in enumerate(re.findall(r"L-\d+", out)):
        add(i, max(30 - n, 1))
except Exception:
    pass

items = [(score, i) for i, score in scores.items() if i not in seen and score >= 0]
items.sort(key=lambda x: (-x[0], x[1]))

for _, i in items[:max_batch]:
    print(i)
PY
}

decide_action() {
python3 - "$ROOT" "$1" << 'PY'
import sys, pathlib
root = pathlib.Path(sys.argv[1])
id_ = sys.argv[2]

txt = ""
for p in [root/"tasks"/"NEXT.md", root/"tasks"/"SWARM-LANES.md", root/"memory"/"SESSION-LOG.md"]:
    try:
        txt += "\n" + p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        pass

scope = "\n".join([line.lower() for line in txt.splitlines() if id_.lower() in line.lower()]) or txt.lower()

if any(w in scope for w in ["blocked", "human_open_item", "unclear", "investigate", "question"]):
    print("s")
elif any(w in scope for w in ["duplicate", "near-duplicate", "stale", "obsolete", "abandoned"]):
    print("d")
else:
    print("k")
PY
}

process_one() {
  local id="$1"
  local action
  action="$(decide_action "$id")"

  LAST_ID="$id"
  LAST_ACTION="$action"
  LAST_RESULT="started"
  write_status
  write_summary

  log "WORK $id action=$action"

  if [ -x "$ROOT/tools/resolve_one.sh" ]; then
    AUTO_ACTION="$action" bash "$ROOT/tools/resolve_one.sh" "$id" || true
  else
    case "$action" in
      d) git commit --allow-empty -m "resolve $id" >/dev/null 2>&1 || true ;;
      k) git commit --allow-empty -m "acknowledge $id" >/dev/null 2>&1 || true ;;
      *) : ;;
    esac
  fi

  echo "$id" >> "$SEEN_FILE"
  LAST_RESULT="done"
  write_status
  write_summary
}

trap 'log "STOP"; write_status; write_summary' EXIT INT TERM

log "START branch=$DEFAULT_BRANCH batch=$MAX_BATCH"
write_status
write_summary

while true; do
  sync_down

  mapfile -t BATCH < <(pick_batch)

  if [ "${#BATCH[@]}" -eq 0 ]; then
    LAST_BATCH="none"
    LAST_ID="none"
    LAST_ACTION="none"
    LAST_RESULT="waiting"
    write_status
    write_summary
    log "NO REAL TASKS -> waiting"
    maybe_screenshot
    sleep "$SLEEP_SECS"
    continue
  fi

  LAST_BATCH="${BATCH[*]}"
  write_status
  write_summary
  log "BATCH ${BATCH[*]}"

  pids=()
  active=()

  for id in "${BATCH[@]}"; do
    if claim "$id"; then
      active+=("$id")
      (
        process_one "$id"
      ) &
      pids+=("$!")
    else
      log "SKIP CLAIMED $id"
    fi
  done

  for p in "${pids[@]}"; do
    wait "$p" || true
  done

  for id in "${active[@]}"; do
    release "$id"
  done

  sync_up
  maybe_screenshot
  log "CYCLE DONE"
  write_status
  write_summary
  sleep "$SLEEP_SECS"
done

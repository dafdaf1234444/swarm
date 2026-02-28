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

# 0. Mass-deletion guard (FM-01, L-346, L-350): abort if staged FILE deletions exceed threshold.
# Protects against WSL filesystem corruption staging mass file deletions via git add -A accidents.
# Counts DELETED FILES (D status), not line-level deletions — avoids false positives on large edits.
FILE_DELETION_THRESHOLD=20
STAGED_FILE_DELETIONS=$(git diff --cached --diff-filter=D --name-only 2>/dev/null | wc -l | tr -d ' ')
if [ "${STAGED_FILE_DELETIONS:-0}" -gt "$FILE_DELETION_THRESHOLD" ]; then
    echo "FAIL: Mass-deletion guard triggered — ${STAGED_FILE_DELETIONS} staged file deletions (threshold: ${FILE_DELETION_THRESHOLD})."
    echo "  This likely means WSL filesystem corruption caused 'git add' to stage file deletions."
    echo "  Run: git diff --cached --diff-filter=D --name-only | head -20 — to inspect."
    echo "  If intentional (compaction archive), set env ALLOW_MASS_DELETION=1 to bypass."
    if [ "${ALLOW_MASS_DELETION:-0}" != "1" ]; then
        exit 1
    fi
    echo "  ALLOW_MASS_DELETION=1 set — bypassing mass-deletion guard."
fi
echo "  Mass-deletion guard: PASS (${STAGED_FILE_DELETIONS:-0} staged file deletions)"

# FM-03: Ghost-lesson resurrection guard (L-346).
# After 'git mv memory/lessons/L-NNN.md memory/lessons/archive/L-NNN.md', WSL may leave
# ghost copies in the source directory. If staged as new-file, they undo the archiving.
ARCHIVE_DIR="memory/lessons/archive"
if [ -d "$ARCHIVE_DIR" ]; then
    GHOST_FILES=""
    while IFS= read -r filepath; do
        lesson_name="$(basename "$filepath")"
        if [ -f "$ARCHIVE_DIR/$lesson_name" ]; then
            GHOST_FILES="$GHOST_FILES $filepath"
        fi
    done < <(git status --porcelain 2>/dev/null | { grep '^A ' || true; } | { grep 'memory/lessons/L-' || true; } | { grep -v '/archive/' || true; } | awk '{print $2}')
    if [ -n "$GHOST_FILES" ]; then
        echo "FAIL: Ghost-lesson resurrection detected —${GHOST_FILES}"
        echo "  These staged new-files already exist in archive/; staging would undo compaction."
        echo "  Fix: git restore --staged${GHOST_FILES}"
        if [ "${ALLOW_GHOST_LESSONS:-0}" != "1" ]; then
            exit 1
        fi
        echo "  ALLOW_GHOST_LESSONS=1 set — bypassing ghost-lesson guard."
    fi
    echo "  Ghost-lesson guard: PASS"
fi

# Near-duplicate lesson guard (G-CC2-4, F-QC1, L-356): bonding curve analog.
# Staged new lesson files are scanned against recent lesson titles for word-overlap >50%.
# Emits DUE warning (not hard FAIL) to enforce increasing cost for duplicate knowledge.
STAGED_NEW_LESSONS=$(git diff --cached --diff-filter=A --name-only 2>/dev/null | { grep 'memory/lessons/L-[0-9]' || true; } | { grep -v '/archive/' || true; })
if [ -n "$STAGED_NEW_LESSONS" ]; then
    "${PYTHON_CMD[@]}" - "$STAGED_NEW_LESSONS" << 'PYEOF'
import sys, os, re

new_lessons = sys.argv[1].split() if len(sys.argv) > 1 else []
lesson_dir = "memory/lessons"

# L-NNN citation check (L-457, F9-NK): new lessons should cite at least one other lesson
# to sustain K_avg > 1.5 threshold (F75). Emits NOTICE (not hard FAIL).
no_citation_lessons = []
for new_path in new_lessons:
    try:
        with open(new_path) as f:
            content = f.read()
        lid = os.path.basename(new_path).replace('.md', '')
        # find all L-NNN citations excluding self
        cites = [c for c in re.findall(r'L-(\d{3})', content) if 'L-' + c != lid]
        if not cites:
            no_citation_lessons.append(os.path.basename(new_path))
    except Exception:
        pass
if no_citation_lessons:
    for f in no_citation_lessons:
        print(f"  NOTICE: {f} has no L-NNN citations — add Related: L-NNN to sustain K_avg>1.5 (L-457)")
else:
    print("  L-NNN citation guard: PASS")

def get_title(path):
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("#"):
                    return re.sub(r"^#+\s*", "", line).lower()
    except Exception:
        pass
    return ""

def word_overlap(a, b):
    wa = set(re.findall(r'\w+', a)) - {"the","a","an","is","are","was","were","to","of","in","for","and","or","L","S"}
    wb = set(re.findall(r'\w+', b)) - {"the","a","an","is","are","was","were","to","of","in","for","and","or","L","S"}
    if not wa or not wb:
        return 0.0
    return len(wa & wb) / min(len(wa), len(wb))

# Get last 20 lesson titles (excluding staged files themselves)
existing = sorted([
    f for f in os.listdir(lesson_dir)
    if f.startswith("L-") and f.endswith(".md") and not f.startswith("L-0")
], reverse=True)[:40]

warned = False
for new_path in new_lessons:
    new_title = get_title(new_path)
    if not new_title:
        continue
    for existing_file in existing:
        existing_path = os.path.join(lesson_dir, existing_file)
        if os.path.abspath(existing_path) == os.path.abspath(new_path):
            continue
        existing_title = get_title(existing_path)
        ov = word_overlap(new_title, existing_title)
        if ov >= 0.5:
            print(f"  NEAR-DUP WARNING: {os.path.basename(new_path)} overlaps {existing_file} ({ov:.0%})")
            print(f"    New:      {new_title}")
            print(f"    Existing: {existing_title}")
            print("    Consider updating the existing lesson instead (F-QC1, G-CC2-4).")
            warned = True
            break

if warned:
    print("  Near-dup guard: WARN (see above) — DUE: update existing lessons before adding new ones")
else:
    print("  Near-dup guard: PASS")
PYEOF
fi

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

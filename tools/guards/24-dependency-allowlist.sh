#!/bin/bash
# Dependency allowlist guard (L-601 structural enforcement)
# Ensures new external (non-stdlib) imports are intentional, not accidental.
# Allowlist: numpy, scipy (F-SP8 numerical tools only)

ALLOWLIST="numpy|scipy"

# Only check staged .py files in tools/
STAGED_PY=$(git diff --cached --name-only 2>/dev/null | { grep '^tools/.*\.py$' || true; })
if [ -z "$STAGED_PY" ]; then
    echo "  Dependency allowlist: SKIP (no staged tools)"
    exit 0
fi

VIOLATIONS=0
while IFS= read -r pyfile; do
    [ -f "$pyfile" ] || continue
    # Extract top-level import lines, skip comments and strings
    # Look for: import X / from X import Y where X is not stdlib and not local
    EXTERN=$(grep -nE '^\s*(import|from)\s+' "$pyfile" 2>/dev/null \
        | grep -vE '^\s*#' \
        | grep -vE '(import|from)\s+(os|sys|re|json|math|pathlib|argparse|collections|datetime|glob|io|hashlib|textwrap|unittest|contextlib|copy|functools|itertools|operator|shutil|subprocess|tempfile|time|typing|urllib|uuid|xml|zlib|base64|bisect|concurrent|csv|decimal|difflib|enum|heapq|importlib|inspect|logging|multiprocessing|random|socket|statistics|string|struct|threading|traceback|warnings|zipfile|abc|ast|codecs|configparser|dataclasses|fnmatch|fractions|getpass|http|mimetypes|numbers|pdb|pickle|platform|pprint|signal|sqlite3|ssl|stat|token|tokenize|__future__|swarm_|lesson_header|compact_core)' \
        | grep -vE '(import|from)\s+\.' \
        | grep -vE "($ALLOWLIST)" \
        || true)
    if [ -n "$EXTERN" ]; then
        echo "  FAIL: ${pyfile} has non-allowlisted imports:"
        echo "$EXTERN" | sed 's/^/    /'
        VIOLATIONS=$((VIOLATIONS + 1))
    fi
done <<< "$STAGED_PY"

if [ "$VIOLATIONS" -gt 0 ]; then
    echo "  Dependency allowlist: FAIL — ${VIOLATIONS} file(s) with unapproved external imports"
    echo "  To add a new dep: update ALLOWLIST in tools/guards/24-dependency-allowlist.sh + requirements.txt"
    exit 1
else
    echo "  Dependency allowlist: PASS"
fi

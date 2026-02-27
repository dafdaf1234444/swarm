#!/usr/bin/env python3

import hashlib
import re
import sys
from pathlib import Path

try:
    from validate_beliefs_extras import print_entropy, print_swarmability
except Exception:
    def print_entropy(*_args, **_kwargs):
        return

    def print_swarmability(*_args, **_kwargs):
        return

REPO_ROOT = Path(__file__).resolve().parent.parent


def _read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except Exception:
        return ""


def parse_beliefs(path: str) -> list[dict]:
    text = _read_text(Path(path))
    beliefs = []
    pat = re.compile(r"^###\s+(?P<id>B\d+):\s*(?P<statement>.+?)$", re.MULTILINE)
    matches = list(pat.finditer(text))
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        block = text[start:end]
        evidence = re.search(r"\*\*Evidence\*\*:\s*(\S+)", block, re.IGNORECASE)
        falsified = re.search(r"\*\*Falsified if\*\*:\s*(.+?)$", block, re.MULTILINE | re.IGNORECASE)
        depends = re.search(r"\*\*Depends on\*\*:\s*(.+?)$", block, re.MULTILINE | re.IGNORECASE)
        tested = re.search(r"\*\*Last tested\*\*:\s*(.+?)$", block, re.MULTILINE | re.IGNORECASE)
        depended = re.search(r"\*\*Depended on by\*\*:\s*(.+?)$", block, re.MULTILINE | re.IGNORECASE)
        dep_ids = []
        if depends:
            s = depends.group(1).strip().lower()
            if s not in ("none", "n/a", "-", ""):
                dep_ids = re.findall(r"B\d+", depends.group(1))
        rev_ids = []
        if depended:
            s = depended.group(1).strip().lower()
            if s not in ("none", "n/a", "-", ""):
                rev_ids = re.findall(r"B\d+", depended.group(1))
        beliefs.append({
            "id": m.group("id"),
            "statement": m.group("statement").strip(),
            "evidence": evidence.group(1).strip().lower() if evidence else "",
            "falsification": falsified.group(1).strip() if falsified else "",
            "depends_on": dep_ids,
            "depended_on_by": rev_ids,
            "last_tested": tested.group(1).strip() if tested else "",
        })
    return beliefs


def check_format(beliefs: list[dict]) -> list[str]:
    out = []
    for b in beliefs:
        bid = b["id"]
        if b["evidence"] not in ("observed", "theorized"):
            out.append(
                f"FAIL FORMAT: {bid} missing or invalid evidence type "
                f"(got '{b['evidence']}', need 'observed' or 'theorized')"
            )
        if not b["falsification"] or b["falsification"].lower() in ("", "none", "n/a"):
            out.append(f"WARN FORMAT: {bid} missing falsification condition")
        if not b["last_tested"]:
            out.append(f"FAIL FORMAT: {bid} missing 'Last tested' field")
    return out


def check_existence(beliefs: list[dict]) -> list[str]:
    known = {b["id"] for b in beliefs}
    out = []
    for b in beliefs:
        for dep in b["depends_on"]:
            if dep not in known:
                out.append(f"FAIL EXISTENCE: {b['id']} depends on {dep}, which is not defined")
    return out


def check_cycles(beliefs: list[dict]) -> list[str]:
    adj = {b["id"]: b["depends_on"] for b in beliefs}
    WHITE, GRAY, BLACK = 0, 1, 2
    color = {bid: WHITE for bid in adj}
    out = []

    def dfs(node: str, path: list[str]) -> None:
        color[node] = GRAY
        for dep in adj.get(node, []):
            if dep not in color:
                continue
            if color[dep] == GRAY:
                start = path.index(dep)
                out.append(f"FAIL CYCLE: circular dependency: {' -> '.join(path[start:] + [dep])}")
            elif color[dep] == WHITE:
                dfs(dep, path + [dep])
        color[node] = BLACK

    for bid in adj:
        if color[bid] == WHITE:
            dfs(bid, [bid])
    return out


def check_dep_consistency(beliefs: list[dict]) -> list[str]:
    out = []
    known = {b["id"] for b in beliefs}
    forward = {b["id"]: set(b["depends_on"]) for b in beliefs}
    reverse = {b["id"]: set(b.get("depended_on_by", [])) for b in beliefs}
    for bid, deps in forward.items():
        for dep in deps:
            if dep in known and bid not in reverse.get(dep, set()):
                out.append(f"WARN DEP_SYNC: {dep} should list {bid} in 'Depended on by'")
    for bid, rev_deps in reverse.items():
        for rdep in rev_deps:
            if rdep in known and bid not in forward.get(rdep, set()):
                out.append(f"WARN DEP_SYNC: {rdep} should list {bid} in 'Depends on'")
    return out


def check_orphans(beliefs: list[dict]) -> list[str]:
    depended_on = set()
    for b in beliefs:
        depended_on.update(b["depends_on"])
    out = []
    for b in beliefs:
        if b["id"] not in depended_on and not b["falsification"]:
            out.append(f"WARN ORPHAN: {b['id']} has no dependents and no falsification condition")
    return out


def cascade_check(beliefs: list[dict], changed_id: str) -> list[str]:
    by_id = {b["id"]: b for b in beliefs}
    if changed_id not in by_id:
        return [f"FAIL CASCADE: unknown belief ID '{changed_id}'"]
    forward: dict[str, list[str]] = {}
    for b in beliefs:
        for dep in b.get("depends_on", []):
            forward.setdefault(dep, []).append(b["id"])
    visited, queue, downstream = set(), [changed_id], []
    while queue:
        for child in forward.get(queue.pop(0), []):
            if child not in visited:
                visited.add(child)
                downstream.append(child)
                queue.append(child)
    if not downstream:
        return [f"INFO CASCADE: {changed_id} has no downstream beliefs"]
    changed_date = by_id[changed_id].get("last_tested", "")[:10]
    out = []
    for did in downstream:
        dep_date = by_id[did].get("last_tested", "")[:10]
        preview = by_id[did]["statement"][:55].rstrip()
        if not dep_date or (changed_date and dep_date < changed_date):
            out.append(f"WARN STALE: {did} ('{preview}') — last {dep_date or 'never'} vs {changed_id} {changed_date}")
        else:
            out.append(f"INFO CASCADE: {did} last {dep_date} >= {changed_id} {changed_date}")
    return out


def check_identity() -> list[str]:
    index_md = REPO_ROOT / "memory" / "INDEX.md"
    core_md = REPO_ROOT / "beliefs" / "CORE.md"
    if not index_md.exists() or not core_md.exists():
        return []
    m = re.search(r"<!--\s*core_md_hash:\s*([a-f0-9]{64})\s*-->", _read_text(index_md))
    if not m:
        return []
    stored = m.group(1)
    current = hashlib.sha256(core_md.read_bytes()).hexdigest()
    if stored != current:
        return [f"FAIL IDENTITY: CORE.md changed without renewal (stored={stored[:12]}..., current={current[:12]}...)"]
    return []


def main() -> int:
    quick = "--quick" in sys.argv
    raw = [a for a in sys.argv[1:] if a != "--quick"]
    changed_id, args = None, []
    i = 0
    while i < len(raw):
        if raw[i].startswith("--changed="):
            changed_id = raw[i].split("=", 1)[1]
        elif raw[i] == "--changed" and i + 1 < len(raw):
            changed_id = raw[i + 1]
            i += 1
        else:
            args.append(raw[i])
        i += 1

    path = args[0] if args else "beliefs/DEPS.md"
    if not Path(path).exists():
        print(f"ERROR: {path} not found")
        return 1
    beliefs = parse_beliefs(path)
    if not beliefs:
        print(f"ERROR: No beliefs found in {path}")
        return 1

    issues: list[str] = []
    existence = check_existence(beliefs)
    issues.extend(existence)
    issues.extend(check_cycles(beliefs))
    issues.extend(check_orphans(beliefs))
    issues.extend(check_dep_consistency(beliefs))
    issues.extend(check_format(beliefs))
    issues.extend(check_identity())

    n_obs = sum(1 for b in beliefs if b["evidence"] == "observed")
    n_the = sum(1 for b in beliefs if b["evidence"] == "theorized")
    for issue in issues:
        print(issue)
    fails = [i for i in issues if i.startswith("FAIL")]
    warns = [i for i in issues if i.startswith("WARN")]
    print()
    print(f"Summary: {len(beliefs)} beliefs, {n_obs} observed, {n_the} theorized, {len(fails)} errors, {len(warns)} warnings")
    exit_code = 1 if fails else 0
    print("RESULT: FAIL" if fails else "RESULT: PASS")

    if not quick:
        print_swarmability(beliefs, bool(fails), not existence)
        print_entropy(beliefs)
    if changed_id:
        print(f"\n=== CASCADE CHECK ({changed_id} changed) ===")
        for issue in cascade_check(beliefs, changed_id):
            print(issue)
    return exit_code


if __name__ == "__main__":
    sys.exit(main())

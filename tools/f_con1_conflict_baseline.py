#!/usr/bin/env python3
"""
F-CON1 baseline: measure C1 (duplicate work) and C3 (lane orphaning) rates
from last N sessions in git log + SWARM-LANES.md.
"""
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent

# --- C1: duplicate work detection from git log ---
C1_KEYWORDS = [
    "already done", "already committed", "already built", "already resolved",
    "verify", "relay", "convergence", "pre-empted", "proof-of-novelty",
    "anti-repeat", "duplicate", "concurrent session", "already fixed",
]

def parse_git_log(n: int = 40) -> list[dict]:
    """Get last n commits with message."""
    result = subprocess.run(
        ["git", "log", f"-{n}", "--format=%H|%s|%b", "--"],
        capture_output=True, text=True, cwd=ROOT
    )
    commits = []
    for block in result.stdout.strip().split("\n"):
        if "|" not in block:
            continue
        parts = block.split("|", 2)
        h, subject = parts[0], parts[1]
        body = parts[2] if len(parts) > 2 else ""
        # Extract session number
        m = re.search(r'\[S(\d+)\]', subject)
        session = int(m.group(1)) if m else 0
        commits.append({"hash": h, "subject": subject, "body": body, "session": session})
    return commits

def classify_c1(commits: list[dict]) -> dict:
    """Classify commits for C1 (duplicate work) signals."""
    c1_commits = []
    production_commits = []
    for c in commits:
        text = (c["subject"] + " " + c["body"]).lower()
        is_c1 = any(kw in text for kw in C1_KEYWORDS)
        is_relay = "relay" in text or "sync" in text or "scale" in text
        if is_c1 or is_relay:
            c1_commits.append(c)
        else:
            production_commits.append(c)
    total = len(commits)
    c1_rate = len(c1_commits) / total if total else 0
    return {
        "total_commits": total,
        "c1_count": len(c1_commits),
        "production_count": len(production_commits),
        "c1_rate": round(c1_rate, 4),
        "c1_examples": [c["subject"][:80] for c in c1_commits[:5]],
    }

# --- C3: lane orphaning from SWARM-LANES ---
def parse_lanes() -> dict:
    """Count ACTIVE/READY/DONE/BLOCKED lanes and detect orphans (no update in >5 sessions)."""
    path = ROOT / "tasks" / "SWARM-LANES.md"
    text = path.read_text(encoding="utf-8", errors="replace")
    
    rows = []
    for line in text.splitlines():
        if not line.startswith("|") or "---" in line:
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 7:
            continue
        status = parts[-2] if len(parts) >= 3 else ""
        session_str = parts[2] if len(parts) > 2 else ""
        rows.append({"raw": line, "status": status, "session": session_str})
    
    status_counts = {}
    for r in rows:
        s = r["status"].upper()
        if s and s not in ("STATUS", "---"):
            status_counts[s] = status_counts.get(s, 0) + 1
    
    active_states = {"ACTIVE", "CLAIMED", "READY", "BLOCKED"}
    active_rows = [r for r in rows if r["status"].upper() in active_states]
    
    # C3: READY lanes that have session markers < current-5 are orphaned
    current_session = 188
    orphaned = []
    for r in active_rows:
        m = re.search(r'S(\d+)', r["session"])
        if m:
            s_num = int(m.group(1))
            if current_session - s_num > 10 and r["status"].upper() == "READY":
                orphaned.append(r["raw"][:80])
    
    total_active = sum(status_counts.get(s, 0) for s in active_states)
    done = status_counts.get("MERGED", 0) + status_counts.get("DONE", 0) + status_counts.get("COMPLETED", 0)
    c3_rate = len(orphaned) / total_active if total_active else 0
    
    return {
        "status_counts": status_counts,
        "total_active": total_active,
        "done_count": done,
        "throughput_rate": round(done / (total_active + done) if (total_active + done) > 0 else 0, 4),
        "orphaned_count": len(orphaned),
        "c3_rate": round(c3_rate, 4),
        "orphaned_examples": orphaned[:5],
    }

def run(n: int = 40) -> dict:
    commits = parse_git_log(n)
    c1 = classify_c1(commits)
    c3 = parse_lanes()
    
    # Baseline verdict
    c1_elevated = c1["c1_rate"] > 0.3
    c3_elevated = c3["c3_rate"] > 0.4
    
    return {
        "experiment": "F-CON1",
        "title": "Conflict baseline: C1 duplicate-work + C3 lane-orphaning rates",
        "session": "S189",
        "date": "2026-02-28",
        "window_commits": n,
        "c1_duplicate_work": c1,
        "c3_lane_orphaning": c3,
        "baseline_verdict": {
            "c1_elevated": c1_elevated,
            "c3_elevated": c3_elevated,
            "c1_rate": c1["c1_rate"],
            "c3_rate": c3["c3_rate"],
            "throughput_rate": c3["throughput_rate"],
            "interpretation": (
                "Both C1 and C3 elevated — conflict expert lane needed immediately"
                if c1_elevated and c3_elevated else
                f"C1={'elevated' if c1_elevated else 'nominal'}, C3={'elevated' if c3_elevated else 'nominal'}"
            ),
        },
    }

if __name__ == "__main__":
    result = run()
    print(json.dumps(result, indent=2))

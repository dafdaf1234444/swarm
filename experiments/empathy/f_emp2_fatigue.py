#!/usr/bin/env python3
"""F-EMP2: Within-session quality degradation (empathy fatigue analog).

Measures whether lesson quality degrades as commit ordinal increases within
a session. Uses git log to extract per-session commit sequences, then
matches commits to lessons and extracts Sharpe scores.

Hypothesis: No degradation (flat Sharpe across commit order).
Falsification: Spearman |rho| > 0.15 between commit ordinal and Sharpe.
"""
import json
import re
import subprocess
import sys
from collections import defaultdict
from pathlib import Path
from scipy import stats

LESSONS_DIR = Path("memory/lessons")
OUTPUT = Path("experiments/empathy/f-emp2-fatigue-s541.json")


def get_session_commits():
    """Extract commits grouped by session from git log."""
    result = subprocess.run(
        ["git", "log", "--oneline", "--reverse", "--format=%H %s"],
        capture_output=True, text=True
    )
    sessions = defaultdict(list)
    for line in result.stdout.strip().split("\n"):
        if not line:
            continue
        parts = line.split(" ", 1)
        if len(parts) < 2:
            continue
        sha, msg = parts
        m = re.match(r"\[S(\d+)\]", msg)
        if m:
            s_num = int(m.group(1))
            sessions[s_num].append({"sha": sha[:12], "msg": msg, "ordinal": len(sessions[s_num])})
    return sessions


def extract_lesson_refs(msg):
    """Extract L-NNNN references from commit message."""
    return re.findall(r"L-(\d+)", msg)


def get_lesson_quality(lesson_id):
    """Extract Sharpe and level from a lesson file."""
    path = LESSONS_DIR / f"L-{lesson_id}.md"
    if not path.exists():
        return None
    try:
        text = path.read_text(encoding="utf-8", errors="replace")[:500]
    except Exception:
        return None
    sharpe = None
    level = None
    m = re.search(r"Sharpe:\s*(\d+)", text)
    if m:
        sharpe = int(m.group(1))
    m = re.search(r"level\s*=\s*(L\d)", text)
    if m:
        level = m.group(1)
    return {"sharpe": sharpe, "level": level}


def main():
    sessions = get_session_commits()

    # Filter: sessions with >= 3 commits (enough to detect gradient)
    multi_commit = {s: cs for s, cs in sessions.items() if len(cs) >= 3}

    # Collect (ordinal, quality) pairs
    ordinal_sharpe_pairs = []  # (relative_ordinal, sharpe)
    ordinal_level_pairs = []   # (relative_ordinal, level_numeric)
    session_details = {}

    level_map = {"L1": 1, "L2": 2, "L3": 3, "L4": 4, "L5": 5}

    for s_num in sorted(multi_commit.keys()):
        commits = multi_commit[s_num]
        n_commits = len(commits)
        session_lessons = []

        for c in commits:
            lesson_refs = extract_lesson_refs(c["msg"])
            for lr in lesson_refs:
                q = get_lesson_quality(lr)
                if q and q["sharpe"] is not None:
                    rel_ordinal = c["ordinal"] / max(n_commits - 1, 1)  # 0.0 to 1.0
                    ordinal_sharpe_pairs.append((rel_ordinal, q["sharpe"]))
                    session_lessons.append({
                        "lesson": f"L-{lr}",
                        "ordinal": c["ordinal"],
                        "rel_ordinal": round(rel_ordinal, 3),
                        "sharpe": q["sharpe"],
                        "level": q["level"]
                    })
                    if q["level"] in level_map:
                        ordinal_level_pairs.append((rel_ordinal, level_map[q["level"]]))

        if session_lessons:
            session_details[f"S{s_num}"] = {
                "n_commits": n_commits,
                "n_lessons_with_sharpe": len(session_lessons),
                "lessons": session_lessons
            }

    # Compute statistics
    if len(ordinal_sharpe_pairs) < 10:
        print(f"Insufficient data: {len(ordinal_sharpe_pairs)} pairs (need ≥10)")
        sys.exit(1)

    ordinals = [p[0] for p in ordinal_sharpe_pairs]
    sharpes = [p[1] for p in ordinal_sharpe_pairs]

    rho_sharpe, p_sharpe = stats.spearmanr(ordinals, sharpes)

    # Early vs late split
    early = [s for o, s in ordinal_sharpe_pairs if o <= 0.33]
    late = [s for o, s in ordinal_sharpe_pairs if o >= 0.67]
    early_mean = sum(early) / len(early) if early else 0
    late_mean = sum(late) / len(late) if late else 0

    # Level analysis
    rho_level = None
    p_level = None
    if len(ordinal_level_pairs) >= 10:
        l_ords = [p[0] for p in ordinal_level_pairs]
        l_vals = [p[1] for p in ordinal_level_pairs]
        rho_level, p_level = stats.spearmanr(l_ords, l_vals)

    # L3+ rate by position
    early_l3plus = sum(1 for o, l in ordinal_level_pairs if o <= 0.33 and l >= 3)
    early_total = sum(1 for o, _ in ordinal_level_pairs if o <= 0.33)
    late_l3plus = sum(1 for o, l in ordinal_level_pairs if o >= 0.67 and l >= 3)
    late_total = sum(1 for o, _ in ordinal_level_pairs if o >= 0.67)
    early_l3_rate = early_l3plus / early_total if early_total > 0 else 0
    late_l3_rate = late_l3plus / late_total if late_total > 0 else 0

    # Per-session gradient (does any session show strong degradation?)
    session_gradients = []
    for s_key, sd in session_details.items():
        lessons = sd["lessons"]
        if len(lessons) >= 3:
            s_ords = [l["rel_ordinal"] for l in lessons]
            s_sharps = [l["sharpe"] for l in lessons]
            if len(set(s_sharps)) > 1:  # need variance
                r, p = stats.spearmanr(s_ords, s_sharps)
                session_gradients.append({"session": s_key, "rho": round(r, 3), "p": round(p, 4), "n": len(lessons)})

    degrading = sum(1 for sg in session_gradients if sg["rho"] < -0.3)
    improving = sum(1 for sg in session_gradients if sg["rho"] > 0.3)

    # Verdict
    fatigue_detected = abs(rho_sharpe) > 0.15 and p_sharpe < 0.05
    verdict = "FATIGUE DETECTED" if fatigue_detected else "NO FATIGUE"
    if rho_sharpe < -0.15 and p_sharpe < 0.05:
        verdict = "FATIGUE CONFIRMED — quality degrades with position"
    elif rho_sharpe > 0.15 and p_sharpe < 0.05:
        verdict = "ANTI-FATIGUE — quality IMPROVES with position (warmup effect)"

    result = {
        "experiment": "F-EMP2: Within-session quality degradation",
        "session": "S541",
        "date": "2026-03-24",
        "hypothesis": "No degradation: Sharpe flat across commit order",
        "method": "Spearman correlation of relative commit ordinal vs Sharpe score",
        "data": {
            "total_sessions_analyzed": len(multi_commit),
            "sessions_with_lessons": len(session_details),
            "total_ordinal_sharpe_pairs": len(ordinal_sharpe_pairs),
            "total_ordinal_level_pairs": len(ordinal_level_pairs),
        },
        "results": {
            "sharpe_gradient": {
                "spearman_rho": round(rho_sharpe, 4),
                "p_value": round(p_sharpe, 6),
                "early_third_mean": round(early_mean, 2),
                "late_third_mean": round(late_mean, 2),
                "delta": round(late_mean - early_mean, 2),
            },
            "level_gradient": {
                "spearman_rho": round(rho_level, 4) if rho_level is not None else None,
                "p_value": round(p_level, 6) if p_level is not None else None,
                "early_l3plus_rate": round(early_l3_rate, 3),
                "late_l3plus_rate": round(late_l3_rate, 3),
            },
            "per_session": {
                "sessions_with_gradient": len(session_gradients),
                "degrading_sessions": degrading,
                "improving_sessions": improving,
                "neutral_sessions": len(session_gradients) - degrading - improving,
            }
        },
        "verdict": verdict,
        "falsification_threshold": "|rho| > 0.15 and p < 0.05",
    }

    # Print summary
    print(f"=== F-EMP2: Within-Session Quality Gradient ===")
    print(f"Sessions analyzed: {len(multi_commit)} (≥3 commits)")
    print(f"Sessions with lesson data: {len(session_details)}")
    print(f"Ordinal-Sharpe pairs: {len(ordinal_sharpe_pairs)}")
    print(f"\nSharpe gradient: rho={rho_sharpe:.4f}, p={p_sharpe:.6f}")
    print(f"  Early third mean: {early_mean:.2f}")
    print(f"  Late third mean:  {late_mean:.2f}")
    print(f"  Delta:            {late_mean - early_mean:+.2f}")
    if rho_level is not None:
        print(f"\nLevel gradient: rho={rho_level:.4f}, p={p_level:.6f}")
    print(f"  Early L3+ rate:   {early_l3_rate:.1%}")
    print(f"  Late L3+ rate:    {late_l3_rate:.1%}")
    print(f"\nPer-session: {degrading} degrading, {improving} improving, {len(session_gradients) - degrading - improving} neutral")
    print(f"\n>>> VERDICT: {verdict}")

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(json.dumps(result, indent=2) + "\n")
    print(f"\nArtifact: {OUTPUT}")


if __name__ == "__main__":
    main()

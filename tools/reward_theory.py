#!/usr/bin/env python3
"""
reward_theory.py — Map, measure, and audit the swarm's implicit reward channels.

L-1127 identified 6 reward channels with 5/6 Goodharted. This tool makes the
reward structure visible so it can be improved.

Usage:
    python3 tools/reward_theory.py              # full audit
    python3 tools/reward_theory.py --summary    # one-line alignment score
    python3 tools/reward_theory.py --channel N  # deep-dive channel N (1-6)
    python3 tools/reward_theory.py --session SN # per-session reward profile (M3)
    python3 tools/reward_theory.py --json       # JSON output (combinable)

Part of F-SWARMER1 colony: swarmer-swarm anti-attractor intervention #1.
Per-session tracking enables M3 (L-1131): sessions declare + measure reward targeting.
"""

import json as json_mod
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _count_lessons():
    """Count total lessons."""
    lesson_dir = ROOT / "memory" / "lessons"
    if not lesson_dir.exists():
        return 0
    return len([f for f in lesson_dir.iterdir() if f.name.startswith("L-") and f.suffix == ".md"])


def _count_principles():
    """Count principles from PRINCIPLES.md header."""
    pfile = ROOT / "memory" / "PRINCIPLES.md"
    if not pfile.exists():
        return 0
    text = pfile.read_text(errors="replace")
    removed_idx = text.find("Removed:")
    active = text[:removed_idx] if removed_idx > 0 else text
    return len(re.findall(r'\bP-\d+\b', active))


def _measure_channel_1_compaction():
    """Channel 1: Context window selection pressure — favors compactness."""
    lesson_dir = ROOT / "memory" / "lessons"
    if not lesson_dir.exists():
        return {"aligned": False, "metric": "unknown", "detail": "no lessons"}

    total = 0
    under_20 = 0
    for f in lesson_dir.iterdir():
        if f.name.startswith("L-") and f.suffix == ".md":
            total += 1
            lines = f.read_text(errors="replace").strip().split("\n")
            if len(lines) <= 20:
                under_20 += 1

    compact_rate = under_20 / total if total > 0 else 0
    return {
        "aligned": False,  # structural Goodhart — compactness proxy for value
        "metric": f"{compact_rate:.1%} lessons ≤20 lines",
        "detail": f"{under_20}/{total} compact. Goodhart: shorter != better. Fix: reward Sharpe*compactness, not compactness alone.",
        "goodhart_type": "proxy_for_value"
    }


def _measure_channel_2_citations():
    """Channel 2: Citation in-degree — rewards being mentioned, not mechanism quality."""
    lesson_dir = ROOT / "memory" / "lessons"
    if not lesson_dir.exists():
        return {"aligned": False, "metric": "unknown"}

    cite_counts = {}
    total = 0
    for f in sorted(lesson_dir.iterdir()):
        if not (f.name.startswith("L-") and f.suffix == ".md"):
            continue
        total += 1
        text = f.read_text(errors="replace")
        refs = re.findall(r'\bL-(\d+)\b', text)
        for ref in refs:
            lid = f"L-{ref}"
            if lid != f.stem:
                cite_counts[lid] = cite_counts.get(lid, 0) + 1

    cited = len([v for v in cite_counts.values() if v > 0])
    uncited = total - cited
    top_5 = sorted(cite_counts.items(), key=lambda x: -x[1])[:5]

    return {
        "aligned": False,
        "metric": f"{cited}/{total} cited ({cited/total:.0%}), {uncited} orphans",
        "detail": f"Top 5: {', '.join(f'{k}={v}' for k,v in top_5)}. Goodhart: citation rewards presence, not mechanism invocation (L-1057).",
        "goodhart_type": "presence_not_mechanism"
    }


def _measure_channel_3_dispatch():
    """Channel 3: UCB1 dispatch — rewards high merge-rate, not value produced."""
    lanes_path = ROOT / "tasks" / "SWARM-LANES.md"
    if not lanes_path.exists():
        return {"aligned": False, "metric": "unknown"}

    text = lanes_path.read_text(errors="replace")
    merged = len(re.findall(r'\bMERGED\b', text))
    abandoned = len(re.findall(r'\bABANDONED\b', text))
    total = merged + abandoned
    merge_rate = merged / total if total > 0 else 0

    scoring_path = ROOT / "tools" / "dispatch_scoring.py"
    sharpe_weighted = False
    if scoring_path.exists():
        scoring_text = scoring_path.read_text(errors="replace")
        sharpe_weighted = "sharpe_factor" in scoring_text and "sharpe_sum" in scoring_text

    if sharpe_weighted:
        return {
            "aligned": True,
            "metric": f"{merge_rate:.0%} merge rate ({merged}/{total})",
            "detail": f"ALIGNED (S463). UCB1 exploit term now Sharpe-weighted: quality = merge_rate × log(lessons) × (avg_sharpe/7.7). High-Sharpe domains score higher regardless of merge rate.",
            "goodhart_type": None
        }

    return {
        "aligned": False,
        "metric": f"{merge_rate:.0%} merge rate ({merged}/{total})",
        "detail": f"Goodhart: easy/safe lanes merge more. Fix: weight by Sharpe of produced lessons.",
        "goodhart_type": "mergeability_not_value"
    }


def _measure_channel_4_sharpe():
    """Channel 4: Sharpe ratio — rewards recency, not depth."""
    lesson_dir = ROOT / "memory" / "lessons"
    if not lesson_dir.exists():
        return {"aligned": False, "metric": "unknown"}

    sharpe_vals = []
    for f in sorted(lesson_dir.iterdir()):
        if not (f.name.startswith("L-") and f.suffix == ".md"):
            continue
        text = f.read_text(errors="replace")
        m = re.search(r'Sharpe:\s*(\d+)', text)
        if m:
            sharpe_vals.append(int(m.group(1)))

    if not sharpe_vals:
        return {"aligned": False, "metric": "no Sharpe data"}

    avg = sum(sharpe_vals) / len(sharpe_vals)
    recent_50 = sharpe_vals[-50:] if len(sharpe_vals) >= 50 else sharpe_vals
    recent_avg = sum(recent_50) / len(recent_50)

    return {
        "aligned": False,
        "metric": f"avg {avg:.1f}, recent-50 avg {recent_avg:.1f}",
        "detail": f"n={len(sharpe_vals)} lessons with Sharpe. Goodhart: recency inflates score. Fix: separate depth score from freshness score.",
        "goodhart_type": "recency_not_depth"
    }


def _measure_channel_5_falsification():
    """Channel 5: Falsification premium — the ONLY correctly-aligned channel."""
    lesson_dir = ROOT / "memory" / "lessons"
    if not lesson_dir.exists():
        return {"aligned": True, "metric": "unknown"}

    falsified_count = 0
    total = 0
    for f in sorted(lesson_dir.iterdir()):
        if not (f.name.startswith("L-") and f.suffix == ".md"):
            continue
        total += 1
        text = f.read_text(errors="replace").lower()
        if "falsif" in text:
            falsified_count += 1

    rate = falsified_count / total if total > 0 else 0

    return {
        "aligned": True,
        "metric": f"{rate:.1%} lessons mention falsification ({falsified_count}/{total})",
        "detail": "ALIGNED. Productive wrongness gets 2.4x citation (L-698). Incentive correct: being wrong and learning > being right and stagnant.",
        "goodhart_type": None
    }


def _measure_channel_6_survival():
    """Channel 6: Compactification survival — used tools persist, unused die."""
    tools_dir = ROOT / "tools"
    if not tools_dir.exists():
        return {"aligned": False, "metric": "unknown"}

    py_tools = [f for f in tools_dir.iterdir() if f.suffix == ".py"]
    total = len(py_tools)

    return {
        "aligned": False,
        "metric": f"{total} tools in tools/",
        "detail": "Goodhart: survival rewards being referenced in orient/maintenance, not producing value. Zombie tools persist because nothing actively removes them. Fix: tool sunset protocol (unused >30 sessions → archive).",
        "goodhart_type": "survival_not_merit"
    }


CHANNELS = [
    ("Context selection pressure", _measure_channel_1_compaction),
    ("Citation in-degree", _measure_channel_2_citations),
    ("UCB1 dispatch allocation", _measure_channel_3_dispatch),
    ("Sharpe ratio", _measure_channel_4_sharpe),
    ("Falsification premium", _measure_channel_5_falsification),
    ("Compactification survival", _measure_channel_6_survival),
]


# --- Per-session reward profiling (M3 tracking, L-1131) ---

def _get_session_lessons(session_id):
    """Find lessons produced by a session (reads Session: header)."""
    lesson_dir = ROOT / "memory" / "lessons"
    if not lesson_dir.exists():
        return []
    sid_num = re.sub(r'\D', '', session_id)
    results = []
    for f in sorted(lesson_dir.iterdir()):
        if not (f.name.startswith("L-") and f.suffix == ".md"):
            continue
        text = f.read_text(errors="replace")
        if re.search(rf'Session:\s*S{sid_num}\b', text):
            results.append((f.stem, text))
    return results


def _get_session_lanes(session_id):
    """Find lanes involving a session from SWARM-LANES.md."""
    lanes_path = ROOT / "tasks" / "SWARM-LANES.md"
    if not lanes_path.exists():
        return []
    text = lanes_path.read_text(errors="replace")
    sid = session_id.upper() if session_id.startswith(("s", "S")) else f"S{session_id}"
    results = []
    for line in text.split("\n"):
        if not line.startswith("|") or "---" in line:
            continue
        if sid in line:
            status_m = re.search(r'\b(MERGED|ABANDONED|ACTIVE|CLAIMED|BLOCKED)\b', line)
            status = status_m.group(1) if status_m else "UNKNOWN"
            lane_m = re.search(r'DOMEX-\S+', line)
            lane_id = lane_m.group(0).rstrip(" |") if lane_m else "unknown"
            results.append({"lane": lane_id, "status": status})
    return results


def session_reward_profile(session_id):
    """Analyze which reward channels a session engaged (M3 per-session tracking)."""
    lessons = _get_session_lessons(session_id)
    lanes = _get_session_lanes(session_id)

    channels = {}
    for i in range(1, 7):
        channels[i] = {"name": CHANNELS[i - 1][0], "engaged": False, "evidence": []}

    for lid, text in lessons:
        lines = text.strip().split("\n")
        # Ch1: lesson compactness
        if len(lines) <= 20:
            channels[1]["engaged"] = True
            channels[1]["evidence"].append(f"{lid}: {len(lines)}L (compact)")

        # Ch2: citation production
        cites_m = re.search(r'Cites:\s*(.+)', text)
        if cites_m:
            cite_count = len(re.findall(r'L-\d+', cites_m.group(1)))
            if cite_count > 0:
                channels[2]["engaged"] = True
                channels[2]["evidence"].append(f"{lid}: cites {cite_count} lessons")

        # Ch4: Sharpe
        sharpe_m = re.search(r'Sharpe:\s*(\d+)', text)
        if sharpe_m:
            channels[4]["engaged"] = True
            channels[4]["evidence"].append(f"{lid}: Sharpe {sharpe_m.group(1)}")

        # Ch5: falsification
        if "falsif" in text.lower():
            channels[5]["engaged"] = True
            channels[5]["evidence"].append(f"{lid}: falsification content")

        # Ch6: tool references
        if re.search(r'tools/\w+\.py', text):
            channels[6]["engaged"] = True
            channels[6]["evidence"].append(f"{lid}: references tools/")

    # Ch3: lane merges
    merged = [l for l in lanes if l["status"] == "MERGED"]
    if merged:
        channels[3]["engaged"] = True
        channels[3]["evidence"] = [f"{l['lane']}: MERGED" for l in merged]

    engaged_count = sum(1 for c in channels.values() if c["engaged"])
    return channels, engaged_count, 6, lessons, lanes


def print_session_profile(session_id):
    """Print per-session reward profile."""
    channels, engaged, total, lessons, lanes = session_reward_profile(session_id)
    print(f"=== SESSION {session_id.upper()} REWARD PROFILE (M3) ===")
    print(f"Channels engaged: {engaged}/{total} = {engaged / total:.0%}")
    print(f"Lessons: {len(lessons)} | Lanes: {len(lanes)}\n")

    for i in range(1, 7):
        ch = channels[i]
        icon = "+" if ch["engaged"] else "-"
        print(f"  {icon} Ch{i}: {ch['name']}")
        for ev in ch["evidence"]:
            print(f"      {ev}")

    gaps = [channels[i]["name"] for i in range(1, 7) if not channels[i]["engaged"]]
    if gaps:
        print(f"\n  Gaps: {', '.join(gaps)}")
        print(f"  M3: next session should target one of these channels")
    print()


# --- Core audit ---

def audit_all():
    """Run full reward channel audit."""
    results = []
    aligned = 0
    for name, fn in CHANNELS:
        r = fn()
        r["name"] = name
        results.append(r)
        if r.get("aligned"):
            aligned += 1
    return results, aligned, len(CHANNELS)


def print_audit(results, aligned, total):
    """Print formatted audit."""
    print(f"=== REWARD THEORY AUDIT (L-1127, F-SWARMER1) ===")
    print(f"Alignment: {aligned}/{total} = {aligned / total:.0%}\n")

    for i, r in enumerate(results, 1):
        status = "ALIGNED" if r.get("aligned") else "GOODHARTED"
        icon = "\u2713" if r.get("aligned") else "\u2717"
        print(f"  {icon} Channel {i}: {r['name']} [{status}]")
        print(f"    Metric: {r.get('metric', 'unknown')}")
        if r.get("detail"):
            print(f"    {r['detail']}")
        if r.get("goodhart_type"):
            print(f"    Goodhart type: {r['goodhart_type']}")
        print()

    print(f"--- Prescription ---")
    print(f"  Target: {aligned}/{total} \u2192 {aligned + 1}/{total} (next channel to fix)")
    goodharted = [r for r in results if not r.get("aligned")]
    if goodharted:
        easiest = goodharted[0]
        print(f"  Lowest-effort fix: {easiest['name']}")
        print(f"  Mechanism: replace proxy metric with composite (proxy \u00d7 quality)")
    print()


def print_summary():
    """Print one-line alignment score."""
    _, aligned, total = audit_all()
    print(f"Reward alignment: {aligned}/{total} = {aligned / total:.0%} (target: \u226533%, L-1127)")


def main():
    args = sys.argv[1:]
    use_json = "--json" in args

    if "--session" in args:
        idx = args.index("--session")
        if idx + 1 < len(args):
            sid = args[idx + 1]
            if use_json:
                channels, engaged, total, lessons, lanes = session_reward_profile(sid)
                out = {
                    "session": sid.upper(),
                    "engaged": engaged,
                    "total": total,
                    "rate": f"{engaged / total:.0%}",
                    "lessons_produced": len(lessons),
                    "lanes": len(lanes),
                    "channels": {
                        i: {"name": c["name"], "engaged": c["engaged"], "evidence": c["evidence"]}
                        for i, c in channels.items()
                    },
                    "gaps": [c["name"] for c in channels.values() if not c["engaged"]],
                }
                print(json_mod.dumps(out, indent=2))
            else:
                print_session_profile(sid)
        else:
            print("Usage: --session SNN")
    elif "--summary" in args:
        if use_json:
            _, aligned, total = audit_all()
            print(json_mod.dumps({"aligned": aligned, "total": total, "rate": f"{aligned / total:.0%}"}))
        else:
            print_summary()
    elif "--channel" in args:
        idx = args.index("--channel")
        if idx + 1 < len(args):
            ch = int(args[idx + 1]) - 1
            if 0 <= ch < len(CHANNELS):
                name, fn = CHANNELS[ch]
                r = fn()
                r["name"] = name
                if use_json:
                    print(json_mod.dumps(r, indent=2))
                else:
                    print_audit([r], 1 if r.get("aligned") else 0, 1)
            else:
                print(f"Channel must be 1-{len(CHANNELS)}")
        else:
            print("Usage: --channel N")
    else:
        results, aligned, total = audit_all()
        if use_json:
            print(json_mod.dumps({
                "aligned": aligned, "total": total,
                "rate": f"{aligned / total:.0%}",
                "channels": results,
            }, indent=2))
        else:
            print_audit(results, aligned, total)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
orient_sections.py — Display sections for orient.py main() output.

Extracted from orient.py (DOMEX-META-S426). Each function returns a list of
output lines for one section of the orient display. main() in orient.py
calls these in sequence and prints.

Pattern: section_xxx(data) -> list[str]
"""

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def _cached_artifact(root, subdir, pattern, session_num, max_age=20, min_age=-5):
    """Load latest cached JSON artifact. Returns (data, age_str) or None."""
    try:
        files = sorted((root / "experiments" / subdir).glob(pattern))
        if not files:
            return None
        data = json.loads(files[-1].read_text())
        m = re.search(r"-s(\d+)", files[-1].name)
        if not m:
            return None
        age = session_num - int(m.group(1))
        if min_age <= age <= max_age:
            return data, f"S{m.group(1)}" + (f", {age}s ago" if age > 0 else "")
    except Exception:
        pass
    return None


def _run_tool_json(tool_name, args=None, timeout=15, root=ROOT):
    """Run a tool and parse JSON output. Returns dict or None."""
    cmd = [sys.executable, str(root / "tools" / f"{tool_name}.py")] + (args or [])
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return json.loads(r.stdout) if r.returncode == 0 and r.stdout.strip() else None
    except Exception:
        return None


def section_maintenance(maint_out, maint_level, brief):
    """Maintenance details section."""
    lines = []
    if not brief or maint_level != "NOTICE-only":
        signal_lines = [l for l in maint_out.splitlines()
                        if l.strip() and "===" not in l and "maintenance" not in l.lower()[:10]]
        if signal_lines:
            lines.append("--- Maintenance ---")
            for line in signal_lines[:10]:
                lines.append(f"  {line}")
            lines.append("")
    return lines


def section_session_triggers(session_num, maint_out, evaluate_fn):
    """Session triggers (F-META6)."""
    lines = []
    try:
        top_trigger, active_triggers = evaluate_fn(session_num, maint_out=maint_out)
        if top_trigger:
            lines.append("--- Session Triggers (F-META6) ---")
            lines.append(f"  \U0001f534 {top_trigger[2]}: {top_trigger[0]} — {top_trigger[1][:80]}")
            if len(active_triggers) > 1:
                lines.append(f"  \U0001f4cb {len(active_triggers)-1} additional triggers active")
            lines.append("")
    except Exception:
        pass
    return lines


def section_open_signals(open_signals):
    """Open signals (L-703, L-803, L-808)."""
    lines = []
    if open_signals:
        lines.append(f"--- Open signals ({len(open_signals)} unresolved) ---")
        for sig in open_signals[:5]:
            age_tag = f" ({sig['age']}s ago)" if sig['age'] else ""
            icon = '\U0001f4e2' if sig['priority'] == 'P1' else '\U0001f4cb'
            lines.append(f"  {icon} {sig['id']}{age_tag}: {sig['content'][:90]}")
        if len(open_signals) > 5:
            lines.append(f"  ... and {len(open_signals) - 5} more")
        neglected = [s for s in open_signals if s.get("age", 0) > 20]
        if neglected:
            p1_neg = [s for s in neglected if s["priority"] == "P1"]
            tag = f" including {len(p1_neg)} P1" if p1_neg else ""
            lines.append(f"  \u26a0 BACKLOG: {len(neglected)} signals >20s old{tag} — sensing without acting")
            lines.append(f"    Oldest: {neglected[0]['id']} (age {neglected[0]['age']}s): {neglected[0]['content'][:60]}")
        lines.append("")
    return lines


def section_index_coverage(index_text, check_fn):
    """INDEX.md coverage check (F-BRN4)."""
    lines = []
    index_notice = check_fn(index_text)
    if index_notice:
        lines.append(f"  {index_notice}")
        lines.append("")
    return lines


def section_precompact_checkpoint(session, root=ROOT):
    """PreCompact checkpoint notice (F-CC3, L-342)."""
    lines = []
    checkpoints = sorted((root / "workspace").glob("precompact-checkpoint-*.json"),
                         key=lambda p: p.stat().st_mtime)
    if not checkpoints:
        return lines
    try:
        cp = json.loads(checkpoints[-1].read_text())
        uncommitted = cp.get("uncommitted_files", [])
        still_uncommitted, stale_ratio = [], 1
        if uncommitted:
            status_out = subprocess.run(["git", "status", "--short"], capture_output=True, text=True, cwd=str(root)).stdout
            status_files = {l.split()[-1] for l in status_out.strip().split("\n") if l.strip()}
            still_uncommitted = [f for f in uncommitted if f in status_files]
            stale_ratio = 1 - (len(still_uncommitted) / len(uncommitted))
        cp_session = next((int(re.search(r'\[S(\d+)\]', l).group(1)) for l in cp.get("recent_git_log", []) if re.search(r'\[S(\d+)\]', l)), 0)
        cur_num = int(session[1:]) if session[1:].isdigit() else 0
        if stale_ratio < 0.8 and (cur_num - cp_session if cp_session else 999) <= 2:
            absorbed = []
            if still_uncommitted and cp_session:
                try:
                    log_out = subprocess.run(["git", "log", "--name-only", "--format=", "--diff-filter=M", "HEAD~10..HEAD"], capture_output=True, text=True, cwd=str(root)).stdout
                    committed = {l.strip() for l in log_out.splitlines() if l.strip()}
                    absorbed = [f for f in still_uncommitted if f in committed]
                except Exception:
                    pass
            lines.append("--- !! COMPACTION RESUME DETECTED ---")
            lines.append(f"  Checkpoint: {checkpoints[-1].name} ({cp.get('trigger', '?')} at {cp.get('timestamp', '?')})")
            hint = cp.get("next_md", {}).get("For next session", "")
            if hint:
                lines.append(f"  In-flight: {hint[:120].splitlines()[0]}")
            if still_uncommitted:
                lines.append(f"  Uncommitted files ({len(still_uncommitted)}/{len(uncommitted)}): {', '.join(still_uncommitted[:5])}")
            if absorbed:
                lines.append(f"  \u26a0 Likely proxy-absorbed ({len(absorbed)}/{len(still_uncommitted)}): working tree diffs may be stale (L-526)")
            staged = cp.get("staged_files", [])
            if staged:
                lines.append(f"  \u26a0 STAGED FILES ({len(staged)}): {', '.join(staged[:5])}")
                lines.append(f"    Run: git reset HEAD -- <files> before staging new work (FM-19 stale-write risk)")
            lines.append("")
    except Exception:
        pass
    return lines


def section_key_state(key_state):
    """Key state from NEXT.md."""
    lines = []
    if key_state:
        lines.append("--- Key state ---")
        for s in key_state:
            lines.append(f"  {s}")
        lines.append("")
    return lines


def section_priorities(priorities):
    """Priorities from NEXT.md."""
    lines = []
    if priorities:
        lines.append("--- Priorities ---")
        for i, p in enumerate(priorities, 1):
            lines.append(f"  {i}. {p}")
        lines.append("")
    return lines


def section_frontiers(frontiers):
    """Open frontiers (critical/important)."""
    lines = []
    if frontiers:
        lines.append("--- Open frontiers (critical/important) ---")
        for f in frontiers:
            lines.append(f"  \u2022 {f}")
        lines.append("")
    return lines


def section_stale_beliefs(session_num, check_fn):
    """Stale beliefs — untested >50 sessions (L-483)."""
    lines = []
    try:
        stale_beliefs = check_fn(session_num)
        if stale_beliefs:
            lines.append(f"--- Stale beliefs ({len(stale_beliefs)} not re-tested >50 sessions) ---")
            for b in stale_beliefs[:5]:
                lines.append(f"  \u26a0 {b}")
            lines.append("")
    except Exception:
        pass
    return lines


def section_self_application(session_num, check_fn):
    """Self-application gap — CORE P14: infrastructure subject to swarm dynamics."""
    lines = []
    try:
        stale_infra = check_fn(session_num)
        if stale_infra:
            lines.append(f"--- Self-application gap ({len(stale_infra)} components not evolved >50s) ---")
            for si in stale_infra:
                lines.append(f"  \u2298 {si}")
            lines.append("  Suggested (pick 1):")
            for si in stale_infra[:3]:
                name = si.split("(")[0].strip().replace(" ", "-")
                lines.append(f"    python3 tools/open_lane.py --lane EVOLVE-{name}-S{session_num} --session S{session_num} --expect 'modernize-{name}' --artifact 'tools/{si.split('(')[0].strip()}' --intent 'P14: evolve stale infrastructure'")
            lines.append("")
    except Exception:
        pass
    return lines


def section_stale_lanes(current_sess_num, check_fn):
    """Stale lanes — cross-session open lanes (L-515)."""
    lines = []
    try:
        stale_lanes = check_fn(current_sess_num)
        if stale_lanes:
            lines.append(f"--- Stale lanes ({len(stale_lanes)} opened in prior session — execute or close) ---")
            for sl in stale_lanes:
                art_note = "\u2717 artifact missing" if not sl["has_artifact"] else "\u2713 artifact exists"
                gap = sl.get("gap", 1)
                gap_warn = f" — GAP={gap}s \u26a0 67% abandon rate (L-733)" if gap > 2 else ""
                lines.append(f"  \u26a0 {sl['lane']} (S{sl['opened']}) — {art_note}{gap_warn}")
            closeable = [sl for sl in stale_lanes if not sl["has_artifact"]]
            if closeable:
                lines.append("  Close stale (no artifact):")
                for sl in closeable[:3]:
                    lines.append(
                        f"    python3 tools/close_lane.py --lane {sl['lane']}"
                        f" --status ABANDONED --note 'stale — no artifact produced'"
                    )
            lines.append("")
        return lines, stale_lanes
    except Exception:
        return lines, []


def section_pci(session_num, compute_fn, root=ROOT):
    """Scientific Rigor — Protocol Compliance Index (PCI)."""
    lines = []
    try:
        pci_result = compute_fn(session_num)
        pci_val = pci_result["pci"]
        d = pci_result["details"]
        lines.append("--- Scientific Rigor (PCI) ---")
        lines.append(f"  PCI: {pci_val:.3f} (target >0.10)")
        lines.append(f"  EAD field presence: {pci_result['ead']:.0%} ({d['ead']} lanes with actual+diff — L-813: measures field presence, not prediction quality)")
        lines.append(f"  Belief freshness: {pci_result['belief_freshness']:.0%} ({d['belief_freshness']} tested <50 sessions)")
        lines.append(f"  Frontier testability: {pci_result['frontier_testability']:.0%} ({d['frontier_testability']} with test evidence)")
        # Cached artifact displays
        ks = _cached_artifact(root, "meta", "knowledge-state-s*.json", session_num, max_age=20, min_age=0)
        if ks:
            dist = ks[0].get("global_states", {}); total = sum(dist.values()) or 1
            lines.append(f"  Knowledge attention ({ks[1]}): BLIND-SPOT {dist.get('BLIND-SPOT',0)/total:.1%} | DECAYED {dist.get('DECAYED',0)/total:.1%} (L-813: citation-recency, not validity — actual false knowledge ~5-10%) | refresh: python3 tools/knowledge_state.py --json")
        sq = _cached_artifact(root, "meta", "science-quality-s*.json", session_num, max_age=30)
        if sq:
            lines.append(f"  Science quality ({sq[1]}): mean {sq[0].get('mean_quality',0):.0%} | pre-reg {sq[0].get('criteria_means',{}).get('pre_registration',0):.0%} | falsif lanes {sq[0].get('falsification_lanes','?/0')} | refresh: python3 tools/science_quality.py --json")
        bm = _cached_artifact(root, "meta", "bayes-meta-s*.json", session_num, max_age=30)
        if bm:
            ece = bm[0].get("results", {}).get("ece", "?")
            ece_flag = " \u26a0 OVERCONFIDENT" if isinstance(ece, float) and ece > 0.15 else ""
            lines.append(f"  Bayesian calibration ({bm[1]}): ECE={ece:.3f}{ece_flag} | {bm[0].get('n_frontiers_with_posteriors','?')} frontiers | refresh: python3 tools/bayes_meta.py --json > experiments/meta/bayes-meta-s<N>.json")
        es = _cached_artifact(root, "evaluation", "eval-sufficiency-s*.json", session_num, max_age=50)
        if es:
            cont = es[0].get("continuous_composite", es[0].get("composite_normalized"))
            cont_str = f" ({cont:.0%} continuous)" if cont is not None else ""
            lines.append(f"  Mission sufficiency ({es[1]}): {es[0].get('overall','?')}{cont_str} — next: {es[0].get('next_improvement_target','?')} | refresh: python3 tools/eval_sufficiency.py --save")
        if pci_val < 0.10:
            lines.append("  Tip: check `beliefs/CHALLENGES.md` for untested beliefs and open a DOMEX lane")
        lines.append("")
    except Exception:
        pass
    return lines


def section_prescription_gap(root=ROOT):
    """Prescription gap (L-831/L-843/L-875)."""
    lines = []
    try:
        er_path = root / "tools" / "enforcement_router.py"
        if er_path.exists():
            er_result = subprocess.run(
                [sys.executable, str(er_path), "--json", "--min-sharpe", "9"],
                capture_output=True, text=True, timeout=10
            )
            if er_result.returncode == 0:
                er_data = json.loads(er_result.stdout)
                act_rate = er_data.get("actionable_gap_rate", 0)
                n_act = er_data.get("actionable_aspirational_count", 0)
                n_obs = er_data.get("observational_aspirational_count", 0)
                hs_asp = er_data.get("high_sharpe_aspirational", [])
                if act_rate > 0.15:
                    lines.append("--- Prescription Gap (L-843) ---")
                    lines.append(f"  ASPIRATIONAL (unimplemented): {act_rate:.0%} of rule-bearing lessons ({n_act} actionable, {n_obs} observational)")
                    act_gaps = [h for h in hs_asp if h.get("actionable")]
                    if act_gaps:
                        top = act_gaps[0]
                        lines.append(f"  Top gap: {top['lesson']} Sh={top['sharpe']} — {top['rule'][:70]}")
                    lines.append("  Full report: python3 tools/enforcement_router.py")
                    lines.append("")
    except Exception:
        pass
    return lines


def section_level_balance(root=ROOT):
    """Level balance check (L-895/SIG-46)."""
    lines = []
    try:
        import glob as _glob_lvl
        lesson_files = sorted(_glob_lvl.glob(str(root / "memory" / "lessons" / "L-*.md")))
        if len(lesson_files) >= 10:
            recent_n = lesson_files[-10:]
            l3plus_kw = ["strategy", "campaign", "architecture", "organizational",
                         "paradigm", "redesign", "direction", "what should", "reframing",
                         "missing layer", "system design", "philosophy", "identity"]
            l3plus_count = 0
            for lf in recent_n:
                try:
                    txt = Path(lf).read_text()
                    if re.search(r"[Ll]evel[=:\s]+L[3-5]", txt):
                        l3plus_count += 1
                        continue
                    txt_lower = txt.lower()
                    if any(k in txt_lower for k in l3plus_kw):
                        l3plus_count += 1
                except Exception:
                    pass
            if l3plus_count == 0:
                lines.append("--- Level Imbalance (L-895, SIG-46) ---")
                lines.append(f"  \u26a0 0/{len(recent_n)} recent lessons at L3+ (strategy/architecture/paradigm)")
                lines.append("  Swarm is 100% measurement. Consider: strategic direction, architecture review,")
                lines.append("  or paradigm challenge instead of another DOMEX experiment.")
                lines.append("")
    except Exception:
        pass
    return lines


def section_succession_phase(root=ROOT):
    """Attention carrying capacity / r-K phase indicator (L-1121)."""
    lines = []
    try:
        import glob as _gl
        n_lessons = len(_gl.glob(str(root / "memory" / "lessons" / "L-*.md")))
        if n_lessons < 100:
            return lines
        attn = 1.0 / n_lessons
        threshold = 1.0 / 500  # integration-bound crossover at N~550 (L-912)
        if attn >= threshold:
            return lines
        def _count_lessons(diff_filter):
            try:
                r = subprocess.run(["git", "log", "--oneline", f"--diff-filter={diff_filter}", "--name-only", "-10", "--", "memory/lessons/L-*.md"], capture_output=True, text=True, cwd=str(root), timeout=5)
                return len([l for l in r.stdout.splitlines() if l.startswith("memory/lessons/L-") and l.endswith(".md")])
            except Exception:
                return 0
        new_l, mod_l = _count_lessons("A"), _count_lessons("M")
        lines.append("--- Succession Phase (L-1121) ---")
        lines.append(f"  Attention carrying capacity: {n_lessons/500:.1f}x past threshold (N={n_lessons}, K_threshold=500)")
        lines.append(f"  Attention per lesson: {attn:.5f} (threshold: {threshold:.4f})")
        if new_l > 0 or mod_l > 0:
            r_k = new_l / max(mod_l, 1)
            mode = "r-mode (producing)" if r_k > 2 else "K-mode (integrating)" if r_k < 0.5 else "balanced"
            lines.append(f"  Recent r/K: {new_l} new / {mod_l} modified = {r_k:.1f} ({mode})")
            if r_k > 3:
                lines.append("  \u26a0 High r/K ratio — consider integration: compact, cross-reference, revive DECAYED")
        lines.append("")
    except Exception:
        pass
    return lines


def section_stalled_campaigns(root=ROOT):
    """Stalled 2-wave campaigns (F-STR3, L-845)."""
    stall_map: dict[str, str] = {}
    lines = []
    data = _run_tool_json("dispatch_optimizer", ["--json", "--all"], root=root)
    if data:
        for d in data:
            for fid in (d.get("wave_2_stalls") or []):
                stall_map[fid] = d["domain"]
    if stall_map:
        lines.append(f"--- Stalled Campaigns ({len(stall_map)} frontiers in 2-wave valley — 11% resolve) ---")
        for fid, dom in sorted(stall_map.items())[:8]:
            lines.append(f"  \u26a0 {fid} ({dom}) — needs hardening lane (mode shift required)")
        lines.append("  Fix: open DOMEX-<DOM>-S<N> with --mode hardening for any of the above")
        lines.append("")
    return lines, stall_map


def section_stale_experiments(check_fn):
    """Stale domain experiments (L-246)."""
    lines = []
    stale_experiments = check_fn()
    if stale_experiments:
        lines.append(f"--- Unrun domain experiments ({len(stale_experiments)}) ---")
        for e in stale_experiments[:6]:
            lines.append(f"  \u25cb {e}")
        lines.append("")
    return lines


def section_experiment_harvest_gap(check_fn):
    """Experiment harvest gap (F-IS7, L-578)."""
    lines = []
    try:
        harvest_gaps = check_fn(threshold=5)
        if harvest_gaps:
            lines.append(f"--- Experiment harvest gap ({len(harvest_gaps)} domains: \u22655 experiments, 0 lessons) ---")
            for domain, count in harvest_gaps[:6]:
                lines.append(f"  \U0001f4e6 {domain} ({count} experiments) — no lessons extracted yet")
            lines.append("")
    except Exception:
        pass
    return lines


def section_stale_baselines(session_num, check_fn):
    """Stale hardcoded baselines in tools (FM-20, L-820)."""
    lines = []
    try:
        stale = check_fn(session_num)
        if stale:
            lines.append(f"--- Stale baselines ({len(stale)} hardcoded session values >50s behind) ---")
            for s in stale[:5]:
                lines.append(f"  ! {s['file']}:{s['line']} = {s['value']} ({s['age']}s stale, {s['pattern']})")
            lines.append("")
    except Exception:
        pass
    return lines


def section_underused_tools(check_fn, log_text):
    """Underused core tools."""
    lines = []
    underused_tools, latest_sid, start_sid = check_fn(log_text)
    if underused_tools:
        window = "recent sessions"
        if latest_sid is not None and start_sid is not None:
            window = f"S{start_sid}..S{latest_sid}"
        lines.append(f"--- Underused core tools ({len(underused_tools)} in {window}) ---")
        for tool in underused_tools[:6]:
            lines.append(f"  \u25cb {tool}")
        lines.append("")
    return lines


def section_cascade_state(maint_output: str = None):
    """Cross-layer cascade monitor (F-FLT4, L-1018, P-303). Only shown when layers failing."""
    lines = []
    try:
        import sys
        from pathlib import Path
        from concurrent.futures import ThreadPoolExecutor
        sys.path.insert(0, str(Path(__file__).parent))
        from cascade_monitor import (
            check_tool_layer, check_quality_layer, check_knowledge_layer,
            check_evaluation_layer, check_attention_layer, detect_cascades,
        )
        # Parallelize independent layer checks (Q=8.5s, E=5s dominate when sequential)
        # Pass maint_output to Q layer to avoid redundant maintenance.py subprocess call
        with ThreadPoolExecutor(max_workers=5) as pool:
            futures = {
                "T": pool.submit(check_tool_layer),
                "Q": pool.submit(check_quality_layer, maint_output),
                "K": pool.submit(check_knowledge_layer),
                "E": pool.submit(check_evaluation_layer),
                "A": pool.submit(check_attention_layer),
            }
        layers = {k: v.result() for k, v in futures.items()}
        failing = [k for k, v in layers.items() if v.get("failing")]
        cascades = detect_cascades(layers)
        if cascades:
            lines.append(f"--- CASCADE ALERT ({len(cascades)} active cascades) ---")
            for c in cascades:
                lines.append(f"  ! {c['layers']} (severity={c['severity']})")
            lines.append("")
        elif failing:
            failing_str = ", ".join(f"{k}:{layers[k].get('evidence','')}" for k in failing)
            lines.append(f"  NOTICE: cascade layers failing (no cascade yet): {failing_str}")
    except Exception:
        pass
    return lines


def section_recent_commits(recent_commits):
    """Recent commits for collision avoidance (L-251)."""
    lines = []
    if recent_commits:
        lines.append("--- Recent commits (avoid repeating) ---")
        for c in recent_commits:
            lines.append(f"  \u2713 {c[:100]}")
        lines.append("")
    return lines


def section_session_log_tail(log_text, brief):
    """Session log tail (behavioral pattern)."""
    lines = []
    if not brief and log_text:
        from orient_state import extract_session_log_tail
        tail = extract_session_log_tail(log_text)
        if tail:
            lines.append("--- Recent sessions (behavioral pattern) ---")
            for entry in tail:
                lines.append(f"  {entry[:120]}")
            lines.append("")
    return lines


def section_agent_positions():
    """Agent positions (S340 council)."""
    lines = []
    try:
        from agent_state import get_position_summary
        positions = get_position_summary()
        if positions:
            lines.append(f"--- Active agents ({len(positions)}) ---")
            for p in positions:
                lines.append(f"  {p['session']} \u2192 {p['domain']} ({p.get('lane', '?')})")
            domains = [p["domain"] for p in positions]
            dupes = [d for d in set(domains) if domains.count(d) > 1]
            if dupes:
                lines.append(f"  \u26a0 COLLISION: multiple agents on: {', '.join(dupes)}")
            lines.append("")
    except Exception:
        pass
    return lines


def section_concurrent_activity(root=ROOT):
    """Active sessions, task claims, and concurrency-level recommendation (L-686, L-526)."""
    lines = []
    try:
        sys.path.insert(0, str(root / "tools"))
        from claim import get_active_sessions, get_active_task_claims
        sessions = get_active_sessions()
        task_claims = get_active_task_claims()
        n = len(sessions)
        if not sessions and not task_claims:
            return lines
        level, icon = (("EXTREME", "\U0001f534") if n >= 5 else ("HIGH", "\U0001f7e0") if n >= 3 else ("MODERATE", "\U0001f7e1") if n >= 1 else ("LOW", "\U0001f7e2"))
        lines.append(f"--- Concurrent activity ({n} sessions, {icon} {level}) ---")
        for s in sessions[:5]:
            label = s.get("current_task", "(idle)") + (f": {s['description'][:40]}" if s.get("description") else "")
            lines.append(f"  {s['session']:15s} {s['age_s']:4d}s ago  {label}")
        if task_claims:
            lines.append(f"  Task claims: {', '.join(task_claims.keys())}")
        if n >= 5:
            lines.append(f"  \u26a0 EXTREME concurrency (N={n}): commit-by-proxy likely (L-526). Recommend: verification/historian mode. Re-check git log before EACH task.")
        elif n >= 3:
            lines.append(f"  \u26a0 HIGH concurrency (N={n}): planned tasks may be pre-empted (L-526). Recommend: verification/historian/meta-reflection. Re-check git log --oneline -3 before each task.")
        lines.append("")
    except Exception:
        pass
    return lines


def section_historian_repair(root=ROOT):
    """Historian repair — SIG-39."""
    lines = []
    hr_data = _run_tool_json("historian_repair", ["--json"], root=root)
    if hr_data:
        high_items = [i for i in hr_data.get("items", []) if i.get("severity") == "HIGH"]
        if high_items:
            cat_icons = {"beliefs": "\U0001f534", "frontiers": "\U0001f7e1", "domains": "\u26aa"}
            lines.append(f"--- Historian repair ({hr_data.get('total', 0)} stale, {len(high_items)} HIGH) ---")
            for item in high_items[:3]:
                lines.append(f"  {cat_icons.get(item.get('category',''),chr(0x25cb))} [{item['item_id']}] {item['category']} — stale {item['sessions_stale']}s — {item['description'][:60]}")
            if len(high_items) > 3:
                lines.append(f"  ... and {len(high_items) - 3} more HIGH items")
            lines.append("  Run: python3 tools/historian_repair.py")
            lines.append("")
    return lines


def section_meta_tooler(root=ROOT):
    """Meta-tooler scan — SIG-39."""
    lines = []
    mt = _run_tool_json("meta_tooler", ["--json"], timeout=30, root=root)
    if mt and (mt.get("high", 0) > 0 or mt.get("medium", 0) > 5):
        lines.append(f"--- Meta-tooler ({mt['total_tools']} tools, HIGH={mt['high']} MEDIUM={mt['medium']}) ---")
        for f in mt.get("findings", []):
            if f["severity"] == "HIGH":
                lines.append(f"  \U0001f534 [{f['category']}] {f['tool']}: {f['message']}")
        lines.append("  Run: python3 tools/meta_tooler.py")
        lines.append("")
    return lines


def _item_resolved_by_actual(canon: str, actual_texts: list[str]) -> bool:
    """Check if a canonical next-item was addressed in any actual: field.

    Uses keyword overlap: if >=2 significant tokens from the canonical item
    appear in any actual text, consider it resolved.
    """
    stop_words = {"the", "a", "an", "in", "on", "at", "to", "for", "of", "is",
                  "and", "or", "with", "from", "by", "as", "its", "it", "be",
                  "was", "were", "has", "had", "not", "no", "but", "if", "so",
                  "that", "this", "than", "more", "very", "just", "also", "all",
                  "each", "per", "any", "s", "yet", "re", "vs"}
    # Extract significant tokens (letters/digits, >=3 chars, not stop words)
    # Split word-compound hyphens (claim-vs-evidence → claim, evidence)
    # but keep identifiers intact (FM-30, ISO-7 stay as-is)
    import re as _re
    raw_tokens = _re.findall(r'[A-Za-z0-9_-]{3,}', canon)
    tokens: set[str] = set()
    for t in raw_tokens:
        # Only split if all hyphen-parts are alphabetic words (not IDs like FM-30)
        parts = t.split('-')
        if len(parts) > 1 and all(p.isalpha() and len(p) >= 2 for p in parts):
            tokens.update(p.lower() for p in parts if len(p) >= 3)
        else:
            tokens.add(t.lower())
    tokens -= stop_words
    if len(tokens) < 2:
        return False  # too few tokens to match reliably
    for actual in actual_texts:
        actual_lower = actual.lower()
        matches = sum(1 for t in tokens if t in actual_lower)
        if matches >= 2 and matches >= len(tokens) * 0.4:
            return True
    return False


def section_zombie_carryover(root=ROOT):
    """Zombie items + carried-over% from NEXT.md session trails (L-978 TG-2/TG-4)."""
    lines = []
    try:
        sys.path.insert(0, str(root / "tools"))
        from trails_generalizer import parse_session_notes, canonicalize
        from collections import Counter
        next_path = root / "tasks" / "NEXT.md"
        if not next_path.exists():
            return lines
        notes = parse_session_notes(next_path.read_text(encoding="utf-8"))
        if len(notes) < 2:
            return lines
        actual_texts = [n.get("actual_text", "") for n in notes if n.get("actual_text")]
        item_counter = Counter()
        for note in notes:
            seen: set[str] = set()
            for item in note["next_items"]:
                c = canonicalize(item)
                if c not in seen:
                    item_counter[c] += 1; seen.add(c)
        # Exclusion: dropped zombies + resolved by actual: fields
        dropped: set[str] = set()
        try:
            dp = root / "tools" / "zombie_drops.json"
            if dp.exists():
                dropped = {e.get("canonical", "") for e in json.loads(dp.read_text()).get("drops", []) if e.get("canonical")}
        except Exception:
            pass
        resolved = {c for c in item_counter if _item_resolved_by_actual(c, actual_texts)}
        excluded = dropped | resolved
        zombies = [(it, cnt) for it, cnt in item_counter.most_common() if cnt >= 5 and it not in excluded]
        # Carried-over% for latest session (TG-4)
        prior_items = {canonicalize(it) for n in notes[-6:-1] for it in n["next_items"]}
        latest_items = [canonicalize(it) for it in notes[-1]["next_items"] if canonicalize(it) not in excluded]
        carried = sum(1 for it in latest_items if it in prior_items) if latest_items else 0
        pct = (carried / len(latest_items) * 100) if latest_items else 0.0
        if zombies or pct >= 30:
            lines.append("--- Zombie Items (L-978 TG-2/TG-4) ---")
            warn = " — target <30%" if pct >= 30 else ""
            lines.append(f"  {'⚠ ' if pct >= 30 else ''}Carried-over: {pct:.0f}% ({carried}/{len(latest_items)}){warn}")
            if zombies:
                lines.append(f"  Zombies ({len(zombies)} items recurring 5+ sessions):")
                for item, count in zombies[:5]:
                    lines.append(f"    \U0001f480 {count:3d}x  {item[:60]}")
            if resolved:
                lines.append(f"  Resolved by actual: {len(resolved)} item(s) excluded")
            lines.append("")
    except Exception:
        pass
    return lines


def section_closure_metric(root=ROOT):
    """Trail-provenance closure metric (L-1118, L-1125)."""
    lines = []
    try:
        import glob as _glob_closure
        lesson_files = sorted(_glob_closure.glob(str(root / "memory" / "lessons" / "L-*.md")))
        if len(lesson_files) < 20:
            return lines
        recent = lesson_files[-20:]
        external_markers = ["arxiv", "doi:", "http://", "https://", "10.", "et al"]
        ext_count = 0
        for lf in recent:
            try:
                txt = Path(lf).read_text(encoding="utf-8")
                cites_match = re.search(r"^\*{0,2}Cites\*{0,2}:\s*(.+)", txt, re.MULTILINE)  # L-1169
                if not cites_match:
                    continue
                cites_line = cites_match.group(1).lower()
                if any(m in cites_line for m in external_markers):
                    ext_count += 1
            except Exception:
                pass
        ext_pct = ext_count / len(recent) * 100
        if ext_pct < 20:
            lines.append("--- External Closure (L-1118, L-1125) ---")
            lines.append(f"  \u26a0 Trail provenance: {ext_pct:.0f}% external ({ext_count}/{len(recent)} recent Cites: headers)")
            lines.append("  Cites: headers reference only internal artifacts.")
            lines.append("  L-1125: trail provenance is cheapest break point.")
            lines.append("")
    except Exception:
        pass
    return lines


def section_knowledge_swarm(root=ROOT):
    """Knowledge self-organization (SIG-62, L-1121, S457): revive/compress/crosslink/orphan."""
    lines = []
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from knowledge_swarm import (
            parse_lesson_meta, build_citation_maps, classify_items,
            revive_candidates, compress_candidates, crosslink_suggestions,
            detect_orphaned_principles, section_output,
        )
        from swarm_io import session_number, lesson_paths
        current = session_number()
        lessons = {}
        for path in lesson_paths():
            meta = parse_lesson_meta(path)
            if meta:
                lessons[meta["id"]] = meta
        if len(lessons) < 100:
            return lines
        outbound, inbound = build_citation_maps(lessons)
        states = classify_items(lessons, inbound, current)
        results = {
            "revival": revive_candidates(lessons, states, inbound, current),
            "compress": compress_candidates(lessons, states, inbound, current),
            "crosslinks": crosslink_suggestions(lessons, states, inbound, outbound),
            "orphaned_principles": detect_orphaned_principles(lessons, states),
        }
        lines = section_output(results, current)
    except Exception:
        pass
    return lines


def section_correction_propagation(root=ROOT):
    """Correction propagation gaps (L-1132, L-1097, F-IC1)."""
    lines = []
    try:
        sys.path.insert(0, str(Path(__file__).parent))
        from correction_propagation import run_analysis
        from swarm_io import session_number
        result = run_analysis(session=session_number(), classify=True)
        total = result.get("total_uncorrected_citations", 0)
        rate = result.get("avg_correction_rate", 1.0)
        queue = result.get("correction_queue", [])
        high = [q for q in queue if q.get("priority") == "HIGH"]
        if high:
            lines.append("")
            lines.append("--- Correction Propagation (L-1132) ---")
            lines.append(f"  {total} uncorrected citations | {len(high)} HIGH priority | correction rate {rate:.0%}")
            for item in high[:5]:
                lines.append(f"  -> {item['citer']} cites falsified {item['needs_correction_about']} (content-dependent)")
            lines.append("  Run: python3 tools/correction_propagation.py")
    except Exception:
        pass
    return lines


def section_knowledge_recombination(root=ROOT):
    """Knowledge recombination candidates (SIG-62, knowledge_recombine.py).

    Lesson pairs with shared citations but no direct link — semantic gaps
    where new knowledge can be synthesized. Reads cached JSON artifact.
    """
    lines = []
    try:
        kr_dir = root / "experiments" / "meta"
        kr_files = sorted(kr_dir.glob("knowledge-recombine-s*.json"))
        if not kr_files:
            return lines
        data = json.loads(kr_files[-1].read_text(encoding="utf-8"))
        candidates = data.get("top", [])
        cross = [
            c for c in candidates
            if c.get("cross_domain") and c.get("score", 0) >= 40
        ]
        if not cross:
            return lines
        lines.append("--- Knowledge Recombination (SIG-62) ---")
        lines.append(
            f"  {data.get('total_candidates', '?')} candidate pairs"
            f" ({data.get('cross_domain_candidates', '?')} cross-domain)"
        )
        for i, c in enumerate(cross[:3], 1):
            ta = c.get("title_a", "")[:55]
            tb = c.get("title_b", "")[:55]
            shared = ", ".join(c.get("shared_refs", [])[:4])
            lines.append(
                f"  [{i}] {c['parent_a']} x {c['parent_b']}"
                f" (score={c['score']})"
            )
            lines.append(f"      {ta}")
            lines.append(f"      x {tb}")
            lines.append(f"      Shared: {shared}")
        lines.append(
            "  Refresh: python3 tools/knowledge_recombine.py --json"
            " > experiments/meta/knowledge-recombine-s<N>.json"
        )
        lines.append("")
    except Exception:
        pass
    return lines


def _active_domex_domains(root=ROOT):
    """Return set of domains with active DOMEX lanes (L-1169: concurrency check)."""
    lanes_path = root / "tasks" / "SWARM-LANES.md"
    active = set()
    if not lanes_path.exists():
        return active
    for line in lanes_path.read_text().splitlines():
        if "DOMEX-" not in line:
            continue
        # Active statuses are not MERGED/ABANDONED
        if "| MERGED |" in line or "| ABANDONED |" in line:
            continue
        # Extract domain from lane ID: DOMEX-<DOMAIN>-S<N>
        m = re.search(r"DOMEX-([A-Z]+)-S\d+", line)
        if m:
            active.add(m.group(1).lower())
    return active


def section_epsilon_dispatch(session_num, root=ROOT):
    """ε-dispatch diversity recommendation (F-RAND1, L-601 structural enforcement).

    With probability ε=0.15, recommends a random non-top domain to break UCB1
    rich-get-richer lock. Surfaced in orient so sessions see it (L-1138: naming > ranking).
    L-1169: checks active DOMEX lanes to avoid recommending already-claimed domains.
    """
    import random as _random
    lines = []
    epsilon = 0.15
    if session_num <= 0:
        return lines
    rng = _random.Random(session_num)
    roll = rng.random()
    if roll >= epsilon:
        return lines
    try:
        result = subprocess.run(
            [sys.executable, str(root / "tools" / "dispatch_optimizer.py"), "--json", "--all"],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode != 0 or not result.stdout.strip():
            return lines
        data = json.loads(result.stdout)
        if len(data) < 2:
            return lines
        top_domain = data[0].get("domain", "unknown")
        active_domains = _active_domex_domains(root)
        # Filter out domains with active DOMEX lanes (L-1169)
        candidates = [d for i, d in enumerate(data) if i > 0
                      and d.get("domain", "").lower() not in active_domains]
        if not candidates:
            lines.append("--- \u26a1 \u03b5-dispatch fired but all candidates have active lanes ---")
            lines.append(f"  {len(active_domains)} domains claimed. Skipping diversity override.")
            lines.append("")
            return lines
        rand_idx = rng.randint(0, len(candidates) - 1)
        pick = candidates[rand_idx]
        pick_domain = pick.get("domain", "unknown")
        pick_frontier = pick.get("first_frontier", "")
        lines.append("--- \u26a1 \u03b5-dispatch fired (F-RAND1, L-601) ---")
        lines.append(f"  Diversity override: work on **{pick_domain}** instead of {top_domain}")
        if pick_frontier:
            lines.append(f"  Target frontier: {pick_frontier}")
        lines.append(f"  \u03b5-roll {roll:.3f} < {epsilon} \u2014 breaking UCB1 concentration (Gini 0.506)")
        if active_domains:
            lines.append(f"  ({len(active_domains)} domains filtered: active DOMEX lanes)")
        lines.append(f"  Open a DOMEX lane for {pick_domain}.")
        lines.append("")
    except Exception:
        pass
    return lines


def section_suggested_action(maint_out, open_signals, stall_map, priorities):
    """Suggested next action (concurrency-aware via L-526)."""
    lines = ["--- Suggested next action ---"]
    # Check concurrency level to adjust recommendations
    try:
        from claim import get_active_sessions
        n_concurrent = len(get_active_sessions())
    except Exception:
        n_concurrent = 0
    if n_concurrent >= 3:
        lines.append(f"  \u26a0 N={n_concurrent} concurrent: prefer verification/historian/novel work")
    if "URGENT" in maint_out:
        urgent_lines = [l.strip() for l in maint_out.splitlines() if "URGENT" in l]
        for l in urgent_lines[:2]:
            lines.append(f"  URGENT: {l}")
    elif "[DUE]" in maint_out:
        due_lines = [l.strip() for l in maint_out.splitlines() if l.strip().startswith("!")]
        for l in due_lines[:2]:
            lines.append(f"  DUE: {l.lstrip('! ')}")
    elif open_signals and any(s["priority"] == "P1" and s.get("age", 0) > 30 for s in open_signals):
        stale_p1 = [s for s in open_signals if s["priority"] == "P1" and s.get("age", 0) > 30]
        for s in stale_p1[:2]:
            lines.append(f"  SIGNAL-DUE: {s['id']} ({s['age']}s old, P1): {s['content'][:70]}")
        lines.append(f"  Resolve: `python3 tools/swarm_signal.py resolve {stale_p1[0]['id']} \"<resolution>\"`")
    elif "[PERIODIC]" in maint_out:
        periodic_lines = [l.strip() for l in maint_out.splitlines() if l.strip().startswith("~")]
        for l in periodic_lines[:2]:
            lines.append(f"  PERIODIC: {l.lstrip('~ ')}")
    elif stall_map:
        top_fid, top_dom = next(iter(sorted(stall_map.items())))
        lines.append(f"  STALL: {top_fid} ({top_dom}) in 2-wave valley — open hardening lane to escape (11%\u219231%)")
        if len(stall_map) > 1:
            lines.append(f"  ({len(stall_map)} total stalled: {', '.join(sorted(stall_map)[:5])})")
    elif priorities:
        lines.append(f"  {priorities[0]}")
    else:
        lines.append("  State clean — pick a frontier or run a periodic")
    return lines

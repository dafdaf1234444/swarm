#!/usr/bin/env python3
"""f_ops2_domain_priority.py - prioritize domain work and allocate agent slots.

This tool operationalizes F-OPS2 by turning current swarm state into a
domain-priority schedule that can be swarmed directly.

Inputs:
- domain frontier files (active frontier load + recency)
- tasks/NEXT.md ("For next session" + "What just happened" finding signal)
- tasks/SWARM-LANES.md (active lane pressure / collision risk)

Output:
- policy-by-policy ranking and slot allocation
- recommended policy and per-slot domain plan

Usage:
  python3 tools/f_ops2_domain_priority.py
  python3 tools/f_ops2_domain_priority.py --agent-count 4 --json-out experiments/operations-research/f-ops2-domain-priority-s186.json
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
ACTIVE_LANE_STATUSES = {"CLAIMED", "ACTIVE", "BLOCKED", "READY"}
POLICIES = ("fifo", "risk_first", "value_density", "hybrid")


@dataclass
class DomainState:
    name: str
    frontier_path: str
    active_frontiers: list[str]
    updated_session: int
    age_sessions: int
    next_mentions: int = 0
    next_priority_weight: float = 0.0
    finding_mentions: int = 0
    finding_priority_weight: float = 0.0
    active_lane_pressure: int = 0

    def to_json(self) -> dict:
        return {
            "domain": self.name,
            "frontier_path": self.frontier_path,
            "active_frontier_count": len(self.active_frontiers),
            "active_frontiers": self.active_frontiers,
            "updated_session": self.updated_session,
            "age_sessions": self.age_sessions,
            "next_mentions": self.next_mentions,
            "next_priority_weight": round(self.next_priority_weight, 3),
            "finding_mentions": self.finding_mentions,
            "finding_priority_weight": round(self.finding_priority_weight, 3),
            "active_lane_pressure": self.active_lane_pressure,
        }


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""


def _last_session(text: str) -> int:
    sessions = [int(x) for x in re.findall(r"\bS(\d+)\b", text or "")]
    return max(sessions) if sessions else 0


def _updated_session_from_state_header(text: str) -> int:
    m = re.search(r"^Updated:\s*[0-9]{4}-[0-9]{2}-[0-9]{2}\s+S(\d+)\b", text or "", re.MULTILINE)
    return int(m.group(1)) if m else 0


def _display_path(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT)).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def parse_active_frontiers(frontier_text: str) -> list[str]:
    active_match = re.search(r"## Active(.*?)(?:\n## |\Z)", frontier_text, re.DOTALL)
    if not active_match:
        return []
    active_block = active_match.group(1)
    ordered_unique: list[str] = []
    for line in active_block.splitlines():
        bullet_bold = re.match(r"^\s*[-*]\s+(~~)?\*\*(F-[A-Z0-9]+)\*\*(?:~~)?", line)
        bullet_plain = re.match(r"^\s*[-*]\s+(~~)?(F-[A-Z0-9]+)(?:~~)?\b", line)
        table_row = re.match(r"^\s*\|\s*(~~)?(F-[A-Z0-9]+)(?:~~)?\s*\|", line)
        m = bullet_bold or bullet_plain or table_row
        if not m:
            continue
        if m.group(1):
            # Ignore struck-through IDs inside the Active section.
            continue
        fid = m.group(2)
        if fid not in ordered_unique:
            ordered_unique.append(fid)
    return ordered_unique


def parse_updated_session(frontier_text: str) -> int:
    match = re.search(r"Updated:\s*[0-9]{4}-[0-9]{2}-[0-9]{2}\s*S(\d+)", frontier_text)
    return int(match.group(1)) if match else 0


def load_domain_frontiers(domains_root: Path, current_session: int) -> tuple[list[DomainState], dict[str, str]]:
    states: list[DomainState] = []
    frontier_to_domain: dict[str, str] = {}

    for domain_dir in sorted(domains_root.iterdir(), key=lambda p: p.name):
        if not domain_dir.is_dir():
            continue
        frontier_path = domain_dir / "tasks" / "FRONTIER.md"
        if not frontier_path.exists():
            continue

        text = _read(frontier_path)
        active = parse_active_frontiers(text)
        updated = parse_updated_session(text)
        age = max(0, current_session - updated) if current_session > 0 and updated > 0 else 0
        for fid in active:
            frontier_to_domain[fid] = domain_dir.name

        states.append(
            DomainState(
                name=domain_dir.name,
                frontier_path=_display_path(frontier_path),
                active_frontiers=active,
                updated_session=updated,
                age_sessions=age,
                next_mentions=0,
                next_priority_weight=0.0,
                finding_mentions=0,
                finding_priority_weight=0.0,
                active_lane_pressure=0,
            )
        )

    return states, frontier_to_domain


def parse_next_demand(next_text: str, frontier_to_domain: dict[str, str]) -> tuple[dict[str, int], dict[str, float]]:
    mentions: dict[str, int] = {}
    weights: dict[str, float] = {}

    section = re.search(r"## For next session(.*?)(?:\n## |\Z)", next_text, re.DOTALL)
    if not section:
        return mentions, weights

    lines = section.group(1).splitlines()
    rank = 0
    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        numbered = re.match(r"^(\d+)\.\s+(.*)$", line)
        if not numbered:
            continue
        rank += 1
        body = numbered.group(2)
        ids = set(re.findall(r"\bF-[A-Z0-9]+\b", body))
        priority_weight = max(1.0, 5.0 - rank)
        for fid in ids:
            domain = frontier_to_domain.get(fid)
            if domain is None:
                continue
            mentions[domain] = mentions.get(domain, 0) + 1
            weights[domain] = weights.get(domain, 0.0) + priority_weight

    return mentions, weights


def parse_findings_demand(
    next_text: str,
    frontier_to_domain: dict[str, str],
    *,
    max_lines: int = 20,
) -> tuple[dict[str, int], dict[str, float]]:
    mentions: dict[str, int] = {}
    weights: dict[str, float] = {}

    section = re.search(r"## What just happened(.*?)(?:\n## |\Z)", next_text, re.DOTALL)
    if not section:
        return mentions, weights

    line_count = 0
    for raw in section.group(1).splitlines():
        line = raw.strip()
        if not line:
            continue
        if not re.match(r"^S\d+:", line):
            continue
        line_count += 1
        if line_count > max_lines:
            break

        ids = set(re.findall(r"\bF-[A-Z0-9]+\b", line))
        if not ids:
            continue

        # Newer lines in "What just happened" are higher in the section.
        recency_weight = max(0.5, 5.0 - 0.2 * (line_count - 1))
        low = line.lower()
        urgency_boost = 0.0
        if any(k in low for k in ("open", "next step", "caveat", "unstable", "pending", "deferred", "blocked")):
            urgency_boost += 0.75
        if any(k in low for k in ("resolved", "closed", "superseded")):
            urgency_boost -= 0.25
        line_weight = max(0.2, recency_weight + urgency_boost)

        for fid in ids:
            domain = frontier_to_domain.get(fid)
            if domain is None:
                continue
            mentions[domain] = mentions.get(domain, 0) + 1
            weights[domain] = weights.get(domain, 0.0) + line_weight

    return mentions, weights


def _parse_lane_rows(lanes_text: str) -> list[dict[str, str]]:
    keys = ("date", "lane", "session", "agent", "branch", "pr", "model", "platform", "scope", "etc", "status", "notes")
    rows: list[dict[str, str]] = []
    for raw in lanes_text.splitlines():
        line = raw.strip()
        if not line.startswith("|") or re.match(r"^\|\s*(Date\s*\||[-: ]+\|)", line, re.IGNORECASE):
            continue
        parts = [part.strip() for part in line.strip("|").split("|")]
        if len(parts) < 12:
            continue
        row = dict(zip(keys, parts))
        row["status"] = row["status"].upper()
        rows.append(row)
    return rows


def parse_active_lane_pressure(lanes_text: str, frontier_to_domain: dict[str, str]) -> dict[str, int]:
    latest_by_lane: dict[str, dict[str, str]] = {}
    for row in _parse_lane_rows(lanes_text):
        lane = row.get("lane", "")
        if lane:
            latest_by_lane[lane] = row

    pressure: dict[str, int] = {}
    for row in latest_by_lane.values():
        if row.get("status", "") not in ACTIVE_LANE_STATUSES:
            continue
        scope = row.get("scope", "")
        etc = row.get("etc", "")

        domain = None
        m_scope = re.search(r"domains/([^/\s]+)/", scope)
        if m_scope:
            domain = m_scope.group(1)
        if domain is None:
            m_fid = re.search(r"frontier=(F-[A-Z0-9]+)", etc)
            if m_fid:
                domain = frontier_to_domain.get(m_fid.group(1))
        if domain is None:
            continue
        pressure[domain] = pressure.get(domain, 0) + 1

    return pressure


def policy_score(policy: str, state: DomainState) -> float:
    if policy == "fifo":
        # Oldest queue items first; slight tie-break by unresolved load.
        return float(state.age_sessions) + 0.1 * len(state.active_frontiers)
    if policy == "risk_first":
        # Risk = unresolved pressure + aging + explicit near-term demand + fresh finding pressure.
        return (
            2.0 * len(state.active_frontiers)
            + state.age_sessions
            + state.next_mentions
            + 1.25 * state.finding_mentions
            - state.active_lane_pressure
        )
    if policy == "value_density":
        # Value per expected coordination unit.
        value = 3.0 * state.next_priority_weight + 2.0 * state.finding_priority_weight + len(state.active_frontiers)
        return value / (1.0 + state.active_lane_pressure)
    if policy == "hybrid":
        # Balanced policy: demand + findings + load + freshness normalized by lane pressure.
        value = (
            2.0 * state.next_priority_weight
            + 1.5 * state.finding_priority_weight
            + len(state.active_frontiers)
            + 0.5 * state.age_sessions
        )
        return value / (1.0 + 0.5 * state.active_lane_pressure)
    raise ValueError(f"Unknown policy: {policy}")


def allocate_agents(states: list[DomainState], policy: str, agent_count: int) -> dict[str, int]:
    allocations = {s.name: 0 for s in states}
    base_scores = {s.name: max(0.0, policy_score(policy, s)) for s in states}

    if agent_count <= 0:
        return allocations

    for _ in range(agent_count):
        best_domain = None
        best_marginal = -1.0
        for s in sorted(states, key=lambda item: item.name):
            score = base_scores[s.name]
            marginal = score / (1.0 + allocations[s.name])
            if marginal > best_marginal:
                best_marginal = marginal
                best_domain = s.name
        if best_domain is None:
            break
        allocations[best_domain] += 1

    return allocations


def evaluate_policy(states: list[DomainState], allocations: dict[str, int]) -> dict[str, float]:
    by_name = {s.name: s for s in states}
    projected_gain = 0.0
    collision_risk = 0.0
    for domain, slots in allocations.items():
        st = by_name[domain]
        value_proxy = (
            3.0 * st.next_priority_weight
            + 2.0 * st.finding_priority_weight
            + len(st.active_frontiers)
            + 0.5 * st.age_sessions
        )
        projected_gain += slots * value_proxy
        collision_risk += max(0, slots - 1) * (1.0 + st.active_lane_pressure)
    net = projected_gain - 1.5 * collision_risk
    return {
        "projected_gain": round(projected_gain, 4),
        "collision_risk": round(collision_risk, 4),
        "net_score": round(net, 4),
    }


def build_slot_plan(states: list[DomainState], allocations: dict[str, int], policy: str) -> list[dict]:
    by_name = {s.name: s for s in states}
    slots: list[dict] = []
    slot_number = 0
    ranked = sorted(
        allocations.keys(),
        key=lambda name: (allocations[name], policy_score(policy, by_name[name]), name),
        reverse=True,
    )
    for domain in ranked:
        count = allocations[domain]
        if count <= 0:
            continue
        st = by_name[domain]
        for k in range(count):
            slot_number += 1
            slots.append(
                {
                    "slot": slot_number,
                    "domain": domain,
                    "lane_focus": st.frontier_path,
                    "reason": (
                        f"score={policy_score(policy, st):.3f}; "
                        f"next_weight={st.next_priority_weight:.1f}; "
                        f"finding_weight={st.finding_priority_weight:.1f}; "
                        f"active_frontiers={len(st.active_frontiers)}; "
                        f"lane_pressure={st.active_lane_pressure}; "
                        f"allocation_index={k + 1}/{count}"
                    ),
                }
            )
    return slots


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent-count", type=int, default=4, help="Total agent slots to allocate.")
    parser.add_argument(
        "--policy",
        choices=("all",) + POLICIES,
        default="all",
        help="Evaluate one policy or all policies.",
    )
    parser.add_argument("--next-path", type=Path, default=Path("tasks/NEXT.md"))
    parser.add_argument("--lanes-path", type=Path, default=Path("tasks/SWARM-LANES.md"))
    parser.add_argument("--domains-root", type=Path, default=Path("domains"))
    parser.add_argument(
        "--findings-window",
        type=int,
        default=20,
        help="How many recent 'What just happened' lines to scan for finding pressure.",
    )
    parser.add_argument("--json-out", type=Path, default=None)
    return parser.parse_args()


def main() -> int:
    args = parse_args()

    next_path = args.next_path if args.next_path.is_absolute() else REPO_ROOT / args.next_path
    lanes_path = args.lanes_path if args.lanes_path.is_absolute() else REPO_ROOT / args.lanes_path
    domains_root = args.domains_root if args.domains_root.is_absolute() else REPO_ROOT / args.domains_root

    next_text = _read(next_path)
    current_session = _updated_session_from_state_header(next_text)
    if current_session <= 0:
        current_session = _last_session(next_text)
    if current_session <= 0:
        current_session = _last_session(_read(REPO_ROOT / "memory/SESSION-LOG.md"))

    states, frontier_to_domain = load_domain_frontiers(domains_root, current_session)
    mention_counts, mention_weights = parse_next_demand(next_text, frontier_to_domain)
    finding_counts, finding_weights = parse_findings_demand(
        next_text,
        frontier_to_domain,
        max_lines=max(1, args.findings_window),
    )
    lane_pressure = parse_active_lane_pressure(_read(lanes_path), frontier_to_domain)

    for st in states:
        st.next_mentions = mention_counts.get(st.name, 0)
        st.next_priority_weight = mention_weights.get(st.name, 0.0)
        st.finding_mentions = finding_counts.get(st.name, 0)
        st.finding_priority_weight = finding_weights.get(st.name, 0.0)
        st.active_lane_pressure = lane_pressure.get(st.name, 0)

    selected_policies = list(POLICIES) if args.policy == "all" else [args.policy]
    policy_payload: dict[str, dict] = {}
    for policy in selected_policies:
        scores = {s.name: round(policy_score(policy, s), 6) for s in states}
        ranked = [name for name, _ in sorted(scores.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)]
        allocations = allocate_agents(states, policy, args.agent_count)
        metrics = evaluate_policy(states, allocations)
        policy_payload[policy] = {
            "scores": scores,
            "ranked_domains": ranked,
            "allocations": allocations,
            "metrics": metrics,
        }

    recommended_policy = max(
        policy_payload.keys(),
        key=lambda p: (
            policy_payload[p]["metrics"]["net_score"],
            policy_payload[p]["metrics"]["projected_gain"],
            p == "hybrid",
        ),
    )
    recommended_alloc = policy_payload[recommended_policy]["allocations"]
    recommended_plan = build_slot_plan(states, recommended_alloc, recommended_policy)

    payload = {
        "session": current_session,
        "inputs": {
            "agent_count": args.agent_count,
            "policies_evaluated": selected_policies,
            "next_path": _display_path(next_path),
            "lanes_path": _display_path(lanes_path),
            "domains_root": _display_path(domains_root),
            "findings_window": args.findings_window,
        },
        "domain_signals": [s.to_json() for s in sorted(states, key=lambda x: x.name)],
        "policies": policy_payload,
        "recommended_policy": recommended_policy,
        "recommended_plan": recommended_plan,
    }

    if args.json_out is not None:
        out = args.json_out if args.json_out.is_absolute() else REPO_ROOT / args.json_out
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {out}")
    else:
        print(json.dumps(payload, indent=2))

    rec_metrics = payload["policies"][recommended_policy]["metrics"]
    print(
        "recommended_policy="
        f"{recommended_policy} net={rec_metrics['net_score']:.3f} "
        f"gain={rec_metrics['projected_gain']:.3f} risk={rec_metrics['collision_risk']:.3f}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

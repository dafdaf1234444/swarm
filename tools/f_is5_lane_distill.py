#!/usr/bin/env python3
"""F-IS5 lane distillation: two-pass swarm scoring over arXiv intake lanes."""

from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from random import Random


THEME_TARGETS: dict[str, tuple[str, ...]] = {
    "protocol-orchestration": ("F-IS4", "F-AI2", "F122"),
    "evaluation-scaling": ("F124", "F-FIN1", "P-197"),
    "memory-knowledge": ("F-IS3", "P-152", "F120"),
    "tool-use-execution": ("F111", "F120", "P-195"),
    "safety-reliability": ("F119", "PHIL-13", "F-AI2"),
    "misc": ("F122",),
}

ID_RE = re.compile(r"\b(?:F-[A-Z]+[0-9]+|P-[0-9]+|PHIL-[0-9]+|F[0-9]+)\b")


@dataclass(frozen=True)
class TransferDecision:
    target: str
    decision: str
    rationale: str


@dataclass(frozen=True)
class Claim:
    claim_id: str
    owner: str
    source_set: str
    lane_id: str
    paper_id: str
    theme: str
    claim_text: str
    transfer_decisions: tuple[TransferDecision, ...]


def _summary_snippet(summary: str, limit: int = 18) -> str:
    tokens = (summary or "").split()
    if not tokens:
        return "no summary available"
    joined = " ".join(tokens[:limit])
    return joined + ("..." if len(tokens) > limit else "")


def _is_cross_domain(target: str) -> bool:
    return not target.startswith("F-IS")


def _cross_domain_targets(
    transfer_decisions: tuple[TransferDecision, ...]
) -> tuple[str, ...]:
    return tuple(
        decision.target
        for decision in transfer_decisions
        if _is_cross_domain(decision.target)
    )


def load_active_targets(paths: list[Path]) -> set[str]:
    targets: set[str] = set()
    for path in paths:
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        for match in ID_RE.findall(text):
            targets.add(match)
    return targets


def make_transfer_decisions(
    *,
    owner: str,
    paper_id: str,
    targets: tuple[str, ...],
    seed: int,
    active_targets: set[str],
) -> tuple[TransferDecision, ...]:
    decisions: list[TransferDecision] = []
    for target in targets:
        if target not in active_targets:
            decisions.append(
                TransferDecision(
                    target=target,
                    decision="rejected",
                    rationale="target-not-active",
                )
            )
            continue

        # Deterministic per-owner vote so merge disagreements are explicit and reproducible.
        vote_rng = Random(f"{seed}:{owner}:{paper_id}:{target}")
        threshold = 0.52 if owner.endswith("A") else 0.48
        accepted = vote_rng.random() <= threshold
        decisions.append(
            TransferDecision(
                target=target,
                decision="accepted" if accepted else "rejected",
                rationale="owner-vote-pass" if accepted else "owner-vote-fail",
            )
        )
    return tuple(decisions)


def distill_pass(
    *,
    intake: dict,
    owner: str,
    source: str,
    seed: int,
    per_lane: int,
    active_targets: set[str],
) -> list[Claim]:
    source = (source or "selected").strip().lower()
    if source not in {"selected", "backlog"}:
        raise ValueError(f"Unsupported source set: {source}")

    rng = Random(seed)
    papers = {row["arxiv_id"]: row for row in intake.get("papers", [])}
    lanes = intake.get("lane_plan", [])
    claims: list[Claim] = []

    for lane in lanes:
        lane_id = lane.get("lane_id", "ARX-00")
        theme = lane.get("theme", "misc")
        if source == "backlog":
            paper_ids = list(lane.get("backlog_paper_ids", []))
        else:
            paper_ids = list(lane.get("paper_ids", []))
        if not paper_ids:
            continue
        rng.shuffle(paper_ids)
        selected = paper_ids[: max(1, per_lane)]

        targets = THEME_TARGETS.get(theme, THEME_TARGETS["misc"])
        if owner.endswith("A"):
            claim_targets = tuple(targets[:2])
            verb = "reports"
        else:
            claim_targets = tuple(targets[-2:])
            verb = "suggests"

        for paper_id in selected:
            paper = papers.get(paper_id, {})
            title = paper.get("title", paper_id)
            snippet = _summary_snippet(paper.get("summary_preview", ""))
            claim_text = (
                f"{paper_id} {verb} a {theme} signal via '{title}'. "
                f"Evidence preview: {snippet}"
            )
            transfer_decisions = make_transfer_decisions(
                owner=owner,
                paper_id=paper_id,
                targets=claim_targets,
                seed=seed,
                active_targets=active_targets,
            )
            claims.append(
                Claim(
                    claim_id=f"{owner}|{source}|{lane_id}|{paper_id}",
                    owner=owner,
                    source_set=source,
                    lane_id=lane_id,
                    paper_id=paper_id,
                    theme=theme,
                    claim_text=claim_text,
                    transfer_decisions=transfer_decisions,
                )
            )

    return claims


def summarize_claims(claims: list[Claim], active_targets: set[str]) -> dict:
    total_claims = len(claims)
    unique_claim_ids = {claim.claim_id for claim in claims}
    duplicate_claim_count = total_claims - len(unique_claim_ids)
    duplicate_claim_rate = (
        duplicate_claim_count / total_claims if total_claims else 0.0
    )

    transfer_candidates: set[tuple[str, str]] = set()
    for claim in claims:
        for decision in claim.transfer_decisions:
            if _is_cross_domain(decision.target):
                transfer_candidates.add((claim.paper_id, decision.target))

    by_key: dict[tuple[str, str], dict[str, object]] = defaultdict(
        lambda: {"owners": set(), "decisions": set(), "claim_ids": set()}
    )
    for claim in claims:
        for decision in claim.transfer_decisions:
            if not _is_cross_domain(decision.target):
                continue
            key = (claim.paper_id, decision.target)
            by_key[key]["owners"].add(claim.owner)
            by_key[key]["decisions"].add(decision.decision)
            by_key[key]["claim_ids"].add(claim.claim_id)

    accepted = {
        key
        for key, value in by_key.items()
        if len(value["owners"]) >= 2
        and value["decisions"] == {"accepted"}
        and key[1] in active_targets
    }
    collisions = {
        key
        for key, value in by_key.items()
        if len(value["owners"]) >= 2
        and value["decisions"] == {"accepted", "rejected"}
    }
    contested = {key for key, value in by_key.items() if len(value["owners"]) >= 2}

    transfer_acceptance_rate = (
        len(accepted) / len(transfer_candidates) if transfer_candidates else 0.0
    )
    collision_frequency = len(collisions) / len(contested) if contested else 0.0

    by_owner: dict[str, dict[str, float | int]] = defaultdict(
        lambda: {
            "claims": 0,
            "cross_domain_targets": 0,
            "accepted_targets": 0,
            "rejected_targets": 0,
        }
    )
    for claim in claims:
        by_owner[claim.owner]["claims"] += 1
        for decision in claim.transfer_decisions:
            if not _is_cross_domain(decision.target):
                continue
            by_owner[claim.owner]["cross_domain_targets"] += 1
            if decision.decision == "accepted":
                by_owner[claim.owner]["accepted_targets"] += 1
            else:
                by_owner[claim.owner]["rejected_targets"] += 1

    by_owner_dict = {owner: stats for owner, stats in by_owner.items()}

    return {
        "claims_total": total_claims,
        "claims_unique_id": len(unique_claim_ids),
        "duplicate_claim_count": duplicate_claim_count,
        "duplicate_claim_rate": round(duplicate_claim_rate, 4),
        "transfer_candidates": len(transfer_candidates),
        "contested_transfer_candidates": len(contested),
        "transfer_accepted": len(accepted),
        "transfer_acceptance_rate": round(transfer_acceptance_rate, 4),
        "merge_collision_count": len(collisions),
        "merge_collision_frequency": round(collision_frequency, 4),
        "by_owner": by_owner_dict,
    }


def build_payload(
    *,
    intake: dict,
    claims: list[Claim],
    summary: dict,
    source_path: Path,
    active_target_paths: list[Path],
    source_a: str,
    source_b: str,
) -> dict:
    return {
        "experiment": "F-IS5",
        "title": "two-pass lane distillation scoring",
        "source_intake_artifact": str(source_path).replace("\\", "/"),
        "active_target_sources": [str(path).replace("\\", "/") for path in active_target_paths],
        "pass_count": 2,
        "pass_sources": {"lane-owner-A": source_a, "lane-owner-B": source_b},
        "input_papers": intake.get("retrieved_count", 0),
        "input_lanes": len(intake.get("lane_plan", [])),
        "summary_metrics": summary,
        "claims": [
            {
                "claim_id": claim.claim_id,
                "owner": claim.owner,
                "source_set": claim.source_set,
                "lane_id": claim.lane_id,
                "paper_id": claim.paper_id,
                "theme": claim.theme,
                "claim_text": claim.claim_text,
                "targets": [
                    decision.target for decision in claim.transfer_decisions
                ],
                "cross_domain_targets": list(
                    _cross_domain_targets(claim.transfer_decisions)
                ),
                "transfer_decisions": [
                    {
                        "target": decision.target,
                        "decision": decision.decision,
                        "rationale": decision.rationale,
                        "cross_domain": _is_cross_domain(decision.target),
                    }
                    for decision in claim.transfer_decisions
                ],
            }
            for claim in claims
        ],
        "interpretation": (
            "Pass A and Pass B independently distilled the same lane pack. "
            "Transfer acceptance now requires explicit per-target accepted tags from both owners, "
            "and collision frequency reflects explicit accepted/rejected disagreement."
        ),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--in", dest="input_path", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--per-lane", type=int, default=3)
    parser.add_argument("--seed-a", type=int, default=1861)
    parser.add_argument("--seed-b", type=int, default=1862)
    parser.add_argument("--source-a", choices=("selected", "backlog"), default="selected")
    parser.add_argument("--source-b", choices=("selected", "backlog"), default="selected")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    intake = json.loads(args.input_path.read_text(encoding="utf-8"))
    active_target_paths = [
        Path("tasks/FRONTIER.md"),
        Path("domains/information-science/tasks/FRONTIER.md"),
        Path("domains/finance/tasks/FRONTIER.md"),
        Path("domains/ai/tasks/FRONTIER.md"),
        Path("memory/PRINCIPLES.md"),
        Path("beliefs/PHILOSOPHY.md"),
    ]
    active_targets = load_active_targets(active_target_paths)

    claims_a = distill_pass(
        intake=intake,
        owner="lane-owner-A",
        source=args.source_a,
        seed=args.seed_a,
        per_lane=max(1, args.per_lane),
        active_targets=active_targets,
    )
    claims_b = distill_pass(
        intake=intake,
        owner="lane-owner-B",
        source=args.source_b,
        seed=args.seed_b,
        per_lane=max(1, args.per_lane),
        active_targets=active_targets,
    )
    claims = claims_a + claims_b

    summary = summarize_claims(claims, active_targets)
    payload = build_payload(
        intake=intake,
        claims=claims,
        summary=summary,
        source_path=args.input_path,
        active_target_paths=active_target_paths,
        source_a=args.source_a,
        source_b=args.source_b,
    )
    payload["generated_at_utc"] = datetime.now(timezone.utc).isoformat(
        timespec="seconds"
    ).replace("+00:00", "Z")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {args.out}")
    print(
        "claims=",
        summary["claims_total"],
        "duplicate_rate=",
        summary["duplicate_claim_rate"],
        "transfer_accept_rate=",
        summary["transfer_acceptance_rate"],
        "collision_freq=",
        summary["merge_collision_frequency"],
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

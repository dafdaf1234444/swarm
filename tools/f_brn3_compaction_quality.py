#!/usr/bin/env python3
"""F-BRN3 baseline: compare size-first vs Sharpe-first compaction policies."""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

SESSION_RE = re.compile(r"Updated:\s+\d{4}-\d{2}-\d{2}\s+S(\d+)")
LESSON_SESSION_RE = re.compile(r"(?:\*{0,2})Session(?:\*{0,2})\s*:\s*S(\d+)", re.IGNORECASE)


@dataclass(frozen=True)
class LessonRow:
    lesson_id: str
    session: int | None
    age_sessions: int
    lines: int
    tokens: int
    citations: int
    in_principles: bool
    sharpe: float
    age_norm_sharpe: float


def parse_current_session(next_text: str) -> int:
    m = SESSION_RE.search(next_text)
    return int(m.group(1)) if m else 0


def parse_lesson_session(lesson_text: str) -> int | None:
    m = LESSON_SESSION_RE.search(lesson_text)
    if m:
        return int(m.group(1))
    return None


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def is_citation_source(path: Path, repo_root: Path) -> bool:
    rel = path.relative_to(repo_root).as_posix()
    if rel.startswith("memory/lessons/"):
        return False
    if rel.startswith("experiments/"):
        return False
    if rel == "memory/SESSION-LOG.md":
        return False
    if rel.endswith("FRONTIER-ARCHIVE.md"):
        return False
    return rel.endswith(".md")


def load_citation_sources(repo_root: Path) -> list[str]:
    texts: list[str] = []
    for path in sorted(repo_root.rglob("*.md")):
        if is_citation_source(path, repo_root):
            texts.append(read_text(path))
    return texts


def _count_refs(texts: list[str], needle: str) -> int:
    pat = re.compile(rf"\b{re.escape(needle)}\b")
    return sum(len(pat.findall(t)) for t in texts)


def collect_lessons(
    lessons_dir: Path,
    *,
    citation_sources: list[str],
    principles_text: str,
    current_session: int,
) -> list[LessonRow]:
    raw_rows: list[dict[str, Any]] = []
    max_lesson_num = 0
    for path in sorted(lessons_dir.glob("L-*.md")):
        lesson_id = path.stem.upper()
        text = read_text(path)
        if not text:
            continue
        lesson_num = int(lesson_id.split("-")[1]) if "-" in lesson_id else 0
        max_lesson_num = max(max_lesson_num, lesson_num)
        lines = max(1, len(text.splitlines()))
        tokens = max(1, len(text) // 4)
        session = parse_lesson_session(text)
        citations = _count_refs(citation_sources, lesson_id)
        in_principles = bool(re.search(rf"\b{re.escape(lesson_id)}\b", principles_text))
        raw_rows.append(
            {
                "lesson_id": lesson_id,
                "lesson_num": lesson_num,
                "session": session,
                "lines": lines,
                "tokens": tokens,
                "citations": citations,
                "in_principles": in_principles,
            }
        )

    rows: list[LessonRow] = []
    for raw in raw_rows:
        if current_session and raw["session"] is not None:
            age = max(1, current_session - raw["session"])
        else:
            age = max(1, max_lesson_num - raw["lesson_num"] + 1)
        sharpe = raw["citations"] / raw["lines"]
        age_norm_sharpe = raw["citations"] / age
        rows.append(
            LessonRow(
                lesson_id=raw["lesson_id"],
                session=raw["session"],
                age_sessions=age,
                lines=raw["lines"],
                tokens=raw["tokens"],
                citations=raw["citations"],
                in_principles=raw["in_principles"],
                sharpe=round(sharpe, 6),
                age_norm_sharpe=round(age_norm_sharpe, 6),
            )
        )
    return rows


def select_with_budget(
    rows: list[LessonRow],
    *,
    budget_tokens: int,
    key_fn,
) -> list[LessonRow]:
    chosen: list[LessonRow] = []
    used = 0
    for row in sorted(rows, key=key_fn):
        if used >= budget_tokens:
            break
        chosen.append(row)
        used += row.tokens
    return chosen


def summarize_policy(selected: list[LessonRow], all_rows: list[LessonRow]) -> dict[str, Any]:
    total_tokens = sum(r.tokens for r in all_rows)
    total_citations = sum(r.citations for r in all_rows)
    selected_tokens = sum(r.tokens for r in selected)
    selected_citations = sum(r.citations for r in selected)
    absorbed_count = sum(1 for r in selected if r.in_principles)
    orphan_risk_count = sum(1 for r in selected if (r.citations == 0 and not r.in_principles))
    citation_loss_rate = (
        selected_citations / total_citations if total_citations > 0 else 0.0
    )
    return {
        "selected_count": len(selected),
        "selected_tokens": selected_tokens,
        "selected_token_share": round(selected_tokens / max(1, total_tokens), 6),
        "citation_loss": selected_citations,
        "citation_loss_rate": round(citation_loss_rate, 6),
        "absorbed_count": absorbed_count,
        "absorbed_share": round(absorbed_count / max(1, len(selected)), 6),
        "orphan_risk_count": orphan_risk_count,
        "mean_age_norm_sharpe": round(
            sum(r.age_norm_sharpe for r in selected) / max(1, len(selected)), 6
        ),
        "top_selected": [asdict(r) for r in selected[:10]],
    }


def compare_policies(rows: list[LessonRow], *, budget_fraction: float) -> dict[str, Any]:
    total_tokens = sum(r.tokens for r in rows)
    budget_tokens = max(1, int(round(total_tokens * budget_fraction)))

    size_selected = select_with_budget(
        rows,
        budget_tokens=budget_tokens,
        key_fn=lambda r: (-r.tokens, -r.lines, r.lesson_id),
    )
    sharpe_selected = select_with_budget(
        rows,
        budget_tokens=budget_tokens,
        key_fn=lambda r: (r.age_norm_sharpe, r.citations, -r.tokens, r.lesson_id),
    )

    size_summary = summarize_policy(size_selected, rows)
    sharpe_summary = summarize_policy(sharpe_selected, rows)

    comparison = {
        "citation_loss_rate_delta": round(
            sharpe_summary["citation_loss_rate"] - size_summary["citation_loss_rate"], 6
        ),
        "absorbed_share_delta": round(
            sharpe_summary["absorbed_share"] - size_summary["absorbed_share"], 6
        ),
        "orphan_risk_delta": sharpe_summary["orphan_risk_count"] - size_summary["orphan_risk_count"],
        "quality_policy_better_on_citation_loss": (
            sharpe_summary["citation_loss_rate"] < size_summary["citation_loss_rate"]
        ),
        "quality_policy_better_on_absorbed_share": (
            sharpe_summary["absorbed_share"] > size_summary["absorbed_share"]
        ),
    }

    return {
        "budget_fraction": budget_fraction,
        "budget_tokens": budget_tokens,
        "total_tokens": total_tokens,
        "size_policy": size_summary,
        "sharpe_policy": sharpe_summary,
        "comparison": comparison,
    }


def analyze(
    *,
    repo_root: Path,
    lessons_dir: Path,
    principles_path: Path,
    next_path: Path,
    budget_fraction: float,
) -> dict[str, Any]:
    next_text = read_text(next_path)
    current_session = parse_current_session(next_text)
    principles_text = read_text(principles_path)
    citation_sources = load_citation_sources(repo_root)
    rows = collect_lessons(
        lessons_dir,
        citation_sources=citation_sources,
        principles_text=principles_text,
        current_session=current_session,
    )
    policy = compare_policies(rows, budget_fraction=budget_fraction)
    return {
        "frontier_id": "F-BRN3",
        "check_mode": "verification",
        "current_session": current_session,
        "lesson_count": len(rows),
        "citation_source_count": len(citation_sources),
        "analysis": policy,
    }


def run(
    *,
    out_path: Path,
    repo_root: Path,
    lessons_dir: Path,
    principles_path: Path,
    next_path: Path,
    budget_fraction: float,
) -> dict[str, Any]:
    payload = analyze(
        repo_root=repo_root,
        lessons_dir=lessons_dir,
        principles_path=principles_path,
        next_path=next_path,
        budget_fraction=budget_fraction,
    )
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(
        description="F-BRN3 baseline: size-vs-Sharpe compaction candidate comparison."
    )
    parser.add_argument(
        "--repo-root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
    )
    parser.add_argument("--lessons-dir", type=Path, default=Path("memory/lessons"))
    parser.add_argument("--principles", type=Path, default=Path("memory/PRINCIPLES.md"))
    parser.add_argument("--next", dest="next_path", type=Path, default=Path("tasks/NEXT.md"))
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("experiments/brain/f-brn3-compaction-quality.json"),
    )
    parser.add_argument("--budget-fraction", type=float, default=0.2)
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    payload = run(
        out_path=(repo_root / args.out),
        repo_root=repo_root,
        lessons_dir=(repo_root / args.lessons_dir),
        principles_path=(repo_root / args.principles),
        next_path=(repo_root / args.next_path),
        budget_fraction=args.budget_fraction,
    )

    comp = payload["analysis"]["comparison"]
    print(f"Wrote {args.out.as_posix()}")
    print(
        "citation_loss_rate_delta (sharpe-size): "
        f"{comp['citation_loss_rate_delta']:+.6f}"
    )
    print(
        "absorbed_share_delta (sharpe-size): "
        f"{comp['absorbed_share_delta']:+.6f}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

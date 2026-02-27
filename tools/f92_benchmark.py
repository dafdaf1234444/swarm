#!/usr/bin/env python3
"""
f92_benchmark.py - Controlled colony-size benchmark for F92.

Runs fixed workloads at multiple parallelism levels and reports
wall-time speedup and efficiency.

Usage:
  python3 tools/f92_benchmark.py --profile wiki --workers 1,2,3,4 --runs 3
  python3 tools/f92_benchmark.py --profile compute --workers 1,2,3,4 --runs 3
  python3 tools/f92_benchmark.py --profile all --json-out experiments/spawn-quality/f92-benchmark.json
"""

from __future__ import annotations

import argparse
import json
import shutil
import statistics
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


REPO_ROOT = Path(__file__).resolve().parent.parent
LAB_ROOT = REPO_ROOT / "workspace" / "notes" / "bench" / "f92-bulletin-lab"


@dataclass
class RunResult:
    wall_seconds: float
    failures: int


def _wiki_workload() -> list[list[str]]:
    """Same-task workload used in L-200 (S108): 3 fixed topics."""
    py = sys.executable
    return [
        [py, str(REPO_ROOT / "tools" / "wiki_swarm.py"), "Distributed systems", "--depth", "1", "--fanout", "5"],
        [py, str(REPO_ROOT / "tools" / "wiki_swarm.py"), "Stigmergy", "--depth", "1", "--fanout", "5"],
        [py, str(REPO_ROOT / "tools" / "wiki_swarm.py"), "Error handling", "--depth", "1", "--fanout", "5"],
    ]


def _compute_workload() -> list[list[str]]:
    """
    CPU-heavy synthetic workload with four independent tasks.
    Uses separate subprocesses to avoid GIL effects.
    """
    py = sys.executable
    loops = [500000, 550000, 600000, 650000]
    tasks: list[list[str]] = []
    for n in loops:
        code = (
            "import hashlib\n"
            "data = b'x' * 2048\n"
            f"for _ in range({n}):\n"
            "    hashlib.sha256(data).digest()\n"
        )
        tasks.append([py, "-c", code])
    return tasks


def _prepare_bulletin_lab() -> tuple[Path, Path]:
    """Prepare isolated workspace that uses the real bulletin write path."""
    lab_tools = LAB_ROOT / "tools"
    lab_bulletins = LAB_ROOT / "experiments" / "inter-swarm" / "bulletins"
    lab_tools.mkdir(parents=True, exist_ok=True)
    lab_bulletins.mkdir(parents=True, exist_ok=True)
    shutil.copy2(REPO_ROOT / "tools" / "bulletin.py", lab_tools / "bulletin.py")
    return lab_tools / "bulletin.py", lab_bulletins / "f92-bench.md"


def _bulletin_workload() -> tuple[list[list[str]], Callable[[], None]]:
    """
    Cooperative shared-file workload via real `bulletin.py write`.
    Four tasks append to the same bulletin file.
    """
    script_path, bulletin_file = _prepare_bulletin_lab()
    py = sys.executable
    commands: list[list[str]] = []
    for i in range(4):
        msg = f"F92 benchmark bulletin write task-{i}"
        commands.append([py, str(script_path), "write", "f92-bench", "discovery", msg])

    def reset() -> None:
        if bulletin_file.exists():
            bulletin_file.unlink()

    return commands, reset


def get_workload(profile: str) -> dict[str, dict]:
    if profile == "wiki":
        return {"wiki": {"commands": _wiki_workload(), "reset": None}}
    if profile == "compute":
        return {"compute": {"commands": _compute_workload(), "reset": None}}
    if profile == "bulletin":
        commands, reset = _bulletin_workload()
        return {"bulletin": {"commands": commands, "reset": reset}}
    if profile == "all":
        commands, reset = _bulletin_workload()
        return {
            "wiki": {"commands": _wiki_workload(), "reset": None},
            "compute": {"commands": _compute_workload(), "reset": None},
            "bulletin": {"commands": commands, "reset": reset},
        }
    raise ValueError(f"Unknown profile: {profile}")


def _run_command(cmd: list[str]) -> int:
    proc = subprocess.run(cmd, cwd=str(REPO_ROOT), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return proc.returncode


def run_once(commands: list[list[str]], workers: int) -> RunResult:
    start = time.perf_counter()
    failures = 0
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for rc in pool.map(_run_command, commands):
            if rc != 0:
                failures += 1
    return RunResult(wall_seconds=time.perf_counter() - start, failures=failures)


def benchmark_workload(
    name: str,
    commands: list[list[str]],
    workers: list[int],
    runs: int,
    warmup: int,
    reset: Callable[[], None] | None = None,
) -> dict:
    for _ in range(max(0, warmup)):
        if reset:
            reset()
        run_once(commands, workers=max(workers))

    series: dict[int, list[RunResult]] = {w: [] for w in workers}
    for w in workers:
        for _ in range(runs):
            if reset:
                reset()
            series[w].append(run_once(commands, workers=w))

    medians = {w: statistics.median(x.wall_seconds for x in rs) for w, rs in series.items()}
    means = {w: statistics.mean(x.wall_seconds for x in rs) for w, rs in series.items()}
    failures = {w: sum(x.failures for x in rs) for w, rs in series.items()}

    baseline = medians[min(workers)]
    speedups = {w: (baseline / medians[w]) if medians[w] > 0 else 0.0 for w in workers}
    efficiency = {w: (speedups[w] / w) for w in workers}

    print(f"\n=== F92 Benchmark: {name} ===")
    print(f"Tasks: {len(commands)} | Runs: {runs} | Warmup: {warmup}")
    print(f"{'N':>3}  {'Median(s)':>10}  {'Mean(s)':>10}  {'Speedup':>8}  {'Efficiency':>10}  {'Failures':>8}")
    print("-" * 66)
    for w in workers:
        print(
            f"{w:>3}  {medians[w]:>10.2f}  {means[w]:>10.2f}  "
            f"{speedups[w]:>7.2f}x  {efficiency[w]:>9.3f}  {failures[w]:>8}"
        )

    return {
        "name": name,
        "tasks": len(commands),
        "runs": runs,
        "warmup": warmup,
        "workers": workers,
        "medians_seconds": medians,
        "means_seconds": means,
        "speedup_vs_n1": speedups,
        "efficiency": efficiency,
        "failures": failures,
    }


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Controlled F92 colony-size benchmark")
    parser.add_argument("--profile", choices=["wiki", "compute", "bulletin", "all"], default="all")
    parser.add_argument("--workers", default="1,2,3,4", help="Comma-separated worker counts")
    parser.add_argument("--runs", type=int, default=3, help="Benchmark repetitions per worker count")
    parser.add_argument("--warmup", type=int, default=1, help="Warmup runs (at max worker count)")
    parser.add_argument("--json-out", help="Optional JSON output path")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    workers = sorted({int(x.strip()) for x in args.workers.split(",") if x.strip()})
    if not workers or min(workers) < 1:
        print("Invalid --workers value", file=sys.stderr)
        return 1

    workloads = get_workload(args.profile)
    results = []
    for name, item in workloads.items():
        results.append(
            benchmark_workload(
                name,
                item["commands"],
                workers,
                args.runs,
                args.warmup,
                reset=item.get("reset"),
            )
        )

    payload = {
        "generated_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "profile": args.profile,
        "results": results,
    }

    if args.json_out:
        out = Path(args.json_out)
        if not out.is_absolute():
            out = REPO_ROOT / out
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        print(f"\nWrote: {out}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

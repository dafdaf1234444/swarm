#!/usr/bin/env python3
"""
f92_real_coop_benchmark.py - F92 real cooperative workload benchmark.

Runs a shared-file swarm-like workload where multiple workers perform
read-modify-write updates on one markdown file with lock-file coordination.

Usage:
  python tools/f92_real_coop_benchmark.py
  python tools/f92_real_coop_benchmark.py --runs 5 --workers 1,2,3,4 \
      --out experiments/spawn-quality/f92-real-coop-benchmark-s111.json
"""

from __future__ import annotations

import argparse
import concurrent.futures as cf
import hashlib
import json
import os
import statistics
import tempfile
import time
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent


def worker(
    shared_path: str,
    lock_path: str,
    task_id: int,
    updates_per_task: int,
    hash_loops_per_update: int,
    lock_sleep_seconds: float,
) -> None:
    shared = Path(shared_path)
    for update_idx in range(updates_per_task):
        # Simulate independent local processing before shared write.
        digest = f"{task_id}:{update_idx}".encode("utf-8")
        for _ in range(hash_loops_per_update):
            digest = hashlib.sha1(digest).digest()

        # Simple cross-process lock using lock-file creation.
        fd = None
        while fd is None:
            try:
                fd = os.open(lock_path, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
            except (FileExistsError, PermissionError):
                time.sleep(lock_sleep_seconds)

        try:
            old = shared.read_text(encoding="utf-8")
            line = f"- claim t{task_id} u{update_idx} h{digest.hex()[:8]}\n"
            shared.write_text(old + line, encoding="utf-8")
        finally:
            os.close(fd)
            removed = False
            while not removed:
                try:
                    os.remove(lock_path)
                    removed = True
                except (FileNotFoundError, PermissionError):
                    time.sleep(lock_sleep_seconds)


def run_once(
    *,
    max_workers: int,
    tasks: int,
    updates_per_task: int,
    hash_loops_per_update: int,
    lock_sleep_seconds: float,
) -> float:
    with tempfile.TemporaryDirectory() as td:
        shared = Path(td) / "NEXT-shared.md"
        lock = Path(td) / "NEXT-shared.lock"
        shared.write_text("# Shared NEXT\n\n## Claims\n", encoding="utf-8")

        start = time.perf_counter()
        with cf.ProcessPoolExecutor(max_workers=max_workers) as pool:
            futs = [
                pool.submit(
                    worker,
                    str(shared),
                    str(lock),
                    task_id,
                    updates_per_task,
                    hash_loops_per_update,
                    lock_sleep_seconds,
                )
                for task_id in range(tasks)
            ]
            for fut in futs:
                fut.result()
        elapsed = time.perf_counter() - start

        lines = shared.read_text(encoding="utf-8").splitlines()
        claim_lines = [ln for ln in lines if ln.startswith("- claim ")]
        expected = tasks * updates_per_task
        if len(claim_lines) != expected:
            raise RuntimeError(
                f"shared file integrity failure: {len(claim_lines)} != {expected}"
            )
        return elapsed


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="F92 real cooperative benchmark")
    parser.add_argument("--workers", default="1,2,3,4", help="Worker counts")
    parser.add_argument("--runs", type=int, default=5, help="Repeats per worker")
    parser.add_argument("--tasks", type=int, default=4, help="Total parallel tasks")
    parser.add_argument(
        "--updates-per-task", type=int, default=120, help="Shared-file updates per task"
    )
    parser.add_argument(
        "--hash-loops-per-update",
        type=int,
        default=250,
        help="Local processing per update before file write",
    )
    parser.add_argument(
        "--lock-sleep-seconds",
        type=float,
        default=0.0005,
        help="Sleep between lock retries",
    )
    parser.add_argument(
        "--out",
        default="experiments/spawn-quality/f92-real-coop-benchmark-s111.json",
        help="Output JSON path",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    workers = sorted({int(w.strip()) for w in args.workers.split(",") if w.strip()})
    if not workers or workers[0] < 1:
        raise SystemExit("Invalid --workers")

    # Warmup once for each worker count.
    for w in workers:
        run_once(
            max_workers=w,
            tasks=args.tasks,
            updates_per_task=args.updates_per_task,
            hash_loops_per_update=args.hash_loops_per_update,
            lock_sleep_seconds=args.lock_sleep_seconds,
        )

    results: dict[int, dict[str, object]] = {}
    for w in workers:
        times = [
            run_once(
                max_workers=w,
                tasks=args.tasks,
                updates_per_task=args.updates_per_task,
                hash_loops_per_update=args.hash_loops_per_update,
                lock_sleep_seconds=args.lock_sleep_seconds,
            )
            for _ in range(args.runs)
        ]
        median_s = statistics.median(times)
        results[w] = {
            "times_s": [round(t, 3) for t in times],
            "median_s": round(median_s, 3),
        }

    baseline = results[min(workers)]["median_s"]
    for w in workers:
        median_s = results[w]["median_s"]
        speedup = (baseline / median_s) if median_s > 0 else 0.0
        results[w]["speedup_vs_n1"] = round(speedup, 3)
        results[w]["efficiency"] = round(speedup / w, 3)

    payload = {
        "session": "S111",
        "date": "2026-02-27",
        "workload": {
            "name": "real-shared-file-updates",
            "description": (
                "4 worker processes perform read-modify-write updates on one shared "
                "markdown file using lock-file coordination"
            ),
            "shared_file_kind": "swarm-style markdown handoff file",
            "tasks": args.tasks,
            "updates_per_task": args.updates_per_task,
            "hash_loops_per_update": args.hash_loops_per_update,
            "lock_strategy": "lockfile (create-exclusive + spin)",
        },
        "repeats": args.runs,
        "results": results,
    }

    out_path = Path(args.out)
    if not out_path.is_absolute():
        out_path = REPO_ROOT / out_path
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    print(json.dumps(payload, indent=2))
    print(f"\nWROTE {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

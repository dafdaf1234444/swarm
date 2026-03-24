#!/usr/bin/env python3
"""Focused regressions for tools/guards/23-concurrent-commit.sh."""

import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
GUARD = ROOT / "tools" / "guards" / "23-concurrent-commit.sh"


def _fake_ps_script(lines: list[str]) -> str:
    body = "\n".join(lines) + ("\n" if lines else "")
    return f"#!/bin/sh\ncat <<'EOF'\n{body}EOF\n"


def _run_guard(lines: list[str], extra_env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    with tempfile.TemporaryDirectory() as tmp:
        ps_path = Path(tmp) / "ps"
        ps_path.write_text(_fake_ps_script(lines), encoding="utf-8")
        ps_path.chmod(0o755)

        env = os.environ.copy()
        env["PATH"] = f"{tmp}{os.pathsep}{env['PATH']}"
        if extra_env:
            env.update(extra_env)

        return subprocess.run(
            ["bash", "-lc", f"source '{GUARD}'"],
            capture_output=True,
            text=True,
            cwd=ROOT,
            env=env,
            timeout=15,
        )


class TestConcurrentCommitGuard(unittest.TestCase):
    def test_blocks_missing_temp_index_under_moderate_concurrency(self):
        result = _run_guard(
            [
                "u 1 0.0 0.0 0 0 ? S 00:00 0:00 git commit -m test",
                "u 2 0.0 0.0 0 0 ? S 00:00 0:00 git add file.txt",
                "u 3 0.0 0.0 0 0 ? S 00:00 0:00 git read-tree HEAD",
            ]
        )
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("require GIT_INDEX_FILE=<tmpfile>", result.stdout)

    def test_allows_isolated_index_under_moderate_concurrency(self):
        result = _run_guard(
            [
                "u 1 0.0 0.0 0 0 ? S 00:00 0:00 git commit -m test",
                "u 2 0.0 0.0 0 0 ? S 00:00 0:00 git add file.txt",
                "u 3 0.0 0.0 0 0 ? S 00:00 0:00 git write-tree",
            ],
            {"GIT_INDEX_FILE": "/tmp/swarm-idx"},
        )
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("L-1534 OK: isolated index detected", result.stdout)

    def test_stampede_still_blocks_even_with_temp_index(self):
        result = _run_guard(
            [
                "u 1 0.0 0.0 0 0 ? S 00:00 0:00 git commit -m test",
                "u 2 0.0 0.0 0 0 ? S 00:00 0:00 git add file1",
                "u 3 0.0 0.0 0 0 ? S 00:00 0:00 git add file2",
                "u 4 0.0 0.0 0 0 ? S 00:00 0:00 git read-tree HEAD",
                "u 5 0.0 0.0 0 0 ? S 00:00 0:00 git write-tree",
            ],
            {"GIT_INDEX_FILE": "/tmp/swarm-idx"},
        )
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn("Concurrent-commit stampede detected", result.stdout)


if __name__ == "__main__":
    unittest.main()

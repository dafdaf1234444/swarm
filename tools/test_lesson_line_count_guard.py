#!/usr/bin/env python3
"""Regression tests for tools/guards/11-lesson-line-count.sh."""

import shlex
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parent.parent
GUARD_PATH = REPO_ROOT / "tools" / "guards" / "11-lesson-line-count.sh"


def _run_guard(*, staged_lessons: str = "", staged_new_lessons: str = "", allow_long: bool = False) -> subprocess.CompletedProcess[str]:
    script = f"""
set -euo pipefail
export STAGED_LESSONS={shlex.quote(staged_lessons)}
export STAGED_NEW_LESSONS={shlex.quote(staged_new_lessons)}
export ALLOW_LONG_LESSON={"1" if allow_long else "0"}
source {shlex.quote(str(GUARD_PATH))}
"""
    return subprocess.run(
        ["bash", "-lc", script],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )


def _write_lesson(path: Path, lines: int) -> None:
    path.write_text("\n".join(f"line {idx}" for idx in range(lines)) + "\n", encoding="utf-8")


class LessonLineCountGuardTests(unittest.TestCase):
    def test_passes_for_short_staged_lesson(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            lesson_path = Path(tmp) / "L-999.md"
            _write_lesson(lesson_path, 20)
            result = _run_guard(staged_lessons=str(lesson_path))
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("FM-31 lesson line-count guard: PASS", result.stdout)

    def test_blocks_modified_lesson_even_when_not_new(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            lesson_path = Path(tmp) / "L-999.md"
            _write_lesson(lesson_path, 21)
            result = _run_guard(staged_lessons=str(lesson_path))
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FM-31 FAIL", result.stdout)
        self.assertIn("L-999.md(21L)", result.stdout)

    def test_allow_long_lesson_bypasses_block(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            lesson_path = Path(tmp) / "L-999.md"
            _write_lesson(lesson_path, 24)
            result = _run_guard(staged_lessons=str(lesson_path), allow_long=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("ALLOW_LONG_LESSON=1 set", result.stdout)


if __name__ == "__main__":
    unittest.main()

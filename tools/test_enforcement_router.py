#!/usr/bin/env python3
"""Regressions for enforcement_router structural file discovery."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import enforcement_router  # noqa: E402


class TestEnforcementRouter(unittest.TestCase):
    def test_auto_discover_structural_files_includes_nested_tools(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir)
            guard = repo / "tools" / "guards" / "23-concurrent-commit.sh"
            guard.parent.mkdir(parents=True, exist_ok=True)
            guard.write_text("# L-1528\n# L-1534\n", encoding="utf-8")

            discovered = enforcement_router._auto_discover_structural_files(
                repo, min_refs=2
            )

            self.assertIn("tools/guards/23-concurrent-commit.sh", discovered)

    def test_nested_tool_reference_marks_lesson_structural(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            repo = Path(tmpdir)
            guard = repo / "tools" / "guards" / "23-concurrent-commit.sh"
            guard.parent.mkdir(parents=True, exist_ok=True)
            guard.write_text("# L-1528\n# L-1534\n", encoding="utf-8")

            lessons_dir = repo / "memory" / "lessons"
            lessons_dir.mkdir(parents=True, exist_ok=True)
            (lessons_dir / "L-1534.md").write_text(
                "Sharpe: 10\n"
                "Session: S529\n"
                "## Rule\n"
                "Concurrent sessions MUST use GIT_INDEX_FILE.\n",
                encoding="utf-8",
            )

            rules = enforcement_router.scan_lessons(lessons_dir, min_sharpe=8)
            structural_refs, periodic_refs = enforcement_router.build_reference_maps(repo)

            self.assertEqual(len(rules), 1)
            self.assertEqual(
                enforcement_router.classify(
                    rules[0]["lesson"], structural_refs, periodic_refs
                ),
                "STRUCTURAL",
            )


if __name__ == "__main__":
    unittest.main()

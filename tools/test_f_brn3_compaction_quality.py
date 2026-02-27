#!/usr/bin/env python3
"""Regression tests for F-BRN3 compaction quality baseline."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import f_brn3_compaction_quality as mod


class TestFBrn3CompactionQuality(unittest.TestCase):
    def test_parse_current_session(self):
        self.assertEqual(mod.parse_current_session("Updated: 2026-02-27 S186"), 186)
        self.assertEqual(mod.parse_current_session("Updated: missing"), 0)

    def test_compare_policies_prefers_sharpe_for_citation_loss(self):
        rows = [
            mod.LessonRow(
                lesson_id="L-001",
                session=100,
                age_sessions=86,
                lines=20,
                tokens=120,
                citations=10,
                in_principles=True,
                sharpe=0.5,
                age_norm_sharpe=0.116,
            ),
            mod.LessonRow(
                lesson_id="L-002",
                session=150,
                age_sessions=36,
                lines=20,
                tokens=110,
                citations=0,
                in_principles=True,
                sharpe=0.0,
                age_norm_sharpe=0.0,
            ),
            mod.LessonRow(
                lesson_id="L-003",
                session=151,
                age_sessions=35,
                lines=20,
                tokens=40,
                citations=0,
                in_principles=False,
                sharpe=0.0,
                age_norm_sharpe=0.0,
            ),
        ]
        result = mod.compare_policies(rows, budget_fraction=0.4)
        self.assertTrue(result["comparison"]["quality_policy_better_on_citation_loss"])
        self.assertLess(
            result["sharpe_policy"]["citation_loss_rate"],
            result["size_policy"]["citation_loss_rate"],
        )

    def test_run_writes_artifact(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "memory/lessons").mkdir(parents=True)
            (root / "tasks").mkdir(parents=True)
            (root / "experiments/brain").mkdir(parents=True)

            (root / "memory/lessons/L-001.md").write_text(
                "\n".join(
                    [
                        "# L-001",
                        "**Session**: S100",
                        "payload",
                    ]
                ),
                encoding="utf-8",
            )
            (root / "memory/lessons/L-002.md").write_text(
                "\n".join(
                    [
                        "# L-002",
                        "**Session**: S150",
                        "payload",
                    ]
                ),
                encoding="utf-8",
            )
            (root / "memory/PRINCIPLES.md").write_text(
                "\n".join(
                    [
                        "## Meta",
                        "P-001 cites L-001",
                    ]
                ),
                encoding="utf-8",
            )
            (root / "tasks/NEXT.md").write_text("Updated: 2026-02-27 S186", encoding="utf-8")
            (root / "tasks/FRONTIER.md").write_text("L-001", encoding="utf-8")

            out = root / "experiments/brain/f-brn3-compaction-quality-s186-test.json"
            payload = mod.run(
                out_path=out,
                repo_root=root,
                lessons_dir=root / "memory/lessons",
                principles_path=root / "memory/PRINCIPLES.md",
                next_path=root / "tasks/NEXT.md",
                budget_fraction=0.5,
            )

            self.assertTrue(out.exists())
            self.assertEqual(payload["frontier_id"], "F-BRN3")
            self.assertEqual(payload["current_session"], 186)
            self.assertEqual(payload["lesson_count"], 2)


if __name__ == "__main__":
    unittest.main()

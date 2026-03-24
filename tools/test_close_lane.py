#!/usr/bin/env python3
"""Regression tests for explicit frontier-resolution support in close_lane.py."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import close_lane  # noqa: E402


class TestCloseLaneFrontierResolution(unittest.TestCase):
    def test_update_frontier_file_marks_frontier_non_active_and_upserts_resolved_row(self):
        frontier_text = """# Demo Domain
Updated: 2026-03-01 S500 | Active: 1 | Resolved: 0

## Active

- **F-DEMO1**: Does the demo frontier close cleanly?
  - Evidence stays attached to the frontier block.

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            frontier_path = Path(tmpdir) / "FRONTIER.md"
            frontier_path.write_text(frontier_text, encoding="utf-8")

            changed = close_lane.update_frontier_file(
                frontier_path=frontier_path,
                frontier_id="F-DEMO1",
                session="S527",
                answer="YES — automated close sync landed.",
                today="2026-03-23",
            )

            self.assertTrue(changed)
            updated = frontier_path.read_text(encoding="utf-8")
            self.assertIn("Updated: 2026-03-23 S527 | Active: 0 | Resolved: 1", updated)
            self.assertIn("- ~~**F-DEMO1**~~: Moved to Resolved (S527).", updated)
            self.assertIn("| F-DEMO1 | YES — automated close sync landed. | S527 | 2026-03-23 |", updated)

    def test_update_frontier_file_replaces_existing_resolved_row(self):
        frontier_text = """# Demo Domain
Updated: 2026-03-01 S500 | Active: 1 | Resolved: 1

## Active

- **F-DEMO1**: Does the demo frontier close cleanly?

## Resolved
| ID | Answer | Session | Date |
|----|--------|---------|------|
| F-DEMO1 | OLD ANSWER | S500 | 2026-03-01 |
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            frontier_path = Path(tmpdir) / "FRONTIER.md"
            frontier_path.write_text(frontier_text, encoding="utf-8")

            close_lane.update_frontier_file(
                frontier_path=frontier_path,
                frontier_id="F-DEMO1",
                session="S527",
                answer="UPDATED ANSWER",
                today="2026-03-23",
            )

            updated = frontier_path.read_text(encoding="utf-8")
            self.assertEqual(updated.count("| F-DEMO1 |"), 1)
            self.assertIn("| F-DEMO1 | UPDATED ANSWER | S527 | 2026-03-23 |", updated)


if __name__ == "__main__":
    unittest.main()

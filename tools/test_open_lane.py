#!/usr/bin/env python3
"""Focused regressions for lane metadata generation."""

import tempfile
import unittest
from pathlib import Path
from unittest import mock
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import open_lane


class TestOpenLaneHelpers(unittest.TestCase):
    def test_scope_key_domain_inference_normalizes_artifact_path(self):
        artifact = open_lane.normalize_artifact_path(
            "f-qc6.json",
            domain="",
            focus="global",
            scope_key="domains/quality/tasks/FRONTIER.md",
        )
        self.assertEqual(artifact, "experiments/quality/f-qc6.json")

    def test_append_open_row_writes_check_focus_and_domain_tags(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            lane_file = Path(tmpdir) / "SWARM-LANES.md"
            lane_file.write_text("", encoding="utf-8")
            with mock.patch.object(open_lane, "LANES_FILE", lane_file):
                open_lane.append_open_row(
                    lane_id="COORD-S545-COVERAGE",
                    session="S545",
                    intent="coordination-pass",
                    expect="Coordinator row should clear missing-coordinator DUE for 2 active dispatch lanes.",
                    artifact="tasks/SWARM-LANES.md",
                    frontier="",
                    focus="global",
                    check_mode="coordination",
                    personality="domain-expert",
                    scope_key="domains/quality/tasks/FRONTIER.md",
                    author="ai-session",
                    model="gpt-5",
                    branch="master",
                    domain="",
                    note="test row",
                    check_focus="coordinator-contract",
                )
            text = lane_file.read_text(encoding="utf-8")
            self.assertIn("check_focus=coordinator-contract", text)
            self.assertIn("domain_sync=queued", text)
            self.assertIn("memory_target=domains/quality/tasks/FRONTIER.md", text)


if __name__ == "__main__":
    unittest.main()

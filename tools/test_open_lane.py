#!/usr/bin/env python3
"""Regression tests for artifact path normalization in open_lane.py."""

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent))
import open_lane  # noqa: E402


LANE_HEADER = """# Swarm Lanes
| Date | Lane | Session | Agent | Branch | PR | Model | Platform | Scope-Key | Etc | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
"""


class TestOpenLaneArtifactNormalization(unittest.TestCase):
    def test_normalize_artifact_path_prefixes_bare_json_with_domain_experiments_dir(self):
        self.assertEqual(
            open_lane.normalize_artifact_path(
                artifact="f-fore1-scoring-s999.json",
                domain="forecasting",
                focus="domains/forecasting",
            ),
            "experiments/forecasting/f-fore1-scoring-s999.json",
        )

    def test_normalize_artifact_path_leaves_explicit_paths_unchanged(self):
        self.assertEqual(
            open_lane.normalize_artifact_path(
                artifact="experiments/meta/already-scoped.json",
                domain="meta",
                focus="domains/meta",
            ),
            "experiments/meta/already-scoped.json",
        )

    def test_main_writes_normalized_artifact_to_lane_and_skeleton(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            repo_root = Path(tmpdir)
            lanes_file = repo_root / "tasks" / "SWARM-LANES.md"
            lanes_file.parent.mkdir(parents=True, exist_ok=True)
            lanes_file.write_text(LANE_HEADER, encoding="utf-8")
            archive_file = repo_root / "tasks" / "SWARM-LANES-ARCHIVE.md"
            archive_file.write_text("", encoding="utf-8")

            argv = [
                "open_lane.py",
                "--lane", "DOMEX-FORE-S999",
                "--session", "S999",
                "--domain", "forecasting",
                "--focus", "domains/forecasting",
                "--intent", "regression-test",
                "--expect", "artifact skeleton lands in experiments directory and fails if repo root file appears",
                "--artifact", "f-fore1-scoring-s999.json",
            ]
            with mock.patch.object(open_lane, "REPO_ROOT", repo_root), \
                 mock.patch.object(open_lane, "LANES_FILE", lanes_file), \
                 mock.patch.object(open_lane, "LANES_ARCHIVE", archive_file), \
                 mock.patch.object(sys, "argv", argv):
                open_lane.main()

            normalized = "experiments/forecasting/f-fore1-scoring-s999.json"
            lane_text = lanes_file.read_text(encoding="utf-8")
            self.assertIn(f"artifact={normalized}", lane_text)
            skeleton_path = repo_root / normalized
            self.assertTrue(skeleton_path.exists())
            self.assertFalse((repo_root / "f-fore1-scoring-s999.json").exists())


if __name__ == "__main__":
    unittest.main()

import tempfile
import unittest
from pathlib import Path
import sys

TOOLS_DIR = Path(__file__).resolve().parent
if str(TOOLS_DIR) not in sys.path:
    sys.path.insert(0, str(TOOLS_DIR))
import science_quality


class ScienceQualitySessionSourceTest(unittest.TestCase):
    def test_current_session_prefers_shared_helper(self):
        original_shared = science_quality._shared_session_number
        try:
            science_quality._shared_session_number = lambda: 612
            self.assertEqual(science_quality._current_session(), 612)
        finally:
            science_quality._shared_session_number = original_shared

    def test_current_session_falls_back_to_session_log(self):
        original_root = science_quality.REPO_ROOT
        original_shared = science_quality._shared_session_number
        original_experiments = science_quality.EXPERIMENTS_DIR
        original_lanes = science_quality.LANES_FILE
        original_archive = science_quality.LANES_ARCHIVE
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                root = Path(tmpdir)
                session_log = root / "memory" / "SESSION-LOG.md"
                session_log.parent.mkdir(parents=True)
                session_log.write_text("S530 | old\nS538 | current\n", encoding="utf-8")

                science_quality.REPO_ROOT = root
                science_quality.EXPERIMENTS_DIR = root / "experiments"
                science_quality.LANES_FILE = root / "tasks" / "SWARM-LANES.md"
                science_quality.LANES_ARCHIVE = root / "tasks" / "SWARM-LANES-ARCHIVE.md"
                science_quality._shared_session_number = None

                self.assertEqual(science_quality._current_session(), 538)
        finally:
            science_quality.REPO_ROOT = original_root
            science_quality._shared_session_number = original_shared
            science_quality.EXPERIMENTS_DIR = original_experiments
            science_quality.LANES_FILE = original_lanes
            science_quality.LANES_ARCHIVE = original_archive

    def test_save_writes_periodic_artifact(self):
        original_root = science_quality.REPO_ROOT
        original_experiments = science_quality.EXPERIMENTS_DIR
        original_lanes = science_quality.LANES_FILE
        original_archive = science_quality.LANES_ARCHIVE
        original_shared = science_quality._shared_session_number
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                root = Path(tmpdir)
                (root / "memory").mkdir(parents=True)
                (root / "memory" / "SESSION-LOG.md").write_text("S541 | current\n", encoding="utf-8")
                exp_dir = root / "experiments" / "meta"
                exp_dir.mkdir(parents=True)
                (exp_dir / "science-quality-seed-s541.json").write_text(
                    '{"expect":"mean > 0.5","actual":"baseline comparison p<0.05","mode":"falsification"}\n',
                    encoding="utf-8",
                )
                tasks_dir = root / "tasks"
                tasks_dir.mkdir(parents=True)
                (tasks_dir / "SWARM-LANES.md").write_text("", encoding="utf-8")
                (tasks_dir / "SWARM-LANES-ARCHIVE.md").write_text("", encoding="utf-8")

                science_quality.REPO_ROOT = root
                science_quality.EXPERIMENTS_DIR = root / "experiments"
                science_quality.LANES_FILE = tasks_dir / "SWARM-LANES.md"
                science_quality.LANES_ARCHIVE = tasks_dir / "SWARM-LANES-ARCHIVE.md"
                science_quality._shared_session_number = None

                rc = science_quality.main(["--save"])
                self.assertEqual(rc, 0)

                artifact = root / "experiments" / "meta" / "science-quality-audit-s541.json"
                self.assertTrue(artifact.exists())
                saved = artifact.read_text(encoding="utf-8")
                self.assertIn('"session": "S541"', saved)
                self.assertIn('"mode": "periodic"', saved)

                report = science_quality.build_report()
                self.assertIsNotNone(report)
                self.assertEqual(report["n_experiments"], 1)
        finally:
            science_quality.REPO_ROOT = original_root
            science_quality.EXPERIMENTS_DIR = original_experiments
            science_quality.LANES_FILE = original_lanes
            science_quality.LANES_ARCHIVE = original_archive
            science_quality._shared_session_number = original_shared


if __name__ == "__main__":
    unittest.main()

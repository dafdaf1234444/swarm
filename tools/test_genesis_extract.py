#!/usr/bin/env python3
"""Regression tests for genesis_extract.py compaction."""

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import genesis_extract  # noqa: E402


class TestGenesisExtract(unittest.TestCase):
    def test_principles_projection_preserves_ids(self):
        sample = (
            "# Principles\n"
            "272 live principles.\n\n"
            "S1 (+2 P-001 alpha + P-002 beta).\n"
            "## Architecture\n"
            "**Structure**: P-001 alpha by usage not theory | P-002 beta from action\n"
        )

        projected = genesis_extract._project_principles_text(sample)

        self.assertIn("2 live principles", projected)
        self.assertIn("P-001", projected)
        self.assertIn("P-002", projected)

    def test_lean_bundle_projects_state_and_boots(self):
        with tempfile.TemporaryDirectory(prefix="genesis-extract-") as tmpdir:
            bundle = Path(tmpdir) / "bundle"
            manifest = genesis_extract.extract_genesis(
                bundle,
                top_n=100,
                include_tools=True,
                minimal=True,
                lean=True,
                dry_run=False,
            )

            self.assertLess(manifest["total_bytes"], 350 * 1024)

            generated_size = sum(
                p.stat().st_size
                for p in bundle.rglob("*")
                if p.is_file() and ".git" not in p.parts
            )
            self.assertLess(abs(generated_size - manifest["total_bytes"]), 10 * 1024)

            self.assertIn("hub_lessons_top5", manifest)
            self.assertTrue(manifest["hub_lessons_top5"])

            self.assertEqual(self._run_daughter(bundle, "tools/orient.py").returncode, 0)
            self.assertEqual(
                self._run_daughter(bundle, "tools/validate_beliefs.py", "--quick").returncode,
                0,
            )
            self.assertEqual(self._run_daughter(bundle, "tools/sync_state.py").returncode, 0)

    def _run_daughter(self, bundle: Path, script: str, *args: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            [sys.executable, script, *args],
            cwd=bundle,
            capture_output=True,
            text=True,
            timeout=180,
        )


if __name__ == "__main__":
    unittest.main()

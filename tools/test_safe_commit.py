#!/usr/bin/env python3
"""Focused regressions for concurrent-safe commit helpers."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import safe_commit


class TestSafeCommitHelpers(unittest.TestCase):
    def test_run_validation_prefers_bash_check_sh(self):
        seen = {}

        def fake_run(cmd, **kw):
            seen["cmd"] = cmd
            seen["env"] = kw.get("env", {})
            return ""

        def fake_which(name):
            return "/usr/bin/bash" if name == "bash" else None

        with patch.object(safe_commit, "run", side_effect=fake_run), \
             patch.object(safe_commit.shutil, "which", side_effect=fake_which):
            safe_commit.run_validation("/tmp/swarm-idx")

        self.assertEqual(
            seen["cmd"],
            ["bash", "tools/check.sh", "--quick", "--index-file", "/tmp/swarm-idx"],
        )
        self.assertEqual(seen["env"]["GIT_INDEX_FILE"], "/tmp/swarm-idx")

    def test_rebuild_main_index_skips_when_lock_exists(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            git_dir = root / ".git"
            git_dir.mkdir()
            (git_dir / "index.lock").write_text("busy", encoding="utf-8")

            with patch.object(safe_commit, "ROOT", root), \
                 patch.object(safe_commit, "run") as mocked_run:
                safe_commit.rebuild_main_index()

            mocked_run.assert_not_called()

    def test_rebuild_main_index_uses_atomic_replace(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            git_dir = root / ".git"
            git_dir.mkdir()
            target = git_dir / "index"
            target.write_text("old", encoding="utf-8")

            def fake_run(cmd, **kw):
                Path(kw["env"]["GIT_INDEX_FILE"]).write_text("fresh", encoding="utf-8")
                return ""

            with patch.object(safe_commit, "ROOT", root), \
                 patch.object(safe_commit, "run", side_effect=fake_run):
                safe_commit.rebuild_main_index()

            self.assertEqual(target.read_text(encoding="utf-8"), "fresh")


if __name__ == "__main__":
    unittest.main()

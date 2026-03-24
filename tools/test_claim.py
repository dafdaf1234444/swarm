#!/usr/bin/env python3
"""Regression tests for claim.py session identity handling."""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent))
import claim  # noqa: E402


SCRIPT_PATH = Path(__file__).with_name("claim.py")


class TestSessionIdSelection(unittest.TestCase):
    def test_get_session_id_prefers_explicit_override(self):
        env = {
            "SWARM_SESSION_ID": "manual-session",
            claim.CODEX_THREAD_ENV: "thread-123",
        }
        with mock.patch.dict(os.environ, env, clear=False):
            self.assertEqual(claim.get_session_id(), "manual-session")

    def test_get_session_id_uses_codex_thread_when_available(self):
        env = {claim.CODEX_THREAD_ENV: "thread-123"}
        with mock.patch.dict(os.environ, env, clear=True):
            self.assertEqual(claim.get_session_id(), "codex-thread-123")


class TestCrossProcessClaimRelease(unittest.TestCase):
    def _run(self, cwd: str, *args: str, env: dict[str, str]) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, str(SCRIPT_PATH), *args],
            cwd=cwd,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )

    def test_claim_and_release_share_codex_thread_identity(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            env = {"PATH": os.environ.get("PATH", ""), claim.CODEX_THREAD_ENV: "shared-thread"}

            claimed = self._run(tmpdir, "claim", "demo.txt", env=env)
            released = self._run(tmpdir, "release", "demo.txt", env=env)

            self.assertEqual(claimed.returncode, 0, claimed.stderr)
            self.assertIn("codex-shared-thread", claimed.stdout)
            self.assertEqual(released.returncode, 0, released.stderr)
            self.assertIn("RELEASED: demo.txt by codex-shared-thread", released.stdout)
            self.assertFalse((Path(tmpdir) / "workspace" / "claims" / "demo.txt.claim.json").exists())

    def test_release_still_blocks_other_thread(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            owner_env = {"PATH": os.environ.get("PATH", ""), claim.CODEX_THREAD_ENV: "owner-thread"}
            other_env = {"PATH": os.environ.get("PATH", ""), claim.CODEX_THREAD_ENV: "other-thread"}

            claimed = self._run(tmpdir, "claim", "demo.txt", env=owner_env)
            released = self._run(tmpdir, "release", "demo.txt", env=other_env)

            self.assertEqual(claimed.returncode, 0, claimed.stderr)
            self.assertEqual(released.returncode, 1)
            self.assertIn("WARN: demo.txt is claimed by codex-owner-thread, not codex-other-thread", released.stdout)
            self.assertTrue((Path(tmpdir) / "workspace" / "claims" / "demo.txt.claim.json").exists())


if __name__ == "__main__":
    unittest.main()

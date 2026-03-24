#!/usr/bin/env python3
"""Regression tests for maintenance_health.py startup-path behavior."""

import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent))
import maintenance_health  # noqa: E402


class TestCheckUncommittedWslScoping(unittest.TestCase):
    def test_check_uncommitted_scopes_numstat_to_dirty_paths(self):
        calls = []

        def fake_git(*args):
            calls.append(args)
            if args == ("-c", "core.quotepath=false", "status", "--porcelain"):
                return " M docs/alpha.md\nM  docs/beta.md\n?? scratch.txt\n"
            if args == ("diff", "--numstat", "--ignore-cr-at-eol", "--", "docs/alpha.md", "docs/beta.md"):
                return "1\t1\tdocs/alpha.md\n"
            if args == ("diff", "--cached", "--numstat", "--ignore-cr-at-eol", "--", "docs/alpha.md", "docs/beta.md"):
                return "1\t1\tdocs/beta.md\n"
            return ""

        with mock.patch.object(maintenance_health, "_git", side_effect=fake_git), \
             mock.patch.object(maintenance_health, "_is_wsl_mnt_repo", return_value=True):
            results = maintenance_health.check_uncommitted()

        self.assertEqual(
            calls[1:3],
            [
                ("diff", "--numstat", "--ignore-cr-at-eol", "--", "docs/alpha.md", "docs/beta.md"),
                ("diff", "--cached", "--numstat", "--ignore-cr-at-eol", "--", "docs/alpha.md", "docs/beta.md"),
            ],
        )
        self.assertTrue(any("tracked file(s) uncommitted" in msg for _, msg in results))
        self.assertTrue(any("untracked file(s)" in msg for _, msg in results))

    def test_check_uncommitted_skips_numstat_for_non_crlf_candidate_statuses(self):
        calls = []

        def fake_git(*args):
            calls.append(args)
            if args == ("-c", "core.quotepath=false", "status", "--porcelain"):
                return "A  docs/new.md\nD  docs/old.md\nR  docs/from.md -> docs/to.md\n"
            return ""

        with mock.patch.object(maintenance_health, "_git", side_effect=fake_git), \
             mock.patch.object(maintenance_health, "_is_wsl_mnt_repo", return_value=True):
            results = maintenance_health.check_uncommitted()

        self.assertEqual(calls, [("-c", "core.quotepath=false", "status", "--porcelain")])
        self.assertEqual(len(results), 1)
        self.assertIn("3 tracked file(s) uncommitted", results[0][1])


if __name__ == "__main__":
    unittest.main()

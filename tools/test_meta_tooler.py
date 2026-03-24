#!/usr/bin/env python3
"""Regression tests for automation reference detection in meta_tooler.py."""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools import meta_tooler


class TestMetaTooler(unittest.TestCase):
    def test_guard_and_transitive_import_tools_not_flagged_unreferenced(self):
        flagged = {finding.tool for finding in meta_tooler.scan_unreferenced()}

        self.assertNotIn("lesson_collision_check", flagged)
        self.assertNotIn("stale_write_check", flagged)
        self.assertNotIn("level_inflation_check", flagged)
        self.assertNotIn("numerical_claim_scanner", flagged)
        self.assertNotIn("false_instrument_check", flagged)
        self.assertNotIn("orient_monitors", flagged)
        self.assertNotIn("citation_amplify", flagged)
        self.assertNotIn("gather_council", flagged)

    def test_still_flags_known_unreferenced_tool(self):
        flagged = {finding.tool for finding in meta_tooler.scan_unreferenced()}

        self.assertIn("add_adjacency", flagged)


if __name__ == "__main__":
    unittest.main()

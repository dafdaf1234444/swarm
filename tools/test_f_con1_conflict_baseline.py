#!/usr/bin/env python3
"""Regression checks for the F-CON1 strict-baseline classifier."""

import unittest

from f_con1_conflict_baseline import LaneRow, classify_abandonment, is_strict_c1


class StrictC1Tests(unittest.TestCase):
    def test_detects_concurrent_preemption(self):
        row = LaneRow(
            lane_id="DOMEX-TEST-S500",
            session=500,
            status="MERGED",
            etc="diff=Concurrent session preempted lesson write",
            note="Completed after concurrent absorption",
        )
        self.assertTrue(is_strict_c1(row))
        self.assertEqual(classify_abandonment(row), "strict_c1_concurrent_duplicate")

    def test_excludes_generic_evolutionary_supersession(self):
        row = LaneRow(
            lane_id="DOMEX-TEST-S501",
            session=501,
            status="SUPERSEDED",
            etc="",
            note="Superseded by swarm evolution after frontier re-scope",
        )
        self.assertFalse(is_strict_c1(row))
        self.assertEqual(classify_abandonment(row), "evolutionary_supersession")

    def test_classifies_stale_no_progress(self):
        row = LaneRow(
            lane_id="DOMEX-TEST-S502",
            session=502,
            status="ABANDONED",
            etc="",
            note="Stale >3 sessions; no execution occurred",
        )
        self.assertEqual(classify_abandonment(row), "stale_no_progress")


if __name__ == "__main__":
    unittest.main()

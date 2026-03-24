#!/usr/bin/env python3
"""Regression tests for hurst_estimate.py."""

import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import hurst_estimate  # noqa: E402


class TestHurstEstimate(unittest.TestCase):
    def test_project_series_keeps_lesson_order_by_default(self):
        rows = [
            {"lesson": "L-1", "session": 1, "value": 4.0},
            {"lesson": "L-2", "session": 1, "value": 6.0},
            {"lesson": "L-3", "session": 2, "value": 9.0},
        ]
        projected = hurst_estimate.project_series(rows)
        self.assertEqual(projected["aggregation"], {"mode": "lesson", "agg": "none"})
        self.assertEqual(projected["values"], [4.0, 6.0, 9.0])
        self.assertEqual(projected["bounds"]["first_lesson"], "L-1")
        self.assertEqual(projected["bounds"]["last_lesson"], "L-3")

    def test_project_series_aggregates_by_session(self):
        rows = [
            {"lesson": "L-1", "session": 1, "value": 4.0},
            {"lesson": "L-2", "session": 1, "value": 6.0},
            {"lesson": "L-3", "session": 2, "value": 9.0},
            {"lesson": "L-4", "session": None, "value": 12.0},
        ]
        projected = hurst_estimate.project_series(rows, aggregate="session", agg="mean")
        self.assertEqual(projected["aggregation"], {"mode": "session", "agg": "mean"})
        self.assertEqual(projected["values"], [5.0, 9.0])
        self.assertEqual(projected["bounds"]["first_session"], 1)
        self.assertEqual(projected["bounds"]["last_session"], 2)
        self.assertEqual(projected["bounds"]["dropped_without_session"], 1)

    def test_white_noise_stays_near_half(self):
        rng = random.Random(0)
        series = [rng.gauss(0.0, 1.0) for _ in range(2048)]
        hrs = hurst_estimate.hurst_rs(series)
        hdfa = hurst_estimate.hurst_dfa(series)
        self.assertGreater(hrs, 0.4)
        self.assertLess(hrs, 0.65)
        self.assertGreater(hdfa, 0.4)
        self.assertLess(hdfa, 0.65)

    def test_ar1_plateau_ratio_stays_small(self):
        series = hurst_estimate.simulate_ar1(
            n=2048,
            mean=0.0,
            variance=1.0,
            phi=0.4,
            seed=7,
        )
        ratio = hurst_estimate.acf_plateau_ratio(hurst_estimate.acf_profile(series, max_lag=10))
        self.assertLess(ratio, 0.25)


if __name__ == "__main__":
    unittest.main()

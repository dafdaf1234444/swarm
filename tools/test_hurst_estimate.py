#!/usr/bin/env python3
"""Regression tests for hurst_estimate.py."""

import random
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import hurst_estimate  # noqa: E402


class TestHurstEstimate(unittest.TestCase):
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

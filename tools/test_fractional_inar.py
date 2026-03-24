#!/usr/bin/env python3
"""Regression tests for fractional_inar.py."""

import sys
import unittest
from pathlib import Path

try:
    import numpy as np
    sys.path.insert(0, str(Path(__file__).parent))
    import fractional_inar as fi  # noqa: E402
    HAS_DEPS = True
except ImportError:
    HAS_DEPS = False


@unittest.skipUnless(HAS_DEPS, "numpy/scipy not installed")
class TestFractionalWeights(unittest.TestCase):
    def test_weights_sum_below_one(self):
        for d in [0.1, 0.2, 0.3, 0.4, 0.49]:
            w = fi.fractional_weights(d, 50)
            self.assertLess(np.sum(w), 1.0, f"d={d} weights sum >= 1")

    def test_weights_positive(self):
        w = fi.fractional_weights(0.3, 20)
        self.assertTrue(np.all(w >= 0), "negative weights found")

    def test_weights_decreasing(self):
        w = fi.fractional_weights(0.3, 20)
        for i in range(1, len(w)):
            self.assertLessEqual(w[i], w[i - 1], f"weight {i} > weight {i-1}")


@unittest.skipUnless(HAS_DEPS, "numpy/scipy not installed")
class TestSimulations(unittest.TestCase):
    def test_inar1_produces_nonnegative(self):
        sim = fi.simulate_inar1(100, 0.5, 3.0, seed=42)
        self.assertTrue(np.all(sim >= 0))
        self.assertEqual(len(sim), 100)

    def test_finar_bounded_respects_bounds(self):
        sim = fi.simulate_finar(100, 0.3, 2.0, 20, seed=42, lo=5, hi=10)
        self.assertTrue(np.all(sim >= 5))
        self.assertTrue(np.all(sim <= 10))

    def test_finar_unbounded_runs(self):
        sim = fi.simulate_finar(100, 0.3, 2.0, 20, seed=42)
        self.assertEqual(len(sim), 100)
        self.assertTrue(np.all(np.isfinite(sim)))


@unittest.skipUnless(HAS_DEPS, "numpy/scipy not installed")
class TestACF(unittest.TestCase):
    def test_iid_acf_near_zero(self):
        rng = np.random.RandomState(123)
        series = rng.normal(size=1000)
        a = fi.acf(series, 10)
        self.assertTrue(np.all(np.abs(a) < 0.1))

    def test_plateau_ratio_smoke(self):
        profile = np.array([1.0, 0.9, 0.85, 0.8, 0.78, 0.75, 0.73, 0.71, 0.70, 0.68])
        ratio = fi.plateau_ratio(profile)
        self.assertGreater(ratio, 0.5)


if __name__ == "__main__":
    unittest.main()

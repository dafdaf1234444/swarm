#!/usr/bin/env python3
"""Regression tests for bounded_fou.py."""

import sys
import unittest
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
import bounded_fou  # noqa: E402


class TestBoundedFou(unittest.TestCase):
    def test_empirical_rank_map_preserves_support(self):
        observed = np.array([0.0, 1.0, 1.0, 5.0, 9.0, 9.0])
        latent = np.array([0.2, -1.0, 0.5, 2.0, 1.0, 0.0])

        mapped = bounded_fou.empirical_rank_map(latent, observed)

        self.assertListEqual(sorted(mapped.tolist()), sorted(observed.tolist()))

    def test_simulate_fou_latent_is_finite_and_centered(self):
        latent = bounded_fou.simulate_fou_latent(64, 0.75, 1.2, 1.0, seed=123)

        self.assertEqual(len(latent), 64)
        self.assertTrue(np.isfinite(latent).all())
        self.assertAlmostEqual(float(np.mean(latent)), 0.0, places=6)

    def test_plateau_ratio_smoke(self):
        profile = np.array([1.0, 0.8, 0.7, 0.6, 0.55, 0.5, 0.45, 0.4, 0.35, 0.3])

        ratio = bounded_fou.plateau_ratio(profile)

        self.assertGreater(ratio, 0.0)


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Unit tests for spawn_math utility functions."""

import math
import sys
import tempfile
import unittest
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import spawn_math


class TestSpawnMath(unittest.TestCase):
    def test_std_factor_matches_sqrt_inverse_n_when_rho_zero(self):
        self.assertAlmostEqual(spawn_math.std_factor(3, 0.0), 1 / math.sqrt(3), places=6)

    def test_std_factor_is_one_when_rho_one(self):
        self.assertAlmostEqual(spawn_math.std_factor(3, 1.0), 1.0, places=6)

    def test_recommendation_prefers_single_agent_when_fully_correlated(self):
        report = spawn_math.build_report(
            baseline_quality=0.65,
            baseline_std=0.20,
            rho=1.0,
            coordination_cost=0.03,
            risk_aversion=1.0,
            n_max=6,
            p119_threshold=0.45,
        )
        self.assertEqual(report["recommendation"]["best_n"], 1)
        self.assertFalse(report["recommendation"]["spawn"])

    def test_recommendation_prefers_multi_agent_with_low_correlation_and_low_cost(self):
        report = spawn_math.build_report(
            baseline_quality=0.65,
            baseline_std=0.20,
            rho=0.0,
            coordination_cost=0.01,
            risk_aversion=1.0,
            n_max=6,
            p119_threshold=0.45,
        )
        self.assertGreater(report["recommendation"]["best_n"], 1)
        self.assertTrue(report["recommendation"]["spawn"])

    def test_calibration_from_ai2_artifacts(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            p = Path(tmpdir) / "ai2.json"
            p.write_text(
                json.dumps(
                    {
                        "trials": 200,
                        "leader_error_rate": 0.35,
                        "async": {
                            "follower_error_rate": 0.345,
                            "leader_follower_error_correlation": -0.0254,
                        },
                    }
                ),
                encoding="utf-8",
            )
            cal = spawn_math.calibrate_from_ai2_artifacts([p], coordination_cost_floor=0.01)
            self.assertEqual(cal["artifact_count"], 1)
            self.assertAlmostEqual(cal["inferred_baseline_quality"], 0.655, places=6)
            self.assertAlmostEqual(cal["inferred_rho"], 0.0254, places=6)
            self.assertGreaterEqual(cal["inferred_coordination_cost"], 0.01)


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""Regression tests for soul_trajectory.py."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import soul_trajectory  # noqa: E402


class TestHealthParsing(unittest.TestCase):
    def test_parse_health_checkpoints_extracts_ratio_rows(self):
        sample = """
## S514 Health Check | 2026-03-23

| Metric | Value | Rating | Notes |
|--------|-------|--------|-------|
| Knowledge accuracy | PCI=0.905. Benefit ratio 2.18x CI [1.8, 2.65]. | 4/5 | STRONG. |

## S517 Health Check | 2026-03-23

| Metric | Value | Rating | Notes |
|--------|-------|--------|-------|
| Knowledge accuracy | PCI=0.724. Benefit ratio 2.01x CI [1.68, 2.45]. | 3/5 | WATCH. |
"""
        checkpoints = soul_trajectory.parse_health_checkpoints(sample)
        self.assertEqual(
            [(checkpoint.session, checkpoint.ratio) for checkpoint in checkpoints],
            [(514, 2.18), (517, 2.01)],
        )


class TestIncrementExpansion(unittest.TestCase):
    def test_expand_per_session_increments_respects_gaps(self):
        checkpoints = [
            soul_trajectory.Checkpoint(508, 1.92, "experiment-structured"),
            soul_trajectory.Checkpoint(510, 2.02, "health"),
            soul_trajectory.Checkpoint(511, 2.07, "health"),
        ]
        increments = soul_trajectory.expand_per_session_increments(checkpoints)
        self.assertEqual(len(increments), 3)
        for increment in increments:
            self.assertAlmostEqual(increment, 0.05)


class TestFirstPassage(unittest.TestCase):
    def test_deterministic_hit_session_returns_expected_target(self):
        hit = soul_trajectory.deterministic_hit_session(
            current_session=529,
            current_ratio=2.1,
            slope_per_session=0.1,
            target_ratio=2.4,
        )
        self.assertEqual(hit, 532)

    def test_simulate_first_passage_hits_with_deterministic_increments(self):
        result = soul_trajectory.simulate_first_passage(
            current_session=529,
            current_ratio=2.1,
            increments=[0.1],
            target_ratio=2.4,
            check_sessions=[531, 532],
            max_horizon=10,
            simulations=100,
            seed=7,
        )
        self.assertEqual(result["hit_probabilities"]["531"], 0.0)
        self.assertEqual(result["hit_probabilities"]["532"], 1.0)
        self.assertEqual(result["median_hit_session"], 532)


if __name__ == "__main__":
    unittest.main()

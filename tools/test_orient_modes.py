#!/usr/bin/env python3
"""Focused regressions for orient runtime modes."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import orient


class TestOrientFuturePlanning(unittest.TestCase):
    def test_full_mode_includes_full_analysis_futures(self):
        planned = orient._planned_future_keys(coord=False, fast=False)
        self.assertTrue(orient.FULL_ANALYSIS_FUTURES.issubset(planned))

    def test_coord_mode_skips_full_analysis_futures(self):
        planned = orient._planned_future_keys(coord=True, fast=False)
        self.assertTrue(orient.FULL_ANALYSIS_FUTURES.isdisjoint(planned))

    def test_fast_mode_skips_full_analysis_futures(self):
        planned = orient._planned_future_keys(coord=False, fast=True)
        self.assertTrue(orient.FULL_ANALYSIS_FUTURES.isdisjoint(planned))


if __name__ == "__main__":
    unittest.main()

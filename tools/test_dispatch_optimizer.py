#!/usr/bin/env python3
"""Regression tests for dispatch_optimizer collision filtering."""

import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools import dispatch_optimizer


class TestDispatchOptimizer(unittest.TestCase):
    def test_filter_collision_domains_omits_active_lane_domains(self):
        results = [
            {"domain": "ai"},
            {"domain": "meta"},
            {"domain": "physics"},
        ]
        active_lanes = {
            "meta": ["DOMEX-META-S541"],
            "physics": ["DOMEX-PHY-S541"],
        }

        filtered, omitted = dispatch_optimizer._filter_collision_domains(
            results,
            active_lanes,
            enabled=True,
            requested_domain=None,
        )

        self.assertEqual([row["domain"] for row in filtered], ["ai"])
        self.assertEqual(omitted, ["meta", "physics"])

    def test_filter_collision_domains_preserves_requested_domain(self):
        results = [
            {"domain": "meta"},
            {"domain": "physics"},
        ]
        active_lanes = {
            "meta": ["DOMEX-META-S541"],
            "physics": ["DOMEX-PHY-S541"],
        }

        filtered, omitted = dispatch_optimizer._filter_collision_domains(
            results,
            active_lanes,
            enabled=True,
            requested_domain="meta",
        )

        self.assertEqual([row["domain"] for row in filtered], ["meta"])
        self.assertEqual(omitted, ["physics"])

    def test_filter_collision_domains_is_noop_when_disabled(self):
        results = [{"domain": "meta"}, {"domain": "ai"}]
        active_lanes = {"meta": ["DOMEX-META-S541"]}

        filtered, omitted = dispatch_optimizer._filter_collision_domains(
            results,
            active_lanes,
            enabled=False,
            requested_domain=None,
        )

        self.assertEqual(filtered, results)
        self.assertEqual(omitted, [])


if __name__ == "__main__":
    unittest.main()

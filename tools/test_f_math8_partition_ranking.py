#!/usr/bin/env python3
"""Regression tests for F-MATH8 partition ranking."""

import unittest

import f_math8_partition_ranking as ranking


class PartitionRankingTests(unittest.TestCase):
    def setUp(self):
        self.items = [
            {"id": "L-1", "tokens": 100, "citations": 0, "age": 10, "sharpe": 0.0},
            {"id": "L-2", "tokens": 100, "citations": 2, "age": 1, "sharpe": 2.0},
            {"id": "L-3", "tokens": 1200, "citations": 8, "age": 8, "sharpe": 1.0},
            {"id": "L-4", "tokens": 150, "citations": 4, "age": 20, "sharpe": 0.2},
        ]

    def test_z_partition_scores_differ_from_citation_only(self):
        citation_order = [
            item["id"]
            for item in sorted(self.items, key=lambda item: (ranking._score_item(item, "citation_only", 2.0), item["tokens"], item["id"]))
        ]
        z_order = [
            item["id"]
            for item in sorted(self.items, key=lambda item: (ranking._score_item(item, "z_partition", 2.0), item["tokens"], item["id"]))
        ]
        self.assertNotEqual(citation_order, z_order)

    def test_simulate_strategy_respects_token_budget(self):
        result = ranking.simulate_strategy(self.items, "citation_only", 2.0, 0.2)
        self.assertGreaterEqual(result["achieved_compression"], 0.2)
        self.assertGreater(result["removed_count"], 0)

    def test_falsifier_trips_when_z_loses_badly(self):
        comparison = ranking.compare_strategies(self.items, 2.0, 0.3)
        self.assertIn("falsified", comparison)
        self.assertIn("z_partition", comparison["strategies"])


if __name__ == "__main__":
    unittest.main()

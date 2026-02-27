#!/usr/bin/env python3
"""Regression tests for F-IS5 lane distillation scoring."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import f_is5_lane_distill as mod


def _sample_intake() -> dict:
    return {
        "retrieved_count": 6,
        "papers": [
            {
                "arxiv_id": "2602.00001v1",
                "title": "Safety Signals in Multi-Agent Systems",
                "summary_preview": "A reliability benchmark studies trust, fault isolation, and robust coordination under stress.",
            },
            {
                "arxiv_id": "2602.00002v1",
                "title": "Agent Memory Surfaces",
                "summary_preview": "We propose a memory substrate for long-horizon context management in agents.",
            },
            {
                "arxiv_id": "2602.00003v1",
                "title": "Tool-use Orchestration",
                "summary_preview": "Agentic execution improves when workflows can adapt and schedule tool calls.",
            },
            {
                "arxiv_id": "2602.10001v1",
                "title": "Backlog Safety Study",
                "summary_preview": "Safety backlog paper.",
            },
            {
                "arxiv_id": "2602.10002v1",
                "title": "Backlog Memory Study",
                "summary_preview": "Memory backlog paper.",
            },
            {
                "arxiv_id": "2602.10003v1",
                "title": "Backlog Tool Study",
                "summary_preview": "Tool-use backlog paper.",
            },
        ],
        "lane_plan": [
            {
                "lane_id": "ARX-01",
                "theme": "safety-reliability",
                "paper_ids": ["2602.00001v1"],
                "backlog_paper_ids": ["2602.10001v1"],
            },
            {
                "lane_id": "ARX-02",
                "theme": "memory-knowledge",
                "paper_ids": ["2602.00002v1"],
                "backlog_paper_ids": ["2602.10002v1"],
            },
            {
                "lane_id": "ARX-03",
                "theme": "tool-use-execution",
                "paper_ids": ["2602.00003v1"],
                "backlog_paper_ids": ["2602.10003v1"],
            },
        ],
    }


class TestFIS5LaneDistill(unittest.TestCase):
    def test_distill_pass_produces_claims(self):
        claims = mod.distill_pass(
            intake=_sample_intake(),
            owner="lane-owner-A",
            source="selected",
            seed=10,
            per_lane=1,
            active_targets={"F119", "F-IS3", "F111", "PHIL-13", "P-152", "F120"},
        )
        self.assertEqual(len(claims), 3)
        self.assertEqual(claims[0].owner, "lane-owner-A")
        self.assertEqual(claims[0].source_set, "selected")
        self.assertTrue(claims[0].claim_id.startswith("lane-owner-A"))
        self.assertGreaterEqual(len(claims[0].transfer_decisions), 1)

    def test_summarize_claims_counts_duplicates(self):
        intake = _sample_intake()
        claims_a = mod.distill_pass(
            intake=intake,
            owner="lane-owner-A",
            source="selected",
            seed=1,
            per_lane=1,
            active_targets={"F119", "F-IS3", "F111", "PHIL-13", "P-152", "F120"},
        )
        claims_b = mod.distill_pass(
            intake=intake,
            owner="lane-owner-A",
            source="selected",
            seed=1,
            per_lane=1,
            active_targets={"F119", "F-IS3", "F111", "PHIL-13", "P-152", "F120"},
        )
        summary = mod.summarize_claims(claims_a + claims_b, {"F119", "F-IS3"})
        self.assertGreater(summary["duplicate_claim_count"], 0)

    def test_transfer_acceptance_scored(self):
        claim_a = mod.Claim(
            claim_id="A|selected|ARX-01|2602.00001v1",
            owner="lane-owner-A",
            source_set="selected",
            lane_id="ARX-01",
            paper_id="2602.00001v1",
            theme="safety-reliability",
            claim_text="owner A claim",
            transfer_decisions=(
                mod.TransferDecision(
                    target="F119", decision="accepted", rationale="owner-vote-pass"
                ),
            ),
        )
        claim_b = mod.Claim(
            claim_id="B|selected|ARX-01|2602.00001v1",
            owner="lane-owner-B",
            source_set="selected",
            lane_id="ARX-01",
            paper_id="2602.00001v1",
            theme="safety-reliability",
            claim_text="owner B claim",
            transfer_decisions=(
                mod.TransferDecision(
                    target="F119", decision="accepted", rationale="owner-vote-pass"
                ),
            ),
        )
        summary = mod.summarize_claims([claim_a, claim_b], {"F119"})
        self.assertEqual(summary["transfer_accepted"], 1)
        self.assertEqual(summary["merge_collision_count"], 0)

    def test_backlog_source_uses_backlog_ids(self):
        claims = mod.distill_pass(
            intake=_sample_intake(),
            owner="lane-owner-B",
            source="backlog",
            seed=2,
            per_lane=1,
            active_targets={"F119", "F-IS3", "F111", "PHIL-13", "P-152", "F120"},
        )
        paper_ids = {claim.paper_id for claim in claims}
        self.assertEqual(paper_ids, {"2602.10001v1", "2602.10002v1", "2602.10003v1"})
        self.assertTrue(all(claim.source_set == "backlog" for claim in claims))

    def test_merge_collision_requires_decision_disagreement(self):
        claim_a = mod.Claim(
            claim_id="A|selected|ARX-02|2602.00002v1",
            owner="lane-owner-A",
            source_set="selected",
            lane_id="ARX-02",
            paper_id="2602.00002v1",
            theme="evaluation-scaling",
            claim_text="owner A claim",
            transfer_decisions=(
                mod.TransferDecision(
                    target="F-FIN1", decision="accepted", rationale="owner-vote-pass"
                ),
            ),
        )
        claim_b = mod.Claim(
            claim_id="B|selected|ARX-02|2602.00002v1",
            owner="lane-owner-B",
            source_set="selected",
            lane_id="ARX-02",
            paper_id="2602.00002v1",
            theme="evaluation-scaling",
            claim_text="owner B claim",
            transfer_decisions=(
                mod.TransferDecision(
                    target="F-FIN1", decision="rejected", rationale="owner-vote-fail"
                ),
            ),
        )
        summary = mod.summarize_claims([claim_a, claim_b], {"F-FIN1"})
        self.assertEqual(summary["transfer_accepted"], 0)
        self.assertEqual(summary["merge_collision_count"], 1)


if __name__ == "__main__":
    unittest.main()

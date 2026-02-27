#!/usr/bin/env python3
"""Regression tests for F-STAT1 reporting-quality baseline."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import f_stat1_reporting_quality as mod


class TestFStat1ReportingQuality(unittest.TestCase):
    def test_latest_active_lanes_uses_latest_row_state(self):
        text = "\n".join(
            [
                "| Date | Lane | Session | Agent | Branch | PR | Model | Platform | Scope-Key | Etc | Status | Notes |",
                "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
                "| 2026-02-27 | L-1 | S186 | codex | b1 | - | GPT-5 | codex-cli | tools/x.py | setup=a focus=global | ACTIVE | work |",
                "| 2026-02-27 | L-1 | S186 | codex | b1 | - | GPT-5 | codex-cli | tools/x.py | setup=a focus=global | MERGED | done |",
                "| 2026-02-27 | L-2 | S186 | codex | b2 | - | GPT-5 | codex-cli | tools/y.py | setup=a focus=global | READY | queued |",
            ]
        )
        rows = mod.parse_lane_rows(text)
        active = mod.latest_active_lanes(rows)
        self.assertEqual(len(active), 1)
        self.assertEqual(active[0]["lane"], "L-2")

    def test_detect_fields_accepts_explicit_none_for_blocked_and_human(self):
        row = {
            "lane": "L-X",
            "status": "READY",
            "session": "S186",
            "model": "GPT-5",
            "platform": "codex-cli",
            "scope_key": "tasks/SWARM-LANES.md",
            "etc": (
                "setup=codex focus=global intent=baseline available=yes blocked=none "
                "next_step=run human_open_item=none"
            ),
            "notes": "Queued run for reporting quality baseline.",
        }
        fields = mod.detect_reporting_fields(row)
        explicit = mod.detect_explicit_reporting_fields(row)
        self.assertTrue(all(fields.values()), fields)
        self.assertFalse(explicit["progress"])
        self.assertAlmostEqual(mod.reporting_score(fields), 1.0, places=4)
        self.assertAlmostEqual(mod.reporting_score(explicit), 0.85, places=4)

    def test_missing_blocked_and_human_fields_reduce_score(self):
        row = {
            "lane": "L-Y",
            "status": "READY",
            "session": "S186",
            "model": "GPT-5",
            "platform": "codex-cli",
            "scope_key": "domains/statistics/tasks/FRONTIER.md",
            "etc": "setup=codex focus=global frontier=F-STAT1 dispatch=domain-expert",
            "notes": "Domain lane queued: run baseline measurement.",
        }
        fields = mod.detect_reporting_fields(row)
        explicit = mod.detect_explicit_reporting_fields(row)
        self.assertFalse(fields["blocked"])
        self.assertFalse(fields["human_open_item"])
        self.assertFalse(explicit["blocked"])
        self.assertFalse(explicit["human_open_item"])
        self.assertAlmostEqual(mod.reporting_score(fields), 0.8, places=4)
        self.assertAlmostEqual(mod.reporting_score(explicit), 0.4, places=4)

    def test_build_report_computes_key_coverage(self):
        full = {
            "lane": "L-FULL",
            "status": "ACTIVE",
            "session": "S186",
            "model": "GPT-5",
            "platform": "codex-cli",
            "scope_key": "a",
            "etc": "setup=codex focus=global intent=x available=yes blocked=none next_step=run human_open_item=none",
            "notes": "Ready and executing.",
        }
        partial = {
            "lane": "L-PART",
            "status": "READY",
            "session": "S186",
            "model": "GPT-5",
            "platform": "codex-cli",
            "scope_key": "b",
            "etc": "setup=codex focus=global frontier=F-STAT1",
            "notes": "Queued run.",
        }
        report = mod.build_report([full, partial])
        self.assertEqual(report["lane_count"], 2)
        self.assertAlmostEqual(report["key_coverage"]["blocked"], 0.5, places=4)
        self.assertAlmostEqual(report["key_coverage"]["human_open_item"], 0.5, places=4)
        self.assertEqual(report["lowest_coverage_keys"][0], "blocked")
        self.assertAlmostEqual(report["explicit_key_coverage"]["progress"], 0.0, places=4)
        self.assertAlmostEqual(report["explicit_contract_ready_rate"], 0.0, places=4)


if __name__ == "__main__":
    unittest.main()

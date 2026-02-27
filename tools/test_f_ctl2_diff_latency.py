#!/usr/bin/env python3
"""Regression tests for F-CTL2 diff-latency baseline tool."""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import f_ctl2_diff_latency as mod


class TestFCTL2DiffLatency(unittest.TestCase):
    def test_diff_event_requires_expectation_and_large_diff(self):
        self.assertTrue(mod.is_diff_event("[S186] Expect-next prediction + diff logged, drift observed"))
        self.assertFalse(mod.is_diff_event("[S186] drift observed in session notes"))
        self.assertFalse(mod.is_diff_event("[S186] expect-next added during routine update"))

    def test_anchor_extraction_and_overlap(self):
        text = "[S186] F123 diff event for F-CTL2 with L-244 and P-182"
        anchors = mod.extract_anchors(text)
        self.assertIn("F123", anchors)
        self.assertIn("F-CTL2", anchors)
        self.assertIn("L-244", anchors)
        self.assertIn("P-182", anchors)

    def test_measure_latency_prefers_anchor_match(self):
        rows = [
            {
                "session": 180,
                "text": "[S180] expect-next drift on F-CTL2",
                "anchors": ["F-CTL2"],
                "is_diff_event": True,
                "is_correction_event": False,
            },
            {
                "session": 181,
                "text": "[S181] fixed unrelated F-FOO",
                "anchors": ["F-FOO"],
                "is_diff_event": False,
                "is_correction_event": True,
            },
            {
                "session": 182,
                "text": "[S182] corrected F-CTL2 detector settings",
                "anchors": ["F-CTL2"],
                "is_diff_event": False,
                "is_correction_event": True,
            },
        ]
        events = mod.measure_latency(rows)
        self.assertEqual(len(events), 1)
        self.assertEqual(events[0]["matched_correction_session"], 182)
        self.assertEqual(events[0]["lag_sessions"], 2)
        self.assertTrue(events[0]["anchor_matched"])

    def test_summarize_handles_unresolved(self):
        events = [
            {"lag_sessions": 1, "anchor_matched": True},
            {"lag_sessions": 3, "anchor_matched": False},
            {"lag_sessions": None, "anchor_matched": False},
        ]
        s = mod.summarize(events)
        self.assertEqual(s["diff_events_total"], 3)
        self.assertEqual(s["resolved_events"], 2)
        self.assertEqual(s["unresolved_events"], 1)
        self.assertAlmostEqual(s["mean_lag_sessions"], 2.0, places=4)
        self.assertAlmostEqual(s["p90_lag_sessions"], 3.0, places=4)

    def test_auto_routing_replay(self):
        events = [
            {"lag_sessions": 0},
            {"lag_sessions": 2},
            {"lag_sessions": 4},
            {"lag_sessions": None},
        ]
        replay = mod.simulate_auto_routing(events, route_after_sessions=1)
        self.assertEqual(replay["eligible_events"], 2)
        self.assertLess(replay["projected_mean_lag"], replay["baseline_mean_lag"])


if __name__ == "__main__":
    unittest.main()

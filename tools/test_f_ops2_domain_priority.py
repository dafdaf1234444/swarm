#!/usr/bin/env python3
"""Unit tests for F-OPS2 domain-priority allocator."""

import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
import f_ops2_domain_priority as mod


class TestFOps2DomainPriority(unittest.TestCase):
    def test_updated_session_from_state_header(self):
        text = "# State\nUpdated: 2026-02-27 S186\n"
        self.assertEqual(mod._updated_session_from_state_header(text), 186)

    def test_parse_active_frontiers(self):
        text = """# Example
## Active
- **F-IS3**: one
- **F-IS4**: two
- ~~**F-IS2**~~: resolved
- ~~F-IS1~~: also resolved

## Resolved
- **F-IS2**: old
"""
        self.assertEqual(mod.parse_active_frontiers(text), ["F-IS3", "F-IS4"])

    def test_parse_next_demand_with_priority_weights(self):
        next_text = """# State
## For next session
1. **F-IS3 / F-FIN1** do this.
2. **F-EVO1** do that.
"""
        frontier_map = {"F-IS3": "information-science", "F-FIN1": "finance", "F-EVO1": "evolution"}
        mentions, weights = mod.parse_next_demand(next_text, frontier_map)
        self.assertEqual(mentions["information-science"], 1)
        self.assertEqual(mentions["finance"], 1)
        self.assertEqual(mentions["evolution"], 1)
        self.assertGreater(weights["information-science"], weights["evolution"])
        self.assertGreater(weights["finance"], weights["evolution"])

    def test_parse_findings_demand_prefers_recent_caveated_lines(self):
        next_text = """# State
## What just happened
S186: F-FIN1 rerun completed with caveat: mean remains unstable; next step is extraction hardening.
S186: F-IS5 intake pass resolved lane packing issue.
S185: F-EVO2 baseline merged.
"""
        frontier_map = {"F-FIN1": "finance", "F-IS5": "information-science", "F-EVO2": "evolution"}
        mentions, weights = mod.parse_findings_demand(next_text, frontier_map, max_lines=3)
        self.assertEqual(mentions["finance"], 1)
        self.assertEqual(mentions["information-science"], 1)
        self.assertEqual(mentions["evolution"], 1)
        self.assertGreater(weights["finance"], weights["evolution"])

    def test_parse_active_lane_pressure_prefers_latest_lane_row(self):
        lanes_text = """| Date | Lane | Session | Agent | Branch | PR | Model | Platform | Scope-Key | Etc | Status | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026-02-27 | L-1 | S186 | codex | local | - | GPT-5 | codex-cli | domains/finance/tasks/FRONTIER.md | setup=x,focus=global | ACTIVE | a |
| 2026-02-27 | L-1 | S186 | codex | local | - | GPT-5 | codex-cli | domains/finance/tasks/FRONTIER.md | setup=x,focus=global | MERGED | b |
| 2026-02-27 | L-2 | S186 | codex | local | - | GPT-5 | codex-cli | tools/wiki_swarm.py | setup=x,focus=global,frontier=F-IS3 | READY | c |
"""
        pressure = mod.parse_active_lane_pressure(lanes_text, {"F-IS3": "information-science"})
        # L-1 latest status is MERGED so it should not contribute pressure.
        self.assertNotIn("finance", pressure)
        self.assertEqual(pressure.get("information-science"), 1)

    def test_allocate_agents_gives_more_slots_to_higher_signal_domain(self):
        states = [
            mod.DomainState(
                name="information-science",
                frontier_path="domains/information-science/tasks/FRONTIER.md",
                active_frontiers=["F-IS3", "F-IS4", "F-IS5"],
                updated_session=186,
                age_sessions=0,
                next_mentions=2,
                next_priority_weight=7.0,
                active_lane_pressure=0,
            ),
            mod.DomainState(
                name="finance",
                frontier_path="domains/finance/tasks/FRONTIER.md",
                active_frontiers=["F-FIN1"],
                updated_session=186,
                age_sessions=0,
                next_mentions=0,
                next_priority_weight=0.0,
                active_lane_pressure=0,
            ),
        ]
        alloc = mod.allocate_agents(states, "hybrid", 4)
        self.assertGreater(alloc["information-science"], alloc["finance"])

    def test_load_domain_frontiers_from_temp_tree(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            d = root / "domains" / "demo" / "tasks"
            d.mkdir(parents=True)
            (d / "FRONTIER.md").write_text(
                "# Demo\nUpdated: 2026-02-27 S180 | Active: 1\n\n## Active\n- **F-DEMO1**: x\n",
                encoding="utf-8",
            )
            states, f_map = mod.load_domain_frontiers(root / "domains", current_session=186)
            self.assertEqual(len(states), 1)
            self.assertEqual(states[0].name, "demo")
            self.assertEqual(states[0].age_sessions, 6)
            self.assertEqual(f_map["F-DEMO1"], "demo")


if __name__ == "__main__":
    unittest.main()

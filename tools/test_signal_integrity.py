#!/usr/bin/env python3
"""Regression tests for signal integrity auditing."""

import contextlib
import io
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).parent))
import domain_map  # noqa: E402
import signal_integrity  # noqa: E402
import swarm_signal  # noqa: E402


class TestSignalIntegrityAudit(unittest.TestCase):
    def test_flags_wrong_source_for_human_directive_signal(self):
        human_text = """
## Directive Log (compressed — evidence for Model)

| Session | Key directive | Impact |
|---------|---------------|--------|
| S527 | **"john von neumann for the swarm"** — apply von Neumann frameworks | SIG-105; self-reproducing automata |

---
"""
        signals = [{
            "id": "SIG-105",
            "date": "2026-03-24",
            "session": "S527",
            "source": "ai-session",
            "target": "broadcast",
            "type": "directive",
            "priority": "P2",
            "content": "john von neumann for the swarm",
            "status": "OPEN",
            "resolution": "—",
        }]

        report = signal_integrity.audit_signal_integrity(human_text=human_text, signals=signals)

        self.assertEqual(report["issue_count"], 1)
        self.assertEqual(report["issues"][0]["issue"], "wrong_source")
        self.assertEqual(report["issues"][0]["signal_id"], "SIG-105")

    def test_passes_when_source_and_session_match(self):
        human_text = """
## Directive Log (compressed — evidence for Model)

| Session | Key directive | Impact |
|---------|---------------|--------|
| S528 | **"swarm world order"** — internal constitution + external inter-swarm law | SIG-111; governance for N humans × N swarms |

---
"""
        signals = [{
            "id": "SIG-111",
            "date": "2026-03-24",
            "session": "S528",
            "source": "human",
            "target": "broadcast",
            "type": "directive",
            "priority": "P2",
            "content": "Swarm world order",
            "status": "OPEN",
            "resolution": "—",
        }]

        report = signal_integrity.audit_signal_integrity(human_text=human_text, signals=signals)

        self.assertEqual(report["issue_count"], 0)


class TestPostHumanCommand(unittest.TestCase):
    def test_post_human_writes_human_source(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            signals_path = Path(tmpdir) / "SIGNALS.md"
            with mock.patch.object(swarm_signal, "SIGNALS_FILE", signals_path):
                with mock.patch.object(swarm_signal, "session_number", return_value=532):
                    with mock.patch.object(sys, "argv", [
                        "swarm_signal.py",
                        "post-human",
                        "directive",
                        "swarm if human signals properly recorded",
                    ]):
                        with contextlib.redirect_stdout(io.StringIO()):
                            swarm_signal.main()

            text = signals_path.read_text(encoding="utf-8")
            self.assertIn("| human | broadcast | directive | P2 | swarm if human signals properly recorded | OPEN |", text)


class TestDomainMap(unittest.TestCase):
    def test_hum_lane_maps_to_human_systems(self):
        self.assertEqual(domain_map.resolve_lane_domain("DOMEX-HUM-S532"), "human-systems")


if __name__ == "__main__":
    unittest.main()

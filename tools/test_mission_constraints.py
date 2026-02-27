#!/usr/bin/env python3
"""Regression tests for F119 degraded/offline transition evidence parsing."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

try:
    # Repo-root invocation (e.g., `python3 -m unittest tools/test_mission_constraints.py`).
    from tools import maintenance  # type: ignore
except Exception:
    # tools/ cwd invocation (e.g., `cd tools && python3 test_mission_constraints.py`).
    import maintenance  # type: ignore


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _seed_repo(root: Path, next_body: str) -> None:
    _write(
        root / "tasks/FRONTIER.md",
        "# Frontier\n- **F119**: mission constraints\n",
    )
    _write(root / "tasks/NEXT.md", next_body)
    _write(
        root / "memory/SESSION-LOG.md",
        "S156 | 2026-02-27 | runtime portability fallback with Beliefs PASS\n",
    )
    _write(
        root / "beliefs/INVARIANTS.md",
        "\n".join(
            [
                "## I9 [MC-SAFE]",
                "## I10 [MC-PORT]",
                "## I11 [MC-LEARN]",
                "## I12 [MC-CONN]",
                "",
            ]
        ),
    )
    _write(root / "tools/check.sh", "choose_python() { :; }\npython3\npython\npy -3\n")
    _write(root / "tools/maintenance.sh", "#!/bin/bash\n")
    _write(root / "tools/bulletin.py", "# stub\n")
    _write(root / "tools/merge_back.py", "# stub\n")
    _write(root / "tools/propagate_challenges.py", "# stub\n")
    _write(
        root / "tools/maintenance.py",
        "\n".join(
            [
                "def check_validator(): pass",
                "def check_runtime_portability(): pass",
                "def check_cross_references(): pass",
                "def check_state_header_sync(): pass",
                "def check_session_log_integrity(): pass",
                "def check_child_bulletins(): pass",
                "def check_help_requests(): pass",
                "def check_swarm_lanes(): pass",
                "all_checks = [",
                "    check_validator,",
                "    check_runtime_portability,",
                "    check_cross_references,",
                "    check_state_header_sync,",
                "    check_session_log_integrity,",
                "    check_child_bulletins,",
                "    check_help_requests,",
                "    check_swarm_lanes,",
                "]",
                "",
            ]
        ),
    )


class TestMissionConstraintEvidence(unittest.TestCase):
    def test_requires_reason_action_and_session_anchor(self):
        text = "\n".join(
            [
                "S151: runtime portability discussed only",
                "S152: runtime portability fallback with bash tools/check.sh --quick",
                "runtime portability with bash tools/check.sh --quick (no session anchor)",
            ]
        )
        sessions = maintenance._reason_action_evidence_sessions(
            text,
            reason_patterns=(r"runtime portability",),
            action_patterns=(r"bash tools/check\.sh --quick",),
        )
        self.assertEqual(sessions, [152])

    def test_ignores_lines_missing_action(self):
        text = "S153: runtime portability on PowerShell"
        sessions = maintenance._reason_action_evidence_sessions(
            text,
            reason_patterns=(r"runtime portability",),
            action_patterns=(r"bash tools/check\.sh --quick",),
        )
        self.assertEqual(sessions, [])

    def test_collects_multiple_matching_sessions(self):
        text = "\n".join(
            [
                "S140: inter-swarm continuity via tools/bulletin.py help-queue",
                "S141: inter-swarm continuity via tools/bulletin.py sync child-a",
                "S141: inter-swarm continuity via tools/bulletin.py offer-help H-123 ack",
            ]
        )
        sessions = maintenance._reason_action_evidence_sessions(
            text,
            reason_patterns=(r"inter-swarm",),
            action_patterns=(r"tools/bulletin\.py",),
        )
        self.assertEqual(sessions, [140, 141, 141])

    def test_matches_multiline_session_entry(self):
        text = "\n".join(
            [
                "S155: runtime portability degraded mode",
                "fallback action: bash tools/check.sh --quick",
            ]
        )
        sessions = maintenance._reason_action_evidence_sessions(
            text,
            reason_patterns=(r"runtime portability",),
            action_patterns=(r"bash tools/check\.sh --quick",),
        )
        self.assertEqual(sessions, [155])


class TestSessionLogIntegrityBackfill(unittest.TestCase):
    def _run_check(self, lines: list[str]) -> list[tuple[str, str]]:
        text = "\n".join(lines)
        with patch.object(maintenance, "_read", return_value=text):
            return maintenance.check_session_log_integrity()

    def test_one_step_backfill_is_benign_when_session_already_seen(self):
        results = self._run_check(
            [
                "S151 | baseline",
                "S152 | baseline",
                "S153 | baseline",
                "S154 | baseline",
                "S155 | baseline",
                "S154 | backfill",
            ]
        )
        self.assertFalse(
            any("recent non-monotonic order" in msg for _, msg in results),
            f"Unexpected non-monotonic notice: {results}",
        )

    def test_one_step_backfill_is_benign_when_session_unseen(self):
        results = self._run_check(
            [
                "S151 | baseline",
                "S152 | baseline",
                "S153 | baseline",
                "S155 | baseline",
                "S154 | backfill",
            ]
        )
        self.assertFalse(
            any("recent non-monotonic order" in msg for _, msg in results),
            f"Unexpected non-monotonic notice: {results}",
        )

    def test_multi_step_backfill_is_flagged_when_session_unseen(self):
        results = self._run_check(
            [
                "S151 | baseline",
                "S152 | baseline",
                "S153 | baseline",
                "S156 | baseline",
                "S154 | backfill",
            ]
        )
        self.assertTrue(
            any("recent non-monotonic order" in msg for _, msg in results),
            f"Expected non-monotonic notice, got: {results}",
        )


class TestMissionConstraintDegradedRuntime(unittest.TestCase):
    def _run_check(
        self,
        *,
        next_lines: list[str],
        session_log_lines: list[str],
        session: int,
        python_status: dict[str, bool],
        py_launcher: bool,
        bash_available: bool,
        exists_overrides: dict[str, bool] | None = None,
    ) -> list[tuple[str, str]]:
        frontier_text = "- **F119**: mission constraints"
        invariants_text = "\n".join(
            [
                "## I9 - Mission safety: do no harm [MC-SAFE]",
                "## I10 - Mission portability: work everywhere [MC-PORT]",
                "## I11 - Mission learning quality: improve knowledge continuously [MC-LEARN]",
                "## I12 - Mission continuity: stay connected under constraints [MC-CONN]",
            ]
        )
        check_sh_text = "\n".join(
            [
                "choose_python() {",
                "python3",
                "python",
                "py -3",
                "}",
            ]
        )
        read_map = {
            "tasks/FRONTIER.md": frontier_text,
            "tasks/NEXT.md": "\n".join(next_lines),
            "beliefs/INVARIANTS.md": invariants_text,
            "tools/check.sh": check_sh_text,
            "memory/SESSION-LOG.md": "\n".join(session_log_lines),
        }
        exists_values = {
            "tools/check.sh": True,
            "tools/maintenance.sh": True,
            "tools/bulletin.py": True,
            "tools/merge_back.py": True,
            "tools/propagate_challenges.py": True,
            "tasks/PR-QUEUE.json": True,
            "tasks/SWARM-LANES.md": True,
        }
        if exists_overrides:
            exists_values.update(exists_overrides)

        real_read = maintenance._read

        def fake_read(path):
            try:
                rel = path.relative_to(maintenance.REPO_ROOT).as_posix()
            except Exception:
                rel = str(path).replace("\\", "/")
            return read_map.get(rel, real_read(path))

        def fake_python_command_runs(cmd: str) -> bool:
            return python_status.get(cmd, False)

        def fake_exists(path: str) -> bool:
            return exists_values.get(path, True)

        def fake_command_exists(cmd: str) -> bool:
            if cmd == "bash":
                return bash_available
            return True

        with patch.object(maintenance, "_read", side_effect=fake_read):
            with patch.object(maintenance, "_python_command_runs", side_effect=fake_python_command_runs):
                with patch.object(maintenance, "_py_launcher_runs", return_value=py_launcher):
                    with patch.object(maintenance, "_exists", side_effect=fake_exists):
                        with patch.object(maintenance, "_command_exists", side_effect=fake_command_exists):
                            with patch.object(maintenance, "_session_number", return_value=session):
                                with patch.object(maintenance, "_tracked_changed_paths", return_value=[]):
                                    return maintenance.check_mission_constraints()

    def test_runtime_portability_co_located_transition_is_not_flagged(self):
        lines = [
            "F119 validation pass",
            "S200: runtime portability no runnable python alias; fallback via bash tools/check.sh --quick; Beliefs PASS NOTICE-only",
        ]
        results = self._run_check(
            next_lines=lines,
            session_log_lines=lines,
            session=200,
            python_status={"python3": False, "python": False},
            py_launcher=False,
            bash_available=True,
        )
        messages = [msg for _, msg in results]
        self.assertFalse(any("runtime portability degraded mode lacks reason+action" in m for m in messages))
        self.assertFalse(any("runtime portability degraded mode lacks reason+outcome" in m for m in messages))
        self.assertFalse(any("runtime portability transition evidence is split across sessions" in m for m in messages))
        self.assertFalse(any("runtime portability degraded transition evidence stale" in m for m in messages))

    def test_offline_continuity_co_located_transition_is_not_flagged(self):
        lines = [
            "F119 validation pass",
            "S200: inter-swarm continuity offline queue sync via tasks/PR-QUEUE.json and tasks/SWARM-LANES.md; Beliefs PASS NOTICE-only",
        ]
        results = self._run_check(
            next_lines=lines,
            session_log_lines=lines,
            session=200,
            python_status={"python3": True, "python": False},
            py_launcher=False,
            bash_available=True,
            exists_overrides={
                "tools/bulletin.py": False,
                "tools/merge_back.py": False,
                "tools/propagate_challenges.py": False,
            },
        )
        messages = [msg for _, msg in results]
        self.assertFalse(any("offline/inter-swarm continuity degraded mode lacks reason+action" in m for m in messages))
        self.assertFalse(any("offline/inter-swarm continuity degraded mode lacks reason+outcome" in m for m in messages))
        self.assertFalse(any("offline/inter-swarm continuity transition evidence is split across sessions" in m for m in messages))
        self.assertFalse(any("offline/inter-swarm continuity degraded transition evidence stale" in m for m in messages))

    def test_runtime_portability_split_sessions_are_flagged(self):
        next_lines = [
            "F119 validation pass",
            "S198: runtime portability python alias missing; fallback via bash tools/check.sh --quick",
            "S199: runtime portability python alias missing; Beliefs PASS NOTICE-only",
        ]
        results = self._run_check(
            next_lines=next_lines,
            session_log_lines=["S199: runtime portability python alias missing; Beliefs PASS NOTICE-only"],
            session=200,
            python_status={"python3": False, "python": False},
            py_launcher=False,
            bash_available=True,
        )
        messages = [msg for _, msg in results]
        self.assertTrue(any("runtime portability transition evidence is split across sessions" in m for m in messages))

    def test_offline_continuity_split_sessions_are_flagged(self):
        next_lines = [
            "F119 validation pass",
            "S198: inter-swarm continuity offline queue sync via tasks/PR-QUEUE.json and tasks/SWARM-LANES.md",
            "S199: inter-swarm continuity offline mode; Beliefs PASS NOTICE-only",
        ]
        results = self._run_check(
            next_lines=next_lines,
            session_log_lines=["S199: inter-swarm continuity offline mode; Beliefs PASS NOTICE-only"],
            session=200,
            python_status={"python3": True, "python": False},
            py_launcher=False,
            bash_available=True,
            exists_overrides={
                "tools/bulletin.py": False,
                "tools/merge_back.py": False,
                "tools/propagate_challenges.py": False,
            },
        )
        messages = [msg for _, msg in results]
        self.assertTrue(any("offline/inter-swarm continuity transition evidence is split across sessions" in m for m in messages))

    def test_runtime_portability_without_fallback_is_due(self):
        lines = [
            "F119 validation pass",
            "S200: runtime portability python alias missing in powershell",
        ]
        results = self._run_check(
            next_lines=lines,
            session_log_lines=lines,
            session=200,
            python_status={"python3": False, "python": False},
            py_launcher=False,
            bash_available=False,
            exists_overrides={
                "tools/check.sh": False,
                "tools/maintenance.sh": False,
            },
        )
        self.assertTrue(any("degraded runtime continuity broken" in msg for _, msg in results))

    def test_powershell_only_line_is_not_transition_evidence(self):
        lines = [
            "F119 validation pass",
            "S200: powershell path fallback via bash tools/check.sh --quick; Beliefs PASS NOTICE-only",
        ]
        results = self._run_check(
            next_lines=lines,
            session_log_lines=lines,
            session=200,
            python_status={"python3": False, "python": False},
            py_launcher=False,
            bash_available=True,
        )
        messages = [msg for _, msg in results]
        self.assertTrue(any("runtime portability degraded mode lacks reason+action transition evidence" in m for m in messages))

    def test_offline_artifacts_missing_is_due(self):
        lines = [
            "F119 validation pass",
            "S200: inter-swarm continuity offline queue sync via tasks/PR-QUEUE.json; Beliefs PASS NOTICE-only",
        ]
        results = self._run_check(
            next_lines=lines,
            session_log_lines=lines,
            session=200,
            python_status={"python3": True, "python": False},
            py_launcher=False,
            bash_available=True,
            exists_overrides={
                "tools/bulletin.py": False,
                "tools/merge_back.py": False,
                "tools/propagate_challenges.py": False,
                "tasks/PR-QUEUE.json": False,
                "tasks/SWARM-LANES.md": False,
            },
        )
        self.assertTrue(any("offline continuity artifacts missing" in msg for _, msg in results))

    def test_runtime_portability_stale_transition_is_flagged(self):
        lines = [
            "F119 validation pass",
            "S200: runtime portability no runnable python alias; fallback via bash tools/check.sh --quick; Beliefs PASS NOTICE-only",
        ]
        results = self._run_check(
            next_lines=lines,
            session_log_lines=lines,
            session=210,
            python_status={"python3": False, "python": False},
            py_launcher=False,
            bash_available=True,
        )
        self.assertTrue(any("runtime portability degraded transition evidence stale" in msg for _, msg in results))

    def test_offline_continuity_stale_transition_is_flagged(self):
        lines = [
            "F119 validation pass",
            "S200: inter-swarm continuity offline queue sync via tasks/PR-QUEUE.json and tasks/SWARM-LANES.md; Beliefs PASS NOTICE-only",
        ]
        results = self._run_check(
            next_lines=lines,
            session_log_lines=lines,
            session=210,
            python_status={"python3": True, "python": False},
            py_launcher=False,
            bash_available=True,
            exists_overrides={
                "tools/bulletin.py": False,
                "tools/merge_back.py": False,
                "tools/propagate_challenges.py": False,
            },
        )
        self.assertTrue(any("offline/inter-swarm continuity degraded transition evidence stale" in msg for _, msg in results))


if __name__ == "__main__":
    unittest.main()

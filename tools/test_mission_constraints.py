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
    _write(root / "tools/check.ps1", "# powershell check wrapper\n")
    _write(root / "tools/maintenance.ps1", "# powershell maintenance wrapper\n")
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

    def test_control_character_is_flagged(self):
        line = "S161 | runtime recheck (" + chr(8) + "ash tools/check.sh --quick)"
        results = self._run_check(
            [
                line,
            ]
        )
        self.assertTrue(
            any("contains control character" in msg for _, msg in results),
            f"Expected control-character notice, got: {results}",
        )


class TestSwarmLaneCoordinationSignals(unittest.TestCase):
    def _run_check(self, lanes_text: str) -> list[tuple[str, str]]:
        with patch.object(maintenance, "_read", return_value=lanes_text):
            return maintenance.check_swarm_lanes()

    def test_active_lane_missing_setup_focus_is_noticed(self):
        lanes_text = "\n".join(
            [
                "| Date | Lane | Session | Agent | Branch | PR | Model | Platform | Scope-Key | Etc | Status | Notes |",
                "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
                "| 2026-02-27 | LANE-1 | S200 | codex | feature/a | - | gpt-5 | windows | tools/maintenance.py | runtime=wsl | ACTIVE | work |",
            ]
        )
        results = self._run_check(lanes_text)
        self.assertTrue(any("missing setup/focus tags in Etc" in msg for _, msg in results))

    def test_multi_setup_without_global_focus_is_noticed(self):
        lanes_text = "\n".join(
            [
                "| Date | Lane | Session | Agent | Branch | PR | Model | Platform | Scope-Key | Etc | Status | Notes |",
                "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
                "| 2026-02-27 | LANE-1 | S200 | codex | feature/a | - | gpt-5 | windows | tools/maintenance.py | setup=windows focus=parser | ACTIVE | work |",
                "| 2026-02-27 | LANE-2 | S200 | copilot | feature/b | - | gpt-5 | wsl | tasks/SWARM-LANES.md | setup=wsl focus=parser | READY | work |",
            ]
        )
        results = self._run_check(lanes_text)
        self.assertTrue(any("no global coordination focus" in msg for _, msg in results))

    def test_multi_setup_with_global_focus_is_not_flagged(self):
        lanes_text = "\n".join(
            [
                "| Date | Lane | Session | Agent | Branch | PR | Model | Platform | Scope-Key | Etc | Status | Notes |",
                "| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |",
                "| 2026-02-27 | LANE-1 | S200 | codex | feature/a | - | gpt-5 | windows | tools/maintenance.py | setup=windows focus=parser | ACTIVE | work |",
                "| 2026-02-27 | LANE-2 | S200 | copilot | feature/b | - | gpt-5 | wsl | tasks/SWARM-LANES.md | setup=wsl focus=global | READY | work |",
            ]
        )
        results = self._run_check(lanes_text)
        self.assertFalse(any("no global coordination focus" in msg for _, msg in results))


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
        pwsh_available: bool = False,
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
            "tools/check.ps1": True,
            "tools/maintenance.ps1": True,
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
            if cmd in {"pwsh", "powershell"}:
                return pwsh_available
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

    def test_runtime_portability_pwsh_wrapper_path_counts_as_fallback(self):
        lines = [
            "F119 validation pass",
            "S200: runtime portability no runnable python alias; fallback via pwsh -NoProfile -File tools/check.ps1 --quick; Beliefs PASS NOTICE-only",
        ]
        results = self._run_check(
            next_lines=lines,
            session_log_lines=lines,
            session=200,
            python_status={"python3": False, "python": False},
            py_launcher=False,
            bash_available=False,
            pwsh_available=True,
            exists_overrides={
                "tools/check.sh": False,
                "tools/maintenance.sh": False,
                "tools/check.ps1": True,
                "tools/maintenance.ps1": True,
            },
        )
        messages = [msg for _, msg in results]
        self.assertFalse(any("degraded runtime continuity broken" in m for m in messages))
        self.assertFalse(any("runtime portability degraded mode lacks reason+action transition evidence" in m for m in messages))

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

    def test_runtime_portability_stale_transition_is_flagged_with_recent_reason_signal(self):
        lines = [
            "F119 validation pass",
            "S200: runtime portability no runnable python alias; fallback via bash tools/check.sh --quick; Beliefs PASS NOTICE-only",
        ]
        results = self._run_check(
            next_lines=lines,
            session_log_lines=lines + ["S212: runtime portability python alias still missing on this host"],
            session=213,
            python_status={"python3": False, "python": False},
            py_launcher=False,
            bash_available=True,
        )
        stale_msgs = [msg for _, msg in results if "runtime portability degraded transition evidence stale" in msg]
        self.assertTrue(stale_msgs)
        self.assertTrue(any("threshold >12 sessions" in msg for msg in stale_msgs))

    def test_offline_continuity_stale_transition_is_flagged_with_recent_reason_signal(self):
        lines = [
            "F119 validation pass",
            "S200: inter-swarm continuity offline queue sync via tasks/PR-QUEUE.json and tasks/SWARM-LANES.md; Beliefs PASS NOTICE-only",
        ]
        results = self._run_check(
            next_lines=lines,
            session_log_lines=lines + ["S212: inter-swarm continuity offline mode on constrained host"],
            session=217,
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

    def test_runtime_portability_stale_transition_is_suppressed_without_recent_reason_signal(self):
        lines = [
            "F119 validation pass",
            "S200: runtime portability no runnable python alias; fallback via bash tools/check.sh --quick; Beliefs PASS NOTICE-only",
        ]
        results = self._run_check(
            next_lines=lines,
            session_log_lines=lines,
            session=220,
            python_status={"python3": False, "python": False},
            py_launcher=False,
            bash_available=True,
        )
        self.assertFalse(any("runtime portability degraded transition evidence stale" in msg for _, msg in results))

    def test_offline_continuity_stale_transition_is_suppressed_without_recent_reason_signal(self):
        lines = [
            "F119 validation pass",
            "S200: inter-swarm continuity offline queue sync via tasks/PR-QUEUE.json and tasks/SWARM-LANES.md; Beliefs PASS NOTICE-only",
        ]
        results = self._run_check(
            next_lines=lines,
            session_log_lines=lines,
            session=220,
            python_status={"python3": True, "python": False},
            py_launcher=False,
            bash_available=True,
            exists_overrides={
                "tools/bulletin.py": False,
                "tools/merge_back.py": False,
                "tools/propagate_challenges.py": False,
            },
        )
        self.assertFalse(any("offline/inter-swarm continuity degraded transition evidence stale" in msg for _, msg in results))

    def test_runtime_portability_transition_at_threshold_is_not_stale(self):
        lines = [
            "F119 validation pass",
            "S200: runtime portability no runnable python alias; fallback via bash tools/check.sh --quick; Beliefs PASS NOTICE-only",
        ]
        results = self._run_check(
            next_lines=lines,
            session_log_lines=lines,
            session=212,
            python_status={"python3": False, "python": False},
            py_launcher=False,
            bash_available=True,
        )
        self.assertFalse(any("runtime portability degraded transition evidence stale" in msg for _, msg in results))

    def test_offline_continuity_transition_at_threshold_is_not_stale(self):
        lines = [
            "F119 validation pass",
            "S200: inter-swarm continuity offline queue sync via tasks/PR-QUEUE.json and tasks/SWARM-LANES.md; Beliefs PASS NOTICE-only",
        ]
        results = self._run_check(
            next_lines=lines,
            session_log_lines=lines,
            session=216,
            python_status={"python3": True, "python": False},
            py_launcher=False,
            bash_available=True,
            exists_overrides={
                "tools/bulletin.py": False,
                "tools/merge_back.py": False,
                "tools/propagate_challenges.py": False,
            },
        )
        self.assertFalse(any("offline/inter-swarm continuity degraded transition evidence stale" in msg for _, msg in results))


class TestMissionConstraintDegradedRuntimeE2E(unittest.TestCase):
    def test_offline_artifacts_missing_emits_due_end_to_end(self):
        next_body = "\n".join(
            [
                "F119 tracked in priorities.",
                "S156: inter-swarm continuity offline queue sync via tasks/PR-QUEUE.json and tasks/SWARM-LANES.md; Beliefs PASS NOTICE-only",
            ]
        )
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _seed_repo(root, next_body)
            (root / "tools/bulletin.py").unlink(missing_ok=True)
            (root / "tools/merge_back.py").unlink(missing_ok=True)
            (root / "tools/propagate_challenges.py").unlink(missing_ok=True)
            (root / "tasks/PR-QUEUE.json").unlink(missing_ok=True)
            (root / "tasks/SWARM-LANES.md").unlink(missing_ok=True)

            with patch.object(maintenance, "REPO_ROOT", root), patch.object(
                maintenance, "_tracked_changed_paths", return_value=[]
            ), patch.object(
                maintenance, "_python_command_runs", side_effect=lambda cmd: cmd in {"python3", "python"}
            ), patch.object(
                maintenance, "_py_launcher_runs", return_value=False
            ), patch.object(
                maintenance, "_command_exists", return_value=True
            ), patch.object(
                maintenance, "_command_runs", return_value=True
            ):
                results = maintenance.check_mission_constraints()

        messages = [msg for _, msg in results]
        self.assertTrue(any("offline continuity artifacts missing" in msg for msg in messages))

    def test_offline_artifacts_present_no_due_end_to_end(self):
        next_body = "\n".join(
            [
                "F119 tracked in priorities.",
                "S156: inter-swarm continuity offline queue sync via tasks/PR-QUEUE.json and tasks/SWARM-LANES.md; Beliefs PASS NOTICE-only",
            ]
        )
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _seed_repo(root, next_body)
            (root / "tools/bulletin.py").unlink(missing_ok=True)
            (root / "tools/merge_back.py").unlink(missing_ok=True)
            (root / "tools/propagate_challenges.py").unlink(missing_ok=True)
            _write(root / "tasks/PR-QUEUE.json", '{"schema":"swarm-pr-queue-v1","items":[]}\n')
            _write(
                root / "tasks/SWARM-LANES.md",
                "| Date | Lane | Session | Agent | Branch | PR | Model | Platform | Scope-Key | Etc | Status | Notes |\n"
                "|---|---|---|---|---|---|---|---|---|---|---|---|\n",
            )

            with patch.object(maintenance, "REPO_ROOT", root), patch.object(
                maintenance, "_tracked_changed_paths", return_value=[]
            ), patch.object(
                maintenance, "_python_command_runs", side_effect=lambda cmd: cmd in {"python3", "python"}
            ), patch.object(
                maintenance, "_py_launcher_runs", return_value=False
            ), patch.object(
                maintenance, "_command_exists", return_value=True
            ), patch.object(
                maintenance, "_command_runs", return_value=True
            ):
                results = maintenance.check_mission_constraints()

        messages = [msg for _, msg in results]
        self.assertFalse(any("offline continuity artifacts missing" in msg for msg in messages))
        self.assertFalse(any("offline/inter-swarm continuity degraded mode lacks" in msg for msg in messages))

    def test_pwsh_wrappers_prevent_degraded_runtime_due_end_to_end(self):
        next_body = "\n".join(
            [
                "F119 tracked in priorities.",
                "S156: runtime portability no runnable python alias; fallback via pwsh -NoProfile -File tools/check.ps1 --quick; Beliefs PASS NOTICE-only",
            ]
        )
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            _seed_repo(root, next_body)
            (root / "tools/check.sh").unlink(missing_ok=True)
            (root / "tools/maintenance.sh").unlink(missing_ok=True)

            def fake_command_exists(cmd: str) -> bool:
                if cmd == "bash":
                    return False
                if cmd in {"pwsh", "powershell"}:
                    return True
                return True

            with patch.object(maintenance, "REPO_ROOT", root), patch.object(
                maintenance, "_tracked_changed_paths", return_value=[]
            ), patch.object(
                maintenance, "_python_command_runs", return_value=False
            ), patch.object(
                maintenance, "_py_launcher_runs", return_value=False
            ), patch.object(
                maintenance, "_command_exists", side_effect=fake_command_exists
            ), patch.object(
                maintenance, "_command_runs", return_value=True
            ):
                results = maintenance.check_mission_constraints()

        messages = [msg for _, msg in results]
        self.assertFalse(any("degraded runtime continuity broken" in msg for msg in messages))


class TestRuntimePortabilityFallbacks(unittest.TestCase):
    def _run_portability(
        self,
        *,
        has_git: bool = True,
        has_bash: bool = False,
        has_pwsh: bool = True,
        has_python3: bool = True,
        has_python: bool = False,
        has_py_launcher: bool = False,
        exists_overrides: dict[str, bool] | None = None,
    ) -> list[tuple[str, str]]:
        exists_values = {
            "workspace/genesis.sh": True,
            "tools/check.sh": True,
            "tools/maintenance.sh": True,
            "tools/check.ps1": True,
            "tools/maintenance.ps1": True,
            "SWARM.md": True,
            "CLAUDE.md": True,
            "AGENTS.md": True,
            "GEMINI.md": True,
            ".cursorrules": True,
            ".windsurfrules": True,
            ".github/copilot-instructions.md": True,
        }
        if exists_overrides:
            exists_values.update(exists_overrides)

        def fake_exists(path: str) -> bool:
            return exists_values.get(path, True)

        def fake_command_exists(cmd: str) -> bool:
            command_map = {
                "git": has_git,
                "bash": has_bash,
                "pwsh": has_pwsh,
                "powershell": has_pwsh,
            }
            return command_map.get(cmd, False)

        def fake_python_command_runs(cmd: str) -> bool:
            py_map = {
                "python3": has_python3,
                "python": has_python,
            }
            return py_map.get(cmd, False)

        with patch.object(maintenance, "_exists", side_effect=fake_exists):
            with patch.object(maintenance, "_command_exists", side_effect=fake_command_exists):
                with patch.object(maintenance, "_python_command_runs", side_effect=fake_python_command_runs):
                    with patch.object(maintenance, "_py_launcher_runs", return_value=has_py_launcher):
                        with patch.object(maintenance, "_is_wsl_mnt_repo", return_value=False):
                            with patch.object(maintenance, "_git", return_value=""):
                                with patch.object(maintenance, "_read", return_value="SWARM.md\nswarm signaling\n"):
                                    return maintenance.check_runtime_portability()

    def test_no_bash_uses_powershell_wrappers_when_python_available(self):
        results = self._run_portability(
            has_bash=False,
            has_pwsh=True,
            has_python3=True,
        )
        messages = [msg for _, msg in results]
        self.assertTrue(any("use PowerShell wrappers" in msg for msg in messages))
        self.assertFalse(any("portable startup path is broken" in msg for msg in messages))

    def test_no_bash_uses_direct_python_when_ps_wrappers_missing(self):
        results = self._run_portability(
            has_bash=False,
            has_pwsh=True,
            has_python3=True,
            exists_overrides={
                "tools/check.ps1": False,
                "tools/maintenance.ps1": False,
            },
        )
        messages = [msg for _, msg in results]
        self.assertTrue(any("use direct python entrypoints" in msg for msg in messages))
        self.assertFalse(any("portable startup path is broken" in msg for msg in messages))

    def test_no_bash_and_no_python_is_due(self):
        results = self._run_portability(
            has_bash=False,
            has_pwsh=True,
            has_python3=False,
            has_python=False,
            has_py_launcher=False,
        )
        due_messages = [msg for level, msg in results if level == "DUE"]
        self.assertTrue(any("No python alias in PATH" in msg for msg in due_messages))
        self.assertTrue(any("portable startup path is broken" in msg for msg in due_messages))


class TestStateHeaderSyncParsing(unittest.TestCase):
    def _run_state_header_sync(
        self,
        *,
        frontier_header: str,
        session: int = 200,
        next_session: int = 200,
        index_session: int = 200,
        dirty: bool = True,
    ) -> list[tuple[str, str]]:
        read_map = {
            "tasks/NEXT.md": f"# State\nUpdated: 2026-02-27 S{next_session}\n",
            "memory/INDEX.md": f"# Memory Index\nUpdated: 2026-02-27 | Sessions: {index_session}\n",
            "tasks/FRONTIER.md": (
                "# Frontier - Open Questions\n\n"
                f"14 active | {frontier_header}\n"
            ),
        }

        real_read = maintenance._read

        def fake_read(path):
            try:
                rel = path.relative_to(maintenance.REPO_ROOT).as_posix()
            except Exception:
                rel = str(path).replace("\\", "/")
            return read_map.get(rel, real_read(path))

        with patch.object(maintenance, "_read", side_effect=fake_read):
            with patch.object(maintenance, "_session_number", return_value=session):
                with patch.object(maintenance, "_git", return_value=("M x" if dirty else "")):
                    return maintenance.check_state_header_sync()

    def test_frontier_header_parses_with_pipe_separator(self):
        results = self._run_state_header_sync(
            frontier_header="Last updated: 2026-02-27 | S200",
            dirty=True,
        )
        self.assertFalse(
            any("State header parse failed" in msg for _, msg in results),
            f"Unexpected parse failure: {results}",
        )

    def test_frontier_header_parses_case_insensitive(self):
        results = self._run_state_header_sync(
            frontier_header="last UPDATED: 2026-02-27 s200",
            dirty=True,
        )
        self.assertFalse(
            any("State header parse failed" in msg for _, msg in results),
            f"Unexpected parse failure: {results}",
        )

    def test_frontier_header_missing_session_is_reported(self):
        results = self._run_state_header_sync(
            frontier_header="Last updated: 2026-02-27",
            dirty=True,
        )
        self.assertTrue(
            any("State header parse failed: FRONTIER" in msg for _, msg in results),
            f"Expected FRONTIER parse failure, got: {results}",
        )


if __name__ == "__main__":
    unittest.main()

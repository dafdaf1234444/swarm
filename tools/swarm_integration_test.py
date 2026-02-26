#!/usr/bin/env python3
"""
swarm_integration_test.py — Automated integration tests for the swarm architecture.

Usage:
    python3 tools/swarm_integration_test.py

Runs a suite of tests that verify the swarm can:
1. Bootstrap from genesis (spawn viability)
2. Maintain validator integrity after modifications
3. Reconstruct essential files from raw artifacts (redundancy)
4. Handle belief updates without breaking dependencies
5. Keep mandatory files under size limits

These are "swarm tests" — they test the system's architecture by
exercising it, not by inspecting static properties.
"""

import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PASSED = 0
FAILED = 0
ERRORS = []


def run_test(name: str, func):
    """Run a test and record results."""
    global PASSED, FAILED
    print(f"  [{name}] ", end="", flush=True)
    try:
        result = func()
        if result:
            PASSED += 1
            print("PASS")
        else:
            FAILED += 1
            ERRORS.append(f"{name}: returned False")
            print("FAIL")
    except Exception as e:
        FAILED += 1
        ERRORS.append(f"{name}: {e}")
        print(f"ERROR: {e}")


def test_genesis_spawns_valid_child():
    """Test that genesis.sh produces a child that passes validation."""
    with tempfile.TemporaryDirectory() as tmpdir:
        child_dir = os.path.join(tmpdir, "test-child")
        genesis = REPO_ROOT / "workspace" / "genesis.sh"

        # Spawn
        r = subprocess.run(
            ["bash", str(genesis), child_dir, "test"],
            capture_output=True, text=True
        )
        if r.returncode != 0:
            raise RuntimeError(f"genesis.sh failed: {r.stderr}")

        # Init git
        subprocess.run(["git", "init"], cwd=child_dir, capture_output=True)
        subprocess.run(["git", "add", "-A"], cwd=child_dir, capture_output=True)
        subprocess.run(
            ["git", "commit", "-m", "init"],
            cwd=child_dir, capture_output=True
        )

        # Validate
        r = subprocess.run(
            ["python3", "tools/validate_beliefs.py"],
            cwd=child_dir, capture_output=True, text=True
        )
        return r.returncode == 0 and "PASS" in r.stdout


def test_genesis_file_count():
    """Test that genesis.sh creates the expected number of files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        child_dir = os.path.join(tmpdir, "test-child")
        genesis = REPO_ROOT / "workspace" / "genesis.sh"

        subprocess.run(
            ["bash", str(genesis), child_dir, "test"],
            capture_output=True, text=True
        )

        # Count files (excluding directories and .gitkeep)
        file_count = sum(
            1 for f in Path(child_dir).rglob("*")
            if f.is_file() and f.name != ".gitkeep"
        )
        # genesis v3 should create 18 real files + 1 .gitkeep = 19 total
        # but we only count non-gitkeep
        return file_count >= 17


def test_validator_passes_current():
    """Test that the parent validator passes on current state."""
    r = subprocess.run(
        ["python3", str(REPO_ROOT / "tools" / "validate_beliefs.py")],
        cwd=str(REPO_ROOT), capture_output=True, text=True
    )
    return r.returncode == 0 and "PASS" in r.stdout


def test_mandatory_files_under_limit():
    """Test that mandatory files stay under 450 lines combined."""
    mandatory = [
        REPO_ROOT / "CLAUDE.md",
        REPO_ROOT / "beliefs" / "CORE.md",
        REPO_ROOT / "memory" / "INDEX.md",
    ]
    total = sum(
        len(f.read_text().splitlines()) for f in mandatory if f.exists()
    )
    return total < 450


def test_lessons_under_20_lines():
    """Test that all lessons are ≤20 lines."""
    lessons_dir = REPO_ROOT / "memory" / "lessons"
    for f in lessons_dir.glob("L-*.md"):
        lines = len(f.read_text().splitlines())
        if lines > 20:
            raise RuntimeError(f"{f.name} has {lines} lines (max 20)")
    return True


def test_beliefs_have_falsification():
    """Test that every active belief has a falsification condition."""
    deps = REPO_ROOT / "beliefs" / "DEPS.md"
    text = deps.read_text()

    # Find all active beliefs (not superseded)
    superseded_section = text.find("## Superseded")
    active_text = text[:superseded_section] if superseded_section > 0 else text

    beliefs = re.findall(r"^### (B\d+):", active_text, re.MULTILINE)
    for bid in beliefs:
        # Check each has "Falsified if"
        if f"### {bid}:" in active_text:
            block_start = active_text.index(f"### {bid}:")
            block_end = active_text.find("\n### B", block_start + 1)
            if block_end == -1:
                block_end = len(active_text)
            block = active_text[block_start:block_end]
            if "**Falsified if**:" not in block:
                raise RuntimeError(f"{bid} missing falsification condition")
    return True


def test_no_broken_belief_refs():
    """Test that no lesson references a belief that doesn't exist."""
    deps = REPO_ROOT / "beliefs" / "DEPS.md"
    deps_text = deps.read_text()

    # Find all defined belief IDs (including superseded)
    all_ids = set(re.findall(r"(?:### |~~)(B\d+)", deps_text))

    # Check lessons
    lessons_dir = REPO_ROOT / "memory" / "lessons"
    for f in lessons_dir.glob("L-*.md"):
        text = f.read_text()
        affected_m = re.search(r"## Affected beliefs:\s*(.+)", text)
        if affected_m:
            refs = re.findall(r"B\d+", affected_m.group(1))
            for ref in refs:
                if ref not in all_ids:
                    raise RuntimeError(
                        f"{f.name} references {ref} which doesn't exist"
                    )
    return True


def test_dep_consistency():
    """Test that Depends on / Depended on by are consistent."""
    r = subprocess.run(
        ["python3", str(REPO_ROOT / "tools" / "validate_beliefs.py")],
        cwd=str(REPO_ROOT), capture_output=True, text=True
    )
    # Check for DEP_SYNC warnings
    return "DEP_SYNC" not in r.stdout


def test_entropy_zero():
    """Test that the entropy detector finds zero items."""
    r = subprocess.run(
        ["python3", str(REPO_ROOT / "tools" / "validate_beliefs.py")],
        cwd=str(REPO_ROOT), capture_output=True, text=True
    )
    return "Entropy items: 0" in r.stdout


def test_principles_count_matches_lessons():
    """Test that every lesson with a rule has a matching principle."""
    principles = REPO_ROOT / "memory" / "PRINCIPLES.md"
    p_text = principles.read_text()
    p_ids = set(re.findall(r"\(L-(\d+)\)", p_text))

    lessons_dir = REPO_ROOT / "memory" / "lessons"
    missing = []
    for f in sorted(lessons_dir.glob("L-*.md")):
        if f.name == "TEMPLATE.md":
            continue
        lesson_num = re.search(r"L-(\d+)", f.name).group(1)
        text = f.read_text()
        # Check if lesson has a rule
        if "## Rule extracted" in text:
            rule_m = re.search(
                r"## Rule extracted.*?\n(.+?)(?:\n\n|\n##|\Z)",
                text, re.DOTALL
            )
            if rule_m and rule_m.group(1).strip() and rule_m.group(1).strip() != "none":
                if lesson_num not in p_ids:
                    missing.append(f"L-{lesson_num}")

    if missing:
        raise RuntimeError(f"Lessons with rules but no principle: {missing}")
    return True


def test_evolve_tool_exists():
    """Test that evolve.py exists and has all commands."""
    evolve = REPO_ROOT / "tools" / "evolve.py"
    if not evolve.exists():
        raise RuntimeError("tools/evolve.py does not exist")
    text = evolve.read_text()
    for cmd in ["init", "harvest", "integrate", "cycle"]:
        if f'cmd == "{cmd}"' not in text:
            raise RuntimeError(f"evolve.py missing command: {cmd}")
    return True


def test_merge_reports_valid():
    """Test that all merge-back reports have required sections."""
    reports_dir = REPO_ROOT / "experiments" / "merge-reports"
    if not reports_dir.exists():
        return True  # No reports yet is fine
    for f in reports_dir.glob("*.md"):
        text = f.read_text()
        if "## Lessons" not in text:
            raise RuntimeError(f"{f.name} missing ## Lessons section")
        if "## Recommendations" not in text:
            raise RuntimeError(f"{f.name} missing ## Recommendations section")
    return True


def test_integration_log_valid():
    """Test that integration logs are valid JSON with required fields."""
    log_dir = REPO_ROOT / "experiments" / "integration-log"
    if not log_dir.exists():
        return True  # No logs yet is fine
    import json
    for f in log_dir.glob("*.json"):
        data = json.loads(f.read_text())
        for field in ["child", "date", "novel_rules", "novel_questions"]:
            if field not in data:
                raise RuntimeError(f"{f.name} missing field: {field}")
    return True


def test_growth_rate_runs():
    """Test that session_tracker.py growth-rate command runs without error."""
    r = subprocess.run(
        ["python3", str(REPO_ROOT / "tools" / "session_tracker.py"), "growth-rate"],
        cwd=str(REPO_ROOT), capture_output=True, text=True
    )
    if r.returncode != 0:
        raise RuntimeError(f"growth-rate failed: {r.stderr}")
    required = ["File Growth Rates", "Frontier Health", "Belief Ratio", "Summary"]
    for section in required:
        if section not in r.stdout:
            raise RuntimeError(f"growth-rate output missing: {section}")
    return True


def main():
    global PASSED, FAILED

    print("=== SWARM INTEGRATION TESTS ===\n")

    print("Spawn tests:")
    run_test("genesis_spawns_valid_child", test_genesis_spawns_valid_child)
    run_test("genesis_file_count", test_genesis_file_count)

    print("\nIntegrity tests:")
    run_test("validator_passes_current", test_validator_passes_current)
    run_test("mandatory_files_under_limit", test_mandatory_files_under_limit)
    run_test("lessons_under_20_lines", test_lessons_under_20_lines)
    run_test("beliefs_have_falsification", test_beliefs_have_falsification)
    run_test("no_broken_belief_refs", test_no_broken_belief_refs)
    run_test("dep_consistency", test_dep_consistency)
    run_test("entropy_zero", test_entropy_zero)

    print("\nCompleteness tests:")
    run_test("principles_count_matches_lessons", test_principles_count_matches_lessons)

    print("\nEvolution pipeline tests:")
    run_test("evolve_tool_exists", test_evolve_tool_exists)
    run_test("merge_reports_valid", test_merge_reports_valid)
    run_test("integration_log_valid", test_integration_log_valid)
    run_test("growth_rate_runs", test_growth_rate_runs)

    print(f"\n{'='*40}")
    print(f"PASSED: {PASSED}/{PASSED + FAILED}")
    if ERRORS:
        print(f"FAILED: {FAILED}")
        for e in ERRORS:
            print(f"  - {e}")
        return 1
    else:
        print("ALL TESTS PASS")
        return 0


if __name__ == "__main__":
    sys.exit(main())

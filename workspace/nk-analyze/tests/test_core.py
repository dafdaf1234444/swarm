"""Tests for nk_analyze.core — module-level NK analysis."""
import pytest
from nk_analyze.core import (
    analyze_lazy_imports,
    analyze_package,
    classify_architecture,
    detect_cycles,
    find_package_path,
    list_modules,
)


# ---------------------------------------------------------------------------
# find_package_path
# ---------------------------------------------------------------------------

def test_find_package_path_existing():
    path = find_package_path("json")
    assert path is not None
    assert path.is_dir()


def test_find_package_path_missing():
    assert find_package_path("_nonexistent_package_xyz_") is None


# ---------------------------------------------------------------------------
# detect_cycles
# ---------------------------------------------------------------------------

def test_detect_cycles_simple_cycle():
    deps = {"a": ["b"], "b": ["a"], "c": []}
    cycles = detect_cycles(deps)
    assert len(cycles) == 1
    cycle = cycles[0]
    assert set(cycle) >= {"a", "b"}


def test_detect_cycles_three_node_cycle():
    deps = {"a": ["b"], "b": ["c"], "c": ["a"]}
    cycles = detect_cycles(deps)
    assert len(cycles) == 1
    assert len(cycles[0]) == 4  # a → b → c → a


def test_detect_cycles_no_cycles():
    deps = {"a": ["b"], "b": ["c"], "c": []}
    assert detect_cycles(deps) == []


def test_detect_cycles_self_loop():
    deps = {"a": ["a"]}
    cycles = detect_cycles(deps)
    assert len(cycles) == 1


def test_detect_cycles_empty():
    assert detect_cycles({}) == []
    assert detect_cycles({"a": [], "b": []}) == []


# ---------------------------------------------------------------------------
# classify_architecture
# ---------------------------------------------------------------------------

def test_classify_architecture_monolith():
    # n <= 3 → monolith
    assert classify_architecture(2, 1.0, 1, 0, 0.5) == "monolith"


def test_classify_architecture_tangled():
    # cycles > 3
    assert classify_architecture(10, 2.0, 5, 4, 0.2) == "tangled"


def test_classify_architecture_hub_and_spoke():
    assert classify_architecture(10, 0.5, 4, 0, 0.6) == "hub-and-spoke"


def test_classify_architecture_framework():
    assert classify_architecture(10, 3.0, 2, 0, 0.1) == "framework"


def test_classify_architecture_distributed():
    # No dominant pattern
    assert classify_architecture(10, 0.3, 1, 0, 0.1) == "distributed"


# ---------------------------------------------------------------------------
# analyze_package — known packages
# ---------------------------------------------------------------------------

def test_analyze_json_n():
    r = analyze_package("json")
    assert "error" not in r
    assert r["n"] == 5


def test_analyze_json_cycles():
    r = analyze_package("json")
    assert r["cycles"] == 0


def test_analyze_json_architecture():
    r = analyze_package("json")
    assert r["architecture"] == "hub-and-spoke"


def test_analyze_json_k_avg():
    r = analyze_package("json")
    assert abs(r["k_avg"] - 0.4) < 0.05


def test_analyze_json_keys():
    r = analyze_package("json")
    required = {"package", "path", "n", "k_total", "k_avg", "k_n", "k_max",
                "cycles", "cycle_details", "composite", "architecture",
                "total_loc", "modules"}
    assert required.issubset(r.keys())


def test_analyze_logging_n():
    r = analyze_package("logging")
    assert "error" not in r
    assert r["n"] >= 3  # __init__, handlers, config at minimum


def test_analyze_missing_package():
    r = analyze_package("_nonexistent_xyz_")
    assert "error" in r


def test_analyze_composite_formula():
    """composite = k_avg * n + cycles"""
    r = analyze_package("json")
    expected = round(r["k_avg"] * r["n"] + r["cycles"], 2)
    assert abs(r["composite"] - expected) < 0.05


# ---------------------------------------------------------------------------
# analyze_lazy_imports
# ---------------------------------------------------------------------------

def test_analyze_lazy_imports_json():
    r = analyze_lazy_imports("json")
    assert "error" not in r
    assert "static_cycles" in r
    assert "runtime_cycles" in r
    assert isinstance(r["static_cycles"], int)
    assert isinstance(r["runtime_cycles"], int)
    assert r["static_cycles"] >= 0
    assert "lazy_imports" in r


def test_analyze_lazy_imports_missing():
    r = analyze_lazy_imports("_nonexistent_xyz_")
    assert "error" in r


# ---------------------------------------------------------------------------
# list_modules
# ---------------------------------------------------------------------------

def test_list_modules_json():
    from pathlib import Path
    path = find_package_path("json")
    assert path is not None
    mods = list_modules(path)
    assert "decoder" in mods
    assert "encoder" in mods
    assert len(mods) >= 4

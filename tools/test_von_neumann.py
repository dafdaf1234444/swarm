#!/usr/bin/env python3
"""Tests for von_neumann_test.py"""
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from von_neumann_test import analyze, component_stats, minimax_falsification_rate

def test_components_exist():
    r = analyze()
    for key in ["A_constructor", "B_copier", "C_controller", "D_description_boot"]:
        c = r["von_neumann_components"][key]
        assert c["files"] > 0, f"{key} has no files"
        assert c["raw_bytes"] > 0, f"{key} has 0 bytes"
        assert len(c["missing"]) == 0, f"{key} missing: {c['missing']}"

def test_complexity_inequality():
    r = analyze()
    ci = r["complexity_inequality"]
    assert ci["K_D_compressed"] > 0
    assert ci["K_ABC_compressed"] > 0
    assert ci["boot_ratio"] > 0

def test_minimax_bounds():
    assert 0 < minimax_falsification_rate(10, 1) < 1
    assert minimax_falsification_rate(1, 1) == 0.5
    assert minimax_falsification_rate(99, 1) > 0.98

def test_json_serializable():
    r = analyze()
    json.dumps(r, default=str)  # should not raise

if __name__ == "__main__":
    test_components_exist()
    test_complexity_inequality()
    test_minimax_bounds()
    test_json_serializable()
    print("All tests pass")

#!/usr/bin/env python3
"""
nk_analyze.py — Automated NK landscape analysis for Python packages.

Usage:
    python3 tools/nk_analyze.py <package_name>
    python3 tools/nk_analyze.py <package_name> --json
    python3 tools/nk_analyze.py <package_name> --verbose
    python3 tools/nk_analyze.py batch [pkg1 pkg2 ...]
    python3 tools/nk_analyze.py <package_name> --suggest-refactor
    python3 tools/nk_analyze.py <package_name> --lazy
    python3 tools/nk_analyze.py batch --lazy
    python3 tools/nk_analyze.py compare --repo <path> --pkg <subpath> --name <name> <ref1> <ref2>

Analyzes internal dependencies of a Python package and computes:
- N (number of modules), K_total (edges), K_avg, K/N, K_max
- Cycle detection
- Composite score: K_avg * N + Cycles
- Architecture classification (facade, monolith, framework, registry)

Compare mode analyzes a package at two git refs and outputs the delta (ΔNK).

Examples:
    python3 tools/nk_analyze.py json
    python3 tools/nk_analyze.py email --verbose
    python3 tools/nk_analyze.py asyncio --json
    python3 tools/nk_analyze.py batch json email asyncio
    python3 tools/nk_analyze.py batch  # scans default stdlib set
    python3 tools/nk_analyze.py compare --repo workspace/werkzeug --pkg src/werkzeug --name werkzeug 1.0.0 2.0.0
"""

import ast
import importlib
import json as json_mod
import os
import subprocess
import sys
from collections import defaultdict
from pathlib import Path


def find_package_path(package_name: str) -> Path | None:
    """Find the filesystem path of a Python package.

    Returns the package directory for multi-file packages,
    or None for single-file modules (which can't have internal deps).
    """
    try:
        mod = importlib.import_module(package_name)
        if hasattr(mod, "__path__"):
            return Path(mod.__path__[0])
        # Single-file module — no internal dependencies to analyze
        return None
    except ImportError:
        pass
    return None


def list_modules(pkg_path: Path) -> dict[str, Path]:
    """List all .py module files in a package recursively.

    Returns dict mapping dotted module name to filepath.
    E.g., {"__init__": .../pkg/__init__.py, "mime.text": .../pkg/mime/text.py}
    """
    modules = {}
    skip_dirs = {"__pycache__", "tests", "test", "_vendor"}

    for root, dirs, files in os.walk(pkg_path):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        rel_dir = Path(root).relative_to(pkg_path)

        for f in sorted(files):
            if not f.endswith(".py"):
                continue
            stem = f[:-3]  # remove .py
            if rel_dir == Path("."):
                mod_name = stem
            else:
                mod_name = str(rel_dir / stem).replace(os.sep, ".")

            # Clean up sub-package __init__ → use directory name
            if mod_name.endswith(".__init__"):
                mod_name = mod_name[:-9]  # "mime.__init__" → "mime"

            modules[mod_name] = Path(root) / f

    return modules


def _resolve_import_name(node, filepath, package_name, pkg_base):
    """Resolve an import AST node to internal module names.

    Returns a set of dotted module names relative to the package root.
    """
    results = set()

    if isinstance(node, ast.ImportFrom):
        if node.module and node.level == 0:
            parts = node.module.split(".")
            if parts[0] == package_name and len(parts) > 1:
                sub_module = ".".join(parts[1:])
                results.add(sub_module)
                if len(parts) > 2:
                    results.add(parts[1])
        elif node.level >= 1:
            if node.module:
                rel_dir = filepath.parent
                for _ in range(node.level - 1):
                    rel_dir = rel_dir.parent
                parts = node.module.split(".")
                try:
                    prefix = rel_dir.relative_to(pkg_base / package_name)
                    if str(prefix) == ".":
                        dotted = ".".join(parts)
                    else:
                        dotted = str(prefix).replace(os.sep, ".") + "." + ".".join(parts)
                except ValueError:
                    dotted = ".".join(parts)
                results.add(dotted)
                if len(parts) > 0:
                    try:
                        prefix = rel_dir.relative_to(pkg_base / package_name)
                        if str(prefix) == ".":
                            results.add(parts[0])
                        else:
                            results.add(str(prefix).replace(os.sep, ".") + "." + parts[0])
                    except ValueError:
                        results.add(parts[0])
            elif node.names:
                rel_dir = filepath.parent
                for _ in range(node.level - 1):
                    rel_dir = rel_dir.parent
                for alias in node.names:
                    try:
                        prefix = rel_dir.relative_to(pkg_base / package_name)
                        if str(prefix) == ".":
                            results.add(alias.name)
                        else:
                            results.add(str(prefix).replace(os.sep, ".") + "." + alias.name)
                    except ValueError:
                        results.add(alias.name)

    elif isinstance(node, ast.Import):
        for alias in node.names:
            parts = alias.name.split(".")
            if parts[0] == package_name and len(parts) > 1:
                results.add(".".join(parts[1:]))

    return results


def _is_top_level(node, tree):
    """Check if an import node is at module top-level (not inside a function/class)."""
    # Walk the tree with parent tracking to determine nesting
    for top_node in ast.iter_child_nodes(tree):
        if node is top_node:
            return True
    return False


def extract_imports_layered(filepath: Path, package_name: str) -> dict:
    """Extract imports categorized by scope: top-level vs lazy (inside functions).

    Returns {"top_level": [...], "lazy": [...], "lazy_locations": [{"module": ..., "func": ..., "line": ...}]}
    """
    try:
        source = filepath.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(source)
    except (SyntaxError, ValueError):
        return {"top_level": [], "lazy": [], "lazy_locations": []}

    pkg_root = filepath
    while pkg_root.parent.name != package_name and pkg_root.parent != pkg_root:
        pkg_root = pkg_root.parent
    pkg_base = pkg_root.parent.parent

    top_level = set()
    lazy = set()
    lazy_locations = []

    def _walk_scope(node, enclosing_func=None):
        """Walk AST tracking scope depth."""
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Everything inside a function is lazy
                _walk_scope(child, enclosing_func=child.name)
            elif isinstance(child, ast.ClassDef):
                # Class body — imports here are semi-lazy, walk into methods
                _walk_scope(child, enclosing_func=enclosing_func)
            elif isinstance(child, (ast.ImportFrom, ast.Import)):
                names = _resolve_import_name(child, filepath, package_name, pkg_base)
                if enclosing_func is not None:
                    lazy.update(names)
                    for name in names:
                        lazy_locations.append({
                            "module": name,
                            "func": enclosing_func,
                            "line": child.lineno,
                        })
                else:
                    top_level.update(names)
            else:
                _walk_scope(child, enclosing_func=enclosing_func)

    _walk_scope(tree)

    return {
        "top_level": sorted(top_level),
        "lazy": sorted(lazy),
        "lazy_locations": lazy_locations,
    }


def extract_imports(filepath: Path, package_name: str) -> list[str]:
    """Extract internal imports from a Python file using AST parsing.

    Returns dotted module names relative to the package root.
    E.g., for email: ["charset", "mime", "mime.text", "errors"]
    """
    try:
        source = filepath.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(source)
    except (SyntaxError, ValueError):
        return []

    # Determine this file's position relative to package root
    # pkg_base should be the PARENT of the package directory
    # so that pkg_base / package_name = the package root
    pkg_root = filepath
    while pkg_root.parent.name != package_name and pkg_root.parent != pkg_root:
        pkg_root = pkg_root.parent
    pkg_base = pkg_root.parent.parent  # Parent of the package directory

    internal_imports = set()

    for node in ast.walk(tree):
        if isinstance(node, (ast.ImportFrom, ast.Import)):
            internal_imports.update(
                _resolve_import_name(node, filepath, package_name, pkg_base)
            )

    return sorted(internal_imports)


def detect_cycles(deps: dict[str, list[str]]) -> list[list[str]]:
    """Find all cycles in the dependency graph using DFS."""
    cycles = []
    visited = set()
    rec_stack = set()
    path = []

    def dfs(node: str):
        visited.add(node)
        rec_stack.add(node)
        path.append(node)

        for neighbor in deps.get(node, []):
            if neighbor not in visited:
                dfs(neighbor)
            elif neighbor in rec_stack:
                # Found a cycle
                cycle_start = path.index(neighbor)
                cycle = path[cycle_start:] + [neighbor]
                # Normalize: start from smallest element
                min_idx = cycle[:-1].index(min(cycle[:-1]))
                normalized = cycle[min_idx:-1] + cycle[:min_idx] + [cycle[min_idx]]
                if normalized not in cycles:
                    cycles.append(normalized)

        path.pop()
        rec_stack.discard(node)

    for node in sorted(deps.keys()):
        if node not in visited:
            dfs(node)

    return cycles


def classify_architecture(
    n: int, k_avg: float, k_max: int, cycles: int, hub_pct: float
) -> str:
    """Classify the package's architecture pattern."""
    if n <= 3:
        return "monolith"
    if cycles > 3:
        return "tangled"
    if hub_pct > 0.5 and k_max > n * 0.3:
        return "hub-and-spoke"
    if k_avg > 2.0:
        return "framework"
    if k_max > n * 0.4:
        return "registry"
    if hub_pct > 0.3:
        return "facade"
    return "distributed"


def count_lines(filepath: Path) -> int:
    """Count lines in a file."""
    try:
        return len(filepath.read_text(encoding="utf-8", errors="replace").splitlines())
    except Exception:
        return 0


def analyze_package(package_name: str, verbose: bool = False) -> dict:
    """Perform full NK analysis on a Python package."""
    pkg_path = find_package_path(package_name)
    if not pkg_path:
        return {"error": f"'{package_name}' is a single-file module (no internal dependencies to analyze) or not found"}

    # List modules
    modules = list_modules(pkg_path)
    if not modules:
        return {"error": f"No modules found in {pkg_path}"}

    # Build dependency map
    deps: dict[str, list[str]] = {}
    file_info: dict[str, dict] = {}
    module_names = set(modules.keys())

    for mod_name, filepath in modules.items():
        imports = extract_imports(filepath, package_name)
        # Filter to only modules that exist in our list
        valid_imports = [i for i in imports if i in module_names and i != mod_name]
        deps[mod_name] = valid_imports

        file_info[mod_name] = {
            "loc": count_lines(filepath),
            "k_out": len(valid_imports),
            "imports": valid_imports,
        }

    # Compute NK metrics
    n = len(file_info)
    if n == 0:
        return {"error": "No analyzable modules found"}

    k_total = sum(len(d) for d in deps.values())
    k_avg = k_total / n if n > 0 else 0
    k_n = k_avg / n if n > 0 else 0
    k_max = max((len(d) for d in deps.values()), default=0)
    k_max_file = max(deps.keys(), key=lambda k: len(deps[k]), default="")

    # In-degree
    in_degree: dict[str, int] = defaultdict(int)
    for mod, imports in deps.items():
        for imp in imports:
            in_degree[imp] += 1

    # Cycles
    cycles = detect_cycles(deps)
    cycle_count = len(cycles)

    # Composite score (architecture classification)
    composite = k_avg * n + cycle_count
    # Burden score (maintenance prediction, P-061/L-055)
    burden = cycle_count + 0.1 * n

    # Hub analysis
    hub_pct = k_max / k_total if k_total > 0 else 0

    # Architecture classification
    arch = classify_architecture(n, k_avg, k_max, cycle_count, hub_pct)

    # Total LOC
    total_loc = sum(f["loc"] for f in file_info.values())

    result = {
        "package": package_name,
        "path": str(pkg_path),
        "n": n,
        "k_total": k_total,
        "k_avg": round(k_avg, 2),
        "k_n": round(k_n, 3),
        "k_max": k_max,
        "k_max_file": k_max_file,
        "cycles": cycle_count,
        "cycle_details": [" → ".join(c) for c in cycles],
        "composite": round(composite, 1),
        "burden": round(burden, 1),
        "architecture": arch,
        "hub_pct": round(hub_pct, 2),
        "total_loc": total_loc,
        "modules": file_info,
        "in_degree": dict(in_degree),
    }

    return result


def analyze_lazy_imports(package_name: str) -> dict:
    """Analyze lazy vs top-level imports and their effect on cycles.

    Returns comparison of static graph (top-level only) vs runtime graph (all imports).
    """
    pkg_path = find_package_path(package_name)
    if not pkg_path:
        return {"error": f"'{package_name}' not found or single-file module"}

    modules = list_modules(pkg_path)
    if not modules:
        return {"error": f"No modules found in {pkg_path}"}

    module_names = set(modules.keys())
    static_deps = {}
    runtime_deps = {}
    all_lazy = []

    for mod_name, filepath in modules.items():
        layered = extract_imports_layered(filepath, package_name)

        top_valid = [i for i in layered["top_level"] if i in module_names and i != mod_name]
        lazy_valid = [i for i in layered["lazy"] if i in module_names and i != mod_name]
        all_valid = sorted(set(top_valid + lazy_valid))

        static_deps[mod_name] = top_valid
        runtime_deps[mod_name] = all_valid

        for loc in layered["lazy_locations"]:
            if loc["module"] in module_names and loc["module"] != mod_name:
                all_lazy.append({
                    "source": mod_name,
                    "target": loc["module"],
                    "func": loc["func"],
                    "line": loc["line"],
                })

    static_cycles = detect_cycles(static_deps)
    runtime_cycles = detect_cycles(runtime_deps)

    # Find which lazy imports break cycles
    cycle_breaking = []
    for lazy_imp in all_lazy:
        # Test: would adding this edge to the static graph create a new cycle?
        test_deps = {k: list(v) for k, v in static_deps.items()}
        if lazy_imp["target"] not in test_deps.get(lazy_imp["source"], []):
            test_deps.setdefault(lazy_imp["source"], []).append(lazy_imp["target"])
            test_cycles = detect_cycles(test_deps)
            if len(test_cycles) > len(static_cycles):
                new_cycles = [c for c in test_cycles if c not in static_cycles]
                cycle_breaking.append({
                    **lazy_imp,
                    "would_create_cycles": len(new_cycles),
                    "new_cycles": [" → ".join(c) for c in new_cycles],
                })

    return {
        "package": package_name,
        "total_lazy_imports": len(all_lazy),
        "cycle_breaking_lazy": len(cycle_breaking),
        "non_cycle_breaking_lazy": len(all_lazy) - len(cycle_breaking),
        "static_cycles": len(static_cycles),
        "runtime_cycles": len(runtime_cycles),
        "hidden_cycles": len(runtime_cycles) - len(static_cycles),
        "static_cycle_details": [" → ".join(c) for c in static_cycles],
        "runtime_cycle_details": [" → ".join(c) for c in runtime_cycles],
        "lazy_imports": all_lazy,
        "cycle_breaking_details": cycle_breaking,
        "hypothesis_f44": (
            "SUPPORTS" if len(all_lazy) > 0 and len(cycle_breaking) == len(all_lazy)
            else "PARTIAL" if len(cycle_breaking) > 0
            else "NO_LAZY" if len(all_lazy) == 0
            else "REFUTES"
        ),
    }


def print_lazy_report(result: dict):
    """Print lazy import analysis report."""
    if "error" in result:
        print(f"ERROR: {result['error']}")
        return

    pkg = result["package"]
    print(f"\n=== LAZY IMPORT ANALYSIS: {pkg} ===\n")
    print(f"  Total lazy imports (internal): {result['total_lazy_imports']}")
    print(f"  Cycle-breaking lazy imports:   {result['cycle_breaking_lazy']}")
    print(f"  Non-cycle-breaking lazy:       {result['non_cycle_breaking_lazy']}")
    print()
    print(f"  Static cycles (top-level):     {result['static_cycles']}")
    print(f"  Runtime cycles (all imports):  {result['runtime_cycles']}")
    print(f"  Hidden cycles (lazy-deferred): {result['hidden_cycles']}")
    print()

    if result["lazy_imports"]:
        print("  Lazy Imports:")
        for imp in result["lazy_imports"]:
            breaking = any(
                cb["source"] == imp["source"] and cb["target"] == imp["target"]
                for cb in result["cycle_breaking_details"]
            )
            marker = " [CYCLE-BREAKING]" if breaking else ""
            print(f"    {imp['source']}:{imp['line']} → {imp['target']} (in {imp['func']}){marker}")
        print()

    if result["cycle_breaking_details"]:
        print("  Cycle-Breaking Details:")
        for cb in result["cycle_breaking_details"]:
            print(f"    {cb['source']} → {cb['target']} would create {cb['would_create_cycles']} cycle(s):")
            for cyc in cb["new_cycles"]:
                print(f"      {cyc}")
        print()

    verdict = result["hypothesis_f44"]
    print(f"  F44 Hypothesis Verdict: {verdict}")
    if verdict == "SUPPORTS":
        print("    All lazy imports in this package correspond to cycle-breaking.")
    elif verdict == "PARTIAL":
        print("    Some lazy imports break cycles, but some don't.")
    elif verdict == "NO_LAZY":
        print("    No internal lazy imports found — hypothesis not testable.")
    elif verdict == "REFUTES":
        print("    Lazy imports exist but none break cycles.")


def print_report(result: dict, verbose: bool = False):
    """Print a human-readable NK analysis report."""
    if "error" in result:
        print(f"ERROR: {result['error']}")
        return

    pkg = result["package"]
    print(f"=== NK ANALYSIS: {pkg} ===\n")

    print(f"  Path: {result['path']}")
    print(f"  Total LOC: {result['total_loc']}")
    print(f"  Architecture: {result['architecture']}")
    print()

    # Metrics table
    print("  NK Metrics:")
    print(f"    N (modules):          {result['n']}")
    print(f"    K_total (edges):      {result['k_total']}")
    print(f"    K_avg:                {result['k_avg']}")
    print(f"    K/N:                  {result['k_n']}")
    print(f"    K_max:                {result['k_max']} ({result['k_max_file']})")
    print(f"    Cycles:               {result['cycles']}")
    print(f"    K_avg*N + Cycles:     {result['composite']}")
    print(f"    Burden (Cyc+0.1N):   {result['burden']}")
    print(f"    Hub concentration:    {result['hub_pct']:.0%}")
    print()

    if result["cycles"] > 0:
        print("  Cycles:")
        for c in result["cycle_details"]:
            print(f"    {c}")
        print()

    # Module table
    if verbose:
        print("  Modules:")
        print(f"    {'Module':<25} {'LOC':>6} {'K_out':>6} {'K_in':>5}  Imports")
        print("    " + "-" * 70)
        for mod in sorted(result["modules"].keys()):
            info = result["modules"][mod]
            k_in = result["in_degree"].get(mod, 0)
            imports_str = ", ".join(info["imports"]) if info["imports"] else "(none)"
            print(f"    {mod:<25} {info['loc']:>6} {info['k_out']:>6} {k_in:>5}  {imports_str}")
        print()

    # Comparison
    print("  Cross-Package Comparison:")
    benchmarks = [
        ("logging", "Py", 1.0),
        ("json", "Py", 2.0),
        ("urllib", "Py", 6.0),
        ("Express 5", "JS", 6.0),
        ("Express 4", "JS", 15.0),
        ("http.client", "Py", 26.4),
        ("unittest", "Py", 28.0),
        ("Rust serde", "Rust", 30.0),
        ("importlib", "Py", 38.0),
        ("xml", "Py", 38.0),
        ("email", "Py", 46.0),
        ("argparse", "Py", 48.1),
        ("requests", "Py", 55.0),
        ("click", "Py", 68.0),
        ("Go net/http", "Go", 89.0),
        ("multiprocessing", "Py", 102.0),
        ("jinja2", "Py", 109.0),
        ("asyncio", "Py", 128.0),
        ("flask", "Py", 130.0),
        ("werkzeug", "Py", 238.0),
    ]

    # Insert current package
    inserted = False
    print(f"    {'Package':<20} {'Score':>8}")
    print("    " + "-" * 30)
    for name, lang, score in benchmarks:
        if not inserted and result["composite"] <= score:
            print(f"  → {pkg:<20} {result['composite']:>8.1f}  ← THIS")
            inserted = True
        print(f"    {name:<20} {score:>8.1f}")
    if not inserted:
        print(f"  → {pkg:<20} {result['composite']:>8.1f}  ← THIS")


def suggest_refactor(result: dict):
    """Suggest which modules to extract for maximum cycle reduction."""
    if "error" in result:
        print(f"ERROR: {result['error']}")
        return

    if result["cycles"] == 0:
        print(f"\n  {result['package']} has 0 cycles — no refactoring needed for cycle reduction.")
        print(f"  Composite score: {result['composite']}")
        return

    deps = {k: v["imports"] for k, v in result["modules"].items()}

    # Count cycle participation for each module
    participation = {}
    for cycle_str in result["cycle_details"]:
        mods = cycle_str.split(" → ")
        for m in mods[:-1]:
            participation[m] = participation.get(m, 0) + 1

    # Simulate extraction of top candidates
    print(f"\n=== REFACTORING SUGGESTIONS: {result['package']} ===\n")
    print(f"  Current: N={result['n']}, Cycles={result['cycles']}, Composite={result['composite']}")
    print()

    # Sort by cycle participation
    ranked = sorted(participation.items(), key=lambda x: -x[1])

    print(f"  {'Module':<25} {'CyclePart':>10} {'Cycles_after':>13} {'Composite_after':>16} {'CycleReduction':>15}")
    print("  " + "-" * 82)

    for mod, count in ranked[:7]:
        new_deps = {}
        for m, imports in deps.items():
            if m == mod:
                continue
            new_deps[m] = [i for i in imports if i != mod]

        n_after = len(new_deps)
        k_total = sum(len(d) for d in new_deps.values())
        k_avg = k_total / n_after if n_after > 0 else 0
        cycles_after = len(detect_cycles(new_deps))
        composite_after = k_avg * n_after + cycles_after
        cycle_reduction = (1 - cycles_after / result["cycles"]) * 100

        marker = " ← BEST" if mod == ranked[0][0] else ""
        print(
            f"  {mod:<25} {count:>10}/{result['cycles']}"
            f" {cycles_after:>13} {composite_after:>16.1f} {cycle_reduction:>14.0f}%{marker}"
        )

    best_mod = ranked[0][0]
    best_info = result["modules"].get(best_mod, {})
    k_in = result["in_degree"].get(best_mod, 0)
    k_out = best_info.get("k_out", 0)

    print(f"\n  Recommendation: Extract '{best_mod}' first")
    print(f"    - Participates in {ranked[0][1]}/{result['cycles']} cycles ({ranked[0][1]*100//result['cycles']}%)")
    print(f"    - K_in={k_in} (imported by {k_in} modules), K_out={k_out}")
    if k_in > k_out:
        print(f"    - High K_in/K_out ratio → 'cycle passenger' (good extraction candidate)")
    else:
        print(f"    - Low K_in/K_out ratio → 'cycle driver' (extraction may require interface changes)")
    print()


def batch_analyze(packages: list[str]):
    """Analyze multiple packages and print a comparison table."""
    results = []
    for pkg in packages:
        r = analyze_package(pkg)
        if "error" not in r:
            results.append(r)
        else:
            print(f"  SKIP: {pkg} — {r['error']}")

    if not results:
        print("No packages analyzed successfully.")
        return

    # Sort by composite score
    results.sort(key=lambda r: r["composite"])

    print(f"\n{'Package':<25} {'N':>4} {'K_avg':>6} {'K_max':>6} {'Cycles':>7} {'Composite':>10} {'Architecture':<15}")
    print("-" * 80)
    for r in results:
        print(
            f"{r['package']:<25} {r['n']:>4} {r['k_avg']:>6.2f} "
            f"{r['k_max']:>6} {r['cycles']:>7} {r['composite']:>10.1f} "
            f"{r['architecture']:<15}"
        )


def analyze_path(pkg_path: Path, package_name: str) -> dict:
    """Perform NK analysis on a package at a given filesystem path.

    Like analyze_package but takes an explicit path instead of using importlib.
    """
    if not pkg_path.is_dir():
        return {"error": f"Path {pkg_path} is not a directory"}

    modules = list_modules(pkg_path)
    if not modules:
        return {"error": f"No modules found in {pkg_path}"}

    deps: dict[str, list[str]] = {}
    file_info: dict[str, dict] = {}
    module_names = set(modules.keys())

    for mod_name, filepath in modules.items():
        imports = extract_imports(filepath, package_name)
        valid_imports = [i for i in imports if i in module_names and i != mod_name]
        deps[mod_name] = valid_imports
        file_info[mod_name] = {
            "loc": count_lines(filepath),
            "k_out": len(valid_imports),
            "imports": valid_imports,
        }

    n = len(file_info)
    if n == 0:
        return {"error": "No analyzable modules found"}

    k_total = sum(len(d) for d in deps.values())
    k_avg = k_total / n if n > 0 else 0
    k_n = k_avg / n if n > 0 else 0
    k_max = max((len(d) for d in deps.values()), default=0)
    k_max_file = max(deps.keys(), key=lambda k: len(deps[k]), default="")

    in_degree: dict[str, int] = defaultdict(int)
    for mod, imports in deps.items():
        for imp in imports:
            in_degree[imp] += 1

    cycles = detect_cycles(deps)
    cycle_count = len(cycles)
    composite = k_avg * n + cycle_count
    burden = cycle_count + 0.1 * n

    hub_pct = k_max / k_total if k_total > 0 else 0
    arch = classify_architecture(n, k_avg, k_max, cycle_count, hub_pct)
    total_loc = sum(f["loc"] for f in file_info.values())

    return {
        "package": package_name,
        "path": str(pkg_path),
        "n": n,
        "k_total": k_total,
        "k_avg": round(k_avg, 2),
        "k_n": round(k_n, 3),
        "k_max": k_max,
        "k_max_file": k_max_file,
        "cycles": cycle_count,
        "cycle_details": [" → ".join(c) for c in cycles],
        "composite": round(composite, 1),
        "burden": round(burden, 1),
        "architecture": arch,
        "hub_pct": round(hub_pct, 2),
        "total_loc": total_loc,
        "modules": file_info,
        "in_degree": dict(in_degree),
    }


def compare_refs(repo_path: str, pkg_subpath: str, package_name: str,
                 ref1: str, ref2: str, as_json: bool = False) -> dict:
    """Compare NK metrics of a package between two git refs.

    Checks out each ref, runs analyze_path, and computes deltas.
    Restores the original HEAD when done.
    """
    repo = Path(repo_path).resolve()
    if not (repo / ".git").exists():
        return {"error": f"{repo} is not a git repository"}

    # Save current state
    orig_ref = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "HEAD"],
        cwd=repo, capture_output=True, text=True
    ).stdout.strip()
    if orig_ref == "HEAD":
        orig_ref = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=repo, capture_output=True, text=True
        ).stdout.strip()

    results = {}
    for label, ref in [("before", ref1), ("after", ref2)]:
        subprocess.run(
            ["git", "checkout", ref, "--force"],
            cwd=repo, capture_output=True, text=True
        )
        pkg_path = repo / pkg_subpath
        if not pkg_path.is_dir():
            results[label] = {"error": f"Path {pkg_subpath} not found at ref {ref}"}
        else:
            results[label] = analyze_path(pkg_path, package_name)
        results[label]["ref"] = ref

    # Restore original state
    subprocess.run(
        ["git", "checkout", orig_ref, "--force"],
        cwd=repo, capture_output=True, text=True
    )

    # Compute deltas
    before = results["before"]
    after = results["after"]

    if "error" in before or "error" in after:
        return {"before": before, "after": after, "error": "Analysis failed for one or both refs"}

    delta_keys = ["n", "k_total", "k_avg", "k_n", "k_max", "cycles", "composite", "total_loc"]
    deltas = {}
    for key in delta_keys:
        b_val = before.get(key, 0)
        a_val = after.get(key, 0)
        deltas[key] = round(a_val - b_val, 3) if isinstance(a_val, float) else a_val - b_val

    return {
        "package": package_name,
        "ref_before": ref1,
        "ref_after": ref2,
        "before": before,
        "after": after,
        "delta": deltas,
    }


def print_compare_report(result: dict):
    """Print a human-readable ΔNK comparison report."""
    if "error" in result:
        print(f"ERROR: {result['error']}")
        if "before" in result:
            print(f"  Before ({result.get('ref_before', '?')}): {result['before'].get('error', 'OK')}")
            print(f"  After  ({result.get('ref_after', '?')}): {result['after'].get('error', 'OK')}")
        return

    b = result["before"]
    a = result["after"]
    d = result["delta"]
    pkg = result["package"]

    print(f"\n=== ΔNK COMPARISON: {pkg} ===")
    print(f"  Before: {result['ref_before']}")
    print(f"  After:  {result['ref_after']}")
    print()

    def fmt_delta(val, lower_is_better=True):
        if val == 0:
            return "  0"
        sign = "+" if val > 0 else ""
        indicator = ""
        if lower_is_better:
            indicator = " WORSE" if val > 0 else " BETTER"
        else:
            indicator = " BETTER" if val > 0 else " WORSE"
        return f"{sign}{val}{indicator}"

    headers = [
        ("N (modules)", "n", False),
        ("K_total (edges)", "k_total", True),
        ("K_avg", "k_avg", True),
        ("K/N", "k_n", True),
        ("K_max", "k_max", True),
        ("Cycles", "cycles", True),
        ("Composite", "composite", True),
        ("Total LOC", "total_loc", False),
    ]

    print(f"  {'Metric':<20} {'Before':>10} {'After':>10} {'Delta':>15}")
    print("  " + "-" * 58)
    for label, key, lower_better in headers:
        b_val = b.get(key, 0)
        a_val = a.get(key, 0)
        d_val = d.get(key, 0)
        print(f"  {label:<20} {b_val:>10} {a_val:>10} {fmt_delta(d_val, lower_better):>15}")
    print()

    # Architecture change
    b_arch = b.get("architecture", "?")
    a_arch = a.get("architecture", "?")
    if b_arch != a_arch:
        print(f"  Architecture: {b_arch} → {a_arch}")
    else:
        print(f"  Architecture: {b_arch} (unchanged)")
    print()

    # Cycle details comparison
    b_cycles = set(b.get("cycle_details", []))
    a_cycles = set(a.get("cycle_details", []))
    removed = b_cycles - a_cycles
    added = a_cycles - b_cycles
    if removed:
        print(f"  Cycles REMOVED ({len(removed)}):")
        for c in sorted(removed):
            print(f"    - {c}")
    if added:
        print(f"  Cycles ADDED ({len(added)}):")
        for c in sorted(added):
            print(f"    + {c}")
    if not removed and not added:
        if b.get("cycles", 0) == 0:
            print("  No cycles in either version.")
        else:
            print("  Same cycles in both versions.")
    print()

    # Verdict
    composite_improved = d["composite"] < 0
    cycles_improved = d["cycles"] <= 0
    if composite_improved and cycles_improved:
        verdict = "STRUCTURAL IMPROVEMENT — composite and cycles both reduced"
    elif composite_improved:
        verdict = "MIXED — composite improved but cycles increased"
    elif cycles_improved and d["cycles"] < 0:
        verdict = "MIXED — cycles reduced but composite increased"
    elif d["composite"] == 0 and d["cycles"] == 0:
        verdict = "NEUTRAL — no structural change detected"
    else:
        verdict = "STRUCTURAL DEGRADATION — complexity increased"
    print(f"  VERDICT: {verdict}")


def batch_lazy_analyze(packages: list[str]):
    """Analyze lazy imports across multiple packages for F44 hypothesis testing."""
    results = []
    for pkg in packages:
        r = analyze_lazy_imports(pkg)
        if "error" not in r:
            results.append(r)
        else:
            print(f"  SKIP: {pkg} — {r['error']}")

    if not results:
        print("No packages analyzed successfully.")
        return

    print(f"\n{'Package':<20} {'Lazy':>5} {'CycBrk':>7} {'NonCyc':>7} {'StatCyc':>8} {'RunCyc':>7} {'Hidden':>7}  F44")
    print("-" * 85)
    supports = 0
    partial = 0
    refutes = 0
    no_lazy = 0
    for r in results:
        verdict = r["hypothesis_f44"]
        print(
            f"{r['package']:<20} {r['total_lazy_imports']:>5} {r['cycle_breaking_lazy']:>7} "
            f"{r['non_cycle_breaking_lazy']:>7} {r['static_cycles']:>8} {r['runtime_cycles']:>7} "
            f"{r['hidden_cycles']:>7}  {verdict}"
        )
        if verdict == "SUPPORTS":
            supports += 1
        elif verdict == "PARTIAL":
            partial += 1
        elif verdict == "REFUTES":
            refutes += 1
        else:
            no_lazy += 1

    total = len(results)
    testable = total - no_lazy
    print(f"\nSummary: {total} packages, {testable} testable (have lazy imports)")
    if testable > 0:
        print(f"  SUPPORTS: {supports}/{testable} ({supports*100//testable}%)")
        print(f"  PARTIAL:  {partial}/{testable}")
        print(f"  REFUTES:  {refutes}/{testable}")
    print(f"  NO_LAZY:  {no_lazy}/{total}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    package_name = sys.argv[1]
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    as_json = "--json" in sys.argv
    refactor = "--suggest-refactor" in sys.argv or "--refactor" in sys.argv
    lazy = "--lazy" in sys.argv

    if package_name == "compare":
        # Compare mode: analyze a package at two git refs
        args = sys.argv[2:]
        repo_path = None
        pkg_subpath = None
        pkg_name = None
        positional = []
        i = 0
        while i < len(args):
            if args[i] == "--repo" and i + 1 < len(args):
                repo_path = args[i + 1]
                i += 2
            elif args[i] == "--pkg" and i + 1 < len(args):
                pkg_subpath = args[i + 1]
                i += 2
            elif args[i] == "--name" and i + 1 < len(args):
                pkg_name = args[i + 1]
                i += 2
            elif not args[i].startswith("-"):
                positional.append(args[i])
                i += 1
            else:
                i += 1

        if not repo_path or not pkg_subpath or len(positional) < 2:
            print("Usage: nk_analyze.py compare --repo <path> --pkg <subpath> --name <name> <ref1> <ref2>")
            sys.exit(1)

        if not pkg_name:
            pkg_name = Path(pkg_subpath).name

        ref1, ref2 = positional[0], positional[1]
        result = compare_refs(repo_path, pkg_subpath, pkg_name, ref1, ref2, as_json)

        if as_json:
            print(json_mod.dumps(result, indent=2, default=str))
        else:
            print_compare_report(result)
        return

    if package_name == "batch":
        # Batch mode: analyze all remaining args as package names
        packages = [a for a in sys.argv[2:] if not a.startswith("-")]
        if not packages:
            # Default: scan interesting stdlib packages
            packages = [
                "json", "logging", "http", "unittest", "email",
                "asyncio", "multiprocessing", "xml", "sqlite3",
                "urllib", "collections", "importlib",
            ]
        if lazy:
            batch_lazy_analyze(packages)
        else:
            batch_analyze(packages)
        return

    if lazy:
        lazy_result = analyze_lazy_imports(package_name)
        if as_json:
            print(json_mod.dumps(lazy_result, indent=2))
        else:
            print_lazy_report(lazy_result)
        return

    result = analyze_package(package_name, verbose)

    if as_json:
        print(json_mod.dumps(result, indent=2))
    else:
        print_report(result, verbose)
        if refactor:
            suggest_refactor(result)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
nk_analyze.py — Automated NK landscape analysis for Python packages.

Usage:
    python3 tools/nk_analyze.py <package_name>
    python3 tools/nk_analyze.py <package_name> --json
    python3 tools/nk_analyze.py <package_name> --verbose

Analyzes internal dependencies of a Python package and computes:
- N (number of modules), K_total (edges), K_avg, K/N, K_max
- Cycle detection
- Composite score: K_avg * N + Cycles
- Architecture classification (facade, monolith, framework, registry)

Examples:
    python3 tools/nk_analyze.py json
    python3 tools/nk_analyze.py email --verbose
    python3 tools/nk_analyze.py asyncio --json
"""

import ast
import importlib
import json as json_mod
import os
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
    pkg_root = filepath
    while pkg_root.parent.name != package_name and pkg_root.parent != pkg_root:
        pkg_root = pkg_root.parent
    pkg_base = pkg_root.parent  # Directory containing the package

    internal_imports = set()

    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module and node.level == 0:
                # Absolute import: from package.module import ...
                parts = node.module.split(".")
                if parts[0] == package_name and len(parts) > 1:
                    # Could be "from email.mime import text" or "from email.charset import ..."
                    sub_module = ".".join(parts[1:])
                    internal_imports.add(sub_module)
                    # Also try just the first part (e.g., "charset" from "email.charset")
                    if len(parts) > 2:
                        internal_imports.add(parts[1])
            elif node.level >= 1:
                # Relative import: from .module import ... or from ..module import ...
                if node.module:
                    # Resolve relative to current file's position
                    rel_dir = filepath.parent
                    for _ in range(node.level - 1):
                        rel_dir = rel_dir.parent
                    parts = node.module.split(".")
                    # Compute dotted name relative to package root
                    try:
                        prefix = rel_dir.relative_to(pkg_base / package_name)
                        if str(prefix) == ".":
                            dotted = ".".join(parts)
                        else:
                            dotted = str(prefix).replace(os.sep, ".") + "." + ".".join(parts)
                    except ValueError:
                        dotted = ".".join(parts)
                    internal_imports.add(dotted)
                    # Also add just the top-level part
                    if len(parts) > 0:
                        try:
                            prefix = rel_dir.relative_to(pkg_base / package_name)
                            if str(prefix) == ".":
                                internal_imports.add(parts[0])
                            else:
                                internal_imports.add(str(prefix).replace(os.sep, ".") + "." + parts[0])
                        except ValueError:
                            internal_imports.add(parts[0])
                elif node.names:
                    # from . import name1, name2
                    rel_dir = filepath.parent
                    for _ in range(node.level - 1):
                        rel_dir = rel_dir.parent
                    for alias in node.names:
                        try:
                            prefix = rel_dir.relative_to(pkg_base / package_name)
                            if str(prefix) == ".":
                                internal_imports.add(alias.name)
                            else:
                                internal_imports.add(str(prefix).replace(os.sep, ".") + "." + alias.name)
                        except ValueError:
                            internal_imports.add(alias.name)

        elif isinstance(node, ast.Import):
            for alias in node.names:
                parts = alias.name.split(".")
                if parts[0] == package_name and len(parts) > 1:
                    internal_imports.add(".".join(parts[1:]))

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

    # Composite score
    composite = k_avg * n + cycle_count

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
        "architecture": arch,
        "hub_pct": round(hub_pct, 2),
        "total_loc": total_loc,
        "modules": file_info,
        "in_degree": dict(in_degree),
    }

    return result


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
        ("logging", "Py", 3.0),
        ("json", "Py", 4.0),
        ("Express 5", "JS", 6.0),
        ("Express 4", "JS", 15.0),
        ("http.client", "Py", 26.4),
        ("unittest", "Py", 27.0),
        ("argparse", "Py", 48.1),
        ("email", "Py", 61.1),
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


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    package_name = sys.argv[1]
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    as_json = "--json" in sys.argv

    result = analyze_package(package_name, verbose)

    if as_json:
        print(json_mod.dumps(result, indent=2))
    else:
        print_report(result, verbose)


if __name__ == "__main__":
    main()

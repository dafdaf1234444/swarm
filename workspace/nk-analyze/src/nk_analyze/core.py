"""Core NK analysis functions."""

import ast
import importlib
import os
from collections import defaultdict
from pathlib import Path


def find_package_path(package_name: str) -> Path | None:
    """Find the filesystem path of a Python package."""
    try:
        mod = importlib.import_module(package_name)
        if hasattr(mod, "__path__"):
            return Path(mod.__path__[0])
        return None
    except ImportError:
        return None


def list_modules(pkg_path: Path) -> dict[str, Path]:
    """List all .py module files in a package recursively."""
    modules = {}
    skip_dirs = {"__pycache__", "tests", "test", "_vendor"}

    for root, dirs, files in os.walk(pkg_path):
        dirs[:] = [d for d in dirs if d not in skip_dirs]
        rel_dir = Path(root).relative_to(pkg_path)

        for f in sorted(files):
            if not f.endswith(".py"):
                continue
            stem = f[:-3]
            if rel_dir == Path("."):
                mod_name = stem
            else:
                mod_name = str(rel_dir / stem).replace(os.sep, ".")

            if mod_name.endswith(".__init__"):
                mod_name = mod_name[:-9]

            modules[mod_name] = Path(root) / f

    return modules


def _resolve_import_name(node, filepath, package_name, pkg_base):
    """Resolve an import AST node to internal module names."""
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


def extract_imports_layered(filepath: Path, package_name: str) -> dict:
    """Extract imports categorized by scope: top-level vs lazy (inside functions).

    Returns {"top_level": [...], "lazy": [...], "lazy_locations": [...]}
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
        for child in ast.iter_child_nodes(node):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef)):
                _walk_scope(child, enclosing_func=child.name)
            elif isinstance(child, ast.ClassDef):
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
    """Extract internal imports from a Python file using AST parsing."""
    try:
        source = filepath.read_text(encoding="utf-8", errors="replace")
        tree = ast.parse(source)
    except (SyntaxError, ValueError):
        return []

    pkg_root = filepath
    while pkg_root.parent.name != package_name and pkg_root.parent != pkg_root:
        pkg_root = pkg_root.parent
    pkg_base = pkg_root.parent.parent

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
                cycle_start = path.index(neighbor)
                cycle = path[cycle_start:] + [neighbor]
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


def analyze_lazy_imports(package_name: str) -> dict:
    """Analyze lazy vs top-level imports and their effect on cycles."""
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

    cycle_breaking = []
    for lazy_imp in all_lazy:
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


def analyze_package(package_name: str, verbose: bool = False) -> dict:
    """Perform full NK analysis on a Python package."""
    pkg_path = find_package_path(package_name)
    if not pkg_path:
        return {"error": f"'{package_name}' is a single-file module or not found"}

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
        "architecture": arch,
        "hub_pct": round(hub_pct, 2),
        "total_loc": total_loc,
        "modules": file_info,
        "in_degree": dict(in_degree),
    }

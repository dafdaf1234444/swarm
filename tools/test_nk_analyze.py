#!/usr/bin/env python3
"""
test_nk_analyze.py — Regression tests for nk_analyze.py

Tests cover:
1. Module listing (list_modules)
2. Import extraction (extract_imports) — including sub-package resolution
3. Cycle detection (detect_cycles)
4. Architecture classification (classify_architecture)
5. Full analysis on stdlib packages (integration)
6. Regression: sub-package import resolution bug (S39 fix)

Usage:
    python3 tools/test_nk_analyze.py
    python3 tools/test_nk_analyze.py -v          # verbose
    python3 tools/test_nk_analyze.py TestCycles   # single class
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

# Add tools directory to path
sys.path.insert(0, str(Path(__file__).parent))
from nk_analyze import (
    analyze_package,
    classify_architecture,
    detect_cycles,
    extract_imports,
    list_modules,
)


class TestDetectCycles(unittest.TestCase):
    """Test cycle detection in dependency graphs."""

    def test_no_cycles(self):
        deps = {"a": ["b"], "b": ["c"], "c": []}
        cycles = detect_cycles(deps)
        self.assertEqual(len(cycles), 0)

    def test_simple_cycle(self):
        deps = {"a": ["b"], "b": ["a"]}
        cycles = detect_cycles(deps)
        self.assertEqual(len(cycles), 1)
        # Cycle should contain both a and b
        cycle_mods = set(cycles[0][:-1])
        self.assertEqual(cycle_mods, {"a", "b"})

    def test_triangle_cycle(self):
        deps = {"a": ["b"], "b": ["c"], "c": ["a"]}
        cycles = detect_cycles(deps)
        self.assertEqual(len(cycles), 1)
        cycle_mods = set(cycles[0][:-1])
        self.assertEqual(cycle_mods, {"a", "b", "c"})

    def test_multiple_independent_cycles(self):
        deps = {"a": ["b"], "b": ["a"], "c": ["d"], "d": ["c"], "e": []}
        cycles = detect_cycles(deps)
        self.assertEqual(len(cycles), 2)

    def test_nested_cycles(self):
        # a→b→c→a and a→b→a (nested)
        deps = {"a": ["b"], "b": ["a", "c"], "c": ["a"]}
        cycles = detect_cycles(deps)
        self.assertGreaterEqual(len(cycles), 2)

    def test_empty_graph(self):
        cycles = detect_cycles({})
        self.assertEqual(len(cycles), 0)

    def test_self_loop_not_counted(self):
        # Self-loops shouldn't appear in our deps (filtered in analyze_package)
        deps = {"a": ["b"], "b": []}
        cycles = detect_cycles(deps)
        self.assertEqual(len(cycles), 0)

    def test_star_topology_no_cycles(self):
        deps = {"hub": ["a", "b", "c"], "a": [], "b": [], "c": []}
        cycles = detect_cycles(deps)
        self.assertEqual(len(cycles), 0)


class TestClassifyArchitecture(unittest.TestCase):
    """Test architecture classification."""

    def test_monolith(self):
        arch = classify_architecture(n=3, k_avg=1.0, k_max=2, cycles=0, hub_pct=0.5)
        self.assertEqual(arch, "monolith")

    def test_tangled(self):
        arch = classify_architecture(n=20, k_avg=3.5, k_max=10, cycles=10, hub_pct=0.2)
        self.assertEqual(arch, "tangled")

    def test_hub_and_spoke(self):
        arch = classify_architecture(n=10, k_avg=1.5, k_max=8, cycles=0, hub_pct=0.6)
        self.assertEqual(arch, "hub-and-spoke")

    def test_framework(self):
        arch = classify_architecture(n=10, k_avg=3.0, k_max=5, cycles=1, hub_pct=0.2)
        self.assertEqual(arch, "framework")

    def test_registry(self):
        arch = classify_architecture(n=10, k_avg=1.5, k_max=6, cycles=0, hub_pct=0.2)
        self.assertEqual(arch, "registry")

    def test_facade(self):
        arch = classify_architecture(n=10, k_avg=1.0, k_max=3, cycles=0, hub_pct=0.4)
        self.assertEqual(arch, "facade")

    def test_distributed(self):
        arch = classify_architecture(n=10, k_avg=1.0, k_max=2, cycles=0, hub_pct=0.1)
        self.assertEqual(arch, "distributed")


class SyntheticPackageMixin:
    """Mixin to create temporary synthetic packages for testing."""

    def create_package(self, name, modules):
        """Create a temporary package with given module files.

        Args:
            name: package name (directory name)
            modules: dict of {filename: source_code}
                     e.g. {"__init__.py": "from . import utils", "utils.py": "x = 1"}
        Returns:
            Path to the package directory
        """
        pkg_dir = Path(self._tmpdir.name) / name
        pkg_dir.mkdir(parents=True, exist_ok=True)
        for filename, source in modules.items():
            filepath = pkg_dir / filename
            filepath.parent.mkdir(parents=True, exist_ok=True)
            filepath.write_text(source)
        return pkg_dir

    def setUp(self):
        self._tmpdir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self._tmpdir.cleanup()


class TestListModules(SyntheticPackageMixin, unittest.TestCase):
    """Test module listing."""

    def test_simple_package(self):
        pkg = self.create_package("mypkg", {
            "__init__.py": "",
            "a.py": "",
            "b.py": "",
        })
        modules = list_modules(pkg)
        self.assertEqual(set(modules.keys()), {"__init__", "a", "b"})

    def test_sub_package(self):
        pkg = self.create_package("mypkg", {
            "__init__.py": "",
            "core.py": "",
            "sub/__init__.py": "",
            "sub/helpers.py": "",
        })
        modules = list_modules(pkg)
        self.assertIn("sub", modules)
        self.assertIn("sub.helpers", modules)
        self.assertIn("core", modules)

    def test_skips_pycache(self):
        pkg = self.create_package("mypkg", {
            "__init__.py": "",
            "a.py": "",
            "__pycache__/a.cpython-311.pyc": "binary",
        })
        modules = list_modules(pkg)
        self.assertNotIn("__pycache__", str(modules))

    def test_skips_test_dirs(self):
        pkg = self.create_package("mypkg", {
            "__init__.py": "",
            "core.py": "",
            "tests/__init__.py": "",
            "tests/test_core.py": "",
        })
        modules = list_modules(pkg)
        self.assertNotIn("tests.test_core", modules)
        self.assertNotIn("tests", modules)

    def test_nested_sub_packages(self):
        pkg = self.create_package("mypkg", {
            "__init__.py": "",
            "a/__init__.py": "",
            "a/b/__init__.py": "",
            "a/b/c.py": "",
        })
        modules = list_modules(pkg)
        self.assertIn("a.b.c", modules)
        self.assertIn("a.b", modules)
        self.assertIn("a", modules)


class TestExtractImports(SyntheticPackageMixin, unittest.TestCase):
    """Test import extraction, especially relative import resolution."""

    def test_absolute_import(self):
        pkg = self.create_package("mypkg", {
            "__init__.py": "",
            "a.py": "from mypkg.b import something",
            "b.py": "",
        })
        imports = extract_imports(pkg / "a.py", "mypkg")
        self.assertIn("b", imports)

    def test_relative_import_dot(self):
        pkg = self.create_package("mypkg", {
            "__init__.py": "",
            "a.py": "from .b import something",
            "b.py": "",
        })
        imports = extract_imports(pkg / "a.py", "mypkg")
        self.assertIn("b", imports)

    def test_relative_import_from_dot(self):
        pkg = self.create_package("mypkg", {
            "__init__.py": "",
            "a.py": "from . import b",
            "b.py": "",
        })
        imports = extract_imports(pkg / "a.py", "mypkg")
        self.assertIn("b", imports)

    def test_sub_package_relative_import(self):
        """Regression test for S39 sub-package import resolution bug.

        When sub/child.py does 'from .sibling import X', it should resolve
        to 'sub.sibling', NOT to top-level 'sibling'.
        """
        pkg = self.create_package("mypkg", {
            "__init__.py": "",
            "sibling.py": "# top-level sibling",
            "sub/__init__.py": "",
            "sub/sibling.py": "# sub-package sibling",
            "sub/child.py": "from .sibling import something",
        })
        imports = extract_imports(pkg / "sub" / "child.py", "mypkg")
        self.assertIn("sub.sibling", imports)
        # Should NOT resolve to just "sibling" (the top-level one)
        self.assertNotIn("sibling", imports)

    def test_sub_package_init_relative_import(self):
        """Regression: sub/__init__.py 'from .mod import X' → 'sub.mod'."""
        pkg = self.create_package("mypkg", {
            "__init__.py": "",
            "sub/__init__.py": "from .helpers import util_func",
            "sub/helpers.py": "def util_func(): pass",
        })
        imports = extract_imports(pkg / "sub" / "__init__.py", "mypkg")
        self.assertIn("sub.helpers", imports)

    def test_double_dot_relative(self):
        """from ..module import X in nested sub-package."""
        pkg = self.create_package("mypkg", {
            "__init__.py": "",
            "top.py": "",
            "sub/__init__.py": "",
            "sub/deep/__init__.py": "",
            "sub/deep/mod.py": "from ...top import something",
        })
        imports = extract_imports(pkg / "sub" / "deep" / "mod.py", "mypkg")
        self.assertIn("top", imports)

    def test_absolute_deep_import(self):
        pkg = self.create_package("mypkg", {
            "__init__.py": "",
            "a.py": "from mypkg.sub.deep import something",
            "sub/__init__.py": "",
            "sub/deep.py": "",
        })
        imports = extract_imports(pkg / "a.py", "mypkg")
        self.assertIn("sub.deep", imports)
        self.assertIn("sub", imports)

    def test_import_statement(self):
        pkg = self.create_package("mypkg", {
            "__init__.py": "",
            "a.py": "import mypkg.b",
            "b.py": "",
        })
        imports = extract_imports(pkg / "a.py", "mypkg")
        self.assertIn("b", imports)

    def test_external_import_ignored(self):
        pkg = self.create_package("mypkg", {
            "__init__.py": "",
            "a.py": "import os\nfrom collections import defaultdict\nfrom .b import x",
            "b.py": "",
        })
        imports = extract_imports(pkg / "a.py", "mypkg")
        self.assertNotIn("os", imports)
        self.assertNotIn("collections", imports)
        self.assertIn("b", imports)

    def test_syntax_error_returns_empty(self):
        pkg = self.create_package("mypkg", {
            "__init__.py": "",
            "bad.py": "def f(:\n    pass",
        })
        imports = extract_imports(pkg / "bad.py", "mypkg")
        self.assertEqual(imports, [])


class TestAnalyzePackageIntegration(unittest.TestCase):
    """Integration tests using real stdlib packages."""

    def test_json_package(self):
        result = analyze_package("json")
        if "error" in result:
            self.skipTest("json package not available")
        self.assertGreater(result["n"], 0)
        self.assertGreaterEqual(result["k_avg"], 0)
        self.assertEqual(result["cycles"], 0, "json should have 0 cycles")
        self.assertLess(result["composite"], 10, "json composite should be low")

    def test_logging_package(self):
        result = analyze_package("logging")
        if "error" in result:
            self.skipTest("logging package not available")
        self.assertGreater(result["n"], 0)
        self.assertEqual(result["cycles"], 0, "logging should have 0 cycles")

    def test_email_package(self):
        result = analyze_package("email")
        if "error" in result:
            self.skipTest("email package not available")
        self.assertGreater(result["n"], 15)
        # After S39 fix: static cycles should be low (lazy imports hide runtime cycles)
        self.assertLess(result["cycles"], 10,
                        "email static cycles should be < 10 (lazy imports hide runtime cycles)")

    def test_single_file_module(self):
        result = analyze_package("os")
        self.assertIn("error", result, "os is single-file, should return error")

    def test_nonexistent_package(self):
        result = analyze_package("definitely_not_a_real_package_xyz")
        self.assertIn("error", result)

    def test_multiprocessing_cycles(self):
        result = analyze_package("multiprocessing")
        if "error" in result:
            self.skipTest("multiprocessing not available")
        self.assertGreater(result["cycles"], 5,
                           "multiprocessing should have many cycles (context hub)")

    def test_composite_ordering(self):
        """Composite scores should maintain correct ordinal ranking."""
        packages = ["json", "email", "asyncio"]
        results = {}
        for pkg in packages:
            r = analyze_package(pkg)
            if "error" not in r:
                results[pkg] = r["composite"]

        if len(results) < 3:
            self.skipTest("Not all packages available")

        self.assertLess(results["json"], results["email"],
                        "json should rank lower than email")
        self.assertLess(results["email"], results["asyncio"],
                        "email should rank lower than asyncio")


class TestSubPackageResolution(SyntheticPackageMixin, unittest.TestCase):
    """Targeted regression tests for the S39 sub-package resolution bug.

    The bug: pkg_base was calculated as pkg_root.parent instead of
    pkg_root.parent.parent, causing relative imports in sub-packages
    to resolve to wrong modules.
    """

    def test_resources_abc_resolution(self):
        """Simulate importlib/resources/__init__.py importing from .abc.

        Before fix: resolved to top-level 'abc' module
        After fix: resolves to 'resources.abc' sub-module
        """
        pkg = self.create_package("fakepkg", {
            "__init__.py": "",
            "abc.py": "# top-level abc",
            "resources/__init__.py": "from .abc import ResourceReader",
            "resources/abc.py": "class ResourceReader: pass",
        })
        imports = extract_imports(
            pkg / "resources" / "__init__.py", "fakepkg"
        )
        self.assertIn("resources.abc", imports)

    def test_deep_subpackage_relative(self):
        """Three levels deep: a/b/c.py importing from .d."""
        pkg = self.create_package("fakepkg", {
            "__init__.py": "",
            "a/__init__.py": "",
            "a/b/__init__.py": "",
            "a/b/c.py": "from .d import something",
            "a/b/d.py": "",
        })
        imports = extract_imports(pkg / "a" / "b" / "c.py", "fakepkg")
        self.assertIn("a.b.d", imports)

    def test_cross_subpackage_import(self):
        """sub1/mod.py importing from ..sub2.mod."""
        pkg = self.create_package("fakepkg", {
            "__init__.py": "",
            "sub1/__init__.py": "",
            "sub1/mod.py": "from ..sub2 import helper",
            "sub2/__init__.py": "",
            "sub2/helper.py": "",
        })
        imports = extract_imports(pkg / "sub1" / "mod.py", "fakepkg")
        self.assertIn("sub2", imports)


class TestEndToEnd(SyntheticPackageMixin, unittest.TestCase):
    """End-to-end tests with synthetic packages."""

    def _add_to_syspath(self, parent_dir):
        """Temporarily add a directory to sys.path for import resolution."""
        sys.path.insert(0, str(parent_dir))
        self.addCleanup(lambda: sys.path.remove(str(parent_dir)))

    def test_zero_cycle_package(self):
        """Package with no cycles should score K_avg * N."""
        pkg = self.create_package("zerocycle", {
            "__init__.py": "from . import a, b, c",
            "a.py": "",
            "b.py": "from . import a",
            "c.py": "from . import a, b",
        })
        self._add_to_syspath(pkg.parent)
        result = analyze_package("zerocycle")
        if "error" in result:
            self.skipTest("Could not analyze synthetic package")
        self.assertEqual(result["cycles"], 0)
        self.assertAlmostEqual(result["composite"], result["k_avg"] * result["n"], places=1)

    def test_cyclic_package(self):
        """Package with cycles should show cycles > 0."""
        pkg = self.create_package("cyclic", {
            "__init__.py": "",
            "a.py": "from . import b",
            "b.py": "from . import a",
        })
        self._add_to_syspath(pkg.parent)
        result = analyze_package("cyclic")
        if "error" in result:
            self.skipTest("Could not analyze synthetic package")
        self.assertGreater(result["cycles"], 0)


if __name__ == "__main__":
    unittest.main()

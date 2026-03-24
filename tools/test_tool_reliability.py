#!/usr/bin/env python3
"""Regression tests for tool_reliability.py substrate filtering."""

import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).parent))

import tool_reliability as mod


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class TestToolReliabilityScope(unittest.TestCase):
    def test_default_scope_excludes_test_modules(self):
        with tempfile.TemporaryDirectory() as td:
            tools_dir = Path(td) / "tools"
            lessons_dir = Path(td) / "memory" / "lessons"
            _write(tools_dir / "alpha.py", "print('alpha')\n")
            _write(tools_dir / "beta.py", "print('beta')\n")
            _write(tools_dir / "test_alpha.py", "import alpha\n")
            _write(lessons_dir / "L-900.md", "# L-900\nTool: alpha.py\n")

            with patch.object(mod, "TOOLS_DIR", tools_dir), patch.object(mod, "LESSON_DIR", lessons_dir):
                names = [tool["name"] for tool in mod.discover_tools()]
                self.assertEqual(names, ["alpha.py", "beta.py"])

                graph = mod.compute_import_graph()
                self.assertNotIn("alpha.py", graph, "test modules should not count as downstream readers by default")

                data = mod.audit_tools()
                self.assertEqual(data["n_tools"], 2)
                self.assertEqual(data["n_test_modules_excluded"], 1)

    def test_include_tests_restores_broad_audit_scope(self):
        with tempfile.TemporaryDirectory() as td:
            tools_dir = Path(td) / "tools"
            lessons_dir = Path(td) / "memory" / "lessons"
            _write(tools_dir / "alpha.py", "print('alpha')\n")
            _write(tools_dir / "test_alpha.py", "import alpha\n")
            _write(lessons_dir / "L-901.md", "# L-901\nTool: alpha.py\n")

            with patch.object(mod, "TOOLS_DIR", tools_dir), patch.object(mod, "LESSON_DIR", lessons_dir):
                names = [tool["name"] for tool in mod.discover_tools(include_tests=True)]
                self.assertEqual(names, ["alpha.py", "test_alpha.py"])

                graph = mod.compute_import_graph(include_tests=True)
                self.assertIn("alpha.py", graph)
                self.assertIn("test_alpha.py", graph["alpha.py"])


if __name__ == "__main__":
    unittest.main()

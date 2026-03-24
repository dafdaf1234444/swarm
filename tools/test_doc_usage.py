#!/usr/bin/env python3
"""Regression tests for doc_usage.py."""

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import doc_usage  # noqa: E402


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


class TestDocUsage(unittest.TestCase):
    def test_collect_doc_usage_classifies_reference_sources(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)

            write(root / "docs" / "LIVE.md", "# Live\n")
            write(root / "docs" / "DOC-ONLY.md", "# Doc-only\n")
            write(root / "docs" / "HIST-S123.md", "# Historical\n")
            write(root / "docs" / "ORPHAN.md", "# Orphan\n")
            write(root / "README.md", "See docs/LIVE.md\n")
            write(root / "memory" / "INDEX.md", "Operational ref docs/LIVE.md\n")
            write(root / "docs" / "INDEX.md", "Doc cluster docs/DOC-ONLY.md\n")
            write(root / "tasks" / "NEXT-ARCHIVE.md", "Old ref docs/HIST-S123.md\n")

            reports = {
                report["doc"]: report
                for report in doc_usage.collect_doc_usage(root)
            }

            live = reports["docs/LIVE.md"]
            self.assertEqual(live["entry_refs"], 1)
            self.assertEqual(live["operational_refs"], 1)
            self.assertEqual(live["status"], "live")
            self.assertEqual(live["recommendation"], "keep")

            doc_only = reports["docs/DOC-ONLY.md"]
            self.assertEqual(doc_only["doc_refs"], 1)
            self.assertEqual(doc_only["status"], "non-live")
            self.assertEqual(doc_only["recommendation"], "index-or-merge")

            hist = reports["docs/HIST-S123.md"]
            self.assertEqual(hist["archive_refs"], 1)
            self.assertTrue(hist["historical_name"])
            self.assertEqual(hist["recommendation"], "archive-candidate")

            orphan = reports["docs/ORPHAN.md"]
            self.assertEqual(orphan["recommendation"], "orphaned")
            self.assertEqual(orphan["status"], "non-live")


if __name__ == "__main__":
    unittest.main()

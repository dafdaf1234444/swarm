#!/usr/bin/env python3
"""Compatibility shim for the archived testimony calibration tool.

Historical notes and artifacts still point at ``tools/testimony_calibration.py``.
The implementation was archived to ``tools/archive/testimony_calibration.py``.
Keep the legacy entrypoint alive so those references remain executable.
"""

from __future__ import annotations

import runpy
from pathlib import Path


ARCHIVED_TOOL = Path(__file__).with_name("archive") / "testimony_calibration.py"


def main() -> None:
    runpy.run_path(str(ARCHIVED_TOOL), run_name="__main__")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""cite_parse.py — Shared citation parser with typed edge support (L-1292).

Recognizes both legacy Cites: and typed relation headers:
  Supports: L-601, P-011    → edge type SUPPORTS
  Contradicts: L-500        → edge type CONTRADICTS
  Extends: L-450            → edge type EXTENDS
  Requires: L-300           → edge type REQUIRES
  Cites: L-100, L-200       → edge type CITES (untyped, backward compat)

All tools that parse citations can import this instead of rolling their own regex.

Usage:
  from cite_parse import parse_lesson_citations, CitedRef

  refs = parse_lesson_citations(lesson_text)
  # refs = [CitedRef("L-601", "SUPPORTS"), CitedRef("L-500", "CONTRADICTS"), ...]

  # Legacy mode (flat set of IDs, backward compat):
  from cite_parse import parse_lesson_ids
  ids = parse_lesson_ids(lesson_text)
  # ids = {"L-601", "L-500", "L-450", ...}
"""

import re
from dataclasses import dataclass
from typing import List, Set

# Typed header patterns — order matters (most specific first)
TYPED_HEADERS = [
    ("SUPPORTS", re.compile(r"^\*{0,2}Supports\*{0,2}:\s*(.+)", re.MULTILINE)),
    ("CONTRADICTS", re.compile(r"^\*{0,2}Contradicts\*{0,2}:\s*(.+)", re.MULTILINE)),
    ("EXTENDS", re.compile(r"^\*{0,2}Extends\*{0,2}:\s*(.+)", re.MULTILINE)),
    ("REQUIRES", re.compile(r"^\*{0,2}Requires\*{0,2}:\s*(.+)", re.MULTILINE)),
    ("CITES", re.compile(r"^\*{0,2}Cites?\*{0,2}:\s*(.+)", re.MULTILINE)),
]

# Generic ref patterns
L_RE = re.compile(r"\bL-(\d+)\b")
P_RE = re.compile(r"\bP-(\d+)\b")
F_RE = re.compile(r"\bF-([A-Z][A-Z0-9-]+\d*)\b")


@dataclass(frozen=True)
class CitedRef:
    """A typed citation reference."""
    target: str       # e.g. "L-601", "P-011", "F-META8"
    edge_type: str    # SUPPORTS, CONTRADICTS, EXTENDS, REQUIRES, CITES, BODY

    def is_lesson(self) -> bool:
        return self.target.startswith("L-")

    def is_principle(self) -> bool:
        return self.target.startswith("P-")


def parse_lesson_citations(text: str) -> List[CitedRef]:
    """Parse all citations from lesson text with edge types.

    Returns typed refs from headers + BODY-typed refs from body text.
    """
    refs = []
    header_targets = set()  # Track what's in headers to avoid body duplicates

    # Parse typed headers
    for edge_type, pattern in TYPED_HEADERS:
        for m in pattern.finditer(text):
            header_line = m.group(1)
            for lm in L_RE.finditer(header_line):
                target = f"L-{lm.group(1)}"
                refs.append(CitedRef(target, edge_type))
                header_targets.add(target)
            for pm in P_RE.finditer(header_line):
                target = f"P-{pm.group(1)}"
                refs.append(CitedRef(target, edge_type))
                header_targets.add(target)

    # Parse body text for additional L-refs (type = BODY)
    # Skip header lines (first 10 lines or until first ## section)
    lines = text.splitlines()
    body_start = 0
    for i, line in enumerate(lines):
        if i > 0 and line.startswith("##"):
            body_start = i
            break
    if body_start == 0:
        body_start = min(10, len(lines))

    body_text = "\n".join(lines[body_start:])
    for lm in L_RE.finditer(body_text):
        target = f"L-{lm.group(1)}"
        if target not in header_targets:
            refs.append(CitedRef(target, "BODY"))

    return refs


def parse_lesson_ids(text: str) -> Set[str]:
    """Legacy mode: return flat set of all cited lesson IDs (no edge types).

    Backward-compatible with tools that just need ID sets.
    """
    return {ref.target for ref in parse_lesson_citations(text) if ref.is_lesson()}


def parse_all_refs(text: str) -> Set[str]:
    """Return all L-NNN references found anywhere in text (no typing)."""
    return {f"L-{m.group(1)}" for m in L_RE.finditer(text)}

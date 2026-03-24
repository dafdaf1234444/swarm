#!/usr/bin/env python3
"""Shared lesson header parsing (SIG-80, L-1332, S533 consolidation).

14 tools had independent parse_lesson implementations extracting overlapping
fields. This module provides one parser that handles both YAML frontmatter
(L-1000+) and legacy markdown headers (L-1..L-999).
"""

import re
from pathlib import Path
from typing import Optional

# Matches Domain: field, allowing optional bold (**Domain:**), up to pipe or EOL.
_DOMAIN_RE = re.compile(r"\*{0,2}Domain\*{0,2}:\s*([^\n|]+)")
_SESSION_RE = re.compile(r"\*{0,2}Session\*{0,2}:\s*S?(\d+)")
_SESSION_ALT_RE = re.compile(r"session:\s*S?(\d+)")
_SHARPE_RE = re.compile(r"\*{0,2}Sharpe\*{0,2}:\s*(-?\d+)")
_LEVEL_RE = re.compile(r"\*{0,2}Level\*{0,2}:\s*(L\d)")
_CONFIDENCE_RE = re.compile(r"\*{0,2}Confidence\*{0,2}:\s*(\w+)", re.I)
_TITLE_YAML_RE = re.compile(r"^Title:\s*(.+)", re.M)
_TITLE_MD_RE = re.compile(r"^#\s+L-\d+[:\s]*(.+)", re.M)
_CITES_RE = re.compile(r"^\*{0,2}Cites?\*{0,2}:\s*(.+)", re.M)
_EXTERNAL_RE = re.compile(r"^\*{0,2}External\*{0,2}:\s*(.+)", re.M)
_TAGS_RE = re.compile(r"^\*{0,2}Tags\*{0,2}:\s*(.+)", re.M)
_ID_RE = re.compile(r"^Id:\s*(L-\d+)", re.M)
_L_REF = re.compile(r"L-(\d+)")
_P_REF = re.compile(r"P-(\d+)")
_YAML_FENCE = re.compile(r"^---\s*$", re.M)


def parse_domain_field(header_text: str) -> list[str]:
    """Extract domain names from a lesson header block.

    Handles: Domain: meta | Domain: meta, nk-complexity |
    **Domain**: meta (ISO-15) | pipe-delimited fields
    """
    m = _DOMAIN_RE.search(header_text)
    if not m:
        return []
    raw = m.group(1).strip()
    raw = re.sub(r"\([^)]*\)", "", raw).strip()
    domains = []
    for part in raw.split(","):
        slug = part.strip().lower().replace(" ", "-")
        if slug and not re.match(r"^(sharpe|iso|confidence|level|frontier|l-\d|p-\d)", slug):
            domains.append(slug)
    return domains


def _parse_cites(text: str) -> set[str]:
    """Extract L-NNN and P-NNN references from a Cites: header line."""
    m = _CITES_RE.search(text)
    if not m:
        return set()
    line = m.group(1)
    refs = set()
    for lm in _L_REF.finditer(line):
        refs.add(f"L-{lm.group(1)}")
    for pm in _P_REF.finditer(line):
        refs.add(f"P-{pm.group(1)}")
    return refs


def parse_lesson(path: Path, current_session: int = 0) -> Optional[dict]:
    """Parse a lesson file into structured metadata.

    Returns dict with keys: id, num, title, session, age, domain (list),
    sharpe, level, confidence, cites (set of L-/P- refs), tags, external, body.
    Returns None if the file can't be parsed.
    """
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except (OSError, UnicodeDecodeError):
        return None

    num_m = re.search(r"\d+", path.stem)
    if not num_m:
        return None
    num = int(num_m.group())
    lid = f"L-{num}"

    # Detect format: YAML frontmatter vs legacy markdown
    fences = list(_YAML_FENCE.finditer(text))
    if len(fences) >= 2:
        header = text[fences[0].end():fences[1].start()]
        body = text[fences[1].end():].strip()
    else:
        header = "\n".join(text.splitlines()[:10])
        body = text

    # Title
    title = ""
    tm = _TITLE_YAML_RE.search(header)
    if tm:
        title = tm.group(1).strip()
    if not title:
        tm = _TITLE_MD_RE.search(text)
        if tm:
            title = tm.group(1).strip()

    # Session
    sm = _SESSION_RE.search(header)
    if not sm:
        sm = _SESSION_ALT_RE.search(header)
    session = int(sm.group(1)) if sm else 0
    age = (current_session - session) if (current_session and session) else 0

    # Domain
    domains = parse_domain_field(header)

    # Sharpe
    shm = _SHARPE_RE.search(header)
    sharpe = int(shm.group(1)) if shm else -1

    # Level
    lvm = _LEVEL_RE.search(header)
    level = lvm.group(1) if lvm else ""

    # Confidence
    cm = _CONFIDENCE_RE.search(header)
    confidence = cm.group(1).lower() if cm else ""

    # Cites
    cites = _parse_cites(text)

    # Tags
    tags = []
    tgm = _TAGS_RE.search(header)
    if tgm:
        raw_tags = tgm.group(1).strip().strip("[]")
        tags = [t.strip() for t in raw_tags.split(",") if t.strip()]

    # External
    ext = ""
    em = _EXTERNAL_RE.search(header)
    if em:
        ext = em.group(1).strip()

    return {
        "id": lid,
        "num": num,
        "title": title,
        "session": session,
        "age": age,
        "domain": domains,
        "sharpe": sharpe,
        "level": level,
        "confidence": confidence,
        "cites": cites,
        "tags": tags,
        "external": ext,
        "body": body,
    }

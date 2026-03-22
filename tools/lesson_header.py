#!/usr/bin/env python3
"""Shared lesson header parsing — canonical Domain: field extraction (SIG-80, L-1332).

Six tools had divergent regexes for Domain: headers (42% disagreement rate).
This module provides one function that all domain-parsing code should use.
"""

import re

# Matches Domain: field, allowing optional bold (**Domain:**), up to pipe or EOL.
_DOMAIN_RE = re.compile(r"\*{0,2}Domain\*{0,2}:\s*([^\n|]+)")


def parse_domain_field(header_text: str) -> list[str]:
    """Extract domain names from a lesson header block (first ~5 lines).

    Returns a list of cleaned, lowercased domain slugs.
    Empty list if no Domain: field found.

    Handles all known formats:
      Domain: meta
      Domain: meta, nk-complexity
      **Domain**: meta (ISO-15, P-210)   ← strips parenthetical metadata
      Domain: meta | Sharpe: 7           ← pipe-delimited fields
    """
    m = _DOMAIN_RE.search(header_text)
    if not m:
        return []
    raw = m.group(1).strip()
    # Remove parenthetical metadata bleed like "(ISO-15, P-210)"
    raw = re.sub(r"\([^)]*\)", "", raw).strip()
    # Split on comma, clean each
    domains = []
    for part in raw.split(","):
        slug = part.strip().lower().replace(" ", "-")
        # Skip empty or obvious non-domain tokens
        if slug and not re.match(r"^(sharpe|iso|confidence|level|frontier|l-\d|p-\d)", slug):
            domains.append(slug)
    return domains

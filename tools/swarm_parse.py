#!/usr/bin/env python3

import re


def active_principle_ids(text: str) -> tuple[set[int], set[int]]:
    all_ids = {int(m.group(1)) for m in re.finditer(r"\bP-(\d+)\b", text)}
    superseded = {int(m.group(1)) for m in re.finditer(r"\bP-(\d+)→", text)}
    superseded |= {
        int(m.group(1))
        for m in re.finditer(r"\(P-(\d+)\s+(?:merged|superseded|absorbed)\)", text, re.IGNORECASE)
    }
    for m in re.finditer(r"P-(\d+)\+P-(\d+)\s+merged", text, re.IGNORECASE):
        superseded.add(int(m.group(1)))
        superseded.add(int(m.group(2)))
    return all_ids, superseded


def active_frontier_ids(text: str) -> set[int]:
    return {int(m.group(1)) for m in re.finditer(r"^- \*\*F(\d+)\*\*:", text, re.MULTILINE)}


def archived_frontier_ids(text: str) -> set[int]:
    return {int(m.group(1)) for m in re.finditer(r"\|\s*F(\d+)\s*\|", text)}

#!/usr/bin/env python3
"""Claude Code PreToolUse hook: block 'git add -A' and 'git add .' in this repo.

WSL mass-deletion bug: 'git add -A' on a WSL-corrupted tree stages mass deletions
(729 files deleted in one incident, L-179 / MEMORY.md). This hook blocks those patterns
at execution time and prints the safe alternative.
"""
import json
import sys
import re


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    # Only intercept Bash tool
    if tool_name != "Bash":
        sys.exit(0)

    command = tool_input.get("command", "")

    # Block 'git add -A', 'git add .', 'git add --all'
    # Use (?=[\s$]) to avoid false positives on paths like .claude/settings.json
    if re.search(r'\bgit\s+add\s+(-A|--all|\.(?=\s|$))', command):
        print(
            "BLOCKED: 'git add -A / git add .' is forbidden in this repo (WSL mass-deletion risk).\n"
            "Safe alternative: git add <specific named files>\n"
            "See: MEMORY.md 'WSL filesystem corruption' section and L-179.",
            file=sys.stderr,
        )
        # exit 2 = block the tool call and show error to LLM
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()

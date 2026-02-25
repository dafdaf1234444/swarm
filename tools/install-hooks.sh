#!/bin/bash
# Install swarm git hooks
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cp "$REPO_ROOT/tools/pre-commit.hook" "$REPO_ROOT/.git/hooks/pre-commit"
chmod +x "$REPO_ROOT/.git/hooks/pre-commit"
echo "Pre-commit hook installed."

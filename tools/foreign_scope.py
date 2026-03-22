#!/usr/bin/env python3
"""foreign_scope.py — Detect modifiable vs infrastructure scope in foreign repos.

Complements substrate_detect.py (L-1301). When swarming a foreign repo,
identifies which files are likely editable source vs read-only infrastructure
(lock files, CI configs, build scripts). Helps agents avoid modifying
infrastructure they don't understand.

Usage:
    python3 tools/foreign_scope.py [path]
"""

import json
import os
import sys
from pathlib import Path


# Files that are typically read-only infrastructure
INFRA_PATTERNS = {
    # Lock files (never manually edit)
    "locks": ["*.lock", "package-lock.json", "yarn.lock", "pnpm-lock.yaml",
              "Pipfile.lock", "poetry.lock", "uv.lock", "Cargo.lock", "go.sum",
              "Gemfile.lock", "composer.lock", "bun.lockb"],
    # Build/CI config (understand before touching)
    "ci": [".github/workflows/*", ".gitlab-ci.yml", ".circleci/*",
           "Jenkinsfile", ".travis.yml"],
    # Build configs (usually generated or carefully tuned)
    "build": ["Makefile", "CMakeLists.txt", "build.rs", "webpack.config.*",
              "vite.config.*", "rollup.config.*", "tsconfig.json",
              "babel.config.*", ".babelrc"],
    # Package/project definitions (modify with care)
    "project": ["pyproject.toml", "setup.py", "setup.cfg", "package.json",
                "Cargo.toml", "go.mod", "pom.xml", "build.gradle*",
                "Gemfile", "composer.json", "pubspec.yaml", "mix.exs"],
    # Environment/deployment
    "deploy": ["Dockerfile", "docker-compose.yml", "docker-compose.yaml",
               "*.tf", "terraform.tfvars", "k8s/*", "helm/*"],
    # Meta
    "meta": [".gitignore", ".gitattributes", "LICENSE", "LICENSE.*"],
}

# Directories that typically contain editable source
SOURCE_DIRS = ["src/", "lib/", "app/", "pkg/", "cmd/", "internal/",
               "components/", "pages/", "routes/", "handlers/",
               "services/", "models/", "views/", "controllers/"]

# Directories that are typically test code (editable, but different scope)
TEST_DIRS = ["tests/", "test/", "spec/", "__tests__/", "e2e/",
             "integration/", "benchmarks/", "bench/"]


def _glob_match(root: Path, pattern: str) -> list[str]:
    """Return matching file paths relative to root."""
    if "*" in pattern:
        return [str(p.relative_to(root)) for p in root.glob(pattern) if p.is_file()]
    p = root / pattern
    if p.exists() and p.is_file():
        return [pattern]
    return []


def detect_scope(repo_path: str = ".") -> dict:
    """
    Analyze a repo's file scope. Returns:
    {
        "infra": {"locks": [...], "ci": [...], ...},  # read-only files by category
        "source_dirs": [str],      # directories containing editable source
        "test_dirs": [str],        # directories containing tests
        "editable_count": int,     # rough count of source files
        "infra_count": int,        # count of infrastructure files
    }
    """
    root = Path(repo_path).resolve()
    result = {
        "infra": {},
        "source_dirs": [],
        "test_dirs": [],
        "editable_count": 0,
        "infra_count": 0,
    }

    # Find infrastructure files
    for category, patterns in INFRA_PATTERNS.items():
        found = []
        for pattern in patterns:
            found.extend(_glob_match(root, pattern))
        if found:
            result["infra"][category] = sorted(set(found))
            result["infra_count"] += len(found)

    # Find source directories
    for d in SOURCE_DIRS:
        if (root / d).is_dir():
            result["source_dirs"].append(d)
            # Count files in source dir (rough)
            result["editable_count"] += sum(1 for _ in (root / d).rglob("*") if _.is_file())

    # Find test directories
    for d in TEST_DIRS:
        if (root / d).is_dir():
            result["test_dirs"].append(d)

    return result


def scope_text(info: dict) -> str:
    """Human-readable scope summary for orient output."""
    lines = []

    if info["source_dirs"]:
        lines.append(f"Source dirs (editable): {', '.join(info['source_dirs'])} "
                     f"(~{info['editable_count']} files)")

    if info["test_dirs"]:
        lines.append(f"Test dirs: {', '.join(info['test_dirs'])}")

    if info["infra"]:
        infra_summary = []
        for cat, files in info["infra"].items():
            infra_summary.append(f"{cat}({len(files)})")
        lines.append(f"Infrastructure (read-only): {', '.join(infra_summary)} "
                     f"= {info['infra_count']} files total")

        # Show specific lock files
        if "locks" in info["infra"]:
            lines.append(f"  Lock files (never edit): {', '.join(info['infra']['locks'])}")

    if not lines:
        lines.append("No standard project structure detected. Read README.md for guidance.")

    return "\n".join(lines)


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "."
    info = detect_scope(path)
    print(json.dumps(info, indent=2))
    print()
    print("--- Scope ---")
    print(scope_text(info))

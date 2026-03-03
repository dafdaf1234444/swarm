#!/usr/bin/env python3
"""INDEX.md bucket organizer — propose and apply splits for overflowing themes (F-BRN4).

Analyzes INDEX.md theme buckets, identifies overflow (>40L limit),
proposes sub-theme splits based on lesson title keyword clustering.

Usage:
  python3 tools/index_organizer.py              # analyze and propose splits
  python3 tools/index_organizer.py --apply "Theme Name"  # apply a specific split
  python3 tools/index_organizer.py --threshold 30  # custom overflow threshold
"""

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from swarm_io import REPO_ROOT, read_text, lesson_paths

INDEX_PATH = REPO_ROOT / "memory" / "INDEX.md"
THEME_MAPPING_PATH = REPO_ROOT / "experiments" / "quality" / "f-qc4-theme-mapping-s383.json"
LESSONS_DIR = REPO_ROOT / "memory" / "lessons"

STOPWORDS = {
    "the", "a", "an", "is", "are", "in", "of", "for", "to", "at", "by",
    "with", "and", "or", "not", "from", "as", "on", "that", "this", "it",
    "its", "be", "was", "were", "has", "have", "had", "do", "does", "did",
    "will", "would", "can", "could", "should", "may", "might", "must",
    "how", "what", "when", "where", "why", "which", "who", "more", "than",
    "but", "if", "then", "so", "no", "yes", "all", "each", "every", "any",
    "few", "some", "most", "other", "such", "only", "own", "same", "also",
    "just", "about", "above", "after", "before", "between", "into",
    "through", "during", "without", "within", "along", "across",
}


def parse_index(text):
    """Parse INDEX.md themes table into structured data."""
    themes = {}
    for i, line in enumerate(text.split("\n")):
        m = re.match(r"^\s*\|\s*(?![-|])\s*([^|]+?)\s*\|\s*(\d+)\s*\|\s*([^|]*)\s*\|", line)
        if m:
            themes[m.group(1).strip()] = {
                "count": int(m.group(2)),
                "insight": m.group(3).strip(),
                "line_num": i,
            }
    return themes


def load_theme_mapping():
    """Load lesson-to-theme mapping from experiment artifact."""
    if not THEME_MAPPING_PATH.exists():
        return {}
    try:
        with open(THEME_MAPPING_PATH) as f:
            return json.load(f)
    except Exception:
        return {}


def build_theme_lessons(mapping, themes):
    """Build reverse map: theme_name -> [lesson_ids]."""
    theme_lessons = defaultdict(list)
    theme_names = set(themes.keys())

    def best_match(raw):
        if raw in theme_names:
            return raw
        raw_w = set(raw.lower().split())
        best, best_s = None, 0
        for tn in theme_names:
            overlap = len(raw_w & set(tn.lower().split()))
            if overlap > best_s:
                best_s = overlap
                best = tn
        return best if best_s >= 2 else raw

    for lid, theme in mapping.items():
        theme_lessons[best_match(theme)].append(lid)
    return dict(theme_lessons)


def get_lesson_title(lid):
    """Get a lesson's title from its file."""
    path = LESSONS_DIR / f"{lid}.md"
    if not path.exists():
        return ""
    text = read_text(path)
    if not text:
        return ""
    for line in text.split("\n")[:5]:
        m = re.match(r"#\s+L-\d+[:\s]+(.*)", line)
        if m:
            return m.group(1).strip()
    return ""


def tokenize_title(title):
    """Extract meaningful words from a title."""
    return [w for w in re.findall(r"[a-z]+", title.lower())
            if len(w) > 2 and w not in STOPWORDS]


def propose_splits(theme_name, lesson_ids, target_size=35):
    """Propose sub-theme splits for an overflowing bucket."""
    if len(lesson_ids) <= target_size:
        return [{"sub_name": theme_name, "lessons": lesson_ids,
                 "count": len(lesson_ids)}]

    # Load titles and tokenize
    tokens_map = {lid: tokenize_title(get_lesson_title(lid)) for lid in lesson_ids}
    word_freq = Counter()
    for tokens in tokens_map.values():
        word_freq.update(set(tokens))

    # Extract theme category prefix
    parts = theme_name.split(" -- ")
    category = parts[0] if len(parts) > 1 else theme_name
    theme_words = set(tokenize_title(theme_name))

    # Pick discriminating words as cluster seeds
    n = len(lesson_ids)
    candidates = [(w, c) for w, c in word_freq.most_common(50)
                  if w not in theme_words
                  and c >= max(3, n * 0.08) and c <= n * 0.7]

    n_splits = min(3, max(2, n // target_size + 1))
    seeds = [w for w, _ in candidates[:n_splits]]

    if len(seeds) < 2:
        # Fallback: split by chronological position
        mid = n // 2
        sorted_ids = sorted(lesson_ids,
                           key=lambda x: int(re.search(r"\d+", x).group()))
        return [
            {"sub_name": f"{category} -- Early", "lessons": sorted_ids[:mid],
             "count": mid},
            {"sub_name": f"{category} -- Recent", "lessons": sorted_ids[mid:],
             "count": n - mid},
        ]

    # Assign lessons to clusters
    clusters = {s: [] for s in seeds}
    for lid in lesson_ids:
        tokens = set(tokens_map[lid])
        matched = next((s for s in seeds if s in tokens), None)
        if matched:
            clusters[matched].append(lid)
        else:
            smallest = min(clusters.keys(), key=lambda s: len(clusters[s]))
            clusters[smallest].append(lid)

    return sorted(
        [{"sub_name": f"{category} -- {s.capitalize()}", "lessons": sorted(m),
          "count": len(m)} for s, m in clusters.items()],
        key=lambda x: x["count"], reverse=True)


def analyze_overflow(themes, threshold=40):
    """Find overflowing theme buckets."""
    return sorted(
        [{"name": n, "count": d["count"], "insight": d["insight"],
          "line_num": d["line_num"]}
         for n, d in themes.items() if d["count"] > threshold],
        key=lambda x: x["count"], reverse=True)


def apply_split(index_path, old_theme, splits):
    """Apply a split to INDEX.md by replacing one theme row with sub-theme rows."""
    text = read_text(index_path)
    if not text:
        return False
    lines = text.split("\n")
    new_lines = []
    replaced = False
    for line in lines:
        if not replaced and old_theme in line and re.match(r"^\s*\|", line):
            for s in splits:
                new_lines.append(
                    f"| {s['sub_name']} | {s['count']} | Split from {old_theme} |")
            replaced = True
        else:
            new_lines.append(line)
    if not replaced:
        print(f"Error: '{old_theme}' not found")
        return False
    with open(index_path, "w") as f:
        f.write("\n".join(new_lines))
    print(f"Split '{old_theme}' -> {len(splits)} sub-themes")
    return True


def main():
    parser = argparse.ArgumentParser(description="INDEX.md bucket organizer")
    parser.add_argument("--apply", help="Apply split for named theme")
    parser.add_argument("--threshold", type=int, default=40)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    index_text = read_text(INDEX_PATH)
    if not index_text:
        print("Error: cannot read INDEX.md")
        return

    themes = parse_index(index_text)
    overflow = analyze_overflow(themes, args.threshold)

    mapping = load_theme_mapping()
    theme_lessons = build_theme_lessons(mapping, themes) if mapping else {}

    if args.apply:
        lessons = theme_lessons.get(args.apply, [])
        splits = propose_splits(args.apply, lessons) if lessons else []
        if splits:
            apply_split(INDEX_PATH, args.apply, splits)
        return

    print(f"=== INDEX.md BUCKET ANALYSIS (threshold={args.threshold}) ===")
    print(f"Total themes: {len(themes)}, Overflowing: {len(overflow)}\n")

    if not overflow:
        print("All buckets within limits.")
        return

    for item in overflow:
        name = item["name"]
        lessons = theme_lessons.get(name, [])
        splits = propose_splits(name, lessons) if lessons else []

        print(f"  {name} ({item['count']} lessons)")
        if splits:
            print("    Proposed splits:")
            for s in splits:
                sample = ", ".join(s["lessons"][:4])
                suffix = f" — {sample}..." if sample else ""
                print(f'      "{s["sub_name"]}" ({s["count"]}){suffix}')
            print(f'    Apply: python3 tools/index_organizer.py --apply "{name}"')
        print()

    print(f"Summary: {len(overflow)} buckets overflowing, {len(overflow)} proposals")


if __name__ == "__main__":
    main()

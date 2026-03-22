#!/usr/bin/env python3
"""Citation-graph retrieval tool — F-BRN7 intervention (b).

Given a lesson ID or keyword, find related lessons via citation graph traversal.
Coverage: 86.6% of lessons reachable via giant component (vs 29.5% INDEX pointers).
Zero maintenance cost — edges from Cites: headers are self-updating.
# L-929: Citation graph is primary retrieval; INDEX is cold-start fallback only.
# L-1292: Typed edges (Supports/Contradicts/Extends) for semantic graph queries.

Usage:
    python3 tools/citation_retrieval.py L-601               # 2-hop neighbors
    python3 tools/citation_retrieval.py L-601 --hops 3      # 3-hop neighbors
    python3 tools/citation_retrieval.py --keyword retrieval  # keyword → graph walk
    python3 tools/citation_retrieval.py --stats              # graph statistics
    python3 tools/citation_retrieval.py L-601 --typed        # show edge types
"""
import argparse, sys
from collections import defaultdict, deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from cite_parse import parse_lesson_citations, parse_all_refs  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
LESSONS_DIR = ROOT / "memory" / "lessons"


def build_graph(typed=False):
    """Parse all lessons and return adjacency lists + metadata.

    If typed=True, also returns edge_types dict: (src, tgt) → set of edge types.
    """
    outbound = defaultdict(set)   # lesson → set of cited lessons
    inbound = defaultdict(set)    # lesson → set of lessons that cite it
    titles = {}                   # lesson → title line
    edge_types = defaultdict(set) if typed else None  # (src, tgt) → {SUPPORTS, ...}

    for f in sorted(LESSONS_DIR.glob("L-*.md")):
        lid = f.stem  # e.g. "L-601"
        text = f.read_text(encoding="utf-8", errors="replace")
        lines = text.splitlines()
        titles[lid] = lines[0].lstrip("# ").strip() if lines else lid

        if typed:
            refs = parse_lesson_citations(text)
            for ref in refs:
                if ref.is_lesson() and ref.target != lid:
                    outbound[lid].add(ref.target)
                    inbound[ref.target].add(lid)
                    edge_types[(lid, ref.target)].add(ref.edge_type)
        else:
            # Fast path: just find all L-NNN refs
            for target in parse_all_refs(text):
                if target != lid:
                    outbound[lid].add(target)
                    inbound[target].add(lid)

    # Filter edges to existing lessons only
    all_ids = set(titles.keys())
    for lid in list(outbound.keys()):
        outbound[lid] = outbound[lid] & all_ids
    for lid in list(inbound.keys()):
        if lid not in all_ids:
            del inbound[lid]
        else:
            inbound[lid] = inbound[lid] & all_ids

    if typed:
        return outbound, inbound, titles, edge_types
    return outbound, inbound, titles


def bfs(start_set, outbound, inbound, max_hops):
    """BFS from start_set, following edges in both directions."""
    visited = {}  # node → hop distance
    queue = deque()
    for s in start_set:
        visited[s] = 0
        queue.append((s, 0))

    while queue:
        node, dist = queue.popleft()
        if dist >= max_hops:
            continue
        neighbors = outbound.get(node, set()) | inbound.get(node, set())
        for nb in neighbors:
            if nb not in visited:
                visited[nb] = dist + 1
                queue.append((nb, dist + 1))

    return visited


def keyword_search(keyword, titles):
    """Find lessons whose title contains the keyword."""
    kw = keyword.lower()
    return [lid for lid, t in titles.items() if kw in t.lower()]


def print_results(visited, titles, start_set, max_hops):
    """Print retrieval results grouped by hop distance."""
    by_hop = defaultdict(list)
    for lid, dist in sorted(visited.items(), key=lambda x: (x[1], x[0])):
        by_hop[dist].append(lid)

    total = len(visited) - len(start_set)
    print(f"\n  Found {total} related lessons within {max_hops} hops\n")

    for hop in range(max_hops + 1):
        nodes = by_hop.get(hop, [])
        if not nodes:
            continue
        label = "Seeds" if hop == 0 else f"Hop {hop}"
        print(f"  --- {label} ({len(nodes)}) ---")
        for lid in nodes[:15]:
            title = titles.get(lid, lid)
            if len(title) > 80:
                title = title[:77] + "..."
            print(f"    {lid}: {title}")
        if len(nodes) > 15:
            print(f"    ... +{len(nodes) - 15} more")
        print()


def print_stats(outbound, inbound, titles, edge_types=None):
    """Print citation graph statistics."""
    all_nodes = set(titles.keys())
    n = len(all_nodes)
    edges = sum(len(v) for v in outbound.values())
    zero_out = sum(1 for lid in all_nodes if not outbound.get(lid))
    zero_in = sum(1 for lid in all_nodes if not inbound.get(lid))
    isolated = sum(1 for lid in all_nodes
                   if not outbound.get(lid) and not inbound.get(lid))

    # Giant component via BFS from most-cited node
    top = sorted(inbound.keys(), key=lambda x: len(inbound[x]), reverse=True)
    if top:
        gc = bfs({top[0]}, outbound, inbound, max_hops=999)
    else:
        gc = {}

    print(f"\n  Citation Graph Statistics (N={n})")
    print(f"  {'─' * 40}")
    print(f"  Edges:              {edges}")
    print(f"  Avg out-degree:     {edges / n:.2f}")
    print(f"  Zero outbound:      {zero_out} ({zero_out * 100 / n:.1f}%)")
    print(f"  Zero inbound:       {zero_in} ({zero_in * 100 / n:.1f}%)")
    print(f"  Isolated:           {isolated} ({isolated * 100 / n:.1f}%)")
    print(f"  Giant component:    {len(gc)} ({len(gc) * 100 / n:.1f}%)")

    # Typed edge breakdown (L-1292)
    if edge_types:
        type_counts = defaultdict(int)
        for etypes in edge_types.values():
            for t in etypes:
                type_counts[t] += 1
        total_typed = sum(type_counts.values())
        print(f"\n  Edge types ({total_typed} typed edges):")
        for t in ["SUPPORTS", "CONTRADICTS", "EXTENDS", "REQUIRES", "CITES", "BODY"]:
            c = type_counts.get(t, 0)
            if c:
                print(f"    {t:14s} {c:4d} ({c * 100 / total_typed:.1f}%)")
        typed_non_body = sum(c for t, c in type_counts.items() if t not in ("CITES", "BODY"))
        print(f"    Semantically typed: {typed_non_body}/{total_typed} ({typed_non_body * 100 / total_typed:.1f}%)")
    print()

    # Top-10 most cited
    top10 = sorted(all_nodes, key=lambda x: len(inbound.get(x, set())),
                   reverse=True)[:10]
    print(f"  Top-10 most cited:")
    for lid in top10:
        ic = len(inbound.get(lid, set()))
        title = titles.get(lid, lid)
        if len(title) > 60:
            title = title[:57] + "..."
        print(f"    {lid} ({ic} citations): {title}")
    print()


def main():
    ap = argparse.ArgumentParser(description="Citation-graph retrieval (F-BRN7)")
    ap.add_argument("lesson", nargs="?", help="Lesson ID (e.g. L-601)")
    ap.add_argument("--hops", type=int, default=2, help="Max hops (default 2)")
    ap.add_argument("--keyword", "-k", help="Search by keyword in titles")
    ap.add_argument("--stats", action="store_true", help="Show graph statistics")
    ap.add_argument("--typed", action="store_true", help="Show typed edge info (L-1292)")
    args = ap.parse_args()

    if args.typed or args.stats:
        outbound, inbound, titles, edge_types = build_graph(typed=True)
    else:
        outbound, inbound, titles = build_graph()
        edge_types = None

    if args.stats:
        print_stats(outbound, inbound, titles, edge_types)
        return

    seeds = set()
    if args.lesson:
        lid = args.lesson.upper()
        if not lid.startswith("L-"):
            lid = f"L-{lid}"
        if lid not in titles:
            print(f"  Lesson {lid} not found.", file=sys.stderr)
            sys.exit(1)
        seeds.add(lid)

    if args.keyword:
        matches = keyword_search(args.keyword, titles)
        if not matches:
            print(f"  No lessons match keyword '{args.keyword}'", file=sys.stderr)
            sys.exit(1)
        print(f"  Keyword '{args.keyword}' matched {len(matches)} lesson(s)")
        seeds.update(matches)

    if not seeds:
        ap.print_help()
        sys.exit(1)

    visited = bfs(seeds, outbound, inbound, args.hops)
    print_results(visited, titles, seeds, args.hops)


if __name__ == "__main__":
    main()

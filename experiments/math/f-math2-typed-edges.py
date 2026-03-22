#!/usr/bin/env python3
"""F-MATH2 Experiment: Typed vs Untyped Edge Learning Paths

Hypothesis: Typed edges produce shorter learning paths when a learner only needs
the STATEMENT of a prerequisite (not its proof). For "uses_in_statement" deps,
you only need to learn the node's statement — not recurse into that node's own
proof prerequisites. For "uses_in_proof" deps, you need the full chain.

Protocol:
  1. Full path (untyped): treat all edges as "uses_in_proof" — DFS through
     every prerequisite recursively. This is what `math_tree.py path` does.
  2. Statement-aware path (typed): for "uses_in_statement" deps, include only
     the referenced node itself (its statement suffices), without recursing into
     that node's own prerequisites. For "uses_in_proof" deps, recurse fully.
  3. Compare path lengths and orderings for 5 target theorems.

Expected outcome: Statement-aware paths are strictly shorter (or equal) for every
target. The reduction is largest for nodes whose prereq trees contain deep
chains of "uses_in_statement" edges (e.g., Group -> Abelian group -> Ring ->
Field -> Vector space).
"""

import json
import sys
from collections import OrderedDict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
NODES_DIR = ROOT / "domains" / "mathematics" / "nodes"

# --- Target selection ---
# 5 theorems with varied depths, each having >= 3 prereqs in its full path,
# and significant uses_in_statement edges in the prereq tree.
TARGETS = ["T-011", "T-033", "T-040", "T-004", "T-007"]


def load_all_nodes():
    """Load all 100 math nodes from disk."""
    nodes = {}
    for f in sorted(NODES_DIR.glob("*.json")):
        try:
            node = json.loads(f.read_text(encoding="utf-8"))
            nodes[node["id"]] = node
        except (json.JSONDecodeError, KeyError):
            print(f"WARNING: corrupt node file {f}", file=sys.stderr)
    return nodes


def full_path(nodes, target):
    """Untyped learning path: DFS through ALL prerequisites regardless of edge type.

    This treats every edge as "uses_in_proof" — you must learn the full
    proof chain for every prerequisite.
    Returns list of node IDs in topological (learning) order.
    """
    visited = set()
    order = []

    def dfs(nid):
        if nid in visited:
            return
        visited.add(nid)
        node = nodes.get(nid)
        if not node:
            return
        for dep in node.get("prerequisites", []):
            dfs(dep["ref"])
        order.append(nid)

    dfs(target)
    return order


def statement_aware_path(nodes, target):
    """Typed learning path: respects edge types.

    - "uses_in_proof" edges: recurse fully (you need to understand the proof)
    - "uses_in_statement" edges: include only the referenced node itself
      (you only need to know what it IS, not how it's proved/constructed)
    - "generalizes"/"specializes": treat as proof deps (full recurse)

    Returns list of node IDs in topological (learning) order.
    """
    visited = set()
    order = []

    def dfs(nid, recurse_fully=True):
        if nid in visited:
            return
        visited.add(nid)
        node = nodes.get(nid)
        if not node:
            return
        if recurse_fully:
            # Recurse into prerequisites, respecting edge types
            for dep in node.get("prerequisites", []):
                edge_type = dep.get("edge_type", "uses_in_proof")
                if edge_type == "uses_in_statement":
                    # Only need the statement — add the node but don't recurse
                    dfs(dep["ref"], recurse_fully=False)
                else:
                    # Need full proof chain
                    dfs(dep["ref"], recurse_fully=True)
        # If not recurse_fully, we still add this node but don't explore its deps
        order.append(nid)

    dfs(target, recurse_fully=True)
    return order


def compute_depth(nodes, nid, memo=None):
    """Compute graph depth of a node."""
    if memo is None:
        memo = {}
    if nid in memo:
        return memo[nid]
    node = nodes.get(nid)
    if not node or not node.get("prerequisites"):
        memo[nid] = 0
        return 0
    d = 1 + max(
        (compute_depth(nodes, dep["ref"], memo)
         for dep in node["prerequisites"] if dep["ref"] in nodes),
        default=0
    )
    memo[nid] = d
    return d


def count_edge_types_in_tree(nodes, target):
    """Count uses_in_statement vs uses_in_proof edges in the full prereq tree."""
    visited = set()
    stmt_count = 0
    proof_count = 0
    other_count = 0

    def dfs(nid):
        nonlocal stmt_count, proof_count, other_count
        if nid in visited:
            return
        visited.add(nid)
        node = nodes.get(nid)
        if not node:
            return
        for dep in node.get("prerequisites", []):
            etype = dep.get("edge_type", "uses_in_proof")
            if etype == "uses_in_statement":
                stmt_count += 1
            elif etype == "uses_in_proof":
                proof_count += 1
            else:
                other_count += 1
            dfs(dep["ref"])

    dfs(target)
    return {"uses_in_statement": stmt_count, "uses_in_proof": proof_count, "other": other_count}


def analyze_pruned_nodes(nodes, full, stmt_aware):
    """Identify which nodes were pruned (in full but not in statement-aware)."""
    full_set = set(full)
    stmt_set = set(stmt_aware)
    pruned = full_set - stmt_set
    return sorted(pruned)


def main():
    nodes = load_all_nodes()
    print(f"Loaded {len(nodes)} nodes from {NODES_DIR}\n")
    print("=" * 78)
    print("F-MATH2 EXPERIMENT: Typed vs Untyped Edge Learning Paths")
    print("=" * 78)

    depth_memo = {}
    results = []

    for target in TARGETS:
        if target not in nodes:
            print(f"\nERROR: {target} not found, skipping")
            continue

        node = nodes[target]
        d = compute_depth(nodes, target, depth_memo)
        edge_counts = count_edge_types_in_tree(nodes, target)

        fp = full_path(nodes, target)
        sp = statement_aware_path(nodes, target)
        pruned = analyze_pruned_nodes(nodes, fp, sp)
        reduction = len(fp) - len(sp)
        reduction_pct = (reduction / len(fp) * 100) if len(fp) > 0 else 0

        print(f"\n{'─' * 78}")
        print(f"TARGET: {target} — {node['title']}")
        print(f"  Type: {node['type']}, Domain: {node.get('domain', '?')}, Depth: {d}")
        print(f"  Direct prereqs: {len(node.get('prerequisites', []))}")
        print(f"  Edge types in tree: {edge_counts}")
        print()
        print(f"  Full path (untyped):       {len(fp)} nodes")
        print(f"  Statement-aware (typed):   {len(sp)} nodes")
        print(f"  Reduction:                 {reduction} nodes ({reduction_pct:.1f}%)")
        print()

        if pruned:
            print(f"  Pruned nodes ({len(pruned)}):")
            for pid in pruned:
                pn = nodes.get(pid, {})
                print(f"    - {pid} ({pn.get('type', '?')}): {pn.get('title', '?')}")
        else:
            print("  Pruned nodes: none (all prereqs are proof-deps)")

        print()
        print(f"  Full path order:")
        for i, nid in enumerate(fp):
            n = nodes.get(nid, {})
            marker = " <-- TARGET" if nid == target else ""
            in_stmt = " [PRUNED in typed]" if nid in set(pruned) else ""
            print(f"    {i+1:2d}. {nid:8s} ({n.get('type', '?'):10s}): {n.get('title', '?')}{marker}{in_stmt}")

        print()
        print(f"  Statement-aware path order:")
        for i, nid in enumerate(sp):
            n = nodes.get(nid, {})
            marker = " <-- TARGET" if nid == target else ""
            print(f"    {i+1:2d}. {nid:8s} ({n.get('type', '?'):10s}): {n.get('title', '?')}{marker}")

        results.append({
            "target": target,
            "title": node["title"],
            "type": node["type"],
            "domain": node.get("domain", "general"),
            "depth": d,
            "direct_prereqs": len(node.get("prerequisites", [])),
            "edge_types_in_tree": edge_counts,
            "full_path": {"length": len(fp), "nodes": fp},
            "statement_aware_path": {"length": len(sp), "nodes": sp},
            "reduction": {
                "nodes": reduction,
                "percentage": round(reduction_pct, 1),
            },
            "pruned_nodes": [
                {"id": pid, "type": nodes[pid]["type"], "title": nodes[pid]["title"]}
                for pid in pruned if pid in nodes
            ],
        })

    # --- Summary ---
    print(f"\n{'=' * 78}")
    print("SUMMARY")
    print(f"{'=' * 78}")

    total_full = sum(r["full_path"]["length"] for r in results)
    total_stmt = sum(r["statement_aware_path"]["length"] for r in results)
    total_pruned = sum(r["reduction"]["nodes"] for r in results)
    avg_reduction_pct = (total_pruned / total_full * 100) if total_full > 0 else 0

    print(f"\n  {'Target':8s} {'Full':>6s} {'Typed':>6s} {'Pruned':>7s} {'Reduction':>10s}")
    print(f"  {'─' * 45}")
    for r in results:
        print(f"  {r['target']:8s} {r['full_path']['length']:6d} "
              f"{r['statement_aware_path']['length']:6d} "
              f"{r['reduction']['nodes']:7d} "
              f"{r['reduction']['percentage']:9.1f}%")
    print(f"  {'─' * 45}")
    print(f"  {'TOTAL':8s} {total_full:6d} {total_stmt:6d} {total_pruned:7d} {avg_reduction_pct:9.1f}%")

    # --- Hypothesis evaluation ---
    print(f"\n{'─' * 78}")
    print("HYPOTHESIS EVALUATION")
    print(f"{'─' * 78}")

    all_shorter_or_equal = all(
        r["statement_aware_path"]["length"] <= r["full_path"]["length"]
        for r in results
    )
    any_strictly_shorter = any(
        r["statement_aware_path"]["length"] < r["full_path"]["length"]
        for r in results
    )

    hypothesis_confirmed = all_shorter_or_equal and any_strictly_shorter

    print(f"\n  H0: Typed edges do NOT produce shorter learning paths")
    print(f"  H1: Typed edges produce shorter (or equal) paths, with at least")
    print(f"      one strictly shorter path")
    print()
    print(f"  All statement-aware <= full:  {all_shorter_or_equal}")
    print(f"  Any strictly shorter:         {any_strictly_shorter}")
    print(f"  Average reduction:            {avg_reduction_pct:.1f}%")
    print()

    if hypothesis_confirmed:
        print(f"  RESULT: H1 CONFIRMED — typed edges produce shorter learning paths")
        print(f"  The statement-aware path prunes nodes whose full proof chain is")
        print(f"  unnecessary when only the statement is needed. Average reduction")
        print(f"  of {avg_reduction_pct:.1f}% across {len(results)} targets.")
    else:
        print(f"  RESULT: H1 NOT CONFIRMED")
        if not all_shorter_or_equal:
            print(f"  Some statement-aware paths are LONGER than full paths (bug?)")
        if not any_strictly_shorter:
            print(f"  No path was strictly shorter — all edges may be proof deps")

    # Deeper finding: which edge type chains cause the biggest reductions?
    print(f"\n{'─' * 78}")
    print("DEEPER ANALYSIS: Statement-dep chain depth vs reduction")
    print(f"{'─' * 78}")
    for r in results:
        stmt_ratio = r["edge_types_in_tree"]["uses_in_statement"] / max(
            r["edge_types_in_tree"]["uses_in_statement"] +
            r["edge_types_in_tree"]["uses_in_proof"], 1
        )
        print(f"\n  {r['target']} ({r['title']})")
        print(f"    Statement edge ratio: {stmt_ratio:.1%} "
              f"({r['edge_types_in_tree']['uses_in_statement']} / "
              f"{r['edge_types_in_tree']['uses_in_statement'] + r['edge_types_in_tree']['uses_in_proof']})")
        print(f"    Path reduction: {r['reduction']['percentage']:.1f}%")
        print(f"    Pruned nodes: {[p['id'] for p in r['pruned_nodes']]}")

    # --- JSON output ---
    output = {
        "experiment": "F-MATH2",
        "hypothesis": "Typed edges produce shorter learning paths when statement deps "
                      "don't require recursing into proof prerequisites",
        "targets": TARGETS,
        "results": results,
        "summary": {
            "total_full_path_nodes": total_full,
            "total_statement_aware_nodes": total_stmt,
            "total_pruned": total_pruned,
            "average_reduction_pct": round(avg_reduction_pct, 1),
            "hypothesis_confirmed": hypothesis_confirmed,
            "all_shorter_or_equal": all_shorter_or_equal,
            "any_strictly_shorter": any_strictly_shorter,
        },
    }

    output_path = Path(__file__).resolve().parent / "f-math2-results.json"
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=False) + "\n",
                           encoding="utf-8")
    print(f"\n\nResults written to {output_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)

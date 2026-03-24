#!/usr/bin/env python3
"""reach.py — Measure and improve the swarm's internal reach.

Internal reach = how well any part of the swarm can find, access, and build
on any other part. Three layers:

  1. Domain adjacency reach — can domains route to each other?
  2. Lesson citation reach — can lessons find related knowledge?
  3. Cross-layer reach — do domain links predict lesson links?

Usage:
    python3 tools/reach.py                    # full report
    python3 tools/reach.py --domains          # domain adjacency only
    python3 tools/reach.py --lessons          # lesson reach only
    python3 tools/reach.py --gaps             # actionable gap analysis
    python3 tools/reach.py --for DOMAIN       # contextual reach for a domain
    python3 tools/reach.py --json             # machine-readable
    python3 tools/reach.py --save S529        # save experiment artifact
"""

import argparse
import json
import re
import sys
from collections import defaultdict, deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

ROOT = Path(__file__).resolve().parent.parent
DOMAINS_DIR = ROOT / "domains"
LESSONS_DIR = ROOT / "memory" / "lessons"


def load_adjacency_graph():
    adj = defaultdict(set)
    all_domains = set()
    for ddir in sorted(DOMAINS_DIR.iterdir()):
        if not ddir.is_dir():
            continue
        domain_file = ddir / "DOMAIN.md"
        if not domain_file.exists():
            continue
        name = ddir.name
        all_domains.add(name)
        text = domain_file.read_text(encoding="utf-8", errors="replace")
        for line in text.splitlines()[:10]:
            if line.startswith("Adjacent:"):
                neighbors = [n.strip() for n in line.split(":", 1)[1].split(",")]
                for n in neighbors:
                    if n:
                        adj[name].add(n)
                        adj[n].add(name)
                break
    return dict(adj), all_domains


def domain_bfs(adj, start, all_domains):
    visited = set()
    queue = deque([start])
    while queue:
        node = queue.popleft()
        if node in visited:
            continue
        visited.add(node)
        for neighbor in adj.get(node, set()):
            if neighbor in all_domains and neighbor not in visited:
                queue.append(neighbor)
    return visited


def domain_components(adj, all_domains):
    visited = set()
    components = []
    for d in sorted(all_domains):
        if d not in visited:
            comp = domain_bfs(adj, d, all_domains)
            components.append(comp)
            visited |= comp
    return sorted(components, key=len, reverse=True)


def domain_diameter(adj, component):
    max_dist = 0
    for start in component:
        dist = {start: 0}
        queue = deque([start])
        while queue:
            node = queue.popleft()
            for neighbor in adj.get(node, set()):
                if neighbor in component and neighbor not in dist:
                    dist[neighbor] = dist[node] + 1
                    queue.append(neighbor)
        if dist:
            max_dist = max(max_dist, max(dist.values()))
    return max_dist


def find_bridges(adj, all_domains):
    comps = domain_components(adj, all_domains)
    if not comps:
        return []
    giant = comps[0]
    bridges = []
    for candidate in giant:
        reduced_adj = {}
        for d, neighbors in adj.items():
            if d == candidate:
                continue
            reduced_adj[d] = neighbors - {candidate}
        remaining = giant - {candidate}
        if not remaining:
            continue
        start = next(iter(remaining))
        reachable = domain_bfs(reduced_adj, start, remaining)
        if len(reachable) < len(remaining):
            bridges.append(candidate)
    return bridges


def analyze_domains():
    adj, all_domains = load_adjacency_graph()
    comps = domain_components(adj, all_domains)
    degrees = {d: len(adj.get(d, set()) & all_domains) for d in all_domains}
    isolated = sorted([d for d, deg in degrees.items() if deg == 0])
    avg_degree = sum(degrees.values()) / len(degrees) if degrees else 0
    giant = comps[0] if comps else set()
    bridges = find_bridges(adj, all_domains) if len(giant) > 2 else []
    total_pairs = len(all_domains) * (len(all_domains) - 1) / 2
    reachable_pairs = sum(len(c) * (len(c) - 1) / 2 for c in comps)
    reachability = reachable_pairs / total_pairs if total_pairs > 0 else 0
    diameter = domain_diameter(adj, giant) if giant else 0
    edges = set()
    for d, neighbors in adj.items():
        for n in neighbors:
            edges.add(tuple(sorted([d, n])))
    return {
        "total_domains": len(all_domains),
        "total_edges": len(edges),
        "components": len(comps),
        "giant_component_size": len(giant),
        "giant_component_pct": round(len(giant) / len(all_domains) * 100, 1) if all_domains else 0,
        "reachability": round(reachability, 3),
        "diameter": diameter,
        "avg_degree": round(avg_degree, 2),
        "isolated": isolated,
        "isolated_count": len(isolated),
        "bridges": sorted(bridges),
        "bridge_count": len(bridges),
        "component_sizes": [len(c) for c in comps],
    }


def analyze_lessons():
    try:
        from cite_parse import parse_all_refs
    except ImportError:
        return {"error": "cite_parse.py not found"}
    in_degree = defaultdict(int)
    adj = defaultdict(set)
    lesson_domain = {}
    total_lessons = 0
    for f in sorted(LESSONS_DIR.glob("L-*.md")):
        lid = f.stem
        text = f.read_text(encoding="utf-8", errors="replace")
        if text.startswith("<!--"):
            continue
        total_lessons += 1
        m = re.search(r"Domain:\s*(\S+)", text)
        if m:
            lesson_domain[lid] = m.group(1).strip().rstrip(",")
        refs = parse_all_refs(text)
        for ref in refs:
            if ref != lid:
                in_degree[ref] += 1
                adj[lid].add(ref)
                adj[ref].add(lid)
    sinks = [lid for lid in sorted(lesson_domain.keys()) if in_degree.get(lid, 0) == 0]
    sink_ratio = len(sinks) / total_lessons if total_lessons else 0
    sorted_hubs = sorted(in_degree.items(), key=lambda x: -x[1])
    top10_citations = sum(c for _, c in sorted_hubs[:10])
    total_citations = sum(in_degree.values())
    hub_concentration = top10_citations / total_citations if total_citations else 0
    cross_domain = 0
    same_domain = 0
    for lid, refs in adj.items():
        d1 = lesson_domain.get(lid, "")
        for ref in refs:
            d2 = lesson_domain.get(ref, "")
            if d1 and d2:
                if d1 != d2:
                    cross_domain += 1
                else:
                    same_domain += 1
    cross_ratio = cross_domain / (cross_domain + same_domain) if (cross_domain + same_domain) else 0
    return {
        "total_lessons": total_lessons,
        "total_citations": total_citations,
        "sink_count": len(sinks),
        "sink_ratio": round(sink_ratio, 3),
        "hub_concentration_top10": round(hub_concentration, 3),
        "top_hub": sorted_hubs[0] if sorted_hubs else None,
        "cross_domain_citation_ratio": round(cross_ratio, 3),
        "cross_domain_citations": cross_domain,
        "same_domain_citations": same_domain,
    }


def analyze_gaps():
    adj, all_domains = load_adjacency_graph()
    comps = domain_components(adj, all_domains)
    degrees = {d: len(adj.get(d, set()) & all_domains) for d in all_domains}
    isolated = [d for d, deg in sorted(degrees.items()) if deg == 0]
    gaps = []
    for d in isolated:
        gaps.append({"type": "isolated_domain", "domain": d, "impact": "HIGH",
                      "suggestion": f"Add Adjacent: header to domains/{d}/DOMAIN.md"})
    if len(comps) > 1:
        for i, c1 in enumerate(comps):
            for c2 in comps[i + 1:]:
                d1 = sorted(c1, key=lambda d: degrees.get(d, 0), reverse=True)[0]
                d2 = sorted(c2, key=lambda d: degrees.get(d, 0), reverse=True)[0]
                gaps.append({"type": "component_bridge", "from": d1, "to": d2, "impact": "CRITICAL",
                              "suggestion": f"Link {d1} <-> {d2} to merge components of size {len(c1)} and {len(c2)}"})
    for d, deg in sorted(degrees.items(), key=lambda x: x[1]):
        if deg == 1 and d not in isolated:
            neighbor = list(adj.get(d, set()) & all_domains)[0] if adj.get(d) else "?"
            gaps.append({"type": "fragile_link", "domain": d, "only_neighbor": neighbor, "impact": "MEDIUM",
                          "suggestion": f"Add 1-2 more links from {d} to reduce single-point-of-failure"})
    return gaps


def contextual_reach(target_domain):
    adj, all_domains = load_adjacency_graph()
    if target_domain not in all_domains:
        return {"error": f"Unknown domain: {target_domain}"}
    neighbors_1 = adj.get(target_domain, set()) & all_domains
    neighbors_2 = set()
    for n in neighbors_1:
        neighbors_2 |= (adj.get(n, set()) & all_domains)
    neighbors_2 -= neighbors_1
    neighbors_2.discard(target_domain)
    try:
        from cite_parse import parse_all_refs
    except ImportError:
        return {"error": "cite_parse.py not found"}
    target_cites = set()
    for f in sorted(LESSONS_DIR.glob("L-*.md")):
        text = f.read_text(encoding="utf-8", errors="replace")
        if text.startswith("<!--"):
            continue
        m = re.search(r"Domain:\s*(\S+)", text)
        if m and m.group(1).strip().rstrip(",") == target_domain:
            target_cites |= set(parse_all_refs(text))
    suggestions = []
    for f in sorted(LESSONS_DIR.glob("L-*.md")):
        lid = f.stem
        if lid in target_cites:
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        if text.startswith("<!--"):
            continue
        m = re.search(r"Domain:\s*(\S+)", text)
        if not m:
            continue
        domain = m.group(1).strip().rstrip(",")
        if domain not in neighbors_1 and domain not in neighbors_2:
            continue
        sharpe = 5
        sm = re.search(r"Sharpe:\s*(\d+)", text)
        if sm:
            sharpe = int(sm.group(1))
        if sharpe < 7:
            continue
        title = ""
        for line in text.splitlines()[:5]:
            if line.startswith("Title:") or line.startswith("# L-"):
                title = line.strip()[:80]
                break
        hop = 1 if domain in neighbors_1 else 2
        suggestions.append({"lesson": lid, "domain": domain, "sharpe": sharpe, "hop": hop, "title": title})
    suggestions.sort(key=lambda x: (-x["sharpe"], x["hop"]))
    return {"target": target_domain, "neighbors_1hop": sorted(neighbors_1),
            "neighbors_2hop": sorted(neighbors_2)[:10], "suggestions": suggestions[:15]}


def print_report(domain_data=None, lesson_data=None, gap_data=None):
    print("=== SWARM INTERNAL REACH REPORT ===\n")
    if domain_data:
        print("-- Domain Adjacency Reach --")
        print(f"  Domains: {domain_data['total_domains']} | Edges: {domain_data['total_edges']}")
        print(f"  Giant component: {domain_data['giant_component_size']}/{domain_data['total_domains']} ({domain_data['giant_component_pct']}%)")
        print(f"  Reachability: {domain_data['reachability']:.1%}")
        print(f"  Diameter: {domain_data['diameter']} hops")
        print(f"  Avg degree: {domain_data['avg_degree']}")
        if domain_data['isolated']:
            print(f"  ! Isolated ({domain_data['isolated_count']}): {', '.join(domain_data['isolated'][:10])}")
        if domain_data['bridges']:
            print(f"  ! Bridges ({domain_data['bridge_count']}): {', '.join(domain_data['bridges'])}")
        print(f"  Components: {domain_data['components']} (sizes: {domain_data['component_sizes'][:5]})")
        print()
    if lesson_data and "error" not in lesson_data:
        print("-- Lesson Citation Reach --")
        print(f"  Lessons: {lesson_data['total_lessons']} | Citations: {lesson_data['total_citations']}")
        print(f"  Sinks (0 in-degree): {lesson_data['sink_count']} ({lesson_data['sink_ratio']:.1%})")
        print(f"  Hub concentration (top 10): {lesson_data['hub_concentration_top10']:.1%}")
        if lesson_data['top_hub']:
            print(f"  Top hub: {lesson_data['top_hub'][0]} ({lesson_data['top_hub'][1]} citations)")
        print(f"  Cross-domain citations: {lesson_data['cross_domain_citation_ratio']:.1%}")
        print()
    if gap_data:
        print("-- Reach Gaps --")
        for impact in ["CRITICAL", "HIGH", "MEDIUM"]:
            items = [g for g in gap_data if g['impact'] == impact]
            if items:
                print(f"  {impact} ({len(items)}):")
                for g in items[:5]:
                    print(f"    -> {g['suggestion']}")
                if len(items) > 5:
                    print(f"    ... and {len(items) - 5} more")
        print()
    if domain_data and lesson_data and "error" not in lesson_data:
        score = (domain_data['reachability'] * 0.4 + (1 - lesson_data['sink_ratio']) * 0.3 +
                 (1 - lesson_data['hub_concentration_top10']) * 0.15 + lesson_data['cross_domain_citation_ratio'] * 0.15)
        print(f"-- Overall Reach Score: {score:.3f} --")


def main():
    parser = argparse.ArgumentParser(description="Swarm internal reach measurement")
    parser.add_argument("--domains", action="store_true")
    parser.add_argument("--lessons", action="store_true")
    parser.add_argument("--gaps", action="store_true")
    parser.add_argument("--for", dest="for_domain", metavar="DOMAIN")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--save", metavar="SESSION")
    args = parser.parse_args()

    if args.for_domain:
        result = contextual_reach(args.for_domain)
        if args.json:
            print(json.dumps(result, indent=2, default=str))
        else:
            if "error" in result:
                print(f"Error: {result['error']}")
                return
            print(f"=== CONTEXTUAL REACH: {result['target']} ===\n")
            print(f"1-hop: {', '.join(result['neighbors_1hop'])}")
            print(f"2-hop: {', '.join(result['neighbors_2hop'])}")
            if result['suggestions']:
                print("\nHigh-value unreached lessons (Sharpe >= 7):")
                for s in result['suggestions']:
                    print(f"  {s['lesson']} S{s['sharpe']} [{s['domain']}, {'1-hop' if s['hop'] == 1 else '2-hop'}] {s['title']}")
        return

    show_all = not (args.domains or args.lessons or args.gaps)
    domain_data = analyze_domains() if (show_all or args.domains or args.gaps) else None
    lesson_data = analyze_lessons() if (show_all or args.lessons) else None
    gap_data = analyze_gaps() if (show_all or args.gaps) else None

    if args.json:
        result = {}
        if domain_data:
            result["domains"] = domain_data
        if lesson_data:
            result["lessons"] = lesson_data
        if gap_data:
            result["gaps"] = gap_data
        print(json.dumps(result, indent=2, default=str))
    else:
        print_report(domain_data, lesson_data, gap_data)

    if args.save:
        out = ROOT / "experiments" / "meta" / f"reach-s{args.save}.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        with open(out, "w") as f:
            json.dump({"experiment": "reach", "session": f"S{args.save}",
                        "domains": domain_data, "lessons": lesson_data}, f, indent=2, default=str)
        print(f"Saved: {out}")


if __name__ == "__main__":
    main()

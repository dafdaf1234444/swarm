#!/usr/bin/env python3
"""wiki_swarm.py — crawl a small Wikipedia neighborhood from a seed topic.

Usage:
    python3 tools/wiki_swarm.py <topic> [--depth 1] [--fanout 5] [--lang en] [--out FILE]
    python3 tools/wiki_swarm.py --auto [--depth 1] [--fanout 5]
    python3 tools/wiki_swarm.py
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from collections import deque
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
USER_AGENT = "swarm-wiki/0.1 (+https://github.com/dafdaf1234444/swarm)"
DEFAULT_AUTO_TOPIC = "Swarm intelligence"
GENERIC_INVOCATIONS = {
    "swarm",
    "swarm this",
    "swarm it",
    "wiki swarm",
    "start wiki swarm",
    "run wiki swarm",
}
AUTO_TOPICS = [
    ("Swarm intelligence", ("swarm", "colony", "agent", "parallel")),
    ("Stigmergy", ("stigmergy", "bulletin", "append-only", "pheromone")),
    ("Distributed systems", ("distributed", "replication", "consensus", "fault")),
    ("Error handling", ("error handling", "eh", "retry", "failure")),
    ("Conflict-free replicated data type", ("crdt", "append-only", "monotonic")),
    ("Transactive memory", ("transactive", "memory", "specialist", "coordination")),
]
STOPWORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "how",
    "if",
    "in",
    "into",
    "is",
    "it",
    "its",
    "of",
    "on",
    "or",
    "that",
    "the",
    "their",
    "this",
    "to",
    "what",
    "when",
    "where",
    "which",
    "who",
    "why",
    "with",
}


def _request_json(url: str, timeout: int = 15) -> dict:
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8", errors="replace"))


def _clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    return text if text else "(no summary available)"


def _search_titles(query: str, lang: str, limit: int = 1) -> list[str]:
    q = urllib.parse.quote_plus(query)
    url = (
        f"https://{lang}.wikipedia.org/w/api.php"
        f"?action=query&list=search&srsearch={q}&srlimit={limit}&format=json"
    )
    data = _request_json(url)
    return [item.get("title", "").strip() for item in data.get("query", {}).get("search", []) if item.get("title")]


def _keyword_queries(text: str) -> list[str]:
    words = re.findall(r"[A-Za-z][A-Za-z-]+", (text or "").lower())
    keywords: list[str] = []
    for word in words:
        if word in STOPWORDS:
            continue
        stem = word
        if stem.endswith("ing") and len(stem) > 6:
            stem = stem[:-3]
        if stem.startswith("mis") and len(stem) > 6:
            keywords.append(stem[3:])
        keywords.append(stem)

    deduped: list[str] = []
    for word in keywords:
        if word and word not in deduped:
            deduped.append(word)

    queries: list[str] = []
    if len(deduped) >= 3:
        queries.append(" ".join(deduped[:3]))
    if len(deduped) >= 2:
        queries.append(" ".join(deduped[:2]))
    queries.extend(deduped)
    return queries


def resolve_topic(topic: str, lang: str) -> str:
    """Resolve a free-form query to a canonical Wikipedia title."""
    topic = topic.strip()
    if not topic:
        return topic

    results = _search_titles(topic, lang, limit=1)
    if results:
        return results[0]

    for query in _keyword_queries(topic):
        if query == topic:
            continue
        fallback = _search_titles(query, lang, limit=1)
        if fallback:
            return fallback[0]

    return topic


def fetch_summary(title: str, lang: str) -> dict | None:
    """Fetch page summary from REST API."""
    safe_title = urllib.parse.quote(title.replace(" ", "_"), safe="()")
    url = f"https://{lang}.wikipedia.org/api/rest_v1/page/summary/{safe_title}"
    try:
        data = _request_json(url)
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise

    page_url = (
        data.get("content_urls", {})
        .get("desktop", {})
        .get("page", f"https://{lang}.wikipedia.org/wiki/{safe_title}")
    )
    return {
        "title": data.get("title", title),
        "summary": _clean_text(data.get("extract", "")),
        "url": page_url,
    }


def fetch_related_titles(title: str, lang: str, limit: int) -> list[str]:
    """Fetch semantically related titles via search relevance."""
    q = urllib.parse.quote_plus(title)
    # Pull extra candidates to compensate for filtering exact-match and numeric pages.
    search_limit = min(max(limit * 3, 10), 50)
    url = (
        f"https://{lang}.wikipedia.org/w/api.php"
        f"?action=query&list=search&srsearch={q}&srlimit={search_limit}&format=json"
    )
    data = _request_json(url)
    pages = data.get("query", {}).get("search", [])
    titles: list[str] = []
    for page in pages:
        candidate = page.get("title", "").strip()
        if not candidate or candidate == title:
            continue
        if re.match(r"^\d", candidate):
            continue
        titles.append(candidate)
    return titles[:limit]


def fetch_links(title: str, lang: str, limit: int) -> list[str]:
    """Fallback: fetch page links (main namespace only)."""
    safe_title = urllib.parse.quote_plus(title)
    url = (
        f"https://{lang}.wikipedia.org/w/api.php"
        f"?action=query&titles={safe_title}&prop=links&plnamespace=0&pllimit=max&format=json&redirects=1"
    )
    data = _request_json(url)
    pages = data.get("query", {}).get("pages", {})
    if not pages:
        return []

    first_page = next(iter(pages.values()))
    links = first_page.get("links", [])
    titles = [link.get("title", "").strip() for link in links]
    titles = [t for t in titles if t]
    return titles[:limit]


def choose_auto_topic() -> tuple[str, str]:
    """Infer a sensible seed topic from current swarm state files."""
    files = [
        REPO_ROOT / "tasks" / "NEXT.md",
        REPO_ROOT / "tasks" / "FRONTIER.md",
        REPO_ROOT / "memory" / "INDEX.md",
    ]
    corpus = []
    for path in files:
        try:
            corpus.append(path.read_text(encoding="utf-8", errors="replace").lower())
        except Exception:
            continue
    text = "\n".join(corpus)

    best_topic = DEFAULT_AUTO_TOPIC
    best_score = 0
    for topic, keywords in AUTO_TOPICS:
        score = sum(text.count(keyword.lower()) for keyword in keywords)
        if score > best_score:
            best_topic = topic
            best_score = score

    if best_score <= 0:
        return best_topic, "auto(default)"
    return best_topic, f"auto(state-score={best_score})"


def swarm_topic(seed: str, depth: int, fanout: int, lang: str) -> tuple[str, list[dict]]:
    """Breadth-first traversal of Wikipedia pages around a seed topic."""
    root = resolve_topic(seed, lang)
    queue: deque[tuple[str, int]] = deque([(root, 0)])
    visited: set[str] = set()
    nodes: list[dict] = []

    while queue:
        current_title, current_depth = queue.popleft()
        if current_title in visited:
            continue
        visited.add(current_title)

        summary = fetch_summary(current_title, lang)
        if not summary:
            continue

        children: list[str] = []
        if current_depth < depth:
            try:
                children = fetch_related_titles(summary["title"], lang, fanout)
            except Exception:
                try:
                    children = fetch_links(summary["title"], lang, fanout)
                except Exception:
                    children = []

        nodes.append(
            {
                "title": summary["title"],
                "depth": current_depth,
                "summary": summary["summary"],
                "url": summary["url"],
                "children": children,
            }
        )

        if current_depth < depth:
            for child_title in children:
                if child_title not in visited:
                    queue.append((child_title, current_depth + 1))

    return root, nodes


def render_markdown(
    seed: str,
    resolved: str,
    depth: int,
    fanout: int,
    lang: str,
    nodes: list[dict],
    topic_source: str,
) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        f"# Wiki Swarm: {seed}",
        "",
        f"- Resolved topic: `{resolved}`",
        f"- Topic source: `{topic_source}`",
        f"- Depth: {depth}",
        f"- Fanout: {fanout}",
        f"- Language: `{lang}`",
        f"- Generated: {ts}",
        "",
    ]

    if not nodes:
        lines.append("No pages were retrieved.")
        return "\n".join(lines)

    for node in nodes:
        lines.extend(
            [
                f"## {node['title']} (depth {node['depth']})",
                f"- URL: {node['url']}",
                f"- Summary: {node['summary']}",
            ]
        )
        if node["children"]:
            children = ", ".join(node["children"])
            lines.append(f"- Related pages sampled: {children}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Swarm a Wikipedia topic by traversing related pages."
    )
    parser.add_argument("topic", nargs="*", help="Seed topic to explore.")
    parser.add_argument("--depth", type=int, default=1, help="Traversal depth (default: 1).")
    parser.add_argument("--fanout", type=int, default=5, help="Links sampled per page (default: 5).")
    parser.add_argument("--lang", default="en", help="Wikipedia language code (default: en).")
    parser.add_argument("--out", help="Optional output markdown path.")
    parser.add_argument(
        "--auto",
        action="store_true",
        help="Infer a topic from swarm state files when topic is omitted or generic.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    topic = " ".join(args.topic).strip()
    depth = max(0, min(args.depth, 3))
    fanout = max(1, min(args.fanout, 20))
    lang = args.lang.strip() or "en"
    use_auto = args.auto or not topic or topic.lower() in GENERIC_INVOCATIONS
    topic_source = "manual"

    if use_auto:
        topic, topic_source = choose_auto_topic()

    try:
        resolved, nodes = swarm_topic(topic, depth, fanout, lang)
    except Exception as e:
        print(f"wiki_swarm.py error: {e}", file=sys.stderr)
        return 1

    report = render_markdown(topic, resolved, depth, fanout, lang, nodes, topic_source)

    if args.out:
        out_path = Path(args.out)
        if not out_path.is_absolute():
            out_path = REPO_ROOT / out_path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(report, encoding="utf-8")
        print(f"Wrote report: {out_path}")
    else:
        print(report)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

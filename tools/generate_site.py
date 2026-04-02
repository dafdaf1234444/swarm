#!/usr/bin/env python3
"""
generate_site.py — Generate the public records page from the database.

Reads records/*.json, generates docs/records.html with real cards
for real leaders with real evidence.

Run: python3 tools/generate_site.py
"""

import json
import glob
import os

from classify import SINS, classify_facts, highest_tier


def load_all_records():
    """Load all JSON records."""
    records = []
    for path in sorted(glob.glob("records/*.json")):
        if "examples" in path:
            continue  # Skip composite examples
        with open(path) as f:
            data = json.load(f)
        if isinstance(data, list):
            records.extend(data)
        else:
            records.append(data)
    return records


def tier_color(tier):
    return {1: "#d4a574", 2: "#c47474", 3: "#8a4a4a"}.get(tier, "#666")


def tier_label(tier):
    return {1: "TIER 1", 2: "TIER 2", 3: "TIER 3"}.get(tier, "?")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def generate_card_html(record):
    name = esc(record["name"])
    role = esc(record.get("role", ""))
    country = esc(record.get("country", ""))
    said = record.get("said", [])
    did = record.get("did", [])
    facts = record.get("facts", [])
    sources = record.get("sources", [])
    grade = record.get("grade", "C")

    matches = classify_facts(facts + did)
    tier = highest_tier(matches)
    tc = tier_color(tier)

    # Sin badges
    sin_html = ""
    for code in matches:
        sin = SINS[code]
        c = tier_color(sin["tier"])
        sin_html += f'<span style="background:{c};color:#fff;padding:3px 10px;border-radius:5px;font-size:12px;margin:2px 4px 2px 0;display:inline-block;">{esc(sin["name"])}</span>'

    # Said
    said_html = "<br>".join(f'"{esc(s)}"' for s in said[:2])

    # Did — most impactful 3
    did_html = "<br>".join(esc(d) for d in did[:3])
    if len(did) > 3:
        did_html += f'<br><span style="color:#886;">+{len(did)-3} more documented actions</span>'

    # Sources
    src_html = " &middot; ".join(esc(s) for s in sources[:4])
    if len(sources) > 4:
        src_html += f" &middot; +{len(sources)-4} more"

    return f"""
<div class="record-card" style="border-left:4px solid {tc};">
  <div class="rc-header">
    <div class="rc-name">{name}</div>
    <div class="rc-role">{role} — {country}</div>
    <div class="rc-tier" style="background:{tc};">{tier_label(tier)}</div>
  </div>
  <div class="rc-body">
    <div class="rc-said">
      <div class="rc-label" style="color:#6a9a6a;">THEY SAID</div>
      {said_html}
    </div>
    <div class="rc-did">
      <div class="rc-label" style="color:#c47474;">THEY DID</div>
      {did_html}
    </div>
  </div>
  <div class="rc-sins">{sin_html}</div>
  <div class="rc-evidence">
    <span class="rc-grade">Grade {esc(grade)}</span>
    <span class="rc-sources">{src_html}</span>
  </div>
</div>"""


def generate_page(records):
    # Sort by tier (worst first), then name
    def sort_key(r):
        matches = classify_facts(r.get("facts", []) + r.get("did", []))
        return (-highest_tier(matches), r["name"])

    records.sort(key=sort_key)

    cards_html = "\n".join(generate_card_html(r) for r in records)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>The Record — What they said. What they did.</title>
<meta name="description" content="{len(records)} leaders. Public evidence. Grade A. You decide.">
<meta property="og:title" content="The Record — {len(records)} leaders. What they said. What they did.">
<meta property="og:description" content="Public records. Evidence graded. Every source named. You decide what it means.">
<meta property="og:image" content="https://dafdaf1234444.github.io/godding/card.png">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>&#128065;</text></svg>">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
    font-family: Georgia, 'Times New Roman', serif;
    background: #111;
    color: #ddd;
    min-height: 100vh;
}}
.top {{
    text-align: center;
    padding: 60px 20px 40px;
    max-width: 600px;
    margin: 0 auto;
}}
.top h1 {{ font-size: 28px; font-weight: normal; color: #fff; margin-bottom: 10px; }}
.top h1 span {{ color: #d4756a; }}
.top p {{ color: #666; font-size: 15px; line-height: 1.7; margin-bottom: 8px; }}
.count {{ font-size: 48px; color: #d4756a; margin: 20px 0 8px; }}
.count-label {{ color: #666; font-size: 14px; margin-bottom: 30px; }}

.records {{
    max-width: 520px;
    margin: 0 auto;
    padding: 0 16px 60px;
}}

.record-card {{
    background: #1a1a1a;
    border-radius: 12px;
    margin: 20px 0;
    overflow: hidden;
}}
.rc-header {{
    padding: 20px 24px 12px;
    display: flex;
    flex-wrap: wrap;
    align-items: baseline;
    gap: 8px;
}}
.rc-name {{ font-size: 20px; color: #fff; flex: 1; min-width: 200px; }}
.rc-role {{ font-size: 13px; color: #777; flex-basis: 100%; }}
.rc-tier {{
    color: #fff;
    font-size: 11px;
    font-weight: bold;
    padding: 3px 10px;
    border-radius: 5px;
    letter-spacing: 1px;
    position: absolute;
    right: 24px;
}}
.rc-header {{ position: relative; }}

.rc-body {{ padding: 0 24px; }}
.rc-said {{
    background: #1a2a1a;
    margin: 0 -24px;
    padding: 16px 24px;
}}
.rc-did {{
    background: #2a1a1a;
    margin: 0 -24px;
    padding: 16px 24px;
    font-size: 15px;
    line-height: 1.6;
    color: #daa;
}}
.rc-said {{ font-size: 15px; line-height: 1.6; color: #ada; }}
.rc-label {{
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-bottom: 8px;
    font-weight: bold;
}}

.rc-sins {{ padding: 12px 24px; }}
.rc-evidence {{
    padding: 12px 24px;
    background: #151515;
    display: flex;
    align-items: center;
    gap: 10px;
    flex-wrap: wrap;
}}
.rc-grade {{
    background: #2a3a2a;
    color: #7a9a7a;
    font-size: 13px;
    font-weight: bold;
    padding: 4px 12px;
    border-radius: 6px;
    flex-shrink: 0;
}}
.rc-sources {{ font-size: 12px; color: #555; line-height: 1.4; }}

.bottom {{
    text-align: center;
    padding: 40px 20px 60px;
    max-width: 500px;
    margin: 0 auto;
}}
.bottom p {{ color: #555; font-size: 14px; margin-bottom: 12px; line-height: 1.7; }}
.bottom a {{
    color: #888;
    text-decoration: none;
    margin: 0 6px;
    font-size: 13px;
}}
.bottom a:hover {{ color: #ccc; }}
.bottom .big {{
    display: inline-block;
    background: #1a1a1a;
    color: #bbb;
    padding: 14px 28px;
    border-radius: 10px;
    border: 1px solid #333;
    font-size: 15px;
    font-family: inherit;
    text-decoration: none;
    margin: 8px;
}}
.bottom .big:hover {{ background: #222; color: #fff; border-color: #555; }}
</style>
</head>
<body>

<div class="top">
    <h1>What your leaders said.<br><span>What they actually did.</span></h1>
    <div class="count">{len(records)}</div>
    <div class="count-label">leaders &middot; public evidence &middot; Grade A &middot; you decide</div>
    <p>
        Every fact below has a named source. Court records. ICC warrants.
        UN reports. Federal convictions. Their own financial disclosures.
        Their own words.
    </p>
    <p>
        This is not opinion. This is record.
    </p>
</div>

<div class="records">
{cards_html}
</div>

<div class="bottom">
    <p>
        These {len(records)} records are the beginning.<br>
        Anyone can add their country's leader. Same format. Same evidence standard.<br>
        The code is open. The data is open. Nobody controls it.
    </p>

    <a class="big" href="all.html">The six sins no one can defend</a>
    <a class="big" href="see.html">How we verify</a>

    <div style="margin-top:24px;padding-top:20px;border-top:1px solid #222;">
        <a href="spread.html">How to spread this</a>
        <a href="justice.html">What is justice</a>
        <a href="door.html">The door</a>
        <a href="index.html">Godding</a>
    </div>

    <p style="color:#333;font-size:11px;margin-top:32px;">
        No tracking. No ads. No owner. Open source. Public records only.<br>
        The tool describes. It does not sentence. You decide.
    </p>
</div>

</body>
</html>"""


if __name__ == "__main__":
    records = load_all_records()
    print(f"Loaded {len(records)} records")

    html = generate_page(records)
    out_path = "docs/records.html"
    with open(out_path, "w") as f:
        f.write(html)
    print(f"Generated {out_path}")
    print(f"Records by tier:")
    for r in records:
        matches = classify_facts(r.get("facts", []) + r.get("did", []))
        tier = highest_tier(matches)
        print(f"  Tier {tier}: {r['name']}")

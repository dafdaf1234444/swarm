#!/usr/bin/env python3
"""
generate_network.py — Generate a visual network map from all records.

Shows WHO is connected to WHOM, and HOW.
Simple enough that a picture tells the story.

Run: python3 tools/generate_network.py
"""

import json
import glob

from classify import SINS, classify_facts, highest_tier


def load_all_records():
    records = []
    for path in sorted(glob.glob("records/*.json")):
        if "examples" in path:
            continue
        with open(path) as f:
            data = json.load(f)
        if isinstance(data, list):
            records.extend(data)
        else:
            records.append(data)
    return records


# Known connections (from court records, flight logs, financial records)
CONNECTIONS = [
    # Epstein core
    ("Jeffrey Epstein", "Ghislaine Maxwell", "Partner in trafficking — convicted"),
    ("Jeffrey Epstein", "Jean-Luc Brunel", "Supplied victims — charged"),
    ("Jeffrey Epstein", "Prince Andrew (Duke of York)", "Flight logs, island visits, photo with victim"),
    ("Jeffrey Epstein", "Alan Dershowitz", "Legal team + named by victim under oath"),
    ("Jeffrey Epstein", "Bill Clinton", "26+ flights on Epstein's planes"),
    ("Jeffrey Epstein", "Donald Trump", "Photos, quotes, flight records, Mar-a-Lago"),
    ("Jeffrey Epstein", "Bill Gates", "Multiple meetings after conviction"),
    ("Jeffrey Epstein", "Leon Black", "$158M payments after conviction"),
    ("Jeffrey Epstein", "Jes Staley", "1,200+ emails, island visits, prison visits"),
    ("Jeffrey Epstein", "Les Wexner", "Power of attorney, $77M mansion gift"),
    ("Jeffrey Epstein", "Alex Acosta", "Sweetheart plea deal — protected co-conspirators"),
    ("Jeffrey Epstein", "JP Morgan Chase", "Client for 15 years including after conviction"),
    ("Jeffrey Epstein", "Deutsche Bank", "Client after JP Morgan dropped him"),
    ("Ghislaine Maxwell", "Prince Andrew (Duke of York)", "Photo at her London home with victim"),
    ("Ghislaine Maxwell", "Jean-Luc Brunel", "Collaborated on victim recruitment"),
    ("Alex Acosta", "Donald Trump", "Appointed as Labor Secretary"),

    # Geopolitical
    ("Donald Trump", "Vladimir Putin", "Documented relationship, Helsinki summit, intelligence sharing concerns"),
    ("Donald Trump", "Mohammed bin Salman (MBS)", "Arms deal, Kushner $2B Saudi investment"),
    ("Donald Trump", "Benjamin Netanyahu", "Political alliance, policy coordination"),
    ("Vladimir Putin", "Alexander Lukashenko", "Military alliance, enabled Ukraine invasion from Belarus"),
    ("Vladimir Putin", "Bashar al-Assad", "Military intervention to keep Assad in power"),
    ("Vladimir Putin", "Xi Jinping", "'No limits' partnership declared Feb 2022"),
    ("Xi Jinping", "Kim Jong-un", "Primary economic and diplomatic supporter"),

    # Corporate-political
    ("Goldman Sachs (David Solomon / Lloyd Blankfein era)", "Mohammed bin Salman (MBS)", "1MDB connections, Saudi business"),
    ("ExxonMobil Leadership (Rex Tillerson / Darren Woods era)", "Vladimir Putin", "Tillerson received Order of Friendship from Putin"),
    ("Meta / Facebook (Mark Zuckerberg)", "Donald Trump", "Platform policies, political advertising"),
]


def tier_color(tier):
    return {0: "#666", 1: "#d4a574", 2: "#c47474", 3: "#8a4a4a"}.get(tier, "#666")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&#39;")


def generate_network_page(records):
    # Build node data
    nodes = []
    name_to_tier = {}
    for r in records:
        matches = classify_facts(r.get("facts", []) + r.get("did", []))
        tier = highest_tier(matches)
        name_to_tier[r["name"]] = tier
        sin_names = [SINS[c]["name"] for c in matches]
        nodes.append({
            "name": r["name"],
            "role": r.get("role", ""),
            "country": r.get("country", ""),
            "tier": tier,
            "sins": sin_names,
            "grade": r.get("grade", "?"),
        })

    # Filter connections to only include people in our records
    record_names = {r["name"] for r in records}
    edges = []
    for a, b, reason in CONNECTIONS:
        if a in record_names and b in record_names:
            edges.append({"from": a, "to": b, "reason": reason})

    nodes_json = json.dumps(nodes)
    edges_json = json.dumps(edges)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>The Network — Who knows who</title>
<meta name="description" content="Visual map of connections between leaders, CEOs, and the Epstein network.">
<meta property="og:title" content="The Network — Who knows who">
<meta property="og:description" content="Follow the connections. Flight logs. Payments. Meetings. All documented.">
<link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>&#128065;</text></svg>">
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: Georgia, serif; background: #111; color: #ddd; min-height: 100vh; }}
.top {{ text-align: center; padding: 40px 20px 20px; }}
.top h1 {{ font-size: 26px; color: #fff; font-weight: normal; }}
.top h1 span {{ color: #d4756a; }}
.top p {{ color: #666; font-size: 14px; margin-top: 8px; }}
.legend {{ display: flex; justify-content: center; gap: 16px; padding: 16px; flex-wrap: wrap; }}
.legend-item {{ font-size: 12px; display: flex; align-items: center; gap: 6px; }}
.legend-dot {{ width: 14px; height: 14px; border-radius: 50%; }}

.network {{ position: relative; width: 100%; height: 70vh; min-height: 500px; overflow: hidden; }}
canvas {{ width: 100%; height: 100%; }}

.tooltip {{
    display: none;
    position: fixed;
    background: #222;
    border: 1px solid #444;
    border-radius: 8px;
    padding: 14px 18px;
    max-width: 320px;
    z-index: 100;
    pointer-events: none;
}}
.tooltip .tt-name {{ font-size: 16px; color: #fff; margin-bottom: 4px; }}
.tooltip .tt-role {{ font-size: 12px; color: #888; margin-bottom: 8px; }}
.tooltip .tt-sins {{ margin-bottom: 6px; }}
.tooltip .tt-sin {{ display: inline-block; padding: 2px 8px; border-radius: 4px; font-size: 11px; color: #fff; margin: 2px; }}
.tooltip .tt-connections {{ font-size: 12px; color: #999; border-top: 1px solid #333; padding-top: 8px; margin-top: 4px; }}
.tooltip .tt-conn {{ margin: 3px 0; }}

.stats {{ text-align: center; padding: 20px; color: #555; font-size: 13px; }}
.stats span {{ color: #999; }}

.bottom {{ text-align: center; padding: 30px 20px 50px; }}
.bottom a {{ color: #666; text-decoration: none; font-size: 13px; margin: 0 8px; }}
.bottom a:hover {{ color: #999; }}
.bottom .big {{
    display: inline-block; background: #1a1a1a; color: #bbb;
    padding: 14px 28px; border-radius: 10px; border: 1px solid #333;
    font-size: 15px; font-family: inherit; text-decoration: none; margin: 8px;
}}
.bottom .big:hover {{ background: #222; color: #fff; border-color: #555; }}
</style>
</head>
<body>

<div class="top">
    <h1>The Network — <span>who knows who</span></h1>
    <p>Every line is a documented connection. Flight logs. Payments. Meetings. Court records.</p>
</div>

<div class="legend">
    <div class="legend-item"><div class="legend-dot" style="background:#8a4a4a;"></div> Tier 3 — Children harmed</div>
    <div class="legend-item"><div class="legend-dot" style="background:#c47474;"></div> Tier 2 — Murder / slavery / truth</div>
    <div class="legend-item"><div class="legend-dot" style="background:#d4a574;"></div> Tier 1 — Corruption / betrayal</div>
    <div class="legend-item"><div class="legend-dot" style="background:#666;"></div> Tier 0 — Insufficient data</div>
</div>

<div class="network">
    <canvas id="graph"></canvas>
</div>
<div class="tooltip" id="tooltip">
    <div class="tt-name"></div>
    <div class="tt-role"></div>
    <div class="tt-sins"></div>
    <div class="tt-connections"></div>
</div>

<div class="stats">
    <span>{len(nodes)}</span> people &middot;
    <span>{len(edges)}</span> documented connections &middot;
    all sourced &middot; all graded
</div>

<div class="bottom">
    <a class="big" href="records.html">See all records</a>
    <a class="big" href="door.html">Said vs Did</a>
    <div style="margin-top:20px;">
        <a href="all.html">The six sins</a>
        <a href="see.html">How we verify</a>
        <a href="spread.html">How to share</a>
        <a href="index.html">Godding</a>
    </div>
    <p style="color:#333;font-size:11px;margin-top:24px;">
        No tracking. No ads. No owner. Open source.<br>
        Every connection documented. You decide what it means.
    </p>
</div>

<script>
const NODES = {nodes_json};
const EDGES = {edges_json};

const canvas = document.getElementById('graph');
const ctx = canvas.getContext('2d');
const tooltip = document.getElementById('tooltip');

function resize() {{
    const r = canvas.parentElement.getBoundingClientRect();
    canvas.width = r.width * 2;
    canvas.height = r.height * 2;
    canvas.style.width = r.width + 'px';
    canvas.style.height = r.height + 'px';
    ctx.setTransform(2, 0, 0, 2, 0, 0);
}}
resize();
window.addEventListener('resize', () => {{ resize(); }});

const W = () => canvas.width / 2;
const H = () => canvas.height / 2;

const tierColor = {{ 0: '#666', 1: '#d4a574', 2: '#c47474', 3: '#8a4a4a' }};
const tierSize = {{ 0: 6, 1: 8, 2: 10, 3: 14 }};

// Layout: force-directed (simple)
const pos = {{}};
NODES.forEach((n, i) => {{
    const angle = (i / NODES.length) * Math.PI * 2;
    const r = 150 + Math.random() * 80;
    pos[n.name] = {{ x: W()/2 + Math.cos(angle) * r, y: H()/2 + Math.sin(angle) * r, vx: 0, vy: 0 }};
}});

// Count connections per node
const connCount = {{}};
EDGES.forEach(e => {{
    connCount[e.from] = (connCount[e.from] || 0) + 1;
    connCount[e.to] = (connCount[e.to] || 0) + 1;
}});

function simulate() {{
    // Repulsion between all nodes
    for (let i = 0; i < NODES.length; i++) {{
        for (let j = i + 1; j < NODES.length; j++) {{
            const a = pos[NODES[i].name], b = pos[NODES[j].name];
            let dx = b.x - a.x, dy = b.y - a.y;
            let d = Math.sqrt(dx*dx + dy*dy) || 1;
            let f = 800 / (d * d);
            a.vx -= dx / d * f;
            a.vy -= dy / d * f;
            b.vx += dx / d * f;
            b.vy += dy / d * f;
        }}
    }}
    // Attraction along edges
    EDGES.forEach(e => {{
        const a = pos[e.from], b = pos[e.to];
        if (!a || !b) return;
        let dx = b.x - a.x, dy = b.y - a.y;
        let d = Math.sqrt(dx*dx + dy*dy) || 1;
        let f = (d - 100) * 0.01;
        a.vx += dx / d * f;
        a.vy += dy / d * f;
        b.vx -= dx / d * f;
        b.vy -= dy / d * f;
    }});
    // Center gravity
    NODES.forEach(n => {{
        const p = pos[n.name];
        p.vx += (W()/2 - p.x) * 0.002;
        p.vy += (H()/2 - p.y) * 0.002;
        p.x += p.vx * 0.3;
        p.y += p.vy * 0.3;
        p.vx *= 0.8;
        p.vy *= 0.8;
        // Bounds
        p.x = Math.max(40, Math.min(W() - 40, p.x));
        p.y = Math.max(40, Math.min(H() - 40, p.y));
    }});
}}

function draw() {{
    ctx.clearRect(0, 0, W(), H());

    // Draw edges
    EDGES.forEach(e => {{
        const a = pos[e.from], b = pos[e.to];
        if (!a || !b) return;
        ctx.beginPath();
        ctx.moveTo(a.x, a.y);
        ctx.lineTo(b.x, b.y);
        ctx.strokeStyle = 'rgba(255,255,255,0.08)';
        ctx.lineWidth = 1;
        ctx.stroke();
    }});

    // Draw nodes
    NODES.forEach(n => {{
        const p = pos[n.name];
        const c = tierColor[n.tier] || '#666';
        const s = tierSize[n.tier] || 6;
        const conns = connCount[n.name] || 0;
        const size = s + conns * 1.5;

        ctx.beginPath();
        ctx.arc(p.x, p.y, size, 0, Math.PI * 2);
        ctx.fillStyle = c;
        ctx.globalAlpha = 0.8;
        ctx.fill();
        ctx.globalAlpha = 1;

        // Label
        ctx.fillStyle = '#aaa';
        ctx.font = '9px Georgia';
        ctx.textAlign = 'center';
        const short = n.name.length > 20 ? n.name.split(' ').slice(0, 2).join(' ') : n.name;
        ctx.fillText(short, p.x, p.y + size + 12);
    }});
}}

// Simulate
let frame = 0;
function loop() {{
    simulate();
    draw();
    frame++;
    if (frame < 300) requestAnimationFrame(loop);
    else {{ draw(); /* final frame */ }}
}}
loop();

// Tooltip on hover
canvas.addEventListener('mousemove', (evt) => {{
    const rect = canvas.getBoundingClientRect();
    const mx = evt.clientX - rect.left;
    const my = evt.clientY - rect.top;

    let found = null;
    NODES.forEach(n => {{
        const p = pos[n.name];
        const s = (tierSize[n.tier] || 6) + (connCount[n.name] || 0) * 1.5;
        const dx = p.x - mx, dy = p.y - my;
        if (dx*dx + dy*dy < (s+5)*(s+5)) found = n;
    }});

    if (found) {{
        const conns = EDGES.filter(e => e.from === found.name || e.to === found.name);
        let connHtml = conns.map(e => {{
            const other = e.from === found.name ? e.to : e.from;
            return '<div class="tt-conn">&rarr; ' + other + ': ' + e.reason + '</div>';
        }}).join('');

        let sinHtml = found.sins.map(s => {{
            const c = found.tier === 3 ? '#8a4a4a' : found.tier === 2 ? '#c47474' : '#d4a574';
            return '<span class="tt-sin" style="background:' + c + ';">' + s + '</span>';
        }}).join('');

        tooltip.querySelector('.tt-name').textContent = found.name;
        tooltip.querySelector('.tt-role').textContent = found.role + ' — ' + found.country;
        tooltip.querySelector('.tt-sins').innerHTML = sinHtml || '<span style="color:#555;">No sins matched</span>';
        tooltip.querySelector('.tt-connections').innerHTML = connHtml || '<div style="color:#555;">No mapped connections</div>';
        tooltip.style.display = 'block';
        tooltip.style.left = (evt.clientX + 16) + 'px';
        tooltip.style.top = (evt.clientY + 16) + 'px';
    }} else {{
        tooltip.style.display = 'none';
    }}
}});

canvas.addEventListener('mouseleave', () => {{ tooltip.style.display = 'none'; }});
</script>

</body>
</html>"""


if __name__ == "__main__":
    records = load_all_records()
    print(f"Loaded {len(records)} records")
    html = generate_network_page(records)
    with open("docs/network.html", "w") as f:
        f.write(html)
    print(f"Generated docs/network.html")
    print(f"Connections mapped: {len([c for c in CONNECTIONS if c[0] in {r['name'] for r in records} and c[1] in {r['name'] for r in records}])}")

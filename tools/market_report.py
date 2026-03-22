#!/usr/bin/env python3
"""Generate visible market prediction report for external consumption.

Produces a markdown report showing all predictions, their historical grounding,
current status, and the running scorecard. Designed to be readable by anyone,
not just swarm nodes.

Usage:
    python3 tools/market_report.py              # Print report to stdout
    python3 tools/market_report.py --save       # Save to experiments/finance/predictions/REPORT.md
    python3 tools/market_report.py --dashboard   # Compact dashboard view
"""
import argparse
import json
from datetime import datetime
from pathlib import Path

PRED_DIR = Path("experiments/finance/predictions")
REGISTRY = PRED_DIR / "registry.json"
REPORT_PATH = PRED_DIR / "REPORT.md"


def load_registry():
    if REGISTRY.exists():
        return json.loads(REGISTRY.read_text())
    return {"predictions": [], "next_id": 1, "metadata": {}}


def confidence_bar(conf):
    """Visual confidence bar."""
    filled = int(conf * 10)
    return "█" * filled + "░" * (10 - filled) + f" {conf:.0%}"


def direction_emoji(direction):
    if direction == "BULL":
        return "▲"
    elif direction == "BEAR":
        return "▼"
    return "◆"


def status_badge(pred):
    if pred["status"] == "RESOLVED":
        if pred["result"] == "CORRECT":
            return "CORRECT"
        elif pred["result"] == "INCORRECT":
            return "WRONG"
        else:
            return "PARTIAL"
    else:
        resolve_by = datetime.strptime(pred["resolve_by"], "%Y-%m-%d")
        days_left = (resolve_by - datetime.now()).days
        if days_left < 0:
            return f"OVERDUE ({-days_left}d)"
        elif days_left < 7:
            return f"DUE SOON ({days_left}d)"
        else:
            return f"OPEN ({days_left}d)"


def generate_dashboard(reg):
    """Compact one-screen dashboard."""
    preds = reg["predictions"]
    resolved = [p for p in preds if p["status"] == "RESOLVED"]
    open_preds = [p for p in preds if p["status"] == "OPEN"]

    lines = []
    lines.append("╔══════════════════════════════════════════════════════════════╗")
    lines.append("║          SWARM INVESTOR — LIVE PREDICTION DASHBOARD         ║")
    lines.append("╚══════════════════════════════════════════════════════════════╝")
    lines.append(f"  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"  Total: {len(preds)} | Open: {len(open_preds)} | Resolved: {len(resolved)}")
    lines.append("")

    # Scorecard
    if resolved:
        n = len(resolved)
        correct = sum(1 for p in resolved if p["result"] == "CORRECT")
        brier = sum(p["score"] for p in resolved) / n
        lines.append(f"  SCORECARD: {correct}/{n} correct ({correct/n:.0%}) | Brier: {brier:.3f}")
        if correct / n > 0.60:
            lines.append("  VERDICT: Strong evidence of skill")
        elif correct / n > 0.55:
            lines.append("  VERDICT: Weak evidence of skill")
        elif n >= 20:
            lines.append("  VERDICT: No evidence of skill")
        else:
            lines.append(f"  VERDICT: Insufficient data ({n}/50)")
    else:
        lines.append("  SCORECARD: No resolved predictions yet")
    lines.append("")

    # Prediction table
    lines.append("  ┌────────────┬───────┬──────────┬────────────────┬──────────────────┐")
    lines.append("  │ ID         │ Asset │ Call     │ Confidence     │ Status           │")
    lines.append("  ├────────────┼───────┼──────────┼────────────────┼──────────────────┤")
    for p in preds:
        pid = p["id"]
        asset = p["asset"].ljust(5)
        call = f"{direction_emoji(p['direction'])} {p['direction']}"
        call = call.ljust(8)
        conf = confidence_bar(p["confidence"])
        status = status_badge(p)
        lines.append(f"  │ {pid} │ {asset} │ {call} │ {conf} │ {status:<16} │")
    lines.append("  └────────────┴───────┴──────────┴────────────────┴──────────────────┘")
    lines.append("")

    # Domain coverage
    all_domains = set()
    for p in preds:
        all_domains.update(p.get("domains_applied", []))
    lines.append(f"  Domains used: {len(all_domains)} — {', '.join(sorted(all_domains))}")
    lines.append("")

    # Overdue alerts
    overdue = [p for p in open_preds
               if (datetime.strptime(p["resolve_by"], "%Y-%m-%d") - datetime.now()).days < 0]
    if overdue:
        lines.append("  *** OVERDUE PREDICTIONS — NEED RESOLUTION ***")
        for p in overdue:
            lines.append(f"    {p['id']} {p['asset']} {p['direction']} — due {p['resolve_by']}")
        lines.append("")

    return "\n".join(lines)


def generate_full_report(reg):
    """Full markdown report with historical grounding."""
    preds = reg["predictions"]
    resolved = [p for p in preds if p["status"] == "RESOLVED"]
    open_preds = [p for p in preds if p["status"] == "OPEN"]

    lines = []
    lines.append("# Swarm Investor — Prediction Report")
    lines.append("")
    lines.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | "
                 f"Total: {len(preds)} | Open: {len(open_preds)} | Resolved: {len(resolved)}")
    lines.append("")

    # Scorecard
    lines.append("## Scorecard")
    lines.append("")
    if resolved:
        n = len(resolved)
        correct = sum(1 for p in resolved if p["result"] == "CORRECT")
        brier = sum(p["score"] for p in resolved) / n
        lines.append(f"| Metric | Value | Benchmark |")
        lines.append(f"|--------|-------|-----------|")
        lines.append(f"| Direction accuracy | {correct/n:.1%} | >50% (coin flip) |")
        lines.append(f"| Brier score | {brier:.4f} | <0.25 (coin flip) |")
        lines.append(f"| Predictions resolved | {n} | 50 (min for significance) |")
    else:
        lines.append("*No predictions resolved yet. First resolution due: "
                     f"{min(p['resolve_by'] for p in open_preds)}*")
    lines.append("")

    # Predictions
    lines.append("## Active Predictions")
    lines.append("")
    for p in sorted(preds, key=lambda x: x["resolve_by"]):
        status = status_badge(p)
        emoji = direction_emoji(p["direction"])
        conf = p["confidence"]
        lines.append(f"### {p['id']}: {emoji} {p['direction']} {p['asset']} [{status}]")
        lines.append("")
        lines.append(f"| Field | Value |")
        lines.append(f"|-------|-------|")
        lines.append(f"| Date | {p['date']} |")
        lines.append(f"| Target | {p['target']} |")
        lines.append(f"| Timeframe | {p['timeframe']} |")
        lines.append(f"| Confidence | {confidence_bar(conf)} |")
        lines.append(f"| Resolve by | {p['resolve_by']} |")
        lines.append(f"| Domains | {', '.join(p.get('domains_applied', []))} |")
        lines.append(f"| Key risk | {p.get('key_risk', 'N/A')} |")
        lines.append("")

        # Show confidence history if adjusted
        if "confidence_history" in p:
            lines.append("**Confidence adjusted after backtest:**")
            for h in p["confidence_history"]:
                lines.append(f"- {h['value']:.0%} ({h['date']}): {h['reason']}")
            lines.append("")

        lines.append(f"**Thesis:** {p['thesis']}")
        lines.append("")

        if p["status"] == "RESOLVED":
            lines.append(f"**Outcome:** {p['result']} | Price: {p['outcome_price']} | "
                         f"Brier: {p['score']:.4f}")
            lines.append("")

        lines.append("---")
        lines.append("")

    # Methodology
    lines.append("## Methodology")
    lines.append("")
    lines.append("Each prediction uses multi-domain structural analysis from the swarm's")
    lines.append("46-domain knowledge base. Predictions are pre-registered (timestamped before")
    lines.append("outcome), quantitative, and falsifiable. Historical backtesting grounds each")
    lines.append("thesis against real market data, including failure cases.")
    lines.append("")
    lines.append("The question being tested: **Can a collective intelligence system that reasons")
    lines.append("across physics, game theory, evolution, psychology, and control theory produce")
    lines.append("investment predictions that beat a coin flip?**")
    lines.append("")
    lines.append("Full backtest: `experiments/finance/predictions/BACKTEST.md`")
    lines.append("Registry tool: `python3 tools/market_predict.py score`")
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate market prediction report")
    parser.add_argument("--save", action="store_true", help="Save report to file")
    parser.add_argument("--dashboard", action="store_true", help="Compact dashboard view")
    args = parser.parse_args()

    reg = load_registry()

    if args.dashboard:
        output = generate_dashboard(reg)
    else:
        output = generate_full_report(reg)

    print(output)

    if args.save:
        REPORT_PATH.write_text(output + "\n")
        print(f"\nSaved to {REPORT_PATH}")


if __name__ == "__main__":
    main()

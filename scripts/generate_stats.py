#!/usr/bin/env python3
"""
Generate statistics report for exocortex-public-ontologies.

Creates docs/stats.md with auto-updated statistics.

Usage:
    python scripts/generate_stats.py
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
DOCS_DIR = REPO_ROOT / "docs"


def get_stats() -> dict:
    """Run stats.py and return JSON output."""
    result = subprocess.run(
        ["python3", str(REPO_ROOT / "scripts" / "stats.py"), "--json"],
        capture_output=True,
        text=True,
        cwd=REPO_ROOT,
    )
    return json.loads(result.stdout)


def generate_markdown(stats: dict) -> str:
    """Generate markdown report from stats."""
    lines = [
        "---",
        "layout: default",
        "title: Statistics",
        "---",
        "",
        "# Ontology Statistics",
        "",
        f"*Auto-generated on {datetime.utcnow().strftime('%Y-%m-%d %H:%M')} UTC*",
        "",
        "## Overview",
        "",
        f"| Metric | Count |",
        f"|--------|-------|",
        f"| Total Files | **{stats['total_files']:,}** |",
        f"| Statements (triples) | {stats['by_type'].get('statement', 0):,} |",
        f"| Anchors (resources) | {stats['by_type'].get('anchor', 0):,} |",
        f"| Blank Nodes | {stats['by_type'].get('blank_node', 0):,} |",
        f"| Namespaces | {stats['by_type'].get('namespace', 0)} |",
        "",
        "## By Namespace",
        "",
        "| Namespace | Triples | Anchors | Blank Nodes | Total Files |",
        "|-----------|---------|---------|-------------|-------------|",
    ]

    # Sort by statement count descending
    namespaces = sorted(
        stats["by_namespace"].items(),
        key=lambda x: x[1].get("statements", 0),
        reverse=True,
    )

    for ns, data in namespaces:
        lines.append(
            f"| `{ns}` | {data.get('statements', 0):,} | "
            f"{data.get('anchors', 0)} | {data.get('blank_nodes', 0)} | "
            f"{data.get('files', 0):,} |"
        )

    # Top predicates
    if "top_predicates" in stats and stats["top_predicates"]:
        lines.extend(
            [
                "",
                "## Top Predicates",
                "",
                "| Predicate | Usage Count |",
                "|-----------|-------------|",
            ]
        )
        for item in stats["top_predicates"][:15]:
            alias = item.get("alias", item.get("uuid", "?"))
            count = item.get("count", 0)
            lines.append(f"| `{alias}` | {count:,} |")

    # External references summary
    if "external_references" in stats:
        ext = stats["external_references"]
        lines.extend(
            [
                "",
                "## External References",
                "",
                f"Total external wikilinks: **{ext.get('total', 0):,}**",
                "",
                "These are references to resources defined in other ontologies.",
            ]
        )

    lines.append("")
    return "\n".join(lines)


def main():
    """Generate stats.md documentation."""
    print("Generating statistics...")

    stats = get_stats()
    markdown = generate_markdown(stats)

    output_path = DOCS_DIR / "stats.md"
    output_path.write_text(markdown, encoding="utf-8")

    print(f"Generated {output_path}")
    print(f"  Total files: {stats['total_files']:,}")
    print(f"  Triples: {stats['by_type'].get('statement', 0):,}")
    print(f"  Namespaces: {len(stats['by_namespace'])}")


if __name__ == "__main__":
    main()

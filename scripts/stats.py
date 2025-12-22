#!/usr/bin/env python3
"""
Generate statistics for exocortex-public-ontologies.

Shows counts of files, triples, anchors, and predicates per namespace.

Usage:
    python scripts/stats.py [--json] [--markdown]
"""

import os
import sys
import json
import yaml
import re
from pathlib import Path
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional

# Repository root (relative to script location)
REPO_ROOT = Path(__file__).parent.parent
PREFIXES = ['rdf', 'rdfs', 'owl', 'dc', 'dcterms', 'dcam', 'skos', 'foaf', 'prov', 'time', 'geo', 'vcard', 'doap', 'sioc', 'xsd', 'dcat', 'org', 'schema']


@dataclass
class NamespaceStats:
    """Statistics for a single namespace."""
    prefix: str
    total_files: int = 0
    statements: int = 0
    anchors: int = 0
    blank_nodes: int = 0
    namespaces: int = 0
    predicates: Set[str] = field(default_factory=set)
    classes: Set[str] = field(default_factory=set)
    properties: Set[str] = field(default_factory=set)


def parse_frontmatter(filepath: Path) -> Optional[dict]:
    """Parse YAML frontmatter from a markdown file."""
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception:
        return None

    if not content.startswith('---'):
        return None

    end_match = re.search(r'\n---\s*\n', content[3:])
    if not end_match:
        end_match = re.search(r'\n---\s*$', content[3:])
        if not end_match:
            return None

    yaml_content = content[4:3 + end_match.start()]

    try:
        data = yaml.safe_load(yaml_content)
        return data if data else {}
    except yaml.YAMLError:
        return None


def extract_uri_local_name(uri_or_wikilink: str) -> Optional[str]:
    """Extract local name from URI or wikilink."""
    # Handle wikilinks like [[uuid|alias]] or [[uuid]]
    wikilink_match = re.match(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', uri_or_wikilink)
    if wikilink_match:
        return wikilink_match.group(1)

    # Handle URIs
    if '#' in uri_or_wikilink:
        return uri_or_wikilink.split('#')[-1]
    if '/' in uri_or_wikilink:
        return uri_or_wikilink.split('/')[-1]

    return uri_or_wikilink


def collect_namespace_stats(repo_root: Path, prefix: str) -> Optional[NamespaceStats]:
    """Collect statistics for a single namespace."""
    ns_dir = repo_root / prefix
    if not ns_dir.exists():
        return None

    stats = NamespaceStats(prefix=prefix)

    for filepath in ns_dir.glob('*.md'):
        stats.total_files += 1
        data = parse_frontmatter(filepath)
        if not data:
            continue

        metadata = data.get('metadata', '')

        if metadata == 'statement':
            stats.statements += 1
            # Track predicate
            predicate = data.get('predicate', '')
            if predicate:
                local_name = extract_uri_local_name(predicate)
                if local_name:
                    stats.predicates.add(local_name)
        elif metadata == 'anchor':
            stats.anchors += 1
        elif metadata == 'blank_node':
            stats.blank_nodes += 1
        elif metadata == 'namespace':
            stats.namespaces += 1

    return stats


def print_table(stats_list: List[NamespaceStats], output_format: str = 'text'):
    """Print statistics as table."""
    # Sort by total files descending
    sorted_stats = sorted(stats_list, key=lambda s: s.total_files, reverse=True)

    # Calculate totals
    total_files = sum(s.total_files for s in sorted_stats)
    total_statements = sum(s.statements for s in sorted_stats)
    total_anchors = sum(s.anchors for s in sorted_stats)
    total_blank_nodes = sum(s.blank_nodes for s in sorted_stats)
    total_predicates = len(set().union(*(s.predicates for s in sorted_stats)))

    if output_format == 'json':
        result = {
            'namespaces': [
                {
                    'prefix': s.prefix,
                    'files': s.total_files,
                    'statements': s.statements,
                    'anchors': s.anchors,
                    'blank_nodes': s.blank_nodes,
                    'unique_predicates': len(s.predicates)
                }
                for s in sorted_stats
            ],
            'totals': {
                'files': total_files,
                'statements': total_statements,
                'anchors': total_anchors,
                'blank_nodes': total_blank_nodes,
                'unique_predicates': total_predicates
            }
        }
        print(json.dumps(result, indent=2))
        return

    if output_format == 'markdown':
        print("| Namespace | Files | Statements | Anchors | Blank Nodes | Predicates |")
        print("|-----------|------:|----------:|--------:|------------:|-----------:|")
        for s in sorted_stats:
            print(f"| {s.prefix} | {s.total_files:,} | {s.statements:,} | {s.anchors:,} | {s.blank_nodes} | {len(s.predicates)} |")
        print(f"| **Total** | **{total_files:,}** | **{total_statements:,}** | **{total_anchors:,}** | **{total_blank_nodes}** | **{total_predicates}** |")
        return

    # Default: text format
    print("=" * 80)
    print("ONTOLOGY STATISTICS")
    print("=" * 80)
    print()
    print(f"{'Namespace':<12} {'Files':>10} {'Statements':>12} {'Anchors':>10} {'BlankNodes':>12} {'Predicates':>12}")
    print("-" * 80)

    for s in sorted_stats:
        print(f"{s.prefix:<12} {s.total_files:>10,} {s.statements:>12,} {s.anchors:>10,} {s.blank_nodes:>12} {len(s.predicates):>12}")

    print("-" * 80)
    print(f"{'TOTAL':<12} {total_files:>10,} {total_statements:>12,} {total_anchors:>10,} {total_blank_nodes:>12} {total_predicates:>12}")
    print("=" * 80)


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Generate ontology statistics')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    parser.add_argument('--markdown', action='store_true', help='Output as Markdown table')
    parser.add_argument('namespaces', nargs='*', help='Specific namespaces (default: all)')
    args = parser.parse_args()

    namespaces_to_check = args.namespaces if args.namespaces else PREFIXES

    stats_list = []
    for prefix in namespaces_to_check:
        stats = collect_namespace_stats(REPO_ROOT, prefix)
        if stats:
            stats_list.append(stats)

    output_format = 'text'
    if args.json:
        output_format = 'json'
    elif args.markdown:
        output_format = 'markdown'

    print_table(stats_list, output_format)


if __name__ == '__main__':
    main()

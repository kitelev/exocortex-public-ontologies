#!/usr/bin/env python3
"""
Generate statistics for exocortex-public-ontologies.

Displays:
- Total file counts by type
- Per-namespace breakdown
- Top predicates used
- External reference analysis

Usage:
    python scripts/stats.py [--json]
"""

import argparse
import json
import re
import yaml
from pathlib import Path
from collections import Counter, defaultdict
from typing import Dict, List, Set, Tuple

# Repository root (relative to script location)
REPO_ROOT = Path(__file__).parent.parent

# Namespace prefixes
PREFIXES = ['rdf', 'rdfs', 'owl', 'dc', 'dcterms', 'dcam', 'skos', 'foaf', 'prov', 'time', 'geo', 'vcard', 'doap', 'sioc', 'xsd', 'dcat', 'org', 'schema', 'vs']


def parse_frontmatter(filepath: Path) -> dict:
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


def extract_wikilinks(data: dict) -> Set[str]:
    """Extract all wikilink targets from frontmatter values."""
    links = set()
    wikilink_pattern = re.compile(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]')

    for key, value in data.items():
        if isinstance(value, str):
            for match in wikilink_pattern.finditer(value):
                links.add(match.group(1))

    return links


def collect_stats(repo_root: Path) -> dict:
    """Collect all statistics from the repository."""
    stats = {
        'total_files': 0,
        'by_type': Counter(),
        'by_namespace': defaultdict(lambda: {'files': 0, 'anchors': 0, 'statements': 0, 'namespaces': 0, 'blank_nodes': 0}),
        'predicates': Counter(),
        'all_anchors': set(),
        'referenced_anchors': set(),
        'external_refs': Counter(),
    }

    # Collect all anchors first
    for ns in PREFIXES:
        ns_dir = repo_root / ns
        if not ns_dir.exists():
            continue

        for filepath in ns_dir.glob('*.md'):
            data = parse_frontmatter(filepath)
            if data and data.get('metadata') in ('anchor', 'namespace', 'blank_node'):
                stats['all_anchors'].add(filepath.stem)

    # Process all files
    for ns in PREFIXES:
        ns_dir = repo_root / ns
        if not ns_dir.exists():
            continue

        for filepath in ns_dir.glob('*.md'):
            data = parse_frontmatter(filepath)
            if not data:
                continue

            stats['total_files'] += 1
            metadata = data.get('metadata', 'unknown')
            stats['by_type'][metadata] += 1
            stats['by_namespace'][ns]['files'] += 1

            if metadata == 'anchor':
                stats['by_namespace'][ns]['anchors'] += 1
            elif metadata == 'namespace':
                stats['by_namespace'][ns]['namespaces'] += 1
            elif metadata == 'blank_node':
                stats['by_namespace'][ns]['blank_nodes'] += 1
            elif metadata == 'statement':
                stats['by_namespace'][ns]['statements'] += 1

                # Count predicate usage
                predicate = data.get('predicate', '')
                pred_match = re.search(r'\[\[([^\]|]+)', predicate)
                if pred_match:
                    pred_uuid = pred_match.group(1)
                    stats['predicates'][pred_uuid] += 1

                # Track referenced anchors
                wikilinks = extract_wikilinks(data)
                for link in wikilinks:
                    if link in stats['all_anchors']:
                        stats['referenced_anchors'].add(link)
                    else:
                        stats['external_refs'][link] += 1

    return stats


def get_alias_for_uuid(uuid: str, repo_root: Path) -> str:
    """Try to find the alias for a given UUID."""
    for ns in PREFIXES:
        filepath = repo_root / ns / f"{uuid}.md"
        if filepath.exists():
            data = parse_frontmatter(filepath)
            if data and 'aliases' in data and data['aliases']:
                return data['aliases'][0]
    return uuid[:8] + '...'


def print_stats(stats: dict, repo_root: Path, as_json: bool = False):
    """Print statistics in human-readable or JSON format."""
    if as_json:
        # Convert sets and counters to JSON-serializable format
        output = {
            'total_files': stats['total_files'],
            'by_type': dict(stats['by_type']),
            'by_namespace': {k: dict(v) for k, v in stats['by_namespace'].items()},
            'top_predicates': [
                {'uuid': uuid, 'count': count, 'alias': get_alias_for_uuid(uuid, repo_root)}
                for uuid, count in stats['predicates'].most_common(20)
            ],
            'external_refs_count': len(stats['external_refs']),
            'external_refs_total': sum(stats['external_refs'].values()),
        }
        print(json.dumps(output, indent=2))
        return

    print("=" * 60)
    print("EXOCORTEX PUBLIC ONTOLOGIES - STATISTICS")
    print("=" * 60)
    print()

    # Overview
    print("OVERVIEW")
    print("-" * 40)
    print(f"  Total namespaces:    {len(stats['by_namespace'])}")
    print(f"  Total files:         {stats['total_files']:,}")
    print(f"  Total anchors:       {len(stats['all_anchors']):,}")
    print(f"  Total statements:    {stats['by_type'].get('statement', 0):,}")
    print(f"  External refs:       {sum(stats['external_refs'].values()):,} ({len(stats['external_refs']):,} unique)")
    print()

    # By type
    print("FILES BY TYPE")
    print("-" * 40)
    for metadata_type, count in sorted(stats['by_type'].items(), key=lambda x: -x[1]):
        pct = count / stats['total_files'] * 100
        print(f"  {metadata_type:15} {count:>6,} ({pct:5.1f}%)")
    print()

    # By namespace
    print("FILES BY NAMESPACE")
    print("-" * 40)
    print(f"  {'Namespace':<10} {'Files':>8} {'Anchors':>8} {'Stmts':>8} {'BNodes':>8}")
    print(f"  {'-'*10} {'-'*8} {'-'*8} {'-'*8} {'-'*8}")
    for ns in sorted(stats['by_namespace'].keys(), key=lambda x: -stats['by_namespace'][x]['files']):
        ns_stats = stats['by_namespace'][ns]
        print(f"  {ns:<10} {ns_stats['files']:>8,} {ns_stats['anchors']:>8,} {ns_stats['statements']:>8,} {ns_stats['blank_nodes']:>8,}")
    print()

    # Top predicates
    print("TOP 15 PREDICATES")
    print("-" * 40)
    for uuid, count in stats['predicates'].most_common(15):
        alias = get_alias_for_uuid(uuid, repo_root)
        pct = count / stats['by_type'].get('statement', 1) * 100
        print(f"  {alias:35} {count:>6,} ({pct:5.1f}%)")
    print()

    # External refs
    print("TOP 10 EXTERNAL REFERENCES")
    print("-" * 40)
    for uuid, count in stats['external_refs'].most_common(10):
        print(f"  {uuid}  {count:>5,} refs")
    print()


def main():
    parser = argparse.ArgumentParser(description='Generate ontology statistics')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    args = parser.parse_args()

    stats = collect_stats(REPO_ROOT)
    print_stats(stats, REPO_ROOT, args.json)


if __name__ == '__main__':
    main()

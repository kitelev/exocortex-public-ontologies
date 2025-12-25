#!/usr/bin/env python3
"""
Generate cross-reference matrix for ontologies.

Shows which ontologies reference which other ontologies.

Usage:
    python scripts/generate_crossref.py [--output docs/cross-references.md]
"""

import argparse
import re
import yaml
from collections import defaultdict
from pathlib import Path
from typing import Dict, Optional, Set

from common import get_prefix_dirs, get_repo_root

# Repository root
REPO_ROOT = get_repo_root()

# Namespace prefixes loaded from _prefixes.yaml
PREFIXES = get_prefix_dirs()


def parse_frontmatter_fast(filepath: Path) -> Optional[dict]:
    """Parse YAML frontmatter from a markdown file (optimized)."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            first_line = f.readline()
            if not first_line.startswith('---'):
                return None

            lines = [first_line]
            for line in f:
                lines.append(line)
                if line.strip() == '---':
                    break

            yaml_content = ''.join(lines[1:-1])
            return yaml.safe_load(yaml_content) or {}
    except Exception:
        return None


def extract_wikilink_uuids(text: str) -> Set[str]:
    """Extract all UUIDs from wikilinks in text."""
    return set(re.findall(r'\[\[([a-f0-9-]{36})(?:\|[^\]]+)?\]\]', text))


def collect_uuid_to_namespace(repo_root: Path) -> Dict[str, str]:
    """Build mapping from UUID to namespace prefix."""
    uuid_to_ns = {}

    for prefix in PREFIXES:
        ns_dir = repo_root / prefix
        if not ns_dir.exists():
            continue

        for filepath in ns_dir.glob("*.md"):
            uuid = filepath.stem
            uuid_to_ns[uuid] = prefix

    return uuid_to_ns


def collect_references(repo_root: Path) -> Dict[str, Dict[str, int]]:
    """Collect cross-references between namespaces."""
    # First build UUID to namespace mapping
    uuid_to_ns = collect_uuid_to_namespace(repo_root)

    # Now collect references: source_ns -> target_ns -> count
    refs = defaultdict(lambda: defaultdict(int))

    for prefix in PREFIXES:
        ns_dir = repo_root / prefix
        if not ns_dir.exists():
            continue

        for filepath in ns_dir.glob("*.md"):
            fm = parse_frontmatter_fast(filepath)
            if not fm or fm.get("metadata") != "statement":
                continue

            # Get all UUIDs referenced in statement
            subject = fm.get("subject", "")
            predicate = fm.get("predicate", "")
            obj = fm.get("object", "")

            for field in [subject, predicate, obj]:
                if not field:
                    continue
                for uuid in extract_wikilink_uuids(field):
                    target_ns = uuid_to_ns.get(uuid)
                    if target_ns and target_ns != prefix:
                        refs[prefix][target_ns] += 1

    return refs


def generate_matrix_markdown(refs: Dict[str, Dict[str, int]]) -> str:
    """Generate markdown table showing cross-references."""
    lines = []

    lines.append("# Ontology Cross-Reference Matrix")
    lines.append("")
    lines.append("This matrix shows how ontologies reference each other.")
    lines.append("Numbers indicate count of statements referencing the target namespace.")
    lines.append("")
    lines.append("*Generated automatically.*")
    lines.append("")

    # Get all namespaces that are either sources or targets
    all_ns = set(refs.keys())
    for targets in refs.values():
        all_ns.update(targets.keys())

    # Filter to only existing namespaces
    existing_ns = sorted([ns for ns in all_ns if (REPO_ROOT / ns).exists()])

    # Generate table
    lines.append("## Reference Matrix")
    lines.append("")
    lines.append("Rows = source ontology, Columns = target ontology")
    lines.append("")

    # Header
    header = "| Source ↓ / Target → |"
    separator = "|-----|"
    for ns in existing_ns:
        header += f" {ns} |"
        separator += "-----|"
    lines.append(header)
    lines.append(separator)

    # Rows
    for source in existing_ns:
        row = f"| **{source}** |"
        for target in existing_ns:
            if source == target:
                row += " - |"
            else:
                count = refs.get(source, {}).get(target, 0)
                if count > 0:
                    row += f" {count} |"
                else:
                    row += " |"
        lines.append(row)

    lines.append("")

    # Summary statistics
    lines.append("## Summary Statistics")
    lines.append("")

    # Most referenced
    target_counts = defaultdict(int)
    for targets in refs.values():
        for target, count in targets.items():
            target_counts[target] += count

    lines.append("### Most Referenced Ontologies")
    lines.append("")
    lines.append("| Ontology | Total References |")
    lines.append("|----------|-----------------|")
    for ns, count in sorted(target_counts.items(), key=lambda x: -x[1])[:10]:
        lines.append(f"| {ns} | {count} |")
    lines.append("")

    # Most referencing
    source_counts = {ns: sum(targets.values()) for ns, targets in refs.items()}

    lines.append("### Most Referencing Ontologies")
    lines.append("")
    lines.append("| Ontology | References to Others |")
    lines.append("|----------|---------------------|")
    for ns, count in sorted(source_counts.items(), key=lambda x: -x[1])[:10]:
        lines.append(f"| {ns} | {count} |")
    lines.append("")

    # Dependency graph (text format)
    lines.append("## Dependency Relationships")
    lines.append("")
    lines.append("Key dependencies (>100 references):")
    lines.append("")

    for source in sorted(refs.keys()):
        targets = refs[source]
        major_deps = [(t, c) for t, c in targets.items() if c > 100]
        if major_deps:
            deps_str = ", ".join([f"{t} ({c})" for t, c in sorted(major_deps, key=lambda x: -x[1])])
            lines.append(f"- **{source}** → {deps_str}")

    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate cross-reference matrix")
    parser.add_argument("-o", "--output", type=str, default="docs/cross-references.md",
                        help="Output file path")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Verbose output")
    args = parser.parse_args()

    print("Collecting cross-references...")
    refs = collect_references(REPO_ROOT)

    total_refs = sum(sum(targets.values()) for targets in refs.values())
    print(f"  Found {total_refs} cross-references")
    print(f"  Between {len(refs)} source namespaces")

    print("Generating documentation...")
    markdown = generate_matrix_markdown(refs)

    output_path = REPO_ROOT / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(markdown, encoding="utf-8")
    print(f"Written to {args.output}")

    if args.verbose:
        print("\nPreview:")
        print("=" * 60)
        print(markdown[:2000])
        if len(markdown) > 2000:
            print("...")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Generate missing rdfs:label statement files for ontology anchors.
"""

from pathlib import Path
from typing import Set

REPO_ROOT = Path(__file__).parent.parent

# Labels derived from anchor names (converting camelCase/snake_case to readable)
def anchor_to_label(anchor: str) -> str:
    """Convert anchor name to human-readable label."""
    # Remove namespace prefix (e.g., "owl__" -> "")
    if '__' in anchor:
        local_name = anchor.split('__', 1)[1]
    else:
        local_name = anchor

    # Handle camelCase: insert space before uppercase letters
    result = ''
    for i, char in enumerate(local_name):
        if char.isupper() and i > 0 and not local_name[i-1].isupper():
            result += ' '
        result += char

    # Handle snake_case: replace underscores with spaces
    result = result.replace('_', ' ')

    # Handle hyphenated words
    result = result.replace('-', ' ')

    # Capitalize first letter
    if result:
        result = result[0].upper() + result[1:]

    return result


def get_anchors(ns_dir: Path) -> Set[str]:
    """Get all anchor names in this namespace."""
    anchors = set()
    for f in ns_dir.glob('*.md'):
        name = f.stem
        if ' ' not in name and not name.startswith('!'):
            anchors.add(name)
    return anchors


def get_existing_labels(ns_dir: Path) -> Set[str]:
    """Get anchors that already have rdfs:label statements."""
    existing = set()
    for f in ns_dir.glob('* rdfs__label ___.md'):
        name = f.stem.split(' ')[0]
        existing.add(name)
    return existing


def create_label_file(ns_dir: Path, anchor: str, label: str):
    """Create rdfs:label statement file for an anchor."""
    filename = f"{anchor} rdfs__label ___.md"
    filepath = ns_dir / filename

    content = f"""---
metadata: statement
rdf__subject: "[[{anchor}]]"
rdf__predicate: "[[rdfs__label]]"
rdf__object: "{label}"
---
"""
    filepath.write_text(content)
    print(f"  Created: {filename}")


def generate_missing_labels(ns: str, dry_run: bool = True):
    """Generate missing rdfs:label statements for a namespace."""
    ns_dir = REPO_ROOT / ns
    if not ns_dir.exists():
        print(f"  Namespace not found: {ns}")
        return

    anchors = get_anchors(ns_dir)
    existing = get_existing_labels(ns_dir)
    missing = anchors - existing

    if not missing:
        print(f"  All anchors have labels")
        return

    print(f"  Missing labels for {len(missing)} anchors")

    for anchor in sorted(missing):
        label = anchor_to_label(anchor)
        if dry_run:
            print(f"    Would create: {anchor} rdfs__label ___.md ({label})")
        else:
            create_label_file(ns_dir, anchor, label)


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Generate missing rdfs:label statements')
    parser.add_argument('--namespace', '-n', help='Process only this namespace')
    parser.add_argument('--apply', action='store_true', help='Actually create files (default is dry run)')
    args = parser.parse_args()

    namespaces = [args.namespace] if args.namespace else ['owl', 'skos', 'prov', 'time', 'vcard', 'doap', 'sioc', 'xsd']

    print("=" * 60)
    print("Generating Missing rdfs:label Statements")
    print("=" * 60)
    print()

    if not args.apply:
        print("DRY RUN - use --apply to create files")
        print()

    for ns in namespaces:
        print(f"\n{ns.upper()}:")
        generate_missing_labels(ns, dry_run=not args.apply)


if __name__ == '__main__':
    main()

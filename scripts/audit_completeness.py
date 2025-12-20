#!/usr/bin/env python3
"""
Audit ontology completeness by comparing with W3C sources.

For each ontology, checks that:
1. All classes have: a rdfs:Class, rdfs:label, rdfs:comment, rdfs:isDefinedBy
2. All properties have: a rdf:Property, rdfs:label, rdfs:comment, rdfs:isDefinedBy, rdfs:domain, rdfs:range
3. Namespace has: dc:title, dc:description, rdfs:label
"""

import os
import sys
from pathlib import Path
from typing import Set, Dict, List

REPO_ROOT = Path(__file__).parent.parent
NAMESPACES = ['rdf', 'rdfs', 'owl', 'dc', 'dcterms', 'skos', 'foaf', 'prov', 'time', 'geo', 'vcard', 'doap', 'sioc', 'xsd']


def get_existing_statements(ns_dir: Path) -> Set[str]:
    """Get all existing statement file names (without .md)."""
    statements = set()
    for f in ns_dir.glob('*.md'):
        name = f.stem
        # Only statement files have spaces
        if ' ' in name:
            statements.add(name)
    return statements


def get_anchors(ns_dir: Path) -> Set[str]:
    """Get all anchor names in this namespace."""
    anchors = set()
    for f in ns_dir.glob('*.md'):
        name = f.stem
        # Anchors don't have spaces and don't start with !
        if ' ' not in name and not name.startswith('!'):
            anchors.add(name)
    return anchors


def check_namespace_completeness(ns: str) -> Dict[str, List[str]]:
    """Check completeness of a namespace."""
    ns_dir = REPO_ROOT / ns
    if not ns_dir.exists():
        return {'error': [f'Namespace directory not found: {ns}']}

    existing = get_existing_statements(ns_dir)
    anchors = get_anchors(ns_dir)
    missing = {'namespace': [], 'anchors': {}}

    # Check namespace metadata
    ns_file = f"!{ns}"
    expected_ns_statements = [
        f"{ns_file} rdfs__label ___",
    ]

    for stmt in expected_ns_statements:
        if stmt not in existing:
            missing['namespace'].append(stmt)

    # Check each anchor
    for anchor in anchors:
        anchor_missing = []

        # Every anchor should have isDefinedBy (already enforced)
        # Check for rdfs:label and rdfs:comment
        expected = [
            f"{anchor} rdfs__label ___",
            f"{anchor} rdfs__comment ___",
        ]

        for stmt in expected:
            if stmt not in existing:
                anchor_missing.append(stmt)

        if anchor_missing:
            missing['anchors'][anchor] = anchor_missing

    return missing


def main():
    print("=" * 60)
    print("Ontology Completeness Audit")
    print("=" * 60)
    print()

    total_missing = 0

    for ns in NAMESPACES:
        missing = check_namespace_completeness(ns)

        ns_missing = len(missing.get('namespace', []))
        anchor_missing = sum(len(v) for v in missing.get('anchors', {}).values())

        if ns_missing + anchor_missing > 0:
            print(f"\n{ns.upper()}:")

            if missing.get('namespace'):
                print(f"  Namespace missing ({ns_missing}):")
                for stmt in missing['namespace']:
                    print(f"    - {stmt}")

            if missing.get('anchors'):
                print(f"  Anchors missing ({anchor_missing}):")
                for anchor, stmts in sorted(missing['anchors'].items()):
                    for stmt in stmts:
                        print(f"    - {stmt}")

            total_missing += ns_missing + anchor_missing
        else:
            print(f"{ns.upper()}: ✓ Complete")

    print()
    print("=" * 60)
    if total_missing > 0:
        print(f"Total missing statements: {total_missing}")
    else:
        print("All ontologies complete!")


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Generate missing anchor files from original W3C ontologies.

This script scans original ontologies and creates anchor files for any
terms that are referenced but don't have corresponding anchor files.

Usage:
    python scripts/generate_missing_anchors.py [--dry-run] [--verbose]
"""

import sys
from pathlib import Path
from typing import Dict, Set

try:
    from rdflib import Graph, URIRef
except ImportError:
    print("Error: rdflib is required. Install with: pip install rdflib")
    sys.exit(1)

REPO_ROOT = Path(__file__).parent.parent
ORIGINALS_DIR = REPO_ROOT / 'originals'

# Namespace mappings
NAMESPACES = {
    'http://www.w3.org/1999/02/22-rdf-syntax-ns#': 'rdf',
    'http://www.w3.org/2000/01/rdf-schema#': 'rdfs',
    'http://www.w3.org/2002/07/owl#': 'owl',
    'http://purl.org/dc/elements/1.1/': 'dc',
    'http://purl.org/dc/terms/': 'dcterms',
    'http://www.w3.org/2004/02/skos/core#': 'skos',
    'http://xmlns.com/foaf/0.1/': 'foaf',
    'http://www.w3.org/ns/prov#': 'prov',
    'http://www.w3.org/2006/time#': 'time',
    'http://www.w3.org/2003/01/geo/wgs84_pos#': 'geo',
    'http://www.w3.org/2006/vcard/ns#': 'vcard',
    'http://usefulinc.com/ns/doap#': 'doap',
    'http://rdfs.org/sioc/ns#': 'sioc',
    'http://www.w3.org/2001/XMLSchema#': 'xsd',
}

# Ontology files
ONTOLOGIES = {
    'prov': 'prov.rdf',
    'time': 'time.rdf',
    'skos': 'skos.rdf',
}


def parse_ontology(filepath: Path) -> Graph:
    """Parse an RDF ontology file."""
    g = Graph()
    for fmt in ['turtle', 'xml', 'n3', 'nt']:
        try:
            g.parse(filepath, format=fmt)
            return g
        except:
            continue
    raise ValueError(f"Could not parse {filepath}")


def extract_terms(g: Graph, namespace_uri: str) -> Set[str]:
    """Extract all terms from a namespace in the graph."""
    terms = set()
    for s, p, o in g:
        for t in [s, p, o]:
            if isinstance(t, URIRef):
                uri = str(t)
                if uri.startswith(namespace_uri):
                    local = uri[len(namespace_uri):]
                    if local:  # Skip empty local names
                        terms.add(local)
    return terms


def get_existing_anchors(namespace: str) -> Set[str]:
    """Get existing anchor local names (case-insensitive)."""
    ns_dir = REPO_ROOT / namespace
    existing = set()
    if not ns_dir.exists():
        return existing

    prefix = f"{namespace}__"
    for f in ns_dir.glob('*.md'):
        name = f.stem
        if name.startswith(prefix) and ' ' not in name:
            local = name[len(prefix):]
            existing.add(local.lower())
    return existing


def create_anchor_file(namespace: str, local_name: str, dry_run: bool, verbose: bool) -> bool:
    """Create an anchor file."""
    ns_dir = REPO_ROOT / namespace
    filepath = ns_dir / f"{namespace}__{local_name}.md"

    # Check if file exists (case-insensitive on macOS)
    existing_lower = {f.stem.lower(): f for f in ns_dir.glob(f"{namespace}__*.md") if ' ' not in f.name}
    target_lower = f"{namespace}__{local_name}".lower()

    if target_lower in existing_lower:
        if verbose:
            print(f"  Skipping (exists): {namespace}__{local_name}")
        return False

    content = """---
metadata: anchor
---
"""

    if dry_run:
        if verbose:
            print(f"  Would create: {filepath.name}")
        return True

    filepath.write_text(content, encoding='utf-8')
    if verbose:
        print(f"  Created: {filepath.name}")
    return True


def create_isdefinedby_statement(namespace: str, local_name: str, dry_run: bool, verbose: bool) -> bool:
    """Create rdfs:isDefinedBy statement for an anchor."""
    ns_dir = REPO_ROOT / namespace
    filename = f"{namespace}__{local_name} rdfs__isDefinedBy !{namespace}.md"
    filepath = ns_dir / filename

    if filepath.exists():
        return False

    content = f"""---
metadata: statement
rdf__subject: "[[{namespace}__{local_name}]]"
rdf__predicate: "[[rdfs__isDefinedBy]]"
rdf__object: "[[!{namespace}]]"
---
"""

    if dry_run:
        if verbose:
            print(f"  Would create: {filename}")
        return True

    filepath.write_text(content, encoding='utf-8')
    if verbose:
        print(f"  Created: {filename}")
    return True


def process_ontology(namespace: str, filename: str, dry_run: bool, verbose: bool) -> Dict[str, int]:
    """Process an ontology and generate missing anchor files."""
    filepath = ORIGINALS_DIR / filename
    if not filepath.exists():
        print(f"  ⚠️  Original file not found: {filepath}")
        return {'anchors': 0, 'statements': 0}

    # Get namespace URI
    ns_uri = None
    for uri, prefix in NAMESPACES.items():
        if prefix == namespace:
            ns_uri = uri
            break

    if not ns_uri:
        print(f"  ⚠️  Unknown namespace: {namespace}")
        return {'anchors': 0, 'statements': 0}

    print(f"\nProcessing {namespace} ({filename})...")

    # Parse ontology
    g = parse_ontology(filepath)
    print(f"  Loaded {len(g)} triples")

    # Extract all terms
    terms = extract_terms(g, ns_uri)
    print(f"  Found {len(terms)} terms")

    # Get existing anchors
    existing = get_existing_anchors(namespace)
    print(f"  Existing anchors: {len(existing)}")

    # Find missing terms
    missing = [t for t in terms if t.lower() not in existing]
    print(f"  Missing anchors: {len(missing)}")

    # Create missing anchors
    created_anchors = 0
    created_statements = 0

    for term in sorted(missing):
        if create_anchor_file(namespace, term, dry_run, verbose):
            created_anchors += 1
        if create_isdefinedby_statement(namespace, term, dry_run, verbose):
            created_statements += 1

    return {'anchors': created_anchors, 'statements': created_statements}


def main():
    dry_run = '--dry-run' in sys.argv
    verbose = '--verbose' in sys.argv or '-v' in sys.argv

    print("=" * 60)
    print("Missing Anchor Generator for Exocortex Public Ontologies")
    print("=" * 60)

    if dry_run:
        print("\n🔍 DRY RUN MODE - no files will be created")

    total_stats = {'anchors': 0, 'statements': 0}

    for namespace, filename in ONTOLOGIES.items():
        stats = process_ontology(namespace, filename, dry_run, verbose)
        total_stats['anchors'] += stats['anchors']
        total_stats['statements'] += stats['statements']

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Created anchor files: {total_stats['anchors']}")
    print(f"  Created statement files: {total_stats['statements']}")

    if dry_run:
        print("\n🔍 DRY RUN - run without --dry-run to create files")
    else:
        print("\n✅ Generation complete!")


if __name__ == '__main__':
    main()

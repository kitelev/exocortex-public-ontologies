#!/usr/bin/env python3
"""
Generate blank node files from original W3C ontologies.

This script:
1. Parses original RDF ontologies (TIME, PROV, SKOS)
2. Identifies all blank nodes and their associated triples
3. Generates short UUIDs for each blank node
4. Creates blank node anchor files ({namespace}!{uuid}.md)
5. Creates statement files for each triple involving blank nodes

Usage:
    python scripts/generate_blank_nodes.py [--dry-run] [--verbose]
"""

import os
import sys
import uuid
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple
from collections import defaultdict

try:
    from rdflib import Graph, BNode, RDF, RDFS, OWL, Namespace, URIRef, Literal
    from rdflib.namespace import XSD, DC, DCTERMS, SKOS as SKOS_NS
except ImportError:
    print("Error: rdflib is required. Install with: pip install rdflib")
    sys.exit(1)

# Repository root
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

# Ontologies that have blank nodes
ONTOLOGIES_WITH_BLANK_NODES = {
    'time': 'time.rdf',
    'prov': 'prov.rdf',
    'skos': 'skos.rdf',
}


def generate_short_uuid() -> str:
    """Generate an 8-character UUID (first 8 chars of UUID4)."""
    return uuid.uuid4().hex[:8]


def uri_to_prefix_local(uri: str) -> Tuple[str, str]:
    """Convert a URI to prefix:localname format."""
    for ns_uri, prefix in NAMESPACES.items():
        if uri.startswith(ns_uri):
            local = uri[len(ns_uri):]
            return prefix, local
    # Unknown namespace - return as-is
    if '#' in uri:
        ns, local = uri.rsplit('#', 1)
        return ns + '#', local
    elif '/' in uri:
        ns, local = uri.rsplit('/', 1)
        return ns + '/', local
    return '', uri


def term_to_filename(term, blank_node_map: Dict[str, str], namespace: str) -> str:
    """
    Convert an RDF term to filename format.

    - URI: prefix__localname
    - Blank node: namespace!uuid
    - Literal: ___ (placeholder)
    - External URI: ___ (treated as literal since we can't link to them)
    """
    if isinstance(term, BNode):
        bn_id = str(term)
        if bn_id in blank_node_map:
            return blank_node_map[bn_id]
        else:
            # Unknown blank node - this shouldn't happen if we process correctly
            return f"_unknown_{bn_id}"

    elif isinstance(term, URIRef):
        uri = str(term)
        # Check if it matches one of our namespaces
        for ns_uri, ns_prefix in NAMESPACES.items():
            if uri.startswith(ns_uri):
                local = uri[len(ns_uri):]
                return f"{ns_prefix}__{local}"
        # External URI - treat as literal (we store the URI as the object value)
        return '___'

    elif isinstance(term, Literal):
        return '___'

    return str(term)


def escape_for_yaml(value: str) -> str:
    """Escape a string value for YAML frontmatter."""
    # Use single quotes for values that contain special chars
    # to avoid YAML escape sequence interpretation
    if '\\' in value or '+' in value or '|' in value or '[' in value or ']' in value or ':' in value:
        # Use single quotes - but need to escape single quotes inside
        if "'" in value:
            escaped = value.replace("'", "''")  # YAML escapes ' as ''
            return f"'{escaped}'"
        return f"'{value}'"
    # Handle multiline or double quotes
    if '\n' in value or '"' in value:
        if "'" not in value:
            return f"'{value}'"
        else:
            escaped = value.replace('"', '\\"')
            return f'"{escaped}"'
    return f'"{value}"'


def term_to_wikilink(term, blank_node_map: Dict[str, str], namespace: str) -> str:
    """
    Convert an RDF term to wikilink format for frontmatter.

    - URI: "[[prefix__localname]]"
    - Blank node: "[[namespace!uuid]]"
    - Literal: 'literal value' (with proper escaping)
    - External URI: '<uri>' as literal
    """
    if isinstance(term, BNode):
        bn_id = str(term)
        if bn_id in blank_node_map:
            return f'"[[{blank_node_map[bn_id]}]]"'
        else:
            return f'"[[_unknown_{bn_id}]]"'

    elif isinstance(term, URIRef):
        uri = str(term)
        for ns_uri, ns_prefix in NAMESPACES.items():
            if uri.startswith(ns_uri):
                local = uri[len(ns_uri):]
                return f'"[[{ns_prefix}__{local}]]"'
        # External URI - treat as literal value
        return escape_for_yaml(f"<{uri}>")

    elif isinstance(term, Literal):
        value = str(term)
        return escape_for_yaml(value)

    return escape_for_yaml(str(term))


def predicate_to_filename(predicate: URIRef) -> str:
    """Convert predicate URI to filename format."""
    uri = str(predicate)

    # Special case: rdf:type -> 'a'
    if uri == str(RDF.type):
        return 'a'

    for ns_uri, ns_prefix in NAMESPACES.items():
        if uri.startswith(ns_uri):
            local = uri[len(ns_uri):]
            return f"{ns_prefix}__{local}"

    return uri.replace('/', '_').replace('#', '__').replace(':', '_')


def parse_ontology(filepath: Path) -> Graph:
    """Parse an RDF ontology file."""
    g = Graph()

    # Try different formats
    for fmt in ['xml', 'turtle', 'n3', 'nt']:
        try:
            g.parse(filepath, format=fmt)
            return g
        except:
            continue

    raise ValueError(f"Could not parse {filepath}")


def find_blank_nodes(g: Graph) -> Set[str]:
    """Find all blank nodes in the graph."""
    blank_nodes = set()
    for s, p, o in g:
        if isinstance(s, BNode):
            blank_nodes.add(str(s))
        if isinstance(o, BNode):
            blank_nodes.add(str(o))
    return blank_nodes


def create_blank_node_map(blank_nodes: Set[str], namespace: str) -> Dict[str, str]:
    """Create a mapping from blank node IDs to our naming format."""
    return {bn: f"{namespace}!{generate_short_uuid()}" for bn in blank_nodes}


def create_blank_node_file(name: str, namespace: str, output_dir: Path, dry_run: bool, verbose: bool) -> None:
    """Create a blank node anchor file."""
    filepath = output_dir / f"{name}.md"
    content = f"""---
metadata: blank_node
---
"""

    if dry_run:
        if verbose:
            print(f"  Would create: {filepath.relative_to(REPO_ROOT)}")
    else:
        filepath.write_text(content, encoding='utf-8')
        if verbose:
            print(f"  Created: {filepath.relative_to(REPO_ROOT)}")


def create_statement_file(
    subject: str,
    predicate: str,
    obj: str,
    subject_wikilink: str,
    predicate_wikilink: str,
    obj_wikilink: str,
    namespace: str,
    output_dir: Path,
    dry_run: bool,
    verbose: bool
) -> None:
    """Create a statement file."""
    filename = f"{subject} {predicate} {obj}.md"
    filepath = output_dir / filename

    content = f"""---
metadata: statement
rdf__subject: {subject_wikilink}
rdf__predicate: {predicate_wikilink}
rdf__object: {obj_wikilink}
---
"""

    if dry_run:
        if verbose:
            print(f"  Would create: {filepath.relative_to(REPO_ROOT)}")
    else:
        filepath.write_text(content, encoding='utf-8')
        if verbose:
            print(f"  Created: {filepath.relative_to(REPO_ROOT)}")


def process_ontology(namespace: str, filename: str, dry_run: bool, verbose: bool) -> Dict[str, int]:
    """Process an ontology and generate blank node files."""
    filepath = ORIGINALS_DIR / filename
    if not filepath.exists():
        print(f"  ⚠️  Original file not found: {filepath}")
        return {'blank_nodes': 0, 'statements': 0}

    output_dir = REPO_ROOT / namespace

    print(f"\nProcessing {namespace} ({filename})...")

    # Parse the ontology
    g = parse_ontology(filepath)
    print(f"  Loaded {len(g)} triples")

    # Find blank nodes
    blank_nodes = find_blank_nodes(g)
    print(f"  Found {len(blank_nodes)} blank nodes")

    if not blank_nodes:
        return {'blank_nodes': 0, 'statements': 0}

    # Create blank node mapping
    blank_node_map = create_blank_node_map(blank_nodes, namespace)

    # Create blank node files
    created_files = 0
    for bn_id, bn_name in blank_node_map.items():
        create_blank_node_file(bn_name, namespace, output_dir, dry_run, verbose)
        created_files += 1

    print(f"  Created {created_files} blank node files")

    # Find all triples involving blank nodes
    statements_created = 0
    for s, p, o in g:
        # Only process triples where subject OR object is a blank node
        if not (isinstance(s, BNode) or isinstance(o, BNode)):
            continue

        # Convert terms to filename format
        subject_fn = term_to_filename(s, blank_node_map, namespace)
        predicate_fn = predicate_to_filename(p)
        object_fn = term_to_filename(o, blank_node_map, namespace)

        # Convert terms to wikilink format
        subject_wl = term_to_wikilink(s, blank_node_map, namespace)

        # Special handling for predicate
        if str(p) == str(RDF.type):
            predicate_wl = '"[[rdf__type]]"'
        else:
            for ns_uri, ns_prefix in NAMESPACES.items():
                if str(p).startswith(ns_uri):
                    local = str(p)[len(ns_uri):]
                    predicate_wl = f'"[[{ns_prefix}__{local}]]"'
                    break
            else:
                predicate_wl = f'"<{str(p)}>"'

        object_wl = term_to_wikilink(o, blank_node_map, namespace)

        # Check if statement file already exists (for non-blank node statements)
        filename = f"{subject_fn} {predicate_fn} {object_fn}.md"
        statement_path = output_dir / filename

        if statement_path.exists():
            if verbose:
                print(f"  Skipping existing: {filename}")
            continue

        create_statement_file(
            subject_fn, predicate_fn, object_fn,
            subject_wl, predicate_wl, object_wl,
            namespace, output_dir, dry_run, verbose
        )
        statements_created += 1

    print(f"  Created {statements_created} statement files")

    return {'blank_nodes': created_files, 'statements': statements_created}


def main():
    dry_run = '--dry-run' in sys.argv
    verbose = '--verbose' in sys.argv or '-v' in sys.argv

    print("=" * 60)
    print("Blank Node Generator for Exocortex Public Ontologies")
    print("=" * 60)

    if dry_run:
        print("\n🔍 DRY RUN MODE - no files will be created")

    total_stats = {'blank_nodes': 0, 'statements': 0}

    for namespace, filename in ONTOLOGIES_WITH_BLANK_NODES.items():
        stats = process_ontology(namespace, filename, dry_run, verbose)
        total_stats['blank_nodes'] += stats['blank_nodes']
        total_stats['statements'] += stats['statements']

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Total blank node files: {total_stats['blank_nodes']}")
    print(f"  Total statement files: {total_stats['statements']}")

    if dry_run:
        print("\n🔍 DRY RUN - run without --dry-run to create files")
    else:
        print("\n✅ Generation complete!")


if __name__ == '__main__':
    main()

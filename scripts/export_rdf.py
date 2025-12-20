#!/usr/bin/env python3
"""
Export file-based ontologies to RDF format (N-Triples).

This script reads the file-based triple format and exports to standard RDF.

Usage:
    python scripts/export_rdf.py [namespace] [--all] [--format turtle|ntriples]

Examples:
    python scripts/export_rdf.py time          # Export TIME ontology
    python scripts/export_rdf.py --all         # Export all ontologies
"""

import sys
import re
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set

try:
    from rdflib import Graph, Namespace, URIRef, Literal, BNode
    from rdflib.namespace import RDF, RDFS, OWL, XSD, DC, DCTERMS, SKOS
except ImportError:
    print("Error: rdflib is required. Install with: pip install rdflib")
    sys.exit(1)

REPO_ROOT = Path(__file__).parent.parent
EXPORTS_DIR = REPO_ROOT / 'exports'

# Namespace URIs
NAMESPACE_URIS = {
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
    'owl': 'http://www.w3.org/2002/07/owl#',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'dcterms': 'http://purl.org/dc/terms/',
    'dcam': 'http://purl.org/dc/dcam/',
    'skos': 'http://www.w3.org/2004/02/skos/core#',
    'foaf': 'http://xmlns.com/foaf/0.1/',
    'prov': 'http://www.w3.org/ns/prov#',
    'prov_o': 'http://www.w3.org/ns/prov-o#',  # PROV-O ontology IRI
    'time': 'http://www.w3.org/2006/time#',
    'geo': 'http://www.w3.org/2003/01/geo/wgs84_pos#',
    'vcard': 'http://www.w3.org/2006/vcard/ns#',
    'doap': 'http://usefulinc.com/ns/doap#',
    'sioc': 'http://rdfs.org/sioc/ns#',
    'xsd': 'http://www.w3.org/2001/XMLSchema#',
}

# Reverse mapping for quick lookup
PREFIX_TO_URI = NAMESPACE_URIS

# Blank node pattern: prefix!hexid (e.g., time!a1b2c3d4, skos!00000001)
BLANK_NODE_PATTERN = re.compile(r'^([a-z]+)!([a-f0-9]{8})$')


def unescape_case(name: str) -> str:
    """Remove dots before uppercase letters (case-escaping for case-insensitive FS).

    Example: '.Month.Of.Year' -> 'MonthOfYear'
    """
    return re.sub(r'\.([A-Z])', r'\1', name)


def parse_frontmatter(filepath: Path) -> Tuple[Optional[dict], Optional[str]]:
    """Parse YAML frontmatter from a markdown file."""
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        return None, str(e)

    if not content.startswith('---'):
        return None, "No frontmatter"

    end_match = re.search(r'\n---\s*\n', content[3:])
    if not end_match:
        end_match = re.search(r'\n---\s*$', content[3:])
        if not end_match:
            return None, "No closing ---"

    # Include the trailing newline before --- for proper block scalar chomping
    yaml_content = content[4:3 + end_match.start() + 1]

    try:
        data = yaml.safe_load(yaml_content)
        return data if data else {}, None
    except yaml.YAMLError as e:
        return None, str(e)


def prefix_local_to_uri(prefix: str, local: str) -> str:
    """Convert prefix:local to full URI."""
    if prefix in PREFIX_TO_URI:
        return PREFIX_TO_URI[prefix] + local
    return f"{prefix}:{local}"


def parse_wikilink(wikilink: str) -> Optional[str]:
    """
    Parse a wikilink and return the anchor name.

    Note: YAML removes outer quotes, so values come as [[anchor]] not "[[anchor]]"

    Examples:
        [[rdf__type]] -> "rdf__type"
        [[time!a1b2c3d4]] -> "time!a1b2c3d4"
    """
    wikilink = wikilink.strip()
    match = re.match(r'^\[\[([^\]|]+)(?:\|[^\]]+)?\]\]$', wikilink)
    if match:
        return match.group(1)
    return None


def anchor_to_term(anchor: str, blank_nodes: Dict[str, BNode]) -> URIRef | BNode:
    """
    Convert an anchor name to an RDF term.

    Examples:
        "rdf__type" -> URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
        "!time" -> URIRef("http://www.w3.org/2006/time#")
        "time!a1b2c3d4" -> BNode(...)
    """
    # Check if it's a blank node
    bn_match = BLANK_NODE_PATTERN.match(anchor)
    if bn_match:
        if anchor not in blank_nodes:
            blank_nodes[anchor] = BNode()
        return blank_nodes[anchor]

    # Check if it's a namespace reference (!prefix)
    if anchor.startswith('!'):
        prefix = anchor[1:]
        if prefix in PREFIX_TO_URI:
            return URIRef(PREFIX_TO_URI[prefix])
        return URIRef(anchor)

    # Regular anchor: prefix__local
    if '__' in anchor:
        prefix, local = anchor.split('__', 1)
        # Unescape case markers (e.g., .Month.Of.Year -> MonthOfYear)
        local = unescape_case(local)
        if prefix in PREFIX_TO_URI:
            return URIRef(PREFIX_TO_URI[prefix] + local)

    # Fallback
    return URIRef(unescape_case(anchor))


def parse_rdf_object(value: str, blank_nodes: Dict[str, BNode]) -> URIRef | BNode | Literal:
    """
    Parse an rdf__object value and return the appropriate RDF term.

    Note: YAML removes outer quotes, so values come in as:
        - Wikilinks: [[prefix__local]] -> URIRef
        - Literals: some text -> Literal
        - Language-tagged literals: "value"@en -> Literal with lang
        - Datatyped literals: "value"^^xsd:type -> Literal with datatype
        - External URIs: <http://...> -> URIRef
    """
    # Use stripped version for pattern detection, but keep original for literals
    stripped = value.strip()

    # Check for wikilink (after YAML parsing, no outer quotes)
    if stripped.startswith('[[') and stripped.endswith(']]'):
        anchor = stripped[2:-2]
        return anchor_to_term(anchor, blank_nodes)

    # Check for external URI
    if stripped.startswith('<') and stripped.endswith('>'):
        uri = stripped[1:-1]
        return URIRef(uri)

    # Check for language-tagged literal: "value"@lang
    lang_match = re.match(r'^"(.*)\"@([a-zA-Z-]+)$', stripped, re.DOTALL)
    if lang_match:
        text = lang_match.group(1)
        lang = lang_match.group(2)
        return Literal(text, lang=lang)

    # Check for datatyped literal: "value"^^<uri> or "value"^^prefix:local or "value"^^[[prefix__local]]
    datatype_match = re.match(r'^"(.*)"\^\^(.+)$', stripped, re.DOTALL)
    if datatype_match:
        text = datatype_match.group(1)
        dtype_str = datatype_match.group(2)
        # Handle <uri> format
        if dtype_str.startswith('<') and dtype_str.endswith('>'):
            dtype_uri = dtype_str[1:-1]
        # Handle [[prefix__local]] wikilink format
        elif dtype_str.startswith('[[') and dtype_str.endswith(']]'):
            anchor = dtype_str[2:-2]  # Remove [[ and ]]
            if '__' in anchor:
                prefix, local = anchor.split('__', 1)
                # Unescape case markers (e.g., any.U.R.I -> anyURI)
                local = unescape_case(local)
                if prefix in PREFIX_TO_URI:
                    dtype_uri = PREFIX_TO_URI[prefix] + local
                else:
                    dtype_uri = anchor
            else:
                dtype_uri = anchor
        # Handle prefix:local format
        elif ':' in dtype_str:
            prefix, local = dtype_str.split(':', 1)
            if prefix in PREFIX_TO_URI:
                dtype_uri = PREFIX_TO_URI[prefix] + local
            else:
                dtype_uri = dtype_str
        else:
            dtype_uri = dtype_str
        return Literal(text, datatype=URIRef(dtype_uri))

    # Plain literal - preserve original whitespace
    # Only strip surrounding quotes if present
    if stripped.startswith('"') and stripped.endswith('"') and len(stripped) >= 2:
        # Remove quotes but keep internal whitespace
        return Literal(stripped[1:-1])

    # Return original value preserving all whitespace
    return Literal(value)


def export_namespace(namespace: str, verbose: bool = False) -> Graph:
    """Export a single namespace to an RDF graph."""
    ns_dir = REPO_ROOT / namespace
    if not ns_dir.exists():
        print(f"  ⚠️  Namespace directory not found: {namespace}/")
        return Graph()

    g = Graph()
    blank_nodes: Dict[str, BNode] = {}

    # Bind common prefixes
    for prefix, uri in PREFIX_TO_URI.items():
        g.bind(prefix, Namespace(uri))

    # Process all statement files
    statement_count = 0
    error_count = 0

    for filepath in ns_dir.glob('*.md'):
        data, error = parse_frontmatter(filepath)

        if error:
            if verbose:
                print(f"  ⚠️  Parse error in {filepath.name}: {error}")
            error_count += 1
            continue

        if not data:
            continue

        metadata = data.get('metadata')

        # Only process statements
        if metadata != 'statement':
            continue

        # Get subject, predicate, object
        subj_val = data.get('rdf__subject', '')
        pred_val = data.get('rdf__predicate', '')
        obj_val = data.get('rdf__object', '')

        if not all([subj_val, pred_val, obj_val]):
            if verbose:
                print(f"  ⚠️  Incomplete statement in {filepath.name}")
            error_count += 1
            continue

        try:
            # Parse subject (wikilink or external URI)
            subj_val_stripped = subj_val.strip()
            if subj_val_stripped.startswith('<') and subj_val_stripped.endswith('>'):
                # External URI
                subject = URIRef(subj_val_stripped[1:-1])
            else:
                subj_anchor = parse_wikilink(subj_val)
                if not subj_anchor:
                    if verbose:
                        print(f"  ⚠️  Invalid subject wikilink in {filepath.name}: {subj_val}")
                    error_count += 1
                    continue
                subject = anchor_to_term(subj_anchor, blank_nodes)

            # Parse predicate (wikilink or external URI)
            pred_val_stripped = pred_val.strip()
            if pred_val_stripped.startswith('<') and pred_val_stripped.endswith('>'):
                predicate = URIRef(pred_val_stripped[1:-1])
            else:
                pred_anchor = parse_wikilink(pred_val)
                if not pred_anchor:
                    if verbose:
                        print(f"  ⚠️  Invalid predicate wikilink in {filepath.name}: {pred_val}")
                    error_count += 1
                    continue
                predicate = anchor_to_term(pred_anchor, blank_nodes)

            # Parse object (wikilink or literal)
            obj = parse_rdf_object(obj_val, blank_nodes)

            # Add triple to graph
            g.add((subject, predicate, obj))
            statement_count += 1

        except Exception as e:
            if verbose:
                print(f"  ⚠️  Error processing {filepath.name}: {e}")
            error_count += 1

    if verbose:
        print(f"  Exported {statement_count} statements, {error_count} errors, {len(blank_nodes)} blank nodes")

    return g


def export_ontology(namespace: str, output_format: str = 'ntriples', verbose: bool = False) -> Path:
    """Export an ontology to a file."""
    print(f"\nExporting {namespace}...")

    g = export_namespace(namespace, verbose)

    if len(g) == 0:
        print(f"  ⚠️  No triples exported for {namespace}")
        return None

    # Create exports directory
    EXPORTS_DIR.mkdir(exist_ok=True)

    # Determine file extension
    if output_format == 'turtle':
        ext = '.ttl'
        fmt = 'turtle'
    else:
        ext = '.nt'
        fmt = 'ntriples'

    output_path = EXPORTS_DIR / f"{namespace}{ext}"

    # Serialize
    g.serialize(destination=str(output_path), format=fmt)

    print(f"  ✅ Exported {len(g)} triples to {output_path.name}")

    return output_path


def main():
    verbose = '--verbose' in sys.argv or '-v' in sys.argv
    export_all = '--all' in sys.argv

    # Determine format
    output_format = 'ntriples'
    if '--format' in sys.argv:
        idx = sys.argv.index('--format')
        if idx + 1 < len(sys.argv):
            fmt = sys.argv[idx + 1].lower()
            if fmt in ('turtle', 'ttl'):
                output_format = 'turtle'

    # Get namespaces to export
    namespaces = []
    for arg in sys.argv[1:]:
        if not arg.startswith('-') and arg in NAMESPACE_URIS:
            namespaces.append(arg)

    if export_all:
        # Export all namespaces that have directories
        namespaces = [ns for ns in NAMESPACE_URIS.keys() if (REPO_ROOT / ns).exists()]

    if not namespaces:
        print("Usage: python scripts/export_rdf.py [namespace] [--all] [--format turtle|ntriples]")
        print("\nAvailable namespaces:")
        for ns in sorted(NAMESPACE_URIS.keys()):
            if (REPO_ROOT / ns).exists():
                print(f"  {ns}")
        sys.exit(1)

    print("=" * 60)
    print("RDF Exporter for Exocortex Public Ontologies")
    print("=" * 60)
    print(f"Format: {output_format}")

    total_triples = 0
    for namespace in namespaces:
        path = export_ontology(namespace, output_format, verbose)
        if path:
            # Count triples
            g = Graph()
            g.parse(path, format=output_format if output_format != 'ntriples' else 'nt')
            total_triples += len(g)

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Exported {len(namespaces)} ontologies")
    print(f"  Total triples: {total_triples}")
    print(f"  Output directory: {EXPORTS_DIR}/")


if __name__ == '__main__':
    main()

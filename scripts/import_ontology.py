#!/usr/bin/env python3
"""
Import RDF ontologies into file-based triple format.

This script reads RDF ontologies in various formats and converts them
to the file-based triple format used in this repository.

Supported formats:
    - RDF/XML (.rdf, .owl, .xml)
    - Turtle (.ttl)
    - N-Triples (.nt)
    - N3 (.n3)
    - JSON-LD (.jsonld, .json)
    - TriG (.trig)
    - N-Quads (.nq)

Usage:
    python scripts/import_ontology.py <input_file> <output_dir> [--prefix PREFIX] [--namespace URI]

Examples:
    python scripts/import_ontology.py originals/rdf.rdf rdfimported --prefix rdf
    python scripts/import_ontology.py ontology.ttl myonto --prefix myonto --namespace http://example.org/onto#
"""

import argparse
import hashlib
import os
import re
import sys
import uuid
from pathlib import Path
from typing import Dict, Optional, Set, Tuple
from collections import defaultdict

# UUIDv5 namespace for URLs (standard)
UUID_NAMESPACE_URL = uuid.UUID('6ba7b811-9dad-11d1-80b4-00c04fd430c8')

try:
    from rdflib import Graph, URIRef, Literal, BNode, Namespace
    from rdflib.namespace import RDF, RDFS, OWL, XSD, DC, DCTERMS, SKOS
except ImportError:
    print("Error: rdflib is required. Install with: pip install rdflib")
    sys.exit(1)

# Known namespace URIs and their prefixes
KNOWN_NAMESPACES = {
    'http://www.w3.org/1999/02/22-rdf-syntax-ns#': 'rdf',
    'http://www.w3.org/2000/01/rdf-schema#': 'rdfs',
    'http://www.w3.org/2002/07/owl#': 'owl',
    'http://purl.org/dc/elements/1.1/': 'dc',
    'http://purl.org/dc/terms/': 'dcterms',
    'http://purl.org/dc/dcam/': 'dcam',
    'http://www.w3.org/2004/02/skos/core#': 'skos',
    'http://xmlns.com/foaf/0.1/': 'foaf',
    'http://www.w3.org/ns/prov#': 'prov',
    'http://www.w3.org/ns/prov-o#': 'prov_o',
    'http://www.w3.org/2006/time#': 'time',
    'http://www.w3.org/2003/01/geo/wgs84_pos#': 'geo',
    'http://www.w3.org/2006/vcard/ns#': 'vcard',
    'http://usefulinc.com/ns/doap#': 'doap',
    'http://rdfs.org/sioc/ns#': 'sioc',
    'http://www.w3.org/2001/XMLSchema#': 'xsd',
}

# Reverse mapping
PREFIX_TO_URI = {v: k for k, v in KNOWN_NAMESPACES.items()}


def detect_format(filepath: Path) -> str:
    """Detect RDF format from file content and extension."""
    # First, try to detect from content
    try:
        content = filepath.read_text(encoding='utf-8')[:500]
        # Check for Turtle/N3 indicators
        if content.strip().startswith('@prefix') or content.strip().startswith('@base'):
            return 'turtle'
        # Check for JSON-LD
        if content.strip().startswith('{') and '"@' in content:
            return 'json-ld'
        # Check for N-Triples (lines ending with .)
        lines = content.strip().split('\n')
        if all(line.strip().endswith('.') or line.strip().startswith('#') or not line.strip() for line in lines[:5] if line.strip()):
            if not content.strip().startswith('<') or '<?xml' not in content:
                # Could be N-Triples - but also could be Turtle without prefix
                pass
        # Check for XML
        if content.strip().startswith('<?xml') or content.strip().startswith('<rdf:RDF'):
            return 'xml'
    except Exception:
        pass

    # Fall back to extension
    suffix = filepath.suffix.lower()
    format_map = {
        '.rdf': 'xml',
        '.owl': 'xml',
        '.xml': 'xml',
        '.ttl': 'turtle',
        '.turtle': 'turtle',
        '.nt': 'nt',
        '.ntriples': 'nt',
        '.n3': 'n3',
        '.jsonld': 'json-ld',
        '.json': 'json-ld',
        '.trig': 'trig',
        '.nq': 'nquads',
    }
    return format_map.get(suffix, 'xml')


def uri_to_uuid(uri: str) -> str:
    """Convert a URI to UUIDv5 using URL namespace.

    This provides case-sensitive, collision-free filenames.

    Example: 'http://purl.org/dc/elements/1.1/contributor' -> 'a1b2c3d4-e5f6-5789-abcd-ef0123456789'
    """
    return str(uuid.uuid5(UUID_NAMESPACE_URL, uri))


def escape_case(name: str) -> str:
    """DEPRECATED: Add dots before uppercase letters for case-insensitive filesystem.

    This function is kept for backward compatibility but should not be used.
    Use uri_to_uuid() instead.

    Example: 'MonthOfYear' -> '.Month.Of.Year'
    """
    # Don't escape if first char is uppercase (it becomes .X which is weird for filename start)
    # Actually, we DO need to escape even the first char for consistency
    result = re.sub(r'([A-Z])', r'.\1', name)
    return result


def uri_to_anchor(uri: str, ontology_prefix: str, ontology_ns: str) -> Tuple[str, str, bool]:
    """
    Convert a URI to an anchor name (UUIDv5).

    Returns: (uuid_string, None, is_external)

    The uuid_string is the full UUIDv5 generated from the URI.
    The second element is kept as None for API compatibility but is unused.

    Examples:
        http://www.w3.org/1999/02/22-rdf-syntax-ns#type -> ('a1b2c3d4-...', None, False)
        http://example.org/foo -> (None, None, True)  # External URI
    """
    uri_str = str(uri)

    # Check known namespaces
    for ns_uri, prefix in KNOWN_NAMESPACES.items():
        if uri_str.startswith(ns_uri):
            return (uri_to_uuid(uri_str), None, False)

    # Check if it's the ontology namespace
    if ontology_ns and uri_str.startswith(ontology_ns):
        return (uri_to_uuid(uri_str), None, False)

    # Check if URI ends with # or / and extract local part
    if '#' in uri_str:
        ns, local = uri_str.rsplit('#', 1)
        ns += '#'
    elif '/' in uri_str:
        ns, local = uri_str.rsplit('/', 1)
        ns += '/'
    else:
        # External URI with no namespace separator
        return (None, None, True)

    # Try to find prefix for the namespace
    if ns in KNOWN_NAMESPACES:
        return (uri_to_uuid(uri_str), None, False)
    else:
        # External URI - not a known namespace
        return (None, None, True)


def bnode_to_anchor(bnode: BNode, prefix: str, bnode_map: Dict[str, str]) -> str:
    """
    Convert a blank node to an anchor name.

    Format: prefix!8hexchars
    """
    bnode_id = str(bnode)
    if bnode_id not in bnode_map:
        # Create a stable 8-char hex ID from the bnode
        hash_bytes = hashlib.md5(bnode_id.encode()).hexdigest()[:8]
        bnode_map[bnode_id] = f"{prefix}!{hash_bytes}"
    return bnode_map[bnode_id]


def term_to_anchor(term, ontology_prefix: str, ontology_ns: str, bnode_map: Dict[str, str], external_uris: Dict[str, str] = None) -> Tuple[str, bool]:
    """
    Convert an RDF term to an anchor name (UUIDv5).

    Returns: (anchor_name, is_external)

    anchor_name examples: 'a1b2c3d4-e5f6-5789-abcd-ef0123456789', '!rdf', '_ext_'
    is_external: True if the anchor is a placeholder for an external URI
    """
    if external_uris is None:
        external_uris = {}

    if isinstance(term, URIRef):
        uri_str = str(term)

        # Check if it's a namespace URI (ends with # or /)
        # and matches a known namespace exactly
        for ns_uri, prefix in KNOWN_NAMESPACES.items():
            if uri_str == ns_uri.rstrip('#/') or uri_str == ns_uri:
                return (f"!{prefix}", False)

        # Check ontology namespace
        if ontology_ns:
            ns_base = ontology_ns.rstrip('#/')
            if uri_str == ns_base or uri_str == ontology_ns:
                return (f"!{ontology_prefix}", False)

        # Regular URI
        uuid_anchor, _, is_external = uri_to_anchor(uri_str, ontology_prefix, ontology_ns)
        if is_external:
            # Create a unique placeholder for this external URI
            ext_key = f"_ext{len(external_uris)}_"
            external_uris[ext_key] = uri_str
            return (ext_key, True)
        else:
            # uuid_anchor is already the full UUIDv5 string
            return (uuid_anchor, False)

    elif isinstance(term, BNode):
        return (bnode_to_anchor(term, ontology_prefix, bnode_map), False)

    else:
        raise ValueError(f"Cannot convert {type(term)} to anchor")


def literal_to_yaml(lit: Literal) -> str:
    """
    Convert an RDF literal to YAML value.

    Examples:
        Literal("hello") -> '"hello"'
        Literal("hello", lang="en") -> '"hello"@en'
        Literal("42", datatype=XSD.integer) -> '"42"^^[[a1b2c3d4-...]]'
    """
    value = str(lit)

    # Escape special characters in the value
    # For YAML, we need to escape quotes and handle newlines
    escaped = value.replace('\\', '\\\\').replace('"', '\\"')

    if lit.language:
        return f'"{escaped}"@{lit.language}'
    elif lit.datatype:
        dtype_str = str(lit.datatype)
        # Convert datatype URI to wikilink using UUIDv5
        dtype_uuid = uri_to_uuid(dtype_str)
        return f'"{escaped}"^^[[{dtype_uuid}]]'
    else:
        # Plain literal
        return f'"{escaped}"'


def make_safe_filename(name: str) -> str:
    """
    Make a string safe for use as a filename.

    Handles special characters that are problematic on various filesystems.
    """
    # Replace problematic characters
    # Keep: alphanumeric, underscore, dot, hyphen, exclamation (for namespace files)
    # Spaces are allowed (used in statement filenames)
    safe = name
    # Remove or replace truly problematic chars
    for char in ['/', '\\', ':', '*', '?', '"', '<', '>', '|']:
        safe = safe.replace(char, '_')
    return safe


def create_namespace_file(output_dir: Path, prefix: str, namespace_uri: str) -> None:
    """Create a namespace declaration file."""
    filename = f"!{prefix}.md"
    filepath = output_dir / filename

    content = f"""---
metadata: namespace
"!": {namespace_uri}
---
"""
    filepath.write_text(content, encoding='utf-8')


def create_anchor_file(output_dir: Path, anchor: str) -> None:
    """Create an anchor file for a resource."""
    filename = f"{make_safe_filename(anchor)}.md"
    filepath = output_dir / filename

    # Don't overwrite if exists
    if filepath.exists():
        return

    content = """---
metadata: anchor
---
"""
    filepath.write_text(content, encoding='utf-8')


def create_blank_node_file(output_dir: Path, anchor: str) -> None:
    """Create a blank node anchor file."""
    filename = f"{make_safe_filename(anchor)}.md"
    filepath = output_dir / filename

    if filepath.exists():
        return

    content = """---
metadata: blank_node
---
"""
    filepath.write_text(content, encoding='utf-8')


def escape_yaml_multiline(value: str) -> str:
    """
    Escape a multiline string for YAML.
    Uses block scalar with keep indicator (|+) for multiline, or quoted string for single line.
    """
    if '\n' in value:
        # For multiline, use block scalar
        # Indent each line by 2 spaces
        lines = value.split('\n')
        indented = '\n'.join('  ' + line for line in lines)
        # Use |+ to keep trailing newlines, add indented blank line at end
        return f"|+\n{indented}\n  "
    else:
        # Single line - escape for YAML double-quoted string
        escaped = value.replace('\\', '\\\\').replace('"', '\\"')
        return f'"{escaped}"'


def create_statement_file(
    output_dir: Path,
    subject_anchor: str,
    predicate_anchor: str,
    obj_anchor_or_literal: str,
    is_literal: bool,
    used_filenames: Dict[str, int],
    subject_uri: Optional[str] = None,
    predicate_uri: Optional[str] = None,
    object_uri: Optional[str] = None,
    subject_is_external: bool = False,
    predicate_is_external: bool = False,
    object_is_external: bool = False
) -> None:
    """
    Create a statement file for an RDF triple.

    Filename format: {subject} {predicate} {object}.md
    For literals, object is replaced with ___ placeholder.
    For external URIs, use _ext_ placeholder.
    """
    # Use 'a' shorthand for rdf:type predicate in filename
    pred_name = 'a' if predicate_anchor == 'rdf__type' else predicate_anchor

    if is_literal:
        # Use ___ for literal placeholder in filename
        base_filename = f"{subject_anchor} {pred_name} ___"
    else:
        base_filename = f"{subject_anchor} {pred_name} {obj_anchor_or_literal}"

    base_filename = make_safe_filename(base_filename)

    # Handle duplicate filenames by adding numeric suffix
    if base_filename in used_filenames:
        used_filenames[base_filename] += 1
        filename = f"{base_filename}{used_filenames[base_filename]}.md"
    else:
        used_filenames[base_filename] = 0
        filename = f"{base_filename}.md"

    # But wait - for literal duplicates, we use ___2, ___3, etc (not ___1)
    # And for first literal, we use ___ (not ___0)
    # Let me re-check the convention...
    # Looking at existing files: ___.md, ___2.md, ___3.md, etc.
    # So first occurrence is ___.md, second is ___2.md

    # Recalculate filename
    count = used_filenames[base_filename]
    if count == 0:
        filename = f"{base_filename}.md"
    else:
        # For ___ files, append number after ___
        if is_literal:
            filename = f"{base_filename}{count + 1}.md"
        else:
            # For non-literals with same subject+predicate+object, this shouldn't happen
            # But if it does, add suffix
            filename = f"{base_filename}_{count + 1}.md"

    filepath = output_dir / filename

    # Build YAML frontmatter
    # Subject
    if subject_is_external:
        subj_yaml = f'"<{subject_uri}>"'
    else:
        subj_yaml = f'"[[{subject_anchor}]]"'

    # Predicate with optional alias for rdf:type
    if predicate_is_external:
        pred_yaml = f'"<{predicate_uri}>"'
    elif predicate_anchor == 'rdf__type':
        pred_yaml = '"[[rdf__type|a]]"'
    else:
        pred_yaml = f'"[[{predicate_anchor}]]"'

    # Object
    if is_literal:
        # obj_anchor_or_literal is the YAML-formatted literal value
        obj_yaml = obj_anchor_or_literal
    elif object_is_external:
        obj_yaml = f'"<{object_uri}>"'
    else:
        obj_yaml = f'"[[{obj_anchor_or_literal}]]"'

    content = f"""---
metadata: statement
rdf__subject: {subj_yaml}
rdf__predicate: {pred_yaml}
rdf__object: {obj_yaml}
---
"""
    filepath.write_text(content, encoding='utf-8')


def import_ontology(
    input_file: Path,
    output_dir: Path,
    prefix: str,
    namespace_uri: Optional[str] = None,
    verbose: bool = False
) -> Tuple[int, int, int]:
    """
    Import an RDF ontology into file-based format.

    Returns: (triple_count, anchor_count, file_count)
    """
    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Load the ontology
    g = Graph()
    fmt = detect_format(input_file)
    if verbose:
        print(f"Loading {input_file} as {fmt}...")
    g.parse(str(input_file), format=fmt)

    if verbose:
        print(f"Loaded {len(g)} triples")

    # Try to detect ontology namespace from the graph
    if not namespace_uri:
        # Look for owl:Ontology or the most common namespace
        for s, p, o in g.triples((None, RDF.type, OWL.Ontology)):
            namespace_uri = str(s)
            if not namespace_uri.endswith('#') and not namespace_uri.endswith('/'):
                namespace_uri += '#'
            break

        if not namespace_uri:
            # Try to detect from common subjects
            ns_counts = defaultdict(int)
            for s, p, o in g:
                if isinstance(s, URIRef):
                    uri = str(s)
                    if '#' in uri:
                        ns = uri.rsplit('#', 1)[0] + '#'
                    elif '/' in uri:
                        ns = uri.rsplit('/', 1)[0] + '/'
                    else:
                        continue
                    ns_counts[ns] += 1

            if ns_counts:
                namespace_uri = max(ns_counts.keys(), key=lambda k: ns_counts[k])

    if verbose:
        print(f"Using namespace: {namespace_uri}")

    # Create namespace file
    create_namespace_file(output_dir, prefix, namespace_uri or f"http://example.org/{prefix}#")

    # Track blank nodes and external URIs
    bnode_map: Dict[str, str] = {}
    external_uris: Dict[str, str] = {}

    # Collect all anchors needed
    anchors: Set[str] = set()
    blank_nodes: Set[str] = set()

    # First pass: identify all resources that need anchor files
    for s, p, o in g:
        # Subject
        if isinstance(s, URIRef):
            anchor, is_ext = term_to_anchor(s, prefix, namespace_uri, bnode_map, external_uris)
            if not is_ext and not anchor.startswith('!'):  # Not a namespace
                anchors.add(anchor)
        elif isinstance(s, BNode):
            bn_anchor, _ = term_to_anchor(s, prefix, namespace_uri, bnode_map, external_uris)
            blank_nodes.add(bn_anchor)

        # Predicate (always URIRef)
        if isinstance(p, URIRef):
            anchor, is_ext = term_to_anchor(p, prefix, namespace_uri, bnode_map, external_uris)
            if not is_ext and not anchor.startswith('!'):
                anchors.add(anchor)

        # Object (if URI or BNode)
        if isinstance(o, URIRef):
            anchor, is_ext = term_to_anchor(o, prefix, namespace_uri, bnode_map, external_uris)
            if not is_ext and not anchor.startswith('!'):
                anchors.add(anchor)
        elif isinstance(o, BNode):
            bn_anchor, _ = term_to_anchor(o, prefix, namespace_uri, bnode_map, external_uris)
            blank_nodes.add(bn_anchor)

    # Create anchor files
    if verbose:
        print(f"Creating {len(anchors)} anchor files...")
    for anchor in anchors:
        create_anchor_file(output_dir, anchor)

    # Create blank node files
    if verbose:
        print(f"Creating {len(blank_nodes)} blank node files...")
    for bn in blank_nodes:
        create_blank_node_file(output_dir, bn)

    # Second pass: create statement files
    used_filenames: Dict[str, int] = {}
    triple_count = 0

    if verbose:
        print(f"Creating statement files...")

    for s, p, o in g:
        # Get subject anchor
        subj_anchor, subj_is_ext = term_to_anchor(s, prefix, namespace_uri, bnode_map, external_uris)
        subj_uri = str(s) if isinstance(s, URIRef) else None

        # Get predicate anchor
        pred_anchor, pred_is_ext = term_to_anchor(p, prefix, namespace_uri, bnode_map, external_uris)
        pred_uri = str(p) if isinstance(p, URIRef) else None

        # Handle object
        if isinstance(o, Literal):
            obj_yaml = literal_to_yaml(o)
            # Check for multiline
            obj_str = str(o)
            if '\n' in obj_str or '\t' in obj_str:
                # Use block scalar for multiline
                obj_yaml = escape_yaml_multiline(obj_str)
                if o.language:
                    # Can't easily use block scalar with language tag
                    # Fall back to escaped string
                    escaped = obj_str.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\t', '\\t')
                    obj_yaml = f'"{escaped}"@{o.language}'
                elif o.datatype:
                    dtype_str = str(o.datatype)
                    # Use UUIDv5 for datatype reference
                    dtype_uuid = uri_to_uuid(dtype_str)
                    escaped = obj_str.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\t', '\\t')
                    obj_yaml = f'"{escaped}"^^[[{dtype_uuid}]]'

            create_statement_file(
                output_dir, subj_anchor, pred_anchor, obj_yaml,
                is_literal=True, used_filenames=used_filenames,
                subject_uri=subj_uri, predicate_uri=pred_uri,
                subject_is_external=subj_is_ext, predicate_is_external=pred_is_ext
            )
        else:
            obj_anchor, obj_is_ext = term_to_anchor(o, prefix, namespace_uri, bnode_map, external_uris)
            obj_uri = str(o) if isinstance(o, URIRef) else None
            create_statement_file(
                output_dir, subj_anchor, pred_anchor, obj_anchor,
                is_literal=False, used_filenames=used_filenames,
                subject_uri=subj_uri, predicate_uri=pred_uri, object_uri=obj_uri,
                subject_is_external=subj_is_ext, predicate_is_external=pred_is_ext,
                object_is_external=obj_is_ext
            )

        triple_count += 1

    # Count files created
    file_count = len(list(output_dir.glob('*.md')))

    return triple_count, len(anchors) + len(blank_nodes), file_count


def main():
    parser = argparse.ArgumentParser(
        description='Import RDF ontologies into file-based triple format.'
    )
    parser.add_argument('input', type=Path, help='Input RDF file')
    parser.add_argument('output', type=Path, help='Output directory')
    parser.add_argument('--prefix', '-p', required=True,
                        help='Namespace prefix (e.g., rdf, owl, myonto)')
    parser.add_argument('--namespace', '-n',
                        help='Namespace URI (auto-detected if not specified)')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Verbose output')

    args = parser.parse_args()

    if not args.input.exists():
        print(f"Error: Input file not found: {args.input}")
        sys.exit(1)

    print(f"Importing {args.input} to {args.output}/")

    triple_count, anchor_count, file_count = import_ontology(
        args.input,
        args.output,
        args.prefix,
        args.namespace,
        args.verbose
    )

    print(f"Done!")
    print(f"  Triples imported: {triple_count}")
    print(f"  Anchors created: {anchor_count}")
    print(f"  Files created: {file_count}")


if __name__ == '__main__':
    main()

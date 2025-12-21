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

# Mapping from namespace URIs to their prefixes
NAMESPACE_URI_TO_PREFIX = {
    'http://www.w3.org/1999/02/22-rdf-syntax-ns#': 'rdf',
    'http://www.w3.org/2000/01/rdf-schema#': 'rdfs',
    'http://www.w3.org/2002/07/owl#': 'owl',
    'http://purl.org/dc/elements/1.1/': 'dc',
    'http://purl.org/dc/terms/': 'dcterms',
    'http://purl.org/dc/dcam/': 'dcam',
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

# Reverse mapping: prefix → namespace URI
PREFIX_TO_NAMESPACE_URI = {v: k for k, v in NAMESPACE_URI_TO_PREFIX.items()}


def extract_prefix_from_uri(uri: str) -> Optional[str]:
    """Extract the namespace prefix from a full URI."""
    if not uri:
        return None
    for ns_uri, prefix in NAMESPACE_URI_TO_PREFIX.items():
        if uri.startswith(ns_uri):
            return prefix
    return None


def extract_localname_from_uri(uri: str) -> str:
    """Extract local name from URI."""
    if '#' in uri:
        return uri.split('#')[-1]
    elif '/' in uri:
        return uri.rstrip('/').split('/')[-1]
    return uri


def format_alias_value(value: str) -> str:
    """Format alias value for YAML, adding quotes if needed."""
    needs_quotes = (
        ':' in value or
        '?' in value or
        value.startswith('[') or
        value.startswith('{') or
        value.startswith('"') or
        value.startswith("'") or
        value.startswith('!') or
        value.startswith('_:') or
        '\n' in value or
        value.startswith('#')
    )
    if needs_quotes:
        escaped = value.replace('\\', '\\\\').replace('"', '\\"')
        return f'"{escaped}"'
    return value


def write_file(filepath: Path, content: str) -> None:
    """Write file with normalized LF line endings."""
    # Normalize CRLF and CR to LF
    content = content.replace('\r\n', '\n').replace('\r', '\n')
    filepath.write_text(content, encoding='utf-8')


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

    Returns: (uuid_string, None, is_local)

    The uuid_string is the full UUIDv5 generated from the URI.
    The second element is kept as None for API compatibility but is unused.
    is_local indicates if this resource belongs to the current ontology namespace.

    ALL URIs are converted to UUIDv5 and use wikilink syntax [[uuid]].
    Missing target files are allowed (resources may be defined elsewhere).

    Examples:
        http://www.w3.org/1999/02/22-rdf-syntax-ns#type -> ('73b69787-...', None, False)
        http://www.w3.org/2000/01/rdf-schema#Class -> ('abcd1234-...', None, False)
        http://example.org/foo -> ('efgh5678-...', None, False)
    """
    uri_str = str(uri)
    uuid_str = uri_to_uuid(uri_str)

    # Check if it belongs to current ontology namespace
    is_local = ontology_ns and uri_str.startswith(ontology_ns)

    return (uuid_str, None, not is_local)


def bnode_to_anchor(bnode: BNode, prefix: str, bnode_map: Dict[str, str], namespace_uri: str) -> Tuple[str, str]:
    """
    Convert a blank node to an anchor name (UUIDv5 from skolem IRI).

    Returns: (uuid_anchor, blank_local_id)

    The blank_local_id is needed for creating the blank node file later.
    """
    bnode_id = str(bnode)
    if bnode_id not in bnode_map:
        # Create a stable 8-char hex ID from the bnode
        hash_bytes = hashlib.md5(bnode_id.encode()).hexdigest()[:8]

        # Build skolem IRI and generate UUID
        base = namespace_uri.rstrip('#/')
        skolem_iri = f"{base}/.well-known/genid/{hash_bytes}"
        bnode_uuid = uri_to_uuid(skolem_iri)

        bnode_map[bnode_id] = (bnode_uuid, hash_bytes)

    return bnode_map[bnode_id]


def term_to_anchor(term, ontology_prefix: str, ontology_ns: str, bnode_map: Dict[str, str],
                   external_uris: Dict[str, str] = None, ontology_uri: str = None,
                   namespace_uuid_map: Dict[str, str] = None) -> Tuple[str, bool]:
    """
    Convert an RDF term to an anchor name (UUIDv5).

    Returns: (anchor_name, is_local)

    anchor_name: Always a UUIDv5 string
    is_local: False if the resource belongs to current ontology namespace

    All URIs are converted to UUIDv5 and will use wikilink syntax [[uuid]].
    Missing target files are allowed.

    Args:
        ontology_uri: The actual ontology URI (may differ from namespace, e.g.,
                      http://www.w3.org/2002/07/owl vs http://www.w3.org/2002/07/owl#)
        namespace_uuid_map: Mapping from namespace URI to its UUID (for namespace references)
    """
    if namespace_uuid_map is None:
        namespace_uuid_map = {}

    if isinstance(term, URIRef):
        uri_str = str(term)

        # FIRST: Check if it's the ontology URI itself (different from namespace)
        # This handles cases like http://www.w3.org/2002/07/owl which is
        # different from the namespace http://www.w3.org/2002/07/owl#
        # Must come BEFORE namespace checks to avoid matching ns.rstrip('#/')
        if ontology_uri and uri_str == ontology_uri:
            # Check if ontology_uri differs from namespace WITH its suffix
            # e.g., ontology_uri = "http://.../owl" vs ontology_ns = "http://.../owl#"
            if ontology_ns and ontology_uri != ontology_ns:
                # It's a distinct ontology URI - return its UUID
                return (uri_to_uuid(ontology_uri), False)
            # Otherwise fall through to namespace check

        # Check if it's a namespace URI (ends with # or /)
        # and matches a known namespace exactly
        # Returns UUID for the namespace
        for ns_uri, prefix in NAMESPACE_URI_TO_PREFIX.items():
            if uri_str == ns_uri:  # Only exact match with suffix
                ns_uuid = namespace_uuid_map.get(ns_uri) or uri_to_uuid(ns_uri)
                return (ns_uuid, False)

        # Check ontology namespace (only exact match with suffix)
        if ontology_ns:
            if uri_str == ontology_ns:
                ns_uuid = namespace_uuid_map.get(ontology_ns) or uri_to_uuid(ontology_ns)
                return (ns_uuid, False)

        # Regular URI - always returns UUID, is_local indicates if it's from current namespace
        uuid_anchor, _, is_not_local = uri_to_anchor(uri_str, ontology_prefix, ontology_ns)
        return (uuid_anchor, is_not_local)

    elif isinstance(term, BNode):
        bnode_uuid, _ = bnode_to_anchor(term, ontology_prefix, bnode_map, ontology_ns or '')
        return (bnode_uuid, False)

    else:
        raise ValueError(f"Cannot convert {type(term)} to anchor")


def literal_to_yaml(lit: Literal) -> str:
    """
    Convert an RDF literal to YAML value.

    The result is a YAML double-quoted string containing the RDF literal notation.
    All special characters are properly escaped for YAML compatibility.

    Examples:
        Literal("hello") -> '"\\\"hello\\\""'  (YAML value: "hello")
        Literal("hello", lang="en") -> '"\\\"hello\\\"@en"'  (YAML value: "hello"@en)
        Literal("42", datatype=XSD.integer) -> '"\\\"42\\\"^^[[uuid]]"'
    """
    value = str(lit)

    # Normalize line endings (CRLF -> LF)
    value = value.replace('\r\n', '\n')
    value = value.replace('\r', '\n')

    # Escape special characters for YAML double-quoted strings
    # Order matters: backslash first, then quotes, then special chars
    escaped = value.replace('\\', '\\\\')
    escaped = escaped.replace('"', '\\"')
    escaped = escaped.replace('\n', '\\n')
    escaped = escaped.replace('\t', '\\t')

    if lit.language:
        # Format: "\"value\"@lang"
        inner = f'\\"{escaped}\\"@{lit.language}'
    elif lit.datatype:
        dtype_str = str(lit.datatype)
        # Convert datatype URI to wikilink using UUIDv5
        dtype_uuid = uri_to_uuid(dtype_str)
        # Format: "\"value\"^^[[uuid]]"
        inner = f'\\"{escaped}\\"^^[[{dtype_uuid}]]'
    else:
        # Plain literal: "\"value\""
        inner = f'\\"{escaped}\\"'

    # Wrap in double quotes for YAML compatibility
    return f'"{inner}"'


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


def create_namespace_file(output_dir: Path, prefix: str, namespace_uri: str) -> str:
    """Create a namespace declaration file.

    Returns: The UUID used for the filename (for link updates).
    """
    # Generate UUIDv5 from namespace URI
    ns_uuid = uri_to_uuid(namespace_uri)
    filename = f"{ns_uuid}.md"
    filepath = output_dir / filename

    # Generate alias: !prefix
    alias = format_alias_value(f"!{prefix}")

    content = f"""---
metadata: namespace
uri: {namespace_uri}
aliases:
  - {alias}
---
"""
    write_file(filepath, content)
    return ns_uuid


def create_anchor_file(output_dir: Path, anchor: str, uri: str = None) -> None:
    """Create an anchor file for a resource.

    Args:
        output_dir: Directory to create the file in
        anchor: The anchor name (UUID)
        uri: Optional URI for this resource (added to frontmatter)
    """
    filename = f"{make_safe_filename(anchor)}.md"
    filepath = output_dir / filename

    # Don't overwrite if exists
    if filepath.exists():
        return

    if uri:
        # Generate alias: prefix:localname
        prefix = extract_prefix_from_uri(uri)
        if prefix:
            localname = extract_localname_from_uri(uri)
            alias = format_alias_value(f"{prefix}:{localname}")
            content = f"""---
metadata: anchor
uri: {uri}
aliases:
  - {alias}
---
"""
        else:
            content = f"""---
metadata: anchor
uri: {uri}
---
"""
    else:
        content = """---
metadata: anchor
---
"""
    write_file(filepath, content)


def create_blank_node_file(output_dir: Path, anchor: str, namespace_uri: str, blank_id: str) -> str:
    """Create a blank node anchor file using skolem IRI.

    Args:
        output_dir: Directory to create file in
        anchor: Original anchor name (prefix!hexid format) - kept for compatibility
        namespace_uri: The namespace URI for skolemization
        blank_id: The blank node local ID

    Returns: The UUID used for the filename.
    """
    # Build skolem IRI (RFC 7511 / W3C RDF 1.1)
    base = namespace_uri.rstrip('#/')
    skolem_iri = f"{base}/.well-known/genid/{blank_id}"

    # Generate UUIDv5 from skolem IRI
    bnode_uuid = uri_to_uuid(skolem_iri)
    filename = f"{bnode_uuid}.md"
    filepath = output_dir / filename

    if filepath.exists():
        return bnode_uuid

    # Generate alias: _:genid-{short_id}
    alias = format_alias_value(f"_:genid-{blank_id}")

    content = f"""---
metadata: blank_node
uri: {skolem_iri}
aliases:
  - {alias}
---
"""
    write_file(filepath, content)
    return bnode_uuid


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


def canonicalize_triple(
    subject_uri: str,
    predicate_uri: str,
    object_value: str,
    is_literal: bool
) -> str:
    """
    Build canonical triple string for UUIDv5 generation.

    Format: {subject_uri}|{predicate_uri}|{object_canonical}

    For literals, object_value should already be in canonical form:
    - "value" for plain strings
    - "value"@lang for language-tagged
    - "value"^^<datatype_uri> for typed literals
    """
    return f"{subject_uri}|{predicate_uri}|{object_value}"


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
    object_canonical: Optional[str] = None
) -> None:
    """
    Create a statement file for an RDF triple.

    Filename format: {uuidv5}.md (UUIDv5 of canonical triple)

    All URIs are represented as wikilinks [[uuid]]. Missing target files are allowed.
    """
    # UUIDv5 for rdf:type (http://www.w3.org/1999/02/22-rdf-syntax-ns#type)
    RDF_TYPE_UUID = '73b69787-81ea-563e-8e09-9c84cad4cf2b'

    # Build canonical triple for UUID generation
    if is_literal:
        # Use the canonical literal form
        obj_for_canonical = object_canonical or obj_anchor_or_literal
    else:
        # For URI objects, use the URI
        obj_for_canonical = object_uri or obj_anchor_or_literal

    # Generate UUIDv5 from canonical triple
    canonical = canonicalize_triple(
        subject_uri or subject_anchor,
        predicate_uri or predicate_anchor,
        obj_for_canonical,
        is_literal
    )
    statement_uuid = uri_to_uuid(canonical)

    # Check for collision (shouldn't happen with proper canonical form)
    filename = f"{statement_uuid}.md"
    filepath = output_dir / filename

    if filepath.exists():
        # This is a duplicate triple - skip it
        return

    # Build YAML frontmatter - ALL URIs use wikilinks [[uuid]]
    # Subject
    subj_yaml = f'"[[{subject_anchor}]]"'

    # Predicate with optional alias for rdf:type
    if predicate_anchor == RDF_TYPE_UUID:
        pred_yaml = f'"[[{RDF_TYPE_UUID}|a]]"'
    else:
        pred_yaml = f'"[[{predicate_anchor}]]"'

    # Object
    if is_literal:
        # obj_anchor_or_literal is the YAML-formatted literal value
        obj_yaml = obj_anchor_or_literal
    else:
        obj_yaml = f'"[[{obj_anchor_or_literal}]]"'

    # Generate statement alias: subj_alias pred_alias obj_alias
    # Subject alias
    if subject_uri:
        prefix = extract_prefix_from_uri(subject_uri)
        if prefix:
            subj_alias = f"{prefix}:{extract_localname_from_uri(subject_uri)}"
        else:
            subj_alias = "?"
    else:
        subj_alias = "?"

    # Predicate alias
    if predicate_anchor == RDF_TYPE_UUID:
        pred_alias = "a"
    elif predicate_uri:
        prefix = extract_prefix_from_uri(predicate_uri)
        if prefix:
            pred_alias = f"{prefix}:{extract_localname_from_uri(predicate_uri)}"
        else:
            pred_alias = "?"
    else:
        pred_alias = "?"

    # Object alias
    if is_literal:
        # Extract literal value for alias (truncate if long)
        lit_match = re.match(r'^"?\\"(.+?)\\"', obj_anchor_or_literal)
        if lit_match:
            lit_val = lit_match.group(1)
            if len(lit_val) > 30:
                obj_alias = lit_val[:30] + "..."
            else:
                obj_alias = lit_val
        else:
            obj_alias = obj_anchor_or_literal[:30] if len(obj_anchor_or_literal) > 30 else obj_anchor_or_literal
    elif object_uri:
        prefix = extract_prefix_from_uri(object_uri)
        if prefix:
            obj_alias = f"{prefix}:{extract_localname_from_uri(object_uri)}"
        else:
            obj_alias = "?"
    else:
        obj_alias = "?"

    statement_alias = f"{subj_alias} {pred_alias} {obj_alias}"
    # Truncate if too long
    if len(statement_alias) > 100:
        statement_alias = statement_alias[:97] + "..."
    alias_yaml = format_alias_value(statement_alias)

    content = f"""---
metadata: statement
subject: {subj_yaml}
predicate: {pred_yaml}
object: {obj_yaml}
aliases:
  - {alias_yaml}
---
"""
    write_file(filepath, content)


def literal_to_canonical(lit: Literal) -> str:
    """
    Convert an RDF literal to canonical N-Triples-like form for UUIDv5 generation.

    Examples:
        Literal("hello") -> '"hello"'
        Literal("hello", lang="en") -> '"hello"@en'
        Literal("42", datatype=XSD.integer) -> '"42"^^http://www.w3.org/2001/XMLSchema#integer'
    """
    value = str(lit)

    # Normalize line endings
    value = value.replace('\r\n', '\n').replace('\r', '\n')

    # Escape for canonical form
    escaped = value.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\t', '\\t')

    if lit.language:
        return f'"{escaped}"@{lit.language}'
    elif lit.datatype:
        return f'"{escaped}"^^{str(lit.datatype)}'
    else:
        return f'"{escaped}"'


def import_ontology(
    input_file: Path,
    output_dir: Path,
    prefix: str,
    namespace_uri: Optional[str] = None,
    verbose: bool = False
) -> Tuple[int, int, int]:
    """
    Import an RDF ontology into file-based format.

    All files use UUIDv5 names:
    - Namespace: UUIDv5(namespace_uri)
    - Anchor: UUIDv5(resource_uri)
    - Blank node: UUIDv5(skolem_iri)
    - Statement: UUIDv5(canonical_triple)

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
    ontology_uri = None  # The actual owl:Ontology URI (may differ from namespace)
    if not namespace_uri:
        # Look for owl:Ontology or the most common namespace
        for s, p, o in g.triples((None, RDF.type, OWL.Ontology)):
            ontology_uri = str(s)  # Save original ontology URI
            namespace_uri = ontology_uri
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

    effective_ns = namespace_uri or f"http://example.org/{prefix}#"

    if verbose:
        print(f"Using namespace: {effective_ns}")
        if ontology_uri and ontology_uri != namespace_uri and ontology_uri != namespace_uri.rstrip('#/'):
            print(f"Ontology URI: {ontology_uri}")

    # Create namespace file and get its UUID
    ns_uuid = create_namespace_file(output_dir, prefix, effective_ns)

    # Build namespace UUID map for term_to_anchor
    namespace_uuid_map: Dict[str, str] = {effective_ns: ns_uuid}
    for ns_uri in NAMESPACE_URI_TO_PREFIX.keys():
        namespace_uuid_map[ns_uri] = uri_to_uuid(ns_uri)

    if verbose:
        print(f"Namespace UUID: {ns_uuid}")

    # If ontology URI differs from namespace (e.g., owl: vs owl#), create anchor for it
    ontology_anchor = None
    if ontology_uri and not ontology_uri.endswith('#') and not ontology_uri.endswith('/'):
        # Ontology URI like http://www.w3.org/2002/07/owl needs its own anchor
        ontology_anchor = uri_to_uuid(ontology_uri)

    # Track blank nodes
    # bnode_map stores: {bnode_id: (uuid_anchor, local_id)}
    bnode_map: Dict[str, Tuple[str, str]] = {}

    # Collect all anchors needed (uuid -> uri mapping for creating files with URI)
    anchors: Dict[str, str] = {}  # uuid -> uri
    blank_nodes: Dict[str, str] = {}  # uuid -> local_id

    def is_local_resource(uri_str: str) -> bool:
        """Check if a URI belongs to THIS ontology's namespace (not external)."""
        # Check if it belongs to the current ontology namespace
        if uri_str.startswith(effective_ns):
            return True
        # Check if it's the ontology URI itself (without # suffix)
        if ontology_uri and uri_str == ontology_uri:
            return True
        # All other URIs are external (belong to other namespaces)
        return False

    # First pass: identify all resources that need anchor files
    # IMPORTANT: Only create anchor files for resources in THIS namespace
    for s, p, o in g:
        # Subject
        if isinstance(s, URIRef):
            uri_str = str(s)
            if is_local_resource(uri_str):
                anchor, _ = term_to_anchor(s, prefix, effective_ns, bnode_map, None,
                                           ontology_uri, namespace_uuid_map)
                anchors[anchor] = uri_str
        elif isinstance(s, BNode):
            bn_uuid, bn_local = bnode_to_anchor(s, prefix, bnode_map, effective_ns)
            blank_nodes[bn_uuid] = bn_local

        # Predicate (always URIRef) - only create anchor if local
        if isinstance(p, URIRef):
            uri_str = str(p)
            if is_local_resource(uri_str):
                anchor, _ = term_to_anchor(p, prefix, effective_ns, bnode_map, None,
                                           ontology_uri, namespace_uuid_map)
                anchors[anchor] = uri_str

        # Object (if URI or BNode) - only create anchor if local
        if isinstance(o, URIRef):
            uri_str = str(o)
            if is_local_resource(uri_str):
                anchor, _ = term_to_anchor(o, prefix, effective_ns, bnode_map, None,
                                           ontology_uri, namespace_uuid_map)
                anchors[anchor] = uri_str
        elif isinstance(o, BNode):
            bn_uuid, bn_local = bnode_to_anchor(o, prefix, bnode_map, effective_ns)
            blank_nodes[bn_uuid] = bn_local

    # Remove namespace UUID from anchors (it's created separately)
    if ns_uuid in anchors:
        del anchors[ns_uuid]

    # Create anchor files with URIs
    if verbose:
        print(f"Creating {len(anchors)} anchor files...")
    for anchor_uuid, anchor_uri in anchors.items():
        create_anchor_file(output_dir, anchor_uuid, uri=anchor_uri)

    # Create ontology anchor if it differs from namespace
    if ontology_anchor and ontology_anchor not in anchors:
        if verbose:
            print(f"Creating ontology anchor: {ontology_anchor} for {ontology_uri}")
        create_anchor_file(output_dir, ontology_anchor, uri=ontology_uri)

    # Create blank node files
    if verbose:
        print(f"Creating {len(blank_nodes)} blank node files...")
    for bn_uuid, bn_local in blank_nodes.items():
        create_blank_node_file(output_dir, f"{prefix}!{bn_local}", effective_ns, bn_local)

    # Second pass: create statement files
    used_filenames: Dict[str, int] = {}
    triple_count = 0

    if verbose:
        print(f"Creating statement files...")

    for s, p, o in g:
        # IMPORTANT: Only create statements where subject belongs to THIS namespace
        # This prevents duplicate statements across ontologies
        if isinstance(s, URIRef):
            subj_uri = str(s)
            if not is_local_resource(subj_uri):
                # Skip statements about resources from other namespaces
                continue
        elif isinstance(s, BNode):
            # Blank nodes are always local to this ontology
            bn_uuid, bn_local = bnode_to_anchor(s, prefix, bnode_map, effective_ns)
            base = effective_ns.rstrip('#/')
            subj_uri = f"{base}/.well-known/genid/{bn_local}"
        else:
            subj_uri = None

        # Get subject anchor
        subj_anchor, _ = term_to_anchor(s, prefix, effective_ns, bnode_map, None,
                                        ontology_uri, namespace_uuid_map)

        # Get predicate anchor and URI
        pred_anchor, _ = term_to_anchor(p, prefix, effective_ns, bnode_map, None,
                                        ontology_uri, namespace_uuid_map)
        pred_uri = str(p) if isinstance(p, URIRef) else None

        # Handle object
        if isinstance(o, Literal):
            # Get canonical literal for UUID generation
            obj_canonical = literal_to_canonical(o)

            obj_str = str(o)
            # Normalize CRLF to LF before escaping
            obj_str = obj_str.replace('\r\n', '\n').replace('\r', '\n')
            # Check for multiline/special characters - always use escaped string for frontmatter
            if '\n' in obj_str or '\t' in obj_str:
                # Escape special characters for YAML double-quoted string
                escaped = obj_str.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\t', '\\t')
                if o.language:
                    obj_yaml = f'"\\"{escaped}\\"@{o.language}"'
                elif o.datatype:
                    dtype_str = str(o.datatype)
                    dtype_uuid = uri_to_uuid(dtype_str)
                    obj_yaml = f'"\\"{escaped}\\"^^[[{dtype_uuid}]]"'
                else:
                    obj_yaml = f'"\\"{escaped}\\""'
            else:
                obj_yaml = literal_to_yaml(o)

            create_statement_file(
                output_dir, subj_anchor, pred_anchor, obj_yaml,
                is_literal=True, used_filenames=used_filenames,
                subject_uri=subj_uri, predicate_uri=pred_uri,
                object_canonical=obj_canonical
            )
        else:
            obj_anchor, _ = term_to_anchor(o, prefix, effective_ns, bnode_map, None,
                                           ontology_uri, namespace_uuid_map)
            if isinstance(o, URIRef):
                obj_uri = str(o)
            elif isinstance(o, BNode):
                bn_uuid, bn_local = bnode_to_anchor(o, prefix, bnode_map, effective_ns)
                base = effective_ns.rstrip('#/')
                obj_uri = f"{base}/.well-known/genid/{bn_local}"
            else:
                obj_uri = None

            create_statement_file(
                output_dir, subj_anchor, pred_anchor, obj_anchor,
                is_literal=False, used_filenames=used_filenames,
                subject_uri=subj_uri, predicate_uri=pred_uri, object_uri=obj_uri
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

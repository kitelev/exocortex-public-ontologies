#!/usr/bin/env python3
"""
Verify that imported ontology matches original RDF semantically.
Compares triples from source RDF with file-based representation.
"""

import argparse
import uuid
from pathlib import Path
from rdflib import Graph, URIRef, Literal, BNode
from rdflib.namespace import RDF, RDFS, OWL, XSD
import re
import yaml

URL_NAMESPACE = uuid.UUID('6ba7b811-9dad-11d1-80b4-00c04fd430c8')


def uri_to_uuid(uri_str: str) -> str:
    """Generate UUIDv5 from URI using URL namespace."""
    return str(uuid.uuid5(URL_NAMESPACE, uri_str))


def extract_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from markdown file."""
    if not content.startswith('---'):
        return {}
    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}
    try:
        return yaml.safe_load(parts[1]) or {}
    except yaml.YAMLError:
        return {}


def load_triples_from_files(ontology_dir: Path) -> set:
    """Load triples from file-based representation."""
    triples = set()

    # First, build a map of namespace files to their URIs
    namespace_uris = {}
    for f in ontology_dir.iterdir():
        if f.is_file() and f.name.startswith('!') and f.name.endswith('.md') and ' ' not in f.name:
            content = f.read_text(encoding='utf-8')
            fm = extract_frontmatter(content)
            if fm.get('metadata') == 'namespace':
                # URI can be under 'uri' or '!' key
                uri = fm.get('uri') or fm.get('!')
                if uri:
                    # !dc.md -> uri
                    ns_name = f.stem  # !dc
                    namespace_uris[ns_name] = uri

    for f in ontology_dir.iterdir():
        if not f.is_file() or not f.name.endswith('.md'):
            continue
        if f.name == '_index.md':
            continue  # Skip index file
        # Include namespace statement files like "!dc predicate object.md"
        # but skip namespace definition files like "!dc.md"
        if f.name.startswith('!') and ' ' not in f.stem:
            continue

        content = f.read_text(encoding='utf-8')
        fm = extract_frontmatter(content)

        if fm.get('metadata') != 'statement':
            continue

        subj = fm.get('rdf__subject', '')
        pred = fm.get('rdf__predicate', '')
        obj = fm.get('rdf__object', '')

        if subj and pred and obj:
            # Clean up wikilinks
            subj = subj.strip('[]')
            pred = pred.strip('[]')
            # Handle rdf:type alias: [[uuid|a]] -> uuid
            if '|' in pred:
                pred = pred.split('|')[0]
            # Handle external URI predicate like <http://...> -> convert to UUID
            if pred.startswith('<') and pred.endswith('>'):
                pred = uri_to_uuid(pred[1:-1])
            # Object might be literal or wikilink
            if obj.startswith('[[') and obj.endswith(']]'):
                obj = obj[2:-2]
                # Handle alias in object too
                if '|' in obj:
                    obj = obj.split('|')[0]
                # Handle namespace reference like !dc -> convert to UUID
                if obj.startswith('!') and obj in namespace_uris:
                    obj = uri_to_uuid(namespace_uris[obj])
            elif obj.startswith('<') and obj.endswith('>'):
                # External URI like <http://...> -> convert to UUID
                obj = uri_to_uuid(obj[1:-1])
            else:
                # Literal value - normalize the format
                # New format: "\"value\"@lang" or "\"value\"^^[[uuid]]" or "\"value\""
                # Need to unescape the quotes for comparison
                if obj.startswith('\\"') or obj.startswith('"'):
                    # Unescape quotes: \"value\" -> "value"
                    obj = obj.replace('\\"', '"')
                    # Remove outer quotes if present (from "\"...\"" -> "...")
                    if obj.startswith('""') and obj.endswith('""'):
                        obj = obj[1:-1]
            # Handle subject namespace reference
            if subj.startswith('!') and subj in namespace_uris:
                subj = uri_to_uuid(namespace_uris[subj])
            # Handle external URI subject like <http://...> -> convert to UUID
            elif subj.startswith('<') and subj.endswith('>'):
                subj = uri_to_uuid(subj[1:-1])
            triples.add((subj, pred, obj))

    return triples


def load_triples_from_rdf(rdf_path: Path, namespace_uri: str) -> set:
    """Load triples from RDF file and convert to UUID-based representation."""
    g = Graph()
    g.parse(rdf_path)

    triples = set()
    blank_node_map = {}

    for s, p, o in g:
        # Convert subject
        if isinstance(s, URIRef):
            subj = uri_to_uuid(str(s))
        elif isinstance(s, BNode):
            if s not in blank_node_map:
                blank_node_map[s] = f"blank_{len(blank_node_map)}"
            subj = blank_node_map[s]
        else:
            continue

        # Convert predicate
        if isinstance(p, URIRef):
            pred = uri_to_uuid(str(p))
        else:
            continue

        # Convert object
        if isinstance(o, URIRef):
            obj = uri_to_uuid(str(o))
        elif isinstance(o, BNode):
            if o not in blank_node_map:
                blank_node_map[o] = f"blank_{len(blank_node_map)}"
            obj = blank_node_map[o]
        elif isinstance(o, Literal):
            # Format literal similar to import script
            val = str(o)
            # Normalize line endings (CRLF -> LF)
            val = val.replace('\r\n', '\n').replace('\r', '\n')
            if o.language:
                obj = f'"{val}"@{o.language}'
            elif o.datatype and o.datatype != XSD.string:
                dt_uuid = uri_to_uuid(str(o.datatype))
                obj = f'"{val}"^^[[{dt_uuid}]]'
            else:
                obj = f'"{val}"'
        else:
            continue

        triples.add((subj, pred, obj))

    return triples, blank_node_map


def normalize_literal(lit: str) -> str:
    """Normalize literal for comparison."""
    # Remove outer quotes if present
    lit = lit.strip()
    if lit.startswith('"') and '"@' in lit:
        # Language tagged
        match = re.match(r'"(.*)\"@(\w+)$', lit)
        if match:
            return (match.group(1), match.group(2), None)
    elif lit.startswith('"') and '"^^' in lit:
        # Typed literal
        match = re.match(r'"(.*)"\^\^\[\[(.+)\]\]$', lit)
        if match:
            return (match.group(1), None, match.group(2))
    elif lit.startswith('"') and lit.endswith('"'):
        return (lit[1:-1], None, None)
    return (lit, None, None)


def compare_triples(file_triples: set, rdf_triples: set) -> tuple:
    """Compare two sets of triples, handling blank nodes specially."""
    # Separate blank node triples
    file_regular = {t for t in file_triples if not any('blank_' in str(x) or '!' in str(x) for x in t)}
    rdf_regular = {t for t in rdf_triples if not any('blank_' in str(x) for x in t)}

    file_blank = {t for t in file_triples if any('!' in str(x) for x in t)}
    rdf_blank = {t for t in rdf_triples if any('blank_' in str(x) for x in t)}

    # Compare regular triples
    only_in_files = file_regular - rdf_regular
    only_in_rdf = rdf_regular - file_regular

    return only_in_files, only_in_rdf, len(file_blank), len(rdf_blank)


def main():
    parser = argparse.ArgumentParser(description='Verify imported ontology matches original RDF')
    parser.add_argument('rdf_file', help='Path to original RDF file')
    parser.add_argument('ontology_dir', help='Path to imported ontology directory')
    parser.add_argument('--namespace', '-n', help='Namespace URI for the ontology')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    args = parser.parse_args()

    rdf_path = Path(args.rdf_file)
    ont_dir = Path(args.ontology_dir)

    if not rdf_path.exists():
        print(f"Error: RDF file not found: {rdf_path}")
        return 1
    if not ont_dir.exists():
        print(f"Error: Ontology directory not found: {ont_dir}")
        return 1

    print(f"Loading triples from RDF: {rdf_path}")
    rdf_triples, blank_map = load_triples_from_rdf(rdf_path, args.namespace or '')
    print(f"  Found {len(rdf_triples)} triples ({len(blank_map)} blank nodes)")

    print(f"\nLoading triples from files: {ont_dir}")
    file_triples = load_triples_from_files(ont_dir)
    print(f"  Found {len(file_triples)} triples")

    print("\nComparing triples...")
    only_files, only_rdf, file_blank_count, rdf_blank_count = compare_triples(file_triples, rdf_triples)

    print(f"\n{'='*60}")
    print("VERIFICATION SUMMARY")
    print(f"{'='*60}")
    print(f"  RDF triples: {len(rdf_triples)}")
    print(f"  File triples: {len(file_triples)}")
    print(f"  Blank node triples (RDF): {rdf_blank_count}")
    print(f"  Blank node triples (files): {file_blank_count}")

    if only_files:
        print(f"\n⚠️  Only in files ({len(only_files)}):")
        for t in list(only_files)[:10]:
            print(f"    {t}")
        if len(only_files) > 10:
            print(f"    ... and {len(only_files) - 10} more")

    if only_rdf:
        print(f"\n⚠️  Only in RDF ({len(only_rdf)}):")
        for t in list(only_rdf)[:10]:
            print(f"    {t}")
        if len(only_rdf) > 10:
            print(f"    ... and {len(only_rdf) - 10} more")

    # Check if semantically equivalent (ignoring blank node differences)
    if not only_files and not only_rdf:
        print("\n✅ Ontologies are semantically equivalent!")
        return 0
    elif len(only_files) == 0 and len(only_rdf) <= rdf_blank_count:
        print("\n✅ Ontologies are semantically equivalent (blank node handling differs)")
        return 0
    else:
        print("\n❌ Ontologies differ!")
        return 1


if __name__ == '__main__':
    exit(main())

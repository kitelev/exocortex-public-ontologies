#!/usr/bin/env python3
"""
Add URI field to anchor frontmatter and generate _index.md files.

This script:
1. Adds 'uri' field to all anchor files based on namespace metadata
2. Generates _index.md with UUID → label mapping for each ontology
"""

import os
import re
import sys
from pathlib import Path
from collections import defaultdict

# Namespace URI prefixes
NAMESPACE_URIS = {
    'dc': 'http://purl.org/dc/elements/1.1/',
    'dcam': 'http://purl.org/dc/dcam/',
    'dcterms': 'http://purl.org/dc/terms/',
    'doap': 'http://usefulinc.com/ns/doap#',
    'foaf': 'http://xmlns.com/foaf/0.1/',
    'geo': 'http://www.w3.org/2003/01/geo/wgs84_pos#',
    'owl': 'http://www.w3.org/2002/07/owl#',
    'prov': 'http://www.w3.org/ns/prov#',
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
    'sioc': 'http://rdfs.org/sioc/ns#',
    'skos': 'http://www.w3.org/2004/02/skos/core#',
    'time': 'http://www.w3.org/2006/time#',
    'vcard': 'http://www.w3.org/2006/vcard/ns#',
    'xsd': 'http://www.w3.org/2001/XMLSchema#',
}

# UUID regex pattern
UUID_PATTERN = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$')


def extract_frontmatter(content: str) -> tuple[dict, str]:
    """Extract frontmatter and body from markdown content."""
    if not content.startswith('---'):
        return {}, content

    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}, content

    frontmatter = {}
    for line in parts[1].strip().split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            frontmatter[key.strip()] = value.strip()

    return frontmatter, '---' + parts[1] + '---' + parts[2]


def find_uri_from_statements(ontology_dir: Path, anchor_uuid: str) -> str | None:
    """
    Find URI by looking at rdfs:label statements for this anchor.
    Statement format: {subject_uuid} {predicate_uuid} ___.md
    The rdfs:label predicate UUID is: 3e98087c-7fe5-5523-b25a-b83b0f6bbd8c
    """
    # We can't directly find URI from statements
    # Need to use reverse lookup from namespace file
    return None


def extract_label_from_statements(ontology_dir: Path, anchor_uuid: str) -> str | None:
    """
    Extract rdfs:label from statement files.
    rdfs:label UUID is d0e9e696-d3f2-5966-a62f-d8358cbde741
    """
    rdfs_label_uuid = 'd0e9e696-d3f2-5966-a62f-d8358cbde741'

    for f in ontology_dir.iterdir():
        if not f.is_file() or not f.name.endswith('.md'):
            continue

        # Check if this is a statement with our anchor as subject and rdfs:label as predicate
        parts = f.stem.split(' ')
        if len(parts) >= 2 and parts[0] == anchor_uuid and parts[1] == rdfs_label_uuid:
            # Read the file to get the label value
            content = f.read_text(encoding='utf-8')
            fm, _ = extract_frontmatter(content)
            if 'rdf__object' in fm:
                obj = fm['rdf__object']
                # Parse literal: "value"@lang or "value"^^type
                # YAML may wrap in single quotes: '"value"@en' -> 'value'
                match = re.search(r'"([^"]*)"', obj)
                if match:
                    return match.group(1)

    return None


def get_uri_from_namespace(namespace_file: Path, anchor_uuid: str) -> str | None:
    """
    Try to reconstruct URI from namespace prefix.
    Since we use UUIDv5 with URL namespace, we can't reverse it.
    We need to use the label or other heuristics.
    """
    return None


def process_ontology(ontology_dir: Path, namespace: str, dry_run: bool = False, verbose: bool = False) -> dict:
    """
    Process a single ontology directory.
    Returns mapping of UUID → (uri, label) for index generation.
    """
    if namespace not in NAMESPACE_URIS:
        if verbose:
            print(f"  Skipping {namespace}: unknown namespace")
        return {}

    base_uri = NAMESPACE_URIS[namespace]
    index_data = {}
    modified_count = 0

    # First pass: collect all anchors
    anchors = []
    for f in ontology_dir.iterdir():
        if not f.is_file() or not f.name.endswith('.md'):
            continue
        if f.name.startswith('!') or f.name.startswith('_'):
            continue

        # Check if it's an anchor file (UUID format, no spaces)
        stem = f.stem
        if ' ' in stem:
            continue
        if not UUID_PATTERN.match(stem):
            continue

        content = f.read_text(encoding='utf-8')
        fm, _ = extract_frontmatter(content)
        if fm.get('metadata') == 'anchor':
            anchors.append((f, stem))

    if verbose:
        print(f"  Found {len(anchors)} anchor files")

    # Second pass: process each anchor
    for anchor_file, anchor_uuid in anchors:
        content = anchor_file.read_text(encoding='utf-8')

        # Extract label from statements
        label = extract_label_from_statements(ontology_dir, anchor_uuid)

        # Try to find the local name by checking if the anchor has a label
        # that matches a known pattern
        uri = None
        if label:
            # Construct URI from label (assuming it's the local name)
            # This is a heuristic and may not always be correct
            local_name = label
            uri = base_uri + local_name

        # Check if URI field already exists
        if 'uri:' in content:
            # Extract existing URI
            match = re.search(r'^uri:\s*(.+)$', content, re.MULTILINE)
            if match:
                uri = match.group(1).strip()
        elif uri:
            # Add URI to frontmatter
            new_content = content.replace(
                'metadata: anchor',
                f'metadata: anchor\nuri: {uri}'
            )
            if not dry_run:
                anchor_file.write_text(new_content, encoding='utf-8')
            modified_count += 1
            if verbose:
                print(f"    Added URI to {anchor_uuid[:8]}...: {uri}")

        # Store for index
        if label or uri:
            index_data[anchor_uuid] = {
                'label': label,
                'uri': uri
            }

    if verbose:
        print(f"  Modified {modified_count} anchor files")

    return index_data


def generate_index(ontology_dir: Path, namespace: str, index_data: dict, dry_run: bool = False) -> None:
    """Generate _index.md file with UUID → label/uri mapping."""
    if not index_data:
        return

    lines = [
        '---',
        'metadata: index',
        '---',
        '',
        f'# {namespace.upper()} Index',
        '',
        'UUID → Label mapping for human-readable lookup.',
        '',
        '| UUID | Label | URI |',
        '|------|-------|-----|',
    ]

    for uuid, data in sorted(index_data.items(), key=lambda x: x[1].get('label') or ''):
        label = data.get('label') or ''
        uri = data.get('uri') or ''
        lines.append(f'| `{uuid[:8]}...` | {label} | {uri} |')

    lines.append('')

    index_path = ontology_dir / '_index.md'
    if not dry_run:
        index_path.write_text('\n'.join(lines), encoding='utf-8')
    print(f"  Generated {index_path.name} with {len(index_data)} entries")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Add URI to anchors and generate index files')
    parser.add_argument('path', nargs='?', default='.', help='Path to ontologies root')
    parser.add_argument('--dry-run', '-n', action='store_true', help='Do not modify files')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    args = parser.parse_args()

    root = Path(args.path).resolve()
    if not root.is_dir():
        print(f"Error: {root} is not a directory")
        sys.exit(1)

    print(f"Processing ontologies in {root}")

    # Process each ontology directory
    for d in sorted(root.iterdir()):
        if not d.is_dir():
            continue
        if d.name.startswith('.') or d.name in ('scripts', 'originals', 'exports', '~templates'):
            continue

        namespace = d.name
        print(f"\nProcessing {namespace}/")

        index_data = process_ontology(d, namespace, args.dry_run, args.verbose)
        generate_index(d, namespace, index_data, args.dry_run)

    print("\nDone!")


if __name__ == '__main__':
    main()

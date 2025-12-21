#!/usr/bin/env python3
"""
Migrate file-based ontology files to UUIDv5 naming.

This script:
1. Renames anchor files (dc__contributor.md -> {uuid}.md)
2. Renames statement files similarly
3. Updates all wikilinks in all files to use new names

UUIDv5 is generated from the full URI using the URL namespace.

Usage:
    python scripts/migrate_to_uuid.py <ontology_dir> [--dry-run]

Examples:
    python scripts/migrate_to_uuid.py dc --dry-run
    python scripts/migrate_to_uuid.py dc
    python scripts/migrate_to_uuid.py .  # All ontologies
"""

import argparse
import re
import sys
import uuid
from pathlib import Path
from typing import Dict, Optional, Tuple
import yaml

# URL namespace for UUIDv5
UUID_NAMESPACE = uuid.UUID('6ba7b811-9dad-11d1-80b4-00c04fd430c8')

# Known namespace URIs and their prefixes
KNOWN_NAMESPACES = {
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
    'owl': 'http://www.w3.org/2002/07/owl#',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'dcterms': 'http://purl.org/dc/terms/',
    'dcam': 'http://purl.org/dc/dcam/',
    'skos': 'http://www.w3.org/2004/02/skos/core#',
    'foaf': 'http://xmlns.com/foaf/0.1/',
    'prov': 'http://www.w3.org/ns/prov#',
    'prov_o': 'http://www.w3.org/ns/prov-o#',
    'time': 'http://www.w3.org/2006/time#',
    'geo': 'http://www.w3.org/2003/01/geo/wgs84_pos#',
    'vcard': 'http://www.w3.org/2006/vcard/ns#',
    'doap': 'http://usefulinc.com/ns/doap#',
    'sioc': 'http://rdfs.org/sioc/ns#',
    'xsd': 'http://www.w3.org/2001/XMLSchema#',
}


def unescape_case(name: str) -> str:
    """Remove dots before uppercase letters.

    Example: '.Month.Of.Year' -> 'MonthOfYear'
    """
    return re.sub(r'\.([A-Z])', r'\1', name)


def anchor_to_uri(anchor: str, ontology_namespaces: Dict[str, str]) -> Optional[str]:
    """
    Convert an anchor name to full URI.

    Examples:
        'rdf__type' -> 'http://www.w3.org/1999/02/22-rdf-syntax-ns#type'
        'dc__contributor' -> 'http://purl.org/dc/elements/1.1/contributor'
        'time__.Month.Of.Year' -> 'http://www.w3.org/2006/time#MonthOfYear'
        '!dc' -> 'http://purl.org/dc/elements/1.1/'
        'time!00000000' -> None (blank node)
    """
    # Namespace reference (e.g., !dc)
    if anchor.startswith('!'):
        prefix = anchor[1:]
        ns_uri = ontology_namespaces.get(prefix) or KNOWN_NAMESPACES.get(prefix)
        if ns_uri:
            return ns_uri.rstrip('#/')
        return None

    # Blank node (e.g., time!00000000)
    if '!' in anchor and not anchor.startswith('!'):
        return None  # Blank nodes don't have URIs

    # Regular anchor (e.g., rdf__type, dc__contributor)
    if '__' not in anchor:
        return None

    prefix, local = anchor.split('__', 1)

    # Unescape case-escaping (e.g., .Month.Of.Year -> MonthOfYear)
    local = unescape_case(local)

    # Find namespace URI
    ns_uri = ontology_namespaces.get(prefix) or KNOWN_NAMESPACES.get(prefix)
    if not ns_uri:
        return None

    return ns_uri + local


def uri_to_uuid(uri: str) -> str:
    """Generate UUIDv5 from URI using URL namespace."""
    return str(uuid.uuid5(UUID_NAMESPACE, uri))


def load_namespace_file(filepath: Path) -> Optional[Tuple[str, str]]:
    """Load namespace from a !prefix.md file.

    Returns: (prefix, namespace_uri) or None
    """
    content = filepath.read_text(encoding='utf-8')

    # Parse YAML frontmatter
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return None

    try:
        frontmatter = yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return None

    if frontmatter.get('metadata') != 'namespace':
        return None

    ns_uri = frontmatter.get('!')
    if not ns_uri:
        return None

    # Extract prefix from filename (!dc.md -> dc)
    prefix = filepath.stem[1:]

    return prefix, ns_uri


def collect_ontology_namespaces(root_dir: Path) -> Dict[str, str]:
    """Collect all namespace mappings from all ontology directories."""
    namespaces = dict(KNOWN_NAMESPACES)

    for ns_file in root_dir.rglob('!*.md'):
        result = load_namespace_file(ns_file)
        if result:
            prefix, uri = result
            namespaces[prefix] = uri

    return namespaces


def parse_frontmatter(content: str) -> Optional[dict]:
    """Parse YAML frontmatter from file content."""
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return None

    try:
        return yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return None


def extract_wikilinks(text: str) -> list:
    """Extract all wikilinks from text.

    Returns list of (full_match, anchor, alias) tuples.
    Alias is None if not present.
    """
    # Pattern: [[anchor]] or [[anchor|alias]]
    pattern = r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]'
    matches = []
    for m in re.finditer(pattern, text):
        matches.append((m.group(0), m.group(1), m.group(2)))
    return matches


def build_rename_map(
    root_dir: Path,
    namespaces: Dict[str, str],
    dry_run: bool = False
) -> Dict[str, str]:
    """Build mapping from old anchor names to new UUIDv5 names.

    Returns: {old_anchor: new_uuid_name}
    """
    rename_map = {}

    for md_file in root_dir.rglob('*.md'):
        # Skip namespace files (!prefix.md)
        if md_file.stem.startswith('!'):
            continue

        content = md_file.read_text(encoding='utf-8')
        frontmatter = parse_frontmatter(content)

        if not frontmatter:
            continue

        metadata_type = frontmatter.get('metadata')

        if metadata_type == 'anchor':
            # This is an anchor file - its name is the anchor
            old_anchor = md_file.stem
            uri = anchor_to_uri(old_anchor, namespaces)
            if uri:
                new_name = uri_to_uuid(uri)
                rename_map[old_anchor] = new_name
                if dry_run:
                    print(f"  ANCHOR: {old_anchor} -> {new_name}")
                    print(f"          URI: {uri}")

        elif metadata_type == 'blank_node':
            # Blank nodes stay as-is (they have no URI)
            pass

    return rename_map


def rename_files_and_update_links(
    root_dir: Path,
    rename_map: Dict[str, str],
    dry_run: bool = False
) -> Tuple[int, int, int]:
    """Rename files and update wikilinks.

    Returns: (files_renamed, links_updated, files_with_updated_links)
    """
    files_renamed = 0
    links_updated = 0
    files_with_links_updated = 0

    # Collect all files first (to avoid issues with renaming during iteration)
    all_files = list(root_dir.rglob('*.md'))

    # First pass: update wikilinks in all files
    for md_file in all_files:
        content = md_file.read_text(encoding='utf-8')
        original_content = content

        # Find and replace wikilinks
        wikilinks = extract_wikilinks(content)

        for full_match, anchor, alias in wikilinks:
            if anchor in rename_map:
                new_anchor = rename_map[anchor]

                # Preserve alias if present
                if alias:
                    new_link = f'[[{new_anchor}|{alias}]]'
                else:
                    new_link = f'[[{new_anchor}]]'

                content = content.replace(full_match, new_link, 1)
                links_updated += 1

        if content != original_content:
            files_with_links_updated += 1
            if dry_run:
                print(f"  UPDATE LINKS: {md_file.relative_to(root_dir)}")
            else:
                md_file.write_text(content, encoding='utf-8')

    # Second pass: rename files
    # Need to re-collect files after potential content changes
    all_files = list(root_dir.rglob('*.md'))

    for md_file in all_files:
        # Skip namespace files
        if md_file.stem.startswith('!'):
            continue

        old_stem = md_file.stem
        new_stem = None

        # Check if this is an anchor file that needs renaming
        if old_stem in rename_map:
            new_stem = rename_map[old_stem]
        else:
            # Statement file: replace anchor references in filename
            # Format: "subject predicate object.md"
            parts = old_stem.split(' ')
            new_parts = []
            changed = False

            for part in parts:
                if part in rename_map:
                    new_parts.append(rename_map[part])
                    changed = True
                else:
                    new_parts.append(part)

            if changed:
                new_stem = ' '.join(new_parts)

        if new_stem and new_stem != old_stem:
            new_path = md_file.parent / f"{new_stem}.md"

            if dry_run:
                print(f"  RENAME: {old_stem}.md -> {new_stem}.md")
            else:
                md_file.rename(new_path)

            files_renamed += 1

    return files_renamed, links_updated, files_with_links_updated


def main():
    parser = argparse.ArgumentParser(
        description='Migrate ontology files to UUIDv5 naming.'
    )
    parser.add_argument('directory', type=Path,
                        help='Ontology directory to migrate (or . for all)')
    parser.add_argument('--dry-run', '-n', action='store_true',
                        help='Show what would be done without making changes')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Verbose output')

    args = parser.parse_args()

    # Determine root directory
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent

    if args.directory == Path('.'):
        target_dir = repo_root
    else:
        target_dir = repo_root / args.directory
        if not target_dir.exists():
            # Try as absolute path
            target_dir = args.directory

    if not target_dir.exists():
        print(f"Error: Directory not found: {target_dir}")
        sys.exit(1)

    print(f"Migrating: {target_dir}")
    if args.dry_run:
        print("DRY RUN - no changes will be made\n")

    # Collect namespaces from all ontology directories
    print("Collecting namespaces...")
    namespaces = collect_ontology_namespaces(repo_root)
    print(f"Found {len(namespaces)} namespace mappings\n")

    # Build rename map
    print("Building rename map...")
    rename_map = build_rename_map(target_dir, namespaces, args.dry_run and args.verbose)
    print(f"Found {len(rename_map)} anchors to rename\n")

    if not rename_map:
        print("Nothing to migrate.")
        return

    # Rename files and update links
    print("Renaming files and updating links...")
    files_renamed, links_updated, files_with_links = rename_files_and_update_links(
        target_dir, rename_map, args.dry_run
    )

    print(f"\nSummary:")
    print(f"  Files renamed: {files_renamed}")
    print(f"  Links updated: {links_updated}")
    print(f"  Files with updated links: {files_with_links}")

    if args.dry_run:
        print("\nThis was a dry run. Run without --dry-run to apply changes.")


if __name__ == '__main__':
    main()

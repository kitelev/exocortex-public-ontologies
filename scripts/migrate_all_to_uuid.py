#!/usr/bin/env python3
"""
Migrate ALL file types to UUIDv5 naming.

This script converts:
1. Namespace files: !prefix.md → {uuid}.md (from namespace URI)
2. Statement files: {s} {p} {o}.md → {uuid}.md (from canonical triple)
3. Blank node files: prefix!id.md → {uuid}.md (from skolem IRI)

Anchors already use UUIDv5 and remain unchanged.

Usage:
    python scripts/migrate_all_to_uuid.py [--dry-run] [--verbose]
    python scripts/migrate_all_to_uuid.py dc --dry-run  # Single ontology

Examples:
    python scripts/migrate_all_to_uuid.py --dry-run -v
    python scripts/migrate_all_to_uuid.py
"""

import argparse
import re
import sys
import uuid
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set
import yaml

# URL namespace for UUIDv5 (standard RFC 4122)
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
    'time': 'http://www.w3.org/2006/time#',
    'geo': 'http://www.w3.org/2003/01/geo/wgs84_pos#',
    'vcard': 'http://www.w3.org/2006/vcard/ns#',
    'doap': 'http://usefulinc.com/ns/doap#',
    'sioc': 'http://rdfs.org/sioc/ns#',
    'xsd': 'http://www.w3.org/2001/XMLSchema#',
}

# UUID for rdf:type (for detecting 'a' shorthand)
RDF_TYPE_UUID = '73b69787-81ea-563e-8e09-9c84cad4cf2b'


def uri_to_uuid(uri: str) -> str:
    """Generate UUIDv5 from URI using URL namespace."""
    return str(uuid.uuid5(UUID_NAMESPACE, uri))


def is_valid_uuid(s: str) -> bool:
    """Check if string is a valid UUID."""
    try:
        uuid.UUID(s)
        return True
    except ValueError:
        return False


def parse_frontmatter(content: str) -> Optional[dict]:
    """Parse YAML frontmatter from file content."""
    match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
    if not match:
        return None
    try:
        return yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return None


def extract_wikilink(text: str) -> Optional[Tuple[str, Optional[str]]]:
    """Extract anchor and alias from wikilink text like [[anchor]] or [[anchor|alias]]."""
    match = re.match(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]', text)
    if match:
        return match.group(1), match.group(2)
    return None


def load_namespace_files(root_dir: Path) -> Dict[str, Tuple[str, Path]]:
    """Load all namespace files and return mapping prefix -> (uri, filepath)."""
    namespaces = {}

    for ns_file in root_dir.rglob('!*.md'):
        content = ns_file.read_text(encoding='utf-8')
        frontmatter = parse_frontmatter(content)

        if frontmatter and frontmatter.get('metadata') == 'namespace':
            ns_uri = frontmatter.get('!')
            if ns_uri:
                prefix = ns_file.stem[1:]  # Remove leading !
                namespaces[prefix] = (ns_uri, ns_file)

    return namespaces


def load_anchor_uris(root_dir: Path) -> Dict[str, str]:
    """Load all anchor files and return mapping uuid -> uri."""
    anchor_uris = {}

    for md_file in root_dir.rglob('*.md'):
        stem = md_file.stem

        # Skip non-anchor files
        if stem.startswith('!') or stem.startswith('_') or ' ' in stem or '!' in stem:
            continue

        if not is_valid_uuid(stem):
            continue

        content = md_file.read_text(encoding='utf-8')
        frontmatter = parse_frontmatter(content)

        if frontmatter and frontmatter.get('metadata') == 'anchor':
            uri = frontmatter.get('uri')
            if uri:
                anchor_uris[stem] = uri

    return anchor_uris


def canonicalize_literal(yaml_value: str) -> str:
    """
    Convert YAML literal value to canonical form for hashing.

    Input formats (from frontmatter):
        "\"value\""                    -> "value"
        "\"value\"@en"                 -> "value"@en
        "\"value\"^^[[uuid]]"          -> "value"^^<uri>

    Output: N-Triples-like canonical form
    """
    # Remove outer quotes if present
    if yaml_value.startswith('"') and yaml_value.endswith('"'):
        inner = yaml_value[1:-1]
    else:
        inner = yaml_value

    # Parse the literal
    # Escaped inner quotes: \"value\" or \"value\"@lang or \"value\"^^[[uuid]]

    # Check for datatype
    dt_match = re.match(r'^\\?"(.*)\\?"\^\^\[\[([^\]]+)\]\]$', inner)
    if dt_match:
        value = dt_match.group(1)
        dtype_ref = dt_match.group(2)
        # dtype_ref is either UUID or alias like uuid|alias
        if '|' in dtype_ref:
            dtype_ref = dtype_ref.split('|')[0]
        # We'll resolve UUID to URI later
        return f'"{value}"^^{dtype_ref}'

    # Check for language tag
    lang_match = re.match(r'^\\?"(.*)\\?"@(\w+(?:-\w+)*)$', inner)
    if lang_match:
        value = lang_match.group(1)
        lang = lang_match.group(2)
        return f'"{value}"@{lang}'

    # Plain literal
    plain_match = re.match(r'^\\?"(.*)\\?"$', inner)
    if plain_match:
        value = plain_match.group(1)
        return f'"{value}"'

    # Fallback: return as-is
    return yaml_value


def resolve_object_ref(obj_yaml: str, anchor_uris: Dict[str, str],
                       namespace_uris: Dict[str, str]) -> str:
    """
    Resolve object reference to canonical form.

    Returns:
        - Full URI for wikilinks: [[uuid]] -> http://...
        - Canonical literal: "value"@en
        - External URI: <http://...> -> http://...
        - Blank node ref: _:id
    """
    obj_yaml = obj_yaml.strip()

    # External URI: "<http://...>"
    if obj_yaml.startswith('"<') and obj_yaml.endswith('>"'):
        return obj_yaml[2:-2]  # Remove "< and >"

    # Wikilink: "[[uuid]]" or "[[uuid|alias]]"
    wikilink_match = re.match(r'^"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]"$', obj_yaml)
    if wikilink_match:
        ref = wikilink_match.group(1)

        # Namespace reference: !prefix
        if ref.startswith('!'):
            prefix = ref[1:]
            return namespace_uris.get(prefix, ref)

        # UUID reference
        if is_valid_uuid(ref):
            return anchor_uris.get(ref, ref)

        return ref

    # Literal
    return canonicalize_literal(obj_yaml)


def build_canonical_triple(
    subj_yaml: str,
    pred_yaml: str,
    obj_yaml: str,
    anchor_uris: Dict[str, str],
    namespace_uris: Dict[str, str]
) -> Optional[str]:
    """
    Build canonical triple string for UUIDv5 generation.

    Format: {subject_uri}|{predicate_uri}|{object_canonical}
    """
    # Resolve subject
    subj_match = re.match(r'^"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]"$', subj_yaml.strip())
    if not subj_match:
        # External URI
        ext_match = re.match(r'^"<(.+)>"$', subj_yaml.strip())
        if ext_match:
            subj_uri = ext_match.group(1)
        else:
            return None
    else:
        subj_ref = subj_match.group(1)
        if subj_ref.startswith('!'):
            subj_uri = namespace_uris.get(subj_ref[1:])
        else:
            subj_uri = anchor_uris.get(subj_ref)
        if not subj_uri:
            return None

    # Resolve predicate
    pred_match = re.match(r'^"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]"$', pred_yaml.strip())
    if not pred_match:
        ext_match = re.match(r'^"<(.+)>"$', pred_yaml.strip())
        if ext_match:
            pred_uri = ext_match.group(1)
        else:
            return None
    else:
        pred_ref = pred_match.group(1)
        if pred_ref.startswith('!'):
            pred_uri = namespace_uris.get(pred_ref[1:])
        else:
            pred_uri = anchor_uris.get(pred_ref)
        if not pred_uri:
            return None

    # Resolve object
    obj_canonical = resolve_object_ref(obj_yaml, anchor_uris, namespace_uris)

    # For typed literals, resolve datatype UUID to URI
    dt_match = re.match(r'^"(.+)"\^\^([a-f0-9-]{36})$', obj_canonical)
    if dt_match:
        value = dt_match.group(1)
        dtype_uuid = dt_match.group(2)
        dtype_uri = anchor_uris.get(dtype_uuid)
        if dtype_uri:
            obj_canonical = f'"{value}"^^{dtype_uri}'

    return f"{subj_uri}|{pred_uri}|{obj_canonical}"


def build_skolem_iri(namespace_uri: str, blank_id: str) -> str:
    """
    Build skolem IRI for blank node.

    Format: {namespace}.well-known/genid/{blank_id}
    """
    # Remove trailing # or / from namespace
    base = namespace_uri.rstrip('#/')
    return f"{base}/.well-known/genid/{blank_id}"


class MigrationPlan:
    """Holds the migration plan: what to rename and how."""

    def __init__(self):
        # Mapping: old_filename (without .md) -> new_uuid
        self.file_renames: Dict[str, str] = {}

        # Mapping: old_wikilink_ref -> new_uuid (for updating links)
        self.link_updates: Dict[str, str] = {}

        # Files that need content updates
        self.content_updates: Set[Path] = set()

        # Errors encountered
        self.errors: List[str] = []


def plan_namespace_migration(
    namespaces: Dict[str, Tuple[str, Path]],
    plan: MigrationPlan,
    verbose: bool = False
) -> None:
    """Plan migration of namespace files."""
    for prefix, (ns_uri, filepath) in namespaces.items():
        old_name = f"!{prefix}"
        new_uuid = uri_to_uuid(ns_uri)

        plan.file_renames[old_name] = new_uuid
        plan.link_updates[old_name] = new_uuid

        if verbose:
            print(f"  NAMESPACE: !{prefix} -> {new_uuid}")
            print(f"             URI: {ns_uri}")


def plan_blank_node_migration(
    root_dir: Path,
    namespace_uris: Dict[str, str],
    plan: MigrationPlan,
    verbose: bool = False
) -> None:
    """Plan migration of blank node files."""
    for md_file in root_dir.rglob('*.md'):
        stem = md_file.stem

        # Blank node pattern: prefix!hexid (not starting with !)
        if '!' in stem and not stem.startswith('!'):
            parts = stem.split('!')
            if len(parts) == 2:
                prefix, blank_id = parts

                # Get namespace URI for this prefix
                ns_uri = namespace_uris.get(prefix, KNOWN_NAMESPACES.get(prefix))
                if not ns_uri:
                    plan.errors.append(f"Unknown namespace for blank node: {stem}")
                    continue

                # Build skolem IRI
                skolem_iri = build_skolem_iri(ns_uri, blank_id)
                new_uuid = uri_to_uuid(skolem_iri)

                plan.file_renames[stem] = new_uuid
                plan.link_updates[stem] = new_uuid

                if verbose:
                    print(f"  BLANK NODE: {stem} -> {new_uuid}")
                    print(f"              Skolem: {skolem_iri}")


def plan_statement_migration(
    root_dir: Path,
    anchor_uris: Dict[str, str],
    namespace_uris: Dict[str, str],
    plan: MigrationPlan,
    verbose: bool = False
) -> None:
    """Plan migration of statement files."""
    for md_file in root_dir.rglob('*.md'):
        stem = md_file.stem

        # Skip non-statement files
        if stem.startswith('!') or stem.startswith('_'):
            continue

        # Statement files have spaces in name
        if ' ' not in stem:
            continue

        content = md_file.read_text(encoding='utf-8')
        frontmatter = parse_frontmatter(content)

        if not frontmatter or frontmatter.get('metadata') != 'statement':
            continue

        subj = frontmatter.get('rdf__subject', '')
        pred = frontmatter.get('rdf__predicate', '')
        obj = frontmatter.get('rdf__object', '')

        # Build canonical triple
        canonical = build_canonical_triple(subj, pred, obj, anchor_uris, namespace_uris)

        if not canonical:
            plan.errors.append(f"Could not canonicalize: {md_file.name}")
            continue

        new_uuid = uri_to_uuid(canonical)
        plan.file_renames[stem] = new_uuid

        if verbose:
            print(f"  STATEMENT: {stem[:60]}...")
            print(f"             -> {new_uuid}")
            print(f"             Canonical: {canonical[:80]}...")


def update_wikilinks_in_content(content: str, link_updates: Dict[str, str]) -> str:
    """Update all wikilinks in content using the link_updates mapping."""

    def replace_link(match):
        full_match = match.group(0)
        anchor = match.group(1)
        alias = match.group(2)

        if anchor in link_updates:
            new_anchor = link_updates[anchor]
            if alias:
                return f'[[{new_anchor}|{alias}]]'
            else:
                return f'[[{new_anchor}]]'
        return full_match

    # Pattern: [[anchor]] or [[anchor|alias]]
    pattern = r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]'
    return re.sub(pattern, replace_link, content)


def execute_migration(
    root_dir: Path,
    plan: MigrationPlan,
    dry_run: bool = False,
    verbose: bool = False
) -> Tuple[int, int, int]:
    """
    Execute the migration plan.

    Returns: (files_renamed, links_updated, files_modified)
    """
    files_renamed = 0
    links_updated = 0
    files_modified = 0

    # First pass: update wikilinks in all files
    all_files = list(root_dir.rglob('*.md'))

    for md_file in all_files:
        # Skip index files
        if md_file.stem == '_index':
            continue

        content = md_file.read_text(encoding='utf-8')
        new_content = update_wikilinks_in_content(content, plan.link_updates)

        if new_content != content:
            count = len(re.findall(r'\[\[', content)) - len(re.findall(r'\[\[', new_content))
            # Actually count replacements
            for old_ref in plan.link_updates:
                links_updated += content.count(f'[[{old_ref}]]')
                links_updated += content.count(f'[[{old_ref}|')

            files_modified += 1

            if verbose:
                print(f"  UPDATE LINKS: {md_file.relative_to(root_dir)}")

            if not dry_run:
                md_file.write_text(new_content, encoding='utf-8')

    # Second pass: rename files
    # Re-collect after content updates
    all_files = list(root_dir.rglob('*.md'))

    for md_file in all_files:
        stem = md_file.stem

        if stem in plan.file_renames:
            new_name = plan.file_renames[stem]
            new_path = md_file.parent / f"{new_name}.md"

            if verbose:
                print(f"  RENAME: {stem}.md -> {new_name}.md")

            if not dry_run:
                # Handle potential collision
                if new_path.exists() and new_path != md_file:
                    plan.errors.append(f"Collision: {new_path} already exists")
                    continue
                md_file.rename(new_path)

            files_renamed += 1

    return files_renamed, links_updated, files_modified


def regenerate_index(ontology_dir: Path, dry_run: bool = False) -> None:
    """Regenerate _index.md for the ontology directory."""
    index_path = ontology_dir / '_index.md'

    entries = []

    for md_file in ontology_dir.glob('*.md'):
        stem = md_file.stem

        # Skip special files
        if stem.startswith('_') or stem.startswith('~'):
            continue

        # Only process anchor files (single UUID, no spaces)
        if not is_valid_uuid(stem):
            continue

        content = md_file.read_text(encoding='utf-8')
        frontmatter = parse_frontmatter(content)

        if not frontmatter or frontmatter.get('metadata') != 'anchor':
            continue

        uri = frontmatter.get('uri', '')

        # Extract label from URI
        if '#' in uri:
            label = uri.rsplit('#', 1)[1]
        elif '/' in uri:
            label = uri.rsplit('/', 1)[1]
        else:
            label = uri

        entries.append((stem, label, uri))

    # Sort by label
    entries.sort(key=lambda x: x[1].lower())

    # Generate index content
    lines = [
        '# Index',
        '',
        '| UUID | Label | URI |',
        '|------|-------|-----|',
    ]

    for uuid_str, label, uri in entries:
        lines.append(f'| `{uuid_str}` | {label} | {uri} |')

    content = '\n'.join(lines) + '\n'

    if not dry_run:
        index_path.write_text(content, encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(
        description='Migrate ALL file types to UUIDv5 naming.'
    )
    parser.add_argument('ontology', type=str, nargs='?', default=None,
                        help='Specific ontology to migrate (e.g., dc, owl). Omit for all.')
    parser.add_argument('--dry-run', '-n', action='store_true',
                        help='Show what would be done without making changes')
    parser.add_argument('--verbose', '-v', action='store_true',
                        help='Verbose output')

    args = parser.parse_args()

    # Determine directories
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent

    if args.ontology:
        target_dirs = [repo_root / args.ontology]
        if not target_dirs[0].exists():
            print(f"Error: Ontology directory not found: {target_dirs[0]}")
            sys.exit(1)
    else:
        # All ontology directories (exclude scripts, templates, etc.)
        exclude = {'scripts', 'originals', 'exports', '.git', '.obsidian', '.idea', '~templates'}
        target_dirs = [d for d in repo_root.iterdir()
                      if d.is_dir() and d.name not in exclude and not d.name.startswith('.')]

    print(f"Migration targets: {[d.name for d in target_dirs]}")
    if args.dry_run:
        print("DRY RUN - no changes will be made\n")

    # Load all namespace mappings
    print("Loading namespaces...")
    namespaces = load_namespace_files(repo_root)
    namespace_uris = {prefix: uri for prefix, (uri, _) in namespaces.items()}
    # Add known namespaces
    namespace_uris.update(KNOWN_NAMESPACES)
    print(f"Found {len(namespaces)} namespace files\n")

    # Load all anchor URIs
    print("Loading anchor URIs...")
    anchor_uris = load_anchor_uris(repo_root)
    print(f"Found {len(anchor_uris)} anchors with URIs\n")

    # Build migration plan
    plan = MigrationPlan()

    print("Planning namespace migrations...")
    plan_namespace_migration(namespaces, plan, args.verbose)

    for target_dir in target_dirs:
        print(f"\nPlanning migrations for {target_dir.name}/...")

        print("  Planning blank node migrations...")
        plan_blank_node_migration(target_dir, namespace_uris, plan, args.verbose)

        print("  Planning statement migrations...")
        plan_statement_migration(target_dir, anchor_uris, namespace_uris, plan, args.verbose)

    print(f"\nMigration plan:")
    print(f"  Files to rename: {len(plan.file_renames)}")
    print(f"  Links to update: {len(plan.link_updates)}")

    if plan.errors:
        print(f"\nErrors ({len(plan.errors)}):")
        for err in plan.errors[:10]:
            print(f"  - {err}")
        if len(plan.errors) > 10:
            print(f"  ... and {len(plan.errors) - 10} more")

    if not plan.file_renames:
        print("\nNothing to migrate.")
        return

    # Execute migration
    print("\nExecuting migration...")
    files_renamed, links_updated, files_modified = execute_migration(
        repo_root, plan, args.dry_run, args.verbose
    )

    # Regenerate indices
    if not args.dry_run:
        print("\nRegenerating index files...")
        for target_dir in target_dirs:
            regenerate_index(target_dir, args.dry_run)

    print(f"\nSummary:")
    print(f"  Files renamed: {files_renamed}")
    print(f"  Links updated: {links_updated}")
    print(f"  Files modified: {files_modified}")

    if args.dry_run:
        print("\nThis was a dry run. Run without --dry-run to apply changes.")


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Unify frontmatter field names across all ontology files.

Changes:
1. Statement files: rdf__subject → subject, rdf__predicate → predicate, rdf__object → object
2. Namespace files: Remove '!' field (keep only 'uri')
3. Blank node files: skolem_iri → uri

Usage:
    python scripts/unify_frontmatter.py [--dry-run]
"""

import argparse
import yaml
from pathlib import Path

NAMESPACES = ['rdf', 'rdfs', 'owl', 'dc', 'dcterms', 'dcam', 'skos', 'foaf', 'prov', 'time', 'geo', 'vcard', 'doap', 'sioc', 'xsd']


def parse_frontmatter(content: str) -> tuple:
    """Parse YAML frontmatter and body from markdown content."""
    if not content.startswith('---'):
        return None, content

    # Find closing --- at the start of a line
    lines = content.split('\n')
    yaml_end = -1
    for i, line in enumerate(lines[1:], 1):  # Skip first ---
        if line.strip() == '---':
            yaml_end = i
            break

    if yaml_end == -1:
        return None, content

    yaml_content = '\n'.join(lines[1:yaml_end])
    body = '\n'.join(lines[yaml_end + 1:])

    try:
        fm = yaml.safe_load(yaml_content)
        return fm or {}, body
    except yaml.YAMLError:
        return None, content


def format_value(value) -> str:
    """Format a value for YAML output."""
    if not isinstance(value, str):
        return str(value)

    # Check if value needs quoting
    needs_quotes = (
        ':' in value or
        value.startswith('[') or
        value.startswith('{') or
        value.startswith('"') or
        value.startswith("'") or
        '\n' in value or
        value.startswith('#')
    )

    if needs_quotes:
        # Escape backslashes and quotes for proper YAML
        escaped = value.replace('\\', '\\\\').replace('"', '\\"')
        return f'"{escaped}"'
    else:
        return value


def format_frontmatter(fm: dict) -> str:
    """Format frontmatter as YAML with consistent ordering."""
    lines = ['---']

    # Define field order
    order = ['metadata', 'uri', 'subject', 'predicate', 'object']

    # Add fields in order
    for key in order:
        if key in fm:
            lines.append(f'{key}: {format_value(fm[key])}')

    # Add any remaining fields not in order
    for key, value in fm.items():
        if key not in order:
            lines.append(f'{key}: {format_value(value)}')

    lines.append('---')
    return '\n'.join(lines)


def migrate_statement(fm: dict) -> dict:
    """Migrate statement frontmatter fields."""
    new_fm = {'metadata': 'statement'}

    if 'rdf__subject' in fm:
        new_fm['subject'] = fm['rdf__subject']
    if 'rdf__predicate' in fm:
        new_fm['predicate'] = fm['rdf__predicate']
    if 'rdf__object' in fm:
        new_fm['object'] = fm['rdf__object']

    return new_fm


def migrate_namespace(fm: dict) -> dict:
    """Migrate namespace frontmatter fields (remove '!')."""
    new_fm = {'metadata': 'namespace'}

    if 'uri' in fm:
        new_fm['uri'] = fm['uri']
    elif '!' in fm:
        new_fm['uri'] = fm['!']

    return new_fm


def migrate_blank_node(fm: dict) -> dict:
    """Migrate blank_node frontmatter fields (skolem_iri → uri)."""
    new_fm = {'metadata': 'blank_node'}

    if 'skolem_iri' in fm:
        new_fm['uri'] = fm['skolem_iri']
    elif 'uri' in fm:
        new_fm['uri'] = fm['uri']

    return new_fm


def process_file(filepath: Path, dry_run: bool = False) -> tuple:
    """Process a single file. Returns (changed, error_msg)."""
    content = filepath.read_text()
    fm, body = parse_frontmatter(content)

    if fm is None:
        return False, "Could not parse frontmatter"

    metadata = fm.get('metadata')
    if not metadata:
        return False, None  # Skip files without metadata

    # Determine if migration needed and apply
    new_fm = None

    if metadata == 'statement':
        if 'rdf__subject' in fm:
            new_fm = migrate_statement(fm)
    elif metadata == 'namespace':
        if '!' in fm:
            new_fm = migrate_namespace(fm)
    elif metadata == 'blank_node':
        if 'skolem_iri' in fm:
            new_fm = migrate_blank_node(fm)

    if new_fm is None:
        return False, None  # No changes needed

    # Format new content
    new_content = format_frontmatter(new_fm) + body

    if not dry_run:
        filepath.write_text(new_content)

    return True, None


def main():
    parser = argparse.ArgumentParser(description='Unify frontmatter field names')
    parser.add_argument('--dry-run', action='store_true', help='Show changes without applying')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    args = parser.parse_args()

    print("=" * 60)
    print("Frontmatter Unification")
    print("=" * 60)

    if args.dry_run:
        print("DRY RUN - no files will be modified\n")

    stats = {
        'statement': 0,
        'namespace': 0,
        'blank_node': 0,
        'errors': 0
    }

    for ns in NAMESPACES:
        ns_dir = Path(ns)
        if not ns_dir.exists():
            continue

        for filepath in sorted(ns_dir.glob('*.md')):
            if filepath.name == '_index.md':
                continue

            changed, error = process_file(filepath, args.dry_run)

            if error:
                stats['errors'] += 1
                if args.verbose:
                    print(f"  ERROR: {filepath}: {error}")
            elif changed:
                # Determine type from content
                content = filepath.read_text()
                fm, _ = parse_frontmatter(content)
                if fm:
                    metadata = fm.get('metadata')
                    if metadata in stats:
                        stats[metadata] += 1
                    if args.verbose:
                        print(f"  MIGRATED: {filepath}")

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Statements migrated: {stats['statement']}")
    print(f"  Namespaces migrated: {stats['namespace']}")
    print(f"  Blank nodes migrated: {stats['blank_node']}")
    print(f"  Errors: {stats['errors']}")

    if args.dry_run:
        print("\nRun without --dry-run to apply changes.")


if __name__ == '__main__':
    main()

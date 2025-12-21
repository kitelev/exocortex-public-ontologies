#!/usr/bin/env python3
"""Migrate xsd namespace to UUIDv5 naming scheme."""

import uuid
import re
import yaml
from pathlib import Path

NAMESPACE_URL = uuid.UUID('6ba7b811-9dad-11d1-80b4-00c04fd430c8')
XSD_NAMESPACE_UUID = 'daa5bbf6-42d2-51df-846d-92846e956920'  # Generated for http://www.w3.org/2001/XMLSchema#

def generate_uuid5(name: str) -> str:
    """Generate UUIDv5 from name using URL namespace."""
    return str(uuid.uuid5(NAMESPACE_URL, name))

def extract_wikilink(value: str) -> str:
    """Extract UUID from wikilink like '[[uuid]]' or '[[!xsd]]'."""
    if not value:
        return ''
    match = re.search(r'\[\[([^\]]+)\]\]', value)
    if match:
        link = match.group(1)
        # Replace old namespace reference with new UUID
        if link == '!xsd':
            return XSD_NAMESPACE_UUID
        return link
    return value

def parse_frontmatter(content: str) -> tuple:
    """Parse YAML frontmatter and body from markdown content."""
    if not content.startswith('---'):
        return {}, content

    parts = content.split('---', 2)
    if len(parts) < 3:
        return {}, content

    try:
        fm = yaml.safe_load(parts[1])
        body = parts[2].strip()
        return fm or {}, body
    except yaml.YAMLError:
        return {}, content

def format_frontmatter(frontmatter: dict) -> str:
    """Format frontmatter as YAML."""
    lines = ['---']
    for key, value in frontmatter.items():
        if isinstance(value, str):
            if ':' in value or value.startswith('[') or value.startswith('{'):
                lines.append(f'{key}: "{value}"')
            else:
                lines.append(f'{key}: {value}')
        else:
            lines.append(f'{key}: {value}')
    lines.append('---')
    return '\n'.join(lines)

def get_file_type(frontmatter: dict) -> str:
    """Determine file type from frontmatter."""
    metadata = frontmatter.get('metadata', '')
    if metadata == 'namespace':
        return 'namespace'
    elif metadata == 'anchor':
        return 'anchor'
    elif metadata == 'blank_node':
        return 'blank_node'
    elif metadata == 'statement':
        return 'statement'
    return 'unknown'

def get_uuid_for_file(filepath: Path, frontmatter: dict, file_type: str) -> str:
    """Generate UUIDv5 for a file based on its type."""
    if file_type == 'namespace':
        ns_uri = frontmatter.get('!')
        if ns_uri:
            return generate_uuid5(ns_uri)

    elif file_type == 'anchor':
        uri = frontmatter.get('uri')
        if uri:
            return generate_uuid5(uri)

    elif file_type == 'statement':
        # Legacy format uses rdf__subject, rdf__predicate, rdf__object
        subject = extract_wikilink(frontmatter.get('rdf__subject', ''))
        predicate = extract_wikilink(frontmatter.get('rdf__predicate', ''))
        obj = extract_wikilink(frontmatter.get('rdf__object', ''))

        # Build canonical triple format
        canonical = f"{subject}|{predicate}|{obj}"
        return generate_uuid5(canonical)

    return None

def update_statement_links(frontmatter: dict) -> dict:
    """Update statement links to use new namespace UUID."""
    result = dict(frontmatter)
    for key in ['rdf__subject', 'rdf__predicate', 'rdf__object']:
        if key in result:
            value = result[key]
            if '[[!xsd]]' in value:
                result[key] = value.replace('[[!xsd]]', f'[[{XSD_NAMESPACE_UUID}]]')
    return result

def migrate_xsd():
    """Migrate all xsd files to UUID naming."""
    xsd_dir = Path('xsd')

    # Track renames
    renames = []
    updates = []

    for filepath in sorted(xsd_dir.glob('*.md')):
        filename = filepath.name

        # Skip files already with correct UUID name
        if re.match(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\.md$', filename):
            # Check if this is a statement that needs link updates
            content = filepath.read_text()
            fm, body = parse_frontmatter(content)
            if fm.get('metadata') == 'statement' and '[[!xsd]]' in content:
                updates.append((filepath, fm, body))
                print(f"UPDATE LINKS: {filename}")
            else:
                print(f"SKIP (already UUID): {filename}")
            continue

        # Skip index files
        if filename == '_index.md':
            print(f"SKIP (index): {filename}")
            continue

        content = filepath.read_text()
        frontmatter, body = parse_frontmatter(content)
        file_type = get_file_type(frontmatter)

        new_uuid = get_uuid_for_file(filepath, frontmatter, file_type)

        if new_uuid:
            new_path = xsd_dir / f"{new_uuid}.md"
            print(f"RENAME: {filename} -> {new_uuid}.md ({file_type})")
            renames.append((filepath, new_path, frontmatter, body))
        else:
            print(f"WARNING: Cannot determine UUID for {filename} (type={file_type})")
            print(f"  Frontmatter: {frontmatter}")

    # First, update links in existing UUID-named statement files
    print(f"\n=== Updating {len(updates)} statement links ===\n")
    for filepath, fm, body in updates:
        new_fm = update_statement_links(fm)
        new_content = format_frontmatter(new_fm) + '\n' + body if body else format_frontmatter(new_fm) + '\n'
        filepath.write_text(new_content)
        print(f"UPDATED: {filepath.name}")

    # Then, execute renames
    print(f"\n=== Executing {len(renames)} renames ===\n")
    for old_path, new_path, fm, body in renames:
        if new_path.exists():
            print(f"CONFLICT: {new_path.name} already exists, deleting old: {old_path.name}")
            old_path.unlink()
        else:
            # Update links in statement files before renaming
            if fm.get('metadata') == 'statement':
                new_fm = update_statement_links(fm)
                new_content = format_frontmatter(new_fm) + '\n' + body if body else format_frontmatter(new_fm) + '\n'
                old_path.write_text(new_content)
            old_path.rename(new_path)
            print(f"DONE: {old_path.name} -> {new_path.name}")

if __name__ == '__main__':
    migrate_xsd()

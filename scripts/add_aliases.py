#!/usr/bin/env python3
"""
Add human-readable aliases to all ontology files.

Alias formats:
- Anchor: prefix:localname (e.g., rdfs:Class)
- Namespace: !prefix (e.g., !rdf)
- Blank node: _:genid-{short_id} (e.g., _:genid-d3e1d976)
- Statement: {subj_alias} {pred_alias} {obj_alias}

Usage:
    python scripts/add_aliases.py [--dry-run]
"""

import argparse
import re
import yaml
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

# Namespace prefixes (short names for namespace URIs)
PREFIXES = [
    "rdf",
    "rdfs",
    "owl",
    "dc",
    "dcterms",
    "dcam",
    "skos",
    "foaf",
    "prov",
    "time",
    "geo",
    "vcard",
    "doap",
    "sioc",
    "xsd",
    "dcat",
    "org",
    "schema",
    "vs",
    "sh",
    "sosa",
    "as",
    "void",
    "geosparql",
]

# Namespace URI to prefix mapping (canonical)
NS_URI_TO_PREFIX = {
    "http://www.w3.org/1999/02/22-rdf-syntax-ns#": "rdf",
    "http://www.w3.org/2000/01/rdf-schema#": "rdfs",
    "http://www.w3.org/2002/07/owl#": "owl",
    "http://purl.org/dc/elements/1.1/": "dc",
    "http://purl.org/dc/terms/": "dcterms",
    "http://purl.org/dc/dcam/": "dcam",
    "http://www.w3.org/2004/02/skos/core#": "skos",
    "http://xmlns.com/foaf/0.1/": "foaf",
    "http://www.w3.org/ns/prov#": "prov",
    "http://www.w3.org/2006/time#": "time",
    "http://www.w3.org/2003/01/geo/wgs84_pos#": "geo",
    "http://www.w3.org/2006/vcard/ns#": "vcard",
    "http://usefulinc.com/ns/doap#": "doap",
    "http://rdfs.org/sioc/ns#": "sioc",
    "http://www.w3.org/2001/XMLSchema#": "xsd",
    "http://www.w3.org/ns/dcat#": "dcat",
    "http://www.w3.org/ns/org#": "org",
    "https://schema.org/": "schema",
    "http://www.w3.org/2003/06/sw-vocab-status/ns#": "vs",
    "http://www.w3.org/ns/shacl#": "sh",
    "http://www.w3.org/ns/sosa/": "sosa",
    "https://www.w3.org/ns/activitystreams#": "as",
    "http://rdfs.org/ns/void#": "void",
    "http://www.opengis.net/ont/geosparql#": "geosparql",
}

# Ontology URIs (without #) that map to the same prefix
# These are used when owl:Ontology URI differs from namespace URI
ONTOLOGY_URI_TO_PREFIX = {
    "http://www.w3.org/2002/07/owl": "owl",
    "http://www.w3.org/2004/02/skos/core": "skos",
    "http://www.w3.org/2006/time": "time",
    "http://www.w3.org/2006/vcard/ns": "vcard",
    "http://www.w3.org/ns/dcat": "dcat",
    "http://www.w3.org/ns/shacl": "sh",
    "http://www.w3.org/ns/sosa": "sosa",
    "https://www.w3.org/ns/activitystreams": "as",
}

# Maximum length for statement aliases
MAX_ALIAS_LENGTH = 100
MAX_LITERAL_LENGTH = 30


def extract_prefix_from_uri(uri: str) -> Optional[str]:
    """Extract the namespace prefix from a full URI."""
    if not uri:
        return None
    # Try each namespace URI
    for ns_uri, prefix in NS_URI_TO_PREFIX.items():
        if uri.startswith(ns_uri):
            return prefix
    # Try ontology URIs (exact match for ontology anchors)
    if uri in ONTOLOGY_URI_TO_PREFIX:
        return ONTOLOGY_URI_TO_PREFIX[uri]
    return None


def parse_frontmatter(content: str) -> Tuple[Optional[Dict[str, Any]], str]:
    """Parse YAML frontmatter and body from markdown content."""
    if not content.startswith("---"):
        return None, content

    lines = content.split("\n")
    yaml_end = -1
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == "---":
            yaml_end = i
            break

    if yaml_end == -1:
        return None, content

    yaml_content = "\n".join(lines[1:yaml_end])
    body = "\n".join(lines[yaml_end + 1 :])

    try:
        fm = yaml.safe_load(yaml_content)
        return fm or {}, body
    except yaml.YAMLError:
        return None, content


def format_value(value: Any) -> str:
    """Format a value for YAML output."""
    if not isinstance(value, str):
        return str(value)

    needs_quotes = (
        ":" in value
        or "?" in value  # YAML special character
        or value.startswith("[")
        or value.startswith("{")
        or value.startswith('"')
        or value.startswith("'")
        or value.startswith("!")
        or value.startswith("_:")
        or "\n" in value
        or value.startswith("#")
    )

    if needs_quotes:
        escaped = value.replace("\\", "\\\\").replace('"', '\\"')
        return f'"{escaped}"'
    else:
        return value


def format_frontmatter(fm: Dict[str, Any]) -> str:
    """Format frontmatter as YAML with consistent ordering."""
    lines = ["---"]

    # Define field order
    order = ["metadata", "uri", "subject", "predicate", "object", "aliases"]

    for key in order:
        if key in fm:
            value = fm[key]
            if key == "aliases" and isinstance(value, list):
                lines.append("aliases:")
                for alias in value:
                    lines.append(f"  - {format_value(alias)}")
            elif isinstance(value, str):
                lines.append(f"{key}: {format_value(value)}")
            else:
                lines.append(f"{key}: {value}")

    # Add any remaining fields not in order
    for key, value in fm.items():
        if key not in order:
            if isinstance(value, list):
                lines.append(f"{key}:")
                for item in value:
                    lines.append(f"  - {format_value(item)}")
            elif isinstance(value, str):
                lines.append(f"{key}: {format_value(value)}")
            else:
                lines.append(f"{key}: {value}")

    lines.append("---")
    return "\n".join(lines)


def extract_localname(uri: str) -> str:
    """Extract local name from URI."""
    if "#" in uri:
        return uri.split("#")[-1]
    elif "/" in uri:
        return uri.rstrip("/").split("/")[-1]
    return uri


def extract_wikilink_uuid(value: str) -> Optional[str]:
    """Extract UUID from wikilink like [[uuid]] or [[uuid|alias]]."""
    if not value:
        return None
    match = re.search(r"\[\[([^\]|]+)", value)
    if match:
        return match.group(1)
    return None


def is_literal(value: str) -> bool:
    """Check if value is a literal (starts with quote)."""
    if not value:
        return False
    # Literals start with " in our format
    stripped = value.strip()
    return stripped.startswith('"') and not stripped.startswith("[[")


def extract_literal_value(value: str) -> str:
    """Extract the literal value from YAML-encoded literal."""
    # Format is like: "\"value\"@en" or "\"value\"^^[[uuid]]"
    match = re.match(r'^"?\\"(.+?)\\"', value)
    if match:
        literal = match.group(1)
        # Truncate if too long
        if len(literal) > MAX_LITERAL_LENGTH:
            return literal[:MAX_LITERAL_LENGTH] + "..."
        return literal
    # Fallback: just return truncated value
    if len(value) > MAX_LITERAL_LENGTH:
        return value[:MAX_LITERAL_LENGTH] + "..."
    return value


def build_uuid_to_alias_map(repo_root: Path) -> Dict[str, str]:
    """Build mapping from UUID to human-readable alias.

    Uses canonical prefix from URI (not directory name) to ensure
    correct aliases even when files exist in multiple directories.
    """
    uuid_map = {}

    for ns in PREFIXES:
        ns_dir = repo_root / ns
        if not ns_dir.exists():
            continue

        for filepath in ns_dir.glob("*.md"):
            if filepath.name == "_index.md":
                continue

            content = filepath.read_text()
            fm, _ = parse_frontmatter(content)
            if not fm:
                continue

            metadata = fm.get("metadata")
            file_uuid = filepath.stem

            # Skip if already mapped (first occurrence wins)
            if file_uuid in uuid_map:
                continue

            if metadata == "anchor":
                uri = fm.get("uri", "")
                if uri:
                    # Extract prefix from URI, not from directory name
                    prefix = extract_prefix_from_uri(uri)
                    if prefix:
                        localname = extract_localname(uri)
                        uuid_map[file_uuid] = f"{prefix}:{localname}"

            elif metadata == "namespace":
                uri = fm.get("uri", "")
                if uri:
                    # Derive prefix from namespace URI
                    prefix = None
                    for ns_uri, p in NS_URI_TO_PREFIX.items():
                        if uri.rstrip("#/") == ns_uri.rstrip("#/"):
                            prefix = p
                            break
                    if prefix:
                        uuid_map[file_uuid] = f"!{prefix}"
                    else:
                        uuid_map[file_uuid] = f"!{ns}"

            elif metadata == "blank_node":
                uri = fm.get("uri", "")
                if uri:
                    # Extract last part of skolem IRI
                    short_id = uri.split("/")[-1] if "/" in uri else uri[-8:]
                    uuid_map[file_uuid] = f"_:genid-{short_id}"

    return uuid_map


def get_anchor_alias(fm: Dict[str, Any]) -> Optional[str]:
    """Generate alias for anchor file using prefix from URI."""
    uri = fm.get("uri", "")
    if not uri:
        return None
    # Check if this is an ontology URI (exact match, no localname)
    if uri in ONTOLOGY_URI_TO_PREFIX:
        prefix = ONTOLOGY_URI_TO_PREFIX[uri]
        return f"{prefix}:"  # e.g., "owl:" for the OWL ontology itself
    prefix = extract_prefix_from_uri(uri)
    if not prefix:
        return None
    localname = extract_localname(uri)
    return f"{prefix}:{localname}"


def get_namespace_alias(fm: Dict[str, Any], fallback_ns: str) -> str:
    """Generate alias for namespace file."""
    uri = fm.get("uri", "")
    if uri:
        for ns_uri, prefix in NS_URI_TO_PREFIX.items():
            if uri.rstrip("#/") == ns_uri.rstrip("#/"):
                return f"!{prefix}"
    return f"!{fallback_ns}"


def get_blank_node_alias(fm: Dict[str, Any]) -> Optional[str]:
    """Generate alias for blank node file."""
    uri = fm.get("uri", "")
    if not uri:
        return None
    short_id = uri.split("/")[-1] if "/" in uri else uri[-8:]
    return f"_:genid-{short_id}"


def get_statement_alias(fm: Dict[str, Any], uuid_map: Dict[str, str]) -> Optional[str]:
    """Generate alias for statement file."""
    subject = fm.get("subject", "")
    predicate = fm.get("predicate", "")
    obj = fm.get("object", "")

    # Get subject alias
    subj_uuid = extract_wikilink_uuid(subject)
    subj_alias = uuid_map.get(subj_uuid, subj_uuid[:8] + "..." if subj_uuid else "?")

    # Get predicate alias
    pred_uuid = extract_wikilink_uuid(predicate)
    # Check for 'a' alias in wikilink like [[uuid|a]]
    if "|a]]" in predicate or "|a ]]" in predicate:
        pred_alias = "a"
    else:
        pred_alias = uuid_map.get(pred_uuid, pred_uuid[:8] + "..." if pred_uuid else "?")

    # Get object alias
    if is_literal(obj):
        obj_alias = extract_literal_value(obj)
    else:
        obj_uuid = extract_wikilink_uuid(obj)
        obj_alias = uuid_map.get(obj_uuid, obj_uuid[:8] + "..." if obj_uuid else "?")

    alias = f"{subj_alias} {pred_alias} {obj_alias}"

    # Truncate if too long
    if len(alias) > MAX_ALIAS_LENGTH:
        alias = alias[: MAX_ALIAS_LENGTH - 3] + "..."

    return alias


def add_alias_to_file(filepath: Path, uuid_map: Dict[str, str], dry_run: bool = False) -> Tuple[bool, Optional[str]]:
    """Add alias to a file. Returns (changed, error)."""
    content = filepath.read_text()
    fm, body = parse_frontmatter(content)

    if fm is None:
        return False, "Could not parse frontmatter"

    metadata = fm.get("metadata")
    if not metadata:
        return False, None

    ns = filepath.parent.name  # Fallback for namespace files
    alias = None

    if metadata == "anchor":
        alias = get_anchor_alias(fm)
    elif metadata == "namespace":
        alias = get_namespace_alias(fm, ns)
    elif metadata == "blank_node":
        alias = get_blank_node_alias(fm)
    elif metadata == "statement":
        alias = get_statement_alias(fm, uuid_map)

    if not alias:
        return False, None

    # Add alias to frontmatter
    fm["aliases"] = [alias]

    # Format and write
    new_content = format_frontmatter(fm) + body

    if not dry_run:
        filepath.write_text(new_content)

    return True, None


def main() -> None:
    parser = argparse.ArgumentParser(description="Add aliases to ontology files")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without applying")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

    repo_root = Path(".")

    print("=" * 60)
    print("Adding Aliases to Ontology Files")
    print("=" * 60)

    if args.dry_run:
        print("DRY RUN - no files will be modified\n")

    # Step 1: Build UUID to alias mapping
    print("Building UUID → alias mapping...")
    uuid_map = build_uuid_to_alias_map(repo_root)
    print(f"  Found {len(uuid_map)} mappings")

    # Step 2: Process all files
    print("\nProcessing files...")
    stats = {"anchor": 0, "namespace": 0, "blank_node": 0, "statement": 0, "errors": 0}

    for ns in PREFIXES:
        ns_dir = repo_root / ns
        if not ns_dir.exists():
            continue

        for filepath in sorted(ns_dir.glob("*.md")):
            if filepath.name == "_index.md":
                continue

            changed, error = add_alias_to_file(filepath, uuid_map, args.dry_run)

            if error:
                stats["errors"] += 1
                if args.verbose:
                    print(f"  ERROR: {filepath}: {error}")
            elif changed:
                # Determine type
                content = filepath.read_text()
                fm, _ = parse_frontmatter(content)
                if fm:
                    metadata = fm.get("metadata")
                    if metadata in stats:
                        stats[metadata] += 1
                    if args.verbose:
                        alias = fm.get("aliases", [""])[0]
                        print(f"  {filepath.name}: {alias}")

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"  Anchors: {stats['anchor']}")
    print(f"  Namespaces: {stats['namespace']}")
    print(f"  Blank nodes: {stats['blank_node']}")
    print(f"  Statements: {stats['statement']}")
    print(f"  Errors: {stats['errors']}")

    if args.dry_run:
        print("\nRun without --dry-run to apply changes.")


if __name__ == "__main__":
    main()

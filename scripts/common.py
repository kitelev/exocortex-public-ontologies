#!/usr/bin/env python3
"""
Common utilities for ontology scripts.

This module provides shared functionality for loading prefix mappings
from _prefixes.yaml instead of hardcoding them in each script.

Usage:
    from common import load_prefixes, get_uri_to_prefix, get_prefix_dirs

Example:
    prefixes = load_prefixes()
    uri_to_prefix = get_uri_to_prefix(prefixes)
    prefix_dirs = get_prefix_dirs()
"""

import re
import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


def get_repo_root() -> Path:
    """Get the repository root directory."""
    return Path(__file__).parent.parent


def load_prefixes(repo_root: Optional[Path] = None) -> Dict[str, str]:
    """
    Load prefix → URI mapping from _prefixes.yaml.

    Returns:
        Dict mapping prefix names to namespace URIs.
        Example: {"rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#", ...}
    """
    if repo_root is None:
        repo_root = get_repo_root()

    prefixes_file = repo_root / "_prefixes.yaml"
    if not prefixes_file.exists():
        raise FileNotFoundError(f"Prefixes file not found: {prefixes_file}")

    with open(prefixes_file, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        raise ValueError(f"Invalid prefixes file format: expected dict, got {type(data)}")

    return data


def get_uri_to_prefix(prefixes: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    """
    Get URI → prefix mapping (inverted from prefixes).

    Args:
        prefixes: Optional prefix→URI dict. If None, loads from file.

    Returns:
        Dict mapping namespace URIs to prefix names.
        Example: {"http://www.w3.org/1999/02/22-rdf-syntax-ns#": "rdf", ...}
    """
    if prefixes is None:
        prefixes = load_prefixes()

    return {uri: prefix for prefix, uri in prefixes.items()}


def get_prefix_dirs(repo_root: Optional[Path] = None) -> List[str]:
    """
    Get list of prefix directories that exist in the repository.

    This returns only prefixes that have actual directories,
    filtering out external namespaces and ontology URI variants.

    Returns:
        Sorted list of prefix names that have directories.
        Example: ["rdf", "rdfs", "owl", ...]
    """
    if repo_root is None:
        repo_root = get_repo_root()

    prefixes = load_prefixes(repo_root)
    existing_dirs = []

    for prefix in prefixes.keys():
        # Skip ontology URI variants (they use the main prefix's directory)
        if prefix.endswith("-ontology"):
            continue

        # Check if directory exists
        prefix_dir = repo_root / prefix
        if prefix_dir.is_dir():
            existing_dirs.append(prefix)

    return sorted(existing_dirs)


def get_primary_prefixes(prefixes: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    """
    Get only primary namespace prefixes (excluding -ontology variants).

    Returns:
        Dict of primary prefix → URI mappings.
    """
    if prefixes is None:
        prefixes = load_prefixes()

    return {prefix: uri for prefix, uri in prefixes.items() if not prefix.endswith("-ontology")}


def get_ontology_uri_to_prefix(prefixes: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    """
    Get ontology URI → prefix mapping for owl:Ontology resources.

    This maps URIs like "http://www.w3.org/2002/07/owl" to "owl".

    Returns:
        Dict mapping ontology URIs (without #) to prefix names.
    """
    if prefixes is None:
        prefixes = load_prefixes()

    result = {}
    for prefix, uri in prefixes.items():
        if prefix.endswith("-ontology"):
            # Extract base prefix (e.g., "owl-ontology" → "owl")
            base_prefix = prefix.rsplit("-ontology", 1)[0]
            result[uri] = base_prefix

    return result


def extract_prefix_from_uri(uri: str, uri_to_prefix: Optional[Dict[str, str]] = None) -> Optional[str]:
    """
    Extract namespace prefix from a full URI.

    Args:
        uri: Full URI like "http://www.w3.org/2002/07/owl#Class"
        uri_to_prefix: Optional URI→prefix mapping. If None, loads from file.

    Returns:
        Prefix name or None if not found.
    """
    if not uri:
        return None

    if uri_to_prefix is None:
        uri_to_prefix = get_uri_to_prefix()

    # Try each namespace URI (longest match first for specificity)
    for ns_uri in sorted(uri_to_prefix.keys(), key=len, reverse=True):
        if uri.startswith(ns_uri):
            return uri_to_prefix[ns_uri]

    # Try ontology URIs (exact match for URIs without fragment)
    ontology_uris = get_ontology_uri_to_prefix()
    if uri in ontology_uris:
        return ontology_uris[uri]

    return None


def extract_localname(uri: str) -> str:
    """Extract local name from URI (part after # or last /)."""
    if "#" in uri:
        return uri.split("#")[-1]
    elif "/" in uri:
        return uri.rstrip("/").split("/")[-1]
    return uri


def uri_to_curie(uri: str, uri_to_prefix: Optional[Dict[str, str]] = None) -> str:
    """
    Convert full URI to CURIE (prefix:localname) format.

    Args:
        uri: Full URI like "http://www.w3.org/2002/07/owl#Class"
        uri_to_prefix: Optional URI→prefix mapping.

    Returns:
        CURIE like "owl:Class" or localname if prefix not found.
    """
    prefix = extract_prefix_from_uri(uri, uri_to_prefix)
    localname = extract_localname(uri)

    if prefix:
        return f"{prefix}:{localname}"
    return localname


# Common frontmatter parsing utilities


def parse_frontmatter(content: str) -> Tuple[Optional[Dict[str, Any]], str]:
    """
    Parse YAML frontmatter and body from markdown content.

    Returns:
        Tuple of (frontmatter dict or None, body string).
    """
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


def parse_frontmatter_from_file(filepath: Path) -> Optional[Dict[str, Any]]:
    """
    Parse YAML frontmatter from a markdown file.

    Returns:
        Frontmatter dict or None if parsing fails.
    """
    try:
        content = filepath.read_text(encoding="utf-8")
        fm, _ = parse_frontmatter(content)
        return fm
    except Exception:
        return None


def extract_wikilink_uuid(value: str) -> Optional[str]:
    """Extract UUID from wikilink like [[uuid]] or [[uuid|alias]]."""
    if not value:
        return None
    match = re.search(r"\[\[([^\]|]+)", value)
    if match:
        return match.group(1)
    return None

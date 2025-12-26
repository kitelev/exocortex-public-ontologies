#!/usr/bin/env python3
"""
Generate search index for ontology resources.

Creates docs/search-index.json with all anchors for client-side search.

Usage:
    python scripts/generate_search_index.py
"""

import json
import re
import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional

from common import get_prefix_dirs, get_repo_root, load_prefixes

REPO_ROOT = get_repo_root()
DOCS_DIR = REPO_ROOT / "docs"
PREFIXES = get_prefix_dirs()
PREFIX_TO_URI = load_prefixes()


def parse_frontmatter(filepath: Path) -> Optional[Dict[str, Any]]:
    """Parse YAML frontmatter from a markdown file."""
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception:
        return None

    if not content.startswith("---"):
        return None

    end_match = re.search(r"\n---\s*\n", content[3:])
    if not end_match:
        end_match = re.search(r"\n---\s*$", content[3:])
        if not end_match:
            return None

    yaml_content = content[4 : 3 + end_match.start()]

    try:
        return yaml.safe_load(yaml_content) or {}
    except yaml.YAMLError:
        return None


def build_index() -> List[Dict[str, str]]:
    """Build search index from all anchor files."""
    index = []

    for prefix in PREFIXES:
        ns_dir = REPO_ROOT / prefix
        if not ns_dir.exists():
            continue

        ns_uri = PREFIX_TO_URI.get(prefix, "")

        for filepath in ns_dir.glob("*.md"):
            data = parse_frontmatter(filepath)
            if not data:
                continue

            metadata = data.get("metadata")
            if metadata not in ("anchor", "namespace"):
                continue

            aliases = data.get("aliases", [])
            if not aliases:
                continue

            alias = aliases[0] if isinstance(aliases, list) else str(aliases)
            uri = data.get("uri", "")
            uuid = filepath.stem

            # Extract local name from alias for display
            local_name = alias.split(":")[-1] if ":" in alias else alias

            entry = {
                "a": alias,  # alias
                "p": prefix,  # prefix
                "u": uri,  # uri
                "t": metadata[0],  # type: 'a' for anchor, 'n' for namespace
            }

            index.append(entry)

    return index


def main():
    """Generate search index."""
    print("Building search index...")

    index = build_index()

    # Sort by alias
    index.sort(key=lambda x: x.get("a", "").lower())

    output_path = DOCS_DIR / "search-index.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, separators=(",", ":"))

    print(f"Generated {output_path}")
    print(f"  Indexed {len(index)} resources")

    # Show file size
    size_kb = output_path.stat().st_size / 1024
    print(f"  File size: {size_kb:.1f} KB")


if __name__ == "__main__":
    main()

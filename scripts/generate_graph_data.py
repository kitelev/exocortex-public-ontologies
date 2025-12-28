#!/usr/bin/env python3
"""
Generate graph data with real RDF relationships for the visual browser.

Extracts:
- rdfs:subClassOf relationships
- rdfs:subPropertyOf relationships
- rdfs:domain relationships
- rdfs:range relationships
- rdf:type relationships (for main types)

Output: docs/graph-data.json
"""

import json
import re
import sys
from pathlib import Path
from collections import defaultdict

# Add scripts to path
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from common import load_prefixes, get_prefix_dirs, parse_frontmatter_from_file, extract_wikilink_uuid

# Well-known predicate UUIDs (generated from URI using uuid5)
PREDICATES = {
    # rdfs:subClassOf
    "d55dc3fe-9a9f-5908-baae-e67d0fa0eab0": "subClassOf",
    # rdfs:subPropertyOf
    "4b368645-5f7a-551b-940f-acebfe3d0bd2": "subPropertyOf",
    # rdfs:domain
    "84d654c0-420b-5a08-ad64-1f16d51de0b2": "domain",
    # rdfs:range
    "c6a11966-a018-5be8-95a0-eba182c2fd93": "range",
    # rdf:type
    "73b69787-81ea-563e-8e09-9c84cad4cf2b": "type",
}


def load_uuid_map(repo_root: Path, prefixes: list) -> dict:
    """Build UUID -> alias mapping from anchor files."""
    uuid_map = {}

    for prefix in prefixes:
        prefix_dir = repo_root / prefix
        if not prefix_dir.exists():
            continue

        for filepath in prefix_dir.glob("*.md"):
            fm = parse_frontmatter_from_file(filepath)
            if not fm:
                continue

            metadata = fm.get("metadata")
            if metadata not in ("anchor", "namespace"):
                continue

            aliases = fm.get("aliases", [])
            if aliases:
                alias = aliases[0] if isinstance(aliases, list) else aliases
                # Clean up quotes if present
                if isinstance(alias, str):
                    alias = alias.strip('"')
                uuid_map[filepath.stem] = {
                    "alias": alias,
                    "uri": fm.get("uri", ""),
                    "prefix": prefix,
                }

    return uuid_map


def extract_relationships(repo_root: Path, prefixes: list, uuid_map: dict) -> list:
    """Extract RDF relationships from statement files."""
    relationships = []

    for prefix in prefixes:
        prefix_dir = repo_root / prefix
        if not prefix_dir.exists():
            continue

        for filepath in prefix_dir.glob("*.md"):
            fm = parse_frontmatter_from_file(filepath)
            if not fm:
                continue

            if fm.get("metadata") != "statement":
                continue

            subject = fm.get("subject", "")
            predicate = fm.get("predicate", "")
            obj = fm.get("object", "")

            # Extract UUIDs from wikilinks
            subj_uuid = extract_wikilink_uuid(subject)
            pred_uuid = extract_wikilink_uuid(predicate)
            obj_uuid = extract_wikilink_uuid(obj)

            if not subj_uuid or not pred_uuid:
                continue

            # Check if this is a relationship we care about
            rel_type = PREDICATES.get(pred_uuid)
            if not rel_type:
                continue

            # Skip literal objects (no UUID)
            if not obj_uuid:
                continue

            # Get aliases for source and target
            subj_info = uuid_map.get(subj_uuid, {})
            obj_info = uuid_map.get(obj_uuid, {})

            if not subj_info or not obj_info:
                continue

            relationships.append({
                "source": subj_uuid,
                "source_alias": subj_info.get("alias", subj_uuid[:8]),
                "target": obj_uuid,
                "target_alias": obj_info.get("alias", obj_uuid[:8]),
                "type": rel_type,
            })

    return relationships


def build_graph_data(repo_root: Path) -> dict:
    """Build complete graph data for visualization."""
    prefixes = load_prefixes()
    prefix_dirs = get_prefix_dirs(repo_root)

    print(f"Loading UUID map from {len(prefix_dirs)} namespaces...")
    uuid_map = load_uuid_map(repo_root, prefix_dirs)
    print(f"  Found {len(uuid_map)} resources")

    print("Extracting relationships...")
    relationships = extract_relationships(repo_root, prefix_dirs, uuid_map)
    print(f"  Found {len(relationships)} relationships")

    # Count by type
    type_counts = defaultdict(int)
    for rel in relationships:
        type_counts[rel["type"]] += 1

    print("\nRelationship types:")
    for rel_type, count in sorted(type_counts.items()):
        print(f"  {rel_type}: {count}")

    # Build nodes from resources referenced in relationships
    node_uuids = set()
    for rel in relationships:
        node_uuids.add(rel["source"])
        node_uuids.add(rel["target"])

    nodes = []
    for uuid in node_uuids:
        info = uuid_map.get(uuid, {})
        if info:
            nodes.append({
                "id": uuid,
                "alias": info.get("alias", uuid[:8]),
                "uri": info.get("uri", ""),
                "prefix": info.get("prefix", ""),
            })

    print(f"\nTotal nodes: {len(nodes)}")

    return {
        "nodes": nodes,
        "links": relationships,
    }


def main():
    repo_root = SCRIPT_DIR.parent
    output_file = repo_root / "docs" / "graph-data.json"

    print("=" * 60)
    print("Graph Data Generator")
    print("=" * 60)

    graph_data = build_graph_data(repo_root)

    # Write output
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(graph_data, f, indent=2)

    print(f"\n✅ Generated {output_file}")
    print(f"   Nodes: {len(graph_data['nodes'])}")
    print(f"   Links: {len(graph_data['links'])}")


if __name__ == "__main__":
    main()

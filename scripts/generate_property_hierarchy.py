#!/usr/bin/env python3
"""
Generate property hierarchy documentation for ontologies.

Creates Markdown documentation showing the property hierarchy (rdfs:subPropertyOf)
relationships in the ontology collection.

Usage:
    python scripts/generate_property_hierarchy.py [--output docs/property-hierarchy.md]
    python scripts/generate_property_hierarchy.py --namespace foaf --output docs/foaf-properties.md
"""

import argparse
import re
import yaml
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Set

from common import get_prefix_dirs, get_repo_root

# Repository root
REPO_ROOT = get_repo_root()

# Namespace prefixes loaded from _prefixes.yaml
PREFIXES = get_prefix_dirs()

# Well-known UUIDs
RDF_TYPE_UUID = "73b69787-81ea-563e-8e09-9c84cad4cf2b"
RDFS_SUBPROPERTY_UUID = "4b368645-5f7a-551b-940f-acebfe3d0bd2"

# Property type UUIDs
PROPERTY_TYPES = {
    "f1afe09a-f371-5a01-a530-be18bfdb4d6b": "rdf:Property",
    "1ca4d39e-3c44-575a-8e82-b745bf274777": "owl:ObjectProperty",
    "73d101aa-9788-5397-ac46-4569ceaae23d": "owl:DatatypeProperty",
    "c4d46947-b828-50f4-871e-f29b15045aa5": "owl:AnnotationProperty",
}


def parse_frontmatter(filepath: Path) -> Optional[dict]:
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
        data = yaml.safe_load(yaml_content)
        return data if data else {}
    except yaml.YAMLError:
        return None


def extract_wikilink_uuid(value: str) -> Optional[str]:
    """Extract UUID from wikilink like [[uuid]] or [[uuid|alias]]."""
    match = re.match(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", value.strip())
    if match:
        return match.group(1)
    return None


def collect_property_data(repo_root: Path, namespace_filter: Optional[str] = None) -> Dict:
    """Collect property and subPropertyOf data from ontologies."""
    data = {
        "properties": {},  # uuid -> {uri, prefix, local, type}
        "subproperty_of": {},  # child_uuid -> [parent_uuid, ...]
        "uuid_to_info": {},  # uuid -> {uri, prefix, local, aliases, type}
    }

    # First pass: collect all anchors and their info
    for prefix in PREFIXES:
        ns_dir = repo_root / prefix
        if not ns_dir.exists():
            continue

        for filepath in ns_dir.glob("*.md"):
            fm = parse_frontmatter(filepath)
            if not fm:
                continue

            metadata = fm.get("metadata")
            if metadata == "anchor":
                uuid = filepath.stem
                uri = fm.get("uri", "")
                aliases = fm.get("aliases", [])

                # Extract prefix:local from alias
                label = ""
                prefix_local = ""
                if aliases:
                    alias = aliases[0]
                    if ":" in alias:
                        prefix_local = alias
                        label = alias.split(":", 1)[1]

                data["uuid_to_info"][uuid] = {
                    "uri": uri,
                    "prefix": prefix,
                    "local": label,
                    "aliases": aliases,
                    "prefix_local": prefix_local,
                    "type": None,
                }

    # Second pass: find properties (rdf:type rdf:Property or owl:*Property)
    for prefix in PREFIXES:
        ns_dir = repo_root / prefix
        if not ns_dir.exists():
            continue

        for filepath in ns_dir.glob("*.md"):
            fm = parse_frontmatter(filepath)
            if not fm:
                continue

            if fm.get("metadata") != "statement":
                continue

            pred_uuid = extract_wikilink_uuid(fm.get("predicate", ""))
            if pred_uuid != RDF_TYPE_UUID:
                continue

            obj_uuid = extract_wikilink_uuid(fm.get("object", ""))
            if obj_uuid not in PROPERTY_TYPES:
                continue

            # This is a property definition
            subj_uuid = extract_wikilink_uuid(fm.get("subject", ""))
            if subj_uuid and subj_uuid in data["uuid_to_info"]:
                info = data["uuid_to_info"][subj_uuid]
                info["type"] = PROPERTY_TYPES[obj_uuid]

                # Only include properties from filtered namespace
                if namespace_filter is None or info["prefix"] == namespace_filter:
                    data["properties"][subj_uuid] = info

    # Third pass: find rdfs:subPropertyOf relationships
    for prefix in PREFIXES:
        ns_dir = repo_root / prefix
        if not ns_dir.exists():
            continue

        for filepath in ns_dir.glob("*.md"):
            fm = parse_frontmatter(filepath)
            if not fm:
                continue

            if fm.get("metadata") != "statement":
                continue

            pred_uuid = extract_wikilink_uuid(fm.get("predicate", ""))
            if pred_uuid != RDFS_SUBPROPERTY_UUID:
                continue

            subj_uuid = extract_wikilink_uuid(fm.get("subject", ""))
            obj_uuid = extract_wikilink_uuid(fm.get("object", ""))

            if subj_uuid and obj_uuid:
                if namespace_filter is None or (
                    subj_uuid in data["uuid_to_info"] and data["uuid_to_info"][subj_uuid]["prefix"] == namespace_filter
                ):
                    if subj_uuid not in data["subproperty_of"]:
                        data["subproperty_of"][subj_uuid] = []
                    data["subproperty_of"][subj_uuid].append(obj_uuid)

    return data


def build_hierarchy_tree(data: Dict) -> Dict[str, List[str]]:
    """Build parent -> children tree."""
    children_of = defaultdict(list)

    for child_uuid, parent_uuids in data["subproperty_of"].items():
        for parent_uuid in parent_uuids:
            children_of[parent_uuid].append(child_uuid)

    return dict(children_of)


def find_root_properties(data: Dict) -> Set[str]:
    """Find properties that are not subPropertyOf any other property in our set."""
    all_properties = set(data["properties"].keys())

    roots = set()
    for prop_uuid in all_properties:
        if prop_uuid not in data["subproperty_of"]:
            roots.add(prop_uuid)
        else:
            # Check if all parents are external
            parents = data["subproperty_of"][prop_uuid]
            if all(p not in all_properties for p in parents):
                roots.add(prop_uuid)

    return roots


def get_property_label(uuid: str, data: Dict) -> str:
    """Get human-readable label for a property."""
    if uuid in data["uuid_to_info"]:
        info = data["uuid_to_info"][uuid]
        return info.get("prefix_local") or info.get("local") or uuid[:8]
    return uuid[:8]


def get_property_type_emoji(uuid: str, data: Dict) -> str:
    """Get emoji based on property type."""
    if uuid in data["uuid_to_info"]:
        ptype = data["uuid_to_info"][uuid].get("type")
        if ptype == "owl:ObjectProperty":
            return "🔗"
        elif ptype == "owl:DatatypeProperty":
            return "📝"
        elif ptype == "owl:AnnotationProperty":
            return "📎"
    return "⚙️"


def generate_tree_markdown(
    root_uuid: str, children_of: Dict[str, List[str]], data: Dict, indent: int = 0, visited: Optional[Set[str]] = None
) -> List[str]:
    """Generate markdown tree for a property and its descendants."""
    if visited is None:
        visited = set()

    if root_uuid in visited:
        return []

    visited.add(root_uuid)
    lines = []

    label = get_property_label(root_uuid, data)
    emoji = get_property_type_emoji(root_uuid, data)
    prefix = "  " * indent + "- "
    lines.append(f"{prefix}{emoji} `{label}`")

    # Sort children by label
    children = children_of.get(root_uuid, [])
    children_sorted = sorted(children, key=lambda u: get_property_label(u, data).lower())

    for child_uuid in children_sorted:
        if child_uuid in data["properties"]:
            lines.extend(generate_tree_markdown(child_uuid, children_of, data, indent + 1, visited))

    return lines


def generate_documentation(data: Dict, namespace_filter: Optional[str] = None) -> str:
    """Generate markdown documentation for property hierarchy."""
    lines = []

    # Header
    if namespace_filter:
        lines.append(f"# {namespace_filter.upper()} Property Hierarchy")
        lines.append("")
        lines.append(f"Property hierarchy for the **{namespace_filter}** namespace.")
    else:
        lines.append("# Property Hierarchy")
        lines.append("")
        lines.append("Complete property hierarchy across all ontologies.")

    lines.append("")
    lines.append(f"*Generated automatically. Total properties: {len(data['properties'])}*")
    lines.append("")

    # Legend
    lines.append("**Legend:** 🔗 ObjectProperty | 📝 DatatypeProperty | 📎 AnnotationProperty | ⚙️ Property")
    lines.append("")

    # Build tree and find roots
    children_of = build_hierarchy_tree(data)
    roots = find_root_properties(data)

    # Group roots by namespace
    roots_by_ns = defaultdict(list)
    for root_uuid in roots:
        if root_uuid in data["uuid_to_info"]:
            ns = data["uuid_to_info"][root_uuid]["prefix"]
            roots_by_ns[ns].append(root_uuid)
        elif root_uuid in data["properties"]:
            ns = data["properties"][root_uuid].get("prefix", "unknown")
            roots_by_ns[ns].append(root_uuid)

    # Generate by namespace
    for ns in sorted(roots_by_ns.keys()):
        roots_in_ns = sorted(roots_by_ns[ns], key=lambda u: get_property_label(u, data).lower())

        lines.append(f"## {ns}")
        lines.append("")

        for root_uuid in roots_in_ns:
            tree_lines = generate_tree_markdown(root_uuid, children_of, data)
            lines.extend(tree_lines)

        lines.append("")

    # Properties with subPropertyOf but not in hierarchy (external parents)
    with_external_parents = []
    for prop_uuid in data["properties"]:
        if prop_uuid in data["subproperty_of"] and prop_uuid not in roots:
            # Has parents but they're external
            parents = data["subproperty_of"][prop_uuid]
            if all(p not in data["properties"] for p in parents):
                with_external_parents.append(prop_uuid)

    if with_external_parents:
        lines.append("## Properties with External Parents")
        lines.append("")
        lines.append("Properties that extend properties from other ontologies:")
        lines.append("")
        for uuid in sorted(with_external_parents, key=lambda u: get_property_label(u, data).lower()):
            label = get_property_label(uuid, data)
            emoji = get_property_type_emoji(uuid, data)
            parents = data["subproperty_of"].get(uuid, [])
            parent_labels = [get_property_label(p, data) for p in parents]
            lines.append(f"- {emoji} `{label}` → {', '.join(parent_labels)}")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate property hierarchy documentation")
    parser.add_argument("-o", "--output", type=str, default="docs/property-hierarchy.md", help="Output file path")
    parser.add_argument("-n", "--namespace", type=str, default=None, help="Filter to specific namespace")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

    print("Collecting property data...")
    data = collect_property_data(REPO_ROOT, args.namespace)

    print(f"  Found {len(data['properties'])} properties")
    print(f"  Found {len(data['subproperty_of'])} subPropertyOf relationships")

    print("Generating documentation...")
    markdown = generate_documentation(data, args.namespace)

    # Ensure docs directory exists
    output_path = REPO_ROOT / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(markdown, encoding="utf-8")
    print(f"Written to {args.output}")

    if args.verbose:
        print("\nPreview:")
        print("=" * 60)
        print(markdown[:2000])
        if len(markdown) > 2000:
            print("...")


if __name__ == "__main__":
    main()

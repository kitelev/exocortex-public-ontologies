#!/usr/bin/env python3
"""
Generate class hierarchy documentation for ontologies.

Creates Markdown documentation showing the class hierarchy (rdfs:subClassOf)
relationships in the ontology collection.

Usage:
    python scripts/generate_class_hierarchy.py [--output docs/class-hierarchy.md]
    python scripts/generate_class_hierarchy.py --namespace owl --output docs/owl-hierarchy.md
"""

import argparse
import re
import yaml
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

# Repository root
REPO_ROOT = Path(__file__).parent.parent

# Namespace prefixes
PREFIXES = [
    "rdf", "rdfs", "owl", "dc", "dcterms", "dcam", "skos", "foaf",
    "prov", "time", "geo", "vcard", "doap", "sioc", "xsd", "dcat",
    "org", "schema", "vs", "sh", "sosa", "as", "void", "geosparql",
]

# Well-known UUIDs
RDF_TYPE_UUID = "73b69787-81ea-563e-8e09-9c84cad4cf2b"
RDFS_SUBCLASS_UUID = "d55dc3fe-9a9f-5908-baae-e67d0fa0eab0"
RDFS_CLASS_UUID = "30488677-f427-5947-8a14-02903ca20a7e"
OWL_CLASS_UUID = "581d50c0-7bc2-5a97-bdc2-9c056f43c807"

# Namespace URI to prefix
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

    yaml_content = content[4:3 + end_match.start()]

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


def collect_class_data(repo_root: Path, namespace_filter: Optional[str] = None) -> Dict:
    """Collect class and subclass data from ontologies."""
    data = {
        "classes": {},       # uuid -> {uri, prefix, local, label}
        "subclass_of": {},   # child_uuid -> [parent_uuid, ...]
        "uuid_to_info": {},  # uuid -> {uri, prefix, local, label, aliases}
    }

    prefixes_to_scan = [namespace_filter] if namespace_filter else PREFIXES

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
                }

    # Second pass: find classes (rdf:type rdfs:Class or owl:Class)
    for prefix in prefixes_to_scan:
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
            if obj_uuid not in (RDFS_CLASS_UUID, OWL_CLASS_UUID):
                continue

            # This is a class definition
            subj_uuid = extract_wikilink_uuid(fm.get("subject", ""))
            if subj_uuid and subj_uuid in data["uuid_to_info"]:
                info = data["uuid_to_info"][subj_uuid]
                # Only include classes from filtered namespace
                if namespace_filter is None or info["prefix"] == namespace_filter:
                    data["classes"][subj_uuid] = info

    # Third pass: find rdfs:subClassOf relationships
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
            if pred_uuid != RDFS_SUBCLASS_UUID:
                continue

            subj_uuid = extract_wikilink_uuid(fm.get("subject", ""))
            obj_uuid = extract_wikilink_uuid(fm.get("object", ""))

            if subj_uuid and obj_uuid:
                # Only include relationships where child is in our filtered set
                if namespace_filter is None or (
                    subj_uuid in data["uuid_to_info"]
                    and data["uuid_to_info"][subj_uuid]["prefix"] == namespace_filter
                ):
                    if subj_uuid not in data["subclass_of"]:
                        data["subclass_of"][subj_uuid] = []
                    data["subclass_of"][subj_uuid].append(obj_uuid)

    return data


def build_hierarchy_tree(data: Dict) -> Dict[str, List[str]]:
    """Build parent -> children tree."""
    children_of = defaultdict(list)

    for child_uuid, parent_uuids in data["subclass_of"].items():
        for parent_uuid in parent_uuids:
            children_of[parent_uuid].append(child_uuid)

    return dict(children_of)


def find_root_classes(data: Dict) -> Set[str]:
    """Find classes that are not subclass of any other class in our set."""
    all_classes = set(data["classes"].keys())
    classes_with_parents = set(data["subclass_of"].keys())

    # Root classes are those without parents OR whose parents are external
    roots = set()
    for cls_uuid in all_classes:
        if cls_uuid not in data["subclass_of"]:
            roots.add(cls_uuid)
        else:
            # Check if all parents are external
            parents = data["subclass_of"][cls_uuid]
            if all(p not in all_classes for p in parents):
                roots.add(cls_uuid)

    return roots


def get_class_label(uuid: str, data: Dict) -> str:
    """Get human-readable label for a class."""
    if uuid in data["uuid_to_info"]:
        info = data["uuid_to_info"][uuid]
        return info.get("prefix_local") or info.get("local") or uuid[:8]
    return uuid[:8]


def generate_tree_markdown(
    root_uuid: str,
    children_of: Dict[str, List[str]],
    data: Dict,
    indent: int = 0,
    visited: Optional[Set[str]] = None
) -> List[str]:
    """Generate markdown tree for a class and its descendants."""
    if visited is None:
        visited = set()

    if root_uuid in visited:
        return []

    visited.add(root_uuid)
    lines = []

    label = get_class_label(root_uuid, data)
    prefix = "  " * indent + "- "
    lines.append(f"{prefix}`{label}`")

    # Sort children by label
    children = children_of.get(root_uuid, [])
    children_sorted = sorted(children, key=lambda u: get_class_label(u, data).lower())

    for child_uuid in children_sorted:
        if child_uuid in data["classes"]:  # Only show classes in our set
            lines.extend(generate_tree_markdown(
                child_uuid, children_of, data, indent + 1, visited
            ))

    return lines


def generate_documentation(data: Dict, namespace_filter: Optional[str] = None) -> str:
    """Generate markdown documentation for class hierarchy."""
    lines = []

    # Header
    if namespace_filter:
        lines.append(f"# {namespace_filter.upper()} Class Hierarchy")
        lines.append("")
        lines.append(f"Class hierarchy for the **{namespace_filter}** namespace.")
    else:
        lines.append("# Class Hierarchy")
        lines.append("")
        lines.append("Complete class hierarchy across all ontologies.")

    lines.append("")
    lines.append(f"*Generated automatically. Total classes: {len(data['classes'])}*")
    lines.append("")

    # Build tree and find roots
    children_of = build_hierarchy_tree(data)
    roots = find_root_classes(data)

    # Group roots by namespace
    roots_by_ns = defaultdict(list)
    for root_uuid in roots:
        if root_uuid in data["uuid_to_info"]:
            ns = data["uuid_to_info"][root_uuid]["prefix"]
            roots_by_ns[ns].append(root_uuid)
        elif root_uuid in data["classes"]:
            ns = data["classes"][root_uuid].get("prefix", "unknown")
            roots_by_ns[ns].append(root_uuid)

    # Generate by namespace
    for ns in sorted(roots_by_ns.keys()):
        roots_in_ns = sorted(roots_by_ns[ns], key=lambda u: get_class_label(u, data).lower())

        lines.append(f"## {ns}")
        lines.append("")

        for root_uuid in roots_in_ns:
            tree_lines = generate_tree_markdown(root_uuid, children_of, data)
            lines.extend(tree_lines)

        lines.append("")

    # Orphan classes (classes with no hierarchy relationships in our set)
    orphans = []
    for cls_uuid in data["classes"]:
        if cls_uuid not in roots and cls_uuid not in data["subclass_of"]:
            orphans.append(cls_uuid)

    if orphans:
        lines.append("## Standalone Classes")
        lines.append("")
        lines.append("Classes without subclass relationships in this collection:")
        lines.append("")
        for uuid in sorted(orphans, key=lambda u: get_class_label(u, data).lower()):
            label = get_class_label(uuid, data)
            lines.append(f"- `{label}`")
        lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate class hierarchy documentation")
    parser.add_argument("-o", "--output", type=str, default="docs/class-hierarchy.md",
                        help="Output file path")
    parser.add_argument("-n", "--namespace", type=str, default=None,
                        help="Filter to specific namespace")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Verbose output")
    args = parser.parse_args()

    print("Collecting class data...")
    data = collect_class_data(REPO_ROOT, args.namespace)

    print(f"  Found {len(data['classes'])} classes")
    print(f"  Found {len(data['subclass_of'])} subclass relationships")

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

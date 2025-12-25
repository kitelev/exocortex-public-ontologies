#!/usr/bin/env python3
"""
Generate Mermaid diagrams for ontologies.

Creates UML-style class diagrams showing:
- Classes and their hierarchy (rdfs:subClassOf)
- Properties with domains and ranges
- Cross-ontology relationships

Usage:
    python scripts/generate_mermaid.py [--output docs/diagrams/]
    python scripts/generate_mermaid.py --namespace foaf --output docs/diagrams/foaf.md
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
RDFS_SUBCLASS_UUID = "d55dc3fe-9a9f-5908-baae-e67d0fa0eab0"
RDFS_DOMAIN_UUID = "84d654c0-420b-5a08-ad64-1f16d51de0b2"
RDFS_RANGE_UUID = "c6a11966-a018-5be8-95a0-eba182c2fd93"

# Class type UUIDs
RDFS_CLASS_UUID = "30488677-f427-5947-8a14-02903ca20a7e"
OWL_CLASS_UUID = "581d50c0-7bc2-5a97-bdc2-9c056f43c807"

# Property type UUIDs
PROPERTY_TYPES = {
    "f1afe09a-f371-5a01-a530-be18bfdb4d6b": "Property",
    "1ca4d39e-3c44-575a-8e82-b745bf274777": "ObjectProperty",
    "73d101aa-9788-5397-ac46-4569ceaae23d": "DatatypeProperty",
    "c4d46947-b828-50f4-871e-f29b15045aa5": "AnnotationProperty",
}


def parse_frontmatter_fast(filepath: Path) -> Optional[dict]:
    """Parse YAML frontmatter from a markdown file (optimized)."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            first_line = f.readline()
            if not first_line.startswith('---'):
                return None

            lines = [first_line]
            for line in f:
                lines.append(line)
                if line.strip() == '---':
                    break

            yaml_content = ''.join(lines[1:-1])
            return yaml.safe_load(yaml_content) or {}
    except Exception:
        return None


def extract_wikilink_uuid(value: str) -> Optional[str]:
    """Extract UUID from wikilink like [[uuid]] or [[uuid|alias]]."""
    if not value:
        return None
    match = re.match(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", value.strip())
    return match.group(1) if match else None


def sanitize_mermaid_id(text: str) -> str:
    """Convert text to valid Mermaid identifier."""
    sanitized = re.sub(r'[^a-zA-Z0-9_]', '_', text)
    if sanitized and sanitized[0].isdigit():
        sanitized = '_' + sanitized
    return sanitized


def collect_ontology_data(repo_root: Path, namespace_filter: Optional[str] = None) -> Dict:
    """Collect classes, properties, and relationships."""
    data = {
        "uuid_to_info": {},
        "classes": set(),
        "properties": {},
        "subclass_of": {},
    }

    target_prefixes = [namespace_filter] if namespace_filter else PREFIXES

    # Collect all anchors from target namespaces
    for prefix in target_prefixes:
        ns_dir = repo_root / prefix
        if not ns_dir.exists():
            continue

        for filepath in ns_dir.glob("*.md"):
            fm = parse_frontmatter_fast(filepath)
            if not fm:
                continue

            metadata_type = fm.get("metadata")
            uuid = filepath.stem

            if metadata_type == "anchor":
                aliases = fm.get("aliases", [])
                prefix_local = ""
                local = ""
                if aliases:
                    alias = aliases[0]
                    if ":" in alias:
                        prefix_local = alias
                        local = alias.split(":", 1)[1]

                data["uuid_to_info"][uuid] = {
                    "prefix": prefix,
                    "local": local,
                    "prefix_local": prefix_local,
                    "type": None,
                }

            elif metadata_type == "statement":
                pred_uuid = extract_wikilink_uuid(fm.get("predicate", ""))
                subj_uuid = extract_wikilink_uuid(fm.get("subject", ""))
                obj_uuid = extract_wikilink_uuid(fm.get("object", ""))

                # rdf:type -> class or property
                if pred_uuid == RDF_TYPE_UUID:
                    if obj_uuid in (RDFS_CLASS_UUID, OWL_CLASS_UUID):
                        data["classes"].add(subj_uuid)
                    elif obj_uuid in PROPERTY_TYPES:
                        data["properties"][subj_uuid] = {
                            "type": PROPERTY_TYPES[obj_uuid],
                            "domain": None,
                            "range": None,
                        }

                # rdfs:subClassOf
                elif pred_uuid == RDFS_SUBCLASS_UUID:
                    if subj_uuid not in data["subclass_of"]:
                        data["subclass_of"][subj_uuid] = []
                    data["subclass_of"][subj_uuid].append(obj_uuid)

                # rdfs:domain
                elif pred_uuid == RDFS_DOMAIN_UUID:
                    if subj_uuid in data["properties"]:
                        data["properties"][subj_uuid]["domain"] = obj_uuid

                # rdfs:range
                elif pred_uuid == RDFS_RANGE_UUID:
                    if subj_uuid in data["properties"]:
                        data["properties"][subj_uuid]["range"] = obj_uuid

    # If we need external anchor info, collect it
    needed_uuids = set()
    for parents in data["subclass_of"].values():
        needed_uuids.update(parents)
    for prop in data["properties"].values():
        if prop["domain"]:
            needed_uuids.add(prop["domain"])
        if prop["range"]:
            needed_uuids.add(prop["range"])

    missing_uuids = needed_uuids - set(data["uuid_to_info"].keys())

    if missing_uuids:
        for prefix in PREFIXES:
            if not missing_uuids:
                break
            ns_dir = repo_root / prefix
            if not ns_dir.exists():
                continue

            for filepath in ns_dir.glob("*.md"):
                uuid = filepath.stem
                if uuid not in missing_uuids:
                    continue

                fm = parse_frontmatter_fast(filepath)
                if not fm or fm.get("metadata") != "anchor":
                    continue

                aliases = fm.get("aliases", [])
                prefix_local = ""
                local = ""
                if aliases:
                    alias = aliases[0]
                    if ":" in alias:
                        prefix_local = alias
                        local = alias.split(":", 1)[1]

                data["uuid_to_info"][uuid] = {
                    "prefix": prefix,
                    "local": local,
                    "prefix_local": prefix_local,
                    "type": None,
                }
                missing_uuids.discard(uuid)

    return data


def get_label(uuid: str, data: Dict) -> str:
    """Get human-readable label for a UUID."""
    if uuid in data["uuid_to_info"]:
        info = data["uuid_to_info"][uuid]
        return info.get("prefix_local") or info.get("local") or uuid[:8]
    return uuid[:8]


def generate_class_diagram(data: Dict, max_items: int = 50) -> str:
    """Generate Mermaid classDiagram."""
    lines = ["classDiagram"]

    classes_in_diagram = set()

    # Add classes (limit for readability)
    sorted_classes = sorted(data["classes"], key=lambda u: get_label(u, data).lower())[:max_items]

    for cls_uuid in sorted_classes:
        label = get_label(cls_uuid, data)
        mermaid_id = sanitize_mermaid_id(label)
        classes_in_diagram.add(cls_uuid)
        lines.append(f"    class {mermaid_id}")

    # Add inheritance
    for child_uuid, parents in data["subclass_of"].items():
        if child_uuid not in classes_in_diagram:
            continue
        child_label = get_label(child_uuid, data)
        child_id = sanitize_mermaid_id(child_label)

        for parent_uuid in parents:
            parent_label = get_label(parent_uuid, data)
            parent_id = sanitize_mermaid_id(parent_label)

            if parent_uuid not in classes_in_diagram:
                lines.insert(1, f"    class {parent_id}")
                classes_in_diagram.add(parent_uuid)

            lines.append(f"    {parent_id} <|-- {child_id}")

    # Add properties with domain/range
    prop_count = 0
    for prop_uuid, prop_info in data["properties"].items():
        if prop_count >= 30:  # Limit properties for readability
            break

        domain_uuid = prop_info.get("domain")
        range_uuid = prop_info.get("range")

        if domain_uuid and range_uuid:
            if domain_uuid in classes_in_diagram or range_uuid in classes_in_diagram:
                prop_label = get_label(prop_uuid, data)
                domain_id = sanitize_mermaid_id(get_label(domain_uuid, data))
                range_id = sanitize_mermaid_id(get_label(range_uuid, data))

                if domain_uuid not in classes_in_diagram:
                    lines.insert(1, f"    class {domain_id}")
                    classes_in_diagram.add(domain_uuid)
                if range_uuid not in classes_in_diagram:
                    lines.insert(1, f"    class {range_id}")
                    classes_in_diagram.add(range_uuid)

                arrow = "-->" if prop_info["type"] == "ObjectProperty" else "..>"
                lines.append(f"    {domain_id} {arrow} {range_id} : {prop_label}")
                prop_count += 1

    return "\n".join(lines)


def generate_documentation(data: Dict, namespace: Optional[str] = None) -> str:
    """Generate markdown documentation with Mermaid diagram."""
    lines = []

    if namespace:
        lines.append(f"# {namespace.upper()} Ontology Diagram")
        lines.append("")
        lines.append(f"UML-style class diagram for the **{namespace}** namespace.")
    else:
        lines.append("# Ontology Diagram")
        lines.append("")
        lines.append("UML-style class diagram showing ontology structure.")

    lines.append("")
    lines.append(f"*Generated automatically. Classes: {len(data['classes'])}, Properties: {len(data['properties'])}*")
    lines.append("")

    lines.append("**Legend:**")
    lines.append("- `<|--` Inheritance (rdfs:subClassOf)")
    lines.append("- `-->` Object Property")
    lines.append("- `..>` Datatype Property")
    lines.append("")

    lines.append("```mermaid")
    lines.append(generate_class_diagram(data))
    lines.append("```")
    lines.append("")

    lines.append("## Statistics")
    lines.append("")
    lines.append("| Metric | Count |")
    lines.append("|--------|-------|")
    lines.append(f"| Classes | {len(data['classes'])} |")
    lines.append(f"| Properties | {len(data['properties'])} |")
    lines.append(f"| Inheritance relationships | {sum(len(p) for p in data['subclass_of'].values())} |")

    props_with_domain = sum(1 for p in data['properties'].values() if p.get('domain'))
    props_with_range = sum(1 for p in data['properties'].values() if p.get('range'))
    lines.append(f"| Properties with domain | {props_with_domain} |")
    lines.append(f"| Properties with range | {props_with_range} |")
    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Generate Mermaid diagrams for ontologies")
    parser.add_argument("-o", "--output", type=str, default="docs/diagrams",
                        help="Output directory or file path")
    parser.add_argument("-n", "--namespace", type=str, default=None,
                        help="Generate for specific namespace only")
    parser.add_argument("--all", action="store_true",
                        help="Generate separate diagram for each namespace")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Verbose output")
    args = parser.parse_args()

    output_path = REPO_ROOT / args.output

    if args.all:
        output_path.mkdir(parents=True, exist_ok=True)

        generated = []
        for ns in PREFIXES:
            ns_dir = REPO_ROOT / ns
            if not ns_dir.exists():
                continue

            print(f"Generating diagram for {ns}...")
            data = collect_ontology_data(REPO_ROOT, ns)

            if not data["classes"] and not data["properties"]:
                print(f"  Skipping {ns} (no classes or properties)")
                continue

            markdown = generate_documentation(data, ns)

            ns_output = output_path / f"{ns}.md"
            ns_output.write_text(markdown, encoding="utf-8")
            print(f"  Classes: {len(data['classes'])}, Properties: {len(data['properties'])}")
            generated.append(ns)

        # Generate index
        print("\nGenerating index...")
        index_lines = ["# Ontology Diagrams", "", "Mermaid diagrams for each ontology:", ""]
        for ns in sorted(generated):
            index_lines.append(f"- [{ns}]({ns}.md)")
        index_lines.append("")

        (output_path / "README.md").write_text("\n".join(index_lines), encoding="utf-8")
        print(f"Generated {len(generated)} diagrams")

    else:
        print("Collecting ontology data...")
        data = collect_ontology_data(REPO_ROOT, args.namespace)

        print(f"  Found {len(data['classes'])} classes")
        print(f"  Found {len(data['properties'])} properties")

        markdown = generate_documentation(data, args.namespace)

        if output_path.suffix == ".md":
            output_file = output_path
        else:
            output_path.mkdir(parents=True, exist_ok=True)
            output_file = output_path / (f"{args.namespace}.md" if args.namespace else "all-ontologies.md")

        output_file.parent.mkdir(parents=True, exist_ok=True)
        output_file.write_text(markdown, encoding="utf-8")
        print(f"Written to {output_file.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()

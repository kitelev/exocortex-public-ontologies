#!/usr/bin/env python3
"""
Create anchor and statement files for DefaultAssetLayout definition.

This script generates:
1. Property definitions: Layout_isDefault, Layout_blocks
2. DefaultAssetLayout instance with all its statements
3. Placeholder anchors for the 6 layout blocks

Issue: #1451
"""

import uuid
from pathlib import Path

# Known UUIDs for predicates
PREDICATE_UUIDS = {
    "rdf:type": "73b69787-81ea-563e-8e09-9c84cad4cf2b",
    "rdfs:label": "d0e9e696-d3f2-5966-a62f-d8358cbde741",
    "rdfs:comment": "da1b0b28-9c51-55c3-a963-2337006693de",
    "rdfs:domain": "6f6b4f67-c31d-5673-9863-ee0c1d7f3bb8",
    "rdfs:range": "8bf79888-4cd0-5acb-b5e3-8542f0a5c186",
}

# Known UUIDs for classes
CLASS_UUIDS = {
    "owl:DatatypeProperty": "e2d8eb1f-3c20-5891-8c68-c31e9abf5ef5",
    "owl:ObjectProperty": "fe4fbb92-8f3f-5e6c-beb0-7d8bb2f4b7c7",
    "owl:Class": "30488677-f427-5947-8a14-02903ca20a7e",
    "xsd:boolean": "32c0d57e-f209-5eee-bcbe-45500c2fe63e",
    "rdf:List": "93f1c23c-f7f6-5c85-81c9-2d3e9bfe9f65",
    # exo-ui classes
    "exo-ui:Layout": "e613b698-c9d3-5470-9322-25ce15e43f4e",
    "exo-ui:LayoutBlock": "a80751c1-c327-52ef-a732-7c0461cb4547",
}


def get_uuid_for_uri(uri: str) -> str:
    """Generate UUIDv5 for a given URI."""
    return str(uuid.uuid5(uuid.NAMESPACE_URL, uri))


def create_anchor_file(output_dir: Path, prop_name: str, uri: str) -> str:
    """Create anchor file for a resource. Returns the UUID."""
    prop_uuid = get_uuid_for_uri(uri)
    content = f"""---
metadata: anchor
uri: "{uri}"
aliases:
  - "exo-ui:{prop_name}"
---
"""
    (output_dir / f"{prop_uuid}.md").write_text(content)
    print(f"Created anchor: exo-ui:{prop_name} -> {prop_uuid}.md")
    return prop_uuid


def escape_yaml_string(s: str) -> str:
    """Escape a string for use in YAML."""
    s = s.replace("\\", "\\\\")
    s = s.replace('"', '\\"')
    return s


def create_statement_file(
    output_dir: Path,
    subject_uuid: str,
    subject_alias: str,
    predicate_uuid: str,
    predicate_alias: str,
    obj_value: str,
    obj_uuid: str | None = None,
) -> str:
    """Create statement file. Returns the UUID."""
    # Create canonical form for UUID generation
    canonical = f"https://exocortex.my/ontology/exo-ui#{subject_alias.replace('exo-ui:', '')}|{predicate_alias}|{obj_value}"
    stmt_uuid = get_uuid_for_uri(canonical)

    # Format object based on type
    if obj_value.startswith('"'):
        # Literal - keep as is (but escape inner quotes properly)
        obj_formatted = f'"{escape_yaml_string(obj_value[1:-1])}"'
        alias_obj = escape_yaml_string(obj_value)
    elif obj_uuid:
        # Reference - use quoted wikilink
        obj_formatted = f'"[[{obj_uuid}|{obj_value}]]"'
        alias_obj = obj_value
    else:
        # Plain value (e.g., true, false)
        obj_formatted = f'"{obj_value}"'
        alias_obj = obj_value

    content = f"""---
metadata: statement
subject: "[[{subject_uuid}|{subject_alias}]]"
predicate: "[[{predicate_uuid}|{predicate_alias}]]"
object: {obj_formatted}
aliases:
  - "{subject_alias} {predicate_alias} {alias_obj}"
---
"""
    (output_dir / f"{stmt_uuid}.md").write_text(content)
    print(f"Created statement: {subject_alias} {predicate_alias} {alias_obj[:50]}...")
    return stmt_uuid


def main():
    # Output directory
    output_dir = Path(__file__).parent.parent / "exo-ui"

    # ==========================================
    # 1. Create Layout_isDefault property
    # ==========================================
    prop_name = "Layout_isDefault"
    prop_uri = f"https://exocortex.my/ontology/exo-ui#{prop_name}"
    prop_uuid = create_anchor_file(output_dir, prop_name, prop_uri)

    # Property statements
    # rdf:type owl:DatatypeProperty
    create_statement_file(
        output_dir, prop_uuid, f"exo-ui:{prop_name}",
        PREDICATE_UUIDS["rdf:type"], "rdf:type",
        "owl:DatatypeProperty", CLASS_UUIDS["owl:DatatypeProperty"]
    )

    # rdfs:label
    create_statement_file(
        output_dir, prop_uuid, f"exo-ui:{prop_name}",
        PREDICATE_UUIDS["rdfs:label"], "rdfs:label",
        '"Layout Is Default"'
    )

    # rdfs:comment
    create_statement_file(
        output_dir, prop_uuid, f"exo-ui:{prop_name}",
        PREDICATE_UUIDS["rdfs:comment"], "rdfs:comment",
        '"Whether this layout is the default fallback for asset views"'
    )

    # rdfs:domain exo-ui:Layout
    create_statement_file(
        output_dir, prop_uuid, f"exo-ui:{prop_name}",
        PREDICATE_UUIDS["rdfs:domain"], "rdfs:domain",
        "exo-ui:Layout", CLASS_UUIDS["exo-ui:Layout"]
    )

    # rdfs:range xsd:boolean
    create_statement_file(
        output_dir, prop_uuid, f"exo-ui:{prop_name}",
        PREDICATE_UUIDS["rdfs:range"], "rdfs:range",
        "xsd:boolean", CLASS_UUIDS["xsd:boolean"]
    )

    # ==========================================
    # 2. Create Layout_blocks property
    # ==========================================
    prop_name = "Layout_blocks"
    prop_uri = f"https://exocortex.my/ontology/exo-ui#{prop_name}"
    prop_uuid = create_anchor_file(output_dir, prop_name, prop_uri)

    # rdf:type owl:ObjectProperty
    create_statement_file(
        output_dir, prop_uuid, f"exo-ui:{prop_name}",
        PREDICATE_UUIDS["rdf:type"], "rdf:type",
        "owl:ObjectProperty", CLASS_UUIDS["owl:ObjectProperty"]
    )

    # rdfs:label
    create_statement_file(
        output_dir, prop_uuid, f"exo-ui:{prop_name}",
        PREDICATE_UUIDS["rdfs:label"], "rdfs:label",
        '"Layout Blocks"'
    )

    # rdfs:comment
    create_statement_file(
        output_dir, prop_uuid, f"exo-ui:{prop_name}",
        PREDICATE_UUIDS["rdfs:comment"], "rdfs:comment",
        '"Ordered list of layout blocks to display"'
    )

    # rdfs:domain exo-ui:Layout
    create_statement_file(
        output_dir, prop_uuid, f"exo-ui:{prop_name}",
        PREDICATE_UUIDS["rdfs:domain"], "rdfs:domain",
        "exo-ui:Layout", CLASS_UUIDS["exo-ui:Layout"]
    )

    # rdfs:range rdf:List
    create_statement_file(
        output_dir, prop_uuid, f"exo-ui:{prop_name}",
        PREDICATE_UUIDS["rdfs:range"], "rdfs:range",
        "rdf:List", CLASS_UUIDS["rdf:List"]
    )

    # ==========================================
    # 3. Create 6 LayoutBlock instance anchors
    # ==========================================
    block_names = [
        "IdentityBlock",
        "ClassificationBlock",
        "OutboundRelationsBlock",
        "InboundRelationsBlock",
        "UsageContextBlock",
        "BodyContentBlock",
    ]

    block_uuids = {}
    for block_name in block_names:
        block_uri = f"https://exocortex.my/ontology/exo-ui#{block_name}"
        block_uuid = create_anchor_file(output_dir, block_name, block_uri)
        block_uuids[block_name] = block_uuid

        # Add rdf:type exo-ui:LayoutBlock
        create_statement_file(
            output_dir, block_uuid, f"exo-ui:{block_name}",
            PREDICATE_UUIDS["rdf:type"], "rdf:type",
            "exo-ui:LayoutBlock", CLASS_UUIDS["exo-ui:LayoutBlock"]
        )

        # Add rdfs:label
        label = " ".join(
            word for word in
            [s for s in block_name.replace("Block", " Block").split() if s]
        )
        create_statement_file(
            output_dir, block_uuid, f"exo-ui:{block_name}",
            PREDICATE_UUIDS["rdfs:label"], "rdfs:label",
            f'"{label}"'
        )

    # ==========================================
    # 4. Create DefaultAssetLayout instance
    # ==========================================
    layout_name = "DefaultAssetLayout"
    layout_uri = f"https://exocortex.my/ontology/exo-ui#{layout_name}"
    layout_uuid = create_anchor_file(output_dir, layout_name, layout_uri)

    # Get property UUIDs
    layout_isdefault_uuid = get_uuid_for_uri("https://exocortex.my/ontology/exo-ui#Layout_isDefault")
    layout_blocks_uuid = get_uuid_for_uri("https://exocortex.my/ontology/exo-ui#Layout_blocks")

    # rdf:type exo-ui:Layout
    create_statement_file(
        output_dir, layout_uuid, f"exo-ui:{layout_name}",
        PREDICATE_UUIDS["rdf:type"], "rdf:type",
        "exo-ui:Layout", CLASS_UUIDS["exo-ui:Layout"]
    )

    # rdfs:label
    create_statement_file(
        output_dir, layout_uuid, f"exo-ui:{layout_name}",
        PREDICATE_UUIDS["rdfs:label"], "rdfs:label",
        '"Asset Overview"@en'
    )

    # rdfs:comment
    create_statement_file(
        output_dir, layout_uuid, f"exo-ui:{layout_name}",
        PREDICATE_UUIDS["rdfs:comment"], "rdfs:comment",
        '"Default layout showing all knowledge related to the asset (LODE-style)"@en'
    )

    # Layout_isDefault true
    create_statement_file(
        output_dir, layout_uuid, f"exo-ui:{layout_name}",
        layout_isdefault_uuid, "exo-ui:Layout_isDefault",
        "true"
    )

    # Layout_blocks - for each block in order
    for i, block_name in enumerate(block_names):
        create_statement_file(
            output_dir, layout_uuid, f"exo-ui:{layout_name}",
            layout_blocks_uuid, "exo-ui:Layout_blocks",
            f"exo-ui:{block_name}", block_uuids[block_name]
        )

    print(f"\nCreated all files in {output_dir}")
    print("Run 'python scripts/validate.py exo-ui' to validate")


if __name__ == "__main__":
    main()

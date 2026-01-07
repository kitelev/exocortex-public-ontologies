#!/usr/bin/env python3
"""
Add LayoutBlock properties (order, query, renderer, headless) for IdentityBlock and ClassificationBlock.

This script generates statement files for:
1. LayoutBlock_order (1 for Identity, 2 for Classification)
2. LayoutBlock_query (SPARQL SELECT queries)
3. LayoutBlock_renderer ("identity", "classification")
4. LayoutBlock_headless (true for both - CLI compatible)

Issue: #1452
"""

import uuid
from pathlib import Path

# Known UUIDs from existing ontology files
PREDICATE_UUIDS = {
    "LayoutBlock_order": "cc698067-b441-5e4c-ae7b-52a77737745d",
    "LayoutBlock_query": "aef46832-408e-5f1f-a464-72b3f1767af3",
    "LayoutBlock_renderer": "b84d3e2d-bd2e-5c6e-aafa-dbec54672cca",
    "LayoutBlock_headless": "92c86a99-0f8b-5549-b173-b3454b3715e8",
}

# Known UUIDs for blocks
BLOCK_UUIDS = {
    "IdentityBlock": "88610dd8-88b3-5c05-b6ad-2e96836b5052",
    "ClassificationBlock": "af38ed21-7762-5d41-855d-f918abb80c5f",
}

# SPARQL queries from the implementation plan (lines 2401-2425)
IDENTITY_QUERY = '''SELECT ?label ?uid ?createdAt ?isDefinedBy
WHERE {
    ?asset exo:Asset_label ?label .
    ?asset exo:Asset_uid ?uid .
    ?asset exo:Asset_createdAt ?createdAt .
    ?asset exo:Asset_isDefinedBy ?isDefinedBy .
}'''

CLASSIFICATION_QUERY = '''SELECT ?class ?prototype
WHERE {
    OPTIONAL { ?asset rdf:type ?class . FILTER(?class != owl:NamedIndividual) }
    OPTIONAL { ?asset exo:Asset_prototype ?prototype }
}'''


def get_uuid_for_uri(uri: str) -> str:
    """Generate UUIDv5 for a given URI."""
    return str(uuid.uuid5(uuid.NAMESPACE_URL, uri))


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
) -> str:
    """Create statement file. Returns the UUID."""
    # Create canonical form for UUID generation
    # Clean the object value for the canonical form
    obj_canonical = obj_value.strip()
    if obj_canonical.startswith('"') and obj_canonical.endswith('"'):
        obj_canonical = obj_canonical[1:-1]
    canonical = f"https://exocortex.my/ontology/exo-ui#{subject_alias.replace('exo-ui:', '')}|{predicate_alias}|{obj_canonical[:100]}"
    stmt_uuid = get_uuid_for_uri(canonical)

    # Format object - always as a quoted string
    obj_formatted = f'"{escape_yaml_string(obj_value)}"'
    alias_obj = obj_value[:50].replace('\n', ' ')

    content = f"""---
metadata: statement
subject: "[[{subject_uuid}|{subject_alias}]]"
predicate: "[[{predicate_uuid}|exo-ui:{predicate_alias}]]"
object: {obj_formatted}
aliases:
  - "{subject_alias} exo-ui:{predicate_alias} {escape_yaml_string(alias_obj)}"
---
"""
    file_path = output_dir / f"{stmt_uuid}.md"
    file_path.write_text(content)
    print(f"Created: {file_path.name} ({subject_alias} {predicate_alias})")
    return stmt_uuid


def main():
    # Output directory
    output_dir = Path(__file__).parent.parent / "exo-ui"

    # Block definitions: (name, uuid, order, renderer, query)
    blocks = [
        ("IdentityBlock", BLOCK_UUIDS["IdentityBlock"], "1", "identity", IDENTITY_QUERY),
        ("ClassificationBlock", BLOCK_UUIDS["ClassificationBlock"], "2", "classification", CLASSIFICATION_QUERY),
    ]

    for block_name, block_uuid, order, renderer, query in blocks:
        subject_alias = f"exo-ui:{block_name}"

        print(f"\n=== {block_name} ===")

        # 1. LayoutBlock_order
        create_statement_file(
            output_dir,
            block_uuid,
            subject_alias,
            PREDICATE_UUIDS["LayoutBlock_order"],
            "LayoutBlock_order",
            order,
        )

        # 2. LayoutBlock_query
        create_statement_file(
            output_dir,
            block_uuid,
            subject_alias,
            PREDICATE_UUIDS["LayoutBlock_query"],
            "LayoutBlock_query",
            query,
        )

        # 3. LayoutBlock_renderer
        create_statement_file(
            output_dir,
            block_uuid,
            subject_alias,
            PREDICATE_UUIDS["LayoutBlock_renderer"],
            "LayoutBlock_renderer",
            renderer,
        )

        # 4. LayoutBlock_headless
        create_statement_file(
            output_dir,
            block_uuid,
            subject_alias,
            PREDICATE_UUIDS["LayoutBlock_headless"],
            "LayoutBlock_headless",
            "true",
        )

    print(f"\n=== Summary ===")
    print(f"Created 8 statement files in {output_dir}")
    print("Run 'python scripts/validate.py exo-ui' to validate")


if __name__ == "__main__":
    main()

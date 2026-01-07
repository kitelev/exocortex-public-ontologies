#!/usr/bin/env python3
"""
Add/update labels and comments for OutboundRelationsBlock and InboundRelationsBlock.

Issue: kitelev/exocortex#1453
"""

import uuid
from pathlib import Path

# Known UUIDs
PREDICATE_UUIDS = {
    "rdfs:label": "d0e9e696-d3f2-5966-a62f-d8358cbde741",
    "rdfs:comment": "da1b0b28-9c51-55c3-a963-2337006693de",
}

# Known UUIDs for blocks
BLOCK_UUIDS = {
    "OutboundRelationsBlock": "02be2d6a-7e46-5871-bb56-1fe82e90d3c2",
    "InboundRelationsBlock": "a0afdb62-d723-58d1-9186-0b406deaabff",
}


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
    obj_canonical = obj_value.strip()
    if obj_canonical.startswith('"') and obj_canonical.endswith('"'):
        obj_canonical = obj_canonical[1:-1]
    canonical = f"https://exocortex.my/ontology/exo-ui#{subject_alias.replace('exo-ui:', '')}|{predicate_alias}|{obj_canonical[:100]}"
    stmt_uuid = get_uuid_for_uri(canonical)

    obj_formatted = f'"{escape_yaml_string(obj_value)}"'
    alias_obj = obj_value[:50].replace('\n', ' ')

    content = f"""---
metadata: statement
subject: "[[{subject_uuid}|{subject_alias}]]"
predicate: "[[{predicate_uuid}|{predicate_alias}]]"
object: {obj_formatted}
aliases:
  - "{subject_alias} {predicate_alias} {escape_yaml_string(alias_obj)}"
---
"""
    file_path = output_dir / f"{stmt_uuid}.md"

    # Check if file exists
    if file_path.exists():
        print(f"Updated: {file_path.name} ({subject_alias} {predicate_alias})")
    else:
        print(f"Created: {file_path.name} ({subject_alias} {predicate_alias})")

    file_path.write_text(content)
    return stmt_uuid


def main():
    output_dir = Path(__file__).parent.parent / "exo-ui"

    # Labels and comments for each block
    blocks_data = [
        {
            "name": "OutboundRelationsBlock",
            "uuid": BLOCK_UUIDS["OutboundRelationsBlock"],
            "labels": [
                ('References (outbound)"@en', "References (outbound)@en"),
                ('Ссылается на"@ru', "Ссылается на@ru"),
            ],
            "comment": "Shows assets this asset references."
        },
        {
            "name": "InboundRelationsBlock",
            "uuid": BLOCK_UUIDS["InboundRelationsBlock"],
            "labels": [
                ('Referenced by (inbound)"@en', "Referenced by (inbound)@en"),
                ('На него ссылаются"@ru', "На него ссылаются@ru"),
            ],
            "comment": "Shows assets that reference this asset."
        },
    ]

    for block in blocks_data:
        subject_alias = f"exo-ui:{block['name']}"
        print(f"\n=== {block['name']} ===")

        # Add labels
        for label_value, _ in block["labels"]:
            create_statement_file(
                output_dir,
                block["uuid"],
                subject_alias,
                PREDICATE_UUIDS["rdfs:label"],
                "rdfs:label",
                label_value,
            )

        # Add comment
        create_statement_file(
            output_dir,
            block["uuid"],
            subject_alias,
            PREDICATE_UUIDS["rdfs:comment"],
            "rdfs:comment",
            block["comment"],
        )

    print(f"\n=== Summary ===")
    print(f"Created/updated label and comment files in {output_dir}")


if __name__ == "__main__":
    main()

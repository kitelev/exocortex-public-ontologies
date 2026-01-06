#!/usr/bin/env python3
"""
Create anchor and statement files for exo-ui ontology properties.

This script generates:
1. Anchor files for each property
2. Statement files for rdf:type, rdfs:label, rdfs:comment, rdfs:domain, rdfs:range
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
    "xsd:string": "936caa86-c233-5829-b9ec-ad6eb152c274",
    "xsd:boolean": "32c0d57e-f209-5eee-bcbe-45500c2fe63e",
    "xsd:integer": "94277b3a-2e5b-5b33-942f-6b57e6bd7ea7",
    "rdf:List": "93f1c23c-f7f6-5c85-81c9-2d3e9bfe9f65",
    "rdf:Property": "6a5b2d2c-42ae-5dab-94e1-f4e6f5c6c8d2",
    # exo-ui classes
    "exo-ui:Command": "715070f9-2d3c-5b32-ab42-c859fe85cb7b",
    "exo-ui:Action": "1f16e8cb-80fe-5693-9817-8f4b97b27c67",
    "exo-ui:Button": "3afde00a-61dc-5831-b340-575bf528413f",
    "exo-ui:ButtonGroup": "9224dd06-9a3f-52d4-acab-8139b21d1768",
    "exo-ui:Condition": "226820e2-09a1-5d53-9b58-c6e7af122e70",
    "exo-ui:CreateAssetAction": "95867d28-3b55-596f-b4ba-ab0fb508a0b7",
    "exo-ui:UpdatePropertyAction": "4c6193c6-80c5-53b0-8d32-71aa9cfcc0ac",
    "exo-ui:NavigateAction": "fb793dc4-95f3-5ded-8b1e-204137fc5266",
    "exo-ui:ExecuteSPARQLAction": "3e71acb3-fe54-5c5c-83e6-a50f0151b266",
    "exo-ui:ShowModalAction": "8529e550-b8fa-57a4-b366-afd23513d60b",
    "exo-ui:CustomHandlerAction": "9ab7bcc5-4d72-5de4-a1b7-562f078c747d",
    "exo-ui:CompositeAction": "6021ac7f-7f15-5abc-8103-352f43a8707d",
}


def get_uuid_for_uri(uri: str) -> str:
    """Generate UUIDv5 for a given URI."""
    return str(uuid.uuid5(uuid.NAMESPACE_URL, uri))


def create_anchor_file(output_dir: Path, prop_name: str, uri: str) -> str:
    """Create anchor file for a property. Returns the UUID."""
    prop_uuid = get_uuid_for_uri(uri)
    content = f"""---
metadata: anchor
uri: "{uri}"
aliases:
  - "exo-ui:{prop_name}"
---
"""
    (output_dir / f"{prop_uuid}.md").write_text(content)
    return prop_uuid


def escape_yaml_string(s: str) -> str:
    """Escape a string for use in YAML."""
    # Escape backslashes first, then quotes
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
    alias_suffix: str,
) -> str:
    """Create statement file. Returns the UUID."""
    # Create canonical form for UUID generation
    canonical = (
        f"https://exocortex.my/ontology/exo-ui#{subject_alias.replace('exo-ui:', '')}|{predicate_alias}|{obj_value}"
    )
    stmt_uuid = get_uuid_for_uri(canonical)

    # Format object based on type
    if obj_value.startswith('"'):
        # Literal - need proper quoting
        # obj_value is like '"some text"'
        inner_text = obj_value[1:-1]  # Remove outer quotes
        obj_formatted = f'"{escape_yaml_string(inner_text)}"'
        # For alias, escape the whole thing
        alias_obj = escape_yaml_string(obj_value)
    else:
        # Reference - need to lookup UUID
        obj_uuid = CLASS_UUIDS.get(obj_value)
        if obj_uuid:
            obj_formatted = f'"[[{obj_uuid}|{obj_value}]]"'
        else:
            # Generate UUID for unknown references
            obj_uri = obj_value.replace(":", "/")  # rough approximation
            obj_uuid = get_uuid_for_uri(f"https://exocortex.my/ontology/{obj_uri}")
            obj_formatted = f'"[[{obj_uuid}|{obj_value}]]"'
        alias_obj = obj_value

    # Escape alias suffix for YAML
    alias_escaped = escape_yaml_string(f"{subject_alias} {predicate_alias} {alias_suffix}")

    content = f"""---
metadata: statement
subject: "[[{subject_uuid}|{subject_alias}]]"
predicate: "[[{predicate_uuid}|{predicate_alias}]]"
object: {obj_formatted}
aliases:
  - "{alias_escaped}"
---
"""
    (output_dir / f"{stmt_uuid}.md").write_text(content)
    return stmt_uuid


# Property definitions
# Format: (name, type, label, comment, domain, range)
PROPERTIES = [
    # Command properties (6)
    (
        "Command_id",
        "DatatypeProperty",
        "command ID",
        "Unique command identifier for Obsidian (e.g., 'exocortex:create-task')",
        "exo-ui:Command",
        "xsd:string",
    ),
    (
        "Command_name",
        "DatatypeProperty",
        "command name",
        "Human-readable command name shown in Command Palette",
        "exo-ui:Command",
        "xsd:string",
    ),
    (
        "Command_hotkey",
        "DatatypeProperty",
        "hotkey",
        "Keyboard shortcut (e.g., 'Ctrl+Shift+T', 'Mod+K')",
        "exo-ui:Command",
        "xsd:string",
    ),
    (
        "Command_icon",
        "DatatypeProperty",
        "icon",
        "Lucide icon name (e.g., 'plus-circle', 'check', 'trash')",
        "exo-ui:Command",
        "xsd:string",
    ),
    (
        "Command_action",
        "ObjectProperty",
        "action",
        "Action to execute when command is invoked",
        "exo-ui:Command",
        "exo-ui:Action",
    ),
    (
        "Command_condition",
        "ObjectProperty",
        "condition",
        "Condition for command visibility in Command Palette",
        "exo-ui:Command",
        "exo-ui:Condition",
    ),
    # Button properties (8)
    (
        "Button_label",
        "DatatypeProperty",
        "button label",
        "Text displayed on button. Can include template variables: {{asset.label}}",
        "exo-ui:Button",
        "xsd:string",
    ),
    (
        "Button_variant",
        "DatatypeProperty",
        "variant",
        "Visual style: primary, secondary, success, warning, danger",
        "exo-ui:Button",
        "xsd:string",
    ),
    ("Button_icon", "DatatypeProperty", "icon", "Optional Lucide icon before label", "exo-ui:Button", "xsd:string"),
    (
        "Button_action",
        "ObjectProperty",
        "action",
        "Action to execute when button is clicked",
        "exo-ui:Button",
        "exo-ui:Action",
    ),
    (
        "Button_group",
        "ObjectProperty",
        "group",
        "Button group membership (Creation, Status, Planning, Maintenance)",
        "exo-ui:Button",
        "exo-ui:ButtonGroup",
    ),
    (
        "Button_condition",
        "ObjectProperty",
        "condition",
        "Condition for button visibility",
        "exo-ui:Button",
        "exo-ui:Condition",
    ),
    (
        "Button_order",
        "DatatypeProperty",
        "order",
        "Sort order within group (lower = first)",
        "exo-ui:Button",
        "xsd:integer",
    ),
    ("Button_tooltip", "DatatypeProperty", "tooltip", "Hover tooltip text", "exo-ui:Button", "xsd:string"),
    # Action properties (12)
    (
        "Action_targetClass",
        "ObjectProperty",
        "target class",
        "For CreateAssetAction: class of asset to create",
        "exo-ui:CreateAssetAction",
        "owl:Class",
    ),
    (
        "Action_template",
        "ObjectProperty",
        "template",
        "For CreateAssetAction: template/prototype for new asset",
        "exo-ui:CreateAssetAction",
        "exo:Prototype",
    ),
    (
        "Action_location",
        "DatatypeProperty",
        "location",
        "For CreateAssetAction: folder path for new asset (supports templates)",
        "exo-ui:CreateAssetAction",
        "xsd:string",
    ),
    (
        "Action_targetProperty",
        "ObjectProperty",
        "target property",
        "For UpdatePropertyAction: property to update",
        "exo-ui:UpdatePropertyAction",
        "rdf:Property",
    ),
    (
        "Action_targetValue",
        "DatatypeProperty",
        "target value",
        "For UpdatePropertyAction: new value (can be literal or URI)",
        "exo-ui:UpdatePropertyAction",
        None,
    ),  # No range specified
    (
        "Action_targetAsset",
        "ObjectProperty",
        "target asset",
        "For UpdatePropertyAction: asset to update (default: current asset)",
        "exo-ui:UpdatePropertyAction",
        "exo:Asset",
    ),
    (
        "Action_target",
        "DatatypeProperty",
        "target",
        "For NavigateAction: asset URI or SPARQL SELECT query",
        "exo-ui:NavigateAction",
        "xsd:string",
    ),
    (
        "Action_query",
        "DatatypeProperty",
        "query",
        "For ExecuteSPARQLAction: SPARQL query to execute",
        "exo-ui:ExecuteSPARQLAction",
        "xsd:string",
    ),
    (
        "Action_modalType",
        "DatatypeProperty",
        "modal type",
        "For ShowModalAction: type of modal (confirm, input, select, custom)",
        "exo-ui:ShowModalAction",
        "xsd:string",
    ),
    (
        "Action_modalParams",
        "DatatypeProperty",
        "modal params",
        "For ShowModalAction: JSON parameters for modal",
        "exo-ui:ShowModalAction",
        "xsd:string",
    ),
    (
        "Action_handler",
        "DatatypeProperty",
        "handler",
        "For CustomHandlerAction: registered TypeScript handler ID",
        "exo-ui:CustomHandlerAction",
        "xsd:string",
    ),
    (
        "Action_actions",
        "ObjectProperty",
        "actions",
        "For CompositeAction: ordered list of actions to execute",
        "exo-ui:CompositeAction",
        "rdf:List",
    ),
    # Condition properties (7)
    (
        "Condition_sparql",
        "DatatypeProperty",
        "SPARQL condition",
        "ASK query that returns true/false. Variable ?asset bound to current asset.",
        "exo-ui:Condition",
        "xsd:string",
    ),
    (
        "Condition_assetClass",
        "ObjectProperty",
        "asset class",
        "Simple condition: current asset must be instance of this class",
        "exo-ui:Condition",
        "owl:Class",
    ),
    (
        "Condition_hasProperty",
        "ObjectProperty",
        "has property",
        "Simple condition: current asset must have this property",
        "exo-ui:Condition",
        "rdf:Property",
    ),
    (
        "Condition_propertyValue",
        "DatatypeProperty",
        "property value",
        "Simple condition: property must equal this value",
        "exo-ui:Condition",
        None,
    ),  # No range specified
    (
        "Condition_not",
        "ObjectProperty",
        "not",
        "Negation: condition must be false",
        "exo-ui:Condition",
        "exo-ui:Condition",
    ),
    (
        "Condition_and",
        "ObjectProperty",
        "and",
        "Conjunction: all conditions must be true",
        "exo-ui:Condition",
        "rdf:List",
    ),
    (
        "Condition_or",
        "ObjectProperty",
        "or",
        "Disjunction: at least one condition must be true",
        "exo-ui:Condition",
        "rdf:List",
    ),
    # ButtonGroup properties (3)
    (
        "ButtonGroup_order",
        "DatatypeProperty",
        "order",
        "Display order of button group",
        "exo-ui:ButtonGroup",
        "xsd:integer",
    ),
    (
        "ButtonGroup_collapsible",
        "DatatypeProperty",
        "collapsible",
        "Whether group can be collapsed",
        "exo-ui:ButtonGroup",
        "xsd:boolean",
    ),
    (
        "ButtonGroup_defaultCollapsed",
        "DatatypeProperty",
        "default collapsed",
        "Whether group is collapsed by default",
        "exo-ui:ButtonGroup",
        "xsd:boolean",
    ),
    # CLI-specific Action properties (3)
    (
        "Action_headless",
        "DatatypeProperty",
        "headless",
        "Whether action can execute without UI (CLI mode). True = works in CLI+Obsidian, False = Obsidian only.",
        "exo-ui:Action",
        "xsd:boolean",
    ),
    (
        "Action_cliAlternative",
        "DatatypeProperty",
        "CLI alternative",
        "CLI argument syntax that replaces UI interaction. Example: '--reason \"text\"' instead of modal.",
        "exo-ui:Action",
        "xsd:string",
    ),
    (
        "Action_cliCommand",
        "DatatypeProperty",
        "CLI command",
        "Full CLI command equivalent. Example: 'exocortex command complete --file {{asset}}'.",
        "exo-ui:Action",
        "xsd:string",
    ),
]


def main():
    repo_root = Path(__file__).parent.parent
    output_dir = repo_root / "exo-ui"

    print(f"Creating property files in {output_dir}")

    for prop_name, prop_type, label, comment, domain, range_type in PROPERTIES:
        uri = f"https://exocortex.my/ontology/exo-ui#{prop_name}"
        print(f"  Creating {prop_name}...")

        # Create anchor
        prop_uuid = create_anchor_file(output_dir, prop_name, uri)
        prop_alias = f"exo-ui:{prop_name}"

        # Create rdf:type statement
        owl_type = f"owl:{prop_type}"
        create_statement_file(output_dir, prop_uuid, prop_alias, PREDICATE_UUIDS["rdf:type"], "a", owl_type, owl_type)

        # Create rdfs:label statement
        label_literal = f'"{label}"'
        create_statement_file(
            output_dir, prop_uuid, prop_alias, PREDICATE_UUIDS["rdfs:label"], "rdfs:label", label_literal, label_literal
        )

        # Create rdfs:comment statement
        comment_literal = f'"{comment}"'
        create_statement_file(
            output_dir,
            prop_uuid,
            prop_alias,
            PREDICATE_UUIDS["rdfs:comment"],
            "rdfs:comment",
            comment_literal,
            comment_literal,
        )

        # Create rdfs:domain statement
        create_statement_file(
            output_dir, prop_uuid, prop_alias, PREDICATE_UUIDS["rdfs:domain"], "rdfs:domain", domain, domain
        )

        # Create rdfs:range statement (if specified)
        if range_type:
            create_statement_file(
                output_dir, prop_uuid, prop_alias, PREDICATE_UUIDS["rdfs:range"], "rdfs:range", range_type, range_type
            )

    print(f"\nCreated files for {len(PROPERTIES)} properties")
    print("Run validation: python scripts/validate.py exo-ui")


if __name__ == "__main__":
    main()

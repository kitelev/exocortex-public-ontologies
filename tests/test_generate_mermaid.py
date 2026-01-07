#!/usr/bin/env python3
"""Tests for generate_mermaid.py"""

import sys
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from generate_mermaid import (  # noqa: E402
    parse_frontmatter_fast,
    extract_wikilink_uuid,
    sanitize_mermaid_id,
    get_label,
    collect_ontology_data,
    generate_class_diagram,
)


class TestParseFrontmatterFast:
    """Tests for parse_frontmatter_fast."""

    def test_valid_anchor(self, tmp_path):
        """Test parsing valid anchor frontmatter."""
        file = tmp_path / "test.md"
        file.write_text(
            """---
metadata: anchor
uri: http://example.org/Test
aliases:
  - "example:Test"
---
"""
        )
        data = parse_frontmatter_fast(file)
        assert data is not None
        assert data["metadata"] == "anchor"
        assert data["aliases"] == ["example:Test"]

    def test_valid_statement(self, tmp_path):
        """Test parsing valid statement frontmatter."""
        file = tmp_path / "test.md"
        file.write_text(
            """---
metadata: statement
subject: "[[uuid1]]"
predicate: "[[uuid2]]"
object: "[[uuid3]]"
aliases:
  - "test alias"
---
"""
        )
        data = parse_frontmatter_fast(file)
        assert data is not None
        assert data["metadata"] == "statement"
        assert "[[uuid1]]" in data["subject"]

    def test_no_frontmatter(self, tmp_path):
        """Test parsing file without frontmatter returns None."""
        file = tmp_path / "test.md"
        file.write_text("No frontmatter here")
        data = parse_frontmatter_fast(file)
        assert data is None

    def test_incomplete_frontmatter(self, tmp_path):
        """Test parsing incomplete frontmatter returns partial data."""
        file = tmp_path / "test.md"
        file.write_text(
            """---
metadata: anchor
no closing delimiter
"""
        )
        data = parse_frontmatter_fast(file)
        # Parser returns partial data for incomplete frontmatter
        assert data is None or data.get("metadata") == "anchor"


class TestExtractWikilinkUuid:
    """Tests for extract_wikilink_uuid."""

    def test_simple_wikilink(self):
        """Test extracting UUID from simple wikilink."""
        result = extract_wikilink_uuid("[[uuid-123]]")
        assert result == "uuid-123"

    def test_wikilink_with_alias(self):
        """Test extracting UUID from wikilink with alias."""
        result = extract_wikilink_uuid("[[uuid-456|Some Alias]]")
        assert result == "uuid-456"

    def test_empty_string(self):
        """Test empty string returns None."""
        result = extract_wikilink_uuid("")
        assert result is None

    def test_none_input(self):
        """Test None input returns None."""
        result = extract_wikilink_uuid(None)
        assert result is None

    def test_no_wikilink(self):
        """Test string without wikilink returns None."""
        result = extract_wikilink_uuid("just a string")
        assert result is None


class TestSanitizeMermaidId:
    """Tests for sanitize_mermaid_id."""

    def test_simple_text(self):
        """Test simple alphanumeric text."""
        result = sanitize_mermaid_id("FoafPerson")
        assert result == "FoafPerson"

    def test_colon_replaced(self):
        """Test colon is replaced with underscore."""
        result = sanitize_mermaid_id("foaf:Person")
        assert result == "foaf_Person"

    def test_leading_digit(self):
        """Test leading digit gets underscore prefix."""
        result = sanitize_mermaid_id("123abc")
        assert result == "_123abc"

    def test_special_chars(self):
        """Test special characters are replaced."""
        result = sanitize_mermaid_id("test-name.with.dots")
        assert "_" in result
        assert "-" not in result
        assert "." not in result

    def test_empty_string(self):
        """Test empty string returns empty."""
        result = sanitize_mermaid_id("")
        assert result == ""


class TestGetLabel:
    """Tests for get_label."""

    def test_known_uuid(self):
        """Test getting label for known UUID."""
        data = {
            "uuid_to_info": {
                "test-uuid": {
                    "prefix": "foaf",
                    "local": "Person",
                    "prefix_local": "foaf:Person",
                }
            }
        }
        result = get_label("test-uuid", data)
        assert result == "foaf:Person"

    def test_unknown_uuid(self):
        """Test getting label for unknown UUID returns truncated UUID."""
        data = {"uuid_to_info": {}}
        result = get_label("abcdefgh-1234-5678", data)
        assert result == "abcdefgh"  # First 8 chars

    def test_local_only(self):
        """Test getting label when only local is available."""
        data = {
            "uuid_to_info": {
                "test-uuid": {
                    "prefix": "test",
                    "local": "Thing",
                    "prefix_local": "",
                }
            }
        }
        result = get_label("test-uuid", data)
        assert result == "Thing"


class TestCollectOntologyData:
    """Tests for collect_ontology_data."""

    def test_collect_from_empty_namespace(self, tmp_path):
        """Test collecting from empty namespace returns empty data."""
        ns_dir = tmp_path / "empty"
        ns_dir.mkdir()

        # Need to mock PREFIXES or pass the path
        data = collect_ontology_data(tmp_path, "nonexistent")

        assert data["classes"] == set()
        assert data["properties"] == {}

    def test_collects_blank_nodes(self, tmp_path):
        """Test that blank nodes are tracked."""
        ns_dir = tmp_path / "test"
        ns_dir.mkdir()

        # Create blank node file
        bn_file = ns_dir / "blank-node-uuid.md"
        bn_file.write_text(
            """---
metadata: blank_node
uri: http://example.org/.well-known/genid/123
aliases:
  - "_:genid-123"
---
"""
        )

        data = collect_ontology_data(tmp_path, "test")

        assert "blank-node-uuid" in data["blank_nodes"]


class TestGenerateClassDiagram:
    """Tests for generate_class_diagram."""

    def test_empty_data_returns_header_only(self):
        """Test empty data returns just classDiagram header."""
        data = {
            "uuid_to_info": {},
            "classes": set(),
            "properties": {},
            "subclass_of": {},
            "blank_nodes": set(),
        }
        result = generate_class_diagram(data)
        assert result.strip() == "classDiagram"

    def test_single_class(self):
        """Test diagram with single class."""
        data = {
            "uuid_to_info": {
                "class-uuid": {
                    "prefix": "test",
                    "local": "MyClass",
                    "prefix_local": "test:MyClass",
                }
            },
            "classes": {"class-uuid"},
            "properties": {},
            "subclass_of": {},
            "blank_nodes": set(),
        }
        result = generate_class_diagram(data)
        assert "class test_MyClass" in result

    def test_blank_nodes_filtered(self):
        """Test blank nodes are filtered from classes."""
        data = {
            "uuid_to_info": {
                "class-uuid": {
                    "prefix": "test",
                    "local": "MyClass",
                    "prefix_local": "test:MyClass",
                },
                "blank-uuid": {
                    "prefix": "test",
                    "local": "",
                    "prefix_local": "",
                },
            },
            "classes": {"class-uuid", "blank-uuid"},
            "properties": {},
            "subclass_of": {},
            "blank_nodes": {"blank-uuid"},
        }
        result = generate_class_diagram(data)
        assert "test_MyClass" in result
        assert "blank-uuid" not in result

    def test_inheritance_relationship(self):
        """Test inheritance relationship is generated."""
        data = {
            "uuid_to_info": {
                "child-uuid": {
                    "prefix": "test",
                    "local": "Child",
                    "prefix_local": "test:Child",
                },
                "parent-uuid": {
                    "prefix": "test",
                    "local": "Parent",
                    "prefix_local": "test:Parent",
                },
            },
            "classes": {"child-uuid"},
            "properties": {},
            "subclass_of": {"child-uuid": ["parent-uuid"]},
            "blank_nodes": set(),
        }
        result = generate_class_diagram(data)
        assert "test_Parent <|-- test_Child" in result

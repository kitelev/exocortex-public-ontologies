#!/usr/bin/env python3
"""Tests for check_consistency.py"""

import sys
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from check_consistency import (  # noqa: E402
    parse_frontmatter,
    extract_wikilinks,
    get_prefix_from_uri,
    NS_URI_TO_PREFIX,
    PREFIXES,
)


class TestParseFrontmatter:
    """Tests for parse_frontmatter function."""

    def test_valid_frontmatter(self, tmp_path):
        """Test parsing valid frontmatter."""
        file = tmp_path / "test.md"
        file.write_text(
            """---
metadata: anchor
uri: "http://example.org/test#Thing"
aliases:
  - "test:Thing"
---
"""
        )
        data, error = parse_frontmatter(file)

        assert error is None
        assert data is not None
        assert data["metadata"] == "anchor"
        assert data["uri"] == "http://example.org/test#Thing"

    def test_no_frontmatter(self, tmp_path):
        """Test file without frontmatter."""
        file = tmp_path / "test.md"
        file.write_text("No frontmatter here")

        data, error = parse_frontmatter(file)

        assert data is None
        assert error == "No frontmatter"

    def test_invalid_yaml(self, tmp_path):
        """Test file with invalid YAML."""
        file = tmp_path / "test.md"
        file.write_text(
            """---
invalid: yaml: content
---
"""
        )
        data, error = parse_frontmatter(file)

        assert data is None
        assert "YAML error" in error


class TestExtractWikilinks:
    """Tests for extract_wikilinks function."""

    def test_extract_simple_wikilinks(self):
        """Test extracting simple wikilinks."""
        data = {
            "subject": "[[uuid1]]",
            "predicate": "[[uuid2]]",
            "object": "[[uuid3]]",
        }

        links = extract_wikilinks(data)

        assert "uuid1" in links
        assert "uuid2" in links
        assert "uuid3" in links

    def test_extract_aliased_wikilinks(self):
        """Test extracting wikilinks with aliases."""
        data = {
            "subject": "[[uuid1|Some Label]]",
            "predicate": "[[uuid2|rdf:type]]",
        }

        links = extract_wikilinks(data)

        assert "uuid1" in links
        assert "uuid2" in links
        # Aliases should not be extracted as links
        assert "Some Label" not in links

    def test_no_wikilinks(self):
        """Test data without wikilinks."""
        data = {
            "subject": "literal value",
            "predicate": "another value",
        }

        links = extract_wikilinks(data)

        assert len(links) == 0


class TestGetPrefixFromUri:
    """Tests for get_prefix_from_uri function."""

    def test_known_prefixes(self):
        """Test getting prefix from known URIs."""
        assert get_prefix_from_uri("http://www.w3.org/1999/02/22-rdf-syntax-ns#type") == "rdf"
        assert get_prefix_from_uri("http://www.w3.org/2000/01/rdf-schema#Class") == "rdfs"
        assert get_prefix_from_uri("http://www.w3.org/2002/07/owl#Thing") == "owl"
        assert get_prefix_from_uri("http://www.w3.org/ns/shacl#NodeShape") == "sh"

    def test_unknown_uri(self):
        """Test unknown URI returns None."""
        assert get_prefix_from_uri("http://unknown.org/something#thing") is None

    def test_empty_uri(self):
        """Test empty URI returns None."""
        assert get_prefix_from_uri("") is None


class TestNamespaceMappings:
    """Tests for namespace mappings."""

    def test_all_prefixes_have_mapping(self):
        """Test all PREFIXES have corresponding NS_URI_TO_PREFIX entry."""
        mapped_prefixes = set(NS_URI_TO_PREFIX.values())

        for prefix in PREFIXES:
            assert prefix in mapped_prefixes, f"Missing mapping for prefix: {prefix}"

    def test_no_duplicate_prefixes(self):
        """Test no duplicate prefixes in list."""
        assert len(PREFIXES) == len(set(PREFIXES))

    def test_expected_prefixes(self):
        """Test expected prefixes are present."""
        expected = ["rdf", "rdfs", "owl", "xsd", "dc", "dcterms", "skos", "foaf", "sh", "sosa", "as"]

        for prefix in expected:
            assert prefix in PREFIXES, f"Missing expected prefix: {prefix}"

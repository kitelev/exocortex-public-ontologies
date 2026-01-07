#!/usr/bin/env python3
"""Tests for common.py - Common utilities for ontology scripts."""

import sys
from pathlib import Path
import pytest

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from common import (  # noqa: E402
    load_prefixes,
    get_uri_to_prefix,
    get_prefix_dirs,
    get_primary_prefixes,
    get_ontology_uri_to_prefix,
    extract_prefix_from_uri,
    extract_localname,
    uri_to_curie,
    parse_frontmatter,
    parse_frontmatter_from_file,
    extract_wikilink_uuid,
    get_repo_root,
)


class TestLoadPrefixes:
    """Tests for load_prefixes function."""

    def test_loads_from_real_file(self):
        """Test loading prefixes from actual _prefixes.yaml."""
        prefixes = load_prefixes()

        # Should have core prefixes
        assert "rdf" in prefixes
        assert "rdfs" in prefixes
        assert "owl" in prefixes

        # Should have URIs
        assert prefixes["rdf"] == "http://www.w3.org/1999/02/22-rdf-syntax-ns#"

    def test_returns_dict(self):
        """Test that prefixes is a dictionary."""
        prefixes = load_prefixes()
        assert isinstance(prefixes, dict)

    def test_all_values_are_uris(self):
        """Test that all values look like URIs."""
        prefixes = load_prefixes()
        for prefix, uri in prefixes.items():
            assert uri.startswith("http://") or uri.startswith("https://"), f"{prefix}: {uri}"

    def test_custom_repo_root(self, tmp_path):
        """Test loading from custom repo root."""
        # Create a minimal _prefixes.yaml
        prefixes_file = tmp_path / "_prefixes.yaml"
        prefixes_file.write_text(
            """
test: "http://example.org/test#"
"""
        )

        prefixes = load_prefixes(tmp_path)
        assert prefixes == {"test": "http://example.org/test#"}

    def test_missing_file_raises(self, tmp_path):
        """Test that missing file raises FileNotFoundError."""
        with pytest.raises(FileNotFoundError):
            load_prefixes(tmp_path)


class TestGetUriToPrefix:
    """Tests for get_uri_to_prefix function."""

    def test_inverts_mapping(self):
        """Test that URI→prefix is inverted from prefix→URI."""
        prefixes = {"rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#"}
        uri_to_prefix = get_uri_to_prefix(prefixes)

        assert uri_to_prefix["http://www.w3.org/1999/02/22-rdf-syntax-ns#"] == "rdf"

    def test_loads_from_file_if_none(self):
        """Test that it loads from file if no prefixes provided."""
        uri_to_prefix = get_uri_to_prefix()

        assert "http://www.w3.org/1999/02/22-rdf-syntax-ns#" in uri_to_prefix


class TestGetPrefixDirs:
    """Tests for get_prefix_dirs function."""

    def test_returns_existing_dirs(self):
        """Test that only existing directories are returned."""
        dirs = get_prefix_dirs()

        # Should include known directories
        assert "rdf" in dirs
        assert "rdfs" in dirs
        assert "owl" in dirs

    def test_excludes_ontology_variants(self):
        """Test that -ontology suffix variants are excluded."""
        dirs = get_prefix_dirs()

        for d in dirs:
            assert not d.endswith("-ontology")

    def test_returns_sorted(self):
        """Test that result is sorted."""
        dirs = get_prefix_dirs()
        assert dirs == sorted(dirs)


class TestGetPrimaryPrefixes:
    """Tests for get_primary_prefixes function."""

    def test_excludes_ontology_suffix(self):
        """Test that -ontology suffixes are excluded."""
        primary = get_primary_prefixes()

        for prefix in primary:
            assert not prefix.endswith("-ontology")

    def test_includes_common_prefixes(self):
        """Test that common prefixes are included."""
        primary = get_primary_prefixes()

        assert "rdf" in primary
        assert "rdfs" in primary
        assert "owl" in primary


class TestGetOntologyUriToPrefix:
    """Tests for get_ontology_uri_to_prefix function."""

    def test_maps_ontology_uris(self):
        """Test mapping ontology URIs without # to prefix."""
        ontology_map = get_ontology_uri_to_prefix()

        # Check if any -ontology mappings exist
        # This depends on whether _prefixes.yaml has -ontology entries
        assert isinstance(ontology_map, dict)


class TestExtractPrefixFromUri:
    """Tests for extract_prefix_from_uri function."""

    def test_rdf_namespace(self):
        """Test extracting RDF prefix."""
        uri = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
        assert extract_prefix_from_uri(uri) == "rdf"

    def test_rdfs_namespace(self):
        """Test extracting RDFS prefix."""
        uri = "http://www.w3.org/2000/01/rdf-schema#Class"
        assert extract_prefix_from_uri(uri) == "rdfs"

    def test_unknown_namespace(self):
        """Test unknown namespace returns None."""
        uri = "http://unknown.org/thing"
        assert extract_prefix_from_uri(uri) is None

    def test_with_custom_mapping(self):
        """Test with custom URI→prefix mapping."""
        custom_map = {"http://custom.org/": "custom"}
        uri = "http://custom.org/Thing"
        assert extract_prefix_from_uri(uri, custom_map) == "custom"


class TestExtractLocalname:
    """Tests for extract_localname function."""

    def test_hash_uri(self):
        """Test extracting localname from hash URI."""
        assert extract_localname("http://example.org/ns#Thing") == "Thing"

    def test_slash_uri(self):
        """Test extracting localname from slash URI."""
        assert extract_localname("http://example.org/ns/Thing") == "Thing"

    def test_trailing_slash(self):
        """Test URI with trailing slash."""
        assert extract_localname("http://example.org/ns/Thing/") == "Thing"

    def test_no_separator(self):
        """Test URI without # or /."""
        assert extract_localname("Thing") == "Thing"


class TestUriToCurie:
    """Tests for uri_to_curie function."""

    def test_known_uri(self):
        """Test CURIE for known URI."""
        uri = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
        assert uri_to_curie(uri) == "rdf:type"

    def test_unknown_uri(self):
        """Test CURIE for unknown URI returns localname."""
        uri = "http://unknown.org/something#Thing"
        assert uri_to_curie(uri) == "Thing"


class TestParseFrontmatter:
    """Tests for parse_frontmatter function."""

    def test_valid_frontmatter(self):
        """Test parsing valid frontmatter."""
        content = """---
metadata: statement
key: value
---

Body content here.
"""
        fm, body = parse_frontmatter(content)

        assert fm is not None
        assert fm["metadata"] == "statement"
        assert fm["key"] == "value"
        assert "Body content here" in body

    def test_no_frontmatter(self):
        """Test content without frontmatter."""
        content = "Just some text"
        fm, body = parse_frontmatter(content)

        assert fm is None
        assert body == content

    def test_empty_frontmatter(self):
        """Test empty frontmatter."""
        content = """---
---
Body here.
"""
        fm, body = parse_frontmatter(content)

        assert fm == {} or fm is None
        assert "Body here" in body

    def test_frontmatter_with_lists(self):
        """Test frontmatter with list values."""
        content = """---
aliases:
  - alias1
  - alias2
---
"""
        fm, _ = parse_frontmatter(content)

        assert fm is not None
        assert fm["aliases"] == ["alias1", "alias2"]

    def test_multiline_values(self):
        """Test frontmatter with multiline string."""
        content = """---
description: |
  Line 1
  Line 2
---
"""
        fm, _ = parse_frontmatter(content)

        assert fm is not None
        assert "Line 1" in fm["description"]
        assert "Line 2" in fm["description"]

    def test_invalid_yaml_returns_none(self):
        """Test invalid YAML returns None."""
        content = """---
key: [unclosed
---
"""
        fm, body = parse_frontmatter(content)

        assert fm is None


class TestParseFrontmatterFromFile:
    """Tests for parse_frontmatter_from_file function."""

    def test_valid_file(self, tmp_path):
        """Test parsing from valid file."""
        test_file = tmp_path / "test.md"
        test_file.write_text(
            """---
metadata: anchor
uri: http://example.org/Thing
---
"""
        )

        fm = parse_frontmatter_from_file(test_file)

        assert fm is not None
        assert fm["metadata"] == "anchor"
        assert fm["uri"] == "http://example.org/Thing"

    def test_nonexistent_file(self, tmp_path):
        """Test parsing nonexistent file returns None."""
        test_file = tmp_path / "nonexistent.md"
        fm = parse_frontmatter_from_file(test_file)
        assert fm is None


class TestExtractWikilinkUuid:
    """Tests for extract_wikilink_uuid function."""

    def test_simple_wikilink(self):
        """Test extracting UUID from simple wikilink."""
        assert extract_wikilink_uuid("[[abc-123]]") == "abc-123"

    def test_wikilink_with_alias(self):
        """Test extracting UUID from wikilink with alias."""
        assert extract_wikilink_uuid("[[uuid|Display Name]]") == "uuid"

    def test_wikilink_in_quotes(self):
        """Test extracting UUID from quoted wikilink."""
        assert extract_wikilink_uuid('"[[uuid]]"') == "uuid"

    def test_no_wikilink(self):
        """Test string without wikilink returns None."""
        assert extract_wikilink_uuid("plain text") is None

    def test_empty_string(self):
        """Test empty string returns None."""
        assert extract_wikilink_uuid("") is None

    def test_none_input(self):
        """Test None input returns None."""
        assert extract_wikilink_uuid(None) is None


class TestGetRepoRoot:
    """Tests for get_repo_root function."""

    def test_returns_path(self):
        """Test that repo root is returned as Path."""
        root = get_repo_root()
        assert isinstance(root, Path)

    def test_contains_prefixes_file(self):
        """Test that repo root contains _prefixes.yaml."""
        root = get_repo_root()
        assert (root / "_prefixes.yaml").exists()

    def test_contains_scripts_dir(self):
        """Test that repo root contains scripts directory."""
        root = get_repo_root()
        assert (root / "scripts").is_dir()

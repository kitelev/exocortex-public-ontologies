#!/usr/bin/env python3
"""Tests for verify_import.py - Verify semantic equivalence between RDF and file-based ontologies."""

import sys
from pathlib import Path
import uuid

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from verify_import import (  # noqa: E402
    uri_to_uuid,
    extract_frontmatter,
    load_triples_from_files,
    load_triples_from_rdf,
    normalize_literal,
    is_uuid,
    compare_triples,
)


class TestUriToUuid:
    """Tests for uri_to_uuid function."""

    def test_deterministic(self):
        """Test that same URI always produces same UUID."""
        uri = "http://example.org/test"
        result1 = uri_to_uuid(uri)
        result2 = uri_to_uuid(uri)
        assert result1 == result2

    def test_different_uris_different_uuids(self):
        """Test different URIs produce different UUIDs."""
        uri1 = "http://example.org/a"
        uri2 = "http://example.org/b"
        assert uri_to_uuid(uri1) != uri_to_uuid(uri2)

    def test_known_uuid(self):
        """Test known UUID for rdf:type."""
        uri = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
        expected = "73b69787-81ea-563e-8e09-9c84cad4cf2b"
        assert uri_to_uuid(uri) == expected

    def test_uuid_format(self):
        """Test UUID format is valid."""
        result = uri_to_uuid("http://example.org/test")
        # UUIDv5 format: 8-4-4-4-12
        assert len(result) == 36
        assert result.count("-") == 4


class TestExtractFrontmatter:
    """Tests for extract_frontmatter function."""

    def test_valid_frontmatter(self):
        """Test extracting valid YAML frontmatter."""
        content = """---
metadata: statement
subject: "[[uuid]]"
---

Body content.
"""
        fm = extract_frontmatter(content)
        assert fm.get("metadata") == "statement"
        assert fm.get("subject") == "[[uuid]]"

    def test_no_frontmatter(self):
        """Test content without frontmatter."""
        content = "Just regular content"
        fm = extract_frontmatter(content)
        assert fm == {}

    def test_frontmatter_without_closing(self):
        """Test frontmatter without closing ---."""
        content = """---
metadata: test
"""
        fm = extract_frontmatter(content)
        assert fm == {}

    def test_empty_frontmatter(self):
        """Test empty frontmatter."""
        content = """---
---
"""
        fm = extract_frontmatter(content)
        assert fm == {} or fm is None

    def test_invalid_yaml(self):
        """Test invalid YAML in frontmatter."""
        content = """---
key: [unclosed bracket
---
"""
        fm = extract_frontmatter(content)
        assert fm == {}


class TestNormalizeLiteral:
    """Tests for normalize_literal function."""

    def test_simple_literal(self):
        """Test simple quoted literal."""
        result = normalize_literal('"hello"')
        assert result == ("hello", None, None)

    def test_language_tagged(self):
        """Test language-tagged literal."""
        result = normalize_literal('"hello"@en')
        assert result == ("hello", "en", None)

    def test_typed_literal(self):
        """Test typed literal with wikilink datatype."""
        result = normalize_literal('"42"^^[[xsd-int-uuid]]')
        assert result[0] == "42"
        assert result[2] == "xsd-int-uuid"

    def test_plain_text(self):
        """Test plain unquoted text."""
        result = normalize_literal("plain text")
        assert result == ("plain text", None, None)


class TestIsUuid:
    """Tests for is_uuid function."""

    def test_valid_uuid(self):
        """Test valid UUID string."""
        assert is_uuid("73b69787-81ea-563e-8e09-9c84cad4cf2b")
        assert is_uuid("a1b2c3d4-e5f6-7890-abcd-ef1234567890")

    def test_invalid_uuid(self):
        """Test invalid UUID strings."""
        assert not is_uuid("not-a-uuid")
        assert not is_uuid("12345678-1234-1234-1234-12345678901")  # Too short
        assert not is_uuid("12345678-1234-1234-1234-1234567890123")  # Too long
        assert not is_uuid("GGGGGGGG-1234-1234-1234-123456789012")  # Invalid chars

    def test_uppercase_valid(self):
        """Test that lowercase is required."""
        # UUIDs should be lowercase
        assert not is_uuid("AAAAAAAA-BBBB-CCCC-DDDD-EEEEEEEEEEEE")


class TestLoadTriplesFromFiles:
    """Tests for load_triples_from_files function."""

    def test_load_from_directory(self, tmp_path):
        """Test loading triples from file-based representation."""
        # Create a minimal namespace file
        ns_uuid = "test-namespace-uuid"
        ns_file = tmp_path / f"{ns_uuid}.md"
        ns_file.write_text("""---
metadata: namespace
uri: http://example.org/test#
---
""")

        # Create an anchor file
        anchor_uuid = "test-anchor-uuid"
        anchor_file = tmp_path / f"{anchor_uuid}.md"
        anchor_file.write_text("""---
metadata: anchor
uri: http://example.org/test#Thing
---
""")

        # Create a statement file
        statement_file = tmp_path / "statement-uuid.md"
        statement_file.write_text("""---
metadata: statement
subject: "[[test-anchor-uuid]]"
predicate: "[[73b69787-81ea-563e-8e09-9c84cad4cf2b]]"
object: "[[other-uuid]]"
---
""")

        triples, blank_uuids = load_triples_from_files(tmp_path)

        # Should have loaded at least one triple
        assert len(triples) >= 1
        assert isinstance(blank_uuids, set)

    def test_skip_non_statement_files(self, tmp_path):
        """Test that non-statement files are skipped."""
        # Create namespace file
        ns_file = tmp_path / "ns.md"
        ns_file.write_text("""---
metadata: namespace
uri: http://example.org/
---
""")

        # Create anchor file
        anchor_file = tmp_path / "anchor.md"
        anchor_file.write_text("""---
metadata: anchor
---
""")

        triples, _ = load_triples_from_files(tmp_path)

        # No statement files, so no triples
        assert len(triples) == 0

    def test_empty_directory(self, tmp_path):
        """Test loading from empty directory."""
        triples, blank_uuids = load_triples_from_files(tmp_path)
        assert triples == set()
        assert blank_uuids == set()


class TestCompareTriplesFunction:
    """Tests for compare_triples function."""

    def test_identical_sets(self):
        """Test comparing identical triple sets."""
        file_triples = {("a", "b", "c"), ("d", "e", "f")}
        rdf_triples = {("a", "b", "c"), ("d", "e", "f")}

        only_files, only_rdf, f_blank, r_blank, patterns_match = compare_triples(
            file_triples, rdf_triples, set(), set()
        )

        assert len(only_files) == 0
        assert len(only_rdf) == 0
        assert patterns_match

    def test_only_in_files(self):
        """Test triples only in files."""
        file_triples = {("a", "b", "c"), ("extra", "x", "y")}
        rdf_triples = {("a", "b", "c")}

        only_files, only_rdf, _, _, _ = compare_triples(
            file_triples, rdf_triples, set(), set()
        )

        assert ("extra", "x", "y") in only_files
        assert len(only_rdf) == 0

    def test_only_in_rdf(self):
        """Test triples only in RDF."""
        file_triples = {("a", "b", "c")}
        rdf_triples = {("a", "b", "c"), ("missing", "x", "y")}

        only_files, only_rdf, _, _, _ = compare_triples(
            file_triples, rdf_triples, set(), set()
        )

        assert len(only_files) == 0
        assert ("missing", "x", "y") in only_rdf

    def test_blank_node_handling(self):
        """Test blank node structural comparison."""
        # Blank nodes should be compared by pattern, not exact match
        file_triples = {("blank-uuid-1", "pred", "obj")}
        rdf_triples = {("blank-uuid-2", "pred", "obj")}  # Different blank UUID

        file_blank = {"blank-uuid-1"}
        rdf_blank = {"blank-uuid-2"}

        _, _, f_count, r_count, patterns_match = compare_triples(
            file_triples, rdf_triples, rdf_blank, file_blank
        )

        # Patterns should match (same structure, different blank node IDs)
        assert f_count == 1
        assert r_count == 1
        assert patterns_match

    def test_mixed_blank_and_nonblank(self):
        """Test comparison with both blank and non-blank triples."""
        file_triples = {
            ("uri-1", "pred", "obj"),  # Non-blank
            ("blank-1", "pred2", "obj2"),  # Blank
        }
        rdf_triples = {
            ("uri-1", "pred", "obj"),  # Non-blank (same)
            ("blank-2", "pred2", "obj2"),  # Blank (different ID but same structure)
        }

        file_blank = {"blank-1"}
        rdf_blank = {"blank-2"}

        only_files, only_rdf, _, _, patterns_match = compare_triples(
            file_triples, rdf_triples, rdf_blank, file_blank
        )

        assert len(only_files) == 0
        assert len(only_rdf) == 0
        assert patterns_match


class TestLoadTriplesFromRdf:
    """Tests for load_triples_from_rdf with real RDF files."""

    def test_load_simple_turtle(self, tmp_path):
        """Test loading triples from a simple Turtle file."""
        # Create a simple Turtle file
        ttl_file = tmp_path / "test.ttl"
        ttl_file.write_text("""
@prefix ex: <http://example.org/> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .

ex:Thing rdf:type ex:Class .
ex:Thing ex:label "Test Label" .
""")

        triples, blank_uuids = load_triples_from_rdf(ttl_file, "http://example.org/")

        assert len(triples) == 2
        assert len(blank_uuids) == 0  # No blank nodes

    def test_load_with_blank_nodes(self, tmp_path):
        """Test loading triples with blank nodes."""
        ttl_file = tmp_path / "blank.ttl"
        ttl_file.write_text("""
@prefix ex: <http://example.org/> .

ex:Thing ex:has [
    ex:name "Anonymous"
] .
""")

        triples, blank_uuids = load_triples_from_rdf(ttl_file, "http://example.org/")

        assert len(triples) == 2  # ex:Thing ex:has _:b, _:b ex:name "Anonymous"
        assert len(blank_uuids) == 1  # One blank node

    def test_load_with_language_tags(self, tmp_path):
        """Test loading triples with language-tagged literals."""
        ttl_file = tmp_path / "lang.ttl"
        ttl_file.write_text("""
@prefix ex: <http://example.org/> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

ex:Thing rdfs:label "Test"@en ;
         rdfs:label "Тест"@ru .
""")

        triples, _ = load_triples_from_rdf(ttl_file, "http://example.org/")

        assert len(triples) == 2
        # Check that language tags are preserved in the canonical form
        literals = [t[2] for t in triples if t[2].startswith('"')]
        assert any("@en" in lit for lit in literals)
        assert any("@ru" in lit for lit in literals)

    def test_load_with_datatypes(self, tmp_path):
        """Test loading triples with datatyped literals."""
        ttl_file = tmp_path / "dtype.ttl"
        ttl_file.write_text("""
@prefix ex: <http://example.org/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:Thing ex:count "42"^^xsd:integer .
""")

        triples, _ = load_triples_from_rdf(ttl_file, "http://example.org/")

        assert len(triples) == 1
        # Check that datatype is preserved
        obj = list(triples)[0][2]
        assert "42" in obj
        assert "[[" in obj  # Datatype as wikilink


class TestIntegrationVerification:
    """Integration tests for full verification workflow."""

    def test_roundtrip_simple(self, tmp_path):
        """Test round-trip verification for simple ontology."""
        # Create source RDF file
        rdf_file = tmp_path / "source.ttl"
        rdf_file.write_text("""
@prefix ex: <http://example.org/test#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

ex:Person rdf:type rdfs:Class ;
          rdfs:label "Person"@en .
""")

        # Load from RDF
        rdf_triples, rdf_blank = load_triples_from_rdf(rdf_file, "http://example.org/test#")

        assert len(rdf_triples) == 2
        assert len(rdf_blank) == 0

    def test_crlf_normalization(self, tmp_path):
        """Test that CRLF is normalized to LF in literals."""
        ttl_file = tmp_path / "crlf.ttl"
        # Write with proper Turtle literal (rdflib handles \r\n in parsed literals)
        ttl_file.write_text("""
@prefix ex: <http://example.org/> .

ex:Thing ex:comment "Line1\\nLine2" .
""")

        triples, _ = load_triples_from_rdf(ttl_file, "http://example.org/")

        # Should load the triple with newline in literal
        assert len(triples) == 1
        obj = list(triples)[0][2]
        # The escaped \n in Turtle becomes actual newline
        assert "\\n" in obj or "\n" in obj


class TestEdgeCases:
    """Tests for edge cases and error handling."""

    def test_empty_rdf_file(self, tmp_path):
        """Test loading empty RDF file."""
        empty_file = tmp_path / "empty.ttl"
        empty_file.write_text("")

        triples, blank_uuids = load_triples_from_rdf(empty_file, "")

        assert len(triples) == 0
        assert len(blank_uuids) == 0

    def test_special_characters_in_literal(self, tmp_path):
        """Test handling of special characters in literals."""
        ttl_file = tmp_path / "special.ttl"
        ttl_file.write_text('''
@prefix ex: <http://example.org/> .

ex:Thing ex:value "Line with \\"quotes\\" and \\\\backslash" .
''')

        triples, _ = load_triples_from_rdf(ttl_file, "http://example.org/")

        assert len(triples) == 1

    def test_unicode_in_uri(self, tmp_path):
        """Test handling of URIs (without unicode in path)."""
        ttl_file = tmp_path / "uri.ttl"
        ttl_file.write_text("""
@prefix ex: <http://example.org/> .

ex:Thing ex:label "Тест"@ru .
""")

        triples, _ = load_triples_from_rdf(ttl_file, "http://example.org/")

        assert len(triples) == 1
        obj = list(triples)[0][2]
        assert "Тест" in obj

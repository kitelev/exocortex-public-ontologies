#!/usr/bin/env python3
"""
Tests for export_rdf.py - Export file-based ontologies to RDF format.
"""

import sys
from pathlib import Path

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from export_rdf import (  # noqa: E402
    parse_frontmatter,
    parse_wikilink,
    resolve_uuid_to_uri,
    parse_rdf_object_uuid,
    build_uuid_map,
    export_namespace,
    PREFIX_TO_URI,
    REPO_ROOT,
)
from rdflib import URIRef, Literal, BNode  # noqa: E402


class TestParseWikilink:
    """Tests for parse_wikilink function."""

    def test_simple_wikilink(self):
        """Test simple wikilink parsing."""
        assert parse_wikilink("[[rdf__type]]") == "rdf__type"

    def test_wikilink_with_alias(self):
        """Test wikilink with display alias."""
        assert parse_wikilink("[[uuid-here|Display Name]]") == "uuid-here"

    def test_wikilink_with_whitespace(self):
        """Test wikilink with surrounding whitespace."""
        assert parse_wikilink("  [[anchor]]  ") == "anchor"

    def test_invalid_wikilink_no_brackets(self):
        """Test invalid format without brackets."""
        assert parse_wikilink("not_a_wikilink") is None

    def test_invalid_wikilink_partial(self):
        """Test invalid format with partial brackets."""
        assert parse_wikilink("[single]") is None


class TestResolveUuidToUri:
    """Tests for resolve_uuid_to_uri function."""

    def test_known_uuid(self):
        """Test resolving a known UUID."""
        uuid_map = {"abc-123": "http://example.org/thing"}
        blank_nodes = {}
        term = resolve_uuid_to_uri("abc-123", uuid_map, blank_nodes)
        assert isinstance(term, URIRef)
        assert str(term) == "http://example.org/thing"

    def test_unknown_uuid_creates_bnode(self):
        """Test that unknown UUID creates a blank node."""
        uuid_map = {}
        blank_nodes = {}
        term = resolve_uuid_to_uri("unknown-uuid", uuid_map, blank_nodes)
        assert isinstance(term, BNode)
        assert "unknown-uuid" in blank_nodes

    def test_consistent_bnode(self):
        """Test that same UUID returns same blank node."""
        uuid_map = {}
        blank_nodes = {}
        term1 = resolve_uuid_to_uri("same-uuid", uuid_map, blank_nodes)
        term2 = resolve_uuid_to_uri("same-uuid", uuid_map, blank_nodes)
        assert term1 == term2


class TestParseRdfObjectUuid:
    """Tests for parse_rdf_object_uuid function."""

    def test_wikilink_object(self):
        """Test wikilink object parsing with UUID."""
        uuid_map = {"some-uuid": "http://example.org/Thing"}
        blank_nodes = {}
        term = parse_rdf_object_uuid("[[some-uuid]]", uuid_map, blank_nodes)
        assert isinstance(term, URIRef)
        assert str(term) == "http://example.org/Thing"

    def test_wikilink_with_alias(self):
        """Test wikilink with alias."""
        uuid_map = {"uuid-123": "http://example.org/Type"}
        blank_nodes = {}
        term = parse_rdf_object_uuid("[[uuid-123|Display Name]]", uuid_map, blank_nodes)
        assert isinstance(term, URIRef)
        assert str(term) == "http://example.org/Type"

    def test_external_uri(self):
        """Test external URI parsing."""
        uuid_map = {}
        blank_nodes = {}
        term = parse_rdf_object_uuid("<http://example.org/thing>", uuid_map, blank_nodes)
        assert isinstance(term, URIRef)
        assert str(term) == "http://example.org/thing"

    def test_language_tagged_literal(self):
        """Test language-tagged literal parsing."""
        uuid_map = {}
        blank_nodes = {}
        term = parse_rdf_object_uuid('"Hello"@en', uuid_map, blank_nodes)
        assert isinstance(term, Literal)
        assert str(term) == "Hello"
        assert term.language == "en"

    def test_datatyped_literal_uri(self):
        """Test datatyped literal with full URI."""
        uuid_map = {}
        blank_nodes = {}
        term = parse_rdf_object_uuid('"2024"^^<http://www.w3.org/2001/XMLSchema#gYear>', uuid_map, blank_nodes)
        assert isinstance(term, Literal)
        assert str(term) == "2024"
        assert "gYear" in str(term.datatype)

    def test_datatyped_literal_wikilink(self):
        """Test datatyped literal with wikilink format."""
        uuid_map = {"xsd-string-uuid": "http://www.w3.org/2001/XMLSchema#string"}
        blank_nodes = {}
        term = parse_rdf_object_uuid('"value"^^[[xsd-string-uuid]]', uuid_map, blank_nodes)
        assert isinstance(term, Literal)
        assert str(term) == "value"
        assert "string" in str(term.datatype)

    def test_plain_literal(self):
        """Test plain literal parsing."""
        uuid_map = {}
        blank_nodes = {}
        term = parse_rdf_object_uuid('"Just some text"', uuid_map, blank_nodes)
        assert isinstance(term, Literal)
        assert str(term) == "Just some text"

    def test_multiline_literal(self):
        """Test multiline literal preservation."""
        uuid_map = {}
        blank_nodes = {}
        term = parse_rdf_object_uuid('"Line 1\nLine 2"', uuid_map, blank_nodes)
        assert isinstance(term, Literal)
        assert "\n" in str(term)


class TestExportNamespace:
    """Integration tests for export_namespace function."""

    def test_export_rdf_namespace(self):
        """Test exporting the RDF namespace."""
        graph = export_namespace("rdf", verbose=False)
        # RDF namespace should have triples
        assert len(graph) > 0
        # Check for rdf:type triple
        type_uri = URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
        triples_with_type = list(graph.triples((type_uri, None, None)))
        assert len(triples_with_type) > 0

    def test_export_rdfs_namespace(self):
        """Test exporting the RDFS namespace."""
        graph = export_namespace("rdfs", verbose=False)
        assert len(graph) > 0
        # Check for rdfs:Class
        class_uri = URIRef("http://www.w3.org/2000/01/rdf-schema#Class")
        triples = list(graph.triples((class_uri, None, None)))
        assert len(triples) > 0

    def test_export_nonexistent_namespace(self):
        """Test exporting a nonexistent namespace."""
        graph = export_namespace("nonexistent_xyz_123", verbose=False)
        assert len(graph) == 0

    def test_export_owl_namespace(self):
        """Test exporting the OWL namespace."""
        graph = export_namespace("owl", verbose=False)
        assert len(graph) > 0

    def test_export_skos_namespace(self):
        """Test exporting the SKOS namespace."""
        graph = export_namespace("skos", verbose=False)
        assert len(graph) > 0


class TestRoundTrip:
    """Round-trip verification tests: export then check structural validity."""

    def test_rdf_round_trip_structure(self):
        """Test that RDF export has correct triple structure."""
        graph = export_namespace("rdf", verbose=False)

        # Every triple should have subject, predicate, object
        for s, p, o in graph:
            # Subject should be URI or BNode
            assert isinstance(s, (URIRef, BNode))
            # Predicate should be URI
            assert isinstance(p, URIRef)
            # Object should be URI, BNode, or Literal
            assert isinstance(o, (URIRef, BNode, Literal))

    def test_rdfs_labels_preserved(self):
        """Test that rdfs:label values are preserved in export."""
        graph = export_namespace("rdfs", verbose=False)

        label_uri = URIRef("http://www.w3.org/2000/01/rdf-schema#label")

        # Check that there are label triples
        labels = list(graph.triples((None, label_uri, None)))
        assert len(labels) > 0

        # All label values should be literals
        for _, _, obj in labels:
            assert isinstance(obj, Literal)

    def test_owl_class_types_preserved(self):
        """Test that rdf:type statements are preserved for OWL classes."""
        graph = export_namespace("owl", verbose=False)

        type_uri = URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")

        # Check that there are type triples
        types = list(graph.triples((None, type_uri, None)))
        assert len(types) > 0


class TestParseFrontmatter:
    """Tests for frontmatter parsing."""

    def test_parse_valid_frontmatter(self, tmp_path):
        """Test parsing valid frontmatter."""
        test_file = tmp_path / "test.md"
        test_file.write_text(
            """---
metadata: statement
subject: "[[abc]]"
predicate: "[[def]]"
object: "test value"
---

Content here.
"""
        )
        data, error = parse_frontmatter(test_file)
        assert error is None
        assert data is not None
        assert data["metadata"] == "statement"
        assert data["subject"] == "[[abc]]"

    def test_parse_no_frontmatter(self, tmp_path):
        """Test file without frontmatter."""
        test_file = tmp_path / "test.md"
        test_file.write_text("Just regular content\n")
        data, error = parse_frontmatter(test_file)
        assert data is None
        assert error == "No frontmatter"

    def test_parse_invalid_yaml(self, tmp_path):
        """Test file with invalid YAML frontmatter."""
        test_file = tmp_path / "test.md"
        test_file.write_text(
            """---
key: value
  bad_indent: oops
---
"""
        )
        data, error = parse_frontmatter(test_file)
        assert data is None
        assert error is not None


class TestBlankNodeHandling:
    """Tests for blank node handling in export."""

    def test_blank_nodes_created_consistently(self):
        """Test that blank nodes are created consistently for unknown UUIDs."""
        uuid_map = {}  # Empty map means UUID not found -> creates BNode
        blank_nodes = {}

        # First reference should create a new BNode
        term1 = resolve_uuid_to_uri("unknown-uuid-1", uuid_map, blank_nodes)
        assert isinstance(term1, BNode)

        # Second reference to same UUID should return same BNode
        term2 = resolve_uuid_to_uri("unknown-uuid-1", uuid_map, blank_nodes)
        assert term1 == term2

    def test_different_blank_nodes_different_bnodes(self):
        """Test that different unknown UUIDs create different BNodes."""
        uuid_map = {}
        blank_nodes = {}

        term1 = resolve_uuid_to_uri("uuid-a", uuid_map, blank_nodes)
        term2 = resolve_uuid_to_uri("uuid-b", uuid_map, blank_nodes)

        assert isinstance(term1, BNode)
        assert isinstance(term2, BNode)
        assert term1 != term2

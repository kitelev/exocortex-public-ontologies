#!/usr/bin/env python3
"""Tests for import_ontology.py"""

import sys
import uuid
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from import_ontology import (
    uri_to_uuid,
    extract_prefix_from_uri,
    extract_localname_from_uri,
    format_alias_value,
    literal_to_canonical,
    canonicalize_triple,
    NAMESPACE_URI_TO_PREFIX,
    ONTOLOGY_URI_TO_PREFIX,
)


class TestUriToUuid:
    """Tests for uri_to_uuid function."""

    def test_known_predicate(self):
        """Test UUID for rdf:type."""
        uri = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
        expected = "73b69787-81ea-563e-8e09-9c84cad4cf2b"
        
        assert uri_to_uuid(uri) == expected

    def test_known_class(self):
        """Test UUID for rdfs:Class."""
        uri = "http://www.w3.org/2000/01/rdf-schema#Class"
        
        result = uri_to_uuid(uri)
        
        assert len(result) == 36  # UUID format
        assert result.count('-') == 4

    def test_deterministic(self):
        """Test that same URI always gives same UUID."""
        uri = "http://example.org/test"
        
        result1 = uri_to_uuid(uri)
        result2 = uri_to_uuid(uri)
        
        assert result1 == result2

    def test_different_uris(self):
        """Test that different URIs give different UUIDs."""
        uri1 = "http://example.org/a"
        uri2 = "http://example.org/b"
        
        assert uri_to_uuid(uri1) != uri_to_uuid(uri2)


class TestExtractPrefixFromUri:
    """Tests for extract_prefix_from_uri function."""

    def test_rdf_namespace(self):
        """Test RDF namespace prefix extraction."""
        uri = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
        
        assert extract_prefix_from_uri(uri) == "rdf"

    def test_rdfs_namespace(self):
        """Test RDFS namespace prefix extraction."""
        uri = "http://www.w3.org/2000/01/rdf-schema#Class"
        
        assert extract_prefix_from_uri(uri) == "rdfs"

    def test_ontology_uri(self):
        """Test ontology URI (without #) prefix extraction."""
        uri = "http://www.w3.org/2006/vcard/ns"
        
        assert extract_prefix_from_uri(uri) == "vcard"

    def test_unknown_namespace(self):
        """Test unknown namespace returns None."""
        uri = "http://unknown.org/something"
        
        assert extract_prefix_from_uri(uri) is None

    def test_empty_uri(self):
        """Test empty URI returns None."""
        assert extract_prefix_from_uri("") is None
        assert extract_prefix_from_uri(None) is None


class TestExtractLocalnameFromUri:
    """Tests for extract_localname_from_uri function."""

    def test_hash_uri(self):
        """Test extracting localname from hash URI."""
        uri = "http://www.w3.org/2000/01/rdf-schema#Class"
        
        assert extract_localname_from_uri(uri) == "Class"

    def test_slash_uri(self):
        """Test extracting localname from slash URI."""
        uri = "http://xmlns.com/foaf/0.1/Person"
        
        assert extract_localname_from_uri(uri) == "Person"

    def test_trailing_slash(self):
        """Test URI with trailing slash."""
        uri = "http://example.org/something/"
        
        assert extract_localname_from_uri(uri) == "something"


class TestFormatAliasValue:
    """Tests for format_alias_value function."""

    def test_simple_value(self):
        """Test simple value without special chars."""
        assert format_alias_value("simple") == "simple"

    def test_colon_value(self):
        """Test value with colon gets quoted."""
        result = format_alias_value("rdf:type")
        
        assert result.startswith('"')
        assert result.endswith('"')

    def test_bracket_value(self):
        """Test value with bracket gets quoted."""
        assert format_alias_value("[test]").startswith('"')

    def test_exclamation_value(self):
        """Test value with exclamation gets quoted."""
        assert format_alias_value("!rdf").startswith('"')


class TestLiteralToCanonical:
    """Tests for literal_to_canonical function."""

    def test_simple_import(self):
        """Test that rdflib is available for literal tests."""
        try:
            from rdflib import Literal
            lit = Literal("hello")
            result = literal_to_canonical(lit)
            assert result == '"hello"'
        except ImportError:
            pass  # Skip if rdflib not installed

    def test_language_tagged(self):
        """Test language-tagged literal."""
        try:
            from rdflib import Literal
            lit = Literal("hello", lang="en")
            result = literal_to_canonical(lit)
            assert result == '"hello"@en'
        except ImportError:
            pass


class TestCanonicalizeTriple:
    """Tests for canonicalize_triple function."""

    def test_uri_triple(self):
        """Test canonicalizing URI triple."""
        result = canonicalize_triple(
            "http://example.org/s",
            "http://example.org/p",
            "http://example.org/o",
            is_literal=False
        )
        
        assert result == "http://example.org/s|http://example.org/p|http://example.org/o"

    def test_literal_triple(self):
        """Test canonicalizing literal triple."""
        result = canonicalize_triple(
            "http://example.org/s",
            "http://example.org/p",
            '"hello"',
            is_literal=True
        )
        
        assert result == 'http://example.org/s|http://example.org/p|"hello"'


class TestNamespaceMappings:
    """Tests for namespace mappings."""

    def test_all_prefixes_have_uris(self):
        """Test that common prefixes are mapped."""
        expected_prefixes = ['rdf', 'rdfs', 'owl', 'xsd', 'dc', 'dcterms']
        
        for prefix in expected_prefixes:
            assert prefix in NAMESPACE_URI_TO_PREFIX.values()

    def test_ontology_uris_mapped(self):
        """Test ontology URIs without # are mapped."""
        assert 'http://www.w3.org/2006/vcard/ns' in ONTOLOGY_URI_TO_PREFIX
        assert ONTOLOGY_URI_TO_PREFIX['http://www.w3.org/2006/vcard/ns'] == 'vcard'

#!/usr/bin/env python3
"""Tests for import_ontology.py"""

import sys
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from import_ontology import (  # noqa: E402
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
        assert result.count("-") == 4

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
            "http://example.org/s", "http://example.org/p", "http://example.org/o", is_literal=False
        )

        assert result == "http://example.org/s|http://example.org/p|http://example.org/o"

    def test_literal_triple(self):
        """Test canonicalizing literal triple."""
        result = canonicalize_triple("http://example.org/s", "http://example.org/p", '"hello"', is_literal=True)

        assert result == 'http://example.org/s|http://example.org/p|"hello"'


class TestNamespaceMappings:
    """Tests for namespace mappings."""

    def test_all_prefixes_have_uris(self):
        """Test that common prefixes are mapped."""
        expected_prefixes = ["rdf", "rdfs", "owl", "xsd", "dc", "dcterms"]

        for prefix in expected_prefixes:
            assert prefix in NAMESPACE_URI_TO_PREFIX.values()

    def test_ontology_uris_mapped(self):
        """Test ontology URIs without # are mapped."""
        assert "http://www.w3.org/2006/vcard/ns" in ONTOLOGY_URI_TO_PREFIX
        assert ONTOLOGY_URI_TO_PREFIX["http://www.w3.org/2006/vcard/ns"] == "vcard"


# Import additional functions for integration tests
from import_ontology import (  # noqa: E402
    import_ontology,
    detect_format,
    create_namespace_file,
    create_anchor_file,
    create_statement_file,
    create_blank_node_file,
    literal_to_yaml,
    write_file,
    bnode_to_anchor,
    term_to_anchor,
)


class TestDetectFormat:
    """Tests for detect_format function."""

    def test_detect_xml_by_extension(self, tmp_path):
        """Test detecting RDF/XML by extension."""
        rdf_file = tmp_path / "test.rdf"
        rdf_file.write_text("dummy content")
        assert detect_format(rdf_file) == "xml"

    def test_detect_turtle_by_extension(self, tmp_path):
        """Test detecting Turtle by extension."""
        ttl_file = tmp_path / "test.ttl"
        ttl_file.write_text("dummy content")
        assert detect_format(ttl_file) == "turtle"

    def test_detect_ntriples_by_extension(self, tmp_path):
        """Test detecting N-Triples by extension."""
        nt_file = tmp_path / "test.nt"
        nt_file.write_text("dummy content")
        assert detect_format(nt_file) == "nt"

    def test_detect_turtle_by_content(self, tmp_path):
        """Test detecting Turtle by @prefix content."""
        ttl_file = tmp_path / "test.unknown"
        ttl_file.write_text("@prefix ex: <http://example.org/> .\n")
        assert detect_format(ttl_file) == "turtle"

    def test_detect_xml_by_content(self, tmp_path):
        """Test detecting XML by <?xml declaration."""
        xml_file = tmp_path / "test.unknown"
        xml_file.write_text('<?xml version="1.0"?>\n<rdf:RDF>')
        assert detect_format(xml_file) == "xml"


class TestCreateNamespaceFile:
    """Tests for create_namespace_file function."""

    def test_creates_file(self, tmp_path):
        """Test that namespace file is created."""
        ns_uuid = create_namespace_file(tmp_path, "test", "http://example.org/test#")

        # Should return UUID
        assert len(ns_uuid) == 36

        # File should exist
        ns_file = tmp_path / f"{ns_uuid}.md"
        assert ns_file.exists()

    def test_file_content(self, tmp_path):
        """Test namespace file content."""
        ns_uuid = create_namespace_file(tmp_path, "myns", "http://example.org/myns#")
        ns_file = tmp_path / f"{ns_uuid}.md"

        content = ns_file.read_text()
        assert "metadata: namespace" in content
        assert "uri: http://example.org/myns#" in content
        assert "aliases:" in content


class TestCreateAnchorFile:
    """Tests for create_anchor_file function."""

    def test_creates_file(self, tmp_path):
        """Test that anchor file is created."""
        anchor_uuid = uri_to_uuid("http://example.org/Thing")
        create_anchor_file(tmp_path, anchor_uuid, uri="http://example.org/Thing")

        anchor_file = tmp_path / f"{anchor_uuid}.md"
        assert anchor_file.exists()

    def test_file_content(self, tmp_path):
        """Test anchor file content."""
        anchor_uuid = uri_to_uuid("http://www.w3.org/2000/01/rdf-schema#Class")
        create_anchor_file(tmp_path, anchor_uuid, uri="http://www.w3.org/2000/01/rdf-schema#Class")

        anchor_file = tmp_path / f"{anchor_uuid}.md"
        content = anchor_file.read_text()

        assert "metadata: anchor" in content
        assert "uri:" in content
        assert "aliases:" in content

    def test_no_overwrite(self, tmp_path):
        """Test that existing files are not overwritten."""
        anchor_uuid = "test-uuid"
        anchor_file = tmp_path / f"{anchor_uuid}.md"

        # Create file with specific content
        anchor_file.write_text("original content")

        # Try to create again
        create_anchor_file(tmp_path, anchor_uuid, uri="http://example.org/new")

        # Should not be overwritten
        assert anchor_file.read_text() == "original content"


class TestCreateBlankNodeFile:
    """Tests for create_blank_node_file function."""

    def test_creates_file(self, tmp_path):
        """Test that blank node file is created."""
        bn_uuid = create_blank_node_file(tmp_path, "test!abc123", "http://example.org/", "abc123")

        bn_file = tmp_path / f"{bn_uuid}.md"
        assert bn_file.exists()

    def test_skolem_uri(self, tmp_path):
        """Test that blank node uses skolem IRI."""
        bn_uuid = create_blank_node_file(tmp_path, "test!abc123", "http://example.org/", "abc123")

        bn_file = tmp_path / f"{bn_uuid}.md"
        content = bn_file.read_text()

        assert "metadata: blank_node" in content
        assert "uri:" in content
        assert ".well-known/genid" in content


class TestLiteralToYaml:
    """Tests for literal_to_yaml function."""

    def test_simple_literal(self):
        """Test simple literal."""
        from rdflib import Literal

        lit = Literal("hello")
        result = literal_to_yaml(lit)

        assert '\\"hello\\"' in result

    def test_language_tagged_literal(self):
        """Test language-tagged literal."""
        from rdflib import Literal

        lit = Literal("hello", lang="en")
        result = literal_to_yaml(lit)

        assert "@en" in result

    def test_datatyped_literal(self):
        """Test datatyped literal."""
        from rdflib import Literal
        from rdflib.namespace import XSD

        lit = Literal("42", datatype=XSD.integer)
        result = literal_to_yaml(lit)

        assert "^^[[" in result  # Datatype as wikilink

    def test_escape_quotes(self):
        """Test escaping quotes in literal."""
        from rdflib import Literal

        lit = Literal('He said "hello"')
        result = literal_to_yaml(lit)

        assert '\\"' in result  # Escaped quotes

    def test_escape_newlines(self):
        """Test escaping newlines."""
        from rdflib import Literal

        lit = Literal("Line1\nLine2")
        result = literal_to_yaml(lit)

        assert "\\n" in result


class TestWriteFile:
    """Tests for write_file function."""

    def test_normalizes_crlf(self, tmp_path):
        """Test that CRLF is normalized to LF."""
        test_file = tmp_path / "test.md"
        write_file(test_file, "Line1\r\nLine2\r\n")

        content = test_file.read_bytes()
        assert b"\r\n" not in content
        assert b"\n" in content

    def test_normalizes_cr(self, tmp_path):
        """Test that CR alone is normalized to LF."""
        test_file = tmp_path / "test.md"
        write_file(test_file, "Line1\rLine2\r")

        content = test_file.read_bytes()
        assert b"\r" not in content


class TestImportOntologyIntegration:
    """Integration tests for import_ontology function."""

    def test_import_simple_turtle(self, tmp_path):
        """Test importing a simple Turtle file."""
        # Create source Turtle file
        source_file = tmp_path / "source.ttl"
        source_file.write_text("""
@prefix ex: <http://example.org/test#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .

ex:Thing rdf:type rdfs:Class ;
         rdfs:label "Thing"@en .
""")

        output_dir = tmp_path / "output"

        triple_count, anchor_count, file_count = import_ontology(
            source_file,
            output_dir,
            prefix="ex",
            namespace_uri="http://example.org/test#",
        )

        # Should have imported triples
        assert triple_count == 2  # rdf:type and rdfs:label
        assert anchor_count >= 1  # At least ex:Thing
        assert file_count > 0

        # Check files were created
        md_files = list(output_dir.glob("*.md"))
        assert len(md_files) > 0

    def test_import_with_blank_nodes(self, tmp_path):
        """Test importing ontology with blank nodes."""
        source_file = tmp_path / "blank.ttl"
        source_file.write_text("""
@prefix ex: <http://example.org/test#> .

ex:Thing ex:has [
    ex:name "Anonymous"
] .
""")

        output_dir = tmp_path / "output"

        triple_count, anchor_count, file_count = import_ontology(
            source_file,
            output_dir,
            prefix="ex",
            namespace_uri="http://example.org/test#",
        )

        assert triple_count == 2  # ex:Thing ex:has _:b, _:b ex:name "..."
        assert file_count > 0

        # Check for blank node file
        md_files = list(output_dir.glob("*.md"))
        contents = [f.read_text() for f in md_files]
        blank_node_count = sum(1 for c in contents if "metadata: blank_node" in c)
        assert blank_node_count >= 1

    def test_import_creates_namespace_file(self, tmp_path):
        """Test that namespace file is created."""
        source_file = tmp_path / "test.ttl"
        source_file.write_text("""
@prefix ex: <http://example.org/ns#> .
ex:A ex:p ex:B .
""")

        output_dir = tmp_path / "output"
        import_ontology(source_file, output_dir, prefix="ex", namespace_uri="http://example.org/ns#")

        # Find namespace file
        md_files = list(output_dir.glob("*.md"))
        namespace_files = [f for f in md_files if "metadata: namespace" in f.read_text()]

        assert len(namespace_files) == 1

    def test_import_with_datatypes(self, tmp_path):
        """Test importing triples with datatyped literals."""
        source_file = tmp_path / "dtype.ttl"
        source_file.write_text("""
@prefix ex: <http://example.org/test#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:Thing ex:count "42"^^xsd:integer ;
         ex:active "true"^^xsd:boolean .
""")

        output_dir = tmp_path / "output"

        triple_count, _, _ = import_ontology(
            source_file,
            output_dir,
            prefix="ex",
            namespace_uri="http://example.org/test#",
        )

        assert triple_count == 2

        # Check that datatype wikilinks are in the files
        statement_files = [
            f for f in output_dir.glob("*.md") if "metadata: statement" in f.read_text()
        ]

        assert len(statement_files) == 2

        # At least one should have datatype wikilink
        all_content = " ".join(f.read_text() for f in statement_files)
        assert "^^[[" in all_content  # Datatype as wikilink

    def test_uuid_filenames(self, tmp_path):
        """Test that all files have UUID filenames."""
        source_file = tmp_path / "test.ttl"
        source_file.write_text("""
@prefix ex: <http://example.org/test#> .
ex:Thing ex:label "Test" .
""")

        output_dir = tmp_path / "output"
        import_ontology(source_file, output_dir, prefix="ex", namespace_uri="http://example.org/test#")

        # All files should have UUID names
        import re

        uuid_pattern = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\.md$")

        for md_file in output_dir.glob("*.md"):
            assert uuid_pattern.match(md_file.name), f"Invalid filename: {md_file.name}"


class TestBnodeToAnchor:
    """Tests for bnode_to_anchor function."""

    def test_consistent_mapping(self):
        """Test that same BNode maps to same UUID."""
        from rdflib import BNode

        bnode = BNode("abc123")
        bnode_map = {}

        uuid1, local1 = bnode_to_anchor(bnode, "test", bnode_map, "http://example.org/")
        uuid2, local2 = bnode_to_anchor(bnode, "test", bnode_map, "http://example.org/")

        assert uuid1 == uuid2
        assert local1 == local2

    def test_different_bnodes_different_uuids(self):
        """Test that different BNodes map to different UUIDs."""
        from rdflib import BNode

        bnode1 = BNode("a")
        bnode2 = BNode("b")
        bnode_map = {}

        uuid1, _ = bnode_to_anchor(bnode1, "test", bnode_map, "http://example.org/")
        uuid2, _ = bnode_to_anchor(bnode2, "test", bnode_map, "http://example.org/")

        assert uuid1 != uuid2


class TestTermToAnchor:
    """Tests for term_to_anchor function."""

    def test_uriref_to_uuid(self):
        """Test URIRef conversion to UUID."""
        from rdflib import URIRef

        uri = URIRef("http://www.w3.org/1999/02/22-rdf-syntax-ns#type")
        bnode_map = {}

        anchor, is_external = term_to_anchor(uri, "rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#", bnode_map)

        assert anchor == "73b69787-81ea-563e-8e09-9c84cad4cf2b"
        assert not is_external  # rdf:type is local to rdf namespace

    def test_external_uriref(self):
        """Test external URIRef is marked as external."""
        from rdflib import URIRef

        uri = URIRef("http://www.w3.org/2000/01/rdf-schema#Class")
        bnode_map = {}

        anchor, is_external = term_to_anchor(uri, "rdf", "http://www.w3.org/1999/02/22-rdf-syntax-ns#", bnode_map)

        assert len(anchor) == 36  # UUID format
        assert is_external  # rdfs:Class is external to rdf namespace

    def test_bnode_conversion(self):
        """Test BNode conversion."""
        from rdflib import BNode

        bnode = BNode("test")
        bnode_map = {}

        anchor, is_external = term_to_anchor(bnode, "test", "http://example.org/", bnode_map)

        assert len(anchor) == 36  # UUID format
        assert not is_external  # Blank nodes are always local

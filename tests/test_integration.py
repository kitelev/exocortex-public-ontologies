#!/usr/bin/env python3
"""Integration tests for the full import → validate → export cycle."""

import shutil
import sys
import tempfile
from pathlib import Path

import pytest

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from import_ontology import import_ontology  # noqa: E402
from validate import validate_all, ValidationResult  # noqa: E402


class TestImportValidateCycle:
    """Test the full import → validate cycle."""

    @pytest.fixture
    def temp_dir(self):
        """Create a temporary directory for tests."""
        temp = tempfile.mkdtemp()
        yield Path(temp)
        shutil.rmtree(temp)

    @pytest.fixture
    def sample_turtle(self, temp_dir):
        """Create a sample Turtle ontology file."""
        content = """@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix test: <http://example.org/test#> .

test: a owl:Ontology ;
    rdfs:label "Test Ontology" .

test:Person a owl:Class ;
    rdfs:label "Person"@en ;
    rdfs:comment "A human being." .

test:name a owl:DatatypeProperty ;
    rdfs:label "name" ;
    rdfs:domain test:Person ;
    rdfs:range rdfs:Literal .

test:knows a owl:ObjectProperty ;
    rdfs:label "knows" ;
    rdfs:domain test:Person ;
    rdfs:range test:Person .
"""
        file_path = temp_dir / "test.ttl"
        file_path.write_text(content)
        return file_path

    def test_import_creates_files(self, temp_dir, sample_turtle):
        """Test that import creates expected files."""
        output_dir = temp_dir / "output"

        triple_count, anchor_count, file_count = import_ontology(sample_turtle, output_dir, "test", verbose=False)

        assert triple_count > 0
        assert anchor_count > 0
        assert file_count > 0
        assert output_dir.exists()
        assert len(list(output_dir.glob("*.md"))) == file_count

    def test_import_creates_namespace_file(self, temp_dir, sample_turtle):
        """Test that import creates a namespace file."""
        output_dir = temp_dir / "output"

        import_ontology(sample_turtle, output_dir, "test", verbose=False)

        # Find namespace file (has metadata: namespace)
        namespace_files = []
        for md_file in output_dir.glob("*.md"):
            content = md_file.read_text()
            if "metadata: namespace" in content:
                namespace_files.append(md_file)

        assert len(namespace_files) == 1

    def test_import_creates_anchor_files(self, temp_dir, sample_turtle):
        """Test that import creates anchor files for classes and properties."""
        output_dir = temp_dir / "output"

        import_ontology(sample_turtle, output_dir, "test", verbose=False)

        # Count anchor files
        anchor_files = []
        for md_file in output_dir.glob("*.md"):
            content = md_file.read_text()
            if "metadata: anchor" in content:
                anchor_files.append(md_file)

        # Should have anchors for: Person, name, knows
        assert len(anchor_files) >= 3

    def test_import_creates_statement_files(self, temp_dir, sample_turtle):
        """Test that import creates statement files."""
        output_dir = temp_dir / "output"

        import_ontology(sample_turtle, output_dir, "test", verbose=False)

        # Count statement files
        statement_files = []
        for md_file in output_dir.glob("*.md"):
            content = md_file.read_text()
            if "metadata: statement" in content:
                statement_files.append(md_file)

        assert len(statement_files) > 0

    def test_import_all_files_have_aliases(self, temp_dir, sample_turtle):
        """Test that all imported files have aliases."""
        output_dir = temp_dir / "output"

        import_ontology(sample_turtle, output_dir, "test", verbose=False)

        for md_file in output_dir.glob("*.md"):
            content = md_file.read_text()
            assert "aliases:" in content, f"Missing aliases in {md_file.name}"


class TestValidateImportedOntology:
    """Test validation of imported ontologies."""

    @pytest.fixture
    def imported_ontology(self, tmp_path):
        """Create an imported ontology for validation tests."""
        # Create a minimal valid ontology structure
        ontology_dir = tmp_path / "test"
        ontology_dir.mkdir()

        # Create namespace file
        ns_file = ontology_dir / "abc12345-1234-5678-9abc-def012345678.md"
        ns_file.write_text(
            """---
metadata: namespace
uri: "http://example.org/test#"
aliases:
  - "!test"
---
"""
        )

        # Create anchor file
        anchor_file = ontology_dir / "def67890-1234-5678-9abc-def012345678.md"
        anchor_file.write_text(
            """---
metadata: anchor
uri: "http://example.org/test#Person"
aliases:
  - "test:Person"
---
"""
        )

        # Create statement file
        stmt_file = ontology_dir / "fed09876-1234-5678-9abc-def012345678.md"
        stmt_file.write_text(
            """---
metadata: statement
subject: "[[def67890-1234-5678-9abc-def012345678]]"
predicate: "[[73b69787-81ea-563e-8e09-9c84cad4cf2b|a]]"
object: "[[external-class-uuid]]"
aliases:
  - "test:Person a external:Class"
---
"""
        )

        return tmp_path

    def test_validate_structure(self, imported_ontology):
        """Test basic validation of imported structure."""
        # This tests that validate_all runs without crashing
        # Full validation requires all referenced anchors to exist
        result = validate_all(imported_ontology, verbose=False, target_namespaces=["test"])

        assert isinstance(result, ValidationResult)


class TestRealOntologyValidation:
    """Test validation of real ontologies in the repository."""

    def test_validate_rdf_ontology(self):
        """Test validation of RDF ontology."""
        repo_root = Path(__file__).parent.parent
        if not (repo_root / "rdf").exists():
            pytest.skip("RDF ontology not found")

        result = validate_all(repo_root, verbose=False, target_namespaces=["rdf"])

        assert not result.orphaned_anchors, f"Found orphaned anchors: {result.orphaned_anchors}"
        assert not result.invalid_frontmatter, f"Found invalid frontmatter: {result.invalid_frontmatter}"
        assert not result.naming_violations, f"Found naming violations: {result.naming_violations}"

    def test_validate_shacl_ontology(self):
        """Test validation of SHACL ontology."""
        repo_root = Path(__file__).parent.parent
        if not (repo_root / "sh").exists():
            pytest.skip("SHACL ontology not found")

        result = validate_all(repo_root, verbose=False, target_namespaces=["sh"])

        assert not result.orphaned_anchors
        assert not result.invalid_frontmatter
        assert not result.naming_violations

    def test_validate_sosa_ontology(self):
        """Test validation of SOSA ontology."""
        repo_root = Path(__file__).parent.parent
        if not (repo_root / "sosa").exists():
            pytest.skip("SOSA ontology not found")

        result = validate_all(repo_root, verbose=False, target_namespaces=["sosa"])

        assert not result.orphaned_anchors
        assert not result.invalid_frontmatter
        assert not result.naming_violations


class TestFileFormats:
    """Test file format consistency."""

    def test_uuid_filename_format(self):
        """Test that all ontology files use UUID filenames."""
        import re

        repo_root = Path(__file__).parent.parent
        uuid_pattern = re.compile(r"^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}\.md$")

        for namespace_dir in repo_root.iterdir():
            if not namespace_dir.is_dir():
                continue
            if namespace_dir.name.startswith(".") or namespace_dir.name in [
                "scripts",
                "tests",
                "originals",
                "~templates",
                "docs",
            ]:
                continue

            for md_file in namespace_dir.glob("*.md"):
                assert uuid_pattern.match(md_file.name), f"Non-UUID filename: {namespace_dir.name}/{md_file.name}"

    def test_frontmatter_format(self):
        """Test that all files have valid YAML frontmatter."""
        import yaml

        repo_root = Path(__file__).parent.parent

        for namespace_dir in repo_root.iterdir():
            if not namespace_dir.is_dir():
                continue
            if namespace_dir.name.startswith(".") or namespace_dir.name in [
                "scripts",
                "tests",
                "originals",
                "~templates",
                "docs",
            ]:
                continue

            for md_file in list(namespace_dir.glob("*.md"))[:10]:  # Sample 10 files per namespace
                content = md_file.read_text()
                assert content.startswith("---"), f"Missing frontmatter in {md_file}"

                # Extract frontmatter
                end_match = content.find("\n---", 3)
                assert end_match > 0, f"No closing --- in {md_file}"

                yaml_content = content[4:end_match]
                try:
                    data = yaml.safe_load(yaml_content)
                    assert data is not None, f"Empty frontmatter in {md_file}"
                    assert "metadata" in data, f"Missing metadata in {md_file}"
                except yaml.YAMLError as e:
                    pytest.fail(f"Invalid YAML in {md_file}: {e}")

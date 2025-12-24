#!/usr/bin/env python3
"""Tests for validate.py"""

import sys
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from validate import (  # noqa: E402
    parse_frontmatter,
    check_naming_convention,
    extract_wikilinks,
    has_body_content,
    ValidationResult,
)


class TestParseFrontmatter:
    """Tests for parse_frontmatter function."""

    def test_valid_frontmatter(self, tmp_path):
        """Test parsing valid YAML frontmatter."""
        file = tmp_path / "test.md"
        file.write_text("---\nmetadata: anchor\nuri: http://example.org\n---\n")

        data, error = parse_frontmatter(file)

        assert error is None
        assert data == {"metadata": "anchor", "uri": "http://example.org"}

    def test_missing_frontmatter(self, tmp_path):
        """Test file without frontmatter."""
        file = tmp_path / "test.md"
        file.write_text("No frontmatter here")

        data, error = parse_frontmatter(file)

        assert data is None
        assert "No frontmatter found" in error

    def test_invalid_yaml(self, tmp_path):
        """Test invalid YAML in frontmatter."""
        file = tmp_path / "test.md"
        file.write_text("---\nmetadata: [invalid: yaml\n---\n")

        data, error = parse_frontmatter(file)

        assert data is None
        assert "YAML parse error" in error


class TestCheckNamingConvention:
    """Tests for check_naming_convention function."""

    def test_valid_uuid(self, tmp_path):
        """Test valid UUID filename."""
        file = tmp_path / "73b69787-81ea-563e-8e09-9c84cad4cf2b.md"
        file.touch()

        valid, error = check_naming_convention(file, "anchor")

        assert valid is True
        assert error == ""

    def test_invalid_filename(self, tmp_path):
        """Test non-UUID filename."""
        file = tmp_path / "not-a-uuid.md"
        file.touch()

        valid, error = check_naming_convention(file, "anchor")

        assert valid is False
        assert "must be UUID format" in error


class TestExtractWikilinks:
    """Tests for extract_wikilinks function."""

    def test_single_wikilink(self):
        """Test extracting single wikilink."""
        data = {"subject": "[[abc123]]"}

        links = extract_wikilinks(data)

        assert links == {"abc123"}

    def test_wikilink_with_alias(self):
        """Test extracting wikilink with alias."""
        data = {"predicate": "[[73b69787-81ea-563e-8e09-9c84cad4cf2b|rdf:type]]"}

        links = extract_wikilinks(data)

        assert links == {"73b69787-81ea-563e-8e09-9c84cad4cf2b"}

    def test_multiple_wikilinks(self):
        """Test extracting multiple wikilinks."""
        data = {"subject": "[[aaa]]", "predicate": "[[bbb]]", "object": "[[ccc]]"}

        links = extract_wikilinks(data)

        assert links == {"aaa", "bbb", "ccc"}

    def test_no_wikilinks(self):
        """Test data without wikilinks."""
        data = {"metadata": "anchor", "uri": "http://example.org"}

        links = extract_wikilinks(data)

        assert links == set()


class TestHasBodyContent:
    """Tests for has_body_content function."""

    def test_no_body(self, tmp_path):
        """Test file with only frontmatter."""
        file = tmp_path / "test.md"
        file.write_text("---\nmetadata: anchor\n---\n")

        assert has_body_content(file) is False

    def test_with_body(self, tmp_path):
        """Test file with body content."""
        file = tmp_path / "test.md"
        file.write_text("---\nmetadata: anchor\n---\n\nSome body content")

        assert has_body_content(file) is True

    def test_whitespace_only_body(self, tmp_path):
        """Test file with only whitespace after frontmatter."""
        file = tmp_path / "test.md"
        file.write_text("---\nmetadata: anchor\n---\n\n   \n")

        assert has_body_content(file) is False


class TestValidationResult:
    """Tests for ValidationResult dataclass."""

    def test_no_errors(self):
        """Test has_errors returns False when no errors."""
        result = ValidationResult()

        assert result.has_errors() is False

    def test_has_orphaned_anchors(self):
        """Test has_errors returns True with orphaned anchors."""
        result = ValidationResult()
        result.orphaned_anchors = ["test"]

        assert result.has_errors() is True

    def test_has_missing_aliases(self):
        """Test has_errors returns True with missing aliases."""
        result = ValidationResult()
        result.missing_aliases = ["file.md"]

        assert result.has_errors() is True

    def test_external_wikilinks_not_error(self):
        """Test external wikilinks don't count as errors."""
        result = ValidationResult()
        result.external_wikilinks = [("file.md", "link")]

        assert result.has_errors() is False

    def test_summary(self):
        """Test summary generation."""
        result = ValidationResult()
        result.orphaned_anchors = ["a", "b"]
        result.missing_aliases = ["c"]

        summary = result.summary()

        assert "Orphaned anchors: 2" in summary
        assert "Missing aliases: 1" in summary

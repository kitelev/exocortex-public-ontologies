#!/usr/bin/env python3
"""Tests for semantic_lint.py"""

import sys
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from semantic_lint import (  # noqa: E402
    parse_frontmatter_fast,
    extract_wikilink_uuid,
    LintIssue,
    lint_namespace,
    progress_bar,
    calculate_grade,
    generate_report,
    RDF_TYPE_UUID,
    RDFS_LABEL_UUID,
    RDFS_COMMENT_UUID,
    RDFS_CLASS_UUID,
    OWL_CLASS_UUID,
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
        """Test parsing incomplete frontmatter."""
        file = tmp_path / "test.md"
        file.write_text(
            """---
metadata: anchor
no closing delimiter
"""
        )
        data = parse_frontmatter_fast(file)
        # Parser returns partial data or None for incomplete frontmatter
        assert data is None or data.get("metadata") == "anchor"

    def test_empty_frontmatter(self, tmp_path):
        """Test parsing empty frontmatter."""
        file = tmp_path / "test.md"
        file.write_text(
            """---
---
"""
        )
        data = parse_frontmatter_fast(file)
        assert data == {} or data is None


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

    def test_wikilink_with_spaces(self):
        """Test wikilink with leading/trailing spaces."""
        result = extract_wikilink_uuid("  [[uuid-789]]  ")
        assert result == "uuid-789"


class TestLintIssue:
    """Tests for LintIssue class."""

    def test_create_warning(self):
        """Test creating a warning issue."""
        issue = LintIssue("warning", "missing-label", "foaf:Person", "Class missing rdfs:label")
        assert issue.severity == "warning"
        assert issue.category == "missing-label"
        assert issue.resource == "foaf:Person"
        assert issue.message == "Class missing rdfs:label"

    def test_create_info(self):
        """Test creating an info issue."""
        issue = LintIssue("info", "missing-comment", "foaf:Agent", "Missing comment")
        assert issue.severity == "info"
        assert issue.category == "missing-comment"

    def test_create_error(self):
        """Test creating an error issue."""
        issue = LintIssue("error", "invalid-uri", "bad:Thing", "Invalid URI format")
        assert issue.severity == "error"


class TestProgressBar:
    """Tests for progress_bar."""

    def test_zero_percent(self):
        """Test 0% progress bar."""
        result = progress_bar(0, width=10)
        assert result == "░░░░░░░░░░"

    def test_hundred_percent(self):
        """Test 100% progress bar."""
        result = progress_bar(100, width=10)
        assert result == "██████████"

    def test_fifty_percent(self):
        """Test 50% progress bar."""
        result = progress_bar(50, width=10)
        assert result == "█████░░░░░"

    def test_custom_width(self):
        """Test custom width progress bar."""
        result = progress_bar(50, width=20)
        assert len(result) == 20
        assert result.count("█") == 10
        assert result.count("░") == 10

    def test_partial_percent(self):
        """Test non-round percentage."""
        result = progress_bar(33, width=10)
        assert len(result) == 10
        assert result.count("█") == 3


class TestCalculateGrade:
    """Tests for calculate_grade."""

    def test_grade_a(self):
        """Test grade A conditions."""
        grade, icon = calculate_grade(95, 85)
        assert grade == "A"
        assert icon == "🟢"

    def test_grade_b(self):
        """Test grade B conditions."""
        grade, icon = calculate_grade(85, 65)
        assert grade == "B"
        assert icon == "🟡"

    def test_grade_c(self):
        """Test grade C conditions."""
        grade, icon = calculate_grade(70, 30)
        assert grade == "C"
        assert icon == "🟠"

    def test_grade_d(self):
        """Test grade D conditions."""
        grade, icon = calculate_grade(50, 30)
        assert grade == "D"
        assert icon == "🔴"

    def test_boundary_grade_a(self):
        """Test boundary condition for grade A."""
        grade, icon = calculate_grade(90, 80)
        assert grade == "A"

    def test_boundary_grade_b(self):
        """Test boundary condition for grade B."""
        grade, icon = calculate_grade(80, 60)
        assert grade == "B"

    def test_boundary_grade_c(self):
        """Test boundary condition for grade C."""
        grade, icon = calculate_grade(60, 0)
        assert grade == "C"


class TestLintNamespace:
    """Tests for lint_namespace."""

    def test_nonexistent_namespace(self, tmp_path):
        """Test linting nonexistent namespace."""
        stats, issues = lint_namespace(tmp_path, "nonexistent")
        assert stats == {}
        assert issues == []

    def test_empty_namespace(self, tmp_path):
        """Test linting empty namespace directory."""
        ns_dir = tmp_path / "empty"
        ns_dir.mkdir()

        stats, issues = lint_namespace(tmp_path, "empty")
        assert stats["classes"] == 0
        assert stats["properties"] == 0

    def test_namespace_with_class(self, tmp_path):
        """Test linting namespace with a class."""
        ns_dir = tmp_path / "test"
        ns_dir.mkdir()

        # Create anchor for class
        anchor_uuid = "class-anchor-uuid"
        anchor = ns_dir / f"{anchor_uuid}.md"
        anchor.write_text(
            """---
metadata: anchor
aliases:
  - "test:MyClass"
---
"""
        )

        # Create type statement (class is rdf:type owl:Class)
        type_stmt = ns_dir / "type-stmt-uuid.md"
        type_stmt.write_text(
            f"""---
metadata: statement
subject: "[[{anchor_uuid}]]"
predicate: "[[{RDF_TYPE_UUID}]]"
object: "[[{OWL_CLASS_UUID}]]"
---
"""
        )

        stats, issues = lint_namespace(tmp_path, "test")
        assert stats["classes"] == 1
        # Class without label/comment generates warnings
        assert len([i for i in issues if i.severity == "warning"]) >= 1

    def test_class_with_label(self, tmp_path):
        """Test class with label doesn't generate warning."""
        ns_dir = tmp_path / "test"
        ns_dir.mkdir()

        anchor_uuid = "class-uuid"
        anchor = ns_dir / f"{anchor_uuid}.md"
        anchor.write_text(
            """---
metadata: anchor
aliases:
  - "test:MyClass"
---
"""
        )

        # Type statement
        type_stmt = ns_dir / "type-stmt.md"
        # Use explicit UUIDs to ensure f-string works correctly
        rdf_type = "73b69787-81ea-563e-8e09-9c84cad4cf2b"
        owl_class = "581d50c0-7bc2-5a97-bdc2-9c056f43c807"
        rdfs_label = "d0e9e696-d3f2-5966-a62f-d8358cbde741"

        type_stmt.write_text(
            f"""---
metadata: statement
subject: "[[{anchor_uuid}]]"
predicate: "[[{rdf_type}]]"
object: "[[{owl_class}]]"
---
"""
        )

        # Label statement - use single quotes for YAML to allow double quotes in value
        label_stmt = ns_dir / "label-stmt.md"
        label_stmt.write_text(
            f"""---
metadata: statement
subject: "[[{anchor_uuid}]]"
predicate: "[[{rdfs_label}]]"
object: '"MyClass"@en'
---
"""
        )

        stats, issues = lint_namespace(tmp_path, "test")
        # No warning for missing label (class has label)
        label_warnings = [i for i in issues if i.category == "missing-label" and "Class" in i.message]
        assert (
            len(label_warnings) == 0
        ), f"Expected no label warnings, got: {[(i.resource, i.message) for i in label_warnings]}, stats={stats}"


class TestGenerateReport:
    """Tests for generate_report."""

    def test_empty_stats(self):
        """Test generating report with empty stats."""
        report = generate_report({}, {})
        assert "# Semantic Lint Report" in report
        assert "## Summary" in report

    def test_namespace_filter_in_title(self):
        """Test namespace filter appears in title."""
        report = generate_report({}, {}, namespace_filter="foaf")
        assert "# Semantic Lint Report: foaf" in report

    def test_summary_section(self):
        """Test summary section with stats."""
        stats = {
            "test": {
                "classes": 10,
                "properties": 20,
                "classes_with_label": 8,
                "classes_with_comment": 7,
                "properties_with_label": 18,
                "properties_with_comment": 15,
                "properties_with_domain": 12,
                "properties_with_range": 14,
            }
        }
        report = generate_report(stats, {"test": []})
        assert "Total Classes | 10" in report
        assert "Total Properties | 20" in report

    def test_grade_distribution(self):
        """Test grade distribution section."""
        stats = {
            "ns1": {
                "classes": 10,
                "properties": 10,
                "classes_with_label": 10,
                "classes_with_comment": 10,
                "properties_with_label": 10,
                "properties_with_comment": 10,
                "properties_with_domain": 10,
                "properties_with_range": 10,
            }
        }
        report = generate_report(stats, {"ns1": []})
        assert "Grade Distribution" in report
        assert "Excellent" in report or "A" in report

    def test_issue_counts(self):
        """Test issue counts section."""
        issues = {
            "test": [
                LintIssue("warning", "missing-label", "test:X", "Missing label"),
                LintIssue("warning", "missing-label", "test:Y", "Missing label"),
                LintIssue("info", "missing-comment", "test:Z", "Missing comment"),
            ]
        }
        stats = {
            "test": {
                "classes": 3,
                "properties": 0,
                "classes_with_label": 1,
                "classes_with_comment": 2,
                "properties_with_label": 0,
                "properties_with_comment": 0,
                "properties_with_domain": 0,
                "properties_with_range": 0,
            }
        }
        report = generate_report(stats, issues)
        assert "Issue Counts" in report
        assert "missing-label" in report

    def test_warnings_section(self):
        """Test warnings by namespace section."""
        issues = {
            "foaf": [
                LintIssue("warning", "missing-label", "foaf:Agent", "Missing label"),
            ]
        }
        stats = {
            "foaf": {
                "classes": 1,
                "properties": 0,
                "classes_with_label": 0,
                "classes_with_comment": 0,
                "properties_with_label": 0,
                "properties_with_comment": 0,
                "properties_with_domain": 0,
                "properties_with_range": 0,
            }
        }
        report = generate_report(stats, issues)
        assert "Warnings by Namespace" in report
        assert "foaf" in report
        assert "foaf:Agent" in report

    def test_quality_grade_overall(self):
        """Test overall quality grade section."""
        stats = {
            "test": {
                "classes": 10,
                "properties": 10,
                "classes_with_label": 10,
                "classes_with_comment": 10,
                "properties_with_label": 10,
                "properties_with_comment": 10,
                "properties_with_domain": 10,
                "properties_with_range": 10,
            }
        }
        report = generate_report(stats, {"test": []})
        assert "Quality Grade" in report
        assert "Overall Grade" in report


class TestWellKnownUuids:
    """Tests for well-known UUID constants."""

    def test_rdf_type_uuid(self):
        """Test RDF_TYPE_UUID is correct."""
        assert RDF_TYPE_UUID == "73b69787-81ea-563e-8e09-9c84cad4cf2b"

    def test_rdfs_label_uuid(self):
        """Test RDFS_LABEL_UUID is correct."""
        assert RDFS_LABEL_UUID == "d0e9e696-d3f2-5966-a62f-d8358cbde741"

    def test_rdfs_comment_uuid(self):
        """Test RDFS_COMMENT_UUID is correct."""
        assert RDFS_COMMENT_UUID == "da1b0b28-9c51-55c3-a963-2337006693de"

    def test_rdfs_class_uuid(self):
        """Test RDFS_CLASS_UUID is correct."""
        assert RDFS_CLASS_UUID == "30488677-f427-5947-8a14-02903ca20a7e"

    def test_owl_class_uuid(self):
        """Test OWL_CLASS_UUID is correct."""
        assert OWL_CLASS_UUID == "581d50c0-7bc2-5a97-bdc2-9c056f43c807"

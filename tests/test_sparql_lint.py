#!/usr/bin/env python3
"""Tests for sparql_lint.py"""

import sys
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from sparql_lint import (  # noqa: E402
    SPARQLLinter,
    LintIssue,
    Severity,
    lint_query,
    format_results,
    load_prefixes,
)


class TestSeverity:
    """Tests for Severity enum."""

    def test_error_value(self):
        """Test ERROR severity value."""
        assert Severity.ERROR.value == "error"

    def test_warning_value(self):
        """Test WARNING severity value."""
        assert Severity.WARNING.value == "warning"

    def test_info_value(self):
        """Test INFO severity value."""
        assert Severity.INFO.value == "info"


class TestLintIssue:
    """Tests for LintIssue dataclass."""

    def test_create_issue(self):
        """Test creating a lint issue."""
        issue = LintIssue(severity=Severity.ERROR, line=1, column=5, message="Test message", rule="test-rule")
        assert issue.severity == Severity.ERROR
        assert issue.line == 1
        assert issue.column == 5
        assert issue.message == "Test message"
        assert issue.rule == "test-rule"

    def test_str_error(self):
        """Test string representation of error."""
        issue = LintIssue(Severity.ERROR, 1, 5, "Error message", "test-rule")
        result = str(issue)
        assert "❌" in result
        assert "Line 1:5" in result
        assert "test-rule" in result
        assert "Error message" in result

    def test_str_warning(self):
        """Test string representation of warning."""
        issue = LintIssue(Severity.WARNING, 2, 10, "Warning message", "warn-rule")
        result = str(issue)
        assert "⚠️" in result
        assert "Line 2:10" in result

    def test_str_info(self):
        """Test string representation of info."""
        issue = LintIssue(Severity.INFO, 3, 1, "Info message", "info-rule")
        result = str(issue)
        assert "ℹ️" in result
        assert "Line 3:1" in result


class TestLoadPrefixes:
    """Tests for load_prefixes function."""

    def test_loads_prefixes(self):
        """Test that prefixes are loaded from _prefixes.yaml."""
        prefixes = load_prefixes()
        assert isinstance(prefixes, dict)
        assert "rdf" in prefixes
        assert "rdfs" in prefixes
        assert "owl" in prefixes

    def test_no_ontology_prefixes(self):
        """Test that -ontology prefixes are filtered out."""
        prefixes = load_prefixes()
        for key in prefixes:
            assert not key.endswith("-ontology")


class TestSPARQLLinterSyntax:
    """Tests for SPARQL syntax checking."""

    def test_empty_query(self):
        """Test empty query detection."""
        issues = lint_query("")
        assert len(issues) == 1
        assert issues[0].rule == "empty-query"
        assert issues[0].severity == Severity.ERROR

    def test_whitespace_only_query(self):
        """Test whitespace-only query detection."""
        issues = lint_query("   \n\t  ")
        assert len(issues) == 1
        assert issues[0].rule == "empty-query"

    def test_unclosed_braces(self):
        """Test unclosed braces detection."""
        issues = lint_query("SELECT ?s WHERE { ?s ?p ?o")
        error_issues = [i for i in issues if i.rule == "unclosed-braces"]
        assert len(error_issues) == 1
        assert error_issues[0].severity == Severity.ERROR

    def test_extra_braces(self):
        """Test extra closing braces detection."""
        issues = lint_query("SELECT ?s WHERE { ?s ?p ?o } }")
        error_issues = [i for i in issues if i.rule == "extra-braces"]
        assert len(error_issues) == 1

    def test_missing_query_type(self):
        """Test missing query type detection."""
        issues = lint_query("{ ?s ?p ?o }")
        error_issues = [i for i in issues if i.rule == "missing-query-type"]
        assert len(error_issues) == 1

    def test_valid_query_types(self):
        """Test valid query types are accepted."""
        for query_type in ["SELECT", "CONSTRUCT", "ASK", "DESCRIBE"]:
            query = f"{query_type} * WHERE {{ ?s ?p ?o }}"
            issues = lint_query(query)
            query_type_errors = [i for i in issues if i.rule == "missing-query-type"]
            assert len(query_type_errors) == 0


class TestSPARQLLinterPrefixes:
    """Tests for prefix checking."""

    def test_known_prefix(self):
        """Test known prefixes don't generate errors."""
        query = "SELECT ?s WHERE { ?s rdf:type owl:Class } LIMIT 10"
        issues = lint_query(query)
        prefix_errors = [i for i in issues if i.rule == "unknown-prefix"]
        assert len(prefix_errors) == 0

    def test_unknown_prefix(self):
        """Test unknown prefixes generate errors."""
        query = "SELECT ?s WHERE { ?s unknown:property ?o } LIMIT 10"
        issues = lint_query(query)
        prefix_errors = [i for i in issues if i.rule == "unknown-prefix"]
        assert len(prefix_errors) == 1
        assert "unknown" in prefix_errors[0].message

    def test_declared_prefix(self):
        """Test declared prefixes are recognized."""
        query = """PREFIX custom: <http://example.org/>
SELECT ?s WHERE { ?s custom:property ?o } LIMIT 10"""
        issues = lint_query(query)
        prefix_errors = [i for i in issues if i.rule == "unknown-prefix"]
        assert len(prefix_errors) == 0

    def test_multiple_unknown_prefixes(self):
        """Test multiple unknown prefixes are detected."""
        query = "SELECT ?s WHERE { ?s foo:a ?o . ?o bar:b ?x } LIMIT 10"
        issues = lint_query(query)
        prefix_errors = [i for i in issues if i.rule == "unknown-prefix"]
        assert len(prefix_errors) == 2


class TestSPARQLLinterSelectStar:
    """Tests for SELECT * checking."""

    def test_select_star_warning(self):
        """Test SELECT * generates info message."""
        query = "SELECT * WHERE { ?s ?p ?o } LIMIT 10"
        issues = lint_query(query)
        star_issues = [i for i in issues if i.rule == "select-star"]
        assert len(star_issues) == 1
        assert star_issues[0].severity == Severity.INFO

    def test_explicit_variables_no_warning(self):
        """Test explicit variables don't generate warning."""
        query = "SELECT ?s ?p ?o WHERE { ?s ?p ?o } LIMIT 10"
        issues = lint_query(query)
        star_issues = [i for i in issues if i.rule == "select-star"]
        assert len(star_issues) == 0


class TestSPARQLLinterLimit:
    """Tests for LIMIT checking."""

    def test_missing_limit_warning(self):
        """Test missing LIMIT generates warning."""
        query = "SELECT ?s WHERE { ?s ?p ?o }"
        issues = lint_query(query)
        limit_issues = [i for i in issues if i.rule == "missing-limit"]
        assert len(limit_issues) == 1
        assert limit_issues[0].severity == Severity.WARNING

    def test_with_limit_no_warning(self):
        """Test query with LIMIT doesn't generate warning."""
        query = "SELECT ?s WHERE { ?s ?p ?o } LIMIT 100"
        issues = lint_query(query)
        limit_issues = [i for i in issues if i.rule == "missing-limit"]
        assert len(limit_issues) == 0

    def test_aggregation_no_limit_warning(self):
        """Test aggregation queries don't need LIMIT."""
        query = "SELECT (COUNT(?s) AS ?count) WHERE { ?s ?p ?o }"
        issues = lint_query(query)
        limit_issues = [i for i in issues if i.rule == "missing-limit"]
        assert len(limit_issues) == 0


class TestSPARQLLinterFilters:
    """Tests for FILTER checking."""

    def test_filter_not_exists_info(self):
        """Test FILTER NOT EXISTS generates info."""
        query = "SELECT ?s WHERE { ?s ?p ?o . FILTER NOT EXISTS { ?s rdf:type ?t } } LIMIT 10"
        issues = lint_query(query)
        filter_issues = [i for i in issues if i.rule == "filter-not-exists"]
        assert len(filter_issues) == 1
        assert filter_issues[0].severity == Severity.INFO


class TestFormatResults:
    """Tests for format_results function."""

    def test_no_issues(self):
        """Test formatting with no issues."""
        result = format_results([], "SELECT ?s WHERE { ?s ?p ?o }")
        assert "No issues found" in result
        assert "✅" in result

    def test_with_issues(self):
        """Test formatting with issues."""
        issues = [
            LintIssue(Severity.ERROR, 1, 1, "Error", "rule1"),
            LintIssue(Severity.WARNING, 2, 1, "Warning", "rule2"),
        ]
        result = format_results(issues, "SELECT ?s")
        assert "2 issue(s)" in result
        assert "1 errors" in result
        assert "1 warnings" in result


class TestSPARQLLinterIntegration:
    """Integration tests for SPARQLLinter."""

    def test_good_query(self):
        """Test a well-formed query has minimal issues."""
        query = """
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
SELECT ?name ?email
WHERE {
    ?person foaf:name ?name .
    ?person foaf:mbox ?email .
}
LIMIT 100
"""
        issues = lint_query(query)
        # Should have no errors
        errors = [i for i in issues if i.severity == Severity.ERROR]
        assert len(errors) == 0

    def test_problematic_query(self):
        """Test a query with multiple issues."""
        query = "SELECT * WHERE { ?s unknown:prop ?o"
        issues = lint_query(query)
        assert len(issues) >= 2  # At least unclosed braces and unknown prefix

    def test_multiline_query(self):
        """Test multiline query parsing."""
        query = """
SELECT ?s ?p ?o
WHERE {
    ?s ?p ?o .
    FILTER(?p = rdf:type)
}
LIMIT 10
"""
        issues = lint_query(query)
        # Should parse correctly without syntax errors
        syntax_errors = [i for i in issues if i.rule in ("unclosed-braces", "extra-braces")]
        assert len(syntax_errors) == 0

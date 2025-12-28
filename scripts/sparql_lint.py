#!/usr/bin/env python3
"""
SPARQL query linter for the Exocortex ontologies.

Checks SPARQL queries for:
- Syntax errors
- Unknown prefixes
- SELECT * usage (prefer explicit variables)
- Missing LIMIT on potentially expensive queries
- Unused variables
- Inefficient patterns

Usage:
    python scripts/sparql_lint.py <query_file_or_string>
    python scripts/sparql_lint.py --file queries.txt
    echo "SELECT * WHERE { ?s ?p ?o }" | python scripts/sparql_lint.py -
"""

import argparse
import re
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Optional, Set

import yaml

# Load prefixes from _prefixes.yaml
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
PREFIXES_FILE = REPO_ROOT / "_prefixes.yaml"


def load_prefixes() -> dict:
    """Load prefix definitions from _prefixes.yaml."""
    if PREFIXES_FILE.exists():
        with open(PREFIXES_FILE, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f) or {}
            # Filter out ontology URIs (those with -ontology suffix)
            return {k: v for k, v in data.items() if not k.endswith("-ontology")}
    return {}


KNOWN_PREFIXES = load_prefixes()

# Built-in SPARQL functions
SPARQL_FUNCTIONS = {
    "str", "lang", "langmatches", "datatype", "bound", "iri", "uri", "bnode",
    "rand", "abs", "ceil", "floor", "round", "concat", "strlen", "ucase", "lcase",
    "encode_for_uri", "contains", "strstarts", "strends", "strbefore", "strafter",
    "year", "month", "day", "hours", "minutes", "seconds", "timezone", "tz",
    "now", "uuid", "struuid", "md5", "sha1", "sha256", "sha384", "sha512",
    "coalesce", "if", "sameTerm", "isIRI", "isURI", "isBlank", "isLiteral",
    "isNumeric", "regex", "replace", "exists", "not exists", "count", "sum",
    "min", "max", "avg", "sample", "group_concat"
}


class Severity(Enum):
    """Issue severity levels."""
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"


@dataclass
class LintIssue:
    """Represents a lint issue in a SPARQL query."""
    severity: Severity
    line: int
    column: int
    message: str
    rule: str

    def __str__(self) -> str:
        icon = {"error": "❌", "warning": "⚠️", "info": "ℹ️"}[self.severity.value]
        return f"{icon} Line {self.line}:{self.column} [{self.rule}] {self.message}"


class SPARQLLinter:
    """SPARQL query linter."""

    def __init__(self, known_prefixes: Optional[dict] = None):
        self.known_prefixes = known_prefixes or KNOWN_PREFIXES
        self.issues: List[LintIssue] = []

    def lint(self, query: str) -> List[LintIssue]:
        """Lint a SPARQL query and return issues."""
        self.issues = []

        if not query.strip():
            self.issues.append(LintIssue(
                severity=Severity.ERROR,
                line=1,
                column=1,
                message="Empty query",
                rule="empty-query"
            ))
            return self.issues

        # Run all checks
        self._check_syntax(query)
        self._check_prefixes(query)
        self._check_select_star(query)
        self._check_limit(query)
        self._check_variables(query)
        self._check_filters(query)
        self._check_optional_patterns(query)

        return self.issues

    def _check_syntax(self, query: str) -> None:
        """Check basic SPARQL syntax."""
        lines = query.split("\n")

        # Check for unclosed braces
        open_braces = 0
        for i, line in enumerate(lines, 1):
            # Ignore braces in strings
            line_no_strings = re.sub(r'"[^"]*"', '', line)
            line_no_strings = re.sub(r"'[^']*'", '', line_no_strings)
            open_braces += line_no_strings.count("{") - line_no_strings.count("}")

        if open_braces > 0:
            self.issues.append(LintIssue(
                severity=Severity.ERROR,
                line=len(lines),
                column=1,
                message=f"Unclosed braces: {open_braces} opening brace(s) without closing",
                rule="unclosed-braces"
            ))
        elif open_braces < 0:
            self.issues.append(LintIssue(
                severity=Severity.ERROR,
                line=len(lines),
                column=1,
                message=f"Extra closing braces: {-open_braces} extra closing brace(s)",
                rule="extra-braces"
            ))

        # Check for query type keyword
        query_upper = query.upper()
        has_query_type = any(kw in query_upper for kw in [
            "SELECT", "CONSTRUCT", "ASK", "DESCRIBE", "INSERT", "DELETE"
        ])
        if not has_query_type:
            self.issues.append(LintIssue(
                severity=Severity.ERROR,
                line=1,
                column=1,
                message="Query must start with SELECT, CONSTRUCT, ASK, DESCRIBE, INSERT, or DELETE",
                rule="missing-query-type"
            ))

        # Check WHERE clause for SELECT/CONSTRUCT/DESCRIBE
        if "SELECT" in query_upper or "CONSTRUCT" in query_upper or "DESCRIBE" in query_upper:
            if "WHERE" not in query_upper and "{" in query:
                # Some queries use implicit WHERE
                pass
            elif "WHERE" not in query_upper and "{" not in query:
                self.issues.append(LintIssue(
                    severity=Severity.ERROR,
                    line=1,
                    column=1,
                    message="SELECT/CONSTRUCT/DESCRIBE queries require a WHERE clause or pattern",
                    rule="missing-where"
                ))

    def _check_prefixes(self, query: str) -> None:
        """Check for undefined prefixes."""
        lines = query.split("\n")

        # Extract declared prefixes
        declared_prefixes: Set[str] = set()
        prefix_pattern = re.compile(r"PREFIX\s+(\w+):", re.IGNORECASE)

        for line in lines:
            for match in prefix_pattern.finditer(line):
                declared_prefixes.add(match.group(1).lower())

        # Add well-known prefixes
        all_known = declared_prefixes | set(self.known_prefixes.keys())

        # Find used prefixes in query body
        used_prefix_pattern = re.compile(r"(?<![:\w])(\w+):[A-Za-z_]")

        for i, line in enumerate(lines, 1):
            # Skip PREFIX declarations
            if line.strip().upper().startswith("PREFIX"):
                continue

            for match in used_prefix_pattern.finditer(line):
                prefix = match.group(1).lower()
                if prefix not in all_known:
                    self.issues.append(LintIssue(
                        severity=Severity.ERROR,
                        line=i,
                        column=match.start() + 1,
                        message=f"Unknown prefix '{prefix}:'",
                        rule="unknown-prefix"
                    ))

    def _check_select_star(self, query: str) -> None:
        """Check for SELECT * usage."""
        lines = query.split("\n")

        select_star_pattern = re.compile(r"SELECT\s+\*", re.IGNORECASE)

        for i, line in enumerate(lines, 1):
            match = select_star_pattern.search(line)
            if match:
                self.issues.append(LintIssue(
                    severity=Severity.INFO,
                    line=i,
                    column=match.start() + 1,
                    message="Consider using explicit variables instead of SELECT *",
                    rule="select-star"
                ))

    def _check_limit(self, query: str) -> None:
        """Check for missing LIMIT on potentially expensive queries."""
        query_upper = query.upper()

        # Only check SELECT queries
        if "SELECT" not in query_upper:
            return

        # Check if LIMIT is present
        if "LIMIT" in query_upper:
            return

        # Check if this is a subquery (inside braces after SELECT)
        # Skip this check for aggregation queries
        if any(func in query_upper for func in ["COUNT(", "SUM(", "AVG(", "MIN(", "MAX("]):
            return

        # Warn about missing LIMIT
        lines = query.split("\n")
        self.issues.append(LintIssue(
            severity=Severity.WARNING,
            line=len(lines),
            column=1,
            message="Consider adding LIMIT to prevent expensive full-table scans",
            rule="missing-limit"
        ))

    def _check_variables(self, query: str) -> None:
        """Check for variable usage issues."""
        lines = query.split("\n")

        # Find all variable references
        var_pattern = re.compile(r"\?(\w+)")
        all_vars: Set[str] = set()

        for line in lines:
            for match in var_pattern.finditer(line):
                all_vars.add(match.group(1))

        # Find SELECT variables
        select_match = re.search(r"SELECT\s+((?:\??\w+\s*)+)\s+(?:WHERE|FROM|\{)", query, re.IGNORECASE)
        if select_match and "*" not in select_match.group(1):
            select_vars_str = select_match.group(1)
            select_vars = set(re.findall(r"\?(\w+)", select_vars_str))

            # Find variables used in WHERE clause
            where_match = re.search(r"WHERE\s*\{(.+)\}", query, re.IGNORECASE | re.DOTALL)
            if where_match:
                where_vars = set(re.findall(r"\?(\w+)", where_match.group(1)))

                # Check for unused SELECT variables
                for var in select_vars:
                    if var not in where_vars:
                        # Find line with this variable
                        for i, line in enumerate(lines, 1):
                            if f"?{var}" in line and "SELECT" in line.upper():
                                self.issues.append(LintIssue(
                                    severity=Severity.WARNING,
                                    line=i,
                                    column=line.find(f"?{var}") + 1,
                                    message=f"Variable ?{var} in SELECT is not bound in WHERE clause",
                                    rule="unbound-variable"
                                ))
                                break

    def _check_filters(self, query: str) -> None:
        """Check for potentially inefficient FILTER patterns."""
        lines = query.split("\n")

        # Check for complex REGEX without flags
        regex_pattern = re.compile(r"FILTER\s*\(\s*REGEX\s*\([^)]+\)\s*\)", re.IGNORECASE)

        for i, line in enumerate(lines, 1):
            match = regex_pattern.search(line)
            if match:
                # Check if 'i' flag is used
                if "'i'" not in line.lower() and '"i"' not in line.lower():
                    self.issues.append(LintIssue(
                        severity=Severity.INFO,
                        line=i,
                        column=match.start() + 1,
                        message="REGEX without case-insensitive flag may miss matches",
                        rule="regex-no-flag"
                    ))

        # Check for FILTER NOT EXISTS pattern (with or without parentheses)
        not_exists_pattern = re.compile(r"FILTER\s*(?:\(\s*)?NOT\s+EXISTS", re.IGNORECASE)

        for i, line in enumerate(lines, 1):
            match = not_exists_pattern.search(line)
            if match:
                self.issues.append(LintIssue(
                    severity=Severity.INFO,
                    line=i,
                    column=match.start() + 1,
                    message="FILTER NOT EXISTS can be expensive; consider MINUS if applicable",
                    rule="filter-not-exists"
                ))

    def _check_optional_patterns(self, query: str) -> None:
        """Check for nested OPTIONAL patterns."""
        lines = query.split("\n")

        # Count OPTIONAL nesting
        optional_depth = 0
        max_depth = 0

        for i, line in enumerate(lines, 1):
            optional_count = line.upper().count("OPTIONAL")
            optional_depth += optional_count

            closing_braces = line.count("}")
            optional_depth = max(0, optional_depth - closing_braces)

            if optional_depth > max_depth:
                max_depth = optional_depth

            if optional_depth > 2:
                self.issues.append(LintIssue(
                    severity=Severity.WARNING,
                    line=i,
                    column=1,
                    message=f"Deeply nested OPTIONAL (depth {optional_depth}) can be slow",
                    rule="nested-optional"
                ))


def lint_query(query: str, known_prefixes: Optional[dict] = None) -> List[LintIssue]:
    """Lint a SPARQL query and return issues."""
    linter = SPARQLLinter(known_prefixes)
    return linter.lint(query)


def format_results(issues: List[LintIssue], query: str) -> str:
    """Format lint results for display."""
    lines = []

    if not issues:
        lines.append("✅ No issues found")
    else:
        error_count = sum(1 for i in issues if i.severity == Severity.ERROR)
        warning_count = sum(1 for i in issues if i.severity == Severity.WARNING)
        info_count = sum(1 for i in issues if i.severity == Severity.INFO)

        lines.append(f"Found {len(issues)} issue(s): {error_count} errors, {warning_count} warnings, {info_count} info")
        lines.append("")

        for issue in issues:
            lines.append(str(issue))

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="SPARQL query linter")
    parser.add_argument("query", nargs="?", help="SPARQL query string or '-' for stdin")
    parser.add_argument("-f", "--file", type=str, help="Read query from file")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    # Get query
    if args.file:
        query = Path(args.file).read_text(encoding="utf-8")
    elif args.query == "-":
        query = sys.stdin.read()
    elif args.query:
        query = args.query
    else:
        parser.print_help()
        sys.exit(1)

    # Lint query
    issues = lint_query(query)

    # Output results
    if args.json:
        import json
        output = [
            {
                "severity": i.severity.value,
                "line": i.line,
                "column": i.column,
                "message": i.message,
                "rule": i.rule
            }
            for i in issues
        ]
        print(json.dumps(output, indent=2))
    else:
        print(format_results(issues, query))

    # Exit with error if there are errors
    if any(i.severity == Severity.ERROR for i in issues):
        sys.exit(1)


if __name__ == "__main__":
    main()

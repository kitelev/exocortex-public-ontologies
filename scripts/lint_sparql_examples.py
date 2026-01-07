#!/usr/bin/env python3
"""
Lint SPARQL examples in documentation files.

Extracts SPARQL code blocks from markdown files and runs them through sparql_lint.

Usage:
    python scripts/lint_sparql_examples.py [--fix]
"""

import argparse
import re
import sys
from pathlib import Path
from typing import List, Tuple

from sparql_lint import lint_query, Severity, LintIssue


def extract_sparql_blocks(content: str) -> List[Tuple[int, str]]:
    """Extract SPARQL code blocks from markdown content.

    Returns list of (line_number, query) tuples.
    """
    blocks = []
    # Match ```sparql ... ``` blocks
    pattern = re.compile(r"```sparql\s*\n(.*?)```", re.DOTALL | re.IGNORECASE)

    for match in pattern.finditer(content):
        # Calculate line number
        line_num = content[: match.start()].count("\n") + 1
        query = match.group(1).strip()
        if query:
            blocks.append((line_num, query))

    return blocks


def lint_file(filepath: Path) -> List[Tuple[int, str, List[LintIssue]]]:
    """Lint all SPARQL blocks in a markdown file.

    Returns list of (line_number, query, issues) tuples.
    """
    results = []

    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return results

    blocks = extract_sparql_blocks(content)

    for line_num, query in blocks:
        issues = lint_query(query)
        # Filter out INFO-level issues for documentation examples
        issues = [i for i in issues if i.severity != Severity.INFO]
        if issues:
            results.append((line_num, query, issues))

    return results


def main():
    parser = argparse.ArgumentParser(description="Lint SPARQL examples in documentation")
    parser.add_argument("--path", type=str, default="docs", help="Path to search for markdown files")
    parser.add_argument("-v", "--verbose", action="store_true", help="Show all checked files")
    args = parser.parse_args()

    search_path = Path(args.path)
    if not search_path.exists():
        print(f"Path not found: {search_path}")
        sys.exit(1)

    # Find all markdown files
    md_files = list(search_path.rglob("*.md"))

    total_blocks = 0
    total_errors = 0
    total_warnings = 0
    files_with_issues = []

    for filepath in sorted(md_files):
        results = lint_file(filepath)

        if args.verbose:
            blocks = extract_sparql_blocks(filepath.read_text(encoding="utf-8"))
            if blocks:
                print(f"  {filepath}: {len(blocks)} SPARQL block(s)")

        for line_num, query, issues in results:
            if not files_with_issues or files_with_issues[-1][0] != filepath:
                files_with_issues.append((filepath, []))
            files_with_issues[-1][1].append((line_num, query, issues))

            for issue in issues:
                if issue.severity == Severity.ERROR:
                    total_errors += 1
                elif issue.severity == Severity.WARNING:
                    total_warnings += 1

        total_blocks += len(extract_sparql_blocks(filepath.read_text(encoding="utf-8")))

    # Print results
    print(f"\nSPARQL Documentation Linter")
    print(f"=" * 40)
    print(f"Files scanned: {len(md_files)}")
    print(f"SPARQL blocks found: {total_blocks}")
    print(f"Errors: {total_errors}")
    print(f"Warnings: {total_warnings}")
    print()

    if files_with_issues:
        print("Issues found:")
        print("-" * 40)

        for filepath, file_issues in files_with_issues:
            print(f"\n{filepath}:")
            for line_num, query, issues in file_issues:
                print(f"  Line {line_num}:")
                # Show first line of query
                first_line = query.split("\n")[0][:60]
                print(f"    Query: {first_line}...")
                for issue in issues:
                    icon = "❌" if issue.severity == Severity.ERROR else "⚠️"
                    print(f"    {icon} {issue.message}")
    else:
        print("✅ No issues found in SPARQL examples")

    # Exit with error if there are errors
    if total_errors > 0:
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()

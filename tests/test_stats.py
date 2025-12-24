#!/usr/bin/env python3
"""Tests for stats.py"""

import sys
from pathlib import Path

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from stats import (  # noqa: E402
    parse_frontmatter,
    extract_wikilinks,
    PREFIXES,
)


class TestStatsParseFrontmatter:
    """Tests for parse_frontmatter in stats.py."""

    def test_valid_statement(self, tmp_path):
        """Test parsing valid statement frontmatter."""
        file = tmp_path / "test.md"
        file.write_text(
            """---
metadata: statement
subject: "[[aaa]]"
predicate: "[[bbb]]"
object: "[[ccc]]"
aliases:
  - "test alias"
---
"""
        )

        data = parse_frontmatter(file)

        assert data is not None
        assert data["metadata"] == "statement"
        assert "subject" in data
        assert "aliases" in data

    def test_invalid_file(self, tmp_path):
        """Test parsing invalid file returns None."""
        file = tmp_path / "test.md"
        file.write_text("no frontmatter")

        data = parse_frontmatter(file)

        assert data is None


class TestStatsExtractWikilinks:
    """Tests for extract_wikilinks in stats.py."""

    def test_extract_from_statement(self):
        """Test extracting wikilinks from statement data."""
        data = {
            "subject": "[[uuid1]]",
            "predicate": "[[uuid2|alias]]",
            "object": "[[uuid3]]",
        }

        links = extract_wikilinks(data)

        assert "uuid1" in links
        assert "uuid2" in links
        assert "uuid3" in links

    def test_literal_object_no_wikilink(self):
        """Test literal objects don't extract as wikilinks."""
        data = {
            "subject": "[[uuid1]]",
            "predicate": "[[uuid2]]",
            "object": '"just a string"',
        }

        links = extract_wikilinks(data)

        assert "uuid1" in links
        assert "uuid2" in links
        assert len(links) == 2


class TestPrefixes:
    """Tests for PREFIXES constant."""

    def test_all_expected_prefixes(self):
        """Test all expected prefixes are present."""
        expected = ["rdf", "rdfs", "owl", "xsd", "dc", "dcterms", "skos", "foaf", "prov", "vs", "sh", "sosa", "as"]

        for prefix in expected:
            assert prefix in PREFIXES, f"Missing prefix: {prefix}"

    def test_no_duplicates(self):
        """Test no duplicate prefixes."""
        assert len(PREFIXES) == len(set(PREFIXES))

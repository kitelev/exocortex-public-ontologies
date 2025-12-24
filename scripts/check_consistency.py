#!/usr/bin/env python3
"""
Check consistency across ontology namespaces.

Performs cross-namespace checks:
- Cross-reference integrity (wikilinks between namespaces)
- Duplicate anchor detection (same URI in multiple namespaces)
- Subject-namespace alignment (statements in correct namespace)
- Alias format consistency
- External reference analysis

Usage:
    python scripts/check_consistency.py [--verbose] [--fix]
"""

import argparse
import re
import yaml
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

# Repository root (relative to script location)
REPO_ROOT = Path(__file__).parent.parent

# Namespace prefixes
PREFIXES = [
    "rdf",
    "rdfs",
    "owl",
    "dc",
    "dcterms",
    "dcam",
    "skos",
    "foaf",
    "prov",
    "time",
    "geo",
    "vcard",
    "doap",
    "sioc",
    "xsd",
    "dcat",
    "org",
    "schema",
    "vs",
    "sh",
    "sosa",
    "as",
    "void",
    "geosparql",
]

# Namespace URI to prefix mapping
NS_URI_TO_PREFIX = {
    "http://www.w3.org/1999/02/22-rdf-syntax-ns#": "rdf",
    "http://www.w3.org/2000/01/rdf-schema#": "rdfs",
    "http://www.w3.org/2002/07/owl#": "owl",
    "http://purl.org/dc/elements/1.1/": "dc",
    "http://purl.org/dc/terms/": "dcterms",
    "http://purl.org/dc/dcam/": "dcam",
    "http://www.w3.org/2004/02/skos/core#": "skos",
    "http://xmlns.com/foaf/0.1/": "foaf",
    "http://www.w3.org/ns/prov#": "prov",
    "http://www.w3.org/2006/time#": "time",
    "http://www.w3.org/2003/01/geo/wgs84_pos#": "geo",
    "http://www.w3.org/2006/vcard/ns#": "vcard",
    "http://usefulinc.com/ns/doap#": "doap",
    "http://rdfs.org/sioc/ns#": "sioc",
    "http://www.w3.org/2001/XMLSchema#": "xsd",
    "http://www.w3.org/ns/dcat#": "dcat",
    "http://www.w3.org/ns/org#": "org",
    "https://schema.org/": "schema",
    "http://www.w3.org/2003/06/sw-vocab-status/ns#": "vs",
    "http://www.w3.org/ns/shacl#": "sh",
    "http://www.w3.org/ns/sosa/": "sosa",
    "https://www.w3.org/ns/activitystreams#": "as",
    "http://rdfs.org/ns/void#": "void",
    "http://www.opengis.net/ont/geosparql#": "geosparql",
}


def parse_frontmatter(filepath: Path) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
    """Parse YAML frontmatter from a markdown file."""
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        return None, f"Could not read file: {e}"

    if not content.startswith("---"):
        return None, "No frontmatter"

    end_match = re.search(r"\n---\s*\n", content[3:])
    if not end_match:
        end_match = re.search(r"\n---\s*$", content[3:])
        if not end_match:
            return None, "No closing ---"

    yaml_content = content[4 : 3 + end_match.start()]

    try:
        data = yaml.safe_load(yaml_content)
        return data if data else {}, None
    except yaml.YAMLError as e:
        return None, f"YAML error: {e}"


def extract_wikilinks(data: Dict[str, Any]) -> Set[str]:
    """Extract all wikilink targets from frontmatter values."""
    links = set()
    wikilink_pattern = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")

    for key, value in data.items():
        if isinstance(value, str):
            for match in wikilink_pattern.finditer(value):
                links.add(match.group(1))

    return links


def get_prefix_from_uri(uri: str) -> Optional[str]:
    """Get namespace prefix from a full URI."""
    for ns_uri, prefix in NS_URI_TO_PREFIX.items():
        if uri.startswith(ns_uri):
            return prefix
    return None


def collect_all_data(repo_root: Path) -> Dict[str, Any]:
    """Collect all anchors, statements, and namespaces."""
    data = {
        "anchors": {},  # uuid -> {uri, prefix, filepath}
        "statements": [],  # list of {filepath, subject, predicate, object, wikilinks}
        "namespaces": {},  # uuid -> {uri, prefix, filepath}
        "blank_nodes": {},  # uuid -> {uri, prefix, filepath}
        "uri_to_uuid": {},  # uri -> uuid (for duplicate detection)
        "uuid_to_ns": {},  # uuid -> namespace directory
    }

    for ns in PREFIXES:
        ns_dir = repo_root / ns
        if not ns_dir.exists():
            continue

        for filepath in ns_dir.glob("*.md"):
            fm, error = parse_frontmatter(filepath)
            if error or not fm:
                continue

            metadata = fm.get("metadata")
            file_uuid = filepath.stem

            data["uuid_to_ns"][file_uuid] = ns

            if metadata == "anchor":
                uri = fm.get("uri", "")
                prefix = get_prefix_from_uri(uri) if uri else None
                data["anchors"][file_uuid] = {
                    "uri": uri,
                    "prefix": prefix,
                    "filepath": filepath,
                    "namespace": ns,
                    "aliases": fm.get("aliases", []),
                }
                if uri:
                    if uri in data["uri_to_uuid"]:
                        data["uri_to_uuid"][uri].append(file_uuid)
                    else:
                        data["uri_to_uuid"][uri] = [file_uuid]

            elif metadata == "namespace":
                uri = fm.get("uri", "")
                data["namespaces"][file_uuid] = {
                    "uri": uri,
                    "filepath": filepath,
                    "namespace": ns,
                    "aliases": fm.get("aliases", []),
                }

            elif metadata == "blank_node":
                uri = fm.get("uri", "")
                data["blank_nodes"][file_uuid] = {
                    "uri": uri,
                    "filepath": filepath,
                    "namespace": ns,
                }

            elif metadata == "statement":
                wikilinks = extract_wikilinks(fm)
                data["statements"].append(
                    {
                        "filepath": filepath,
                        "namespace": ns,
                        "subject": fm.get("subject", ""),
                        "predicate": fm.get("predicate", ""),
                        "object": fm.get("object", ""),
                        "wikilinks": wikilinks,
                        "aliases": fm.get("aliases", []),
                    }
                )

    return data


def check_duplicate_anchors(data: Dict[str, Any], verbose: bool) -> List[Tuple[str, List[str]]]:
    """Find URIs that are defined in multiple anchor files."""
    duplicates = []
    for uri, uuids in data["uri_to_uuid"].items():
        if len(uuids) > 1:
            duplicates.append((uri, uuids))
            if verbose:
                print(f"  Duplicate URI: {uri}")
                for uuid in uuids:
                    anchor = data["anchors"].get(uuid, {})
                    print(f"    - {anchor.get('namespace', '?')}/{uuid}.md")
    return duplicates


def check_cross_namespace_refs(data: Dict[str, Any], verbose: bool) -> Dict[str, List[Tuple[str, str, str]]]:
    """Analyze cross-namespace references."""
    cross_refs = defaultdict(list)  # from_ns -> [(to_ns, uuid, filepath)]

    all_known_uuids = set(data["anchors"].keys()) | set(data["namespaces"].keys()) | set(data["blank_nodes"].keys())

    for stmt in data["statements"]:
        from_ns = stmt["namespace"]
        for link in stmt["wikilinks"]:
            if link in all_known_uuids:
                to_ns = data["uuid_to_ns"].get(link)
                if to_ns and to_ns != from_ns:
                    cross_refs[from_ns].append((to_ns, link, str(stmt["filepath"])))

    if verbose:
        for from_ns, refs in sorted(cross_refs.items()):
            to_counts = defaultdict(int)
            for to_ns, _, _ in refs:
                to_counts[to_ns] += 1
            print(f"  {from_ns} -> " + ", ".join(f"{ns}:{count}" for ns, count in sorted(to_counts.items())))

    return dict(cross_refs)


def check_external_refs(data: Dict[str, Any], verbose: bool) -> Dict[str, int]:
    """Find references to UUIDs not in any known namespace."""
    external_counts = defaultdict(int)
    all_known_uuids = set(data["anchors"].keys()) | set(data["namespaces"].keys()) | set(data["blank_nodes"].keys())

    for stmt in data["statements"]:
        for link in stmt["wikilinks"]:
            if link not in all_known_uuids:
                external_counts[link] += 1

    if verbose and external_counts:
        print(f"  Found {len(external_counts)} unique external references")
        for uuid, count in sorted(external_counts.items(), key=lambda x: -x[1])[:10]:
            print(f"    {uuid}: {count} refs")

    return dict(external_counts)


def check_subject_namespace_alignment(data: Dict[str, Any], verbose: bool) -> List[Tuple[str, str, str]]:
    """Check that statement subjects are in the correct namespace directory."""
    misaligned = []
    wikilink_pattern = re.compile(r"\[\[([^\]|]+)")

    for stmt in data["statements"]:
        subject = stmt["subject"]
        match = wikilink_pattern.search(subject)
        if match:
            subj_uuid = match.group(1)
            subj_ns = data["uuid_to_ns"].get(subj_uuid)
            stmt_ns = stmt["namespace"]

            # Statement should be in the same namespace as its subject
            # (unless subject is external)
            if subj_ns and subj_ns != stmt_ns:
                misaligned.append((str(stmt["filepath"]), subj_ns, stmt_ns))
                if verbose:
                    print(f"  {stmt_ns}/{stmt['filepath'].name}: subject from {subj_ns}")

    return misaligned


def check_alias_format(data: Dict[str, Any], verbose: bool) -> List[Tuple[str, str, str]]:
    """Check that aliases follow expected format."""
    issues = []

    # Check anchor aliases (should be prefix:localname)
    for uuid, anchor in data["anchors"].items():
        aliases = anchor.get("aliases", [])
        if not aliases:
            issues.append((str(anchor["filepath"]), "anchor", "missing alias"))
            if verbose:
                print(f"  {anchor['namespace']}/{uuid}.md: missing anchor alias")
        else:
            alias = aliases[0]
            # Anchor alias should contain ':' OR be a schema.org extension domain
            is_schema_extension = alias.endswith(".schema.org")
            if ":" not in alias and not alias.startswith("_:") and not is_schema_extension:
                issues.append((str(anchor["filepath"]), "anchor", f"invalid format: {alias}"))
                if verbose:
                    print(f"  {anchor['namespace']}/{uuid}.md: invalid alias format '{alias}'")

    # Check namespace aliases (should be !prefix)
    for uuid, ns in data["namespaces"].items():
        aliases = ns.get("aliases", [])
        if not aliases:
            issues.append((str(ns["filepath"]), "namespace", "missing alias"))
            if verbose:
                print(f"  {ns['namespace']}/{uuid}.md: missing namespace alias")
        else:
            alias = aliases[0]
            if not alias.startswith("!"):
                issues.append((str(ns["filepath"]), "namespace", f"should start with !: {alias}"))
                if verbose:
                    print(f"  {ns['namespace']}/{uuid}.md: namespace alias should start with !")

    return issues


def print_summary(
    duplicates: List[Tuple[str, List[str]]],
    cross_refs: Dict[str, List[Tuple[str, str, str]]],
    external_refs: Dict[str, int],
    misaligned: List[Tuple[str, str, str]],
    alias_issues: List[Tuple[str, str, str]],
) -> None:
    """Print summary of consistency check results."""
    print("\n" + "=" * 60)
    print("CONSISTENCY CHECK SUMMARY")
    print("=" * 60)

    total_cross = sum(len(refs) for refs in cross_refs.values())
    total_external = sum(external_refs.values())

    print(f"\n  Duplicate URIs:           {len(duplicates)}")
    print(f"  Cross-namespace refs:     {total_cross}")
    print(f"  External refs:            {total_external} ({len(external_refs)} unique)")
    print(f"  Subject misalignments:    {len(misaligned)}")
    print(f"  Alias issues:             {len(alias_issues)}")

    # Status
    has_issues = duplicates or misaligned or alias_issues
    print("\n" + "-" * 60)
    if has_issues:
        print("STATUS: Issues found (see above)")
    else:
        print("STATUS: All checks passed")


def main() -> None:
    parser = argparse.ArgumentParser(description="Check ontology consistency")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

    print("=" * 60)
    print("Exocortex Public Ontologies - Consistency Check")
    print("=" * 60)
    print()

    print("Collecting data...")
    data = collect_all_data(REPO_ROOT)
    print(f"  Anchors: {len(data['anchors'])}")
    print(f"  Namespaces: {len(data['namespaces'])}")
    print(f"  Blank nodes: {len(data['blank_nodes'])}")
    print(f"  Statements: {len(data['statements'])}")

    print("\nChecking for duplicate URIs...")
    duplicates = check_duplicate_anchors(data, args.verbose)

    print("\nAnalyzing cross-namespace references...")
    cross_refs = check_cross_namespace_refs(data, args.verbose)

    print("\nFinding external references...")
    external_refs = check_external_refs(data, args.verbose)

    print("\nChecking subject-namespace alignment...")
    misaligned = check_subject_namespace_alignment(data, args.verbose)

    print("\nChecking alias format...")
    alias_issues = check_alias_format(data, args.verbose)

    print_summary(duplicates, cross_refs, external_refs, misaligned, alias_issues)


if __name__ == "__main__":
    main()

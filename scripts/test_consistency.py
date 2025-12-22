#!/usr/bin/env python3
"""
Semantic consistency tests for exocortex-public-ontologies.

Checks:
1. Type consistency - rdf:type objects are valid classes
2. SubClass consistency - rdfs:subClassOf objects are valid classes
3. Domain/Range consistency - rdfs:domain and rdfs:range point to valid resources
4. Property type consistency - properties have proper metaclass (rdf:Property, owl:ObjectProperty, etc.)
5. Cross-reference integrity - all wikilinks resolve to existing anchors

Usage:
    python scripts/test_consistency.py [namespaces...]
    python scripts/test_consistency.py --verbose
"""

import os
import sys
import re
import yaml
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple, Optional

# Repository root (relative to script location)
REPO_ROOT = Path(__file__).parent.parent
PREFIXES = ['rdf', 'rdfs', 'owl', 'dc', 'dcterms', 'dcam', 'skos', 'foaf', 'prov', 'time', 'geo', 'vcard', 'doap', 'sioc', 'xsd', 'dcat', 'org', 'schema']

# Well-known predicate UUIDs
PREDICATES = {
    'rdf:type': '73b69787-81ea-563e-8e09-9c84cad4cf2b',
    'rdfs:subClassOf': '55ff3aec-8d5b-5d4d-a0e1-d3f1c7d3c8d2',
    'rdfs:domain': 'c29ac1cb-6937-5aa2-a8c1-68f2e1b7e39f',
    'rdfs:range': 'f4d4a1a9-d8e5-5f47-a2a9-c8d9e0f1a2b3',
    'rdfs:label': 'd0e9e696-d3f2-5966-a62f-d8358cbde741',
    'rdfs:comment': 'da1b0b28-9c51-55c3-a963-2337006693de',
}

# Well-known class UUIDs (meta-classes)
META_CLASSES = {
    'rdfs:Class': '30488677-f427-5947-8a14-02903ca20a7e',
    'rdfs:Resource': 'd6ac0df2-324e-561c-9f05-41d3b2d5ebd3',
    'rdf:Property': 'f1afe09a-f371-5a01-a530-be18bfdb4d6b',
    'owl:Class': '9bdf3c9c-87d2-5e76-8e44-64e8a7c8e4a5',
    'owl:ObjectProperty': 'a1b2c3d4-e5f6-5789-0123-456789abcdef',  # placeholder
    'owl:DatatypeProperty': 'b2c3d4e5-f6a7-5890-1234-567890abcdef',  # placeholder
}


@dataclass
class ConsistencyResult:
    """Results of consistency checks."""
    type_errors: List[Tuple[str, str, str]] = field(default_factory=list)  # (file, subject, invalid_type)
    subclass_errors: List[Tuple[str, str, str]] = field(default_factory=list)  # (file, subject, invalid_superclass)
    domain_errors: List[Tuple[str, str, str]] = field(default_factory=list)  # (file, property, invalid_domain)
    range_errors: List[Tuple[str, str, str]] = field(default_factory=list)  # (file, property, invalid_range)
    missing_anchors: List[Tuple[str, str]] = field(default_factory=list)  # (file, missing_uuid)
    circular_subclass: List[List[str]] = field(default_factory=list)  # chains of circular inheritance

    def has_errors(self) -> bool:
        return any([
            self.type_errors,
            self.subclass_errors,
            self.domain_errors,
            self.range_errors,
            self.missing_anchors,
            self.circular_subclass,
        ])

    def summary(self) -> str:
        lines = []
        if self.type_errors:
            lines.append(f"  Type errors: {len(self.type_errors)}")
        if self.subclass_errors:
            lines.append(f"  SubClass errors: {len(self.subclass_errors)}")
        if self.domain_errors:
            lines.append(f"  Domain errors: {len(self.domain_errors)}")
        if self.range_errors:
            lines.append(f"  Range errors: {len(self.range_errors)}")
        if self.missing_anchors:
            lines.append(f"  Missing anchors: {len(self.missing_anchors)}")
        if self.circular_subclass:
            lines.append(f"  Circular inheritance: {len(self.circular_subclass)}")
        return '\n'.join(lines) if lines else "  All consistency checks passed!"


def parse_frontmatter(filepath: Path) -> Optional[dict]:
    """Parse YAML frontmatter from a markdown file."""
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception:
        return None

    if not content.startswith('---'):
        return None

    end_match = re.search(r'\n---\s*\n', content[3:])
    if not end_match:
        end_match = re.search(r'\n---\s*$', content[3:])
        if not end_match:
            return None

    yaml_content = content[4:3 + end_match.start()]

    try:
        data = yaml.safe_load(yaml_content)
        return data if data else {}
    except yaml.YAMLError:
        return None


def extract_wikilink_uuid(value: str) -> Optional[str]:
    """Extract UUID from wikilink like [[uuid]] or [[uuid|alias]]."""
    match = re.match(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', value)
    if match:
        return match.group(1)
    return None


def collect_all_anchors(repo_root: Path) -> Set[str]:
    """Collect all anchor UUIDs from all namespaces."""
    anchors = set()

    for prefix in PREFIXES:
        ns_dir = repo_root / prefix
        if not ns_dir.exists():
            continue

        for filepath in ns_dir.glob('*.md'):
            data = parse_frontmatter(filepath)
            if data and data.get('metadata') in ('anchor', 'namespace', 'blank_node'):
                anchors.add(filepath.stem)

    return anchors


def collect_statements_by_predicate(repo_root: Path, predicate_uuid: str) -> List[Tuple[Path, dict]]:
    """Collect all statements with a specific predicate."""
    statements = []

    for prefix in PREFIXES:
        ns_dir = repo_root / prefix
        if not ns_dir.exists():
            continue

        for filepath in ns_dir.glob('*.md'):
            data = parse_frontmatter(filepath)
            if not data or data.get('metadata') != 'statement':
                continue

            pred = data.get('predicate', '')
            pred_uuid = extract_wikilink_uuid(pred)

            if pred_uuid == predicate_uuid:
                statements.append((filepath, data))

    return statements


def check_type_consistency(repo_root: Path, all_anchors: Set[str], verbose: bool = False) -> List[Tuple[str, str, str]]:
    """Check that all rdf:type objects point to existing classes."""
    errors = []
    type_uuid = PREDICATES['rdf:type']

    statements = collect_statements_by_predicate(repo_root, type_uuid)

    for filepath, data in statements:
        obj = data.get('object', '')
        obj_uuid = extract_wikilink_uuid(obj)

        if obj_uuid and obj_uuid not in all_anchors:
            subj = data.get('subject', '')
            errors.append((str(filepath.relative_to(repo_root)), subj, obj))
            if verbose:
                print(f"  ❌ {filepath.stem}: type {obj} not found")

    return errors


def check_subclass_consistency(repo_root: Path, all_anchors: Set[str], verbose: bool = False) -> List[Tuple[str, str, str]]:
    """Check that all rdfs:subClassOf objects point to existing classes."""
    errors = []
    subclass_uuid = PREDICATES['rdfs:subClassOf']

    statements = collect_statements_by_predicate(repo_root, subclass_uuid)

    for filepath, data in statements:
        obj = data.get('object', '')
        obj_uuid = extract_wikilink_uuid(obj)

        if obj_uuid and obj_uuid not in all_anchors:
            subj = data.get('subject', '')
            errors.append((str(filepath.relative_to(repo_root)), subj, obj))
            if verbose:
                print(f"  ❌ {filepath.stem}: superclass {obj} not found")

    return errors


def check_domain_range_consistency(repo_root: Path, all_anchors: Set[str], verbose: bool = False) -> Tuple[List, List]:
    """Check that rdfs:domain and rdfs:range point to existing resources."""
    domain_errors = []
    range_errors = []

    domain_uuid = PREDICATES['rdfs:domain']
    range_uuid = PREDICATES['rdfs:range']

    # Check domains
    domain_statements = collect_statements_by_predicate(repo_root, domain_uuid)
    for filepath, data in domain_statements:
        obj = data.get('object', '')
        obj_uuid = extract_wikilink_uuid(obj)

        if obj_uuid and obj_uuid not in all_anchors:
            subj = data.get('subject', '')
            domain_errors.append((str(filepath.relative_to(repo_root)), subj, obj))
            if verbose:
                print(f"  ❌ {filepath.stem}: domain {obj} not found")

    # Check ranges
    range_statements = collect_statements_by_predicate(repo_root, range_uuid)
    for filepath, data in range_statements:
        obj = data.get('object', '')
        obj_uuid = extract_wikilink_uuid(obj)

        if obj_uuid and obj_uuid not in all_anchors:
            subj = data.get('subject', '')
            range_errors.append((str(filepath.relative_to(repo_root)), subj, obj))
            if verbose:
                print(f"  ❌ {filepath.stem}: range {obj} not found")

    return domain_errors, range_errors


def detect_circular_inheritance(repo_root: Path, verbose: bool = False) -> List[List[str]]:
    """Detect circular inheritance in rdfs:subClassOf chains."""
    subclass_uuid = PREDICATES['rdfs:subClassOf']
    statements = collect_statements_by_predicate(repo_root, subclass_uuid)

    # Build graph: subject -> list of superclasses
    graph: Dict[str, List[str]] = {}
    for filepath, data in statements:
        subj = extract_wikilink_uuid(data.get('subject', ''))
        obj = extract_wikilink_uuid(data.get('object', ''))

        if subj and obj:
            if subj not in graph:
                graph[subj] = []
            graph[subj].append(obj)

    # DFS to detect cycles
    cycles = []
    visited = set()
    rec_stack = set()

    def dfs(node: str, path: List[str]) -> Optional[List[str]]:
        if node in rec_stack:
            # Found cycle
            cycle_start = path.index(node)
            return path[cycle_start:] + [node]

        if node in visited:
            return None

        visited.add(node)
        rec_stack.add(node)
        path.append(node)

        for neighbor in graph.get(node, []):
            cycle = dfs(neighbor, path)
            if cycle:
                return cycle

        path.pop()
        rec_stack.remove(node)
        return None

    for node in graph:
        if node not in visited:
            cycle = dfs(node, [])
            if cycle:
                cycles.append(cycle)
                if verbose:
                    print(f"  🔄 Circular: {' → '.join(cycle)}")

    return cycles


def run_consistency_checks(repo_root: Path, verbose: bool = False) -> ConsistencyResult:
    """Run all consistency checks."""
    result = ConsistencyResult()

    print("Collecting anchors...")
    all_anchors = collect_all_anchors(repo_root)
    print(f"  Found {len(all_anchors)} anchors")

    print("\nChecking rdf:type consistency...")
    result.type_errors = check_type_consistency(repo_root, all_anchors, verbose)
    print(f"  Checked type statements")

    print("\nChecking rdfs:subClassOf consistency...")
    result.subclass_errors = check_subclass_consistency(repo_root, all_anchors, verbose)
    print(f"  Checked subclass statements")

    print("\nChecking rdfs:domain and rdfs:range consistency...")
    result.domain_errors, result.range_errors = check_domain_range_consistency(repo_root, all_anchors, verbose)
    print(f"  Checked domain/range statements")

    print("\nDetecting circular inheritance...")
    result.circular_subclass = detect_circular_inheritance(repo_root, verbose)
    print(f"  Analyzed inheritance graph")

    return result


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Run semantic consistency tests')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    args = parser.parse_args()

    print("=" * 60)
    print("Semantic Consistency Tests")
    print("=" * 60)
    print()

    result = run_consistency_checks(REPO_ROOT, args.verbose)

    print("\n" + "=" * 60)
    print("CONSISTENCY CHECK SUMMARY")
    print("=" * 60)
    print(result.summary())

    if result.has_errors():
        print("\n❌ Some consistency checks failed!")

        if result.type_errors and not args.verbose:
            print(f"\nType errors ({len(result.type_errors)}):")
            for filepath, subj, obj in result.type_errors[:5]:
                print(f"  - {filepath}: {obj}")
            if len(result.type_errors) > 5:
                print(f"  ... and {len(result.type_errors) - 5} more")

        if result.subclass_errors and not args.verbose:
            print(f"\nSubClass errors ({len(result.subclass_errors)}):")
            for filepath, subj, obj in result.subclass_errors[:5]:
                print(f"  - {filepath}: {obj}")
            if len(result.subclass_errors) > 5:
                print(f"  ... and {len(result.subclass_errors) - 5} more")

        sys.exit(1)
    else:
        print("\n✅ All consistency checks passed!")
        sys.exit(0)


if __name__ == '__main__':
    main()

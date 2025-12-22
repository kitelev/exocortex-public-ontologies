#!/usr/bin/env python3
"""
Validation tools for exocortex-public-ontologies.

Checks:
1. Orphaned anchors - anchors not referenced in any statement
2. External wikilinks - references to anchors not in this repository (INFO only, not error)
3. File format - proper YAML frontmatter structure
4. Metadata consistency - all files have valid metadata property
5. Blank node format - proper naming convention {namespace}!{uuid}

Note: External wikilinks (to resources defined in other ontologies) are allowed.
These are reported as INFO but do not cause validation failure.

Usage:
    python scripts/validate.py [--fix] [--verbose]
"""

import os
import re
import sys
import yaml
from pathlib import Path
from typing import Dict, List, Set, Tuple
from dataclasses import dataclass, field

# Repository root (relative to script location)
REPO_ROOT = Path(__file__).parent.parent
# Namespace prefixes (short names for namespace URIs, e.g., 'rdf' for http://www.w3.org/1999/02/22-rdf-syntax-ns#)
PREFIXES = ['rdf', 'rdfs', 'owl', 'dc', 'dcterms', 'dcam', 'skos', 'foaf', 'prov', 'time', 'geo', 'vcard', 'doap', 'sioc', 'xsd', 'dcat', 'org', 'schema']
EXCLUDED_DIRS = ['~templates', 'scripts', '.git']


# Required properties for statement files (exactly these 4 required + optional aliases)
STATEMENT_REQUIRED_PROPS = {'metadata', 'subject', 'predicate', 'object'}
STATEMENT_OPTIONAL_PROPS = {'aliases'}

# Required properties for anchor files (metadata required, uri and aliases optional)
ANCHOR_REQUIRED_PROPS = {'metadata'}
ANCHOR_OPTIONAL_PROPS = {'uri', 'aliases'}

# Required properties for namespace files
NAMESPACE_REQUIRED_PROPS = {'metadata', 'uri'}
NAMESPACE_OPTIONAL_PROPS = {'aliases'}

# Required properties for blank_node files
BLANK_NODE_REQUIRED_PROPS = {'metadata', 'uri'}
BLANK_NODE_OPTIONAL_PROPS = {'aliases'}

# Valid metadata values
VALID_METADATA = {'namespace', 'anchor', 'statement', 'blank_node', 'index'}

# UUID pattern: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx (standard UUID format)
UUID_PATTERN = re.compile(r'^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$')


@dataclass
class ValidationResult:
    """Holds validation results."""
    orphaned_anchors: List[str] = field(default_factory=list)
    external_wikilinks: List[Tuple[str, str]] = field(default_factory=list)  # INFO only, not error
    invalid_frontmatter: List[Tuple[str, str]] = field(default_factory=list)
    missing_metadata: List[str] = field(default_factory=list)
    invalid_metadata: List[Tuple[str, str]] = field(default_factory=list)
    naming_violations: List[Tuple[str, str]] = field(default_factory=list)
    frontmatter_prop_violations: List[Tuple[str, str]] = field(default_factory=list)
    has_body_violations: List[str] = field(default_factory=list)
    orphaned_blank_nodes: List[str] = field(default_factory=list)
    undefined_blank_nodes: List[Tuple[str, str]] = field(default_factory=list)

    def has_errors(self) -> bool:
        """Check if there are any validation errors.

        Note: external_wikilinks are NOT errors - they are expected when
        referencing resources from other ontologies.
        """
        return any([
            self.orphaned_anchors,
            # external_wikilinks are INFO only, not errors
            self.invalid_frontmatter,
            self.missing_metadata,
            self.invalid_metadata,
            self.naming_violations,
            self.frontmatter_prop_violations,
            self.has_body_violations,
            self.orphaned_blank_nodes,
            self.undefined_blank_nodes
        ])

    def summary(self) -> str:
        lines = []
        if self.orphaned_anchors:
            lines.append(f"  Orphaned anchors: {len(self.orphaned_anchors)}")
        if self.external_wikilinks:
            lines.append(f"  External wikilinks (INFO): {len(self.external_wikilinks)}")
        if self.invalid_frontmatter:
            lines.append(f"  Invalid frontmatter: {len(self.invalid_frontmatter)}")
        if self.missing_metadata:
            lines.append(f"  Missing metadata: {len(self.missing_metadata)}")
        if self.invalid_metadata:
            lines.append(f"  Invalid metadata: {len(self.invalid_metadata)}")
        if self.naming_violations:
            lines.append(f"  Naming convention violations: {len(self.naming_violations)}")
        if self.frontmatter_prop_violations:
            lines.append(f"  Frontmatter property violations: {len(self.frontmatter_prop_violations)}")
        if self.has_body_violations:
            lines.append(f"  Files with body content: {len(self.has_body_violations)}")
        if self.orphaned_blank_nodes:
            lines.append(f"  Orphaned blank nodes: {len(self.orphaned_blank_nodes)}")
        if self.undefined_blank_nodes:
            lines.append(f"  Undefined blank nodes: {len(self.undefined_blank_nodes)}")
        return '\n'.join(lines) if lines else "  All checks passed!"


def check_naming_convention(filepath: Path, metadata: str) -> Tuple[bool, str]:
    """
    Check if filename follows naming convention.

    All files MUST be UUIDv5:
    - Namespace: {uuid}.md (from namespace URI)
    - Anchor: {uuid}.md (from resource URI)
    - Blank node: {uuid}.md (from skolem IRI)
    - Statement: {uuid}.md (from canonical triple)
    """
    filename = filepath.stem  # without .md

    # All files must be UUID format
    if UUID_PATTERN.match(filename):
        return True, ""  # Valid UUID format

    # Non-UUID format - not allowed
    return False, f"Filename must be UUID format, got: {filename}"


def parse_frontmatter(filepath: Path) -> Tuple[dict, str]:
    """Parse YAML frontmatter from a markdown file."""
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception as e:
        return None, f"Cannot read file: {e}"

    if not content.startswith('---'):
        return None, "No frontmatter found (missing opening ---)"

    # Find closing ---
    end_match = re.search(r'\n---\s*\n', content[3:])
    if not end_match:
        # Try end of file
        end_match = re.search(r'\n---\s*$', content[3:])
        if not end_match:
            return None, "No closing --- found"

    yaml_content = content[4:3 + end_match.start()]

    try:
        data = yaml.safe_load(yaml_content)
        return data if data else {}, None
    except yaml.YAMLError as e:
        return None, f"YAML parse error: {e}"


def has_body_content(filepath: Path) -> bool:
    """Check if file has any content after frontmatter (body)."""
    try:
        content = filepath.read_text(encoding='utf-8')
    except Exception:
        return False

    if not content.startswith('---'):
        return True  # No frontmatter means everything is body

    # Find closing ---
    end_match = re.search(r'\n---\s*\n', content[3:])
    if not end_match:
        end_match = re.search(r'\n---\s*$', content[3:])
        if not end_match:
            return False  # Invalid file

    # Content after closing ---
    body_start = 3 + end_match.end()
    body = content[body_start:].strip()
    return len(body) > 0


def extract_wikilinks(data: dict) -> Set[str]:
    """Extract all wikilink targets from frontmatter values."""
    links = set()
    wikilink_pattern = re.compile(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]')

    for key, value in data.items():
        if isinstance(value, str):
            for match in wikilink_pattern.finditer(value):
                links.add(match.group(1))

    return links


def get_all_anchors(repo_root: Path) -> Set[str]:
    """Get all anchor names (files with metadata: anchor, namespace, or blank_node)."""
    anchors = set()

    for ns in PREFIXES:
        ns_dir = repo_root / ns
        if not ns_dir.exists():
            continue

        for filepath in ns_dir.glob('*.md'):
            data, error = parse_frontmatter(filepath)
            if data and data.get('metadata') in ('anchor', 'namespace', 'blank_node'):
                # Anchor name is filename without .md
                anchors.add(filepath.stem)

    return anchors


def validate_file(filepath: Path, all_anchors: Set[str], all_anchors_lower: Set[str], result: ValidationResult, verbose: bool = False):
    """Validate a single file.

    Args:
        all_anchors: Set of anchor names (original case)
        all_anchors_lower: Set of anchor names (lowercase) for case-insensitive comparison
    """
    rel_path = filepath.relative_to(REPO_ROOT)

    # Parse frontmatter
    data, error = parse_frontmatter(filepath)
    if error:
        result.invalid_frontmatter.append((str(rel_path), error))
        if verbose:
            print(f"  ❌ {rel_path}: {error}")
        return

    # Check metadata property
    metadata = data.get('metadata')
    if not metadata:
        result.missing_metadata.append(str(rel_path))
        if verbose:
            print(f"  ⚠️  {rel_path}: missing metadata property")
    elif metadata not in VALID_METADATA:
        result.invalid_metadata.append((str(rel_path), f"invalid value: {metadata}"))
        if verbose:
            print(f"  ❌ {rel_path}: invalid metadata value '{metadata}'")

    # Check wikilinks in statements
    if metadata == 'statement':
        wikilinks = extract_wikilinks(data)
        for link in wikilinks:
            # Use case-insensitive comparison for macOS compatibility
            if link.lower() not in all_anchors_lower:
                # External wikilinks are allowed (resources may be defined elsewhere)
                result.external_wikilinks.append((str(rel_path), link))
                if verbose:
                    print(f"  ℹ️  {rel_path}: external link [[{link}]]")

        # Check statement has exactly 4 required properties + optional aliases
        props = set(data.keys())
        allowed = STATEMENT_REQUIRED_PROPS | STATEMENT_OPTIONAL_PROPS
        missing = STATEMENT_REQUIRED_PROPS - props
        extra = props - allowed
        if missing or extra:
            errors = []
            if missing:
                errors.append(f"missing: {', '.join(sorted(missing))}")
            if extra:
                errors.append(f"extra: {', '.join(sorted(extra))}")
            error_msg = f"statement: {'; '.join(errors)}"
            result.frontmatter_prop_violations.append((str(rel_path), error_msg))
            if verbose:
                print(f"  📋 {rel_path}: {error_msg}")

    # Check anchor has required properties (metadata) and optional (uri)
    if metadata == 'anchor':
        props = set(data.keys())
        allowed = ANCHOR_REQUIRED_PROPS | ANCHOR_OPTIONAL_PROPS
        extra = props - allowed
        if extra:
            error_msg = f"anchor: extra properties: {', '.join(sorted(extra))}"
            result.frontmatter_prop_violations.append((str(rel_path), error_msg))
            if verbose:
                print(f"  📋 {rel_path}: {error_msg}")

    # Check blank_node has required properties (metadata) and optional (skolem_iri)
    if metadata == 'blank_node':
        props = set(data.keys())
        allowed = BLANK_NODE_REQUIRED_PROPS | BLANK_NODE_OPTIONAL_PROPS
        extra = props - allowed
        if extra:
            error_msg = f"blank_node: extra properties: {', '.join(sorted(extra))}"
            result.frontmatter_prop_violations.append((str(rel_path), error_msg))
            if verbose:
                print(f"  📋 {rel_path}: {error_msg}")

    # Check namespace has required properties (metadata and !) and optional (uri)
    if metadata == 'namespace':
        props = set(data.keys())
        allowed = NAMESPACE_REQUIRED_PROPS | NAMESPACE_OPTIONAL_PROPS
        missing = NAMESPACE_REQUIRED_PROPS - props
        extra = props - allowed
        errors = []
        if missing:
            errors.append(f"missing: {', '.join(sorted(missing))}")
        if extra:
            errors.append(f"extra: {', '.join(sorted(extra))}")
        if errors:
            error_msg = f"namespace: {'; '.join(errors)}"
            result.frontmatter_prop_violations.append((str(rel_path), error_msg))
            if verbose:
                print(f"  📋 {rel_path}: {error_msg}")

    # Check naming convention
    if metadata:
        valid, error = check_naming_convention(filepath, metadata)
        if not valid:
            result.naming_violations.append((str(rel_path), error))
            if verbose:
                print(f"  📛 {rel_path}: {error}")

    # Check for body content (only frontmatter allowed, except for index files)
    if metadata != 'index' and has_body_content(filepath):
        result.has_body_violations.append(str(rel_path))
        if verbose:
            print(f"  📄 {rel_path}: has body content (only frontmatter allowed)")


def find_orphaned_anchors(repo_root: Path, all_anchors: Set[str], all_blank_nodes: Set[str], all_namespaces: Set[str], verbose: bool = False) -> List[str]:
    """Find anchors that are not referenced in any statement.

    Excludes:
    - Namespace files (expected to not be referenced)
    - Blank nodes (handled separately by find_blank_node_issues)
    """
    referenced = set()

    # Collect all wikilinks from statements
    for ns in PREFIXES:
        ns_dir = repo_root / ns
        if not ns_dir.exists():
            continue

        for filepath in ns_dir.glob('*.md'):
            data, _ = parse_frontmatter(filepath)
            if data and data.get('metadata') == 'statement':
                referenced.update(extract_wikilinks(data))

    # Find anchors not in referenced set
    orphaned = []
    for anchor in all_anchors:
        if anchor not in referenced:
            # Namespace files are expected to not be referenced (or only in imports)
            if anchor.startswith('!'):
                continue
            # UUID-named namespace files are also excluded
            if anchor in all_namespaces:
                continue
            # UUID blank nodes are handled separately
            if anchor in all_blank_nodes:
                continue
            orphaned.append(anchor)

    return sorted(orphaned)


def get_all_namespace_files(repo_root: Path) -> Set[str]:
    """Get all namespace file names (files with metadata: namespace)."""
    namespaces = set()

    for ns in PREFIXES:
        ns_dir = repo_root / ns
        if not ns_dir.exists():
            continue

        for filepath in ns_dir.glob('*.md'):
            data, error = parse_frontmatter(filepath)
            if data and data.get('metadata') == 'namespace':
                namespaces.add(filepath.stem)

    return namespaces


def get_all_blank_nodes(repo_root: Path) -> Set[str]:
    """Get all defined blank node names (files with metadata: blank_node)."""
    blank_nodes = set()

    for ns in PREFIXES:
        ns_dir = repo_root / ns
        if not ns_dir.exists():
            continue

        for filepath in ns_dir.glob('*.md'):
            data, error = parse_frontmatter(filepath)
            if data and data.get('metadata') == 'blank_node':
                blank_nodes.add(filepath.stem)

    return blank_nodes


def find_blank_node_issues(repo_root: Path, verbose: bool = False) -> Tuple[List[str], List[Tuple[str, str]]]:
    """
    Find blank node issues:
    1. Orphaned blank nodes - defined but never referenced in any statement wikilinks

    All files must be UUIDv5 format. Blank node references are extracted from wikilinks.

    Returns: (orphaned_blank_nodes, undefined_blank_nodes)
    """
    defined_blank_nodes = get_all_blank_nodes(repo_root)
    referenced_blank_nodes = set()

    for ns in PREFIXES:
        ns_dir = repo_root / ns
        if not ns_dir.exists():
            continue

        for filepath in ns_dir.glob('*.md'):
            data, _ = parse_frontmatter(filepath)
            if data and data.get('metadata') == 'statement':
                # Extract blank node references from wikilinks in frontmatter
                wikilinks = extract_wikilinks(data)
                for link in wikilinks:
                    # Check if this wikilink refers to a defined blank node
                    if link in defined_blank_nodes:
                        referenced_blank_nodes.add(link)

    # Find orphaned blank nodes (defined but never referenced)
    orphaned = []
    for bn in defined_blank_nodes:
        if bn not in referenced_blank_nodes:
            orphaned.append(bn)
            if verbose:
                print(f"  👻 Orphaned blank node: {bn}")

    return sorted(orphaned), []


def validate_all(repo_root: Path, verbose: bool = False, target_namespaces: List[str] = None) -> ValidationResult:
    """Run all validation checks.

    Args:
        repo_root: Path to repository root
        verbose: Print verbose output
        target_namespaces: If provided, only validate these namespaces. Otherwise validate all.
    """
    result = ValidationResult()

    namespaces_to_check = target_namespaces if target_namespaces else PREFIXES

    print("Collecting anchors...")
    # Collect anchors from ALL namespaces (needed for cross-references)
    all_anchors = get_all_anchors(repo_root)
    all_anchors_lower = {a.lower() for a in all_anchors}  # For case-insensitive matching
    print(f"  Found {len(all_anchors)} anchors")

    print("\nValidating files...")
    file_count = 0
    for ns in namespaces_to_check:
        ns_dir = repo_root / ns
        if not ns_dir.exists():
            print(f"  ⚠️  Namespace directory not found: {ns}/")
            continue

        for filepath in ns_dir.glob('*.md'):
            validate_file(filepath, all_anchors, all_anchors_lower, result, verbose)
            file_count += 1

    print(f"  Validated {file_count} files")

    # Get blank nodes and namespaces first (needed for orphaned anchor check)
    all_blank_nodes = get_all_blank_nodes(repo_root)
    all_namespaces = get_all_namespace_files(repo_root)

    print("\nChecking for orphaned anchors...")
    result.orphaned_anchors = find_orphaned_anchors(repo_root, all_anchors, all_blank_nodes, all_namespaces, verbose)
    if result.orphaned_anchors and verbose:
        for anchor in result.orphaned_anchors:
            print(f"  👻 {anchor}")

    print("\nChecking blank nodes...")
    result.orphaned_blank_nodes, result.undefined_blank_nodes = find_blank_node_issues(repo_root, verbose)
    if result.undefined_blank_nodes and verbose:
        for filepath, bn in result.undefined_blank_nodes:
            print(f"  ❌ {filepath}: undefined blank node {bn}")

    return result


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Validate exocortex-public-ontologies')
    parser.add_argument('namespaces', nargs='*', help='Specific namespaces to validate (default: all)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    args = parser.parse_args()

    print("=" * 60)
    print("Exocortex Public Ontologies Validator")
    print("=" * 60)
    print()

    # Determine which namespaces to validate
    target_namespaces = None
    if args.namespaces:
        target_namespaces = args.namespaces
        print(f"Validating namespaces: {', '.join(target_namespaces)}\n")
    else:
        print("Validating all namespaces\n")

    result = validate_all(REPO_ROOT, args.verbose, target_namespaces)

    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    print(result.summary())

    # Show external wikilinks info (not an error)
    if result.external_wikilinks:
        print(f"\nℹ️  External wikilinks: {len(result.external_wikilinks)} references to resources not in this repository")
        print("   (This is normal - these may be defined in other ontologies)")

    if result.has_errors():
        print("\n❌ Validation failed!")

        if result.orphaned_anchors and not args.verbose:
            print(f"\nOrphaned anchors ({len(result.orphaned_anchors)}):")
            for anchor in result.orphaned_anchors[:10]:
                print(f"  - {anchor}")
            if len(result.orphaned_anchors) > 10:
                print(f"  ... and {len(result.orphaned_anchors) - 10} more")

        if result.external_wikilinks and not args.verbose:
            print(f"\nExternal wikilinks - INFO ({len(result.external_wikilinks)}):")
            for filepath, link in result.external_wikilinks[:10]:
                print(f"  - {filepath} → [[{link}]]")
            if len(result.external_wikilinks) > 10:
                print(f"  ... and {len(result.external_wikilinks) - 10} more")

        if result.invalid_frontmatter and not args.verbose:
            print(f"\nInvalid frontmatter ({len(result.invalid_frontmatter)}):")
            for filepath, error in result.invalid_frontmatter[:10]:
                print(f"  - {filepath}: {error}")

        if result.naming_violations and not args.verbose:
            print(f"\nNaming convention violations ({len(result.naming_violations)}):")
            for filepath, error in result.naming_violations[:20]:
                print(f"  - {filepath}: {error}")
            if len(result.naming_violations) > 20:
                print(f"  ... and {len(result.naming_violations) - 20} more")

        if result.frontmatter_prop_violations and not args.verbose:
            print(f"\nFrontmatter property violations ({len(result.frontmatter_prop_violations)}):")
            for filepath, error in result.frontmatter_prop_violations[:20]:
                print(f"  - {filepath}: {error}")
            if len(result.frontmatter_prop_violations) > 20:
                print(f"  ... and {len(result.frontmatter_prop_violations) - 20} more")

        if result.has_body_violations and not args.verbose:
            print(f"\nFiles with body content ({len(result.has_body_violations)}):")
            for filepath in result.has_body_violations[:20]:
                print(f"  - {filepath}")
            if len(result.has_body_violations) > 20:
                print(f"  ... and {len(result.has_body_violations) - 20} more")

        if result.orphaned_blank_nodes and not args.verbose:
            print(f"\nOrphaned blank nodes ({len(result.orphaned_blank_nodes)}):")
            for bn in result.orphaned_blank_nodes[:20]:
                print(f"  - {bn}")
            if len(result.orphaned_blank_nodes) > 20:
                print(f"  ... and {len(result.orphaned_blank_nodes) - 20} more")

        if result.undefined_blank_nodes and not args.verbose:
            print(f"\nUndefined blank nodes ({len(result.undefined_blank_nodes)}):")
            for filepath, bn in result.undefined_blank_nodes[:20]:
                print(f"  - {filepath}: {bn}")
            if len(result.undefined_blank_nodes) > 20:
                print(f"  ... and {len(result.undefined_blank_nodes) - 20} more")

        sys.exit(1)
    else:
        print("\n✅ All validations passed!")
        sys.exit(0)


if __name__ == '__main__':
    main()

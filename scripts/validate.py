#!/usr/bin/env python3
"""
Validation tools for exocortex-public-ontologies.

Checks:
1. Orphaned anchors - anchors not referenced in any statement
2. Broken wikilinks - references to non-existent anchors
3. File format - proper YAML frontmatter structure
4. Metadata consistency - all files have valid metadata property

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
NAMESPACES = ['rdf', 'rdfs', 'owl', 'dc', 'dcterms', 'skos', 'foaf', 'prov', 'time', 'geo', 'vcard']
EXCLUDED_DIRS = ['~templates', 'scripts', '.git']


@dataclass
class ValidationResult:
    """Holds validation results."""
    orphaned_anchors: List[str] = field(default_factory=list)
    broken_wikilinks: List[Tuple[str, str]] = field(default_factory=list)
    invalid_frontmatter: List[Tuple[str, str]] = field(default_factory=list)
    missing_metadata: List[str] = field(default_factory=list)
    invalid_metadata: List[Tuple[str, str]] = field(default_factory=list)
    naming_violations: List[Tuple[str, str]] = field(default_factory=list)

    def has_errors(self) -> bool:
        return any([
            self.orphaned_anchors,
            self.broken_wikilinks,
            self.invalid_frontmatter,
            self.missing_metadata,
            self.invalid_metadata,
            self.naming_violations
        ])

    def summary(self) -> str:
        lines = []
        if self.orphaned_anchors:
            lines.append(f"  Orphaned anchors: {len(self.orphaned_anchors)}")
        if self.broken_wikilinks:
            lines.append(f"  Broken wikilinks: {len(self.broken_wikilinks)}")
        if self.invalid_frontmatter:
            lines.append(f"  Invalid frontmatter: {len(self.invalid_frontmatter)}")
        if self.missing_metadata:
            lines.append(f"  Missing metadata: {len(self.missing_metadata)}")
        if self.invalid_metadata:
            lines.append(f"  Invalid metadata: {len(self.invalid_metadata)}")
        if self.naming_violations:
            lines.append(f"  Naming convention violations: {len(self.naming_violations)}")
        return '\n'.join(lines) if lines else "  All checks passed!"


def check_naming_convention(filepath: Path, metadata: str) -> Tuple[bool, str]:
    """
    Check if filename follows naming convention.

    Naming conventions:
    - Namespace: !{prefix}.md
    - Anchor: {prefix}__{localname}.md
    - Statement: {subject} {predicate} {object}.md
      - subject: {prefix}__{name} or !{prefix}
      - predicate: {prefix}__{name} or 'a' (for rdf:type)
      - object: {prefix}__{name} or !{prefix} or ___ (literal)
    """
    filename = filepath.stem  # without .md
    ns_dir = filepath.parent.name  # namespace directory

    # Valid prefixes (must have __ separator)
    prefixes = NAMESPACES + ['!']

    if metadata == 'namespace':
        # Must be !{prefix}
        if not filename.startswith('!'):
            return False, f"Namespace file must start with '!', got: {filename}"
        return True, ""

    elif metadata == 'anchor':
        # Must be {prefix}__{localname}
        if '__' not in filename:
            return False, f"Anchor must have format {{prefix}}__{{name}}, got: {filename}"
        prefix = filename.split('__')[0]
        if prefix not in NAMESPACES:
            return False, f"Unknown prefix '{prefix}' in anchor: {filename}"
        return True, ""

    elif metadata == 'statement':
        # Must be {subject} {predicate} {object}
        parts = filename.split(' ')
        if len(parts) != 3:
            return False, f"Statement must have 3 space-separated parts, got {len(parts)}: {filename}"

        subject, predicate, obj = parts

        # Validate subject: must be {prefix}__{name} or !{prefix}
        if subject.startswith('!'):
            if subject[1:] not in NAMESPACES:
                return False, f"Unknown namespace in subject: {subject}"
        elif '__' in subject:
            prefix = subject.split('__')[0]
            if prefix not in NAMESPACES:
                return False, f"Unknown prefix in subject: {subject}"
        else:
            return False, f"Subject must have prefix ({{prefix}}__{{name}}), got: {subject}"

        # Validate predicate: must be {prefix}__{name} or 'a'
        if predicate == 'a':
            pass  # OK - shorthand for rdf:type
        elif '__' in predicate:
            prefix = predicate.split('__')[0]
            if prefix not in NAMESPACES:
                return False, f"Unknown prefix in predicate: {predicate}"
        else:
            return False, f"Predicate must have prefix or be 'a', got: {predicate}"

        # Validate object: must be {prefix}__{name} or !{prefix} or ___
        if obj == '___':
            pass  # OK - literal placeholder
        elif obj.startswith('!'):
            if obj[1:] not in NAMESPACES:
                return False, f"Unknown namespace in object: {obj}"
        elif '__' in obj:
            prefix = obj.split('__')[0]
            if prefix not in NAMESPACES:
                return False, f"Unknown prefix in object: {obj}"
        else:
            return False, f"Object must have prefix, be '___', or be namespace, got: {obj}"

        return True, ""

    return True, ""


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
    """Get all anchor names (files with metadata: anchor or namespace)."""
    anchors = set()

    for ns in NAMESPACES:
        ns_dir = repo_root / ns
        if not ns_dir.exists():
            continue

        for filepath in ns_dir.glob('*.md'):
            data, error = parse_frontmatter(filepath)
            if data and data.get('metadata') in ('anchor', 'namespace'):
                # Anchor name is filename without .md
                anchors.add(filepath.stem)

    return anchors


def validate_file(filepath: Path, all_anchors: Set[str], result: ValidationResult, verbose: bool = False):
    """Validate a single file."""
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
    elif metadata not in ('namespace', 'anchor', 'statement'):
        result.invalid_metadata.append((str(rel_path), f"invalid value: {metadata}"))
        if verbose:
            print(f"  ❌ {rel_path}: invalid metadata value '{metadata}'")

    # Check wikilinks in statements
    if metadata == 'statement':
        wikilinks = extract_wikilinks(data)
        for link in wikilinks:
            if link not in all_anchors:
                result.broken_wikilinks.append((str(rel_path), link))
                if verbose:
                    print(f"  🔗 {rel_path}: broken link to [[{link}]]")

    # Check naming convention
    if metadata:
        valid, error = check_naming_convention(filepath, metadata)
        if not valid:
            result.naming_violations.append((str(rel_path), error))
            if verbose:
                print(f"  📛 {rel_path}: {error}")


def find_orphaned_anchors(repo_root: Path, all_anchors: Set[str], verbose: bool = False) -> List[str]:
    """Find anchors that are not referenced in any statement."""
    referenced = set()

    # Collect all wikilinks from statements
    for ns in NAMESPACES:
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
            orphaned.append(anchor)

    return sorted(orphaned)


def validate_all(repo_root: Path, verbose: bool = False) -> ValidationResult:
    """Run all validation checks."""
    result = ValidationResult()

    print("Collecting anchors...")
    all_anchors = get_all_anchors(repo_root)
    print(f"  Found {len(all_anchors)} anchors")

    print("\nValidating files...")
    file_count = 0
    for ns in NAMESPACES:
        ns_dir = repo_root / ns
        if not ns_dir.exists():
            print(f"  ⚠️  Namespace directory not found: {ns}/")
            continue

        for filepath in ns_dir.glob('*.md'):
            validate_file(filepath, all_anchors, result, verbose)
            file_count += 1

    print(f"  Validated {file_count} files")

    print("\nChecking for orphaned anchors...")
    result.orphaned_anchors = find_orphaned_anchors(repo_root, all_anchors, verbose)
    if result.orphaned_anchors and verbose:
        for anchor in result.orphaned_anchors:
            print(f"  👻 {anchor}")

    return result


def main():
    verbose = '--verbose' in sys.argv or '-v' in sys.argv

    print("=" * 60)
    print("Exocortex Public Ontologies Validator")
    print("=" * 60)
    print()

    result = validate_all(REPO_ROOT, verbose)

    print("\n" + "=" * 60)
    print("VALIDATION SUMMARY")
    print("=" * 60)
    print(result.summary())

    if result.has_errors():
        print("\n❌ Validation failed!")

        if result.orphaned_anchors and not verbose:
            print(f"\nOrphaned anchors ({len(result.orphaned_anchors)}):")
            for anchor in result.orphaned_anchors[:10]:
                print(f"  - {anchor}")
            if len(result.orphaned_anchors) > 10:
                print(f"  ... and {len(result.orphaned_anchors) - 10} more")

        if result.broken_wikilinks and not verbose:
            print(f"\nBroken wikilinks ({len(result.broken_wikilinks)}):")
            for filepath, link in result.broken_wikilinks[:10]:
                print(f"  - {filepath} → [[{link}]]")
            if len(result.broken_wikilinks) > 10:
                print(f"  ... and {len(result.broken_wikilinks) - 10} more")

        if result.invalid_frontmatter and not verbose:
            print(f"\nInvalid frontmatter ({len(result.invalid_frontmatter)}):")
            for filepath, error in result.invalid_frontmatter[:10]:
                print(f"  - {filepath}: {error}")

        if result.naming_violations and not verbose:
            print(f"\nNaming convention violations ({len(result.naming_violations)}):")
            for filepath, error in result.naming_violations[:20]:
                print(f"  - {filepath}: {error}")
            if len(result.naming_violations) > 20:
                print(f"  ... and {len(result.naming_violations) - 20} more")

        sys.exit(1)
    else:
        print("\n✅ All validations passed!")
        sys.exit(0)


if __name__ == '__main__':
    main()

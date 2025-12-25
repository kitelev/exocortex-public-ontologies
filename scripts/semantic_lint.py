#!/usr/bin/env python3
"""
Semantic linter for ontologies.

Checks for best practices:
- Labels on classes and properties
- Comments/descriptions on classes and properties
- Domains and ranges on properties
- Consistent naming conventions

Usage:
    python scripts/semantic_lint.py [--namespace foaf] [--output docs/lint-report.md]
"""

import argparse
import re
import yaml
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

from common import get_prefix_dirs, get_repo_root

# Repository root
REPO_ROOT = get_repo_root()

# Namespace prefixes loaded from _prefixes.yaml
PREFIXES = get_prefix_dirs()

# Well-known UUIDs
RDF_TYPE_UUID = "73b69787-81ea-563e-8e09-9c84cad4cf2b"
RDFS_LABEL_UUID = "d0e9e696-d3f2-5966-a62f-d8358cbde741"
RDFS_COMMENT_UUID = "da1b0b28-9c51-55c3-a963-2337006693de"
RDFS_DOMAIN_UUID = "84d654c0-420b-5a08-ad64-1f16d51de0b2"
RDFS_RANGE_UUID = "c6a11966-a018-5be8-95a0-eba182c2fd93"
RDFS_ISDEFINEDBY_UUID = "2e218ab8-518d-5cd0-a660-f575a101e5d8"

# Class type UUIDs
RDFS_CLASS_UUID = "30488677-f427-5947-8a14-02903ca20a7e"
OWL_CLASS_UUID = "581d50c0-7bc2-5a97-bdc2-9c056f43c807"

# Property type UUIDs
PROPERTY_TYPES = {
    "f1afe09a-f371-5a01-a530-be18bfdb4d6b": "rdf:Property",
    "1ca4d39e-3c44-575a-8e82-b745bf274777": "owl:ObjectProperty",
    "73d101aa-9788-5397-ac46-4569ceaae23d": "owl:DatatypeProperty",
    "c4d46947-b828-50f4-871e-f29b15045aa5": "owl:AnnotationProperty",
}


def parse_frontmatter_fast(filepath: Path) -> Optional[dict]:
    """Parse YAML frontmatter from a markdown file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            first_line = f.readline()
            if not first_line.startswith("---"):
                return None

            lines = [first_line]
            for line in f:
                lines.append(line)
                if line.strip() == "---":
                    break

            yaml_content = "".join(lines[1:-1])
            return yaml.safe_load(yaml_content) or {}
    except Exception:
        return None


def extract_wikilink_uuid(value: str) -> Optional[str]:
    """Extract UUID from wikilink."""
    if not value:
        return None
    match = re.match(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", value.strip())
    return match.group(1) if match else None


class LintIssue:
    """Represents a lint issue."""

    def __init__(self, severity: str, category: str, resource: str, message: str):
        self.severity = severity  # "error", "warning", "info"
        self.category = category
        self.resource = resource
        self.message = message


def lint_namespace(repo_root: Path, namespace: str) -> Tuple[Dict, List[LintIssue]]:
    """Lint a single namespace and return statistics and issues."""
    ns_dir = repo_root / namespace
    if not ns_dir.exists():
        return {}, []

    issues = []
    stats = {
        "classes": 0,
        "properties": 0,
        "classes_with_label": 0,
        "classes_with_comment": 0,
        "properties_with_label": 0,
        "properties_with_comment": 0,
        "properties_with_domain": 0,
        "properties_with_range": 0,
    }

    # First pass: identify classes and properties
    classes = set()
    properties = set()
    has_label = set()
    has_comment = set()
    has_domain = set()
    has_range = set()
    has_isdefinedby = set()

    uuid_to_alias = {}

    for filepath in ns_dir.glob("*.md"):
        fm = parse_frontmatter_fast(filepath)
        if not fm:
            continue

        uuid = filepath.stem
        metadata = fm.get("metadata")

        if metadata == "anchor":
            aliases = fm.get("aliases", [])
            if aliases:
                uuid_to_alias[uuid] = aliases[0]

        elif metadata == "statement":
            pred_uuid = extract_wikilink_uuid(fm.get("predicate", ""))
            subj_uuid = extract_wikilink_uuid(fm.get("subject", ""))
            obj_uuid = extract_wikilink_uuid(fm.get("object", ""))

            # Identify classes and properties
            if pred_uuid == RDF_TYPE_UUID:
                if obj_uuid in (RDFS_CLASS_UUID, OWL_CLASS_UUID):
                    classes.add(subj_uuid)
                elif obj_uuid in PROPERTY_TYPES:
                    properties.add(subj_uuid)

            # Track labels
            elif pred_uuid == RDFS_LABEL_UUID:
                has_label.add(subj_uuid)

            # Track comments
            elif pred_uuid == RDFS_COMMENT_UUID:
                has_comment.add(subj_uuid)

            # Track domain
            elif pred_uuid == RDFS_DOMAIN_UUID:
                has_domain.add(subj_uuid)

            # Track range
            elif pred_uuid == RDFS_RANGE_UUID:
                has_range.add(subj_uuid)

            # Track isDefinedBy
            elif pred_uuid == RDFS_ISDEFINEDBY_UUID:
                has_isdefinedby.add(subj_uuid)

    # Calculate statistics
    stats["classes"] = len(classes)
    stats["properties"] = len(properties)
    stats["classes_with_label"] = len(classes & has_label)
    stats["classes_with_comment"] = len(classes & has_comment)
    stats["properties_with_label"] = len(properties & has_label)
    stats["properties_with_comment"] = len(properties & has_comment)
    stats["properties_with_domain"] = len(properties & has_domain)
    stats["properties_with_range"] = len(properties & has_range)

    # Generate issues
    def get_alias(uuid):
        return uuid_to_alias.get(uuid, uuid[:8])

    # Classes without labels
    for cls in classes - has_label:
        issues.append(LintIssue("warning", "missing-label", get_alias(cls), f"Class missing rdfs:label"))

    # Classes without comments
    for cls in classes - has_comment:
        issues.append(LintIssue("info", "missing-comment", get_alias(cls), f"Class missing rdfs:comment"))

    # Properties without labels
    for prop in properties - has_label:
        issues.append(LintIssue("warning", "missing-label", get_alias(prop), f"Property missing rdfs:label"))

    # Properties without comments
    for prop in properties - has_comment:
        issues.append(LintIssue("info", "missing-comment", get_alias(prop), f"Property missing rdfs:comment"))

    # Properties without domain
    for prop in properties - has_domain:
        issues.append(LintIssue("info", "missing-domain", get_alias(prop), f"Property missing rdfs:domain"))

    # Properties without range
    for prop in properties - has_range:
        issues.append(LintIssue("info", "missing-range", get_alias(prop), f"Property missing rdfs:range"))

    return stats, issues


def generate_report(
    all_stats: Dict[str, Dict], all_issues: Dict[str, List[LintIssue]], namespace_filter: Optional[str] = None
) -> str:
    """Generate markdown lint report."""
    lines = []

    if namespace_filter:
        lines.append(f"# Semantic Lint Report: {namespace_filter}")
    else:
        lines.append("# Semantic Lint Report")

    lines.append("")
    lines.append("Quality assessment of ontology definitions.")
    lines.append("")
    lines.append("*Generated automatically.*")
    lines.append("")

    # Summary
    lines.append("## Summary")
    lines.append("")

    total_classes = sum(s["classes"] for s in all_stats.values())
    total_props = sum(s["properties"] for s in all_stats.values())
    total_cls_label = sum(s["classes_with_label"] for s in all_stats.values())
    total_cls_comment = sum(s["classes_with_comment"] for s in all_stats.values())
    total_prop_label = sum(s["properties_with_label"] for s in all_stats.values())
    total_prop_comment = sum(s["properties_with_comment"] for s in all_stats.values())
    total_prop_domain = sum(s["properties_with_domain"] for s in all_stats.values())
    total_prop_range = sum(s["properties_with_range"] for s in all_stats.values())

    lines.append("| Metric | Count | Percentage |")
    lines.append("|--------|-------|------------|")
    lines.append(f"| Total Classes | {total_classes} | - |")
    if total_classes > 0:
        lines.append(f"| Classes with label | {total_cls_label} | {100*total_cls_label/total_classes:.1f}% |")
        lines.append(f"| Classes with comment | {total_cls_comment} | {100*total_cls_comment/total_classes:.1f}% |")
    lines.append(f"| Total Properties | {total_props} | - |")
    if total_props > 0:
        lines.append(f"| Properties with label | {total_prop_label} | {100*total_prop_label/total_props:.1f}% |")
        lines.append(f"| Properties with comment | {total_prop_comment} | {100*total_prop_comment/total_props:.1f}% |")
        lines.append(f"| Properties with domain | {total_prop_domain} | {100*total_prop_domain/total_props:.1f}% |")
        lines.append(f"| Properties with range | {total_prop_range} | {100*total_prop_range/total_props:.1f}% |")

    lines.append("")

    # Per-namespace breakdown
    lines.append("## By Namespace")
    lines.append("")
    lines.append("| Namespace | Classes | Props | Labels | Comments | Domain | Range |")
    lines.append("|-----------|---------|-------|--------|----------|--------|-------|")

    for ns in sorted(all_stats.keys()):
        s = all_stats[ns]
        if s["classes"] == 0 and s["properties"] == 0:
            continue

        cls_label_pct = f"{100*s['classes_with_label']/s['classes']:.0f}%" if s["classes"] > 0 else "-"
        cls_comment_pct = f"{100*s['classes_with_comment']/s['classes']:.0f}%" if s["classes"] > 0 else "-"
        prop_domain_pct = f"{100*s['properties_with_domain']/s['properties']:.0f}%" if s["properties"] > 0 else "-"
        prop_range_pct = f"{100*s['properties_with_range']/s['properties']:.0f}%" if s["properties"] > 0 else "-"

        lines.append(
            f"| {ns} | {s['classes']} | {s['properties']} | {cls_label_pct} | {cls_comment_pct} | {prop_domain_pct} | {prop_range_pct} |"
        )

    lines.append("")

    # Issue counts
    issue_counts = defaultdict(int)
    for ns_issues in all_issues.values():
        for issue in ns_issues:
            issue_counts[f"{issue.severity}:{issue.category}"] += 1

    lines.append("## Issue Counts")
    lines.append("")
    lines.append("| Severity | Category | Count |")
    lines.append("|----------|----------|-------|")
    for key in sorted(issue_counts.keys()):
        severity, category = key.split(":")
        icon = "⚠️" if severity == "warning" else "ℹ️"
        lines.append(f"| {icon} {severity} | {category} | {issue_counts[key]} |")

    lines.append("")

    # Detailed issues by namespace (only warnings)
    lines.append("## Warnings by Namespace")
    lines.append("")

    for ns in sorted(all_issues.keys()):
        warnings = [i for i in all_issues[ns] if i.severity == "warning"]
        if not warnings:
            continue

        lines.append(f"### {ns}")
        lines.append("")
        for issue in warnings[:20]:  # Limit to 20 per namespace
            lines.append(f"- ⚠️ `{issue.resource}`: {issue.message}")
        if len(warnings) > 20:
            lines.append(f"- ... and {len(warnings) - 20} more warnings")
        lines.append("")

    # Quality grade
    lines.append("## Quality Grade")
    lines.append("")

    total_resources = total_classes + total_props
    if total_resources > 0:
        label_coverage = (total_cls_label + total_prop_label) / total_resources
        comment_coverage = (total_cls_comment + total_prop_comment) / total_resources

        if label_coverage >= 0.9 and comment_coverage >= 0.8:
            grade = "A"
            desc = "Excellent - well documented"
        elif label_coverage >= 0.8 and comment_coverage >= 0.6:
            grade = "B"
            desc = "Good - mostly documented"
        elif label_coverage >= 0.6:
            grade = "C"
            desc = "Fair - labels present, comments lacking"
        else:
            grade = "D"
            desc = "Needs improvement"

        lines.append(f"**Overall Grade: {grade}** - {desc}")
        lines.append("")
        lines.append(f"- Label coverage: {100*label_coverage:.1f}%")
        lines.append(f"- Comment coverage: {100*comment_coverage:.1f}%")

    lines.append("")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Semantic linter for ontologies")
    parser.add_argument("-o", "--output", type=str, default="docs/lint-report.md", help="Output file path")
    parser.add_argument("-n", "--namespace", type=str, default=None, help="Lint specific namespace only")
    parser.add_argument("-v", "--verbose", action="store_true", help="Verbose output")
    args = parser.parse_args()

    namespaces = [args.namespace] if args.namespace else PREFIXES

    all_stats = {}
    all_issues = {}

    for ns in namespaces:
        print(f"Linting {ns}...")
        stats, issues = lint_namespace(REPO_ROOT, ns)
        if stats:
            all_stats[ns] = stats
            all_issues[ns] = issues
            print(f"  Classes: {stats['classes']}, Properties: {stats['properties']}")
            warnings = len([i for i in issues if i.severity == "warning"])
            if warnings > 0:
                print(f"  Warnings: {warnings}")

    print("\nGenerating report...")
    report = generate_report(all_stats, all_issues, args.namespace)

    output_path = REPO_ROOT / args.output
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(report, encoding="utf-8")
    print(f"Written to {args.output}")


if __name__ == "__main__":
    main()

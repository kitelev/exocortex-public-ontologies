#!/usr/bin/env python3
"""
Export ontology documentation to PDF and EPUB formats.

Requires:
    pip install weasyprint ebooklib

Usage:
    python scripts/export_docs.py [--format pdf|epub|all] [--namespace PREFIX]

Output:
    docs/exports/ontologies.pdf
    docs/exports/ontologies.epub
    docs/exports/{prefix}.pdf (per namespace)
"""

import argparse
import sys
from pathlib import Path
from html import escape
from datetime import datetime

# Add scripts to path
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from common import load_prefixes, get_prefix_dirs, parse_frontmatter_from_file, extract_wikilink_uuid

# Check dependencies
def check_dependencies(format_type: str = 'all'):
    """Check if required packages are installed."""
    available = {'pdf': False, 'epub': False}

    try:
        import weasyprint
        available['pdf'] = True
    except (ImportError, OSError) as e:
        if format_type in ('pdf', 'all'):
            print(f"⚠️  PDF export unavailable: {type(e).__name__}")
            print("   For PDF support, install system libraries:")
            print("   macOS: brew install pango glib cairo")
            print("   Then: pip install weasyprint")

    try:
        import ebooklib
        available['epub'] = True
    except ImportError:
        if format_type in ('epub', 'all'):
            print("⚠️  EPUB export unavailable")
            print("   Install: pip install ebooklib")

    if format_type == 'pdf' and not available['pdf']:
        return False
    if format_type == 'epub' and not available['epub']:
        return False
    if format_type == 'all' and not any(available.values()):
        print("No export formats available. Install dependencies first.")
        return False

    return available


# Relationship predicates UUIDs
PREDICATES = {
    "d55dc3fe-9a9f-5908-baae-e67d0fa0eab0": ("subClassOf", "rdfs:subClassOf"),
    "4b368645-5f7a-551b-940f-acebfe3d0bd2": ("subPropertyOf", "rdfs:subPropertyOf"),
    "84d654c0-420b-5a08-ad64-1f16d51de0b2": ("domain", "rdfs:domain"),
    "c6a11966-a018-5be8-95a0-eba182c2fd93": ("range", "rdfs:range"),
    "73b69787-81ea-563e-8e09-9c84cad4cf2b": ("type", "rdf:type"),
    "d0e9e696-d3f2-5966-a62f-d8358cbde741": ("label", "rdfs:label"),
    "da1b0b28-9c51-55c3-a963-2337006693de": ("comment", "rdfs:comment"),
    "2e218ab8-518d-5cd0-a660-f575a101e5d8": ("isDefinedBy", "rdfs:isDefinedBy"),
}


# PDF/Print-optimized CSS
PDF_CSS = """
@page {
    size: A4;
    margin: 2cm;
    @bottom-center {
        content: counter(page);
    }
}
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
    font-size: 11pt;
    line-height: 1.5;
    color: #1a1a1a;
}
h1 { font-size: 24pt; color: #0366d6; page-break-after: avoid; margin-top: 1.5cm; }
h2 { font-size: 18pt; color: #24292e; page-break-after: avoid; margin-top: 1cm; border-bottom: 1px solid #e1e4e8; }
h3 { font-size: 14pt; color: #24292e; page-break-after: avoid; }
.namespace-section { page-break-before: always; }
.resource { margin-bottom: 1.5em; page-break-inside: avoid; }
.resource-header { display: flex; align-items: baseline; gap: 0.5em; }
.badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 9pt;
    font-weight: 600;
}
.badge-class { background: #ddf4ff; color: #0969da; }
.badge-property { background: #dafbe1; color: #1a7f37; }
.badge-datatype { background: #ffebe9; color: #cf222e; }
.uri { color: #57606a; font-family: monospace; font-size: 9pt; word-break: break-all; }
.description { background: #f6f8fa; padding: 12px; border-radius: 6px; margin: 8px 0; font-style: italic; }
table { width: 100%; border-collapse: collapse; margin: 12px 0; font-size: 10pt; }
th, td { text-align: left; padding: 6px 8px; border: 1px solid #d0d7de; }
th { background: #f6f8fa; font-weight: 600; }
.toc { page-break-after: always; }
.toc ul { list-style: none; padding-left: 0; }
.toc li { padding: 4px 0; }
.toc a { color: #0366d6; text-decoration: none; }
a { color: #0366d6; text-decoration: none; }
code { background: #f6f8fa; padding: 2px 6px; border-radius: 4px; font-family: monospace; font-size: 10pt; }
.cover { text-align: center; page-break-after: always; padding-top: 30%; }
.cover h1 { font-size: 36pt; margin-bottom: 0.5em; }
.cover .subtitle { font-size: 18pt; color: #57606a; }
.cover .date { margin-top: 2em; color: #57606a; }
.stats { display: flex; gap: 2em; margin: 1em 0; }
.stat { text-align: center; }
.stat-value { font-size: 24pt; font-weight: 600; color: #0366d6; }
.stat-label { font-size: 10pt; color: #57606a; }
"""


def load_resources(repo_root: Path, prefixes: list) -> dict:
    """Load all resources with their properties."""
    resources = {}
    statements = []

    for prefix in prefixes:
        prefix_dir = repo_root / prefix
        if not prefix_dir.exists():
            continue

        for filepath in prefix_dir.glob("*.md"):
            fm = parse_frontmatter_from_file(filepath)
            if not fm:
                continue

            metadata = fm.get("metadata")
            uuid = filepath.stem

            if metadata in ("anchor", "namespace"):
                aliases = fm.get("aliases", [])
                alias = aliases[0] if isinstance(aliases, list) and aliases else str(aliases)
                if isinstance(alias, str):
                    alias = alias.strip('"')

                resources[uuid] = {
                    "alias": alias,
                    "uri": fm.get("uri", ""),
                    "prefix": prefix,
                    "type": metadata,
                    "properties": {},
                }

            elif metadata == "statement":
                subject = fm.get("subject", "")
                predicate = fm.get("predicate", "")
                obj = fm.get("object", "")

                subj_uuid = extract_wikilink_uuid(subject)
                pred_uuid = extract_wikilink_uuid(predicate)
                obj_uuid = extract_wikilink_uuid(obj)

                if subj_uuid and pred_uuid:
                    statements.append((subj_uuid, pred_uuid, obj_uuid or obj))

    # Process statements
    for subj_uuid, pred_uuid, obj_value in statements:
        if subj_uuid not in resources:
            continue

        pred_info = PREDICATES.get(pred_uuid, (pred_uuid[:8], pred_uuid[:8]))
        pred_name, pred_label = pred_info

        if obj_value in resources:
            obj_display = resources[obj_value]["alias"]
        else:
            obj_display = str(obj_value).strip('"').split("@")[0].split("^^")[0]

        if pred_name not in resources[subj_uuid]["properties"]:
            resources[subj_uuid]["properties"][pred_name] = []

        resources[subj_uuid]["properties"][pred_name].append({
            "value": obj_display,
            "predicate": pred_label,
        })

    return resources


def get_resource_type(resource: dict) -> str:
    """Determine if resource is class, property, or datatype."""
    alias = resource["alias"].lower()
    props = resource["properties"]

    if "type" in props:
        types = [p["value"].lower() for p in props["type"]]
        if any("class" in t for t in types):
            return "class"
        if any("property" in t for t in types):
            return "property"
        if any("datatype" in t for t in types):
            return "datatype"

    if "class" in alias or alias[0].isupper():
        return "class"
    return "property"


def generate_pdf_html(resources: dict, prefixes: list, single_prefix: str = None) -> str:
    """Generate HTML optimized for PDF export."""

    if single_prefix:
        filtered_prefixes = [single_prefix]
        title = f"{single_prefix.upper()} Ontology"
    else:
        filtered_prefixes = [p for p in prefixes if any(r["prefix"] == p for r in resources.values())]
        title = "Exocortex Public Ontologies"

    # Calculate stats
    all_resources = [r for r in resources.values() if r["prefix"] in filtered_prefixes]
    total_classes = len([r for r in all_resources if get_resource_type(r) == "class"])
    total_props = len([r for r in all_resources if get_resource_type(r) == "property"])
    total_datatypes = len([r for r in all_resources if get_resource_type(r) == "datatype"])

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <style>{PDF_CSS}</style>
</head>
<body>

<div class="cover">
    <h1>{title}</h1>
    <div class="subtitle">RDF Ontology Documentation</div>
    <div class="stats">
        <div class="stat"><div class="stat-value">{len(filtered_prefixes)}</div><div class="stat-label">Namespaces</div></div>
        <div class="stat"><div class="stat-value">{total_classes}</div><div class="stat-label">Classes</div></div>
        <div class="stat"><div class="stat-value">{total_props}</div><div class="stat-label">Properties</div></div>
    </div>
    <div class="date">Generated: {datetime.now().strftime('%Y-%m-%d')}</div>
</div>

<div class="toc">
    <h1>Table of Contents</h1>
    <ul>
"""

    # TOC
    for prefix in sorted(filtered_prefixes):
        ns_resources = [r for r in resources.values() if r["prefix"] == prefix]
        if not ns_resources:
            continue
        html += f'<li><a href="#ns-{prefix}">{prefix.upper()}</a> ({len(ns_resources)} resources)</li>\n'

    html += "</ul>\n</div>\n"

    # Content sections
    for prefix in sorted(filtered_prefixes):
        ns_resources = [r for r in resources.values() if r["prefix"] == prefix]
        if not ns_resources:
            continue

        classes = [r for r in ns_resources if get_resource_type(r) == "class"]
        properties = [r for r in ns_resources if get_resource_type(r) == "property"]
        datatypes = [r for r in ns_resources if get_resource_type(r) == "datatype"]

        html += f"""
<div class="namespace-section" id="ns-{prefix}">
    <h1>{prefix.upper()} Ontology</h1>
    <p>{len(ns_resources)} resources: {len(classes)} classes, {len(properties)} properties, {len(datatypes)} datatypes</p>
"""

        for section_name, items, badge_class in [
            ("Classes", classes, "badge-class"),
            ("Properties", properties, "badge-property"),
            ("Datatypes", datatypes, "badge-datatype"),
        ]:
            if not items:
                continue

            html += f"<h2>{section_name} ({len(items)})</h2>\n"

            for r in sorted(items, key=lambda x: x["alias"]):
                local = r["alias"].split(":")[-1]
                label = r["properties"].get("label", [{"value": local}])[0]["value"]
                comment = r["properties"].get("comment", [{"value": ""}])[0]["value"]
                uri = r["uri"]

                html += f"""
<div class="resource">
    <div class="resource-header">
        <span class="badge {badge_class}">{section_name[:-1]}</span>
        <strong>{escape(label)}</strong>
    </div>
    <div class="uri">{escape(uri)}</div>
"""
                if comment:
                    html += f'<div class="description">{escape(comment)}</div>\n'

                # Properties table
                other_props = {k: v for k, v in r["properties"].items() if k not in ("label", "comment")}
                if other_props:
                    html += "<table><tr><th>Property</th><th>Value</th></tr>\n"
                    for pred_name, values in sorted(other_props.items()):
                        for v in values:
                            html += f'<tr><td><code>{v["predicate"]}</code></td><td>{escape(v["value"])}</td></tr>\n'
                    html += "</table>\n"

                html += "</div>\n"

        html += "</div>\n"

    html += "</body></html>"
    return html


def generate_epub(resources: dict, prefixes: list, output_path: Path):
    """Generate EPUB ebook."""
    from ebooklib import epub

    book = epub.EpubBook()
    book.set_identifier('exocortex-ontologies')
    book.set_title('Exocortex Public Ontologies')
    book.set_language('en')
    book.add_author('Exocortex Project')

    # CSS
    css = epub.EpubItem(
        uid="style",
        file_name="style/main.css",
        media_type="text/css",
        content=PDF_CSS.encode('utf-8')
    )
    book.add_item(css)

    chapters = []

    # Intro chapter
    intro = epub.EpubHtml(title='Introduction', file_name='intro.xhtml', lang='en')
    intro.content = f"""
    <html><body>
    <h1>Exocortex Public Ontologies</h1>
    <p>This ebook contains documentation for RDF ontologies in the Exocortex knowledge management ecosystem.</p>
    <p>Generated: {datetime.now().strftime('%Y-%m-%d')}</p>
    </body></html>
    """
    intro.add_item(css)
    book.add_item(intro)
    chapters.append(intro)

    # Namespace chapters
    filtered_prefixes = [p for p in prefixes if any(r["prefix"] == p for r in resources.values())]

    for prefix in sorted(filtered_prefixes):
        ns_resources = [r for r in resources.values() if r["prefix"] == prefix]
        if not ns_resources:
            continue

        classes = [r for r in ns_resources if get_resource_type(r) == "class"]
        properties = [r for r in ns_resources if get_resource_type(r) == "property"]

        content = f"<h1>{prefix.upper()} Ontology</h1>\n"
        content += f"<p>{len(ns_resources)} resources</p>\n"

        for section_name, items in [("Classes", classes), ("Properties", properties)]:
            if not items:
                continue
            content += f"<h2>{section_name}</h2>\n<ul>\n"
            for r in sorted(items, key=lambda x: x["alias"])[:50]:  # Limit for EPUB size
                local = r["alias"].split(":")[-1]
                label = r["properties"].get("label", [{"value": local}])[0]["value"]
                content += f"<li><strong>{escape(label)}</strong></li>\n"
            content += "</ul>\n"

        chapter = epub.EpubHtml(title=f'{prefix.upper()}', file_name=f'{prefix}.xhtml', lang='en')
        chapter.content = f"<html><body>{content}</body></html>"
        chapter.add_item(css)
        book.add_item(chapter)
        chapters.append(chapter)

    # Define TOC and spine
    book.toc = [(epub.Section('Ontologies'), chapters)]
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ['nav'] + chapters

    epub.write_epub(str(output_path), book, {})


def export_pdf(html_content: str, output_path: Path):
    """Export HTML to PDF using WeasyPrint."""
    from weasyprint import HTML, CSS

    HTML(string=html_content).write_pdf(
        str(output_path),
        stylesheets=[CSS(string=PDF_CSS)]
    )


def main():
    parser = argparse.ArgumentParser(description='Export ontology documentation to PDF/EPUB')
    parser.add_argument('--format', choices=['pdf', 'epub', 'all'], default='all',
                        help='Output format (default: all)')
    parser.add_argument('--namespace', '-n', type=str, default=None,
                        help='Export single namespace only')
    args = parser.parse_args()

    available = check_dependencies(args.format)
    if not available:
        sys.exit(1)

    repo_root = SCRIPT_DIR.parent
    output_dir = repo_root / "docs" / "exports"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("Ontology Documentation Exporter")
    print("=" * 60)

    prefix_dirs = get_prefix_dirs(repo_root)
    print(f"Loading resources from {len(prefix_dirs)} namespaces...")

    resources = load_resources(repo_root, prefix_dirs)
    print(f"  Found {len(resources)} resources")

    exported = []

    if args.format in ('pdf', 'all') and available.get('pdf'):
        if args.namespace:
            output_file = output_dir / f"{args.namespace}.pdf"
            print(f"Generating PDF for {args.namespace}...")
        else:
            output_file = output_dir / "ontologies.pdf"
            print("Generating PDF...")

        html = generate_pdf_html(resources, prefix_dirs, args.namespace)
        export_pdf(html, output_file)
        print(f"  ✅ {output_file}")
        exported.append(output_file)

    if args.format in ('epub', 'all') and available.get('epub') and not args.namespace:
        output_file = output_dir / "ontologies.epub"
        print("Generating EPUB...")
        generate_epub(resources, prefix_dirs, output_file)
        print(f"  ✅ {output_file}")
        exported.append(output_file)

    if exported:
        print(f"\n✅ Export complete! Files in {output_dir}")
    else:
        print("\n⚠️  No files exported. Check dependencies above.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Generate HTML documentation for ontologies in W3C spec style.

Creates:
- docs/ontology/index.html - Main index with all namespaces
- docs/ontology/{prefix}/index.html - Namespace page with all resources
- docs/ontology/{prefix}/{localname}.html - Individual resource pages

Output: docs/ontology/
"""

import json
import sys
from pathlib import Path
from collections import defaultdict
from html import escape

# Add scripts to path
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))

from common import load_prefixes, get_prefix_dirs, parse_frontmatter_from_file, extract_wikilink_uuid

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

# HTML template
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        :root {{
            --bg: #0d1117;
            --fg: #c9d1d9;
            --link: #58a6ff;
            --border: #30363d;
            --header-bg: #161b22;
            --code-bg: #21262d;
        }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg);
            color: var(--fg);
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            line-height: 1.6;
        }}
        a {{ color: var(--link); text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        h1, h2, h3 {{ color: #fff; }}
        h1 {{ border-bottom: 1px solid var(--border); padding-bottom: 10px; }}
        .uri {{ color: #8b949e; font-family: monospace; font-size: 14px; }}
        .property-table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
        .property-table th, .property-table td {{
            text-align: left;
            padding: 8px 12px;
            border-bottom: 1px solid var(--border);
        }}
        .property-table th {{ background: var(--header-bg); }}
        .badge {{
            display: inline-block;
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 12px;
            margin-right: 4px;
        }}
        .badge-class {{ background: #388bfd33; color: #388bfd; }}
        .badge-property {{ background: #56d36433; color: #56d364; }}
        .badge-datatype {{ background: #f7816633; color: #f78166; }}
        .breadcrumb {{ color: #8b949e; margin-bottom: 20px; }}
        .resource-list {{ list-style: none; padding: 0; }}
        .resource-list li {{ padding: 8px 0; border-bottom: 1px solid var(--border); }}
        .description {{ background: var(--code-bg); padding: 16px; border-radius: 6px; margin: 16px 0; }}
        code {{ background: var(--code-bg); padding: 2px 6px; border-radius: 4px; font-family: monospace; }}
        .nav {{ display: flex; gap: 20px; margin-bottom: 30px; }}
        .nav a {{ padding: 8px 16px; background: var(--header-bg); border-radius: 6px; }}
    </style>
</head>
<body>
{content}
</body>
</html>
"""


def load_resources(repo_root: Path, prefixes: list) -> dict:
    """Load all resources with their properties."""
    resources = {}  # uuid -> {alias, uri, prefix, type, properties}
    statements = []  # list of (subject_uuid, predicate_uuid, object_value)

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
                    "properties": defaultdict(list),
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

    # Process statements to add properties to resources
    for subj_uuid, pred_uuid, obj_value in statements:
        if subj_uuid not in resources:
            continue

        pred_info = PREDICATES.get(pred_uuid, (pred_uuid[:8], pred_uuid[:8]))
        pred_name, pred_label = pred_info

        # Resolve object if it's a UUID reference
        if obj_value in resources:
            obj_display = resources[obj_value]["alias"]
            obj_link = f"../{resources[obj_value]['prefix']}/{obj_display.split(':')[-1]}.html"
        else:
            # Literal value - clean up quotes and language tags
            obj_display = str(obj_value).strip('"').split("@")[0].split("^^")[0]
            obj_link = None

        resources[subj_uuid]["properties"][pred_name].append({
            "value": obj_display,
            "link": obj_link,
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


def generate_resource_page(resource: dict, resources: dict) -> str:
    """Generate HTML page for a single resource."""
    alias = resource["alias"]
    prefix = resource["prefix"]
    uri = resource["uri"]
    rtype = get_resource_type(resource)
    props = resource["properties"]

    badge_class = f"badge-{rtype}"
    type_label = rtype.capitalize()

    # Get label and comment
    label = props.get("label", [{"value": alias.split(":")[-1]}])[0]["value"]
    comment = props.get("comment", [{"value": ""}])[0]["value"]

    # Build properties table
    prop_rows = ""
    for pred_name, values in sorted(props.items()):
        if pred_name in ("label", "comment"):
            continue
        for v in values:
            value_html = f'<a href="{v["link"]}">{escape(v["value"])}</a>' if v["link"] else escape(v["value"])
            prop_rows += f'<tr><td><code>{v["predicate"]}</code></td><td>{value_html}</td></tr>'

    content = f"""
    <div class="breadcrumb">
        <a href="../index.html">Ontologies</a> / <a href="index.html">{prefix}</a> / {alias.split(":")[-1]}
    </div>
    <h1><span class="badge {badge_class}">{type_label}</span> {escape(label)}</h1>
    <div class="uri">{escape(uri)}</div>

    {"<div class='description'>" + escape(comment) + "</div>" if comment else ""}

    <h2>Properties</h2>
    <table class="property-table">
        <tr><th>Predicate</th><th>Value</th></tr>
        {prop_rows if prop_rows else "<tr><td colspan='2'>No properties defined</td></tr>"}
    </table>
    """

    return HTML_TEMPLATE.format(title=f"{alias} - Ontology Documentation", content=content)


def generate_namespace_page(prefix: str, resources: dict) -> str:
    """Generate HTML page for a namespace."""
    ns_resources = [r for r in resources.values() if r["prefix"] == prefix]

    # Group by type
    classes = [r for r in ns_resources if get_resource_type(r) == "class"]
    properties = [r for r in ns_resources if get_resource_type(r) == "property"]
    datatypes = [r for r in ns_resources if get_resource_type(r) == "datatype"]

    def resource_list(items, badge_class):
        if not items:
            return "<p>None</p>"
        html = "<ul class='resource-list'>"
        for r in sorted(items, key=lambda x: x["alias"]):
            local = r["alias"].split(":")[-1]
            label = r["properties"].get("label", [{"value": local}])[0]["value"]
            html += f'<li><a href="{local}.html"><span class="badge {badge_class}">{local}</span></a> {escape(label)}</li>'
        html += "</ul>"
        return html

    content = f"""
    <div class="breadcrumb">
        <a href="../index.html">Ontologies</a> / {prefix}
    </div>
    <h1>{prefix.upper()} Ontology</h1>
    <p>{len(ns_resources)} resources defined</p>

    <h2>Classes ({len(classes)})</h2>
    {resource_list(classes, "badge-class")}

    <h2>Properties ({len(properties)})</h2>
    {resource_list(properties, "badge-property")}

    <h2>Datatypes ({len(datatypes)})</h2>
    {resource_list(datatypes, "badge-datatype")}
    """

    return HTML_TEMPLATE.format(title=f"{prefix.upper()} - Ontology Documentation", content=content)


def generate_index_page(prefixes: list, resources: dict) -> str:
    """Generate main index page."""
    ns_list = ""
    for prefix in sorted(prefixes):
        ns_resources = [r for r in resources.values() if r["prefix"] == prefix]
        if not ns_resources:
            continue
        classes = len([r for r in ns_resources if get_resource_type(r) == "class"])
        props = len([r for r in ns_resources if get_resource_type(r) == "property"])
        ns_list += f'<li><a href="{prefix}/index.html"><strong>{prefix}</strong></a> - {classes} classes, {props} properties</li>'

    content = f"""
    <h1>Exocortex Public Ontologies</h1>
    <p>Documentation for RDF ontologies in the Exocortex knowledge management ecosystem.</p>

    <div class="nav">
        <a href="../browser.html">Visual Browser</a>
        <a href="https://github.com/kitelev/exocortex-public-ontologies">GitHub</a>
    </div>

    <h2>Available Ontologies</h2>
    <ul class="resource-list">
        {ns_list}
    </ul>
    """

    return HTML_TEMPLATE.format(title="Exocortex Public Ontologies", content=content)


def main():
    repo_root = SCRIPT_DIR.parent
    output_dir = repo_root / "docs" / "ontology"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("Ontology Documentation Generator")
    print("=" * 60)

    prefix_dirs = get_prefix_dirs(repo_root)
    print(f"Loading resources from {len(prefix_dirs)} namespaces...")

    resources = load_resources(repo_root, prefix_dirs)
    print(f"  Found {len(resources)} resources")

    # Generate main index
    print("Generating index page...")
    with open(output_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(generate_index_page(prefix_dirs, resources))

    # Generate namespace pages
    for prefix in prefix_dirs:
        ns_resources = [r for r in resources.values() if r["prefix"] == prefix]
        if not ns_resources:
            continue

        ns_dir = output_dir / prefix
        ns_dir.mkdir(exist_ok=True)

        print(f"  {prefix}: {len(ns_resources)} resources")

        # Namespace index
        with open(ns_dir / "index.html", "w", encoding="utf-8") as f:
            f.write(generate_namespace_page(prefix, resources))

        # Individual resource pages
        for r in ns_resources:
            local = r["alias"].split(":")[-1]
            # Sanitize filename
            safe_local = "".join(c if c.isalnum() or c in "-_" else "_" for c in local)
            with open(ns_dir / f"{safe_local}.html", "w", encoding="utf-8") as f:
                f.write(generate_resource_page(r, resources))

    print(f"\n✅ Generated documentation in {output_dir}")
    print(f"   Open {output_dir}/index.html to browse")


if __name__ == "__main__":
    main()

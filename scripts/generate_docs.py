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

# Predicates to show in relationship graph (important semantic relationships)
GRAPH_PREDICATES = {
    "d55dc3fe-9a9f-5908-baae-e67d0fa0eab0": "subClassOf",
    "4b368645-5f7a-551b-940f-acebfe3d0bd2": "subPropertyOf",
    "84d654c0-420b-5a08-ad64-1f16d51de0b2": "domain",
    "c6a11966-a018-5be8-95a0-eba182c2fd93": "range",
    "73b69787-81ea-563e-8e09-9c84cad4cf2b": "type",
}

# HTML template with search and navigation
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
            --accent: #238636;
        }}
        * {{ box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg);
            color: var(--fg);
            margin: 0;
            padding: 0;
            line-height: 1.6;
        }}
        .layout {{
            display: flex;
            min-height: 100vh;
        }}
        .sidebar {{
            width: 280px;
            background: var(--header-bg);
            border-right: 1px solid var(--border);
            padding: 20px;
            position: fixed;
            height: 100vh;
            overflow-y: auto;
        }}
        .sidebar-hidden .sidebar {{ display: none; }}
        .sidebar-hidden .main {{ margin-left: 0; max-width: 100%; }}
        .main {{
            flex: 1;
            margin-left: 280px;
            padding: 20px 40px;
            max-width: 900px;
        }}
        .search-box {{
            width: 100%;
            padding: 10px 12px;
            background: var(--bg);
            border: 1px solid var(--border);
            border-radius: 6px;
            color: var(--fg);
            font-size: 14px;
            margin-bottom: 16px;
        }}
        .search-box:focus {{
            outline: none;
            border-color: var(--link);
        }}
        .search-results {{
            max-height: 300px;
            overflow-y: auto;
            margin-bottom: 16px;
            display: none;
        }}
        .search-results.active {{ display: block; }}
        .search-result {{
            padding: 8px 10px;
            border-radius: 4px;
            cursor: pointer;
            font-size: 13px;
        }}
        .search-result:hover {{ background: var(--bg); }}
        .search-result .prefix {{ color: #8b949e; }}
        .filter-group {{
            margin-bottom: 16px;
        }}
        .filter-group label {{
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 4px 0;
            cursor: pointer;
            font-size: 13px;
        }}
        .filter-group input[type="checkbox"] {{
            accent-color: var(--accent);
        }}
        .sidebar-nav {{
            border-top: 1px solid var(--border);
            padding-top: 16px;
            margin-top: 16px;
        }}
        .sidebar-nav a {{
            display: block;
            padding: 6px 0;
            color: var(--fg);
            text-decoration: none;
            font-size: 13px;
        }}
        .sidebar-nav a:hover {{ color: var(--link); }}
        .sidebar-nav a.active {{ color: var(--link); font-weight: 600; }}
        a {{ color: var(--link); text-decoration: none; }}
        a:hover {{ text-decoration: underline; }}
        h1, h2, h3 {{ color: #fff; }}
        h1 {{ border-bottom: 1px solid var(--border); padding-bottom: 10px; }}
        .uri {{ color: #8b949e; font-family: monospace; font-size: 14px; word-break: break-all; }}
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
        .badge-namespace {{ background: #a371f733; color: #a371f7; }}
        .breadcrumb {{ color: #8b949e; margin-bottom: 20px; }}
        .resource-list {{ list-style: none; padding: 0; }}
        .resource-list li {{ padding: 8px 0; border-bottom: 1px solid var(--border); }}
        .resource-list li.hidden {{ display: none; }}
        .description {{ background: var(--code-bg); padding: 16px; border-radius: 6px; margin: 16px 0; }}
        code {{ background: var(--code-bg); padding: 2px 6px; border-radius: 4px; font-family: monospace; }}
        .nav {{ display: flex; gap: 12px; margin-bottom: 30px; flex-wrap: wrap; }}
        .nav a {{ padding: 8px 16px; background: var(--header-bg); border-radius: 6px; }}
        .toggle-sidebar {{
            position: fixed;
            top: 10px;
            left: 10px;
            z-index: 1000;
            background: var(--header-bg);
            border: 1px solid var(--border);
            color: var(--fg);
            padding: 6px 10px;
            border-radius: 4px;
            cursor: pointer;
            display: none;
        }}
        .stats {{ display: flex; gap: 20px; margin: 16px 0; flex-wrap: wrap; }}
        .stat {{ background: var(--code-bg); padding: 12px 16px; border-radius: 6px; }}
        .stat-value {{ font-size: 24px; font-weight: 600; color: #fff; }}
        .stat-label {{ font-size: 12px; color: #8b949e; }}
        /* Tooltips */
        [data-tooltip] {{
            position: relative;
        }}
        [data-tooltip]:hover::after {{
            content: attr(data-tooltip);
            position: absolute;
            bottom: 100%;
            left: 50%;
            transform: translateX(-50%);
            background: var(--header-bg);
            border: 1px solid var(--border);
            color: var(--fg);
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 12px;
            white-space: normal;
            max-width: 300px;
            z-index: 1000;
            box-shadow: 0 4px 12px rgba(0,0,0,0.4);
            pointer-events: none;
        }}
        /* Relationship graph */
        .graph-container {{
            background: var(--code-bg);
            border-radius: 8px;
            margin: 20px 0;
            padding: 10px;
            min-height: 250px;
            position: relative;
        }}
        .graph-container svg {{
            width: 100%;
            height: 250px;
        }}
        .graph-node {{
            cursor: pointer;
        }}
        .graph-node circle {{
            stroke: var(--border);
            stroke-width: 2;
        }}
        .graph-node.center circle {{
            stroke: var(--link);
            stroke-width: 3;
        }}
        .graph-node text {{
            font-size: 10px;
            fill: var(--fg);
            text-anchor: middle;
            dominant-baseline: middle;
        }}
        .graph-link {{
            stroke: var(--border);
            stroke-opacity: 0.6;
            fill: none;
        }}
        .graph-link-label {{
            font-size: 9px;
            fill: #8b949e;
        }}
        .graph-legend {{
            display: flex;
            gap: 16px;
            flex-wrap: wrap;
            margin-top: 10px;
            font-size: 11px;
            color: #8b949e;
        }}
        .graph-legend span {{
            display: flex;
            align-items: center;
            gap: 4px;
        }}
        .graph-legend-dot {{
            width: 10px;
            height: 10px;
            border-radius: 50%;
        }}
        @media (max-width: 768px) {{
            .sidebar {{ display: none; }}
            .main {{ margin-left: 0; padding: 16px; }}
            .toggle-sidebar {{ display: block; }}
            body.sidebar-open .sidebar {{ display: block; position: fixed; z-index: 999; }}
        }}
    </style>
    <script src="https://d3js.org/d3.v7.min.js"></script>
</head>
<body>
    <button class="toggle-sidebar" onclick="document.body.classList.toggle('sidebar-open')">☰ Menu</button>
    <div class="layout">
        <nav class="sidebar">
            <input type="text" class="search-box" id="search" placeholder="Search terms..." autocomplete="off">
            <div class="search-results" id="searchResults"></div>
            <div class="filter-group" id="filters">
                <strong style="font-size: 12px; color: #8b949e;">FILTER BY TYPE</strong>
                <label><input type="checkbox" checked data-filter="class"> Classes</label>
                <label><input type="checkbox" checked data-filter="property"> Properties</label>
                <label><input type="checkbox" checked data-filter="datatype"> Datatypes</label>
            </div>
            <div class="sidebar-nav" id="sidebarNav">
                {sidebar_nav}
            </div>
        </nav>
        <main class="main">
            {content}
        </main>
    </div>
    <script>
        // Search functionality
        const searchIndex = {search_index};
        const searchInput = document.getElementById('search');
        const searchResults = document.getElementById('searchResults');

        if (searchInput && searchIndex.length > 0) {{
            searchInput.addEventListener('input', function() {{
                const query = this.value.toLowerCase().trim();
                if (query.length < 2) {{
                    searchResults.classList.remove('active');
                    return;
                }}
                const matches = searchIndex.filter(item =>
                    item.label.toLowerCase().includes(query) ||
                    item.alias.toLowerCase().includes(query)
                ).slice(0, 20);

                if (matches.length === 0) {{
                    searchResults.innerHTML = '<div class="search-result">No results</div>';
                }} else {{
                    searchResults.innerHTML = matches.map(m =>
                        `<a href="${{m.url}}" class="search-result">
                            <span class="badge badge-${{m.type}}">${{m.type[0].toUpperCase()}}</span>
                            ${{m.label}} <span class="prefix">${{m.prefix}}</span>
                        </a>`
                    ).join('');
                }}
                searchResults.classList.add('active');
            }});

            // Hide results on outside click
            document.addEventListener('click', function(e) {{
                if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {{
                    searchResults.classList.remove('active');
                }}
            }});

            // Keyboard navigation
            searchInput.addEventListener('keydown', function(e) {{
                if (e.key === 'Escape') {{
                    searchResults.classList.remove('active');
                    this.blur();
                }}
            }});
        }}

        // Filter functionality
        const filters = document.querySelectorAll('[data-filter]');
        const resourceItems = document.querySelectorAll('.resource-list li[data-type]');

        filters.forEach(filter => {{
            filter.addEventListener('change', function() {{
                const activeFilters = Array.from(filters)
                    .filter(f => f.checked)
                    .map(f => f.dataset.filter);

                resourceItems.forEach(item => {{
                    const type = item.dataset.type;
                    item.classList.toggle('hidden', !activeFilters.includes(type));
                }});
            }});
        }});

        // Keyboard shortcut for search
        document.addEventListener('keydown', function(e) {{
            if (e.key === '/' && document.activeElement !== searchInput) {{
                e.preventDefault();
                searchInput?.focus();
            }}
        }});
    </script>
    {graph_script}
</body>
</html>
"""


def load_resources(repo_root: Path, prefixes: list) -> tuple:
    """Load all resources with their properties.

    Returns:
        tuple: (resources dict, statements list for graph building)
    """
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

    return resources, statements


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


def build_tooltip_index(resources: dict) -> dict:
    """Build index of resource UUIDs to their descriptions for tooltips."""
    tooltip_index = {}
    for uuid, r in resources.items():
        if r["type"] == "namespace":
            continue
        comment = r["properties"].get("comment", [{"value": ""}])[0]["value"]
        if comment:
            # Truncate long comments
            if len(comment) > 150:
                comment = comment[:147] + "..."
            tooltip_index[uuid] = comment
    return tooltip_index


def build_graph_data(resource_uuid: str, resources: dict, statements: list) -> dict:
    """Build graph data for a single resource showing its relationships."""
    if resource_uuid not in resources:
        return {"nodes": [], "links": []}

    center = resources[resource_uuid]
    nodes = {}  # uuid -> node data
    links = []

    # Add center node
    nodes[resource_uuid] = {
        "id": resource_uuid,
        "label": center["alias"].split(":")[-1],
        "type": get_resource_type(center),
        "center": True,
        "url": None,  # Current page
    }

    # Find relationships from statements
    for subj_uuid, pred_uuid, obj_value in statements:
        pred_name = GRAPH_PREDICATES.get(pred_uuid)
        if not pred_name:
            continue

        # Outgoing: this resource -> other
        if subj_uuid == resource_uuid and obj_value in resources:
            target = resources[obj_value]
            if obj_value not in nodes:
                local = target["alias"].split(":")[-1]
                nodes[obj_value] = {
                    "id": obj_value,
                    "label": local,
                    "type": get_resource_type(target),
                    "center": False,
                    "url": f"../{target['prefix']}/{local}.html",
                }
            links.append({
                "source": resource_uuid,
                "target": obj_value,
                "label": pred_name,
                "direction": "out",
            })

        # Incoming: other -> this resource
        elif obj_value == resource_uuid and subj_uuid in resources:
            source = resources[subj_uuid]
            if subj_uuid not in nodes:
                local = source["alias"].split(":")[-1]
                nodes[subj_uuid] = {
                    "id": subj_uuid,
                    "label": local,
                    "type": get_resource_type(source),
                    "center": False,
                    "url": f"../{source['prefix']}/{local}.html",
                }
            links.append({
                "source": subj_uuid,
                "target": resource_uuid,
                "label": pred_name,
                "direction": "in",
            })

    # Limit to 20 nodes to keep graph readable
    if len(nodes) > 20:
        # Keep center + top 19 by link count
        link_counts = defaultdict(int)
        for link in links:
            link_counts[link["source"]] += 1
            link_counts[link["target"]] += 1
        sorted_nodes = sorted(
            [n for n in nodes.values() if not n["center"]],
            key=lambda x: link_counts[x["id"]],
            reverse=True
        )[:19]
        keep_ids = {resource_uuid} | {n["id"] for n in sorted_nodes}
        nodes = {k: v for k, v in nodes.items() if k in keep_ids}
        links = [l for l in links if l["source"] in keep_ids and l["target"] in keep_ids]

    return {
        "nodes": list(nodes.values()),
        "links": links,
    }


def generate_graph_script(graph_data: dict) -> str:
    """Generate D3.js script to render relationship graph."""
    if not graph_data["nodes"] or len(graph_data["nodes"]) <= 1:
        return ""

    # Color scheme for node types and link directions
    colors = {
        "class": "#388bfd",
        "property": "#56d364",
        "datatype": "#f78166",
    }

    return f"""
    <script>
    (function() {{
        const graphData = {json.dumps(graph_data)};
        const colors = {json.dumps(colors)};

        const container = document.getElementById('relationshipGraph');
        if (!container || graphData.nodes.length <= 1) return;

        const width = container.clientWidth;
        const height = 250;

        const svg = d3.select(container)
            .append('svg')
            .attr('width', width)
            .attr('height', height);

        // Arrow marker for directed edges
        svg.append('defs').selectAll('marker')
            .data(['end'])
            .enter().append('marker')
            .attr('id', 'arrow')
            .attr('viewBox', '0 -5 10 10')
            .attr('refX', 20)
            .attr('refY', 0)
            .attr('markerWidth', 6)
            .attr('markerHeight', 6)
            .attr('orient', 'auto')
            .append('path')
            .attr('d', 'M0,-5L10,0L0,5')
            .attr('fill', '#8b949e');

        const simulation = d3.forceSimulation(graphData.nodes)
            .force('link', d3.forceLink(graphData.links).id(d => d.id).distance(80))
            .force('charge', d3.forceManyBody().strength(-200))
            .force('center', d3.forceCenter(width / 2, height / 2))
            .force('collision', d3.forceCollide().radius(30));

        const link = svg.append('g')
            .selectAll('line')
            .data(graphData.links)
            .enter().append('line')
            .attr('class', 'graph-link')
            .attr('marker-end', 'url(#arrow)');

        const linkLabel = svg.append('g')
            .selectAll('text')
            .data(graphData.links)
            .enter().append('text')
            .attr('class', 'graph-link-label')
            .text(d => d.label);

        const node = svg.append('g')
            .selectAll('g')
            .data(graphData.nodes)
            .enter().append('g')
            .attr('class', d => 'graph-node' + (d.center ? ' center' : ''))
            .style('cursor', d => d.url ? 'pointer' : 'default')
            .on('click', (event, d) => {{ if (d.url) window.location.href = d.url; }})
            .call(d3.drag()
                .on('start', (event, d) => {{
                    if (!event.active) simulation.alphaTarget(0.3).restart();
                    d.fx = d.x; d.fy = d.y;
                }})
                .on('drag', (event, d) => {{ d.fx = event.x; d.fy = event.y; }})
                .on('end', (event, d) => {{
                    if (!event.active) simulation.alphaTarget(0);
                    d.fx = null; d.fy = null;
                }}));

        node.append('circle')
            .attr('r', d => d.center ? 12 : 8)
            .attr('fill', d => colors[d.type] || '#8b949e');

        node.append('text')
            .attr('dy', 20)
            .text(d => d.label.length > 12 ? d.label.slice(0, 10) + '..' : d.label);

        simulation.on('tick', () => {{
            link.attr('x1', d => d.source.x)
                .attr('y1', d => d.source.y)
                .attr('x2', d => d.target.x)
                .attr('y2', d => d.target.y);

            linkLabel.attr('x', d => (d.source.x + d.target.x) / 2)
                     .attr('y', d => (d.source.y + d.target.y) / 2);

            node.attr('transform', d => `translate(${{d.x}},${{d.y}})`);
        }});
    }})();
    </script>
    """


def build_search_index(resources: dict) -> list:
    """Build search index for all resources."""
    index = []
    for uuid, r in resources.items():
        if r["type"] == "namespace":
            continue
        rtype = get_resource_type(r)
        local = r["alias"].split(":")[-1]
        label = r["properties"].get("label", [{"value": local}])[0]["value"]
        index.append({
            "label": label,
            "alias": r["alias"],
            "prefix": r["prefix"],
            "type": rtype,
            "url": f"{r['prefix']}/{local}.html",
        })
    return index


def build_sidebar_nav(prefixes: list, resources: dict, current_prefix: str = "") -> str:
    """Build sidebar navigation HTML."""
    nav = '<strong style="font-size: 12px; color: #8b949e;">NAMESPACES</strong>'
    for prefix in sorted(prefixes):
        ns_count = len([r for r in resources.values() if r["prefix"] == prefix])
        if ns_count == 0:
            continue
        active = ' class="active"' if prefix == current_prefix else ''
        nav += f'<a href="../{prefix}/index.html"{active}>{prefix} ({ns_count})</a>'
    return nav


def generate_resource_page(resource: dict, resources: dict, prefixes: list,
                           resource_uuid: str, statements: list, tooltip_index: dict) -> str:
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

    # Build properties table with tooltips
    prop_rows = ""
    for pred_name, values in sorted(props.items()):
        if pred_name in ("label", "comment"):
            continue
        for v in values:
            if v["link"]:
                # Try to add tooltip for linked resources
                # Extract UUID from link path (../prefix/localname.html)
                tooltip_attr = ""
                for uuid, desc in tooltip_index.items():
                    if resources.get(uuid, {}).get("alias", "").endswith(v["value"]):
                        tooltip_attr = f' data-tooltip="{escape(desc)}"'
                        break
                value_html = f'<a href="{v["link"]}"{tooltip_attr}>{escape(v["value"])}</a>'
            else:
                value_html = escape(v["value"])
            prop_rows += f'<tr><td><code>{v["predicate"]}</code></td><td>{value_html}</td></tr>'

    # Build relationship graph
    graph_data = build_graph_data(resource_uuid, resources, statements)
    graph_html = ""
    if graph_data["nodes"] and len(graph_data["nodes"]) > 1:
        graph_html = f"""
        <h2>Relationships</h2>
        <div class="graph-container" id="relationshipGraph"></div>
        <div class="graph-legend">
            <span><div class="graph-legend-dot" style="background: #388bfd;"></div> Class</span>
            <span><div class="graph-legend-dot" style="background: #56d364;"></div> Property</span>
            <span><div class="graph-legend-dot" style="background: #f78166;"></div> Datatype</span>
        </div>
        """

    content = f"""
    <div class="breadcrumb">
        <a href="../index.html">Ontologies</a> / <a href="index.html">{prefix}</a> / {alias.split(":")[-1]}
    </div>
    <h1><span class="badge {badge_class}">{type_label}</span> {escape(label)}</h1>
    <div class="uri">{escape(uri)}</div>

    {"<div class='description'>" + escape(comment) + "</div>" if comment else ""}

    {graph_html}

    <h2>Properties</h2>
    <table class="property-table">
        <tr><th>Predicate</th><th>Value</th></tr>
        {prop_rows if prop_rows else "<tr><td colspan='2'>No properties defined</td></tr>"}
    </table>
    """

    search_index = build_search_index(resources)
    sidebar_nav = build_sidebar_nav(prefixes, resources, prefix)
    graph_script = generate_graph_script(graph_data)

    return HTML_TEMPLATE.format(
        title=f"{alias} - Ontology Documentation",
        content=content,
        search_index=json.dumps(search_index),
        sidebar_nav=sidebar_nav,
        graph_script=graph_script
    )


def generate_namespace_page(prefix: str, resources: dict, prefixes: list) -> str:
    """Generate HTML page for a namespace."""
    ns_resources = [r for r in resources.values() if r["prefix"] == prefix]

    # Group by type
    classes = [r for r in ns_resources if get_resource_type(r) == "class"]
    properties = [r for r in ns_resources if get_resource_type(r) == "property"]
    datatypes = [r for r in ns_resources if get_resource_type(r) == "datatype"]

    def resource_list(items, badge_class, rtype):
        if not items:
            return "<p>None</p>"
        html = "<ul class='resource-list'>"
        for r in sorted(items, key=lambda x: x["alias"]):
            local = r["alias"].split(":")[-1]
            label = r["properties"].get("label", [{"value": local}])[0]["value"]
            html += f'<li data-type="{rtype}"><a href="{local}.html"><span class="badge {badge_class}">{local}</span></a> {escape(label)}</li>'
        html += "</ul>"
        return html

    content = f"""
    <div class="breadcrumb">
        <a href="../index.html">Ontologies</a> / {prefix}
    </div>
    <h1>{prefix.upper()} Ontology</h1>

    <div class="stats">
        <div class="stat"><div class="stat-value">{len(classes)}</div><div class="stat-label">Classes</div></div>
        <div class="stat"><div class="stat-value">{len(properties)}</div><div class="stat-label">Properties</div></div>
        <div class="stat"><div class="stat-value">{len(datatypes)}</div><div class="stat-label">Datatypes</div></div>
    </div>

    <h2>Classes ({len(classes)})</h2>
    {resource_list(classes, "badge-class", "class")}

    <h2>Properties ({len(properties)})</h2>
    {resource_list(properties, "badge-property", "property")}

    <h2>Datatypes ({len(datatypes)})</h2>
    {resource_list(datatypes, "badge-datatype", "datatype")}
    """

    search_index = build_search_index(resources)
    sidebar_nav = build_sidebar_nav(prefixes, resources, prefix)

    return HTML_TEMPLATE.format(
        title=f"{prefix.upper()} - Ontology Documentation",
        content=content,
        search_index=json.dumps(search_index),
        sidebar_nav=sidebar_nav,
        graph_script=""  # No graph on namespace pages
    )


def build_namespace_graph_data(resources: dict, statements: list) -> dict:
    """Build graph data showing relationships between namespaces."""
    # Count resources per namespace
    ns_counts = defaultdict(lambda: {"classes": 0, "properties": 0, "total": 0})
    for r in resources.values():
        prefix = r["prefix"]
        rtype = get_resource_type(r)
        ns_counts[prefix]["total"] += 1
        if rtype == "class":
            ns_counts[prefix]["classes"] += 1
        elif rtype == "property":
            ns_counts[prefix]["properties"] += 1

    # Count cross-namespace references
    ns_links = defaultdict(int)  # (source_prefix, target_prefix) -> count
    for subj_uuid, pred_uuid, obj_value in statements:
        if subj_uuid not in resources or obj_value not in resources:
            continue
        src_prefix = resources[subj_uuid]["prefix"]
        tgt_prefix = resources[obj_value]["prefix"]
        if src_prefix != tgt_prefix:
            ns_links[(src_prefix, tgt_prefix)] += 1

    # Build nodes
    nodes = []
    for prefix, counts in ns_counts.items():
        if counts["total"] == 0:
            continue
        nodes.append({
            "id": prefix,
            "label": prefix.upper(),
            "size": min(30, 8 + counts["total"] // 50),  # Size by resource count
            "classes": counts["classes"],
            "properties": counts["properties"],
            "total": counts["total"],
            "url": f"{prefix}/index.html",
        })

    # Build links (aggregate both directions, show strongest connections)
    link_map = {}
    for (src, tgt), count in ns_links.items():
        key = tuple(sorted([src, tgt]))
        if key not in link_map:
            link_map[key] = {"source": key[0], "target": key[1], "weight": 0}
        link_map[key]["weight"] += count

    # Keep only significant links (top 50 by weight)
    links = sorted(link_map.values(), key=lambda x: x["weight"], reverse=True)[:50]

    return {"nodes": nodes, "links": links}


def generate_namespace_graph_script(graph_data: dict) -> str:
    """Generate D3.js script for namespace overview graph."""
    if not graph_data["nodes"]:
        return ""

    return f"""
    <script>
    (function() {{
        const graphData = {json.dumps(graph_data)};

        const container = document.getElementById('namespaceGraph');
        if (!container) return;

        const width = container.clientWidth;
        const height = 400;

        const svg = d3.select(container)
            .append('svg')
            .attr('width', width)
            .attr('height', height);

        // Scale link width by weight
        const maxWeight = Math.max(...graphData.links.map(l => l.weight), 1);
        const linkScale = d3.scaleLinear().domain([1, maxWeight]).range([0.5, 4]);

        const simulation = d3.forceSimulation(graphData.nodes)
            .force('link', d3.forceLink(graphData.links).id(d => d.id).distance(100))
            .force('charge', d3.forceManyBody().strength(-300))
            .force('center', d3.forceCenter(width / 2, height / 2))
            .force('collision', d3.forceCollide().radius(d => d.size + 10));

        const link = svg.append('g')
            .selectAll('line')
            .data(graphData.links)
            .enter().append('line')
            .attr('stroke', '#30363d')
            .attr('stroke-opacity', 0.6)
            .attr('stroke-width', d => linkScale(d.weight));

        const node = svg.append('g')
            .selectAll('g')
            .data(graphData.nodes)
            .enter().append('g')
            .style('cursor', 'pointer')
            .on('click', (event, d) => window.location.href = d.url)
            .call(d3.drag()
                .on('start', (event, d) => {{
                    if (!event.active) simulation.alphaTarget(0.3).restart();
                    d.fx = d.x; d.fy = d.y;
                }})
                .on('drag', (event, d) => {{ d.fx = event.x; d.fy = event.y; }})
                .on('end', (event, d) => {{
                    if (!event.active) simulation.alphaTarget(0);
                    d.fx = null; d.fy = null;
                }}));

        node.append('circle')
            .attr('r', d => d.size)
            .attr('fill', '#a371f7')
            .attr('stroke', '#30363d')
            .attr('stroke-width', 2);

        node.append('text')
            .attr('dy', d => d.size + 12)
            .attr('text-anchor', 'middle')
            .attr('fill', '#c9d1d9')
            .attr('font-size', '10px')
            .text(d => d.label);

        node.append('title')
            .text(d => `${{d.label}}: ${{d.classes}} classes, ${{d.properties}} properties`);

        simulation.on('tick', () => {{
            link.attr('x1', d => d.source.x)
                .attr('y1', d => d.source.y)
                .attr('x2', d => d.target.x)
                .attr('y2', d => d.target.y);

            node.attr('transform', d => `translate(${{d.x}},${{d.y}})`);
        }});
    }})();
    </script>
    """


def generate_index_page(prefixes: list, resources: dict, statements: list) -> str:
    """Generate main index page with namespace overview graph."""
    # Calculate totals
    total_classes = len([r for r in resources.values() if get_resource_type(r) == "class"])
    total_props = len([r for r in resources.values() if get_resource_type(r) == "property"])
    total_datatypes = len([r for r in resources.values() if get_resource_type(r) == "datatype"])
    total_ns = len([p for p in prefixes if any(r["prefix"] == p for r in resources.values())])

    ns_list = ""
    for prefix in sorted(prefixes):
        ns_resources = [r for r in resources.values() if r["prefix"] == prefix]
        if not ns_resources:
            continue
        classes = len([r for r in ns_resources if get_resource_type(r) == "class"])
        props = len([r for r in ns_resources if get_resource_type(r) == "property"])
        ns_list += f'<li data-type="namespace"><a href="{prefix}/index.html"><span class="badge badge-namespace">{prefix}</span></a> {classes} classes, {props} properties</li>'

    # Build namespace graph
    ns_graph_data = build_namespace_graph_data(resources, statements)

    content = f"""
    <h1>Exocortex Public Ontologies</h1>
    <p>Documentation for RDF ontologies in the Exocortex knowledge management ecosystem.</p>
    <p><kbd>/</kbd> to search &bull; Filter by type in sidebar</p>

    <div class="nav">
        <a href="../browser.html">Visual Browser</a>
        <a href="https://github.com/kitelev/exocortex-public-ontologies">GitHub</a>
    </div>

    <div class="stats">
        <div class="stat"><div class="stat-value">{total_ns}</div><div class="stat-label">Namespaces</div></div>
        <div class="stat"><div class="stat-value">{total_classes}</div><div class="stat-label">Classes</div></div>
        <div class="stat"><div class="stat-value">{total_props}</div><div class="stat-label">Properties</div></div>
        <div class="stat"><div class="stat-value">{total_datatypes}</div><div class="stat-label">Datatypes</div></div>
    </div>

    <h2>Namespace Relationships</h2>
    <p style="font-size: 13px; color: #8b949e;">
        Click a namespace to explore. Node size = resource count. Line thickness = cross-references.
    </p>
    <div class="graph-container" id="namespaceGraph" style="min-height: 400px;"></div>

    <h2>Available Ontologies ({total_ns})</h2>
    <ul class="resource-list">
        {ns_list}
    </ul>
    """

    search_index = build_search_index(resources)
    sidebar_nav = build_sidebar_nav(prefixes, resources)
    graph_script = generate_namespace_graph_script(ns_graph_data)

    return HTML_TEMPLATE.format(
        title="Exocortex Public Ontologies",
        content=content,
        search_index=json.dumps(search_index),
        sidebar_nav=sidebar_nav,
        graph_script=graph_script
    )


def main():
    repo_root = SCRIPT_DIR.parent
    output_dir = repo_root / "docs" / "ontology"
    output_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("Ontology Documentation Generator")
    print("=" * 60)

    prefix_dirs = get_prefix_dirs(repo_root)
    print(f"Loading resources from {len(prefix_dirs)} namespaces...")

    resources, statements = load_resources(repo_root, prefix_dirs)
    print(f"  Found {len(resources)} resources")
    print(f"  Found {len(statements)} statements for graph")

    # Build tooltip index
    tooltip_index = build_tooltip_index(resources)
    print(f"  Built tooltip index with {len(tooltip_index)} entries")

    # Generate main index
    print("Generating index page...")
    with open(output_dir / "index.html", "w", encoding="utf-8") as f:
        f.write(generate_index_page(prefix_dirs, resources, statements))

    # Generate namespace pages
    for prefix in prefix_dirs:
        ns_resources = [(uuid, r) for uuid, r in resources.items() if r["prefix"] == prefix]
        if not ns_resources:
            continue

        ns_dir = output_dir / prefix
        ns_dir.mkdir(exist_ok=True)

        print(f"  {prefix}: {len(ns_resources)} resources")

        # Namespace index
        with open(ns_dir / "index.html", "w", encoding="utf-8") as f:
            f.write(generate_namespace_page(prefix, resources, prefix_dirs))

        # Individual resource pages
        for uuid, r in ns_resources:
            local = r["alias"].split(":")[-1]
            # Sanitize filename
            safe_local = "".join(c if c.isalnum() or c in "-_" else "_" for c in local)
            with open(ns_dir / f"{safe_local}.html", "w", encoding="utf-8") as f:
                f.write(generate_resource_page(r, resources, prefix_dirs, uuid, statements, tooltip_index))

    print(f"\n✅ Generated documentation in {output_dir}")
    print(f"   Open {output_dir}/index.html to browse")


if __name__ == "__main__":
    main()

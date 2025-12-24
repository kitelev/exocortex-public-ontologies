#!/usr/bin/env python3
"""
Compare exported file-based ontologies against original W3C sources.

This script performs semantic comparison, handling blank node differences.

Usage:
    python scripts/compare_ontologies.py [namespace] [--all] [--verbose]

Examples:
    python scripts/compare_ontologies.py time          # Compare TIME ontology
    python scripts/compare_ontologies.py --all         # Compare all ontologies
"""

import sys
from pathlib import Path
from typing import Dict, Set, Tuple, Optional
from collections import defaultdict

try:
    from rdflib import Graph, URIRef, Literal, BNode
    from rdflib.compare import isomorphic
except ImportError:
    print("Error: rdflib is required. Install with: pip install rdflib")
    sys.exit(1)

# Import export function from export_rdf
sys.path.insert(0, str(Path(__file__).parent))
from export_rdf import export_namespace, PREFIX_TO_URI  # noqa: E402

REPO_ROOT = Path(__file__).parent.parent
ORIGINALS_DIR = REPO_ROOT / "originals"
EXPORTS_DIR = REPO_ROOT / "exports"

# Mapping from namespace to original file
ORIGINAL_FILES = {
    "time": "time.rdf",
    "prov": "prov.rdf",
    "owl": "owl.rdf",
    "rdf": "rdf.rdf",
    "rdfs": "rdfs.rdf",
    "skos": "skos.rdf",
    "dc": "dc.ttl",
    "dcterms": "dcterms.ttl",
    "geo": "geo.rdf",
}


def detect_format(filepath: Path) -> str:
    """Detect RDF format by inspecting file content."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            first_lines = f.read(500)

        # Check content patterns
        if first_lines.strip().startswith("@prefix") or first_lines.strip().startswith("@base"):
            return "turtle"
        elif first_lines.strip().startswith("<?xml") or first_lines.strip().startswith("<rdf:RDF"):
            return "xml"
        elif first_lines.strip().startswith("#") and "@prefix" in first_lines:
            return "turtle"  # Turtle with comment header
        elif "<" in first_lines and ">" in first_lines and " .\n" in first_lines:
            return "nt"  # N-Triples

        # Fallback to extension
        ext = filepath.suffix.lower()
        if ext == ".ttl":
            return "turtle"
        elif ext in (".rdf", ".xml", ".owl"):
            return "xml"
        elif ext == ".nt":
            return "nt"

        return "turtle"  # Default to turtle as it's more common
    except Exception:
        return "xml"


def load_original(namespace: str) -> Optional[Graph]:
    """Load original ontology from originals directory."""
    if namespace not in ORIGINAL_FILES:
        print(f"  ⚠️  No original file configured for {namespace}")
        return None

    filename = ORIGINAL_FILES[namespace]
    filepath = ORIGINALS_DIR / filename

    if not filepath.exists():
        print(f"  ⚠️  Original file not found: {filepath}")
        return None

    g = Graph()

    # Detect format by content inspection
    fmt = detect_format(filepath)

    try:
        g.parse(str(filepath), format=fmt)
        return g
    except Exception as e:
        print(f"  ⚠️  Error parsing original as {fmt}: {e}")
        # Try alternative formats
        for alt_fmt in ["turtle", "xml", "nt"]:
            if alt_fmt != fmt:
                try:
                    g.parse(str(filepath), format=alt_fmt)
                    return g
                except Exception:
                    pass
        return None


def normalize_triple(triple: Tuple, blank_map: Dict[BNode, str]) -> Tuple:
    """Normalize a triple for comparison, replacing blank nodes with canonical IDs."""

    def normalize_term(term):
        if isinstance(term, BNode):
            if term not in blank_map:
                blank_map[term] = f"_:b{len(blank_map)}"
            return blank_map[term]
        elif isinstance(term, URIRef):
            return str(term)
        elif isinstance(term, Literal):
            # Normalize literal representation
            if term.language:
                return f'"{term}"@{term.language}'
            elif term.datatype:
                return f'"{term}"^^<{term.datatype}>'
            else:
                return f'"{term}"'
        else:
            return str(term)

    s, p, o = triple
    return (normalize_term(s), normalize_term(p), normalize_term(o))


def get_triple_signature(triple: Tuple) -> Tuple:
    """Get a signature for a triple that ignores blank node identity.

    Returns (subject_type, predicate, object_type, literal_value_if_any)
    """
    s, p, o = triple

    s_sig = "BLANK" if isinstance(s, BNode) else str(s)
    p_sig = str(p)

    if isinstance(o, BNode):
        o_sig = ("BLANK", None)
    elif isinstance(o, Literal):
        if o.language:
            o_sig = ("LITERAL", f"{o}@{o.language}")
        elif o.datatype:
            o_sig = ("LITERAL", f"{o}^^{o.datatype}")
        else:
            o_sig = ("LITERAL", str(o))
    else:
        o_sig = ("URI", str(o))

    return (s_sig, p_sig, o_sig)


def build_blank_node_structures(g: Graph) -> Dict[BNode, Set[Tuple]]:
    """Build a map of blank nodes to their outgoing triples."""
    blank_structures = defaultdict(set)

    for s, p, o in g:
        if isinstance(s, BNode):
            # Use signature that handles nested blank nodes
            o_sig = "BLANK" if isinstance(o, BNode) else str(o) if isinstance(o, URIRef) else repr(o)
            blank_structures[s].add((str(p), o_sig))

    return blank_structures


def compare_graphs(original: Graph, exported: Graph, verbose: bool = False) -> Dict:
    """Compare two RDF graphs semantically."""

    results = {
        "original_triples": len(original),
        "exported_triples": len(exported),
        "missing_triples": [],  # In original but not in exported
        "extra_triples": [],  # In exported but not in original
        "isomorphic": False,
        "matched_triples": 0,
    }

    # Try isomorphic comparison first (handles blank nodes correctly)
    try:
        results["isomorphic"] = isomorphic(original, exported)
        if results["isomorphic"]:
            results["matched_triples"] = len(original)
            return results
    except Exception:
        pass

    # Build signature-based comparison for non-blank node triples
    original_named = {}  # Non-blank subject triples
    original_blank = {}  # Blank subject triples (keyed by structure)
    exported_named = {}
    exported_blank = {}

    for s, p, o in original:
        sig = get_triple_signature((s, p, o))
        if isinstance(s, BNode):
            original_blank[sig] = (s, p, o)
        else:
            original_named[sig] = (s, p, o)

    for s, p, o in exported:
        sig = get_triple_signature((s, p, o))
        if isinstance(s, BNode):
            exported_blank[sig] = (s, p, o)
        else:
            exported_named[sig] = (s, p, o)

    # Find differences in named triples
    for sig, triple in original_named.items():
        if sig in exported_named:
            results["matched_triples"] += 1
        else:
            results["missing_triples"].append(triple)

    for sig, triple in exported_named.items():
        if sig not in original_named:
            results["extra_triples"].append(triple)

    # For blank node triples, do structural matching
    # This is a simplified approach - matches by (predicate, object_signature)
    matched_blank_sigs = set()

    for sig, triple in original_blank.items():
        if sig in exported_blank:
            results["matched_triples"] += 1
            matched_blank_sigs.add(sig)
        else:
            # Try to find a structural match
            results["missing_triples"].append(triple)

    for sig, triple in exported_blank.items():
        if sig not in original_blank and sig not in matched_blank_sigs:
            results["extra_triples"].append(triple)

    return results


def format_triple(triple: Tuple) -> str:
    """Format a triple for human-readable output."""
    s, p, o = triple

    def format_term(t):
        if isinstance(t, BNode):
            return f"_:{t}"
        elif isinstance(t, URIRef):
            # Try to shorten with prefix
            uri = str(t)
            for prefix, ns_uri in PREFIX_TO_URI.items():
                if uri.startswith(ns_uri):
                    return f"{prefix}:{uri[len(ns_uri):]}"
            return f"<{uri}>"
        elif isinstance(t, Literal):
            if t.language:
                return f'"{t}"@{t.language}'
            elif t.datatype:
                dtype = str(t.datatype)
                for prefix, ns_uri in PREFIX_TO_URI.items():
                    if dtype.startswith(ns_uri):
                        dtype = f"{prefix}:{dtype[len(ns_uri):]}"
                        break
                return f'"{t}"^^{dtype}'
            else:
                return f'"{t}"'
        return str(t)

    return f"  {format_term(s)} {format_term(p)} {format_term(o)}"


# Languages to keep (filter out all others)
ALLOWED_LANGUAGES = {"en", "ru", None}  # None = no language tag


def filter_graph_by_language(g: Graph) -> Graph:
    """Filter graph to only include literals with allowed languages."""
    filtered = Graph()
    for prefix, ns in g.namespaces():
        filtered.bind(prefix, ns)

    for s, p, o in g:
        if isinstance(o, Literal) and o.language:
            if o.language not in ALLOWED_LANGUAGES:
                continue  # Skip literals with disallowed languages
        filtered.add((s, p, o))

    return filtered


def compare_ontology(namespace: str, verbose: bool = False) -> Optional[Dict]:
    """Compare a single ontology against its original."""
    print(f"\n{'='*60}")
    print(f"Comparing {namespace.upper()} ontology")
    print(f"{'='*60}")

    # Load original
    print("\nLoading original...")
    original = load_original(namespace)
    if original is None:
        return None

    # Filter by allowed languages
    original = filter_graph_by_language(original)
    print(f"  Original: {len(original)} triples (filtered to @en/@ru)")

    # Export our version
    print("\nExporting file-based version...")
    exported = export_namespace(namespace, verbose=False)
    print(f"  Exported: {len(exported)} triples")

    # Compare
    print("\nComparing...")
    results = compare_graphs(original, exported, verbose)

    # Report
    print("\n--- Results ---")
    print(f"  Original triples:  {results['original_triples']}")
    print(f"  Exported triples:  {results['exported_triples']}")
    print(f"  Matched triples:   {results['matched_triples']}")

    if results["isomorphic"]:
        print("\n  ✅ Graphs are ISOMORPHIC (semantically identical)")
    else:
        diff = results["original_triples"] - results["matched_triples"]
        if diff == 0 and len(results["extra_triples"]) == 0:
            print("\n  ✅ All triples matched!")
        else:
            print("\n  ⚠️  Differences found:")

            if results["missing_triples"]:
                print(f"\n  Missing from export ({len(results['missing_triples'])}):")
                for triple in results["missing_triples"][:20]:  # Limit output
                    print(format_triple(triple))
                if len(results["missing_triples"]) > 20:
                    print(f"  ... and {len(results['missing_triples']) - 20} more")

            if results["extra_triples"]:
                print(f"\n  Extra in export ({len(results['extra_triples'])}):")
                for triple in results["extra_triples"][:20]:
                    print(format_triple(triple))
                if len(results["extra_triples"]) > 20:
                    print(f"  ... and {len(results['extra_triples']) - 20} more")

    return results


def main():
    verbose = "--verbose" in sys.argv or "-v" in sys.argv
    compare_all = "--all" in sys.argv

    # Get namespaces to compare
    namespaces = []
    for arg in sys.argv[1:]:
        if not arg.startswith("-") and arg in ORIGINAL_FILES:
            namespaces.append(arg)

    if compare_all:
        namespaces = list(ORIGINAL_FILES.keys())

    if not namespaces:
        print("Usage: python scripts/compare_ontologies.py [namespace] [--all] [--verbose]")
        print("\nAvailable namespaces:")
        for ns in sorted(ORIGINAL_FILES.keys()):
            print(f"  {ns}")
        sys.exit(1)

    total_original = 0
    total_exported = 0
    total_matched = 0
    total_missing = 0
    total_extra = 0

    for namespace in namespaces:
        results = compare_ontology(namespace, verbose)
        if results:
            total_original += results["original_triples"]
            total_exported += results["exported_triples"]
            total_matched += results["matched_triples"]
            total_missing += len(results["missing_triples"])
            total_extra += len(results["extra_triples"])

    # Summary
    print("\n" + "=" * 60)
    print("OVERALL SUMMARY")
    print("=" * 60)
    print(f"  Ontologies compared: {len(namespaces)}")
    print(f"  Total original:      {total_original}")
    print(f"  Total exported:      {total_exported}")
    print(f"  Total matched:       {total_matched}")
    print(f"  Total missing:       {total_missing}")
    print(f"  Total extra:         {total_extra}")

    if total_missing == 0 and total_extra == 0:
        print("\n  ✅ All ontologies match!")
    else:
        match_pct = (total_matched / total_original * 100) if total_original > 0 else 0
        print(f"\n  Match rate: {match_pct:.1f}%")


if __name__ == "__main__":
    main()

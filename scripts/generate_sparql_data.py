#!/usr/bin/env python3
"""
Generate merged N-Triples file for SPARQL query interface.

Creates docs/ontologies.nt with all ontology data for client-side SPARQL.

Usage:
    python scripts/generate_sparql_data.py
"""

import sys
from pathlib import Path

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from export_rdf import export_namespace, PREFIX_TO_URI
from rdflib import Graph

REPO_ROOT = Path(__file__).parent.parent
DOCS_DIR = REPO_ROOT / "docs"


def main():
    """Generate merged N-Triples file."""
    print("Generating SPARQL data file...")

    # Get all namespaces that have directories
    namespaces = [ns for ns in PREFIX_TO_URI.keys() if (REPO_ROOT / ns).exists()]

    # Merge all graphs
    merged = Graph()

    for ns in sorted(namespaces):
        print(f"  Processing {ns}...")
        g = export_namespace(ns, verbose=False)
        for triple in g:
            merged.add(triple)
        print(f"    {len(g)} triples")

    # Serialize to N-Triples
    output_path = DOCS_DIR / "ontologies.nt"
    merged.serialize(destination=str(output_path), format="ntriples")

    # Calculate file size
    size_mb = output_path.stat().st_size / (1024 * 1024)

    print(f"\nGenerated {output_path}")
    print(f"  Total triples: {len(merged)}")
    print(f"  File size: {size_mb:.2f} MB")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Analyze blank node usage in original W3C ontologies.
"""

from pathlib import Path
from collections import defaultdict
from rdflib import Graph, BNode, RDF, RDFS, OWL, Namespace

ORIGINALS_DIR = Path(__file__).parent.parent / 'originals'

# Common predicates that indicate blank node patterns
RESTRICTION_PREDICATES = {
    str(OWL.onProperty),
    str(OWL.someValuesFrom),
    str(OWL.allValuesFrom),
    str(OWL.hasValue),
    str(OWL.cardinality),
    str(OWL.minCardinality),
    str(OWL.maxCardinality),
    str(OWL.onClass),
}

LIST_PREDICATES = {
    str(RDF.first),
    str(RDF.rest),
}


def analyze_ontology(filepath: Path) -> dict:
    """Analyze blank node usage in an ontology file."""
    g = Graph()

    try:
        # Try different formats
        for fmt in ['xml', 'turtle', 'n3', 'nt']:
            try:
                g.parse(filepath, format=fmt)
                break
            except:
                continue
    except Exception as e:
        return {'error': str(e)}

    stats = {
        'total_triples': len(g),
        'blank_nodes': set(),
        'blank_as_subject': 0,
        'blank_as_object': 0,
        'patterns': defaultdict(int),
        'examples': [],
    }

    # Find all blank nodes
    for s, p, o in g:
        if isinstance(s, BNode):
            stats['blank_nodes'].add(str(s))
            stats['blank_as_subject'] += 1
        if isinstance(o, BNode):
            stats['blank_nodes'].add(str(o))
            stats['blank_as_object'] += 1

    # Analyze patterns
    for bn in stats['blank_nodes']:
        bn_node = BNode(bn)

        # Check if it's a restriction
        if (bn_node, RDF.type, OWL.Restriction) in g:
            stats['patterns']['owl:Restriction'] += 1
            # Get example
            if len(stats['examples']) < 3:
                props = list(g.predicate_objects(bn_node))
                stats['examples'].append({
                    'type': 'Restriction',
                    'properties': [(str(p), str(o)) for p, o in props]
                })

        # Check if it's a list element
        elif (bn_node, RDF.first, None) in g:
            stats['patterns']['rdf:List'] += 1

        # Check if it's an axiom
        elif (bn_node, RDF.type, OWL.Axiom) in g:
            stats['patterns']['owl:Axiom'] += 1

        # Check if it's a class expression
        elif (bn_node, RDF.type, OWL.Class) in g:
            stats['patterns']['owl:Class (anonymous)'] += 1

        else:
            # Unknown pattern - get type
            types = list(g.objects(bn_node, RDF.type))
            if types:
                stats['patterns'][f'other: {types[0]}'] += 1
            else:
                stats['patterns']['untyped'] += 1

    stats['blank_nodes'] = len(stats['blank_nodes'])
    return stats


def main():
    print("=" * 70)
    print("Blank Node Analysis in Original Ontologies")
    print("=" * 70)
    print()

    files = list(ORIGINALS_DIR.glob('*.rdf')) + list(ORIGINALS_DIR.glob('*.ttl'))

    summary = []

    for f in sorted(files):
        name = f.stem.upper()
        stats = analyze_ontology(f)

        if 'error' in stats:
            print(f"{name}: ERROR - {stats['error']}")
            continue

        summary.append((name, stats))

        print(f"\n{name}:")
        print(f"  Total triples: {stats['total_triples']}")
        print(f"  Blank nodes: {stats['blank_nodes']}")

        if stats['blank_nodes'] > 0:
            print(f"  As subject: {stats['blank_as_subject']}")
            print(f"  As object: {stats['blank_as_object']}")
            print(f"  Patterns:")
            for pattern, count in sorted(stats['patterns'].items(), key=lambda x: -x[1]):
                print(f"    {pattern}: {count}")

            if stats['examples']:
                print(f"  Example blank node:")
                ex = stats['examples'][0]
                print(f"    Type: {ex['type']}")
                for p, o in ex['properties'][:5]:
                    p_short = p.split('#')[-1] if '#' in p else p.split('/')[-1]
                    o_short = o.split('#')[-1] if '#' in o else o.split('/')[-1]
                    print(f"      {p_short}: {o_short}")

    # Summary table
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"{'Ontology':<12} {'Triples':>8} {'BNodes':>8} {'Restrictions':>12} {'Lists':>8}")
    print("-" * 70)

    total_bnodes = 0
    for name, stats in summary:
        restrictions = stats['patterns'].get('owl:Restriction', 0)
        lists = stats['patterns'].get('rdf:List', 0)
        print(f"{name:<12} {stats['total_triples']:>8} {stats['blank_nodes']:>8} {restrictions:>12} {lists:>8}")
        total_bnodes += stats['blank_nodes']

    print("-" * 70)
    print(f"Total blank nodes across all ontologies: {total_bnodes}")


if __name__ == '__main__':
    main()

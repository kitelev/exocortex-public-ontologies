#!/usr/bin/env python3
"""Generate PROV ontology files from original RDF source."""

import re
from pathlib import Path
from rdflib import Graph, Namespace, URIRef, Literal, BNode
from rdflib.namespace import RDF, RDFS, OWL, XSD, DC, DCTERMS, SKOS
import hashlib

REPO_ROOT = Path(__file__).parent.parent
PROV_DIR = REPO_ROOT / 'prov'

# Load original PROV ontology
g = Graph()
g.parse(REPO_ROOT / 'originals' / 'prov.rdf', format='turtle')

# Namespace definitions
PROV = Namespace('http://www.w3.org/ns/prov#')
PROV_O = URIRef('http://www.w3.org/ns/prov-o#')  # Ontology IRI

# Allowed languages
ALLOWED_LANGUAGES = {'en', 'ru', None}

# Map URIs to prefixes
PREFIX_MAP = {
    str(RDF): 'rdf',
    str(RDFS): 'rdfs',
    str(OWL): 'owl',
    str(XSD): 'xsd',
    str(DC): 'dc',
    str(DCTERMS): 'dcterms',
    str(SKOS): 'skos',
    str(PROV): 'prov',
}

# Extended PRED_MAP for common predicates
PRED_MAP = {
    str(RDF.type): 'rdf__type',
    str(RDF.first): 'rdf__first',
    str(RDF.rest): 'rdf__rest',
    str(RDFS.label): 'rdfs__label',
    str(RDFS.comment): 'rdfs__comment',
    str(RDFS.domain): 'rdfs__domain',
    str(RDFS.range): 'rdfs__range',
    str(RDFS.subClassOf): 'rdfs__subClassOf',
    str(RDFS.subPropertyOf): 'rdfs__subPropertyOf',
    str(RDFS.isDefinedBy): 'rdfs__isDefinedBy',
    str(RDFS.seeAlso): 'rdfs__seeAlso',
    str(OWL.versionInfo): 'owl__versionInfo',
    str(OWL.disjointWith): 'owl__disjointWith',
    str(OWL.equivalentClass): 'owl__equivalentClass',
    str(OWL.equivalentProperty): 'owl__equivalentProperty',
    str(OWL.inverseOf): 'owl__inverseOf',
    str(OWL.unionOf): 'owl__unionOf',
    str(OWL.imports): 'owl__imports',
    str(OWL.annotatedProperty): 'owl__annotatedProperty',
    str(OWL.annotatedSource): 'owl__annotatedSource',
    str(OWL.annotatedTarget): 'owl__annotatedTarget',
    str(SKOS.definition): 'skos__definition',
    str(SKOS.editorialNote): 'skos__editorialNote',
    str(SKOS.example): 'skos__example',
    str(SKOS.note): 'skos__note',
    str(SKOS.historyNote): 'skos__historyNote',
    str(SKOS.scopeNote): 'skos__scopeNote',
    str(DCTERMS.description): 'dcterms__description',
}

# Track blank nodes
blank_node_map = {}
blank_node_counter = 0

def escape_case(name):
    """Add dot before uppercase letters for case-insensitive FS."""
    return re.sub(r'([A-Z])', r'.\1', name)

def uri_to_anchor(uri):
    """Convert URI to anchor format (prefix__local with case escaping)."""
    uri_str = str(uri)

    # Check for namespace URI itself (!prefix format)
    # Only match exact namespace URIs, not stripped versions
    for ns_uri, prefix in PREFIX_MAP.items():
        if uri_str == ns_uri:
            return f'!{prefix}'

    # Check for ontology IRI
    if uri_str == str(PROV_O):
        return '!prov_o'

    # Check for prefix:local
    for ns_uri, prefix in PREFIX_MAP.items():
        if uri_str.startswith(ns_uri):
            local = uri_str[len(ns_uri):]
            return f'{prefix}__{escape_case(local)}'

    # Fallback to external URI
    return f'<{uri_str}>'

def bnode_to_anchor(bnode):
    """Convert blank node to anchor format."""
    global blank_node_counter
    bnode_id = str(bnode)
    if bnode_id not in blank_node_map:
        # Generate 8-char hex ID
        hex_id = hashlib.md5(bnode_id.encode()).hexdigest()[:8]
        blank_node_map[bnode_id] = f'prov!{hex_id}'
    return blank_node_map[bnode_id]

def term_to_anchor(term):
    """Convert any RDF term to anchor format."""
    if isinstance(term, BNode):
        return bnode_to_anchor(term)
    elif isinstance(term, URIRef):
        return uri_to_anchor(term)
    else:
        return None

def escape_yaml_string(s):
    """Properly escape a string for YAML double-quoted format."""
    # Replace backslashes first
    s = s.replace('\\', '\\\\')
    # Replace double quotes
    s = s.replace('"', '\\"')
    # Replace newlines and tabs with escape sequences
    s = s.replace('\n', '\\n')
    s = s.replace('\t', '\\t')
    return s

def literal_to_value(lit):
    """Convert literal to YAML value."""
    text = str(lit)

    # Language-tagged literal
    if lit.language:
        # Escape quotes in text
        escaped = escape_yaml_string(text)
        # Format: "\"text\"@lang"
        return '"' + '\\"' + escaped + '\\"' + '@' + lit.language + '"'

    # Datatyped literal
    if lit.datatype:
        escaped = escape_yaml_string(text)
        dtype_anchor = uri_to_anchor(lit.datatype)
        if dtype_anchor.startswith('<'):
            # External datatype URI
            return '"' + '\\"' + escaped + '\\"' + '^^' + dtype_anchor + '"'
        else:
            # Wikilink datatype
            return '"' + '\\"' + escaped + '\\"' + '^^[[' + dtype_anchor + ']]"'

    # Plain literal
    escaped = escape_yaml_string(text)
    return '"' + '\\"' + escaped + '\\"' + '"'

def object_to_value(obj):
    """Convert object to YAML value (wikilink or literal)."""
    if isinstance(obj, (URIRef, BNode)):
        anchor = term_to_anchor(obj)
        if anchor.startswith('<'):
            return f'"{anchor}"'
        return f'"[[{anchor}]]"'
    elif isinstance(obj, Literal):
        return literal_to_value(obj)
    else:
        return f'"{str(obj)}"'

def pred_to_anchor(pred):
    """Convert predicate URI to anchor, using PRED_MAP for common ones."""
    pred_str = str(pred)
    if pred_str in PRED_MAP:
        return PRED_MAP[pred_str]
    return uri_to_anchor(pred)

def sanitize_filename(s):
    """Remove or replace invalid filename characters."""
    # Replace characters that are problematic in filenames
    s = s.replace('/', '_').replace('\\', '_').replace(':', '_').replace('*', '_')
    s = s.replace('?', '_').replace('"', '_').replace('<', '_').replace('>', '_')
    s = s.replace('|', '_')
    return s

def main():
    # Clear existing files
    for f in PROV_DIR.glob('*.md'):
        f.unlink()

    # Process triples
    statement_files = {}  # (subj_anchor, pred_anchor) -> list of obj values
    node_files = set()  # Set of anchors that need node files

    for s, p, o in g:
        # Filter by language
        if isinstance(o, Literal) and o.language:
            if o.language not in ALLOWED_LANGUAGES:
                continue

        subj_anchor = term_to_anchor(s)
        pred_anchor = pred_to_anchor(p)
        obj_value = object_to_value(o)

        # Track nodes
        if isinstance(s, URIRef):
            node_files.add(subj_anchor)
        if isinstance(s, BNode):
            node_files.add(subj_anchor)
        if isinstance(o, URIRef):
            node_files.add(term_to_anchor(o))
        if isinstance(o, BNode):
            node_files.add(term_to_anchor(o))

        # Group by (subj, pred)
        key = (subj_anchor, pred_anchor)
        if key not in statement_files:
            statement_files[key] = []
        statement_files[key].append(obj_value)

    # Write statement files
    for (subj_anchor, pred_anchor), obj_values in statement_files.items():
        for i, obj_value in enumerate(obj_values):
            suffix = '' if i == 0 else str(i + 1)
            subj_safe = sanitize_filename(subj_anchor)
            pred_safe = sanitize_filename(pred_anchor)
            filename = f'{subj_safe} {pred_safe} ___{suffix}.md'
            filepath = PROV_DIR / filename

            # Format wikilinks for subject and predicate
            if subj_anchor.startswith('<'):
                subj_wikilink = f'"{subj_anchor}"'
            else:
                subj_wikilink = f'"[[{subj_anchor}]]"'

            pred_wikilink = f'"[[{pred_anchor}]]"'

            content = f'''---
metadata: statement
rdf__subject: {subj_wikilink}
rdf__predicate: {pred_wikilink}
rdf__object: {obj_value}
---
'''
            filepath.write_text(content, encoding='utf-8')

    # Write node files
    for anchor in node_files:
        if anchor.startswith('<'):
            continue  # Skip external URIs
        anchor_safe = sanitize_filename(anchor)
        filename = f'{anchor_safe}.md'
        filepath = PROV_DIR / filename
        if not filepath.exists():
            content = '''---
metadata: node
---
'''
            filepath.write_text(content, encoding='utf-8')

    # Summary
    print(f"Generated {len(statement_files)} unique (subj,pred) pairs")
    print(f"Total statement files: {sum(len(v) for v in statement_files.values())}")
    print(f"Blank nodes: {len(blank_node_map)}")
    print(f"Node files: {len([a for a in node_files if not a.startswith('<')])}")

if __name__ == '__main__':
    main()

# RDF Ontologies in File-based Triple Format

## File Structure

Each folder represents an ontology (namespace).

### Resource Files

Each RDF resource is represented by an **empty file** with the resource identifier as the filename:
- `rdfs__Class.md` — the resource identifier (empty file)
- `owl__Ontology.md` — the resource identifier (empty file)

### Triple Files

Each RDF triple is represented as a separate file with the format:
```
{subject} {predicate} {object}.md
```

Examples:
- `rdfs__Class a rdfs__Class.md` — type declaration (`rdf:type`)
- `rdfs__Class rdfs__label "Class".md` — literal value
- `rdfs__Class rdfs__subClassOf rdfs__Resource.md` — resource reference

### Ontology Files

The ontology itself is represented by a file with `!` prefix:
- `!rdf.md` — RDF ontology
- `!rdfs.md` — RDFS ontology
- `!owl.md` — OWL ontology

These files contain the `!` property with the ontology URL.

## Naming Conventions

- `__` (double underscore) replaces `:` in prefixed names: `rdfs:Class` → `rdfs__Class`
- `a` is used as shorthand for `rdf:type` (standard SPARQL/Turtle syntax)
- Literal values are quoted: `"Class"`, `"The class of classes."`
- Resource references are unquoted: `rdfs__Resource`

## Example

For the RDF triple:
```turtle
rdfs:Class rdf:type rdfs:Class .
rdfs:Class rdfs:label "Class" .
rdfs:Class rdfs:subClassOf rdfs:Resource .
```

Files:
```
rdfs/
├── rdfs__Class.md                              (empty - resource anchor)
├── rdfs__Class a rdfs__Class.md                (empty - type triple)
├── rdfs__Class rdfs__label "Class".md          (empty - label triple)
├── rdfs__Class rdfs__subClassOf rdfs__Resource.md  (empty - subclass triple)
```

All triple files are empty — the information is encoded in the filename itself.

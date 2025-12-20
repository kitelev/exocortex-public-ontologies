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

Triple files contain YAML frontmatter with reified statement structure:
```yaml
---
rdf:type: "[[rdf__Statement]]"
rdf:subject: "[[{subject}]]"
rdf:predicate: "[[{predicate}]]"
rdf:object: "[[{object}]]"
---
```

For literal values, `rdf:object` contains the literal without wikilinks:
```yaml
rdf:object: "Class"
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
- Literal values are quoted in filename: `"Class"`, `"The class of classes."`
- Resource references are unquoted in filename: `rdfs__Resource`

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
├── rdfs__Class a rdfs__Class.md                (frontmatter with reified triple)
├── rdfs__Class rdfs__label "Class".md          (frontmatter with reified triple)
├── rdfs__Class rdfs__subClassOf rdfs__Resource.md  (frontmatter with reified triple)
```

### Triple File Content Example

File `rdfs__Class a rdfs__Class.md`:
```yaml
---
rdf:type: "[[rdf__Statement]]"
rdf:subject: "[[rdfs__Class]]"
rdf:predicate: "[[rdf__type|a]]"
rdf:object: "[[rdfs__Class]]"
---
```

File `rdfs__Class rdfs__label "Class".md`:
```yaml
---
rdf:type: "[[rdf__Statement]]"
rdf:subject: "[[rdfs__Class]]"
rdf:predicate: "[[rdfs__label]]"
rdf:object: "Class"
---
```

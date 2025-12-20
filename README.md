# RDF Ontologies in File-based Triple Format

## File Structure

Each folder represents a namespace.

### Resource Files

Each RDF resource is represented by an **empty file** with the resource identifier as the filename:
- `rdfs__Class.md` — the resource identifier (empty file)
- `owl__Ontology.md` — the resource identifier (empty file)

### Triple Files

Each RDF triple is represented as a separate file with the format:
```
{subject} {predicate} {object}.md
```

NB: `{object}` не указывается, если его тип [[rdfs__Literal]] - вместо этого указывается `___`

Triple files contain YAML frontmatter with reified statement structure:
```yaml
---
rdf__type: "[[rdf__Statement]]"
rdf__subject: "[[{subject}]]"
rdf__predicate: "[[{predicate}]]"
rdf__object: "[[{object}]]"
---
```

For literal values, `rdf:object` contains the literal without wikilinks:
```yaml
rdf__object: "Class"
```

Если в оригинальном TTL указано `"Class"@en`, то в YAML будет `'"Class"@en'`

Examples:
- `rdfs__Class a rdfs__Class.md` — type declaration (`rdf:type`)
- `rdfs__Class rdfs__label ___.md` — literal value
- `rdfs__Class rdfs__subClassOf rdfs__Resource.md` — resource reference

### Ontology Files

The namespace itself is represented by a file with `!` prefix:
- `!rdf.md` — RDF namespace
- `!rdfs.md` — RDFS namespace
- `!owl.md` — OWL namespace

These files contain the `!` property with the namespace URL.

## Naming Conventions

- `__` (double underscore) replaces `:` in prefixed names: `rdfs:Class` → `rdfs__Class`
- `a` is used as shorthand for `rdf:type` (standard SPARQL/Turtle syntax)
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
├── rdfs__Class rdfs__label ___.md          (frontmatter with reified triple)
├── rdfs__Class rdfs__subClassOf rdfs__Resource.md  (frontmatter with reified triple)
```

### Triple File Content Example

File `rdfs__Class a rdfs__Class.md`:
```yaml
---
rdf__type: "[[rdf__Statement]]"
rdf__subject: "[[rdfs__Class]]"
rdf__predicate: "[[rdf__type|a]]"
rdf__object: "[[rdfs__Class]]"
---
```

File `rdfs__Class rdfs__label ___.md`:
```yaml
---
rdf__type: "[[rdf__Statement]]"
rdf__subject: "[[rdfs__Class]]"
rdf__predicate: "[[rdfs__label]]"
rdf__object: "Class"
---
```

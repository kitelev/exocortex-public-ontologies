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

NB: `{object}` может быть не указан - вместо этого указывается `___`. Это используется, если, например, значение `{object}` слишком длинное. См. пример [[!owl rdfs__comment ___]]

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

Examples:
- `rdfs__Class a rdfs__Class.md` — type declaration (`rdf:type`)
- `rdfs__Class rdfs__label "Class".md` — literal value
- `rdfs__Class rdfs__subClassOf rdfs__Resource.md` — resource reference

### Ontology Files

The namespace itself is represented by a file with `!` prefix:
- `!rdf.md` — RDF namespace
- `!rdfs.md` — RDFS namespace
- `!owl.md` — OWL namespace

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
rdf__type: "[[rdf__Statement]]"
rdf__subject: "[[rdfs__Class]]"
rdf__predicate: "[[rdf__type|a]]"
rdf__object: "[[rdfs__Class]]"
---
```

File `rdfs__Class rdfs__label "Class".md`:
```yaml
---
rdf__type: "[[rdf__Statement]]"
rdf__subject: "[[rdfs__Class]]"
rdf__predicate: "[[rdfs__label]]"
rdf__object: "Class"
---
```

## TODOs
- [ ] Все литералы обернуть в двойные кавычки
	- [ ] При необходимости добавить типизацию
		- Пример `"2000-07-11"^^<http://www.w3.org/2001/XMLSchema#date>`
- [ ] Обновить этот файл через ИИ
- [ ] Описать через ИИ
	- [ ] [[skos__definition]]
	- [ ] [[skos__scopeNote]]
	- [ ] [[owl__AnnotationProperty]]
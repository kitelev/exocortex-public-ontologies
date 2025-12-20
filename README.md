# Exocortex Public Ontologies

File-based RDF ontologies for knowledge management in Obsidian.

## Overview

This repository contains standard W3C and Dublin Core ontologies converted to a file-based triple format. Each RDF triple is represented as a separate Markdown file with YAML frontmatter, enabling:

- **Graph navigation** via Obsidian wikilinks
- **SPARQL-like queries** via Dataview plugin
- **Class hierarchy visualization** via Graph View
- **Human-readable** knowledge representation

Part of the [Exocortex](https://github.com/kitelev/exocortex) knowledge management ecosystem.

## Included Ontologies

| Namespace | Prefix | URI | Files | Coverage |
|-----------|--------|-----|-------|----------|
| RDF | `rdf` | `http://www.w3.org/1999/02/22-rdf-syntax-ns#` | 139 | 100% |
| RDFS | `rdfs` | `http://www.w3.org/2000/01/rdf-schema#` | 86 | 100% |
| OWL 2 | `owl` | `http://www.w3.org/2002/07/owl#` | 432 | 100% |
| Dublin Core Elements | `dc` | `http://purl.org/dc/elements/1.1/` | 84 | 100% |
| Dublin Core Terms | `dcterms` | `http://purl.org/dc/terms/` | 343 | 100% |
| SKOS | `skos` | `http://www.w3.org/2004/02/skos/core` | 126 | 100% |
| FOAF | `foaf` | `http://xmlns.com/foaf/0.1/` | 346 | 100% |
| PROV-O | `prov` | `http://www.w3.org/ns/prov#` | 285 | 100% |
| TIME | `time` | `http://www.w3.org/2006/time#` | 377 | 100% |
| GEO | `geo` | `http://www.w3.org/2003/01/geo/wgs84_pos#` | 33 | 100% |
| VCARD | `vcard` | `http://www.w3.org/2006/vcard/ns#` | 395 | 100% |
| DOAP | `doap` | `http://usefulinc.com/ns/doap#` | 225 | 100% |
| SIOC | `sioc` | `http://rdfs.org/sioc/ns#` | 434 | 100% |
| XSD | `xsd` | `http://www.w3.org/2001/XMLSchema#` | 37 | Core types |

**Total: 3,342 files — 14 ontologies**

## Directory Structure

```
exocortex-public-ontologies/
├── rdf/                    # RDF namespace
│   ├── !rdf.md             # Namespace declaration
│   ├── rdf__Property.md    # Resource anchor
│   ├── rdf__type.md        # Resource anchor
│   └── rdf__type rdfs__label ___.md  # Triple file
├── rdfs/                   # RDFS namespace
├── owl/                    # OWL namespace
├── dc/                     # Dublin Core Elements
├── dcterms/                # Dublin Core Terms
├── skos/                   # SKOS vocabulary
├── foaf/                   # FOAF (Friend of a Friend)
├── prov/                   # PROV-O (Provenance)
├── time/                   # TIME (Temporal entities)
├── geo/                    # GEO (WGS84 coordinates)
├── vcard/                  # VCARD (Contact information)
├── doap/                   # DOAP (Description of a Project)
├── sioc/                   # SIOC (Online Communities)
├── xsd/                    # XSD (XML Schema datatypes)
├── scripts/                # Validation tools
│   ├── validate.py         # Integrity checker
│   └── install-hooks.sh    # Git hooks installer
└── ~templates/             # Obsidian templates
    ├── ~rdf__Statement.md
    └── ~(dataview) Triples.md
```

## File Format

All files have a `metadata` property indicating their type:
- `namespace` — namespace declaration files
- `anchor` — resource anchor files
- `statement` — RDF triple files

### 1. Namespace Files (`!{prefix}.md`)

Define the namespace URI:

```yaml
---
metadata: namespace
"!": http://www.w3.org/1999/02/22-rdf-syntax-ns#
---
```

### 2. Resource Files (`{prefix}__{localname}.md`)

Anchor points for wikilinks:

```yaml
---
metadata: anchor
---
```

Examples: `rdf__Property.md`, `rdfs__Class.md`, `owl__Ontology.md`

### 3. Triple Files (`{subject} {predicate} {object}.md`)

Each RDF triple is a file with statement structure:

**Filename format:**
```
{subject} {predicate} {object}.md
```

**Special cases:**
- Object is a literal: use `___` placeholder
  - `rdfs__Class rdfs__label ___.md`
- Predicate is `rdf:type`: use shorthand `a`
  - `rdf__Property a rdfs__Class.md`

**File content (YAML frontmatter):**

```yaml
---
metadata: statement
rdf__subject: "[[rdf__Property]]"
rdf__predicate: "[[rdf__type|a]]"
rdf__object: "[[rdfs__Class]]"
---
```

For literal values:
```yaml
---
metadata: statement
rdf__subject: "[[rdf__type]]"
rdf__predicate: "[[rdfs__label]]"
rdf__object: type
---
```

Language-tagged literals are preserved:
```yaml
rdf__object: '"Class"@en'
```

## Naming Conventions

| Original | File-based |
|----------|------------|
| `rdfs:Class` | `rdfs__Class` |
| `rdf:type` | `a` (in filenames) |
| `:` (prefix separator) | `__` (double underscore) |
| Literal object | `___` (triple underscore) |
| Namespace file | `!` prefix |

## Usage with Obsidian

### Graph View: Class Hierarchy

To visualize the class hierarchy (only anchors and `rdfs:subClassOf` relations):

```
-(["metadata":statement] -["rdf__predicate":rdfs__subClassOf]) -file:"rdfs__subClassOf.md"
```

This filter:
- Hides all statements EXCEPT those with `rdfs__subClassOf` predicate
- Excludes the `rdfs__subClassOf` property anchor itself

### Graph View: Clean Structure

To hide common meta-properties and focus on domain-specific relations:

```
-file:rdfs__range.md
-file:rdfs__domain.md
-file:rdf__type.md
-["rdf__predicate":rdfs__comment]
-["rdf__predicate":rdfs__label]
-["rdf__predicate":rdfs__isdefinedby]
-file:rdf__property
-file:rdfs__Class.md
-file:rdfs__subClassOf.md
-file:rdfs__Resource
-["metadata":namespace]
```

This filter hides:
- Meta-properties (`rdfs:range`, `rdfs:domain`, `rdf:type`)
- Documentation triples (`rdfs:comment`, `rdfs:label`, `rdfs:isDefinedBy`)
- Core class anchors (`rdfs:Class`, `rdfs:Resource`, `rdf:Property`)
- Namespace declarations

### Querying Triples with Dataview

Find all triples where a resource is the subject:

```dataview
TABLE WITHOUT ID
    link(file.link, "_") AS "_",
    rdf__subject,
    rdf__predicate,
    rdf__object
WHERE rdf__subject = [[rdfs__Class]]
```

Find all triples where a resource is the object:

```dataview
TABLE WITHOUT ID
    rdf__subject,
    rdf__predicate,
    rdf__object
WHERE rdf__object = [[rdfs__Resource]]
```

Filter by metadata type:

```dataview
LIST
WHERE metadata = "anchor"
```

### Templates

The `~templates/` folder contains ready-to-use templates:

- **`~rdf__Statement.md`** — Template for creating new triples
- **`~(dataview) Triples.md`** — Embed in any resource to see related triples

## Examples

### RDF Triple

Original Turtle:
```turtle
rdfs:Class rdf:type rdfs:Class .
rdfs:Class rdfs:label "Class" .
rdfs:Class rdfs:subClassOf rdfs:Resource .
```

File-based representation:
```
rdfs/
├── rdfs__Class.md                                  # Resource anchor
├── rdfs__Class a rdfs__Class.md                    # Type declaration
├── rdfs__Class rdfs__label ___.md                  # Label (literal)
└── rdfs__Class rdfs__subClassOf rdfs__Resource.md  # Subclass relation
```

### Cross-Namespace Reference

File: `owl/!owl owl__imports !rdfs.md`

```yaml
---
metadata: statement
rdf__subject: "[[!owl]]"
rdf__predicate: "[[owl__imports]]"
rdf__object: "[[!rdfs]]"
---
```

This represents: `owl: owl:imports rdfs:` (the OWL ontology imports RDFS)

## Integration with Exocortex

These ontologies provide the semantic foundation for:

- **Ontology-driven layouts** in Obsidian
- **SPARQL queries** via `@kitelev/exocortex-cli`
- **Type inference** and validation
- **Vocabulary standardization** across knowledge bases

## Validation

Run the validation script to check ontology integrity:

```bash
python scripts/validate.py
```

The validator checks:
- **Broken wikilinks** — references to non-existent anchors
- **Missing metadata** — files without `metadata` property
- **Invalid metadata** — files with incorrect metadata values
- **Orphaned anchors** — anchors not referenced in any statement

Use `--verbose` for detailed output.

### Pre-commit Hook

Install the git hook to validate automatically before each commit:

```bash
./scripts/install-hooks.sh
```

The hook blocks commits if validation fails.

## Contributing

1. Fork the repository
2. Add new ontologies following the file format
3. Ensure all resources have anchor files
4. Add `metadata` property to all files
5. Run `python scripts/validate.py` to verify integrity
6. Submit a pull request

## License

The ontology definitions are from W3C and Dublin Core standards.
This file-based format is part of the Exocortex project.

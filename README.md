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

### Verified (100% isomorphic with W3C originals)

| Namespace | Prefix | URI | Triples | Files |
|-----------|--------|-----|---------|-------|
| RDF | `rdf` | `http://www.w3.org/1999/02/22-rdf-syntax-ns#` | 127 | 150 |
| RDFS | `rdfs` | `http://www.w3.org/2000/01/rdf-schema#` | 87 | 104 |
| OWL 2 | `owl` | `http://www.w3.org/2002/07/owl#` | 450 | 536 |
| Dublin Core Elements | `dc` | `http://purl.org/dc/elements/1.1/` | 107 | 123 |
| Dublin Core Terms | `dcterms` | `http://purl.org/dc/terms/` | 700 | 799 |
| SKOS | `skos` | `http://www.w3.org/2004/02/skos/core#` | 252 | 288 |
| PROV-O | `prov` | `http://www.w3.org/ns/prov#` | 1146 | 1330 |
| TIME | `time` | `http://www.w3.org/2006/time#` | 894 | 1063 |
| GEO | `geo` | `http://www.w3.org/2003/01/geo/wgs84_pos#` | 33 | 41 |

**Total verified: 3,796 triples — 9 ontologies**

### Additional (not yet verified)

| Namespace | Prefix | URI | Status |
|-----------|--------|-----|--------|
| FOAF | `foaf` | `http://xmlns.com/foaf/0.1/` | Pending |
| VCARD | `vcard` | `http://www.w3.org/2006/vcard/ns#` | Pending |
| DOAP | `doap` | `http://usefulinc.com/ns/doap#` | Pending |
| SIOC | `sioc` | `http://rdfs.org/sioc/ns#` | Pending |
| XSD | `xsd` | `http://www.w3.org/2001/XMLSchema#` | Core types only |

## Directory Structure

```
exocortex-public-ontologies/
├── rdf/                    # RDF namespace
│   ├── !rdf.md             # Namespace declaration
│   ├── _index.md           # UUID → Label lookup table
│   ├── f1afe09a-...md      # Resource anchor (rdf:Property)
│   └── f1afe09a-... d0e9e696-... ___.md  # Triple file
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
├── scripts/                # Tools
│   ├── validate.py         # Integrity checker
│   ├── import_ontology.py  # RDF → file-based converter
│   ├── migrate_to_uuid.py  # Legacy → UUIDv5 migration
│   └── add_uri_and_index.py # Add URI field and generate indices
└── ~templates/             # Obsidian templates
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

### 2. Resource Files (`{uuid}.md`)

Anchor points for wikilinks. File name is UUIDv5 of the full URI:

```yaml
---
metadata: anchor
uri: http://www.w3.org/1999/02/22-rdf-syntax-ns#Property
---
```

Examples:
- `f1afe09a-f371-5a01-a530-be18bfdb4d6b.md` (rdf:Property)
- `30488677-f427-5947-8a14-02903ca20a7e.md` (rdfs:Class)
- `532c87f0-8cfa-5ff5-990f-aac1562178eb.md` (owl:imports)

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
rdf__subject: "[[f1afe09a-f371-5a01-a530-be18bfdb4d6b]]"
rdf__predicate: "[[73b69787-81ea-563e-8e09-9c84cad4cf2b|a]]"
rdf__object: "[[30488677-f427-5947-8a14-02903ca20a7e]]"
---
```

For literal values:
```yaml
---
metadata: statement
rdf__subject: "[[73b69787-81ea-563e-8e09-9c84cad4cf2b]]"
rdf__predicate: "[[d0e9e696-d3f2-5966-a62f-d8358cbde741]]"
rdf__object: type
---
```

Language-tagged literals are preserved:
```yaml
rdf__object: '"Class"@en'
```

## Naming Conventions

### UUIDv5-based File Names

All resource and statement files use **UUIDv5** identifiers derived from their full URI. This solves the case-insensitive file system issue on macOS where resources like `contributor` and `Contributor` would collide.

**UUID Generation:**
- Namespace: URL (`6ba7b811-9dad-11d1-80b4-00c04fd430c8`)
- Input: Full URI of the resource (e.g., `http://purl.org/dc/elements/1.1/contributor`)
- Result: Deterministic UUID (e.g., `65db3e67-614c-5467-8338-61778bb0c03f`)

**Example:**
```
URI: http://purl.org/dc/elements/1.1/contributor
UUID: 65db3e67-614c-5467-8338-61778bb0c03f
File: dc/65db3e67-614c-5467-8338-61778bb0c03f.md
```

### Index Files

Each ontology directory contains `_index.md` with UUID → Label mapping for human-readable lookup:

```markdown
| UUID | Label | URI |
|------|-------|-----|
| `65db3e67...` | Contributor | http://purl.org/dc/elements/1.1/Contributor |
```

### URI in Frontmatter

Anchor files include the original `uri` field for reverse lookup:

```yaml
---
metadata: anchor
uri: http://purl.org/dc/elements/1.1/contributor
---
```

### Special Naming Conventions

| Element | Convention |
|---------|------------|
| `rdf:type` | `a` (in statement filenames) |
| Literal object | `___` (triple underscore placeholder) |
| Namespace file | `!{prefix}.md` (e.g., `!dc.md`) |
| Blank node | `{prefix}!{8-char-uuid}.md` |
| Index file | `_index.md` |

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
WHERE rdf__subject = [[30488677-f427-5947-8a14-02903ca20a7e]]
```

Find all triples where a resource is the object:

```dataview
TABLE WITHOUT ID
    rdf__subject,
    rdf__predicate,
    rdf__object
WHERE rdf__object = [[d6ac0df2-324e-561c-9f05-41d3b2d5ebd3]]
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
├── 30488677-f427-5947-8a14-02903ca20a7e.md         # rdfs:Class anchor
├── 30488677-... a 30488677-....md                   # Type declaration
├── 30488677-... d0e9e696-... ___.md                 # Label (literal)
└── 30488677-... 55ff3aec-... d6ac0df2-....md        # Subclass relation
```

UUIDs:
- `30488677-f427-5947-8a14-02903ca20a7e` = rdfs:Class
- `d0e9e696-d3f2-5966-a62f-d8358cbde741` = rdfs:label
- `55ff3aec-8d5b-5d4d-a0e1-d3f1c7d3c8d2` = rdfs:subClassOf
- `d6ac0df2-324e-561c-9f05-41d3b2d5ebd3` = rdfs:Resource

### Cross-Namespace Reference

File: `owl/!owl 532c87f0-8cfa-5ff5-990f-aac1562178eb !rdfs.md`

```yaml
---
metadata: statement
rdf__subject: "[[!owl]]"
rdf__predicate: "[[532c87f0-8cfa-5ff5-990f-aac1562178eb]]"
rdf__object: "[[!rdfs]]"
---
```

This represents: `owl: owl:imports rdfs:` (the OWL ontology imports RDFS)

### Lookup UUID by URI

Use Python to find UUID for any URI:

```python
import uuid
uri = "http://www.w3.org/2000/01/rdf-schema#label"
print(uuid.uuid5(uuid.NAMESPACE_URL, uri))
# Output: d0e9e696-d3f2-5966-a62f-d8358cbde741
```

Or check `_index.md` files for human-readable mappings.

## Integration with Exocortex

These ontologies provide the semantic foundation for:

- **Ontology-driven layouts** in Obsidian
- **SPARQL queries** via `@kitelev/exocortex-cli`
- **Type inference** and validation
- **Vocabulary standardization** across knowledge bases

## Validation

### Structural Validation

Run the validation script to check ontology integrity:

```bash
python scripts/validate.py
```

The validator checks:
- **Broken wikilinks** — references to non-existent anchors
- **Missing metadata** — files without `metadata` property
- **Invalid metadata** — files with incorrect metadata values
- **Orphaned anchors** — anchors not referenced in any statement
- **Literal placeholder violations** — `___` used for non-literal objects
- **Blank node consistency** — blank nodes properly defined and referenced

Use `--verbose` for detailed output.

### Isomorphism Comparison

Verify that file-based ontologies are semantically identical to W3C originals:

```bash
# Compare specific ontology
python scripts/compare_ontologies.py rdf

# Compare all verified ontologies
python scripts/compare_ontologies.py --all
```

This exports ontologies to RDF/XML and compares with official W3C sources using rdflib graph isomorphism.

### Importing Ontologies

Convert external RDF ontologies to file-based format:

```bash
# Import from RDF/XML, Turtle, N-Triples, or other formats
python scripts/import_ontology.py <input_file> <output_dir> --prefix <prefix>

# Example: Import Dublin Core Terms
python scripts/import_ontology.py dcterms.ttl dcterms --prefix dcterms

# Auto-detect namespace URI or specify explicitly
python scripts/import_ontology.py myonto.owl myonto --prefix myonto --namespace http://example.org/myonto#
```

Supported formats:
- **RDF/XML** (`.rdf`, `.owl`, `.xml`)
- **Turtle** (`.ttl`)
- **N-Triples** (`.nt`)
- **N3** (`.n3`)
- **JSON-LD** (`.jsonld`, `.json`)
- **TriG** (`.trig`)
- **N-Quads** (`.nq`)

The script auto-detects format from file content and handles blank nodes, external URIs, and multiline literals.

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

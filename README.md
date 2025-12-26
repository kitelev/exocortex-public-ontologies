# Exocortex Public Ontologies

[![CI](https://github.com/kitelev/exocortex-public-ontologies/actions/workflows/ci.yml/badge.svg)](https://github.com/kitelev/exocortex-public-ontologies/actions/workflows/ci.yml)
[![Documentation](https://img.shields.io/badge/docs-GitHub%20Pages-blue)](https://kitelev.github.io/exocortex-public-ontologies/)

File-based RDF ontologies for knowledge management in Obsidian.

## Overview

This repository contains standard W3C and Dublin Core ontologies converted to a file-based triple format. Each RDF triple is represented as a separate Markdown file with YAML frontmatter, enabling:

- **Graph navigation** via Obsidian wikilinks
- **SPARQL-like queries** via Dataview plugin
- **Class hierarchy visualization** via Graph View
- **Human-readable** knowledge representation

Part of the [Exocortex](https://github.com/kitelev/exocortex) knowledge management ecosystem.

## Documentation

| Document | Description |
|----------|-------------|
| [Glossary](docs/glossary.md) | RDF/RDFS/OWL terminology with examples |
| [Cheat Sheet](docs/cheat-sheet.md) | Quick reference for all ontologies |
| [Class Hierarchy](docs/class-hierarchy.md) | All classes with rdfs:subClassOf tree |
| [Property Hierarchy](docs/property-hierarchy.md) | All properties with rdfs:subPropertyOf tree |
| [Cross-References](docs/cross-references.md) | Inter-ontology reference matrix |
| [Lint Report](docs/lint-report.md) | Quality assessment (labels, comments, domain/range) |
| [Diagrams](docs/diagrams/) | Mermaid UML diagrams for each ontology |

## Included Ontologies

### Verified (semantically equivalent to originals)

| Ontology | Prefix | Namespace URI | Triples | Files | Status |
|----------|--------|---------------|---------|-------|--------|
| Schema.org | `schema` | `https://schema.org/` | 17,606 | 20,596 | ✅ |
| DCAT | `dcat` | `http://www.w3.org/ns/dcat#` | 1,338 | 1,407 | ✅ |
| TIME | `time` | `http://www.w3.org/2006/time#` | 1,295 | 1,465 | ✅ |
| SHACL | `sh` | `http://www.w3.org/ns/shacl#` | 1,128 | 1,357 | ✅ |
| PROV-O | `prov` | `http://www.w3.org/ns/prov#` | 1,126 | 1,290 | ✅ |
| ActivityStreams | `as` | `https://www.w3.org/ns/activitystreams#` | 948 | 1,253 | ✅ |
| VCARD | `vcard` | `http://www.w3.org/2006/vcard/ns#` | 882 | 1,111 | ✅ |
| ORG | `org` | `http://www.w3.org/ns/org#` | 746 | 817 | ✅ |
| DOAP | `doap` | `http://usefulinc.com/ns/doap#` | 741 | 803 | ✅ |
| Dublin Core Terms | `dcterms` | `http://purl.org/dc/terms/` | 700 | 800 | ✅ |
| SIOC | `sioc` | `http://rdfs.org/sioc/ns#` | 658 | 758 | ✅ |
| FOAF | `foaf` | `http://xmlns.com/foaf/0.1/` | 620 | 696 | ✅ |
| OWL 2 | `owl` | `http://www.w3.org/2002/07/owl#` | 450 | 529 | ✅ |
| SOSA | `sosa` | `http://www.w3.org/ns/sosa/` | 328 | 366 | ✅ |
| SKOS | `skos` | `http://www.w3.org/2004/02/skos/core#` | 252 | 289 | ✅ |
| RDF | `rdf` | `http://www.w3.org/1999/02/22-rdf-syntax-ns#` | 127 | 150 | ✅ |
| Dublin Core Elements | `dc` | `http://purl.org/dc/elements/1.1/` | 107 | 123 | ✅ |
| RDFS | `rdfs` | `http://www.w3.org/2000/01/rdf-schema#` | 87 | 103 | ✅ |
| GEO | `geo` | `http://www.w3.org/2003/01/geo/wgs84_pos#` | 33 | 41 | ✅ |
| Dublin Core Abstract Model | `dcam` | `http://purl.org/dc/dcam/` | 26 | 31 | ✅ |
| GeoSPARQL | `geosparql` | `http://www.opengis.net/ont/geosparql#` | 774 | 853 | ✅ |
| ADMS | `adms` | `http://www.w3.org/ns/adms#` | 151 | 175 | ✅ |
| VOID | `void` | `http://vocab.deri.ie/void#` | 57 | 69 | ✅ |
| GRDDL | `grddl` | `http://www.w3.org/2003/g/data-view#` | 55 | 69 | ✅ |
| VANN | `vann` | `http://purl.org/vocab/vann/` | 38 | 46 | ✅ |

**Total: 30,707 triples, 35,841 files — 26 ontologies**

### Additional

| Ontology | Prefix | Namespace URI | Status |
|----------|--------|---------------|--------|
| XSD | `xsd` | `http://www.w3.org/2001/XMLSchema#` | Core types only (manually created) |

## Directory Structure

```
exocortex-public-ontologies/
├── rdf/                    # RDF namespace
│   ├── 1f51ee89-....md     # Namespace file (uuid5 of namespace URI)
│   ├── f1afe09a-....md     # Anchor file (uuid5 of resource URI)
│   └── 73b69787-....md     # Statement file (uuid5 of canonical triple)
├── rdfs/                   # RDFS namespace
├── owl/                    # OWL namespace
├── dc/                     # Dublin Core Elements
├── dcterms/                # Dublin Core Terms
├── dcam/                   # Dublin Core Abstract Model
├── skos/                   # SKOS vocabulary
├── foaf/                   # FOAF (Friend of a Friend)
├── prov/                   # PROV-O (Provenance)
├── time/                   # TIME (Temporal entities)
├── geo/                    # GEO (WGS84 coordinates)
├── vcard/                  # VCARD (Contact information)
├── doap/                   # DOAP (Description of a Project)
├── sioc/                   # SIOC (Online Communities)
├── dcat/                   # DCAT (Data Catalog Vocabulary)
├── org/                    # ORG (Organization Ontology)
├── schema/                 # Schema.org vocabulary
├── sh/                     # SHACL (Shapes Constraint Language)
├── sosa/                   # SOSA (Sensor, Observation, Sample, Actuator)
├── adms/                   # ADMS (Asset Description Metadata Schema)
├── as/                     # ActivityStreams 2.0
├── xsd/                    # XSD (XML Schema datatypes)
├── vs/                     # Vocabulary Status (term status)
├── vann/                   # VANN (Vocabulary Annotation)
├── void/                   # VOID (Vocabulary of Interlinked Datasets)
├── grddl/                  # GRDDL (Gleaning Resource Descriptions)
├── geosparql/              # GeoSPARQL (Geospatial queries)
├── tests/                  # pytest test suite
├── scripts/                # Tools
│   ├── import_ontology.py  # RDF → file-based converter
│   ├── validate.py         # Integrity checker (runs on pre-commit)
│   ├── verify_import.py    # Semantic equivalence check
│   ├── export_rdf.py       # Export back to RDF format
│   ├── add_aliases.py      # Add human-readable aliases
│   ├── compare_ontologies.py # Compare ontology directories
│   ├── stats.py            # Generate ontology statistics
│   ├── check_consistency.py # Cross-namespace consistency checks
│   ├── test_consistency.py  # Semantic consistency tests
│   └── generate_class_hierarchy.py # Generate class hierarchy docs
└── ~templates/             # Obsidian templates
```

**All files use UUIDv5 names.** No legacy naming formats are allowed.

## File Format

All files have a `metadata` property indicating their type:
- `namespace` — namespace declaration files
- `anchor` — resource anchor files
- `statement` — RDF triple files
- `blank_node` — blank node anchor files

All files include human-readable **aliases** for navigation in Obsidian.

### 1. Namespace Files (`{uuid}.md`)

Define the namespace URI. File name is UUIDv5 of the namespace URI:

```yaml
---
metadata: namespace
uri: http://www.w3.org/1999/02/22-rdf-syntax-ns#
aliases:
  - "!rdf"
---
```

**UUID Generation:**
```python
import uuid
ns_uri = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
file_uuid = uuid.uuid5(uuid.NAMESPACE_URL, ns_uri)
# Result: 1f51ee89-dd69-5793-8a11-89959f0bc850
```

### 2. Resource Files (`{uuid}.md`)

Anchor points for wikilinks. File name is UUIDv5 of the full URI:

```yaml
---
metadata: anchor
uri: http://www.w3.org/1999/02/22-rdf-syntax-ns#Property
aliases:
  - "rdf:Property"
---
```

Examples:
- `f1afe09a-f371-5a01-a530-be18bfdb4d6b.md` (rdf:Property)
- `30488677-f427-5947-8a14-02903ca20a7e.md` (rdfs:Class)
- `532c87f0-8cfa-5ff5-990f-aac1562178eb.md` (owl:imports)

### 3. Triple Files (`{uuid}.md`)

Each RDF triple is a file with statement structure. File name is UUIDv5 of the canonical triple.

**Canonical Triple Format:**
```
{subject_uri}|{predicate_uri}|{object_canonical}
```

Where `object_canonical` is:
- URI: full URI (e.g., `http://www.w3.org/2000/01/rdf-schema#Class`)
- Literal: `"value"@lang` or `"value"^^<datatype_uri>`
- Blank node: skolem IRI

**UUID Generation:**
```python
import uuid
# For: rdfs:Class rdf:type rdfs:Class
canonical = "http://www.w3.org/2000/01/rdf-schema#Class|http://www.w3.org/1999/02/22-rdf-syntax-ns#type|http://www.w3.org/2000/01/rdf-schema#Class"
file_uuid = uuid.uuid5(uuid.NAMESPACE_URL, canonical)
```

**File content (YAML frontmatter):**

```yaml
---
metadata: statement
subject: "[[f1afe09a-f371-5a01-a530-be18bfdb4d6b]]"
predicate: "[[73b69787-81ea-563e-8e09-9c84cad4cf2b|a]]"
object: "[[30488677-f427-5947-8a14-02903ca20a7e]]"
aliases:
  - "rdf:Property a rdfs:Class"
---
```

For literal values:
```yaml
---
metadata: statement
subject: "[[73b69787-81ea-563e-8e09-9c84cad4cf2b]]"
predicate: "[[d0e9e696-d3f2-5966-a62f-d8358cbde741]]"
object: "\"Class\"@en"
aliases:
  - "rdf:type rdfs:label Class"
---
```

### 4. Blank Node Files (`{uuid}.md`)

Blank nodes use skolemization (RFC 7511) for UUID generation:

```yaml
---
metadata: blank_node
uri: http://www.w3.org/ns/prov/.well-known/genid/a1b2c3d4
aliases:
  - "_:genid-a1b2c3d4"
---
```

**UUID Generation:**
```python
import uuid
namespace_uri = "http://www.w3.org/ns/prov#"
blank_local_id = "a1b2c3d4"  # 8-char hex from MD5 hash
uri = f"{namespace_uri.rstrip('#/')}/.well-known/genid/{blank_local_id}"
file_uuid = uuid.uuid5(uuid.NAMESPACE_URL, uri)
```

## Naming Conventions

### UUIDv5-based File Names

**ALL files** use **UUIDv5** identifiers. This provides:
- Case-insensitive filesystem compatibility (macOS)
- Deterministic, reproducible file names
- No spaces in filenames
- Uniform naming across all file types

**UUID Namespace:** URL (`6ba7b811-9dad-11d1-80b4-00c04fd430c8`)

| File Type | Input for UUIDv5 | Example |
|-----------|------------------|---------|
| Namespace | Namespace URI | `uuid5(URL, "http://purl.org/dc/elements/1.1/")` |
| Anchor | Resource URI | `uuid5(URL, "http://purl.org/dc/elements/1.1/contributor")` |
| Statement | Canonical triple | `uuid5(URL, "{subj_uri}\|{pred_uri}\|{obj}")` |
| Blank node | Skolem IRI | `uuid5(URL, "{ns}/.well-known/genid/{id}")` |

**Example:**
```python
import uuid

# Anchor
uri = "http://purl.org/dc/elements/1.1/contributor"
file_uuid = uuid.uuid5(uuid.NAMESPACE_URL, uri)
# Result: 11183371-dee2-5111-8d61-db2d94aa7701

# Statement
canonical = "http://purl.org/dc/elements/1.1/title|http://www.w3.org/2000/01/rdf-schema#label|\"Title\"@en"
file_uuid = uuid.uuid5(uuid.NAMESPACE_URL, canonical)
```

## Aliases

Each file includes a human-readable alias in the `aliases` frontmatter property. This enables:
- **Quick navigation** in Obsidian via alias search
- **Human-readable identification** of UUID-named files
- **RDF-like triple representation** for statements

### Alias Formats

| File Type | Alias Format | Example |
|-----------|--------------|---------|
| Namespace | `!prefix` | `!rdf`, `!rdfs`, `!owl` |
| Anchor | `prefix:localname` | `rdf:Property`, `rdfs:Class` |
| Blank node | `_:genid-{id}` | `_:genid-a1b2c3d4` |
| Statement | `subj pred obj` | `rdfs:Class a rdfs:Class` |

### Statement Aliases

Statement aliases use the format `{subject_alias} {predicate_alias} {object_alias}`:

- **Subject/Object (URI):** `prefix:localname` (e.g., `rdfs:Class`)
- **Predicate `rdf:type`:** Shortened to `a` (RDF/Turtle convention)
- **Literal objects:** Value in quotes, truncated to 30 chars (e.g., `"The class of classes..."`)
- **Unknown resources:** `?` placeholder

**Examples:**
- `rdfs:Class a rdfs:Class`
- `rdf:Property rdfs:label Property`
- `owl:Thing rdfs:comment "The class of OWL individuals..."`

### Generating Aliases

The `scripts/add_aliases.py` script generates aliases for all existing files:

```bash
# Dry run (preview changes)
python scripts/add_aliases.py --dry-run

# Apply aliases
python scripts/add_aliases.py

# Verbose output
python scripts/add_aliases.py -v
```

The `scripts/import_ontology.py` script automatically generates aliases during import.

### Ontology URI vs Namespace URI

Many ontologies distinguish between:
- **Ontology URI**: The URI of the ontology itself (e.g., `http://www.w3.org/2002/07/owl`)
- **Namespace URI**: The prefix for resources (e.g., `http://www.w3.org/2002/07/owl#`)

The import script handles this automatically:
1. Detects ontology URI from `owl:Ontology` declarations
2. Creates separate anchor file for ontology URI if different from namespace
3. Uses namespace URI (with `#` or `/`) for resource prefixes

**Example (OWL):**
```
Ontology URI: http://www.w3.org/2002/07/owl → UUID: 64e92819-163a-5984-92c3-39bf71eb19fd
Namespace URI: http://www.w3.org/2002/07/owl# → Namespace file: !owl.md
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

All files now use UUIDv5 names. Special conventions only apply to frontmatter content:

| Element | Convention | Example |
|---------|------------|---------|
| `rdf:type` | `a` alias in wikilinks | `[[73b69787-...\|a]]` |

**External References:** All URIs (including external resources not defined in this repository) use wikilinks to UUIDv5 files: `[[uuid]]`. The target file may or may not exist - this is allowed because:
- External resources may be defined in other ontologies
- Resources can be imported incrementally
- UUIDv5 is deterministic - the same URI always produces the same UUID

### Literal Encoding Rules

Literals in YAML frontmatter follow specific encoding rules:

| Literal Type | YAML Format | Example |
|--------------|-------------|---------|
| Plain string | `"\"value\""` | `"\"Class\""` |
| Language-tagged | `"\"value\"@lang"` | `"\"Class\"@en"` |
| Typed literal | `"\"value\"^^[[uuid]]"` | `"\"2024-01-01\"^^[[xsd-date-uuid]]"` |
| Multiline | Escaped `\n` | `"\"Line1\\nLine2\"@en"` |

**Important:** CRLF (`\r\n`) is normalized to LF (`\n`) during import.

## Usage with Obsidian

### Graph View: Class Hierarchy

To visualize the class hierarchy (only anchors and `rdfs:subClassOf` relations):

```
-(["metadata":statement] -["predicate":[[55ff3aec-8d5b-5d4d-a0e1-d3f1c7d3c8d2]]]) -file:"55ff3aec-8d5b-5d4d-a0e1-d3f1c7d3c8d2"
```

This filter:
- Hides all statements EXCEPT those with `rdfs:subClassOf` predicate (UUID: `55ff3aec-...`)
- Excludes the `rdfs:subClassOf` property anchor itself

### Graph View: Clean Structure

To hide common meta-properties and focus on domain-specific relations:

```
-["metadata":statement]
-["metadata":namespace]
```

This simplified filter hides all statements and namespace declarations, showing only anchor files (resources).

For more granular control, filter by specific predicate UUIDs:
- `73b69787-81ea-563e-8e09-9c84cad4cf2b` = rdf:type
- `d0e9e696-d3f2-5966-a62f-d8358cbde741` = rdfs:label
- `da1b0b28-9c51-55c3-a963-2337006693de` = rdfs:comment
- `2e218ab8-518d-5cd0-a660-f575a101e5d8` = rdfs:isDefinedBy

### Querying Triples with Dataview

#### Basic Queries

Find all triples where a resource is the subject:

```dataview
TABLE WITHOUT ID
    link(file.link, "_") AS "_",
    subject,
    predicate,
    object
WHERE subject = [[30488677-f427-5947-8a14-02903ca20a7e]]
```

Find all triples where a resource is the object:

```dataview
TABLE WITHOUT ID
    subject,
    predicate,
    object
WHERE object = [[d6ac0df2-324e-561c-9f05-41d3b2d5ebd3]]
```

Filter by metadata type:

```dataview
LIST
WHERE metadata = "anchor"
```

#### Advanced Queries

**Find all Classes (resources with rdf:type rdfs:Class):**
```dataview
TABLE WITHOUT ID
    subject AS "Class",
    object
WHERE predicate = [[73b69787-81ea-563e-8e09-9c84cad4cf2b]]
  AND object = [[30488677-f427-5947-8a14-02903ca20a7e]]
```

**Find all Properties with their domains and ranges:**
```dataview
TABLE WITHOUT ID
    subject AS "Property",
    predicate AS "Relation",
    object AS "Value"
WHERE (predicate = [[c29ac1cb-6937-5aa2-a8c1-68f2e1b7e39f]]
    OR predicate = [[f4d4a1a9-d8e5-5f47-a2a9-c8d9e0f1a2b3]])
```

**Find all rdfs:label values:**
```dataview
TABLE WITHOUT ID
    subject AS "Resource",
    object AS "Label"
WHERE predicate = [[d0e9e696-d3f2-5966-a62f-d8358cbde741]]
  AND metadata = "statement"
```

**Find class hierarchy (rdfs:subClassOf):**
```dataview
TABLE WITHOUT ID
    subject AS "Subclass",
    object AS "Superclass"
WHERE predicate = [[55ff3aec-8d5b-5d4d-a0e1-d3f1c7d3c8d2]]
```

**Count triples by predicate:**
```dataview
TABLE WITHOUT ID
    predicate AS "Predicate",
    length(rows) AS "Count"
WHERE metadata = "statement"
GROUP BY predicate
SORT length(rows) DESC
```

**Find all resources in a namespace (by alias prefix):**
```dataview
LIST
WHERE metadata = "anchor"
  AND contains(aliases, "foaf:")
```

**Find all blank nodes:**
```dataview
LIST
WHERE metadata = "blank_node"
```

**Find owl:ObjectProperty resources:**
```dataview
TABLE WITHOUT ID
    subject AS "Property",
    object AS "Type"
WHERE predicate = [[73b69787-81ea-563e-8e09-9c84cad4cf2b]]
  AND contains(string(object), "ObjectProperty")
```

### Templates

The `~templates/` folder contains ready-to-use templates:

- **`~Statement.md`** — Template for creating new triples
- **`~(dataview) Triples.md`** — Embed in any resource to see related triples

## Examples

### RDF Triple

Original Turtle:
```turtle
rdfs:Class rdf:type rdfs:Class .
rdfs:Class rdfs:label "Class" .
rdfs:Class rdfs:subClassOf rdfs:Resource .
```

File-based representation (all UUIDv5 names):
```
rdfs/
├── 30488677-f427-5947-8a14-02903ca20a7e.md   # rdfs:Class anchor
├── a1b2c3d4-e5f6-5xxx-xxxx-xxxxxxxxxxxx.md   # Statement: Class rdf:type Class
├── b2c3d4e5-f6a7-5xxx-xxxx-xxxxxxxxxxxx.md   # Statement: Class rdfs:label "Class"
└── c3d4e5f6-a7b8-5xxx-xxxx-xxxxxxxxxxxx.md   # Statement: Class rdfs:subClassOf Resource
```

**Key UUIDs:**
| Resource | UUID |
|----------|------|
| `rdfs:Class` | `30488677-f427-5947-8a14-02903ca20a7e` |
| `rdfs:Resource` | `d6ac0df2-324e-561c-9f05-41d3b2d5ebd3` |
| `rdfs:label` | `d0e9e696-d3f2-5966-a62f-d8358cbde741` |
| `rdfs:subClassOf` | `55ff3aec-8d5b-5d4d-a0e1-d3f1c7d3c8d2` |
| `rdf:type` | `73b69787-81ea-563e-8e09-9c84cad4cf2b` |

### Cross-Namespace Reference

Statement: `owl: owl:imports rdfs:` (the OWL ontology imports RDFS)

File: `owl/{uuid}.md` where UUID = uuid5(canonical_triple)

```yaml
---
metadata: statement
subject: "[[64e92819-163a-5984-92c3-39bf71eb19fd]]"
predicate: "[[532c87f0-8cfa-5ff5-990f-aac1562178eb]]"
object: "[[1a2b3c4d-5e6f-5xxx-xxxx-xxxxxxxxxxxx]]"
---
```

Where:
- `64e92819-...` = OWL namespace
- `532c87f0-...` = owl:imports
- `1a2b3c4d-...` = RDFS namespace

### Lookup UUID by URI

Use Python to find UUID for any URI:

```python
import uuid
uri = "http://www.w3.org/2000/01/rdf-schema#label"
print(uuid.uuid5(uuid.NAMESPACE_URL, uri))
# Output: d0e9e696-d3f2-5966-a62f-d8358cbde741
```

Or use aliases in Obsidian for human-readable lookup.

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
# Validate all ontologies
python scripts/validate.py

# Validate specific namespace(s)
python scripts/validate.py dc dcterms owl

# Verbose output
python scripts/validate.py --verbose
```

The validator checks:
- **UUID filename format** — all files must have UUIDv5 names
- **External wikilinks** — references to anchors not in this repository (INFO only, not error)
- **Missing metadata** — files without `metadata` property
- **Invalid metadata** — files with incorrect metadata values
- **Orphaned anchors** — anchors not referenced in any statement
- **Orphaned blank nodes** — blank nodes not referenced in any statement
- **Frontmatter properties** — correct properties per file type

**Note:** External wikilinks (references to resources defined in other ontologies) are allowed and reported as INFO, not as errors. This enables incremental ontology import.

### Semantic Verification

Verify that file-based ontologies are semantically identical to original RDF sources:

```bash
# Verify specific ontology
python scripts/verify_import.py originals/dc.ttl dc

# Verbose output showing differences
python scripts/verify_import.py originals/owl.ttl owl -v
```

The verification script:
1. Loads triples from original RDF file
2. Loads triples from file-based representation
3. Compares both sets for semantic equivalence
4. Reports any differences

### Importing Ontologies

Convert external RDF ontologies to file-based format:

```bash
# Import from RDF/XML, Turtle, N-Triples, or other formats
python scripts/import_ontology.py <input_file> <output_dir> --prefix <prefix>

# Example: Import Dublin Core Terms
python scripts/import_ontology.py dcterms.ttl dcterms --prefix dcterms

# Verbose output
python scripts/import_ontology.py myonto.owl myonto --prefix myonto -v

# Auto-detect or specify namespace
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

**Import handling:**
- Auto-detects format from file content
- Adds `uri` field to all anchor and namespace files
- Generates human-readable `aliases` for all files
- Handles blank nodes with skolem IRIs
- Converts ALL URIs to wikilinks `[[uuid]]` (including external resources)
- Normalizes CRLF to LF in multiline literals
- Escapes all special YAML characters in literals
- Creates separate ontology anchor if ontology URI differs from namespace
- Only creates anchor files for resources in the current namespace

### Post-Import Steps

After importing, validate and verify:

```bash
# Validate the imported ontology
python scripts/validate.py <prefix>

# Verify semantic equivalence
python scripts/verify_import.py originals/<source_file> <ontology_dir>
```

## Tutorial: Importing Your Own Ontology

This guide walks you through importing a custom ontology into the file-based format.

### Step 1: Prepare Your Ontology

Ensure your ontology file is in a supported format:
- RDF/XML (`.rdf`, `.owl`)
- Turtle (`.ttl`)
- N-Triples (`.nt`)
- JSON-LD (`.jsonld`)

Place the file in the `originals/` directory:
```bash
cp ~/myontology.ttl originals/myonto.ttl
```

### Step 2: Choose a Prefix

Select a short, unique prefix for your ontology (2-8 lowercase letters):
- Good: `myonto`, `proj`, `bio`, `geo`
- Bad: `my-ontology`, `MyOntology`, `123ont`

### Step 3: Add Namespace Mapping

Edit the scripts to add your namespace. Add to all PREFIXES lists and namespace mappings:

**scripts/import_ontology.py:**
```python
NAMESPACE_URI_TO_PREFIX = {
    # ... existing entries ...
    "http://example.org/myonto#": "myonto",
}
```

**scripts/validate.py, stats.py, add_aliases.py, check_consistency.py, export_rdf.py:**
```python
PREFIXES = [
    # ... existing entries ...
    "myonto",
]
```

### Step 4: Run the Import

```bash
python scripts/import_ontology.py originals/myonto.ttl myonto --prefix myonto -v
```

**Expected output:**
```
Importing originals/myonto.ttl to myonto/
Done!
  Triples imported: 150
  Anchors created: 25
  Files created: 176
```

### Step 5: Validate

```bash
# Check structural integrity
python scripts/validate.py myonto

# Verify semantic equivalence
python scripts/verify_import.py originals/myonto.ttl myonto --namespace "http://example.org/myonto#"
```

### Step 6: Add Aliases (Optional Enhancement)

If aliases weren't generated correctly, update them:
```bash
python scripts/add_aliases.py --dry-run  # Preview
python scripts/add_aliases.py            # Apply
```

### Step 7: Open in Obsidian

1. Open your vault in Obsidian
2. Navigate to the `myonto/` folder
3. Use Graph View to explore relationships
4. Use Dataview queries to analyze triples

### Troubleshooting Import Issues

| Problem | Solution |
|---------|----------|
| "Namespace not found" | Add namespace mapping to all scripts |
| Zero triples imported | Check if namespace URI matches ontology |
| "External wikilinks" warnings | Normal - references to other ontologies |
| Parse errors | Verify RDF file is valid with `rapper -c file.ttl` |

### Advanced: Custom Import Options

**Specify namespace explicitly:**
```bash
python scripts/import_ontology.py file.owl myonto -p myonto -n "http://example.org/ns#"
```

**Import ontology with different ontology URI vs namespace:**
```bash
# The script auto-detects owl:Ontology declarations
python scripts/import_ontology.py complex.owl myonto -p myonto
```

**Re-import (update existing):**
```bash
rm -rf myonto/  # Remove old version
python scripts/import_ontology.py originals/myonto.ttl myonto -p myonto
```

### Test All Ontologies

Run comprehensive test on all ontologies:

```bash
python scripts/test_all_ontologies.py
```

This script:
1. Backs up each ontology
2. Deletes and reimports from original source
3. Validates structure
4. Verifies semantic equivalence
5. Reports results and timing

### Pre-commit Hook

Install the git hook to validate automatically before each commit:

```bash
./scripts/install-hooks.sh
```

The hook blocks commits if validation fails.

## Scripts Reference

### Core Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `import_ontology.py` | Convert RDF to file-based format | `python scripts/import_ontology.py <input> <output> -p <prefix>` |
| `validate.py` | Check structural integrity | `python scripts/validate.py [namespaces...]` |
| `verify_import.py` | Semantic equivalence check | `python scripts/verify_import.py <rdf_file> <ontology_dir>` |
| `export_rdf.py` | Export back to RDF format | `python scripts/export_rdf.py <ontology_dir> <output_file>` |
| `test_all_ontologies.py` | Comprehensive test suite | `python scripts/test_all_ontologies.py` |

### Utility Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `add_aliases.py` | Add/update human-readable aliases | `python scripts/add_aliases.py [--dry-run]` |
| `compare_ontologies.py` | Compare two ontology directories | `python scripts/compare_ontologies.py <dir1> <dir2>` |
| `stats.py` | Generate statistics for all ontologies | `python scripts/stats.py [--json]` |
| `check_consistency.py` | Cross-namespace consistency checks | `python scripts/check_consistency.py [-v]` |

### Key UUIDs Reference

Common predicate UUIDs for reference:

| Predicate | UUID |
|-----------|------|
| `rdf:type` | `73b69787-81ea-563e-8e09-9c84cad4cf2b` |
| `rdfs:label` | `d0e9e696-d3f2-5966-a62f-d8358cbde741` |
| `rdfs:comment` | `da1b0b28-9c51-55c3-a963-2337006693de` |
| `rdfs:subClassOf` | `55ff3aec-8d5b-5d4d-a0e1-d3f1c7d3c8d2` |
| `rdfs:domain` | `c29ac1cb-6937-5aa2-a8c1-68f2e1b7e39f` |
| `rdfs:range` | `f4d4a1a9-d8e5-5f47-a2a9-c8d9e0f1a2b3` |
| `rdfs:isDefinedBy` | `2e218ab8-518d-5cd0-a660-f575a101e5d8` |
| `owl:imports` | `532c87f0-8cfa-5ff5-990f-aac1562178eb` |

## Testing

Run the full test suite:

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_validate.py -v

# Run tests with coverage
python -m pytest tests/ --cov=scripts
```

### Test Categories

| Test File | Coverage |
|-----------|----------|
| `test_validate.py` | Validation functions and rules |
| `test_import_ontology.py` | Import functions and UUID generation |
| `test_stats.py` | Statistics collection and reporting |
| `test_consistency.py` | Cross-namespace consistency checks |
| `test_integration.py` | Full import → validate cycle |
| `test_export.py` | Export functions and round-trip verification |

**Total: 97 tests**

### Code Quality

```bash
# Format code with black
black scripts/

# Check with flake8
flake8 scripts/

# Type checking with mypy
mypy scripts/
```

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

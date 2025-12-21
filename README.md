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

### Verified (semantically equivalent to originals)

| Namespace | Prefix | URI | Triples | Files | Status |
|-----------|--------|-----|---------|-------|--------|
| Dublin Core Elements | `dc` | `http://purl.org/dc/elements/1.1/` | 107 | 134 | ✅ |
| Dublin Core Abstract Model | `dcam` | `http://purl.org/dc/dcam/` | 53 | 72 | ✅ |
| Dublin Core Terms | `dcterms` | `http://purl.org/dc/terms/` | 700 | 833 | ✅ |
| DOAP | `doap` | `http://usefulinc.com/ns/doap#` | 350 | 420 | ✅ |
| FOAF | `foaf` | `http://xmlns.com/foaf/0.1/` | 631 | 725 | ✅ |
| GEO | `geo` | `http://www.w3.org/2003/01/geo/wgs84_pos#` | 33 | 54 | ✅ |
| OWL 2 | `owl` | `http://www.w3.org/2002/07/owl#` | 450 | 544 | ✅ |
| PROV-O | `prov` | `http://www.w3.org/ns/prov#` | 1146 | 1343 | ✅ |
| RDF | `rdf` | `http://www.w3.org/1999/02/22-rdf-syntax-ns#` | 127 | 166 | ✅ |
| RDFS | `rdfs` | `http://www.w3.org/2000/01/rdf-schema#` | 87 | 107 | ✅ |
| SIOC | `sioc` | `http://rdfs.org/sioc/ns#` | 379 | 452 | ✅ |
| SKOS | `skos` | `http://www.w3.org/2004/02/skos/core#` | 252 | 317 | ✅ |
| TIME | `time` | `http://www.w3.org/2006/time#` | 894 | 1527 | ✅ |
| VCARD | `vcard` | `http://www.w3.org/2006/vcard/ns#` | 516 | 614 | ✅ |

**Total: 5,725+ triples — 14 ontologies**

### Additional

| Namespace | Prefix | URI | Status |
|-----------|--------|-----|--------|
| XSD | `xsd` | `http://www.w3.org/2001/XMLSchema#` | Core types only (manually created) |

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
- Result: Deterministic UUID (e.g., `11183371-dee2-5111-8d61-db2d94aa7701`)

**Example:**
```python
import uuid
uri = "http://purl.org/dc/elements/1.1/contributor"
file_uuid = uuid.uuid5(uuid.NAMESPACE_URL, uri)
# Result: 11183371-dee2-5111-8d61-db2d94aa7701
```

```
URI: http://purl.org/dc/elements/1.1/contributor
UUID: 11183371-dee2-5111-8d61-db2d94aa7701
File: dc/11183371-dee2-5111-8d61-db2d94aa7701.md
```

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

### Index Files

Each ontology directory contains `_index.md` with UUID → Label mapping for human-readable lookup:

```markdown
| UUID | Label | URI |
|------|-------|-----|
| `11183371...` | Contributor | http://purl.org/dc/elements/1.1/contributor |
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

| Element | Convention | Example |
|---------|------------|---------|
| `rdf:type` | `a` shorthand in filenames | `{subj} 73b69787...\|a {obj}.md` |
| Literal object | `___` placeholder | `{subj} {pred} ___.md` |
| Namespace file | `!{prefix}.md` | `!dc.md`, `!owl.md` |
| Blank node | `_ext{n}_` or `{prefix}!{8-char-uuid}` | `_ext1_`, `dc!a1b2c3d4` |
| Index file | `_index.md` | `dc/_index.md` |
| External URI | `<{full-uri}>` in frontmatter | `<http://example.org/ext>` |

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
# Validate all ontologies
python scripts/validate.py

# Validate specific namespace(s)
python scripts/validate.py dc dcterms owl

# Verbose output
python scripts/validate.py --verbose
```

The validator checks:
- **Broken wikilinks** — references to non-existent anchors
- **Missing metadata** — files without `metadata` property
- **Invalid metadata** — files with incorrect metadata values
- **Orphaned anchors** — anchors not referenced in any statement
- **Literal placeholder violations** — `___` used for non-literal objects
- **Blank node consistency** — blank nodes properly defined and referenced
- **UUIDv5 format** — anchor names must be valid UUIDv5 or special patterns

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
- Handles blank nodes with `_ext{n}_` naming
- Preserves external URIs as `<http://...>` references
- Normalizes CRLF to LF in multiline literals
- Escapes all special YAML characters in literals
- Creates separate ontology anchor if ontology URI differs from namespace

### Post-Import Steps

After importing, run these scripts:

```bash
# Add URI field to anchors and generate index file
python scripts/add_uri_and_index.py <ontology_dir>

# Validate the imported ontology
python scripts/validate.py <prefix>

# Verify semantic equivalence
python scripts/verify_import.py originals/<source_file> <ontology_dir>
```

### Test All Ontologies

Run comprehensive test on all ontologies:

```bash
python scripts/test_all_ontologies.py
```

This script:
1. Backs up each ontology
2. Deletes and reimports from original source
3. Adds URI and index
4. Validates structure
5. Verifies semantic equivalence
6. Reports results and timing

### Pre-commit Hook

Install the git hook to validate automatically before each commit:

```bash
./scripts/install-hooks.sh
```

The hook blocks commits if validation fails.

## Scripts Reference

| Script | Purpose | Usage |
|--------|---------|-------|
| `import_ontology.py` | Convert RDF to file-based format | `python scripts/import_ontology.py <input> <output> -p <prefix>` |
| `validate.py` | Check structural integrity | `python scripts/validate.py [namespaces...]` |
| `verify_import.py` | Semantic equivalence check | `python scripts/verify_import.py <rdf_file> <ontology_dir>` |
| `add_uri_and_index.py` | Add URI field and generate index | `python scripts/add_uri_and_index.py <ontology_dir>` |
| `migrate_to_uuid.py` | Migrate legacy names to UUIDv5 | `python scripts/migrate_to_uuid.py <directory>` |
| `test_all_ontologies.py` | Comprehensive test suite | `python scripts/test_all_ontologies.py` |

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

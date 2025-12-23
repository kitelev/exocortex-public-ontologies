# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

File-based RDF ontologies for the Exocortex knowledge management ecosystem. Converts W3C and Dublin Core ontologies into a Markdown/YAML format where each RDF triple is a separate file. This enables Obsidian graph navigation, Dataview queries, and human-readable knowledge representation.

**19 namespaces, 31,030 files, 26,794 triples** (RDF, RDFS, OWL, Dublin Core, SKOS, FOAF, PROV-O, TIME, GEO, VCARD, DOAP, SIOC, DCAT, ORG, Schema.org, XSD types, VS vocab-status).

## Commands

```bash
# Validate all ontologies (runs automatically on pre-commit)
python scripts/validate.py

# Validate specific namespace(s)
python scripts/validate.py dc dcterms owl

# Import RDF ontology to file-based format
python scripts/import_ontology.py <input_file> <output_dir> --prefix <prefix>
# Example: python scripts/import_ontology.py originals/foaf.rdf foaf --prefix foaf

# Verify semantic equivalence after import
python scripts/verify_import.py originals/<source_file> <ontology_dir>

# Export back to RDF format
python scripts/export_rdf.py <ontology_dir> <output_file>

# Add/update human-readable aliases
python scripts/add_aliases.py [--dry-run]

# Test all ontologies (backup, reimport, validate, verify)
python scripts/test_all_ontologies.py

# Install pre-commit validation hook
./scripts/install-hooks.sh

# Generate statistics report
python scripts/stats.py [--json]
```

## Architecture

### File Types (by `metadata` property)

| Type | Purpose | Required Properties |
|------|---------|---------------------|
| `namespace` | Namespace declaration | `metadata`, `uri`, `aliases` |
| `anchor` | Resource anchor point for wikilinks | `metadata`, `aliases` (+ optional `uri`) |
| `statement` | RDF triple | `metadata`, `subject`, `predicate`, `object`, `aliases` |
| `blank_node` | Blank node anchor | `metadata`, `uri`, `aliases` |

**Note:** `aliases` is MANDATORY for all file types (enforced by pre-commit hook).

### UUID Naming Convention

**All files use UUIDv5 names** derived from the URL namespace (`6ba7b811-9dad-11d1-80b4-00c04fd430c8`):

```python
import uuid

# Namespace file: uuid5 of namespace URI
uuid.uuid5(uuid.NAMESPACE_URL, "http://www.w3.org/1999/02/22-rdf-syntax-ns#")

# Anchor file: uuid5 of full resource URI
uuid.uuid5(uuid.NAMESPACE_URL, "http://www.w3.org/2000/01/rdf-schema#Class")

# Statement file: uuid5 of canonical triple format
canonical = "{subject_uri}|{predicate_uri}|{object_canonical}"
uuid.uuid5(uuid.NAMESPACE_URL, canonical)
```

### Directory Structure

Each namespace has its own directory (`rdf/`, `rdfs/`, `owl/`, `dc/`, etc.). Files within directories:
- One namespace file per directory
- Anchor files for resources defined in that namespace
- Statement files for triples where the subject belongs to that namespace

### Wikilink Format

All URI references use wikilinks to UUIDv5 files: `[[uuid]]` or `[[uuid|alias]]`. References to external ontologies are allowed (reported as INFO during validation, not errors).

### Key UUIDs (Common Predicates)

| Predicate | UUID |
|-----------|------|
| `rdf:type` | `73b69787-81ea-563e-8e09-9c84cad4cf2b` |
| `rdfs:label` | `d0e9e696-d3f2-5966-a62f-d8358cbde741` |
| `rdfs:comment` | `da1b0b28-9c51-55c3-a963-2337006693de` |
| `rdfs:subClassOf` | `55ff3aec-8d5b-5d4d-a0e1-d3f1c7d3c8d2` |
| `rdfs:subPropertyOf` | `c6a11966-a018-5be8-95a0-eba182c2fd93` |
| `rdfs:domain` | `6f6b4f67-c31d-5673-9863-ee0c1d7f3bb8` |
| `rdfs:range` | `8bf79888-4cd0-5acb-b5e3-8542f0a5c186` |
| `rdfs:isDefinedBy` | `2e218ab8-518d-5cd0-a660-f575a101e5d8` |
| `owl:imports` | `532c87f0-8cfa-5ff5-990f-aac1562178eb` |
| `vs:term_status` | `eaf1f83f-cee8-50df-869f-f905aa65153c` |

### Key UUIDs (XSD Datatypes)

| Datatype | UUID |
|----------|------|
| `xsd:string` | `936caa86-c233-5829-b9ec-ad6eb152c274` |
| `xsd:boolean` | `32c0d57e-f209-5eee-bcbe-45500c2fe63e` |
| `xsd:integer` | `94277b3a-2e5b-5b33-942f-6b57e6bd7ea7` |
| `xsd:decimal` | `48ed5b9d-eb3c-5c34-9213-5d8ae41ecd98` |
| `xsd:date` | `f9e4597b-3986-557b-9b9e-781d6599bcf5` |
| `xsd:dateTime` | `80d96c2d-b5b7-5475-a992-c19bd5880707` |
| `xsd:anyURI` | `762b4689-bb72-5ab1-82fb-fcfc4504ee49` |
| `xsd:nonNegativeInteger` | `9fe714fa-e171-5cf2-bd85-711174ad070a` |

## Validation Rules

The validator (`scripts/validate.py`) checks:
- UUID filename format for all files
- Required frontmatter properties per file type
- **Mandatory aliases** for all files (human-readable navigation)
- Orphaned anchors (not referenced in any statement)
- Orphaned blank nodes
- Missing or invalid `metadata` values
- No body content (only frontmatter allowed)

External wikilinks (references to other ontologies) are INFO-level, not errors.

## Alias Formats

| File Type | Alias Format | Example |
|-----------|--------------|---------|
| Namespace | `!prefix` | `!rdf`, `!owl` |
| Anchor | `prefix:localname` | `rdfs:Class`, `owl:Thing` |
| Blank node | `_:genid-{short_id}` | `_:genid-d3e1d976` |
| Statement | `{subj} {pred} {obj}` | `rdfs:Class a rdfs:Class` |

## Literal Encoding

Literals in YAML frontmatter:
- Plain: `"\"value\""`
- Language-tagged: `"\"value\"@en"`
- Typed: `"\"value\"^^[[xsd-type-uuid]]"`
- Multiline: `\n` (CRLF normalized to LF during import)

## Import Workflow

1. **Download** original ontology (RDF/XML, Turtle, etc.) to `originals/`
2. **Import**: `python scripts/import_ontology.py originals/onto.rdf onto --prefix onto`
3. **Verify**: `python scripts/verify_import.py originals/onto.rdf onto`
4. **Add to scripts**: Update PREFIXES in `validate.py`, `add_aliases.py`, `import_ontology.py`
5. **Validate**: `python scripts/validate.py onto`
6. **Commit**: `git add -A && git commit -m "feat: add onto ontology"`

## Dependencies

Python with `rdflib` for import/export scripts:
```bash
pip install rdflib
```

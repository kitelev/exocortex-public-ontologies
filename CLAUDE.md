# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

File-based RDF ontologies for the Exocortex knowledge management ecosystem. Converts W3C and Dublin Core ontologies into a Markdown/YAML format where each RDF triple is a separate file. This enables Obsidian graph navigation, Dataview queries, and human-readable knowledge representation.

**17 verified ontologies, 26,794 triples total** (RDF, RDFS, OWL, Dublin Core, SKOS, FOAF, PROV-O, TIME, GEO, VCARD, DOAP, SIOC, DCAT, ORG, Schema.org, plus XSD core types).

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
```

## Architecture

### File Types (by `metadata` property)

| Type | Purpose | Required Properties |
|------|---------|---------------------|
| `namespace` | Namespace declaration | `metadata`, `uri` |
| `anchor` | Resource anchor point for wikilinks | `metadata` (+ optional `uri`, `aliases`) |
| `statement` | RDF triple | `metadata`, `subject`, `predicate`, `object` |
| `blank_node` | Blank node anchor | `metadata`, `uri` |

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
| `rdfs:isDefinedBy` | `2e218ab8-518d-5cd0-a660-f575a101e5d8` |

## Validation Rules

The validator (`scripts/validate.py`) checks:
- UUID filename format for all files
- Required frontmatter properties per file type
- Orphaned anchors (not referenced in any statement)
- Orphaned blank nodes
- Missing or invalid `metadata` values

External wikilinks (references to other ontologies) are INFO-level, not errors.

## Literal Encoding

Literals in YAML frontmatter:
- Plain: `"\"value\""`
- Language-tagged: `"\"value\"@en"`
- Typed: `"\"value\"^^[[xsd-type-uuid]]"`
- Multiline: `\n` (CRLF normalized to LF during import)

## Dependencies

Python with `rdflib` for import/export scripts:
```bash
pip install rdflib
```

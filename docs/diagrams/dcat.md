# DCAT Ontology Diagram

UML-style class diagram for the **dcat** namespace.

*Generated automatically. Classes: 9, Properties: 28*

**Legend:**
- `<|--` Inheritance (rdfs:subClassOf)
- `-->` Object Property
- `..>` Datatype Property

```mermaid
classDiagram
    class dcterms_MediaType
    class skos_Concept
    class _051921fa
    class dcat_Catalog
    class dcat_CatalogRecord
    class dcat_DataService
    class dcat_Dataset
    class dcat_Distribution
    class dcat_Relationship
    class dcat_Resource
    class dcat_Role
    dcat_Resource <|-- dcat_DataService
    _051921fa <|-- dcat_DataService
    skos_Concept <|-- dcat_Role
    dcat_Resource <|-- dcat_Dataset
    dcat_Dataset <|-- dcat_Catalog
    dcat_Distribution --> dcterms_MediaType : dcat:packageFormat
```

## Statistics

| Metric | Count |
|--------|-------|
| Classes | 9 |
| Properties | 28 |
| Inheritance relationships | 7 |
| Properties with domain | 7 |
| Properties with range | 9 |

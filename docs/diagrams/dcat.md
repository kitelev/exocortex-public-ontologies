# DCAT Ontology Diagram

UML-style class diagram for the **dcat** namespace.

*Generated automatically. Classes: 8, Properties: 28*

**Legend:**
- `<|--` Inheritance (rdfs:subClassOf)
- `-->` Object Property (owl:ObjectProperty)
- `..>` Datatype Property (owl:DatatypeProperty)

```mermaid
classDiagram
    class _4e232b4c
    class dcterms_Location
    class dcterms_PeriodOfTime
    class rdfs_Resource
    class rdfs_Literal
    class dcterms_MediaType
    class skos_Concept
    class _1238c9c5
    class _51bb0e06
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
    _51bb0e06 <|-- dcat_CatalogRecord
    _1238c9c5 <|-- dcat_CatalogRecord
    skos_Concept <|-- dcat_Role
    dcat_Resource <|-- dcat_Dataset
    dcat_Dataset <|-- dcat_Catalog
    dcat_Distribution --> dcterms_MediaType : dcat:packageFormat
    dcat_Catalog --> dcat_CatalogRecord : dcat:record
    dcat_Distribution ..> rdfs_Literal : dcat:byteSize
    dcat_Catalog --> dcat_DataService : dcat:service
    dcat_Distribution --> rdfs_Resource : dcat:downloadURL
    dcat_Distribution --> dcterms_MediaType : dcat:compressFormat
    dcat_DataService --> dcat_Dataset : dcat:servesDataset
    dcat_Catalog --> dcat_Catalog : dcat:catalog
    dcat_DataService --> rdfs_Resource : dcat:endpointURL
    dcat_Resource --> dcat_Relationship : dcat:qualifiedRelation
    _4e232b4c --> dcat_Role : dcat:hadRole
```

## Statistics

| Metric | Count |
|--------|-------|
| Classes | 8 |
| Properties | 28 |
| Inheritance relationships | 7 |
| Properties with domain | 21 |
| Properties with range | 27 |

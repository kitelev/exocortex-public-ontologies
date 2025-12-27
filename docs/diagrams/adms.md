# ADMS Ontology Diagram

UML-style class diagram for the **adms** namespace.

*Generated automatically. Classes: 4, Properties: 13*

**Legend:**
- `<|--` Inheritance (rdfs:subClassOf)
- `-->` Object Property
- `..>` Datatype Property

```mermaid
classDiagram
    class dcat_Distribution
    class dcat_Dataset
    class dcat_Catalog
    class adms_Asset
    class adms_AssetDistribution
    class adms_AssetRepository
    class adms_Identifier
    dcat_Catalog <|-- adms_AssetRepository
    dcat_Dataset <|-- adms_Asset
    dcat_Distribution <|-- adms_AssetDistribution
    adms_Asset ..> adms_Asset : adms:sample
```

## Statistics

| Metric | Count |
|--------|-------|
| Classes | 4 |
| Properties | 13 |
| Inheritance relationships | 3 |
| Properties with domain | 1 |
| Properties with range | 3 |

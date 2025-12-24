# RDF Ontology Diagram

UML-style class diagram for the **rdf** namespace.

*Generated automatically. Classes: 7, Properties: 9*

**Legend:**
- `<|--` Inheritance (rdfs:subClassOf)
- `-->` Object Property
- `..>` Datatype Property

```mermaid
classDiagram
    class rdfs_Container
    class rdfs_Resource
    class rdf_Alt
    class rdf_Bag
    class rdf_CompoundLiteral
    class rdf_List
    class rdf_Property
    class rdf_Seq
    class rdf_Statement
    rdfs_Resource <|-- rdf_List
    rdfs_Resource <|-- rdf_Statement
    rdfs_Resource <|-- rdf_CompoundLiteral
    rdfs_Resource <|-- rdf_Property
    rdfs_Container <|-- rdf_Alt
    rdfs_Container <|-- rdf_Seq
    rdfs_Container <|-- rdf_Bag
    rdf_List ..> rdfs_Resource : rdf:first
    rdf_Statement ..> rdfs_Resource : rdf:object
    rdf_List ..> rdf_List : rdf:rest
```

## Statistics

| Metric | Count |
|--------|-------|
| Classes | 7 |
| Properties | 9 |
| Inheritance relationships | 12 |
| Properties with domain | 3 |
| Properties with range | 6 |

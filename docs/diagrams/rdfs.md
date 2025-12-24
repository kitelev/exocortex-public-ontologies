# RDFS Ontology Diagram

UML-style class diagram for the **rdfs** namespace.

*Generated automatically. Classes: 6, Properties: 9*

**Legend:**
- `<|--` Inheritance (rdfs:subClassOf)
- `-->` Object Property
- `..>` Datatype Property

```mermaid
classDiagram
    class rdf_Property
    class rdfs_Class
    class rdfs_Container
    class rdfs_ContainerMembershipProperty
    class rdfs_Datatype
    class rdfs_Literal
    class rdfs_Resource
    rdf_Property <|-- rdfs_ContainerMembershipProperty
    rdfs_Resource <|-- rdfs_Container
    rdfs_Class <|-- rdfs_Datatype
    rdfs_Resource <|-- rdfs_Class
    rdfs_Resource <|-- rdfs_Literal
    rdfs_Resource ..> rdfs_Literal : rdfs:comment
```

## Statistics

| Metric | Count |
|--------|-------|
| Classes | 6 |
| Properties | 9 |
| Inheritance relationships | 5 |
| Properties with domain | 3 |
| Properties with range | 4 |

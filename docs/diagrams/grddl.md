# GRDDL Ontology Diagram

UML-style class diagram for the **grddl** namespace.

*Generated automatically. Classes: 5, Properties: 4*

**Legend:**
- `<|--` Inheritance (rdfs:subClassOf)
- `-->` Object Property
- `..>` Datatype Property

```mermaid
classDiagram
    class owl_FunctionalProperty
    class grddl_InformationResource
    class grddl_RDFGraph
    class grddl_RootNode
    class grddl_Transformation
    class grddl_TransformationProperty
    owl_FunctionalProperty <|-- grddl_TransformationProperty
    grddl_InformationResource <|-- grddl_Transformation
    grddl_RootNode ..> grddl_Transformation : grddl:transformation
```

## Statistics

| Metric | Count |
|--------|-------|
| Classes | 5 |
| Properties | 4 |
| Inheritance relationships | 2 |
| Properties with domain | 1 |
| Properties with range | 1 |

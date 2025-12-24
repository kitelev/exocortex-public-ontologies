# OWL Ontology Diagram

UML-style class diagram for the **owl** namespace.

*Generated automatically. Classes: 26, Properties: 49*

**Legend:**
- `<|--` Inheritance (rdfs:subClassOf)
- `-->` Object Property
- `..>` Datatype Property

```mermaid
classDiagram
    class rdfs_Literal
    class rdf_List
    class rdfs_Class
    class rdfs_Datatype
    class rdf_Property
    class rdfs_Resource
    class owl_AllDifferent
    class owl_AllDisjointClasses
    class owl_AllDisjointProperties
    class owl_Annotation
    class owl_AnnotationProperty
    class owl_AsymmetricProperty
    class owl_Axiom
    class owl_Class
    class owl_DataRange
    class owl_DatatypeProperty
    class owl_DeprecatedClass
    class owl_DeprecatedProperty
    class owl_FunctionalProperty
    class owl_InverseFunctionalProperty
    class owl_IrreflexiveProperty
    class owl_NamedIndividual
    class owl_NegativePropertyAssertion
    class owl_Nothing
    class owl_ObjectProperty
    class owl_Ontology
    class owl_OntologyProperty
    class owl_ReflexiveProperty
    class owl_Restriction
    class owl_SymmetricProperty
    class owl_Thing
    class owl_TransitiveProperty
    owl_ObjectProperty <|-- owl_ReflexiveProperty
    rdfs_Resource <|-- owl_Annotation
    rdf_Property <|-- owl_OntologyProperty
    rdfs_Resource <|-- owl_AllDifferent
    rdfs_Datatype <|-- owl_DataRange
    rdf_Property <|-- owl_FunctionalProperty
    rdfs_Class <|-- owl_Class
    owl_Class <|-- owl_Restriction
    rdfs_Resource <|-- owl_AllDisjointClasses
    rdfs_Class <|-- owl_DeprecatedClass
    owl_ObjectProperty <|-- owl_TransitiveProperty
    rdfs_Resource <|-- owl_Ontology
    rdf_Property <|-- owl_DatatypeProperty
    owl_ObjectProperty <|-- owl_SymmetricProperty
    owl_ObjectProperty <|-- owl_IrreflexiveProperty
    rdfs_Resource <|-- owl_NegativePropertyAssertion
    rdf_Property <|-- owl_DeprecatedProperty
    owl_ObjectProperty <|-- owl_InverseFunctionalProperty
    rdf_Property <|-- owl_ObjectProperty
    owl_ObjectProperty <|-- owl_AsymmetricProperty
    rdfs_Resource <|-- owl_AllDisjointProperties
    rdfs_Resource <|-- owl_Axiom
    owl_Thing <|-- owl_NamedIndividual
    owl_Thing <|-- owl_Nothing
    rdf_Property <|-- owl_AnnotationProperty
    rdf_Property ..> rdf_Property : owl:propertyDisjointWith
    owl_Thing --> owl_Thing : owl:topObjectProperty
    owl_Ontology ..> owl_Ontology : owl:priorVersion
    owl_Restriction ..> rdfs_Class : owl:someValuesFrom
    rdfs_Class ..> rdf_List : owl:oneOf
    owl_NegativePropertyAssertion ..> rdf_Property : owl:assertionProperty
    owl_Thing ..> rdfs_Literal : owl:bottomDataProperty
    rdfs_Resource ..> rdfs_Resource : owl:annotatedSource
    owl_Restriction ..> rdf_List : owl:onProperties
    rdfs_Resource ..> rdfs_Resource : owl:annotatedTarget
    rdfs_Resource ..> rdf_List : owl:members
```

## Statistics

| Metric | Count |
|--------|-------|
| Classes | 26 |
| Properties | 49 |
| Inheritance relationships | 25 |
| Properties with domain | 23 |
| Properties with range | 24 |

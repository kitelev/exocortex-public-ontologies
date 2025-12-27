# SH Ontology Diagram

UML-style class diagram for the **sh** namespace.

*Generated automatically. Classes: 40, Properties: 101*

**Legend:**
- `<|--` Inheritance (rdfs:subClassOf)
- `-->` Object Property
- `..>` Datatype Property

```mermaid
classDiagram
    class owl_Ontology
    class rdf_Property
    class xsd_boolean
    class xsd_anyURI
    class xsd_string
    class rdfs_Class
    class rdfs_Resource
    class sh_AbstractResult
    class sh_ConstraintComponent
    class sh_Function
    class sh_JSConstraint
    class sh_JSExecutable
    class sh_JSFunction
    class sh_JSLibrary
    class sh_JSRule
    class sh_JSTarget
    class sh_JSTargetType
    class sh_JSValidator
    class sh_NodeKind
    class sh_NodeShape
    class sh_Parameter
    class sh_Parameterizable
    class sh_PrefixDeclaration
    class sh_PropertyGroup
    class sh_PropertyShape
    class sh_ResultAnnotation
    class sh_Rule
    class sh_Severity
    class sh_Shape
    class sh_SPARQLAskExecutable
    class sh_SPARQLAskValidator
    class sh_SPARQLConstraint
    class sh_SPARQLConstructExecutable
    class sh_SPARQLExecutable
    class sh_SPARQLFunction
    class sh_SPARQLRule
    class sh_SPARQLSelectExecutable
    class sh_SPARQLSelectValidator
    class sh_SPARQLTarget
    class sh_SPARQLTargetType
    class sh_SPARQLUpdateExecutable
    class sh_Target
    class sh_TargetType
    class sh_TripleRule
    class sh_ValidationReport
    class sh_ValidationResult
    class sh_Validator
    rdfs_Resource <|-- sh_ResultAnnotation
    sh_SPARQLSelectExecutable <|-- sh_SPARQLTargetType
    sh_SPARQLAskExecutable <|-- sh_SPARQLTargetType
    sh_TargetType <|-- sh_SPARQLTargetType
    sh_Parameterizable <|-- sh_ConstraintComponent
    sh_Validator <|-- sh_SPARQLSelectValidator
    sh_SPARQLSelectExecutable <|-- sh_SPARQLSelectValidator
    sh_SPARQLExecutable <|-- sh_SPARQLSelectExecutable
    sh_Rule <|-- sh_TripleRule
    rdfs_Resource <|-- sh_Shape
    sh_Parameterizable <|-- sh_TargetType
    rdfs_Class <|-- sh_TargetType
    rdfs_Resource <|-- sh_ValidationReport
    sh_SPARQLExecutable <|-- sh_SPARQLConstructExecutable
    sh_JSExecutable <|-- sh_JSTargetType
    sh_TargetType <|-- sh_JSTargetType
    sh_Shape <|-- sh_NodeShape
    rdfs_Resource <|-- sh_PropertyGroup
    rdfs_Resource <|-- sh_AbstractResult
    sh_SPARQLExecutable <|-- sh_SPARQLUpdateExecutable
    rdfs_Resource <|-- sh_Target
    sh_JSExecutable <|-- sh_JSTarget
    sh_Target <|-- sh_JSTarget
    sh_Parameterizable <|-- sh_Function
    rdfs_Resource <|-- sh_Validator
    sh_JSExecutable <|-- sh_JSConstraint
    sh_SPARQLSelectExecutable <|-- sh_SPARQLTarget
    sh_SPARQLAskExecutable <|-- sh_SPARQLTarget
    sh_Target <|-- sh_SPARQLTarget
    rdfs_Resource <|-- sh_Rule
    sh_SPARQLExecutable <|-- sh_SPARQLAskExecutable
    sh_SPARQLConstructExecutable <|-- sh_SPARQLRule
    sh_Rule <|-- sh_SPARQLRule
    sh_JSExecutable <|-- sh_JSValidator
    sh_Validator <|-- sh_JSValidator
    sh_JSExecutable <|-- sh_JSFunction
    sh_Function <|-- sh_JSFunction
    sh_JSExecutable <|-- sh_JSRule
    sh_Rule <|-- sh_JSRule
    sh_Shape <|-- sh_PropertyShape
    sh_SPARQLSelectExecutable <|-- sh_SPARQLConstraint
    rdfs_Resource <|-- sh_SPARQLExecutable
    sh_SPARQLAskExecutable <|-- sh_SPARQLFunction
    sh_SPARQLSelectExecutable <|-- sh_SPARQLFunction
    sh_Function <|-- sh_SPARQLFunction
    rdfs_Resource <|-- sh_JSExecutable
    rdfs_Resource <|-- sh_PrefixDeclaration
    rdfs_Resource <|-- sh_JSLibrary
    rdfs_Resource <|-- sh_Severity
    sh_AbstractResult <|-- sh_ValidationResult
    rdfs_Resource <|-- sh_NodeKind
    sh_Validator <|-- sh_SPARQLAskValidator
    sh_SPARQLAskExecutable <|-- sh_SPARQLAskValidator
    rdfs_Resource <|-- sh_Parameterizable
    sh_PropertyShape <|-- sh_Parameter
    sh_PrefixDeclaration ..> xsd_string : sh:prefix
    sh_AbstractResult ..> sh_Severity : sh:resultSeverity
    sh_ValidationReport ..> sh_ValidationResult : sh:result
    sh_AbstractResult ..> rdfs_Resource : sh:resultPath
    sh_PrefixDeclaration ..> xsd_anyURI : sh:namespace
    sh_Shape ..> sh_Target : sh:target
    sh_Shape ..> sh_PropertyShape : sh:property
    sh_AbstractResult ..> sh_AbstractResult : sh:detail
    sh_ValidationReport ..> xsd_boolean : sh:shapesGraphWellFormed
    sh_Shape ..> rdf_Property : sh:targetSubjectsOf
    sh_Shape ..> sh_Rule : sh:rule
    sh_Rule ..> sh_Shape : sh:condition
    owl_Ontology ..> rdfs_Resource : sh:entailment
    sh_Shape ..> rdf_Property : sh:targetObjectsOf
    sh_SPARQLConstructExecutable ..> xsd_string : sh:construct
    owl_Ontology ..> owl_Ontology : sh:shapesGraph
    sh_ConstraintComponent ..> sh_Validator : sh:nodeValidator
    sh_ResultAnnotation ..> xsd_string : sh:annotationVarName
    sh_PropertyShape ..> sh_PropertyGroup : sh:group
```

## Statistics

| Metric | Count |
|--------|-------|
| Classes | 40 |
| Properties | 101 |
| Inheritance relationships | 55 |
| Properties with domain | 25 |
| Properties with range | 47 |

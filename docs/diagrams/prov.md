# PROV Ontology Diagram

UML-style class diagram for the **prov** namespace.

*Generated automatically. Classes: 38, Properties: 65*

**Legend:**
- `<|--` Inheritance (rdfs:subClassOf)
- `-->` Object Property
- `..>` Datatype Property

```mermaid
classDiagram
    class xsd_dateTime
    class b1791eb1
    class _08e29461
    class _16f92030
    class _2e97a557
    class _54ca8a65
    class _5df0710c
    class _8231af0e
    class e675e13f
    class efdc0db0
    class prov_Activity
    class prov_ActivityInfluence
    class prov_Agent
    class prov_AgentInfluence
    class prov_Association
    class prov_Attribution
    class prov_Bundle
    class prov_Collection
    class prov_Communication
    class prov_Delegation
    class prov_Derivation
    class prov_EmptyCollection
    class prov_End
    class prov_Entity
    class prov_EntityInfluence
    class prov_Generation
    class prov_Influence
    class prov_InstantaneousEvent
    class prov_Invalidation
    class prov_Location
    class prov_Organization
    class prov_Person
    class prov_Plan
    class prov_PrimarySource
    class prov_Quotation
    class prov_Revision
    class prov_Role
    class prov_SoftwareAgent
    class prov_Start
    class prov_Usage
    prov_Agent <|-- prov_Person
    prov_Entity <|-- prov_Collection
    prov_Agent <|-- prov_Organization
    prov_ActivityInfluence <|-- prov_Invalidation
    prov_InstantaneousEvent <|-- prov_Invalidation
    prov_ActivityInfluence <|-- prov_Generation
    prov_InstantaneousEvent <|-- prov_Generation
    prov_Entity <|-- prov_Plan
    prov_Agent <|-- prov_SoftwareAgent
    prov_EntityInfluence <|-- prov_End
    prov_InstantaneousEvent <|-- prov_End
    prov_Derivation <|-- prov_PrimarySource
    prov_Derivation <|-- prov_Revision
    prov_EntityInfluence <|-- prov_Usage
    prov_InstantaneousEvent <|-- prov_Usage
    prov_Derivation <|-- prov_Quotation
    prov_EntityInfluence <|-- prov_Start
    prov_InstantaneousEvent <|-- prov_Start
    prov_Collection <|-- prov_EmptyCollection
    prov_AgentInfluence <|-- prov_Delegation
    prov_EntityInfluence <|-- prov_Derivation
    prov_AgentInfluence <|-- prov_Attribution
    prov_Influence <|-- prov_ActivityInfluence
    b1791eb1 <|-- prov_ActivityInfluence
    prov_Entity <|-- prov_Bundle
    prov_Influence <|-- prov_EntityInfluence
    prov_AgentInfluence <|-- prov_Association
    prov_Influence <|-- prov_AgentInfluence
    prov_ActivityInfluence <|-- prov_Communication
    prov_Activity ..> xsd_dateTime : prov:startedAtTime
    _08e29461 --> prov_Role : prov:hadRole
    efdc0db0 --> prov_Location : prov:atLocation
    _54ca8a65 --> prov_Influence : prov:qualifiedInfluence
    prov_Entity --> prov_Entity : prov:hadPrimarySource
    prov_Entity --> prov_Agent : prov:wasAttributedTo
    prov_Entity ..> xsd_dateTime : prov:generatedAtTime
    prov_Entity --> prov_Entity : prov:wasDerivedFrom
    prov_Entity --> prov_Revision : prov:qualifiedRevision
    prov_InstantaneousEvent ..> xsd_dateTime : prov:atTime
    prov_Entity ..> xsd_dateTime : prov:invalidatedAtTime
    prov_Entity --> prov_Invalidation : prov:qualifiedInvalidation
    prov_Activity --> prov_Communication : prov:qualifiedCommunication
```

## Statistics

| Metric | Count |
|--------|-------|
| Classes | 38 |
| Properties | 65 |
| Inheritance relationships | 29 |
| Properties with domain | 21 |
| Properties with range | 18 |

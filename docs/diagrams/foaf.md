# FOAF Ontology Diagram

UML-style class diagram for the **foaf** namespace.

*Generated automatically. Classes: 13, Properties: 62*

**Legend:**
- `<|--` Inheritance (rdfs:subClassOf)
- `-->` Object Property
- `..>` Datatype Property

```mermaid
classDiagram
    class rdfs_Literal
    class geo_SpatialThing
    class owl_Thing
    class foaf_Agent
    class foaf_Document
    class foaf_Group
    class foaf_Image
    class foaf_LabelProperty
    class foaf_OnlineAccount
    class foaf_OnlineChatAccount
    class foaf_OnlineEcommerceAccount
    class foaf_OnlineGamingAccount
    class foaf_Organization
    class foaf_Person
    class foaf_PersonalProfileDocument
    class foaf_Project
    foaf_OnlineAccount <|-- foaf_OnlineEcommerceAccount
    foaf_Agent <|-- foaf_Organization
    foaf_OnlineAccount <|-- foaf_OnlineGamingAccount
    owl_Thing <|-- foaf_OnlineAccount
    foaf_Document <|-- foaf_PersonalProfileDocument
    geo_SpatialThing <|-- foaf_Person
    foaf_Agent <|-- foaf_Person
    foaf_OnlineAccount <|-- foaf_OnlineChatAccount
    foaf_Document <|-- foaf_Image
    foaf_Agent <|-- foaf_Group
    foaf_Person ..> rdfs_Literal : foaf:lastName
    foaf_Agent --> foaf_OnlineAccount : foaf:account
    owl_Thing ..> rdfs_Literal : foaf:name
    foaf_Agent --> foaf_OnlineAccount : foaf:holdsAccount
    foaf_Agent --> foaf_Document : foaf:weblog
```

## Statistics

| Metric | Count |
|--------|-------|
| Classes | 13 |
| Properties | 62 |
| Inheritance relationships | 10 |
| Properties with domain | 15 |
| Properties with range | 20 |

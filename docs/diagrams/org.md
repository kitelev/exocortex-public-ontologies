# ORG Ontology Diagram

UML-style class diagram for the **org** namespace.

*Generated automatically. Classes: 13, Properties: 35*

**Legend:**
- `<|--` Inheritance (rdfs:subClassOf)
- `-->` Object Property
- `..>` Datatype Property

```mermaid
classDiagram
    class foaf_Organization
    class prov_Activity
    class foaf_Agent
    class skos_Concept
    class _1e931111
    class _2c962624
    class _7874a001
    class a3331a7e
    class org_ChangeEvent
    class org_FormalOrganization
    class org_Membership
    class org_Organization
    class org_OrganizationalCollaboration
    class org_OrganizationalUnit
    class org_Post
    class org_Role
    class org_Site
    skos_Concept <|-- org_Role
    org_Organization <|-- org_OrganizationalCollaboration
    foaf_Agent <|-- org_Organization
    prov_Activity <|-- org_ChangeEvent
    org_Organization <|-- org_FormalOrganization
    foaf_Organization <|-- org_FormalOrganization
    org_Organization <|-- org_OrganizationalUnit
    foaf_Agent ..> org_Organization : org:headOf
    org_Organization ..> foaf_Agent : org:hasMember
```

## Statistics

| Metric | Count |
|--------|-------|
| Classes | 13 |
| Properties | 35 |
| Inheritance relationships | 7 |
| Properties with domain | 6 |
| Properties with range | 10 |

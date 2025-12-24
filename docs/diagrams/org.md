# ORG Ontology Diagram

UML-style class diagram for the **org** namespace.

*Generated automatically. Classes: 9, Properties: 35*

**Legend:**
- `<|--` Inheritance (rdfs:subClassOf)
- `-->` Object Property (owl:ObjectProperty)
- `..>` Datatype Property (owl:DatatypeProperty)

```mermaid
classDiagram
    class rdf_Property
    class xsd_string
    class _1e931111
    class foaf_Person
    class foaf_Organization
    class prov_Activity
    class foaf_Agent
    class skos_Concept
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
    org_Organization --> org_Organization : org:hasSubOrganization
    org_Organization --> org_Site : org:hasPrimarySite
    _1e931111 --> org_Role : org:role
    foaf_Person ..> xsd_string : org:location
    org_Organization --> org_ChangeEvent : org:resultedFrom
    org_Organization --> org_Organization : org:linkedTo
    org_OrganizationalUnit --> org_FormalOrganization : org:unitOf
    org_Membership --> org_Organization : org:organization
```

## Statistics

| Metric | Count |
|--------|-------|
| Classes | 9 |
| Properties | 35 |
| Inheritance relationships | 7 |
| Properties with domain | 35 |
| Properties with range | 30 |

# VCARD Ontology Diagram

UML-style class diagram for the **vcard** namespace.

*Generated automatically. Classes: 75, Properties: 84*

**Legend:**
- `<|--` Inheritance (rdfs:subClassOf)
- `-->` Object Property
- `..>` Datatype Property

```mermaid
classDiagram
    class vcard_RelatedType
    class vcard_TelephoneType
    class vcard_Type
    class _0fe2bd43
    class _1e8f15a8
    class _27a61271
    class _27fdff12
    class _5ca151b2
    class _92b55bff
    class _9882b74c
    class _9d9c42b2
    class _9de50819
    class afabe2fd
    class bd3511ac
    class d1db992f
    class e6fb0d42
    class vcard_Acquaintance
    class vcard_Address
    class vcard_Agent
    class vcard_BBS
    class vcard_Car
    class vcard_Cell
    class vcard_Child
    class vcard_Colleague
    class vcard_Contact
    class vcard_Coresident
    class vcard_Coworker
    class vcard_Crush
    class vcard_Date
    class vcard_Dom
    class vcard_Email
    class vcard_Emergency
    class vcard_Fax
    class vcard_Female
    class vcard_Friend
    class vcard_Gender
    class vcard_Group
    class vcard_Home
    class vcard_Individual
    class vcard_Internet
    class vcard_Intl
    class vcard_ISDN
    class vcard_Kin
    class vcard_Kind
    class vcard_Label
    class vcard_Location
    class vcard_Male
    class vcard_Me
    class vcard_Met
    class vcard_Modem
    class vcard_Msg
    class vcard_Muse
    class vcard_Name
    vcard_Type <|-- vcard_Internet
    vcard_Type <|-- vcard_Label
    vcard_Type <|-- vcard_Intl
    vcard_TelephoneType <|-- vcard_BBS
    vcard_RelatedType <|-- vcard_Crush
    vcard_RelatedType <|-- vcard_Met
    vcard_TelephoneType <|-- vcard_Msg
    vcard_TelephoneType <|-- vcard_Car
    vcard_Type <|-- vcard_Home
    vcard_TelephoneType <|-- vcard_Cell
    vcard_RelatedType <|-- vcard_Colleague
    vcard_Kind <|-- vcard_Individual
    vcard_RelatedType <|-- vcard_Date
    vcard_Gender <|-- vcard_Female
    vcard_RelatedType <|-- vcard_Muse
    vcard_RelatedType <|-- vcard_Emergency
    vcard_RelatedType <|-- vcard_Child
    vcard_Kind <|-- vcard_Group
    vcard_TelephoneType <|-- vcard_Fax
    vcard_RelatedType <|-- vcard_Me
    vcard_RelatedType <|-- vcard_Contact
    vcard_RelatedType <|-- vcard_Coresident
    vcard_RelatedType <|-- vcard_Friend
    vcard_TelephoneType <|-- vcard_Modem
    vcard_RelatedType <|-- vcard_Kin
    vcard_RelatedType <|-- vcard_Coworker
    vcard_RelatedType <|-- vcard_Agent
    vcard_Kind <|-- vcard_Location
    vcard_Type <|-- vcard_Dom
    vcard_RelatedType <|-- vcard_Acquaintance
    vcard_Type <|-- vcard_ISDN
    vcard_Gender <|-- vcard_Male
    vcard_Group --> vcard_Kind : vcard:hasMember
```

## Statistics

| Metric | Count |
|--------|-------|
| Classes | 75 |
| Properties | 84 |
| Inheritance relationships | 52 |
| Properties with domain | 1 |
| Properties with range | 19 |

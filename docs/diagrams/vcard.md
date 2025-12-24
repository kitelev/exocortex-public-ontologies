# VCARD Ontology Diagram

UML-style class diagram for the **vcard** namespace.

*Generated automatically. Classes: 62, Properties: 84*

**Legend:**
- `<|--` Inheritance (rdfs:subClassOf)
- `-->` Object Property (owl:ObjectProperty)
- `..>` Datatype Property (owl:DatatypeProperty)

```mermaid
classDiagram
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
    class vcard_Neighbor
    class vcard_None
    class vcard_Organization
    class vcard_Other
    class vcard_Pager
    class vcard_Parcel
    class vcard_Parent
    class vcard_PCS
    class vcard_Postal
    class vcard_Pref
    class vcard_RelatedType
    class vcard_Sibling
    class vcard_Spouse
    class vcard_Sweetheart
    class vcard_Tel
    class vcard_TelephoneType
    class vcard_Text
    class vcard_TextPhone
    class vcard_Type
    class vcard_Unknown
    class vcard_VCard
    class vcard_Video
    class vcard_Voice
    class vcard_Work
    class vcard_X400
    vcard_Type <|-- vcard_X400
    vcard_Gender <|-- vcard_None
    vcard_Type <|-- vcard_Pref
    vcard_Type <|-- vcard_Internet
    vcard_Type <|-- vcard_Label
    vcard_RelatedType <|-- vcard_Spouse
    vcard_Type <|-- vcard_Intl
    vcard_TelephoneType <|-- vcard_BBS
    vcard_RelatedType <|-- vcard_Crush
    vcard_RelatedType <|-- vcard_Met
    vcard_RelatedType <|-- vcard_Sweetheart
    vcard_TelephoneType <|-- vcard_Msg
    vcard_TelephoneType <|-- vcard_Car
    vcard_Type <|-- vcard_Home
    vcard_TelephoneType <|-- vcard_Cell
    vcard_RelatedType <|-- vcard_Colleague
    vcard_TelephoneType <|-- vcard_Text
    vcard_RelatedType <|-- vcard_Neighbor
    vcard_Kind <|-- vcard_Individual
    vcard_TelephoneType <|-- vcard_PCS
    vcard_Type <|-- vcard_Postal
    vcard_RelatedType <|-- vcard_Date
    vcard_Gender <|-- vcard_Female
    vcard_TelephoneType <|-- vcard_TextPhone
    vcard_RelatedType <|-- vcard_Muse
    vcard_RelatedType <|-- vcard_Emergency
    vcard_RelatedType <|-- vcard_Child
    vcard_Kind <|-- vcard_Group
    vcard_TelephoneType <|-- vcard_Fax
    vcard_RelatedType <|-- vcard_Me
    vcard_Gender <|-- vcard_Unknown
    vcard_RelatedType <|-- vcard_Contact
    vcard_RelatedType <|-- vcard_Sibling
    vcard_RelatedType <|-- vcard_Coresident
    vcard_Gender <|-- vcard_Other
    vcard_RelatedType <|-- vcard_Parent
    vcard_RelatedType <|-- vcard_Friend
    vcard_TelephoneType <|-- vcard_Modem
    vcard_RelatedType <|-- vcard_Kin
    vcard_RelatedType <|-- vcard_Coworker
    vcard_TelephoneType <|-- vcard_Video
    vcard_RelatedType <|-- vcard_Agent
    vcard_Kind <|-- vcard_Location
    vcard_Type <|-- vcard_Dom
    vcard_TelephoneType <|-- vcard_Voice
    vcard_Kind <|-- vcard_Organization
    vcard_Type <|-- vcard_Parcel
    vcard_Type <|-- vcard_Work
    vcard_TelephoneType <|-- vcard_Pager
    vcard_RelatedType <|-- vcard_Acquaintance
    vcard_Type <|-- vcard_ISDN
    vcard_Gender <|-- vcard_Male
    vcard_Group --> vcard_Kind : vcard:hasMember
```

## Statistics

| Metric | Count |
|--------|-------|
| Classes | 62 |
| Properties | 84 |
| Inheritance relationships | 52 |
| Properties with domain | 1 |
| Properties with range | 28 |

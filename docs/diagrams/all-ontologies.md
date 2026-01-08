# Ontology Diagram

UML-style class diagram showing ontology structure.

*Generated automatically. Classes: 1583, Properties: 2625*

**Legend:**
- `<|--` Inheritance (rdfs:subClassOf)
- `-->` Object Property
- `..>` Datatype Property

```mermaid
classDiagram
    class dcat_CatalogRecord
    class a2645612
    class e3c847e6
    class xsd_duration
    class ecac7e97
    class a4da0fb1
    class _2a2171fa
    class b6726c50
    class _19807b5a
    class _7fe24472
    class _4dc60cd1
    class _80fa0681
    class a61e6966
    class _072d42ab
    class fea6fe82
    class xsd_nonNegativeInteger
    class _3db4df9a
    class d906d795
    class _5cbfe49e
    class _0143e1ca
    class xsd_dateTime
    class e13dff74
    class _9102dd8b
    class c2addc26
    class xsd_anyURI
    class dcat_Resource
    class dcat_Distribution
    class dcat_Dataset
    class dcat_Catalog
    class adms_Asset
    class adms_AssetDistribution
    class adms_AssetRepository
    class adms_Identifier
    class as_Accept
    class as_Activity
    class as_Add
    class as_Announce
    class as_Application
    class as_Arrive
    class as_Article
    class as_Audio
    class as_Block
    class as_Collection
    class as_CollectionPage
    class as_Create
    class as_Delete
    class as_Dislike
    class as_Document
    class as_Event
    class as_Flag
    class as_Follow
    class as_Group
    class as_Ignore
    class as_Image
    class as_IntransitiveActivity
    class as_Invite
    class as_Join
    class as_Leave
    class as_Like
    class as_Link
    class as_Listen
    class as_Mention
    class as_Move
    class as_Note
    class as_Object
    class as_Offer
    class as_OrderedCollection
    class as_OrderedCollectionPage
    class as_OrderedItems
    class as_Organization
    class as_Page
    class as_Person
    class as_Place
    class as_Profile
    class as_Question
    class as_Read
    class as_Reject
    class as_Relationship
    class as_Remove
    dcat_Catalog <|-- adms_AssetRepository
    dcat_Dataset <|-- adms_Asset
    dcat_Distribution <|-- adms_AssetDistribution
    as_Activity <|-- as_Accept
    as_Activity <|-- as_Move
    as_Activity <|-- as_Add
    as_Activity <|-- as_Remove
    as_Object <|-- as_Person
    as_Activity <|-- as_Dislike
    as_IntransitiveActivity <|-- as_Question
    as_Activity <|-- as_Reject
    as_Activity <|-- as_Announce
    as_Object <|-- as_Document
    as_Document <|-- as_Image
    as_Offer <|-- as_Invite
    as_Activity <|-- as_Read
    as_Object <|-- as_Organization
    as_Activity <|-- as_IntransitiveActivity
    as_Object <|-- as_Activity
    as_Link <|-- as_Mention
    as_Object <|-- as_Group
    as_Collection <|-- as_CollectionPage
    as_Activity <|-- as_Like
    as_Object <|-- as_Article
    as_Object <|-- as_Page
    as_Activity <|-- as_Leave
    as_Activity <|-- as_Offer
    as_Activity <|-- as_Ignore
    as_CollectionPage <|-- as_OrderedCollectionPage
    as_OrderedCollection <|-- as_OrderedCollectionPage
    as_Object <|-- as_Note
    as_Activity <|-- as_Join
    as_Object <|-- as_Collection
    as_Document <|-- as_Audio
    as_Activity <|-- as_Flag
    as_IntransitiveActivity <|-- as_Arrive
    as_Ignore <|-- as_Block
    as_Activity <|-- as_Delete
    as_Object <|-- as_Event
    as_Activity <|-- as_Listen
    as_Activity <|-- as_Create
    as_Object <|-- as_Application
    as_Activity <|-- as_Follow
    as_Object <|-- as_Place
    as_Object <|-- as_Relationship
    as_Object <|-- as_Profile
    dcat_Dataset <|-- dcat_Catalog
    dcat_Resource <|-- dcat_Dataset
    as_Object ..> xsd_anyURI : as:downstreamDuplicates
    as_Object --> c2addc26 : as:to
    as_Place ..> _9102dd8b : as:longitude
    as_Place ..> e13dff74 : as:units
    as_Object ..> xsd_dateTime : as:startTime
    as_Object --> _0143e1ca : as:icon
    as_Activity --> _5cbfe49e : as:result
    as_Activity ..> xsd_anyURI : as:verb
    as_Collection --> d906d795 : as:first
    as_Place ..> _3db4df9a : as:accuracy
    as_OrderedCollectionPage ..> xsd_nonNegativeInteger : as:startIndex
    as_Object --> fea6fe82 : as:tags
    as_Collection ..> xsd_nonNegativeInteger : as:totalItems
    as_Relationship --> _072d42ab : as:subject
    as_CollectionPage --> a61e6966 : as:partOf
    as_Place ..> _9102dd8b : as:altitude
    as_Object --> _80fa0681 : as:bcc
    as_Object ..> xsd_anyURI : as:upstreamDuplicates
    as_Object --> _4dc60cd1 : as:url
    as_Question --> _7fe24472 : as:oneOf
    as_Activity --> _19807b5a : as:actor
    as_Profile --> as_Object : as:describes
    as_Collection --> b6726c50 : as:last
    as_CollectionPage --> _2a2171fa : as:next
    as_Object --> a4da0fb1 : as:bto
    as_Question --> ecac7e97 : as:anyOf
    as_Object ..> xsd_duration : as:duration
    as_Object ..> e3c847e6 : as:summary
    as_Object --> a2645612 : as:attachment
    dcat_Catalog --> dcat_CatalogRecord : dcat:record
```

## Statistics

| Metric | Count |
|--------|-------|
| Classes | 1583 |
| Properties | 2625 |
| Inheritance relationships | 1627 |
| Properties with domain | 369 |
| Properties with range | 386 |

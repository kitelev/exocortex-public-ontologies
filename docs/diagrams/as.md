# AS Ontology Diagram

UML-style class diagram for the **as** namespace.

*Generated automatically. Classes: 159, Properties: 69*

**Legend:**
- `<|--` Inheritance (rdfs:subClassOf)
- `-->` Object Property
- `..>` Datatype Property

```mermaid
classDiagram
    class _8d31565d
    class _295da6b8
    class _6f5a992a
    class _446512f6
    class xsd_anyURI
    class ffe2bb9e
    class c6b8fc39
    class _9102dd8b
    class _209eb1e6
    class _46c57ee3
    class f9bdccc5
    class cc257c19
    class xsd_duration
    class dd501307
    class _840c272b
    class _16f99ad1
    class xsd_dateTime
    class e3c847e6
    class xsd_nonNegativeInteger
    class beebe521
    class _9a9ee80a
    class _0cfb9b07
    class fea6fe82
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
    class as_Service
    class as_TentativeAccept
    class as_TentativeReject
    class as_Tombstone
    as_Activity <|-- as_Remove
    as_Activity <|-- as_Announce
    as_Activity <|-- as_IntransitiveActivity
    as_Reject <|-- as_TentativeReject
    as_CollectionPage <|-- as_OrderedCollectionPage
    as_OrderedCollection <|-- as_OrderedCollectionPage
    as_Object <|-- as_Relationship
    as_Object <|-- as_Organization
    as_Object <|-- as_Profile
    as_Activity <|-- as_Leave
    as_Activity <|-- as_Delete
    as_Activity <|-- as_Follow
    as_Activity <|-- as_Reject
    as_Object <|-- as_Note
    as_Activity <|-- as_Accept
    as_Ignore <|-- as_Block
    as_Accept <|-- as_TentativeAccept
    as_Activity <|-- as_Move
    as_Object <|-- as_Document
    as_Object <|-- as_Application
    as_Activity <|-- as_Read
    as_Object <|-- as_Page
    as_Object <|-- as_Activity
    as_Object <|-- as_Service
    as_Object <|-- as_Group
    as_Activity <|-- as_Dislike
    as_Offer <|-- as_Invite
    as_Link <|-- as_Mention
    as_Activity <|-- as_Add
    as_IntransitiveActivity <|-- as_Arrive
    as_Activity <|-- as_Like
    as_Object <|-- as_Person
    as_Collection <|-- as_CollectionPage
    as_Object <|-- as_Collection
    as_Object <|-- as_Place
    as_Object <|-- as_Article
    as_Activity <|-- as_Listen
    as_IntransitiveActivity <|-- as_Question
    as_Activity <|-- as_Offer
    as_Activity <|-- as_Join
    as_Object <|-- as_Tombstone
    as_Object <|-- as_Event
    as_Document <|-- as_Image
    as_Activity <|-- as_Create
    as_Activity <|-- as_Flag
    as_Activity <|-- as_Ignore
    as_Document <|-- as_Audio
    as_Object --> fea6fe82 : as:tags
    as_Object ..> _0cfb9b07 : as:rating
    as_CollectionPage --> _9a9ee80a : as:next
    as_Activity --> beebe521 : as:result
    as_OrderedCollectionPage ..> xsd_nonNegativeInteger : as:startIndex
    as_Object ..> e3c847e6 : as:summary
    as_Tombstone ..> xsd_dateTime : as:deleted
    as_Object --> _16f99ad1 : as:context
    as_Question --> _840c272b : as:oneOf
    as_Object --> dd501307 : as:generator
    as_Link ..> xsd_nonNegativeInteger : as:width
    as_Object ..> xsd_duration : as:duration
    as_Object --> cc257c19 : as:location
    as_Link ..> xsd_nonNegativeInteger : as:height
    as_Question --> f9bdccc5 : as:anyOf
    as_Collection ..> xsd_nonNegativeInteger : as:totalItems
    as_Object --> _46c57ee3 : as:image
    as_Collection --> _209eb1e6 : as:current
    as_Place ..> _9102dd8b : as:latitude
    as_Profile --> as_Object : as:describes
    as_CollectionPage --> c6b8fc39 : as:partOf
    as_Object ..> xsd_dateTime : as:startTime
    as_Object ..> ffe2bb9e : as:content
    as_Object ..> xsd_anyURI : as:upstreamDuplicates
    as_Link ..> _446512f6 : as:hreflang
    as_Activity --> _6f5a992a : as:instrument
    as_Object --> _295da6b8 : as:inReplyTo
    as_Object --> _8d31565d : as:audience
```

## Statistics

| Metric | Count |
|--------|-------|
| Classes | 159 |
| Properties | 69 |
| Inheritance relationships | 58 |
| Properties with domain | 39 |
| Properties with range | 45 |

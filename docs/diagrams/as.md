# AS Ontology Diagram

UML-style class diagram for the **as** namespace.

*Generated automatically. Classes: 55, Properties: 69*

**Legend:**
- `<|--` Inheritance (rdfs:subClassOf)
- `-->` Object Property (owl:ObjectProperty)
- `..>` Datatype Property (owl:DatatypeProperty)

```mermaid
classDiagram
    class c2addc26
    class b158946c
    class b1267ad9
    class rdf_Property
    class _419d6f92
    class _52dbd1df
    class bfd64013
    class _8d31565d
    class f01fa4be
    class da2c9157
    class _42d9ee06
    class e13dff74
    class _19807b5a
    class _295da6b8
    class a1fb6f8e
    class _6f5a992a
    class _0cb37b3b
    class _446512f6
    class a4da0fb1
    class _3db4df9a
    class bcac78ce
    class ffe2bb9e
    class dd5c9543
    class _6d1e9fe8
    class c6b8fc39
    class xsd_anyURI
    class _6d7404a5
    class _7e41b1e2
    class _9102dd8b
    class _209eb1e6
    class _46c57ee3
    class xsd_string
    class _8f04c583
    class d906d795
    class _033a5b13
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
    class d8445621
    class _190c48bc
    class _63538320
    class _156b67a7
    class f31a29e7
    class _8c4a3232
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
    class as_Travel
    class as_Undo
    class as_Update
    class as_Video
    class as_View
    as_Activity <|-- as_Remove
    as_Activity <|-- as_Announce
    _8c4a3232 <|-- as_IntransitiveActivity
    as_Activity <|-- as_IntransitiveActivity
    f31a29e7 <|-- as_IntransitiveActivity
    as_Reject <|-- as_TentativeReject
    as_CollectionPage <|-- as_OrderedCollectionPage
    as_OrderedCollection <|-- as_OrderedCollectionPage
    _156b67a7 <|-- as_OrderedCollection
    _63538320 <|-- as_OrderedCollection
    as_Object <|-- as_Relationship
    as_Object <|-- as_Organization
    _190c48bc <|-- as_OrderedItems
    d8445621 <|-- as_OrderedItems
    as_Object <|-- as_Profile
    as_Activity <|-- as_Leave
    as_Activity <|-- as_Delete
    as_Activity <|-- as_Follow
    as_Activity <|-- as_Reject
    as_Object <|-- as_Note
    as_Activity <|-- as_Undo
    as_Activity <|-- as_Accept
    as_Ignore <|-- as_Block
    as_Accept <|-- as_TentativeAccept
    as_Activity <|-- as_Move
    as_Object <|-- as_Document
    as_Object <|-- as_Application
    as_Activity <|-- as_Read
    as_Activity <|-- as_Update
    as_Object <|-- as_Page
    as_Object <|-- as_Activity
    as_Object <|-- as_Service
    as_Activity <|-- as_View
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
    as_IntransitiveActivity <|-- as_Travel
    as_Object <|-- as_Place
    as_Object <|-- as_Article
    as_Activity <|-- as_Listen
    as_IntransitiveActivity <|-- as_Question
    as_Activity <|-- as_Offer
    as_Activity <|-- as_Join
    as_Object <|-- as_Tombstone
    as_Document <|-- as_Video
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
    as_Object ..> xsd_dateTime : as:endTime
    as_Link ..> xsd_nonNegativeInteger : as:height
    as_Question --> f9bdccc5 : as:anyOf
    as_Place ..> _033a5b13 : as:radius
    as_Collection --> d906d795 : as:first
    as_Object --> _8f04c583 : as:url
    as_Collection ..> xsd_nonNegativeInteger : as:totalItems
    as_Link ..> xsd_string : as:rel
    as_Object --> _46c57ee3 : as:image
    as_Collection --> _209eb1e6 : as:current
    as_Place ..> _9102dd8b : as:altitude
    as_Place ..> _9102dd8b : as:latitude
    as_Object --> _7e41b1e2 : as:attachment
    as_Object --> _6d7404a5 : as:icon
    as_Object ..> xsd_anyURI : as:downstreamDuplicates
    as_Profile --> as_Object : as:describes
    as_CollectionPage --> c6b8fc39 : as:partOf
    as_Object ..> xsd_dateTime : as:startTime
    as_Object ..> xsd_anyURI : as:objectType
    as_Object --> _6d1e9fe8 : as:cc
    as_Activity --> dd5c9543 : as:origin
    as_Object ..> ffe2bb9e : as:content
    bcac78ce ..> xsd_anyURI : as:id
    as_Object ..> xsd_anyURI : as:upstreamDuplicates
    as_Place ..> _3db4df9a : as:accuracy
    as_Object --> a4da0fb1 : as:bto
    as_Link ..> _446512f6 : as:hreflang
    as_Activity --> _0cb37b3b : as:target
    as_Tombstone --> as_Object : as:formerType
    as_Activity --> _6f5a992a : as:instrument
    as_Object --> a1fb6f8e : as:author
    as_Object --> _295da6b8 : as:inReplyTo
    as_Activity --> _19807b5a : as:actor
    as_Place ..> e13dff74 : as:units
    as_Link ..> xsd_anyURI : as:href
    as_Relationship --> _42d9ee06 : as:subject
    as_Collection --> da2c9157 : as:items
    as_Object ..> xsd_dateTime : as:updated
    as_Activity ..> xsd_anyURI : as:verb
    as_CollectionPage --> f01fa4be : as:prev
    as_Object --> _8d31565d : as:audience
    as_Object --> as_Collection : as:replies
    as_Place ..> _9102dd8b : as:longitude
    as_Object --> bfd64013 : as:tag
    as_Object --> _52dbd1df : as:bcc
    as_Collection --> _419d6f92 : as:last
    as_Object ..> xsd_dateTime : as:published
    as_Relationship --> rdf_Property : as:relationship
    as_Object --> b1267ad9 : as:attachments
    as_Object --> b158946c : as:provider
    as_Object --> c2addc26 : as:to
```

## Statistics

| Metric | Count |
|--------|-------|
| Classes | 55 |
| Properties | 69 |
| Inheritance relationships | 58 |
| Properties with domain | 69 |
| Properties with range | 69 |

# AS Ontology Diagram

UML-style class diagram for the **as** namespace.

*Generated automatically. Classes: 159, Properties: 69*

**Legend:**
- `<|--` Inheritance (rdfs:subClassOf)
- `-->` Object Property
- `..>` Datatype Property

```mermaid
classDiagram
    class as_Activity
    class xsd_anyURI
    class ffe2bb9e
    class xsd_dateTime
    class as_Profile
    class as_Collection
    class a944e7dc
    class _91130058
    class f9bdccc5
    class xsd_string
    class cc257c19
    class xsd_duration
    class dd501307
    class as_Question
    class as_Object
    class _0143e1ca
    class _01fb90c2
    class _072d42ab
    class _08d12d1b
    class _0c2288fc
    class _0c74593a
    class _0cb37b3b
    class _0e78d275
    class _1188811e
    class _11e388fe
    class _156b67a7
    class _1583faea
    class _16f99ad1
    class _190c48bc
    class _19807b5a
    class _1f753f63
    class _1fe72c67
    class _209eb1e6
    class _295da6b8
    class _2a2171fa
    class _2d7e8396
    class _3c97862a
    class _419d6f92
    class _42d9ee06
    class _46c57ee3
    class _46c71669
    class _4da68d22
    class _4dc60cd1
    class _4edfcb9e
    class _50e31cbb
    class _52dbd1df
    class _531c615f
    class _57609c96
    class _5cbfe49e
    class _5da60c63
    class _63538320
    class _64e52252
    class _6a984dd0
    class _6d1e9fe8
    class _6d7404a5
    class _6f5a992a
    class _735f3363
    class _79fc9e6c
    class _7e41b1e2
    class _7fab4898
    class _7fe24472
    class _80fa0681
    class _840c272b
    class _864d84e0
    class _8d31565d
    as_Object --> _16f99ad1 : as:context
    as_Question --> _840c272b : as:oneOf
    as_Object --> dd501307 : as:generator
    as_Object ..> xsd_duration : as:duration
    as_Object --> cc257c19 : as:location
    _11e388fe ..> xsd_string : as:mediaType
    as_Question --> f9bdccc5 : as:anyOf
    _735f3363 --> _91130058 : as:object
    _50e31cbb --> a944e7dc : as:preview
    as_Object --> _46c57ee3 : as:image
    as_Collection --> _209eb1e6 : as:current
    as_Profile --> as_Object : as:describes
    as_Object ..> xsd_dateTime : as:startTime
    as_Object ..> ffe2bb9e : as:content
    as_Object ..> xsd_anyURI : as:upstreamDuplicates
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

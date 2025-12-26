# Ontology Diagram

UML-style class diagram showing ontology structure.

*Generated automatically. Classes: 1422, Properties: 2422*

**Legend:**
- `<|--` Inheritance (rdfs:subClassOf)
- `-->` Object Property
- `..>` Datatype Property

```mermaid
classDiagram
    class prov_Role
    class _7874a001
    class a2645612
    class e3c847e6
    class xsd_duration
    class a4da0fb1
    class as_CollectionPage
    class as_Profile
    class _80fa0681
    class as_Relationship
    class fea6fe82
    class xsd_anyURI
    class as_Activity
    class as_Object
    class _00a269aa
    class _0143e1ca
    class _01fb90c2
    class _072d42ab
    class _08d12d1b
    class _08e29461
    class _0c2288fc
    class _0c74593a
    class _0cb37b3b
    class _0e78d275
    class _0fe2bd43
    class _1188811e
    class _11e388fe
    class _156b67a7
    class _1583faea
    class _16f92030
    class _16f99ad1
    class _190c48bc
    class _19807b5a
    class _1e8f15a8
    class _1e931111
    class _1f753f63
    class _1fe72c67
    class _209eb1e6
    class _27a61271
    class _27fdff12
    class _295da6b8
    class _2a2171fa
    class _2c962624
    class _2d7e8396
    class _2e97a557
    class _3886acbb
    class _3c97862a
    class _419d6f92
    class _42d9ee06
    class _46c57ee3
    class _46c71669
    class _4da68d22
    class _4dc60cd1
    class _4e232b4c
    class _4edfcb9e
    class _50e31cbb
    class _52dbd1df
    class _531c615f
    class _54ca8a65
    class _57609c96
    class _5ca151b2
    class _5cbfe49e
    class _5da60c63
    class _5df0710c
    as_Object --> _0143e1ca : as:icon
    as_Activity --> _5cbfe49e : as:result
    as_Activity ..> xsd_anyURI : as:verb
    as_Object --> fea6fe82 : as:tags
    as_Relationship --> _072d42ab : as:subject
    as_Object --> _80fa0681 : as:bcc
    as_Object ..> xsd_anyURI : as:upstreamDuplicates
    as_Object --> _4dc60cd1 : as:url
    as_Activity --> _19807b5a : as:actor
    as_Profile --> as_Object : as:describes
    as_CollectionPage --> _2a2171fa : as:next
    as_Object --> a4da0fb1 : as:bto
    as_Object ..> xsd_duration : as:duration
    as_Object ..> e3c847e6 : as:summary
    as_Object --> a2645612 : as:attachment
    _2c962624 --> _7874a001 : org:reportsTo
    _08e29461 --> prov_Role : prov:hadRole
```

## Statistics

| Metric | Count |
|--------|-------|
| Classes | 1422 |
| Properties | 2422 |
| Inheritance relationships | 1377 |
| Properties with domain | 266 |
| Properties with range | 287 |

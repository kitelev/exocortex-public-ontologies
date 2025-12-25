# Ontology Diagram

UML-style class diagram showing ontology structure.

*Generated automatically. Classes: 1417, Properties: 2418*

**Legend:**
- `<|--` Inheritance (rdfs:subClassOf)
- `-->` Object Property
- `..>` Datatype Property

```mermaid
classDiagram
    class time_TemporalEntity
    class skos_Collection
    class sh_ResultAnnotation
    class sh_SPARQLConstructExecutable
    class sh_PrefixDeclaration
    class prov_Communication
    class prov_Invalidation
    class prov_InstantaneousEvent
    class prov_Revision
    class prov_Entity
    class prov_Influence
    class prov_Role
    class prov_Activity
    class _8d31565d
    class xsd_anyURI
    class ffe2bb9e
    class xsd_dateTime
    class as_Profile
    class as_Collection
    class a944e7dc
    class xsd_string
    class cc257c19
    class xsd_duration
    class dd501307
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
    as_Object --> _16f99ad1 : as:context
    as_Object --> dd501307 : as:generator
    as_Object ..> xsd_duration : as:duration
    as_Object --> cc257c19 : as:location
    _11e388fe ..> xsd_string : as:mediaType
    _50e31cbb --> a944e7dc : as:preview
    as_Object --> _46c57ee3 : as:image
    as_Collection --> _209eb1e6 : as:current
    as_Profile --> as_Object : as:describes
    as_Object ..> xsd_dateTime : as:startTime
    as_Object ..> ffe2bb9e : as:content
    as_Object ..> xsd_anyURI : as:upstreamDuplicates
    as_Object --> _295da6b8 : as:inReplyTo
    as_Object --> _8d31565d : as:audience
    prov_Activity ..> xsd_dateTime : prov:startedAtTime
    _08e29461 --> prov_Role : prov:hadRole
    _54ca8a65 --> prov_Influence : prov:qualifiedInfluence
    prov_Entity ..> xsd_dateTime : prov:generatedAtTime
    prov_Entity --> prov_Entity : prov:wasDerivedFrom
    prov_Entity --> prov_Revision : prov:qualifiedRevision
    prov_InstantaneousEvent ..> xsd_dateTime : prov:atTime
    prov_Entity ..> xsd_dateTime : prov:invalidatedAtTime
    prov_Entity --> prov_Invalidation : prov:qualifiedInvalidation
    prov_Activity --> prov_Communication : prov:qualifiedCommunication
    sh_PrefixDeclaration ..> xsd_string : sh:prefix
    sh_PrefixDeclaration ..> xsd_anyURI : sh:namespace
    sh_SPARQLConstructExecutable ..> xsd_string : sh:construct
    sh_ResultAnnotation ..> xsd_string : sh:annotationVarName
    skos_Collection --> _3886acbb : skos:member
    time_TemporalEntity ..> xsd_duration : time:hasXSDDuration
```

## Statistics

| Metric | Count |
|--------|-------|
| Classes | 1417 |
| Properties | 2418 |
| Inheritance relationships | 1375 |
| Properties with domain | 242 |
| Properties with range | 311 |

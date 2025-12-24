# Ontology Cheat Sheet

Quick reference for all ontologies in this collection.

---

## RDF/RDFS/OWL Foundation

### rdf: — RDF Core
`http://www.w3.org/1999/02/22-rdf-syntax-ns#`

| Term | Type | Purpose |
|------|------|---------|
| `rdf:type` | Property | Declare instance-of relationship |
| `rdf:Property` | Class | Class of all properties |
| `rdf:Resource` | Class | Class of everything |
| `rdf:Literal` | Class | Class of literal values |
| `rdf:List` | Class | Ordered collections |

### rdfs: — RDF Schema
`http://www.w3.org/2000/01/rdf-schema#`

| Term | Type | Purpose |
|------|------|---------|
| `rdfs:Class` | Class | Define new classes |
| `rdfs:subClassOf` | Property | Class inheritance |
| `rdfs:subPropertyOf` | Property | Property inheritance |
| `rdfs:domain` | Property | Subject constraint |
| `rdfs:range` | Property | Object constraint |
| `rdfs:label` | Property | Human-readable name |
| `rdfs:comment` | Property | Description |

### owl: — Web Ontology Language
`http://www.w3.org/2002/07/owl#`

| Term | Type | Purpose |
|------|------|---------|
| `owl:Class` | Class | OWL class definition |
| `owl:ObjectProperty` | Class | Resource-to-resource |
| `owl:DatatypeProperty` | Class | Resource-to-literal |
| `owl:FunctionalProperty` | Class | At most one value |
| `owl:TransitiveProperty` | Class | A→B, B→C implies A→C |
| `owl:SymmetricProperty` | Class | A→B implies B→A |
| `owl:sameAs` | Property | Identity |
| `owl:imports` | Property | Ontology dependency |

---

## Knowledge Organization

### skos: — Simple Knowledge Organization System
`http://www.w3.org/2004/02/skos/core#`

| Term | Type | Purpose |
|------|------|---------|
| `skos:Concept` | Class | Abstract notion |
| `skos:ConceptScheme` | Class | Collection of concepts |
| `skos:prefLabel` | Property | Preferred label |
| `skos:altLabel` | Property | Alternative label |
| `skos:broader` | Property | Parent concept |
| `skos:narrower` | Property | Child concept |
| `skos:related` | Property | Related concept |
| `skos:inScheme` | Property | Scheme membership |

---

## Dublin Core Metadata

### dc: — Dublin Core Elements
`http://purl.org/dc/elements/1.1/`

| Term | Purpose |
|------|---------|
| `dc:title` | Resource title |
| `dc:creator` | Primary creator |
| `dc:subject` | Topic |
| `dc:description` | Description |
| `dc:date` | Date |
| `dc:type` | Nature/genre |
| `dc:format` | File format |
| `dc:rights` | Rights information |

### dcterms: — Dublin Core Terms
`http://purl.org/dc/terms/`

Extended DC with classes and refined properties:
- `dcterms:Agent`, `dcterms:Location`, `dcterms:PeriodOfTime`
- `dcterms:created`, `dcterms:modified`, `dcterms:issued`
- `dcterms:license`, `dcterms:accessRights`

---

## Social & People

### foaf: — Friend of a Friend
`http://xmlns.com/foaf/0.1/`

| Term | Type | Purpose |
|------|------|---------|
| `foaf:Person` | Class | Human being |
| `foaf:Agent` | Class | Person, org, or software |
| `foaf:Organization` | Class | Organization |
| `foaf:name` | Property | Full name |
| `foaf:mbox` | Property | Email (unique ID) |
| `foaf:knows` | Property | Personal connection |
| `foaf:homepage` | Property | Website |

### org: — Organization Ontology
`http://www.w3.org/ns/org#`

| Term | Type | Purpose |
|------|------|---------|
| `org:Organization` | Class | Organization |
| `org:OrganizationalUnit` | Class | Department/division |
| `org:Role` | Class | Position/role |
| `org:Membership` | Class | Person-org relation |
| `org:hasMember` | Property | Members |
| `org:subOrganizationOf` | Property | Org hierarchy |

### vcard: — vCard Ontology
`http://www.w3.org/2006/vcard/ns#`

Contact information: Address, Email, Tel, etc.

---

## Provenance & Activity

### prov: — PROV Ontology
`http://www.w3.org/ns/prov#`

| Term | Type | Purpose |
|------|------|---------|
| `prov:Entity` | Class | Thing with identity |
| `prov:Activity` | Class | Something that happens |
| `prov:Agent` | Class | Responsible party |
| `prov:wasDerivedFrom` | Property | Entity derivation |
| `prov:wasGeneratedBy` | Property | What created entity |
| `prov:wasAssociatedWith` | Property | Activity responsibility |

### as: — Activity Streams
`https://www.w3.org/ns/activitystreams#`

| Term | Type | Purpose |
|------|------|---------|
| `as:Object` | Class | Base object |
| `as:Activity` | Class | Action taken |
| `as:Create` | Class | Creation activity |
| `as:Update` | Class | Modification |
| `as:Delete` | Class | Removal |
| `as:actor` | Property | Who performed |
| `as:object` | Property | Target of activity |

---

## Time & Space

### time: — OWL-Time
`http://www.w3.org/2006/time#`

| Term | Type | Purpose |
|------|------|---------|
| `time:Instant` | Class | Point in time |
| `time:Interval` | Class | Duration |
| `time:TemporalEntity` | Class | Any temporal thing |
| `time:hasBeginning` | Property | Start instant |
| `time:hasEnd` | Property | End instant |
| `time:before` | Property | Temporal order |

### geo: — WGS84 Geo
`http://www.w3.org/2003/01/geo/wgs84_pos#`

| Term | Type | Purpose |
|------|------|---------|
| `geo:SpatialThing` | Class | Spatial entity |
| `geo:Point` | Class | Location point |
| `geo:lat` | Property | Latitude |
| `geo:long` | Property | Longitude |

### geosparql: — GeoSPARQL
`http://www.opengis.net/ont/geosparql#`

Extended spatial vocabulary for GIS applications.

---

## Data & Catalogs

### dcat: — Data Catalog Vocabulary
`http://www.w3.org/ns/dcat#`

| Term | Type | Purpose |
|------|------|---------|
| `dcat:Catalog` | Class | Data catalog |
| `dcat:Dataset` | Class | Collection of data |
| `dcat:Distribution` | Class | Specific form of dataset |
| `dcat:DataService` | Class | Data access service |
| `dcat:downloadURL` | Property | Direct download |
| `dcat:accessURL` | Property | Access point |

### void: — Vocabulary of Interlinked Datasets
`http://rdfs.org/ns/void#`

Dataset descriptions and statistics.

---

## Software & Projects

### doap: — Description of a Project
`http://usefulinc.com/ns/doap#`

| Term | Type | Purpose |
|------|------|---------|
| `doap:Project` | Class | Software project |
| `doap:Version` | Class | Release version |
| `doap:Repository` | Class | Code repository |
| `doap:name` | Property | Project name |
| `doap:homepage` | Property | Project website |
| `doap:developer` | Property | Developers |

---

## Social Media & Sensors

### sioc: — Semantically-Interlinked Online Communities
`http://rdfs.org/sioc/ns#`

Forums, posts, users, communities.

### sosa: — Sensor, Observation, Sample, and Actuator
`http://www.w3.org/ns/sosa/`

| Term | Type | Purpose |
|------|------|---------|
| `sosa:Sensor` | Class | Observation device |
| `sosa:Observation` | Class | Measurement act |
| `sosa:ObservableProperty` | Class | What's measured |
| `sosa:Result` | Class | Measurement result |

---

## Shapes & Validation

### sh: — SHACL Shapes
`http://www.w3.org/ns/shacl#`

| Term | Type | Purpose |
|------|------|---------|
| `sh:NodeShape` | Class | Shape for nodes |
| `sh:PropertyShape` | Class | Shape for properties |
| `sh:targetClass` | Property | Shape applies to class |
| `sh:path` | Property | Property to validate |
| `sh:datatype` | Property | Required datatype |
| `sh:minCount` | Property | Minimum occurrences |
| `sh:maxCount` | Property | Maximum occurrences |

---

## Massive Vocabulary

### schema: — Schema.org
`https://schema.org/`

930 classes, 1520 properties covering:
- People, Places, Events
- Products, Offers, Reviews
- Organizations, Actions
- Creative works, Media
- Medical, Educational content

---

## Quick Reference: Common Patterns

### Define a Class
```
:MyClass a owl:Class ;
    rdfs:label "My Class" ;
    rdfs:comment "Description..." ;
    rdfs:subClassOf :ParentClass .
```

### Define a Property
```
:myProperty a owl:ObjectProperty ;
    rdfs:label "my property" ;
    rdfs:domain :SubjectClass ;
    rdfs:range :ObjectClass .
```

### Create an Instance
```
:myInstance a :MyClass ;
    rdfs:label "My Instance" ;
    :myProperty :anotherThing .
```

---

## See Also

- [Glossary](glossary.md) - Detailed term definitions
- [Class Hierarchy](class-hierarchy.md) - All classes
- [Property Hierarchy](property-hierarchy.md) - All properties
- [Cross-References](cross-references.md) - Inter-ontology links
- [Mermaid Diagrams](diagrams/) - Visual diagrams

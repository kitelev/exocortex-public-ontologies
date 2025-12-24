# RDF/RDFS/OWL Glossary

A comprehensive glossary of Semantic Web terms used in this ontology collection.

## Core Concepts

### Triple

The fundamental unit of RDF data: **Subject → Predicate → Object**.

```yaml
# Example from this repository
subject: "[[foaf:Person]]"
predicate: "[[rdfs:subClassOf]]"
object: "[[foaf:Agent]]"
```

### URI (Uniform Resource Identifier)

A globally unique identifier for resources. Every class, property, and instance has a URI.

```
http://xmlns.com/foaf/0.1/Person
└── namespace ──────────┘└─local─┘
```

### Namespace

A collection of related terms under a common URI prefix.

| Prefix | Namespace URI | Description |
|--------|---------------|-------------|
| `rdf:` | http://www.w3.org/1999/02/22-rdf-syntax-ns# | RDF core vocabulary |
| `rdfs:` | http://www.w3.org/2000/01/rdf-schema# | RDF Schema |
| `owl:` | http://www.w3.org/2002/07/owl# | Web Ontology Language |
| `xsd:` | http://www.w3.org/2001/XMLSchema# | XML Schema datatypes |

---

## RDF Vocabulary

### rdf:type

Declares the class(es) of a resource. The most fundamental RDF property.

```yaml
subject: "[[foaf:Person]]"
predicate: "[[rdf:type|a]]"
object: "[[owl:Class]]"
```

**Meaning**: "foaf:Person is an owl:Class"

### rdf:Property

The class of all properties. Any relationship between resources is an rdf:Property.

```yaml
subject: "[[rdfs:label]]"
predicate: "[[rdf:type|a]]"
object: "[[rdf:Property]]"
```

### rdf:Resource

The class of everything. All things described by RDF are resources.

### rdf:Literal

The class of literal values (strings, numbers, dates).

```yaml
object: "\"John Smith\"@en"  # Language-tagged literal
object: "\"42\"^^[[xsd:integer]]"  # Typed literal
```

### rdf:List

RDF's representation of ordered collections.

---

## RDFS Vocabulary

### rdfs:Class

The class of all classes. Used to define new types.

```yaml
subject: "[[foaf:Person]]"
predicate: "[[rdf:type|a]]"
object: "[[rdfs:Class]]"
```

### rdfs:subClassOf

Declares class inheritance. If A subClassOf B, then all instances of A are also instances of B.

```yaml
subject: "[[foaf:Person]]"
predicate: "[[rdfs:subClassOf]]"
object: "[[foaf:Agent]]"
```

**Inference**: If John is a foaf:Person, John is also a foaf:Agent.

### rdfs:subPropertyOf

Declares property inheritance. If P subPropertyOf Q, then whenever P holds, Q also holds.

```yaml
subject: "[[foaf:name]]"
predicate: "[[rdfs:subPropertyOf]]"
object: "[[rdfs:label]]"
```

### rdfs:domain

Specifies the class of resources that can be subjects of a property.

```yaml
subject: "[[foaf:name]]"
predicate: "[[rdfs:domain]]"
object: "[[foaf:Person]]"
```

**Inference**: If X foaf:name "John", then X is a foaf:Person.

### rdfs:range

Specifies the class of values that a property can have.

```yaml
subject: "[[foaf:knows]]"
predicate: "[[rdfs:range]]"
object: "[[foaf:Person]]"
```

**Inference**: If X foaf:knows Y, then Y is a foaf:Person.

### rdfs:label

A human-readable name for a resource.

```yaml
subject: "[[foaf:Person]]"
predicate: "[[rdfs:label]]"
object: "\"Person\"@en"
```

### rdfs:comment

A human-readable description of a resource.

```yaml
subject: "[[foaf:Person]]"
predicate: "[[rdfs:comment]]"
object: "\"A person.\""
```

### rdfs:isDefinedBy

Links a resource to its defining ontology.

```yaml
subject: "[[foaf:Person]]"
predicate: "[[rdfs:isDefinedBy]]"
object: "[[!foaf]]"  # Namespace anchor
```

### rdfs:seeAlso

Provides additional information about a resource.

---

## OWL Vocabulary

### owl:Class

OWL's class construct. Equivalent to rdfs:Class but enables more expressions.

### owl:ObjectProperty

A property that relates resources to other resources.

```yaml
subject: "[[foaf:knows]]"
predicate: "[[rdf:type|a]]"
object: "[[owl:ObjectProperty]]"
```

### owl:DatatypeProperty

A property that relates resources to literal values.

```yaml
subject: "[[foaf:name]]"
predicate: "[[rdf:type|a]]"
object: "[[owl:DatatypeProperty]]"
```

### owl:AnnotationProperty

A property used for metadata that doesn't affect reasoning.

```yaml
subject: "[[rdfs:label]]"
predicate: "[[rdf:type|a]]"
object: "[[owl:AnnotationProperty]]"
```

### owl:FunctionalProperty

A property with at most one value for each subject.

```yaml
subject: "[[foaf:birthday]]"
predicate: "[[rdf:type|a]]"
object: "[[owl:FunctionalProperty]]"
```

### owl:InverseFunctionalProperty

A property whose value uniquely identifies the subject.

```yaml
subject: "[[foaf:mbox]]"
predicate: "[[rdf:type|a]]"
object: "[[owl:InverseFunctionalProperty]]"
```

**Meaning**: Email addresses uniquely identify people.

### owl:TransitiveProperty

A property where if A→B and B→C, then A→C.

```yaml
subject: "[[rdfs:subClassOf]]"
predicate: "[[rdf:type|a]]"
object: "[[owl:TransitiveProperty]]"
```

### owl:SymmetricProperty

A property where if A→B then B→A.

```yaml
subject: "[[foaf:knows]]"
predicate: "[[rdf:type|a]]"
object: "[[owl:SymmetricProperty]]"
```

### owl:equivalentClass

Declares that two classes have exactly the same instances.

### owl:equivalentProperty

Declares that two properties have the same extension.

### owl:sameAs

Declares that two URIs refer to the same thing.

### owl:differentFrom

Declares that two resources are not the same.

### owl:disjointWith

Declares that two classes have no common instances.

### owl:Ontology

Declares an ontology document with metadata.

### owl:imports

Declares that an ontology depends on another.

### owl:versionInfo

Provides version information for an ontology.

---

## Property Characteristics Summary

| Characteristic | Meaning | Example |
|---------------|---------|---------|
| Functional | At most one value per subject | `foaf:birthday` |
| InverseFunctional | Value uniquely identifies subject | `foaf:mbox` |
| Transitive | A→B, B→C implies A→C | `rdfs:subClassOf` |
| Symmetric | A→B implies B→A | `foaf:knows` |
| Asymmetric | A→B implies NOT B→A | `skos:broader` |
| Reflexive | A→A always holds | `owl:sameAs` |
| Irreflexive | A→A never holds | `owl:differentFrom` |

---

## File Format in This Repository

### Anchor Files
Define resources (classes, properties, instances):
```yaml
---
metadata: anchor
uri: "http://xmlns.com/foaf/0.1/Person"
aliases:
  - "foaf:Person"
---
```

### Statement Files
Define triples (subject-predicate-object):
```yaml
---
metadata: statement
subject: "[[uuid-of-subject]]"
predicate: "[[uuid-of-predicate]]"
object: "[[uuid-of-object]]"
aliases:
  - "foaf:Person a owl:Class"
---
```

### Namespace Files
Define namespace prefixes:
```yaml
---
metadata: namespace
uri: "http://xmlns.com/foaf/0.1/"
aliases:
  - "!foaf"
---
```

---

## Common Patterns

### Class Definition
```yaml
# 1. Type declaration
foaf:Person a owl:Class

# 2. Label
foaf:Person rdfs:label "Person"@en

# 3. Comment
foaf:Person rdfs:comment "A person."@en

# 4. Hierarchy
foaf:Person rdfs:subClassOf foaf:Agent
```

### Property Definition
```yaml
# 1. Type declaration
foaf:knows a owl:ObjectProperty

# 2. Domain/Range
foaf:knows rdfs:domain foaf:Person
foaf:knows rdfs:range foaf:Person

# 3. Label and comment
foaf:knows rdfs:label "knows"
foaf:knows rdfs:comment "A person known by this person."
```

---

## See Also

- [W3C RDF Primer](https://www.w3.org/TR/rdf-primer/)
- [W3C RDFS Specification](https://www.w3.org/TR/rdf-schema/)
- [W3C OWL Primer](https://www.w3.org/TR/owl-primer/)
- [Class Hierarchy](class-hierarchy.md) - Hierarchical view of classes
- [Property Hierarchy](property-hierarchy.md) - Hierarchical view of properties

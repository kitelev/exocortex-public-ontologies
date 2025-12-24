# GEOSPARQL Ontology Diagram

UML-style class diagram for the **geosparql** namespace.

*Generated automatically. Classes: 6, Properties: 54*

**Legend:**
- `<|--` Inheritance (rdfs:subClassOf)
- `-->` Object Property (owl:ObjectProperty)
- `..>` Datatype Property (owl:DatatypeProperty)

```mermaid
classDiagram
    class geosparql_gmlLiteral
    class geosparql_kmlLiteral
    class ca079f4f
    class rdfs_Literal
    class geosparql_wktLiteral
    class geosparql_dggsLiteral
    class xsd_integer
    class xsd_boolean
    class geosparql_geoJSONLiteral
    class bc7f215b
    class b5c888a2
    class rdfs_Container
    class _090207d1
    class geosparql_Feature
    class geosparql_FeatureCollection
    class geosparql_Geometry
    class geosparql_GeometryCollection
    class geosparql_SpatialObject
    class geosparql_SpatialObjectCollection
    geosparql_SpatialObject <|-- geosparql_Feature
    _090207d1 <|-- geosparql_SpatialObjectCollection
    rdfs_Container <|-- geosparql_SpatialObjectCollection
    b5c888a2 <|-- geosparql_FeatureCollection
    geosparql_SpatialObjectCollection <|-- geosparql_FeatureCollection
    bc7f215b <|-- geosparql_GeometryCollection
    geosparql_SpatialObjectCollection <|-- geosparql_GeometryCollection
    geosparql_SpatialObject <|-- geosparql_Geometry
    geosparql_SpatialObject --> geosparql_SpatialObject : geosparql:ehCovers
    geosparql_Geometry ..> geosparql_geoJSONLiteral : geosparql:asGeoJSON
    geosparql_SpatialObject --> geosparql_SpatialObject : geosparql:sfIntersects
    geosparql_Feature --> geosparql_Geometry : geosparql:hasDefaultGeometry
    geosparql_SpatialObject --> geosparql_SpatialObject : geosparql:ehOverlap
    geosparql_Geometry ..> geosparql_wktLiteral : geosparql:asWKT
    geosparql_SpatialObject --> geosparql_SpatialObject : geosparql:rcc8tppi
    geosparql_SpatialObject --> geosparql_SpatialObject : geosparql:sfDisjoint
    geosparql_SpatialObject --> geosparql_SpatialObject : geosparql:ehInside
    geosparql_Geometry ..> ca079f4f : geosparql:hasMetricSpatialAccuracy
    geosparql_SpatialObject --> geosparql_SpatialObject : geosparql:rcc8ntpp
    geosparql_SpatialObject --> geosparql_SpatialObject : geosparql:ehContains
    geosparql_SpatialObject --> geosparql_SpatialObject : geosparql:sfWithin
    geosparql_SpatialObject --> geosparql_SpatialObject : geosparql:rcc8tpp
    geosparql_SpatialObject --> geosparql_SpatialObject : geosparql:ehDisjoint
    geosparql_SpatialObject --> geosparql_SpatialObject : geosparql:ehCoveredBy
    geosparql_SpatialObject --> geosparql_SpatialObject : geosparql:sfContains
    geosparql_SpatialObject --> geosparql_SpatialObject : geosparql:rcc8ntppi
    geosparql_Geometry ..> geosparql_kmlLiteral : geosparql:asKML
    geosparql_SpatialObject --> geosparql_SpatialObject : geosparql:rcc8eq
    geosparql_SpatialObject --> geosparql_SpatialObject : geosparql:ehEquals
    geosparql_SpatialObject --> geosparql_SpatialObject : geosparql:sfTouches
    geosparql_Feature --> geosparql_Geometry : geosparql:hasCentroid
    geosparql_Feature --> geosparql_Geometry : geosparql:defaultGeometry
    geosparql_Feature --> geosparql_Geometry : geosparql:hasBoundingBox
    geosparql_SpatialObject ..> ca079f4f : geosparql:hasMetricPerimeterLength
    geosparql_Geometry ..> geosparql_gmlLiteral : geosparql:asGML
```

## Statistics

| Metric | Count |
|--------|-------|
| Classes | 6 |
| Properties | 54 |
| Inheritance relationships | 8 |
| Properties with domain | 54 |
| Properties with range | 47 |

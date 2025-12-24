# GEOSPARQL Ontology Diagram

UML-style class diagram for the **geosparql** namespace.

*Generated automatically. Classes: 6, Properties: 54*

**Legend:**
- `<|--` Inheritance (rdfs:subClassOf)
- `-->` Object Property
- `..>` Datatype Property

```mermaid
classDiagram
    class ca079f4f
    class geosparql_kmlLiteral
    class xsd_boolean
    class rdfs_Literal
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
    geosparql_Geometry ..> geosparql_geoJSONLiteral : geosparql:asGeoJSON
    geosparql_Geometry ..> rdfs_Literal : geosparql:hasSerialization
    geosparql_SpatialObject --> geosparql_SpatialObject : geosparql:rcc8tppi
    geosparql_Geometry ..> xsd_boolean : geosparql:isSimple
    geosparql_SpatialObject --> geosparql_SpatialObject : geosparql:rcc8ntpp
    geosparql_SpatialObject --> geosparql_SpatialObject : geosparql:sfContains
    geosparql_Geometry ..> geosparql_kmlLiteral : geosparql:asKML
    geosparql_SpatialObject ..> ca079f4f : geosparql:hasMetricArea
```

## Statistics

| Metric | Count |
|--------|-------|
| Classes | 6 |
| Properties | 54 |
| Inheritance relationships | 8 |
| Properties with domain | 19 |
| Properties with range | 20 |

# Semantic Lint Report

Quality assessment of ontology definitions.

*Generated automatically.*

## Summary

| Metric | Count | Percentage | Coverage |
|--------|-------|------------|----------|
| Total Classes | 1,566 | - | - |
| Classes with label | 1,360 | 86.8% | ████████░░ |
| Classes with comment | 1,345 | 85.9% | ████████░░ |
| Total Properties | 2,625 | - | - |
| Properties with label | 2,482 | 94.6% | █████████░ |
| Properties with comment | 2,459 | 93.7% | █████████░ |
| Properties with domain | 756 | 28.8% | ██░░░░░░░░ |
| Properties with range | 804 | 30.6% | ███░░░░░░░ |

## By Namespace

| Namespace | Grade | Classes | Props | Labels | Comments | Domain | Range |
|-----------|:-----:|---------|-------|--------|----------|--------|-------|
| adms | 🟢 A | 4 | 13 | 100% | 100% | 31% | 69% |
| as | 🔴 D | 159 | 69 | 35% | 33% | 100% | 100% |
| dc | 🟢 A | 0 | 15 | - | - | 0% | 0% |
| dcam | 🟢 A | 1 | 3 | 100% | 100% | 0% | 33% |
| dcat | 🟢 A | 9 | 28 | 89% | 89% | 75% | 96% |
| dcterms | 🟢 A | 22 | 55 | 100% | 100% | 5% | 24% |
| doap | 🟢 A | 14 | 43 | 93% | 93% | 88% | 67% |
| dolce | 🔴 D | 44 | 70 | 0% | 84% | 100% | 100% |
| dul | 🟡 B | 92 | 118 | 79% | 75% | 96% | 93% |
| foaf | 🟢 A | 13 | 62 | 100% | 100% | 89% | 89% |
| geo | 🟢 A | 2 | 5 | 100% | 100% | 60% | 20% |
| geosparql | 🔴 D | 6 | 54 | 0% | 0% | 100% | 87% |
| grddl | 🟢 A | 5 | 4 | 100% | 100% | 50% | 100% |
| org | 🟢 A | 13 | 35 | 69% | 69% | 100% | 86% |
| owl | 🟢 A | 26 | 49 | 100% | 100% | 100% | 100% |
| prov | 🟠 C | 38 | 65 | 79% | 53% | 75% | 74% |
| qudt | 🔴 D | 2 | 0 | 0% | 0% | - | - |
| rdf | 🟢 A | 7 | 9 | 100% | 100% | 100% | 78% |
| rdfs | 🟢 A | 6 | 9 | 100% | 100% | 100% | 100% |
| schema | 🟢 A | 930 | 1520 | 100% | 100% | 0% | 0% |
| sh | 🟢 A | 40 | 101 | 100% | 98% | 53% | 76% |
| sioc | 🟢 A | 11 | 84 | 100% | 100% | 69% | 70% |
| skos | 🟠 C | 5 | 28 | 80% | 0% | 18% | 21% |
| sosa | 🟢 A | 13 | 23 | 100% | 100% | 0% | 4% |
| ssn | 🟢 A | 6 | 15 | 100% | 100% | 0% | 0% |
| time | 🟢 A | 23 | 58 | 87% | 83% | 95% | 95% |
| vann | 🟢 A | 0 | 6 | - | - | 0% | 0% |
| vcard | 🟡 B | 75 | 84 | 83% | 43% | 1% | 33% |

### Grade Distribution

- 🟢 **A** (Excellent): 20 namespaces
- 🟡 **B** (Good): 2 namespaces
- 🟠 **C** (Fair): 2 namespaces
- 🔴 **D** (Needs work): 4 namespaces

## Issue Counts

| Severity | Category | Count |
|----------|----------|-------|
| ℹ️ info | missing-comment | 387 |
| ℹ️ info | missing-domain | 1869 |
| ℹ️ info | missing-range | 1821 |
| ⚠️ warning | missing-label | 349 |

## Warnings by Namespace

### as

- ⚠️ `1f753f63`: Class missing rdfs:label
- ⚠️ `01fb90c2`: Class missing rdfs:label
- ⚠️ `ecac7e97`: Class missing rdfs:label
- ⚠️ `cf5f04fd`: Class missing rdfs:label
- ⚠️ `b5f1f021`: Class missing rdfs:label
- ⚠️ `63538320`: Class missing rdfs:label
- ⚠️ `da2c9157`: Class missing rdfs:label
- ⚠️ `a2645612`: Class missing rdfs:label
- ⚠️ `8de931a5`: Class missing rdfs:label
- ⚠️ `d8445621`: Class missing rdfs:label
- ⚠️ `8f04c583`: Class missing rdfs:label
- ⚠️ `295da6b8`: Class missing rdfs:label
- ⚠️ `c2addc26`: Class missing rdfs:label
- ⚠️ `7fe24472`: Class missing rdfs:label
- ⚠️ `072d42ab`: Class missing rdfs:label
- ⚠️ `2d7e8396`: Class missing rdfs:label
- ⚠️ `08d12d1b`: Class missing rdfs:label
- ⚠️ `c375badc`: Class missing rdfs:label
- ⚠️ `16f99ad1`: Class missing rdfs:label
- ⚠️ `da9f5df3`: Class missing rdfs:label
- ... and 84 more warnings

### dcat

- ⚠️ `4e232b4c`: Class missing rdfs:label

### doap

- ⚠️ `00a269aa`: Class missing rdfs:label

### dolce

- ⚠️ `dolce:set`: Class missing rdfs:label
- ⚠️ `849f1493`: Class missing rdfs:label
- ⚠️ `dolce:dependent-place`: Class missing rdfs:label
- ⚠️ `dolce:spatio-temporal-region`: Class missing rdfs:label
- ⚠️ `dolce:process`: Class missing rdfs:label
- ⚠️ `dolce:temporal-quality`: Class missing rdfs:label
- ⚠️ `dolce:abstract`: Class missing rdfs:label
- ⚠️ `c89ce391`: Class missing rdfs:label
- ⚠️ `dolce:state`: Class missing rdfs:label
- ⚠️ `dolce:non-physical-object`: Class missing rdfs:label
- ⚠️ `dolce:arbitrary-sum`: Class missing rdfs:label
- ⚠️ `dolce:relevant-part`: Class missing rdfs:label
- ⚠️ `dolce:quality-space`: Class missing rdfs:label
- ⚠️ `dolce:region`: Class missing rdfs:label
- ⚠️ `dolce:quale`: Class missing rdfs:label
- ⚠️ `d6e4ceb3`: Class missing rdfs:label
- ⚠️ `dolce:physical-quality`: Class missing rdfs:label
- ⚠️ `dolce:feature`: Class missing rdfs:label
- ⚠️ `dolce:physical-object`: Class missing rdfs:label
- ⚠️ `d39682d2`: Class missing rdfs:label
- ... and 94 more warnings

### dul

- ⚠️ `2a489fda`: Class missing rdfs:label
- ⚠️ `dul:ObjectAggregate`: Class missing rdfs:label
- ⚠️ `b31df9c0`: Class missing rdfs:label
- ⚠️ `a2d449d0`: Class missing rdfs:label
- ⚠️ `4559dd29`: Class missing rdfs:label
- ⚠️ `be7d6220`: Class missing rdfs:label
- ⚠️ `dul:TimeIndexedRelation`: Class missing rdfs:label
- ⚠️ `02519bf3`: Class missing rdfs:label
- ⚠️ `79fad4cd`: Class missing rdfs:label
- ⚠️ `8b1d430f`: Class missing rdfs:label
- ⚠️ `dul:SpatioTemporalRegion`: Class missing rdfs:label
- ⚠️ `688f28a5`: Class missing rdfs:label
- ⚠️ `6c0e841c`: Class missing rdfs:label
- ⚠️ `ebc7a9e0`: Class missing rdfs:label
- ⚠️ `dul:DesignedSubstance`: Class missing rdfs:label
- ⚠️ `dul:InformationEntity`: Class missing rdfs:label
- ⚠️ `5c528107`: Class missing rdfs:label
- ⚠️ `c1388d51`: Class missing rdfs:label
- ⚠️ `bf820665`: Class missing rdfs:label
- ⚠️ `dul:realizesSelfInformation`: Property missing rdfs:label
- ... and 3 more warnings

### geosparql

- ⚠️ `geosparql:Feature`: Class missing rdfs:label
- ⚠️ `geosparql:FeatureCollection`: Class missing rdfs:label
- ⚠️ `geosparql:SpatialObject`: Class missing rdfs:label
- ⚠️ `geosparql:Geometry`: Class missing rdfs:label
- ⚠️ `geosparql:GeometryCollection`: Class missing rdfs:label
- ⚠️ `geosparql:SpatialObjectCollection`: Class missing rdfs:label
- ⚠️ `geosparql:asDGGS`: Property missing rdfs:label
- ⚠️ `geosparql:hasArea`: Property missing rdfs:label
- ⚠️ `geosparql:rcc8tpp`: Property missing rdfs:label
- ⚠️ `geosparql:hasVolume`: Property missing rdfs:label
- ⚠️ `geosparql:ehEquals`: Property missing rdfs:label
- ⚠️ `geosparql:sfOverlaps`: Property missing rdfs:label
- ⚠️ `geosparql:hasMetricSpatialAccuracy`: Property missing rdfs:label
- ⚠️ `geosparql:sfEquals`: Property missing rdfs:label
- ⚠️ `geosparql:hasDefaultGeometry`: Property missing rdfs:label
- ⚠️ `geosparql:isSimple`: Property missing rdfs:label
- ⚠️ `geosparql:coordinateDimension`: Property missing rdfs:label
- ⚠️ `geosparql:hasSpatialAccuracy`: Property missing rdfs:label
- ⚠️ `geosparql:hasBoundingBox`: Property missing rdfs:label
- ⚠️ `geosparql:asKML`: Property missing rdfs:label
- ... and 40 more warnings

### org

- ⚠️ `a3331a7e`: Class missing rdfs:label
- ⚠️ `1e931111`: Class missing rdfs:label
- ⚠️ `7874a001`: Class missing rdfs:label
- ⚠️ `2c962624`: Class missing rdfs:label

### prov

- ⚠️ `16f92030`: Class missing rdfs:label
- ⚠️ `e675e13f`: Class missing rdfs:label
- ⚠️ `8231af0e`: Class missing rdfs:label
- ⚠️ `5df0710c`: Class missing rdfs:label
- ⚠️ `54ca8a65`: Class missing rdfs:label
- ⚠️ `08e29461`: Class missing rdfs:label
- ⚠️ `2e97a557`: Class missing rdfs:label
- ⚠️ `efdc0db0`: Class missing rdfs:label
- ⚠️ `prov:dm`: Property missing rdfs:label
- ⚠️ `prov:category`: Property missing rdfs:label
- ⚠️ `prov:order`: Property missing rdfs:label
- ⚠️ `prov:qualifiedForm`: Property missing rdfs:label
- ⚠️ `prov:n`: Property missing rdfs:label
- ⚠️ `prov:editorsDefinition`: Property missing rdfs:label
- ⚠️ `prov:definition`: Property missing rdfs:label
- ⚠️ `prov:inverse`: Property missing rdfs:label
- ⚠️ `prov:component`: Property missing rdfs:label
- ⚠️ `prov:todo`: Property missing rdfs:label
- ⚠️ `prov:sharesDefinitionWith`: Property missing rdfs:label
- ⚠️ `prov:constraints`: Property missing rdfs:label
- ... and 3 more warnings

### qudt

- ⚠️ `11af25ee`: Class missing rdfs:label
- ⚠️ `c3767404`: Class missing rdfs:label

### skos

- ⚠️ `3886acbb`: Class missing rdfs:label

### time

- ⚠️ `ec3bf17f`: Class missing rdfs:label
- ⚠️ `a308e1b7`: Class missing rdfs:label
- ⚠️ `dec3c87c`: Class missing rdfs:label

### vcard

- ⚠️ `5ca151b2`: Class missing rdfs:label
- ⚠️ `27fdff12`: Class missing rdfs:label
- ⚠️ `92b55bff`: Class missing rdfs:label
- ⚠️ `9de50819`: Class missing rdfs:label
- ⚠️ `1e8f15a8`: Class missing rdfs:label
- ⚠️ `9d9c42b2`: Class missing rdfs:label
- ⚠️ `9882b74c`: Class missing rdfs:label
- ⚠️ `e6fb0d42`: Class missing rdfs:label
- ⚠️ `0fe2bd43`: Class missing rdfs:label
- ⚠️ `d1db992f`: Class missing rdfs:label
- ⚠️ `afabe2fd`: Class missing rdfs:label
- ⚠️ `bd3511ac`: Class missing rdfs:label
- ⚠️ `27a61271`: Class missing rdfs:label

## Quality Grade

**Overall Grade: A** - Excellent - well documented

- Label coverage: 91.7%
- Comment coverage: 90.8%

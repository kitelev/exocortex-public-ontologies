# Semantic Lint Report

Quality assessment of ontology definitions.

*Generated automatically.*

## Summary

| Metric | Count | Percentage | Coverage |
|--------|-------|------------|----------|
| Total Classes | 1,424 | - | - |
| Classes with label | 1,281 | 90.0% | ████████░░ |
| Classes with comment | 1,233 | 86.6% | ████████░░ |
| Total Properties | 2,422 | - | - |
| Properties with label | 2,353 | 97.2% | █████████░ |
| Properties with comment | 2,294 | 94.7% | █████████░ |
| Properties with domain | 573 | 23.7% | ██░░░░░░░░ |
| Properties with range | 624 | 25.8% | ██░░░░░░░░ |

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
| time | 🟢 A | 23 | 58 | 87% | 83% | 95% | 95% |
| vann | 🟢 A | 0 | 6 | - | - | 0% | 0% |
| vcard | 🟡 B | 75 | 84 | 83% | 43% | 1% | 33% |

### Grade Distribution

- 🟢 **A** (Excellent): 19 namespaces
- 🟡 **B** (Good): 1 namespaces
- 🟠 **C** (Fair): 2 namespaces
- 🔴 **D** (Needs work): 3 namespaces

## Issue Counts

| Severity | Category | Count |
|----------|----------|-------|
| ℹ️ info | missing-comment | 319 |
| ℹ️ info | missing-domain | 1849 |
| ℹ️ info | missing-range | 1798 |
| ⚠️ warning | missing-label | 212 |

## Warnings by Namespace

### as

- ⚠️ `c5635ab1`: Class missing rdfs:label
- ⚠️ `a9b8faef`: Class missing rdfs:label
- ⚠️ `cc257c19`: Class missing rdfs:label
- ⚠️ `dd9954bc`: Class missing rdfs:label
- ⚠️ `d906d795`: Class missing rdfs:label
- ⚠️ `1f753f63`: Class missing rdfs:label
- ⚠️ `dd501307`: Class missing rdfs:label
- ⚠️ `072d42ab`: Class missing rdfs:label
- ⚠️ `08d12d1b`: Class missing rdfs:label
- ⚠️ `295da6b8`: Class missing rdfs:label
- ⚠️ `2a2171fa`: Class missing rdfs:label
- ⚠️ `735f3363`: Class missing rdfs:label
- ⚠️ `f7f6018c`: Class missing rdfs:label
- ⚠️ `5cbfe49e`: Class missing rdfs:label
- ⚠️ `f528b339`: Class missing rdfs:label
- ⚠️ `7fe24472`: Class missing rdfs:label
- ⚠️ `fea6fe82`: Class missing rdfs:label
- ⚠️ `ecac7e97`: Class missing rdfs:label
- ⚠️ `57609c96`: Class missing rdfs:label
- ⚠️ `6d1e9fe8`: Class missing rdfs:label
- ... and 84 more warnings

### dcat

- ⚠️ `4e232b4c`: Class missing rdfs:label

### doap

- ⚠️ `00a269aa`: Class missing rdfs:label

### geosparql

- ⚠️ `geosparql:FeatureCollection`: Class missing rdfs:label
- ⚠️ `geosparql:GeometryCollection`: Class missing rdfs:label
- ⚠️ `geosparql:Geometry`: Class missing rdfs:label
- ⚠️ `geosparql:SpatialObject`: Class missing rdfs:label
- ⚠️ `geosparql:Feature`: Class missing rdfs:label
- ⚠️ `geosparql:SpatialObjectCollection`: Class missing rdfs:label
- ⚠️ `geosparql:ehOverlap`: Property missing rdfs:label
- ⚠️ `geosparql:defaultGeometry`: Property missing rdfs:label
- ⚠️ `geosparql:asDGGS`: Property missing rdfs:label
- ⚠️ `geosparql:asWKT`: Property missing rdfs:label
- ⚠️ `geosparql:hasMetricSize`: Property missing rdfs:label
- ⚠️ `geosparql:ehCoveredBy`: Property missing rdfs:label
- ⚠️ `geosparql:isSimple`: Property missing rdfs:label
- ⚠️ `geosparql:hasLength`: Property missing rdfs:label
- ⚠️ `geosparql:spatialDimension`: Property missing rdfs:label
- ⚠️ `geosparql:dimension`: Property missing rdfs:label
- ⚠️ `geosparql:coordinateDimension`: Property missing rdfs:label
- ⚠️ `geosparql:asKML`: Property missing rdfs:label
- ⚠️ `geosparql:hasMetricVolume`: Property missing rdfs:label
- ⚠️ `geosparql:hasSize`: Property missing rdfs:label
- ... and 40 more warnings

### org

- ⚠️ `2c962624`: Class missing rdfs:label
- ⚠️ `a3331a7e`: Class missing rdfs:label
- ⚠️ `7874a001`: Class missing rdfs:label
- ⚠️ `1e931111`: Class missing rdfs:label

### prov

- ⚠️ `e675e13f`: Class missing rdfs:label
- ⚠️ `8231af0e`: Class missing rdfs:label
- ⚠️ `5df0710c`: Class missing rdfs:label
- ⚠️ `54ca8a65`: Class missing rdfs:label
- ⚠️ `efdc0db0`: Class missing rdfs:label
- ⚠️ `16f92030`: Class missing rdfs:label
- ⚠️ `08e29461`: Class missing rdfs:label
- ⚠️ `2e97a557`: Class missing rdfs:label
- ⚠️ `prov:todo`: Property missing rdfs:label
- ⚠️ `prov:editorsDefinition`: Property missing rdfs:label
- ⚠️ `prov:inverse`: Property missing rdfs:label
- ⚠️ `prov:editorialNote`: Property missing rdfs:label
- ⚠️ `prov:category`: Property missing rdfs:label
- ⚠️ `prov:dm`: Property missing rdfs:label
- ⚠️ `prov:definition`: Property missing rdfs:label
- ⚠️ `prov:component`: Property missing rdfs:label
- ⚠️ `prov:qualifiedForm`: Property missing rdfs:label
- ⚠️ `prov:n`: Property missing rdfs:label
- ⚠️ `prov:aq`: Property missing rdfs:label
- ⚠️ `prov:order`: Property missing rdfs:label
- ... and 3 more warnings

### qudt

- ⚠️ `11af25ee`: Class missing rdfs:label
- ⚠️ `c3767404`: Class missing rdfs:label

### skos

- ⚠️ `3886acbb`: Class missing rdfs:label

### time

- ⚠️ `a308e1b7`: Class missing rdfs:label
- ⚠️ `ec3bf17f`: Class missing rdfs:label
- ⚠️ `dec3c87c`: Class missing rdfs:label

### vcard

- ⚠️ `9882b74c`: Class missing rdfs:label
- ⚠️ `5ca151b2`: Class missing rdfs:label
- ⚠️ `bd3511ac`: Class missing rdfs:label
- ⚠️ `9de50819`: Class missing rdfs:label
- ⚠️ `d1db992f`: Class missing rdfs:label
- ⚠️ `9d9c42b2`: Class missing rdfs:label
- ⚠️ `92b55bff`: Class missing rdfs:label
- ⚠️ `0fe2bd43`: Class missing rdfs:label
- ⚠️ `1e8f15a8`: Class missing rdfs:label
- ⚠️ `27a61271`: Class missing rdfs:label
- ⚠️ `27fdff12`: Class missing rdfs:label
- ⚠️ `afabe2fd`: Class missing rdfs:label
- ⚠️ `e6fb0d42`: Class missing rdfs:label

## Quality Grade

**Overall Grade: A** - Excellent - well documented

- Label coverage: 94.5%
- Comment coverage: 91.7%

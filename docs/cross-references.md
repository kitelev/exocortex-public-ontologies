# Ontology Cross-Reference Matrix

This matrix shows how ontologies reference each other.
Numbers indicate count of statements referencing the target namespace.

*Generated automatically.*

## Reference Matrix

Rows = source ontology, Columns = target ontology

| Source ↓ / Target → | adms | as | dc | dcam | dcat | dcterms | doap | foaf | geo | geosparql | grddl | org | owl | prov | rdf | rdfs | schema | sh | sioc | skos | sosa | time | vann | vcard | void | vs | xsd |
|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|-----|
| **adms** | - | | | | 4 | 27 | | 11 | | | | | 14 | | 47 | 81 | | | | 3 | | | 2 | | | | 4 |
| **as** | | - | | | | | | | | | | | 421 | 1 | 878 | 474 | | | | | | | | | | | 28 |
| **dc** | | | - | | | 32 | | | | | | | | | 30 | 45 | | | | 15 | | | | | | | 16 |
| **dcam** | | | | - | | 7 | | | | | | | | | 7 | 16 | | | | | | | | | | | 5 |
| **dcat** | | | | | - | 43 | | 45 | | | | | 55 | 2 | 91 | 599 | | | | 601 | | | | 1 | | | 9 |
| **dcterms** | | | 46 | 36 | | - | | 1 | | | | | 1 | | 154 | 468 | | | | | | | | | | | 99 |
| **doap** | | | 10 | | | | - | 16 | | | | | 11 | | 114 | 682 | | | 2 | | | | | | | | |
| **foaf** | | | 2 | | | 2 | | - | 3 | | | | 135 | | 228 | 391 | | | | 1 | | | | | | 75 | |
| **geo** | | | 3 | | | | | 1 | - | | | | | | 12 | 25 | | | | | | | | | | | |
| **geosparql** | | | | | | 19 | | | | - | | | 81 | | 192 | 343 | 43 | | | 237 | | | 2 | | | | 26 |
| **grddl** | | | | | | | 3 | 3 | | | - | | 4 | | 14 | 42 | | | | | | | | | | | |
| **org** | | | | | | 25 | | 33 | | | | - | 89 | 3 | 161 | 552 | | | | 6 | | | | | | | 12 |
| **owl** | | | 1 | | | | | | | | 1 | | - | | 143 | 427 | | | | | | | | | | | 6 |
| **prov** | | | | | | | | | | | | | 171 | - | 239 | 450 | | | | | | | | | | | 74 |
| **rdf** | | | 3 | | | | | | | | | | 1 | | - | 133 | | | | | | | | | | | |
| **rdfs** | | | 1 | | | | | | | | | | 1 | | 30 | - | | | | | | | | | | | |
| **schema** | | | | | 3 | 6 | | 1 | | | | | 188 | 2 | 4499 | 8090 | - | | | 51 | | | | 1 | | | |
| **sh** | | | | | | | | | | | | | 8 | | 363 | 842 | | - | | | | | | | | | 53 |
| **sioc** | | | | | | 10 | | 6 | | | | | 211 | | 116 | 464 | | | - | | | | | | | | 5 |
| **skos** | | | | | | 7 | | | | | | | 54 | | 104 | 117 | | | | - | | | | | | | |
| **sosa** | | | | | | 8 | | 4 | | | | | 55 | | 53 | 125 | | | | 66 | - | 1 | 2 | | | | 2 |
| **time** | | | | | | 10 | | | | | | | 285 | | 188 | 532 | | | | 382 | | - | | | | | 128 |
| **vann** | | | | | | 8 | | | | | | | 7 | | 7 | 24 | | | | | | | - | | | | |
| **vcard** | | | | | | | | | | | | | 301 | | 274 | 507 | | | | | | | | - | | | 73 |
| **void** | 2 | | 4 | | | 12 | | 29 | | | | | 1 | | 12 | | | | | | | | 2 | | - | | 2 |
| **vs** | | | | | | | | | | | | | | | | | | | | | | | | | | - | |
| **xsd** | | | | | | | | | | | | | | | | | | | | | | | | | | | - |

## Summary Statistics

### Most Referenced Ontologies

| Ontology | Total References |
|----------|-----------------|
| rdfs | 15429 |
| rdf | 7956 |
| owl | 2094 |
| skos | 1362 |
| xsd | 542 |
| dcterms | 216 |
| foaf | 150 |
| vs | 75 |
| dc | 70 |
| schema | 43 |

### Most Referencing Ontologies

| Ontology | References to Others |
|----------|---------------------|
| schema | 12841 |
| as | 1802 |
| time | 1525 |
| dcat | 1446 |
| sh | 1266 |
| vcard | 1155 |
| geosparql | 943 |
| prov | 934 |
| org | 881 |
| foaf | 837 |

## Dependency Relationships

Key dependencies (>100 references):

- **as** → rdf (878), rdfs (474), owl (421)
- **dcat** → skos (601), rdfs (599)
- **dcterms** → rdfs (468), rdf (154)
- **doap** → rdfs (682), rdf (114)
- **foaf** → rdfs (391), rdf (228), owl (135)
- **geosparql** → rdfs (343), skos (237), rdf (192)
- **org** → rdfs (552), rdf (161)
- **owl** → rdfs (427), rdf (143)
- **prov** → rdfs (450), rdf (239), owl (171)
- **rdf** → rdfs (133)
- **schema** → rdfs (8090), rdf (4499), owl (188)
- **sh** → rdfs (842), rdf (363)
- **sioc** → rdfs (464), owl (211), rdf (116)
- **skos** → rdfs (117), rdf (104)
- **sosa** → rdfs (125)
- **time** → rdfs (532), skos (382), owl (285), rdf (188), xsd (128)
- **vcard** → rdfs (507), owl (301), rdf (274)

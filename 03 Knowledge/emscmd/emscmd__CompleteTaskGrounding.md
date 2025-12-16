---
exo__Asset_uid: 50000000-0000-0000-0000-000000000022
exo__Asset_label: Complete Task Grounding
exo__Asset_description: SPARQL UPDATE для завершения задачи
exo__Asset_isDefinedBy: "[[!emscmd]]"
exo__Asset_createdAt: 2025-01-01T00:00:00
exo__Instance_class:
  - "[[exocmd__Grounding]]"
exocmd__Grounding_sparqlUpdate: |
  PREFIX ems: <https://exocortex.my/ontology/ems#>
  PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

  DELETE {
    ?effort ems:Effort_status ems:EffortStatus_Doing .
  }
  INSERT {
    ?effort ems:Effort_status ems:EffortStatus_Done .
    ?effort ems:Effort_endTimestamp ?now .
  }
  WHERE {
    ?targetAsset ems:Task_currentEffort ?effort .
    ?effort ems:Effort_status ems:EffortStatus_Doing .
    BIND(NOW() AS ?now)
  }
exocmd__Grounding_affectedProperties:
  - "[[ems__Effort_status]]"
  - "[[ems__Effort_endTimestamp]]"
---

# Complete Task Grounding

Меняет статус на Done и устанавливает время завершения.

```sparql
DELETE { ?effort ems:Effort_status ems:EffortStatus_Doing }
INSERT {
  ?effort ems:Effort_status ems:EffortStatus_Done .
  ?effort ems:Effort_endTimestamp NOW() .
}
WHERE { ... }
```

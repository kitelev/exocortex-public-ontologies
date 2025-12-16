---
exo__Asset_uid: 50000000-0000-0000-0000-000000000013
exo__Asset_label: Stop Task Grounding
exo__Asset_description: SPARQL UPDATE для остановки задачи
exo__Asset_isDefinedBy: "[[!emscmd]]"
exo__Asset_createdAt: 2025-01-01T00:00:00
exo__Instance_class:
  - "[[exocmd__Grounding]]"
exocmd__Grounding_sparqlUpdate: |
  PREFIX ems: <https://exocortex.my/ontology/ems#>

  DELETE {
    ?effort ems:Effort_status ems:EffortStatus_Doing .
  }
  INSERT {
    ?effort ems:Effort_status ems:EffortStatus_Queued .
  }
  WHERE {
    ?targetAsset ems:Task_currentEffort ?effort .
    ?effort ems:Effort_status ems:EffortStatus_Doing .
  }
exocmd__Grounding_affectedProperties:
  - "[[ems__Effort_status]]"
---

# Stop Task Grounding

Меняет статус текущего Effort с Doing на Queued.

```sparql
DELETE { ?effort ems:Effort_status ems:EffortStatus_Doing }
INSERT { ?effort ems:Effort_status ems:EffortStatus_Queued }
WHERE { ... }
```

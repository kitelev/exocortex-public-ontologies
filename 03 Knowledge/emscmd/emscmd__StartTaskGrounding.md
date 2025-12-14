---
exo__Asset_uid: 60000000-0000-0000-0000-000000000020
exo__Asset_label: Start Task Grounding
exo__Asset_description: SPARQL UPDATE для выполнения команды Start Task
exo__Asset_isDefinedBy: "[[!emscmd]]"
exo__Asset_createdAt: 2025-01-01T00:00:00
exo__Instance_class:
  - "[[exocmd__SparqlGrounding]]"
exo__Grounding_sparql: |
  PREFIX ems: <https://exocortex.my/ontology/ems#>
  PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
  DELETE { $target ems:Effort_status ?oldStatus }
  INSERT {
    $target ems:Effort_status ems:EffortStatusDoing .
    $target ems:Effort_startTimestamp $now .
  }
  WHERE {
    OPTIONAL { $target ems:Effort_status ?oldStatus }
  }
---

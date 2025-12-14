---
exo__Asset_uid: 60000000-0000-0000-0000-000000000002
exo__Asset_label: Task Not Doing
exo__Asset_description: Условие — задача не в статусе Doing. Переиспользуется для команд Start, Resume
exo__Asset_isDefinedBy: "[[!emscmd]]"
exo__Asset_createdAt: 2025-01-01T00:00:00
exo__Instance_class:
  - "[[exocmd__Precondition]]"
exo__Precondition_sparql: |
  PREFIX ems: <https://exocortex.my/ontology/ems#>
  ASK {
    $target a ems:Task .
    OPTIONAL { $target ems:Effort_status ?s }
    FILTER(!BOUND(?s) || ?s != ems:EffortStatusDoing)
  }
---

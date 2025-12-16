---
exo__Asset_uid: 50000000-0000-0000-0000-000000000012
exo__Asset_label: Task Doing Precondition
exo__Asset_description: Проверяет, что задача находится в статусе Doing
exo__Asset_isDefinedBy: "[[!emscmd]]"
exo__Asset_createdAt: 2025-01-01T00:00:00
exo__Instance_class:
  - "[[exocmd__Precondition]]"
exocmd__Precondition_sparqlAsk: |
  PREFIX ems: <https://exocortex.my/ontology/ems#>
  ASK {
    ?targetAsset ems:Task_currentEffort ?effort .
    ?effort ems:Effort_status ems:EffortStatus_Doing .
  }
exocmd__Precondition_expectedResult: true
---

# Task Doing Precondition

Команда доступна, если ASK возвращает **true** — задача в статусе Doing.

```sparql
ASK {
  ?targetAsset ems:Task_currentEffort ?effort .
  ?effort ems:Effort_status ems:EffortStatus_Doing .
}
```

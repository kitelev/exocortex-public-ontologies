---
exo__Asset_uid: 10000000-0000-0000-0000-000000000036
exo__Asset_label: Kanban Lanes
exo__Asset_description: Явный упорядоченный список колонок канбана
exo__Asset_isDefinedBy: "[[!exo]]"
exo__Asset_createdAt: 2025-01-01T00:00:00
exo__Instance_class:
  - "[[exo__ObjectProperty]]"
exo__Property_domain: "[[exo__KanbanLayout]]"
exo__Property_range: "[[rdfs__Resource]]"
---

# Kanban Lanes

Явный список колонок канбана в нужном порядке. Если не указан, колонки создаются автоматически из всех значений `laneProperty`.

## Пример

```yaml
exo__KanbanLayout_lanes:
  - "[[ems__EffortStatus_Queued]]"
  - "[[ems__EffortStatus_Doing]]"
  - "[[ems__EffortStatus_Done]]"
```

Колонки будут в указанном порядке: Queued → Doing → Done.

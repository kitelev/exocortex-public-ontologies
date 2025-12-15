---
exo__Asset_uid: 10000000-0000-0000-0000-000000000031
exo__Asset_label: Kanban Layout
exo__Asset_description: Канбан-доска с колонками по статусам или другому свойству
exo__Asset_isDefinedBy: "[[!exo]]"
exo__Asset_createdAt: 2025-01-01T00:00:00
exo__Instance_class:
  - "[[exo__Class]]"
exo__Class_subClassOf:
  - "[[exo__Layout]]"
---

# Kanban Layout

Канбан-доска — визуализация задач по статусам или этапам. Карточки можно перетаскивать между колонками.

## Специфичные свойства

- `KanbanLayout_laneProperty` — свойство для группировки по колонкам (например, статус)
- `KanbanLayout_lanes` — явный список колонок канбана

## Пример

```yaml
exo__Instance_class:
  - "[[exo__KanbanLayout]]"
exo__Layout_targetClass: "[[ems__Task]]"
exo__KanbanLayout_laneProperty: "[[ems__Effort_status]]"
exo__KanbanLayout_lanes:
  - "[[ems__EffortStatus_Queued]]"
  - "[[ems__EffortStatus_Doing]]"
  - "[[ems__EffortStatus_Done]]"
```

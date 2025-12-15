---
exo__Asset_uid: 10000000-0000-0000-0000-000000000035
exo__Asset_label: Lane Property
exo__Asset_description: Свойство, по которому распределяются карточки по колонкам канбана
exo__Asset_isDefinedBy: "[[!exo]]"
exo__Asset_createdAt: 2025-01-01T00:00:00
exo__Instance_class:
  - "[[exo__ObjectProperty]]"
exo__Property_domain: "[[exo__KanbanLayout]]"
exo__Property_range: "[[exo__Property]]"
---

# Kanban Lane Property

Свойство, значения которого определяют колонки канбан-доски. Обычно это статус или этап.

## Пример

```yaml
exo__KanbanLayout_laneProperty: "[[ems__Effort_status]]"
```

Задачи будут распределены по колонкам Queued, Doing, Done.

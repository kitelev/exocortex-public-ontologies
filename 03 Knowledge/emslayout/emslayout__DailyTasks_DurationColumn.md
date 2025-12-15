---
exo__Asset_uid: 60000000-0000-0000-0000-000000000013
exo__Asset_label: Duration Column
exo__Asset_description: Колонка с длительностью работы над задачей
exo__Asset_isDefinedBy: "[[!emslayout]]"
exo__Asset_createdAt: 2025-01-01T00:00:00
exo__Instance_class:
  - "[[exo__LayoutColumn]]"
exo__LayoutColumn_property: "[[ems__Effort_duration]]"
exo__LayoutColumn_header: Время
exo__LayoutColumn_width: 70px
exo__LayoutColumn_renderer: duration
exo__LayoutColumn_editable: false
exo__LayoutColumn_sortable: true
---

# Duration Column

Вычисляемая длительность: `endTimestamp - startTimestamp` или `NOW() - startTimestamp` для активных задач.

Формат: `1h 23m` или `45m`.

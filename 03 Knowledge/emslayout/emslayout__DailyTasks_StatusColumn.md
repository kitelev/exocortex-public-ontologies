---
exo__Asset_uid: 60000000-0000-0000-0000-000000000011
exo__Asset_label: Status Column
exo__Asset_description: Колонка со статусом текущего Effort задачи
exo__Asset_isDefinedBy: "[[!emslayout]]"
exo__Asset_createdAt: 2025-01-01T00:00:00
exo__Instance_class:
  - "[[exo__LayoutColumn]]"
exo__LayoutColumn_property: "[[ems__Effort_status]]"
exo__LayoutColumn_header: Статус
exo__LayoutColumn_width: 100px
exo__LayoutColumn_renderer: badge
exo__LayoutColumn_editable: true
exo__LayoutColumn_sortable: true
---

# Status Column

Статус задачи отображается как цветной бейдж:
- 🟡 Queued — в очереди
- 🔵 Doing — в работе
- 🟢 Done — завершено

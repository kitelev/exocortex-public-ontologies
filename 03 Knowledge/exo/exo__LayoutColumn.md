---
exo__Asset_uid: 10000000-0000-0000-0000-000000000040
exo__Asset_label: Layout Column
exo__Asset_description: Колонка таблицы — определяет какое свойство отображать и как
exo__Asset_isDefinedBy: "[[!exo]]"
exo__Asset_createdAt: 2025-01-01T00:00:00
exo__Instance_class:
  - "[[exo__Class]]"
exo__Class_subClassOf:
  - "[[exo__Asset]]"
---

# Layout Column

Колонка определяет, какое свойство ассета отображать в таблице и как его форматировать.

## Свойства колонки

- `LayoutColumn_property` — какое свойство отображать
- `LayoutColumn_header` — заголовок колонки (если отличается от label свойства)
- `LayoutColumn_width` — ширина колонки (px, %, auto)
- `LayoutColumn_renderer` — специальный рендерер (link, badge, progress, etc.)
- `LayoutColumn_editable` — можно ли редактировать inline
- `LayoutColumn_sortable` — можно ли сортировать по этой колонке

## Пример

```yaml
exo__Asset_label: Status Column
exo__Instance_class:
  - "[[exo__LayoutColumn]]"
exo__LayoutColumn_property: "[[ems__Effort_status]]"
exo__LayoutColumn_header: Статус
exo__LayoutColumn_width: 100px
exo__LayoutColumn_renderer: badge
exo__LayoutColumn_editable: true
exo__LayoutColumn_sortable: true
```

---
exo__Asset_uid: 10000000-0000-0000-0000-000000000060
exo__Asset_label: Layout Sort
exo__Asset_description: Правило сортировки данных в Layout
exo__Asset_isDefinedBy: "[[!exo]]"
exo__Asset_createdAt: 2025-01-01T00:00:00
exo__Instance_class:
  - "[[exo__Class]]"
exo__Class_subClassOf:
  - "[[exo__Asset]]"
---

# Layout Sort

Определяет порядок сортировки ассетов в Layout.

## Свойства

- `LayoutSort_property` — по какому свойству сортировать
- `LayoutSort_direction` — направление (asc, desc)
- `LayoutSort_nullsPosition` — куда помещать пустые значения (first, last)

## Пример

```yaml
exo__Asset_label: Sort by Start Time
exo__Instance_class:
  - "[[exo__LayoutSort]]"
exo__LayoutSort_property: "[[ems__Effort_startTimestamp]]"
exo__LayoutSort_direction: desc
exo__LayoutSort_nullsPosition: last
```

---
exo__Asset_uid: 10000000-0000-0000-0000-000000000050
exo__Asset_label: Layout Filter
exo__Asset_description: Фильтр для отбора данных в Layout
exo__Asset_isDefinedBy: "[[!exo]]"
exo__Asset_createdAt: 2025-01-01T00:00:00
exo__Instance_class:
  - "[[exo__Class]]"
exo__Class_subClassOf:
  - "[[exo__Asset]]"
---

# Layout Filter

Фильтр определяет условия отбора ассетов для отображения в Layout.

## Свойства фильтра

- `LayoutFilter_property` — по какому свойству фильтровать
- `LayoutFilter_operator` — оператор сравнения (eq, ne, gt, lt, contains, etc.)
- `LayoutFilter_value` — значение для сравнения
- `LayoutFilter_sparql` — SPARQL WHERE clause для сложных фильтров

## Примеры

### Простой фильтр
```yaml
exo__Asset_label: Active Tasks Filter
exo__Instance_class:
  - "[[exo__LayoutFilter]]"
exo__LayoutFilter_property: "[[ems__Effort_status]]"
exo__LayoutFilter_operator: ne
exo__LayoutFilter_value: "[[ems__EffortStatus_Done]]"
```

### SPARQL фильтр
```yaml
exo__Asset_label: Today Tasks Filter
exo__Instance_class:
  - "[[exo__LayoutFilter]]"
exo__LayoutFilter_sparql: |
  ?task ems:Task_currentEffort ?effort .
  ?effort ems:Effort_startTimestamp ?start .
  FILTER(?start >= NOW() - "P1D"^^xsd:duration)
```

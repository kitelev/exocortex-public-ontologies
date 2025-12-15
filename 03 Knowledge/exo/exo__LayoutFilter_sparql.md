---
exo__Asset_uid: 10000000-0000-0000-0000-000000000054
exo__Asset_label: Filter SPARQL
exo__Asset_description: SPARQL WHERE clause для сложных условий фильтрации
exo__Asset_isDefinedBy: "[[!exo]]"
exo__Asset_createdAt: 2025-01-01T00:00:00
exo__Instance_class:
  - "[[exo__DatatypeProperty]]"
exo__Property_domain: "[[exo__LayoutFilter]]"
exo__Property_range: "[[xsd__string]]"
---

# Filter SPARQL

SPARQL WHERE clause для сложных условий, которые нельзя выразить простым оператором.

Переменная `?asset` связана с текущим ассетом.

## Пример

```yaml
exo__LayoutFilter_sparql: |
  ?asset ems:Task_currentEffort ?effort .
  ?effort ems:Effort_startTimestamp ?start .
  FILTER(?start >= NOW() - "P1D"^^xsd:duration)
```

Этот фильтр отберёт задачи, начатые за последние сутки.

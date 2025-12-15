---
exo__Asset_uid: 10000000-0000-0000-0000-000000000023
exo__Asset_label: Filters
exo__Asset_description: Список фильтров, применяемых к данным Layout
exo__Asset_isDefinedBy: "[[!exo]]"
exo__Asset_createdAt: 2025-01-01T00:00:00
exo__Instance_class:
  - "[[exo__ObjectProperty]]"
exo__Property_domain: "[[exo__Layout]]"
exo__Property_range: "[[exo__LayoutFilter]]"
---

# Layout Filters

Список предопределённых фильтров для Layout.

## Пример

```yaml
exo__Layout_filters:
  - "[[TasksTable_ActiveFilter]]"
  - "[[TasksTable_TodayFilter]]"
```

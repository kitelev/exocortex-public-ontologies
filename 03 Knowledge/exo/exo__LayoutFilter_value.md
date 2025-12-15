---
exo__Asset_uid: 10000000-0000-0000-0000-000000000053
exo__Asset_label: Filter Value
exo__Asset_description: Значение для сравнения в фильтре
exo__Asset_isDefinedBy: "[[!exo]]"
exo__Asset_createdAt: 2025-01-01T00:00:00
exo__Instance_class:
  - "[[exo__DatatypeProperty]]"
exo__Property_domain: "[[exo__LayoutFilter]]"
exo__Property_range: "[[rdfs__Resource]]"
---

# Filter Value

Эталонное значение для сравнения. Может быть:
- Ссылкой на ассет: `"[[ems__EffortStatus_Done]]"`
- Литералом: `"urgent"`, `5`, `true`
- Специальным значением: `NOW()`, `TODAY()`

## Примеры

```yaml
# Ссылка на ассет
exo__LayoutFilter_value: "[[ems__EffortStatus_Done]]"

# Строковое значение
exo__LayoutFilter_value: "urgent"

# Числовое значение
exo__LayoutFilter_value: 5
```

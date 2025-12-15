---
exo__Asset_uid: 10000000-0000-0000-0000-000000000063
exo__Asset_label: Sort Nulls Position
exo__Asset_description: Куда помещать ассеты с пустым значением сортируемого свойства
exo__Asset_isDefinedBy: "[[!exo]]"
exo__Asset_createdAt: 2025-01-01T00:00:00
exo__Instance_class:
  - "[[exo__DatatypeProperty]]"
exo__Property_domain: "[[exo__LayoutSort]]"
exo__Property_range: "[[xsd__string]]"
---

# Sort Nulls Position

Определяет, где в отсортированном списке будут ассеты, у которых сортируемое свойство не задано:
- `first` — в начале списка
- `last` — в конце списка

## Пример

```yaml
exo__LayoutSort_nullsPosition: last
```

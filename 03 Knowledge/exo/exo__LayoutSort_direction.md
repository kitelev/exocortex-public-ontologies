---
exo__Asset_uid: 10000000-0000-0000-0000-000000000062
exo__Asset_label: Sort Direction
exo__Asset_description: Направление сортировки (по возрастанию или убыванию)
exo__Asset_isDefinedBy: "[[!exo]]"
exo__Asset_createdAt: 2025-01-01T00:00:00
exo__Instance_class:
  - "[[exo__DatatypeProperty]]"
exo__Property_domain: "[[exo__LayoutSort]]"
exo__Property_range: "[[xsd__string]]"
---

# Sort Direction

Направление сортировки:
- `asc` — по возрастанию (A→Z, 1→9, старые→новые)
- `desc` — по убыванию (Z→A, 9→1, новые→старые)

## Пример

```yaml
exo__LayoutSort_direction: desc
```

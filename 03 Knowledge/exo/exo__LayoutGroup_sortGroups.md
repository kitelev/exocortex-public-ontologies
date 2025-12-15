---
exo__Asset_uid: 10000000-0000-0000-0000-000000000074
exo__Asset_label: Sort Groups
exo__Asset_description: Порядок сортировки групп между собой
exo__Asset_isDefinedBy: "[[!exo]]"
exo__Asset_createdAt: 2025-01-01T00:00:00
exo__Instance_class:
  - "[[exo__DatatypeProperty]]"
exo__Property_domain: "[[exo__LayoutGroup]]"
exo__Property_range: "[[xsd__string]]"
---

# Sort Groups

Определяет порядок отображения групп:
- `asc` — по алфавиту (A→Z)
- `desc` — в обратном порядке (Z→A)
- `count` — по количеству элементов (много→мало)
- `custom` — в порядке, заданном отдельно

## Пример

```yaml
exo__LayoutGroup_sortGroups: count
```

Группы с большим количеством элементов будут показаны первыми.

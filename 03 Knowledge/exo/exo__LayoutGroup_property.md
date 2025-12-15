---
exo__Asset_uid: 10000000-0000-0000-0000-000000000071
exo__Asset_label: Group Property
exo__Asset_description: Свойство, по которому группируются ассеты
exo__Asset_isDefinedBy: "[[!exo]]"
exo__Asset_createdAt: 2025-01-01T00:00:00
exo__Instance_class:
  - "[[exo__ObjectProperty]]"
exo__Property_domain: "[[exo__LayoutGroup]]"
exo__Property_range: "[[exo__Property]]"
---

# Group Property

Свойство, значения которого определяют группы. Ассеты с одинаковым значением попадают в одну группу.

## Пример

```yaml
exo__LayoutGroup_property: "[[ems__Task_project]]"
```

Задачи будут сгруппированы по проектам.

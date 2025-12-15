---
exo__Asset_uid: 10000000-0000-0000-0000-000000000070
exo__Asset_label: Layout Group
exo__Asset_description: Правило группировки данных в Layout
exo__Asset_isDefinedBy: "[[!exo]]"
exo__Asset_createdAt: 2025-01-01T00:00:00
exo__Instance_class:
  - "[[exo__Class]]"
exo__Class_subClassOf:
  - "[[exo__Asset]]"
---

# Layout Group

Определяет, как группировать ассеты в Layout. Группировка создаёт визуальные секции с заголовками.

## Свойства

- `LayoutGroup_property` — по какому свойству группировать
- `LayoutGroup_collapsed` — свёрнуты ли группы по умолчанию
- `LayoutGroup_showCount` — показывать ли количество элементов в группе
- `LayoutGroup_sortGroups` — сортировка групп (asc, desc, custom)

## Пример

```yaml
exo__Asset_label: Group by Project
exo__Instance_class:
  - "[[exo__LayoutGroup]]"
exo__LayoutGroup_property: "[[ems__Task_project]]"
exo__LayoutGroup_collapsed: false
exo__LayoutGroup_showCount: true
exo__LayoutGroup_sortGroups: asc
```

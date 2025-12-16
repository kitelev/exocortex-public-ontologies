---
exo__Asset_uid: 10000000-0000-0000-0000-000000000084
exo__Asset_label: Layout Actions
exo__Asset_description: Набор действий (кнопок команд) для данного Layout
exo__Asset_isDefinedBy: "[[!exo]]"
exo__Asset_createdAt: 2025-01-01T00:00:00
exo__Instance_class:
  - "[[exo__ObjectProperty]]"
exo__Property_domain: "[[exo__Layout]]"
exo__Property_range: "[[exo__LayoutActions]]"
---

# Layout Actions

Связывает Layout с набором действий (кнопок команд), доступных для каждого элемента.

## Пример

```yaml
exo__Instance_class:
  - "[[exo__TableLayout]]"
exo__Layout_targetClass: "[[ems__Task]]"
exo__Layout_columns:
  - "[[emslayout__DailyTasks_LabelColumn]]"
  - "[[emslayout__DailyTasks_StatusColumn]]"
exo__Layout_actions: "[[emslayout__TaskActions]]"
```

Таблица будет содержать колонку с кнопками действий из `TaskActions`.

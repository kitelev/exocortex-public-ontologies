---
exo__Asset_uid: 10000000-0000-0000-0000-000000000030
exo__Asset_label: Table Layout
exo__Asset_description: Табличное представление данных с колонками, сортировкой и фильтрацией
exo__Asset_isDefinedBy: "[[!exo]]"
exo__Asset_createdAt: 2025-01-01T00:00:00
exo__Instance_class:
  - "[[exo__Class]]"
exo__Class_subClassOf:
  - "[[exo__Layout]]"
---

# Table Layout

Табличное представление — наиболее универсальный тип Layout. Отображает данные в виде таблицы с настраиваемыми колонками.

## Возможности

- Настраиваемые колонки (`Layout_columns`)
- Сортировка по любой колонке
- Фильтрация по значениям
- Группировка строк
- Inline-редактирование

## Пример

```yaml
exo__Instance_class:
  - "[[exo__TableLayout]]"
exo__Layout_targetClass: "[[ems__Task]]"
exo__Layout_columns:
  - "[[DailyTasks_LabelColumn]]"
  - "[[DailyTasks_StatusColumn]]"
  - "[[DailyTasks_DurationColumn]]"
exo__Layout_defaultSort: "[[DailyTasks_SortByStart]]"
exo__Layout_filters:
  - "[[DailyTasks_TodayFilter]]"
```

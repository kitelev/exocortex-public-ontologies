---
exo__Asset_uid: 60000000-0000-0000-0000-000000000001
exo__Asset_label: Daily Tasks Layout
exo__Asset_description: Таблица задач за текущий день с колонками статуса, времени и длительности
exo__Asset_isDefinedBy: "[[!emslayout]]"
exo__Asset_createdAt: 2025-01-01T00:00:00
exo__Instance_class:
  - "[[exo__TableLayout]]"
exo__Layout_targetClass: "[[ems__Task]]"
exo__Layout_columns:
  - "[[emslayout__DailyTasks_LabelColumn]]"
  - "[[emslayout__DailyTasks_StatusColumn]]"
  - "[[emslayout__DailyTasks_StartTimeColumn]]"
  - "[[emslayout__DailyTasks_DurationColumn]]"
exo__Layout_defaultSort: "[[emslayout__DailyTasks_SortByStart]]"
exo__Layout_filters:
  - "[[emslayout__DailyTasks_TodayFilter]]"
exo__Layout_actions: "[[emslayout__TaskActions]]"
---

# Daily Tasks Layout

Таблица задач за день — основное представление для ежедневной работы.

## Колонки

| Колонка | Свойство | Рендерер |
|---------|----------|----------|
| Задача | `Asset_label` | link |
| Статус | `Effort_status` | badge |
| Начало | `Effort_startTimestamp` | datetime |
| Длительность | (вычисляемое) | duration |

## Фильтры

- Только задачи с Effort за сегодня
- Исключены архивные задачи

## Сортировка

По времени начала (desc) — последние начатые сверху.

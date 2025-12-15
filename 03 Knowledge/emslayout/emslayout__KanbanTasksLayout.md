---
exo__Asset_uid: 60000000-0000-0000-0000-000000000002
exo__Asset_label: Kanban Tasks Layout
exo__Asset_description: Канбан-доска задач с колонками по статусам
exo__Asset_isDefinedBy: "[[!emslayout]]"
exo__Asset_createdAt: 2025-01-01T00:00:00
exo__Instance_class:
  - "[[exo__KanbanLayout]]"
exo__Layout_targetClass: "[[ems__Task]]"
exo__KanbanLayout_laneProperty: "[[ems__Effort_status]]"
exo__KanbanLayout_lanes:
  - "[[ems__EffortStatus_Queued]]"
  - "[[ems__EffortStatus_Doing]]"
  - "[[ems__EffortStatus_Done]]"
---

# Kanban Tasks Layout

Канбан-доска для визуального управления задачами. Карточки задач распределены по колонкам статусов.

## Колонки (Lanes)

| Статус | Описание |
|--------|----------|
| Queued | Задачи в очереди на выполнение |
| Doing | Задачи в работе (активные) |
| Done | Завершённые задачи |

## Взаимодействие

- Drag & Drop — перетаскивание карточки меняет статус
- Click — открывает задачу
- Quick actions — кнопки Start/Stop/Complete на карточке

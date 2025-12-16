---
exo__Asset_uid: 60000000-0000-0000-0000-000000000040
exo__Asset_label: Task Actions
exo__Asset_description: Кнопки управления задачей — Начать, Остановить, Завершить
exo__Asset_isDefinedBy: "[[!emslayout]]"
exo__Asset_createdAt: 2025-01-01T00:00:00
exo__Instance_class:
  - "[[exo__LayoutActions]]"
exo__LayoutActions_commands:
  - "[[emscmd__StartTaskCommand]]"
  - "[[emscmd__StopTaskCommand]]"
  - "[[emscmd__CompleteTaskCommand]]"
exo__LayoutActions_position: column
exo__LayoutActions_showLabels: false
---

# Task Actions

Стандартный набор кнопок для управления задачами в таблице.

## Кнопки

| Команда | Иконка | Видима когда |
|---------|--------|--------------|
| StartTaskCommand | ▶️ | Задача НЕ в статусе Doing |
| StopTaskCommand | ⏹️ | Задача в статусе Doing |
| CompleteTaskCommand | ✅ | Задача в статусе Doing |

## Поведение

- Кнопки отображаются в отдельной колонке справа
- Только иконки (компактный вид)
- Видимость определяется precondition каждой команды
- Клик выполняет SPARQL UPDATE команды

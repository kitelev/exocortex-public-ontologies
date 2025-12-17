---
type: cmd:Command
cmd:Command_name: completeTask
cmd:Command_label: Завершить задачу
cmd:Command_description: Установить время завершения задачи
cmd:Command_category: action
cmd:Command_targetType: "[[ems__Task]]"
cmd:Command_preconditions:
  - "[[cmd__TaskNotCompleted]]"
---

# CompleteTask Command

Команда завершения задачи.

## Input

Команда не требует ввода — работает с текущей заметкой.

## Preconditions

1. Текущая заметка имеет `type: ems:Task`
2. Задача ещё не завершена (`ems:Effort_endTimestamp` отсутствует)

## Outcome

- Если задача не начата — установить `startTimestamp` = `endTimestamp`
- Установлен `ems:Effort_endTimestamp` = текущее время
- Показано уведомление "Задача завершена"

## Пример

```yaml
# До
type: ems:Task
core:Asset_label: "Написать тесты"
ems:Effort_startTimestamp: "2025-01-15T10:00:00Z"

# После completeTask
type: ems:Task
core:Asset_label: "Написать тесты"
ems:Effort_startTimestamp: "2025-01-15T10:00:00Z"
ems:Effort_endTimestamp: "2025-01-15T11:30:00Z"
```

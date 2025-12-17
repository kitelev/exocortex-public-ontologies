---
type: cmd:Command
cmd:Command_name: startTask
cmd:Command_label: Начать задачу
cmd:Command_description: Установить время начала выполнения задачи
cmd:Command_category: action
cmd:Command_targetType: "[[ems__Task]]"
cmd:Command_preconditions:
  - "[[cmd__TaskNotStarted]]"
---

# StartTask Command

Команда начала выполнения задачи.

## Input

Команда не требует ввода — работает с текущей заметкой.

## Preconditions

1. Текущая заметка имеет `type: ems:Task`
2. Задача ещё не начата (`ems:Effort_startTimestamp` отсутствует)

## Outcome

- Установлен `ems:Effort_startTimestamp` = текущее время
- Показано уведомление "Задача начата"

## Пример

```yaml
# До
type: ems:Task
core:Asset_label: "Написать тесты"

# После startTask
type: ems:Task
core:Asset_label: "Написать тесты"
ems:Effort_startTimestamp: "2025-01-15T10:00:00Z"
```

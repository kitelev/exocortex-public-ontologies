---
type: owl:Ontology
label: Commands Ontology
uri: https://exocortex.my/ontology/application/commands#
prefix: cmd
version: 1.0.0
imports:
  - application
---

# Commands Ontology

Определение команд (Use Cases) системы Exocortex.

## Концепт Command

Command — это декларативное описание действия пользователя:
- **Что делает** (intent)
- **Какие данные нужны** (form)
- **Какие условия** (preconditions)
- **Какой результат** (outcome)

## Категории команд

### Create
Создание новых сущностей:
- [[cmd__CreateTask]]
- [[cmd__CreateProject]]
- [[cmd__CreateArea]]

### Edit
Редактирование существующих:
- [[cmd__EditTask]]
- [[cmd__EditProject]]
- [[cmd__EditArea]]

### Action
Действия над сущностями:
- [[cmd__StartTask]]
- [[cmd__CompleteTask]]
- [[cmd__ArchiveProject]]

### Navigate
Навигация и поиск:
- [[cmd__Search]]
- [[cmd__GoToTask]]
- [[cmd__ListTasks]]

## Принципы

1. **Single Responsibility** — одна команда = одно действие
2. **Declarative** — описание, не реализация
3. **Testable** — можно валидировать без UI

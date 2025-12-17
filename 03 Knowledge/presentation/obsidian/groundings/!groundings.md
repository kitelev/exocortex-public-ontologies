---
type: owl:Ontology
label: Obsidian Groundings
uri: https://exocortex.my/ontology/presentation/obsidian/groundings#
prefix: grnd
version: 1.0.0
imports:
  - presentation/obsidian
  - application/commands
---

# Obsidian Groundings

Привязка абстрактных команд к Obsidian API.

## Концепт Grounding

Grounding — это "заземление" абстрактной команды в конкретной платформе:
- Как команда регистрируется
- Какой UI показывается
- Как взаимодействовать с платформой

## Структура

```
Command (abstract)
    ↓ grounded by
Grounding (platform-specific)
    ↓ uses
Obsidian API
```

## Стандартные groundings

- [[grnd__CreateTaskGrounding]] — создание задачи
- [[grnd__StartTaskGrounding]] — начало задачи
- [[grnd__CompleteTaskGrounding]] — завершение задачи
- [[grnd__SearchGrounding]] — поиск

## Связь с Command

```yaml
type: grnd:Grounding
grnd:Grounding_command: "[[cmd__CreateTask]]"
grnd:Grounding_hotkey: "Cmd+Shift+N"
grnd:Grounding_modalClass: "CreateTaskModal"
```

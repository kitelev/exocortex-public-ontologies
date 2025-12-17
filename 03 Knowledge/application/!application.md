---
type: owl:Ontology
label: Application Layer Ontology
uri: https://exocortex.my/ontology/application#
prefix: app
version: 1.0.0
imports:
  - core
  - meta
---

# Application Layer Ontology

Слой приложения — определение команд, форм и процессов, независимых от платформы.

## Принцип Clean Architecture

Application Layer находится между Domain и Presentation:

```
Presentation (Obsidian, CLI, Web)
        ↓ uses
Application (Commands, Forms, Processes)
        ↓ orchestrates
Domain (EMS, Knowledge)
        ↓ extends
Core (Asset, Reference)
```

## Подмодули

### commands/
Определения команд (Use Cases):
- [[app__Command]] — базовый класс команды
- Конкретные команды (CreateTask, EditProject, etc.)

### forms/
Определения форм ввода:
- [[app__Form]] — базовый класс формы
- [[app__FormField]] — поле формы

### processes/
Бизнес-процессы:
- [[app__Process]] — последовательность шагов

## Принципы

1. **Platform-agnostic** — команды не знают о UI
2. **Domain-driven** — оперируют доменными сущностями
3. **Declarative** — описывают "что", не "как"

## Зависимости

```
application (этот модуль)
  └── domain/* (EMS, Knowledge)
      └── core (Asset)
```

Application НЕ зависит от:
- presentation (UI, layouts)

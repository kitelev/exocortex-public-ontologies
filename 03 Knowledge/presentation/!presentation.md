---
type: owl:Ontology
label: Presentation Layer Ontology
uri: https://exocortex.my/ontology/presentation#
prefix: pres
version: 1.0.0
imports:
  - application
---

# Presentation Layer Ontology

Слой представления — платформо-специфичные реализации UI.

## Принцип Clean Architecture

Presentation — внешний слой, зависящий от Application:

```
Presentation (этот слой)
        ↓ implements
Application (Commands, Forms)
        ↓ uses
Domain (EMS, Knowledge)
        ↓ extends
Core (Asset)
```

## Платформы

### obsidian/
Реализация для Obsidian:
- `layouts/` — визуальные шаблоны для заметок
- `groundings/` — привязка команд к Obsidian API
- `ui/` — UI-компоненты (модалки, нотификации)

### cli/ (будущее)
Реализация для CLI.

### web/ (будущее)
Реализация для веб-интерфейса.

## Принципы

1. **Platform-specific** — знает о конкретной платформе
2. **Thin layer** — минимум логики, делегирует Application
3. **Replaceable** — можно заменить без изменения логики

## Зависимости

```
presentation/obsidian
  └── application (Commands, Forms)
      └── domain/* (EMS)
          └── core
```

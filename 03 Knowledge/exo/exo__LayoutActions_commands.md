---
exo__Asset_uid: 10000000-0000-0000-0000-000000000081
exo__Asset_label: Actions Commands
exo__Asset_description: Список команд, отображаемых как кнопки действий
exo__Asset_isDefinedBy: "[[!exo]]"
exo__Asset_createdAt: 2025-01-01T00:00:00
exo__Instance_class:
  - "[[exo__ObjectProperty]]"
exo__Property_domain: "[[exo__LayoutActions]]"
exo__Property_range: "[[exocmd__Command]]"
---

# Actions Commands

Упорядоченный список команд, которые отображаются как кнопки. Порядок в списке определяет порядок кнопок слева направо.

## Пример

```yaml
exo__LayoutActions_commands:
  - "[[emscmd__StartTaskCommand]]"    # ▶️ Начать
  - "[[emscmd__StopTaskCommand]]"     # ⏹️ Остановить
  - "[[emscmd__CompleteTaskCommand]]" # ✅ Завершить
```

## Связь с Command

Каждая команда содержит:
- `Command_icon` — иконка кнопки
- `Asset_label` — текст кнопки (если showLabels=true)
- `Process_precondition` — условие видимости/активности
- `Grounding_sparqlUpdate` — действие при клике

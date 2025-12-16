---
exo__Asset_uid: 10000000-0000-0000-0000-000000000083
exo__Asset_label: Show Action Labels
exo__Asset_description: Показывать ли текстовые подписи к кнопкам действий
exo__Asset_isDefinedBy: "[[!exo]]"
exo__Asset_createdAt: 2025-01-01T00:00:00
exo__Instance_class:
  - "[[exo__DatatypeProperty]]"
exo__Property_domain: "[[exo__LayoutActions]]"
exo__Property_range: "[[xsd__boolean]]"
---

# Show Action Labels

Если `true`, кнопки отображаются с текстом: `[▶️ Начать]`
Если `false`, только иконки: `[▶️]`

По умолчанию: `false` (компактный вид)

## Пример

```yaml
exo__LayoutActions_showLabels: true
```

Результат: `[▶️ Начать] [⏹️ Остановить] [✅ Завершить]`

---
exo__Asset_uid: 10000000-0000-0000-0000-000000000082
exo__Asset_label: Actions Position
exo__Asset_description: Позиция отображения кнопок действий
exo__Asset_isDefinedBy: "[[!exo]]"
exo__Asset_createdAt: 2025-01-01T00:00:00
exo__Instance_class:
  - "[[exo__DatatypeProperty]]"
exo__Property_domain: "[[exo__LayoutActions]]"
exo__Property_range: "[[xsd__string]]"
---

# Actions Position

Определяет, где отображаются кнопки действий:

| Значение | Описание |
|----------|----------|
| `column` | Отдельная колонка справа (по умолчанию) |
| `inline` | Рядом с названием ассета |
| `hover` | Появляются при наведении на строку |
| `contextMenu` | В контекстном меню (правый клик) |

## Пример

```yaml
exo__LayoutActions_position: hover
```

Кнопки появятся только при наведении мыши на строку.

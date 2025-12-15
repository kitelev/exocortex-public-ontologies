---
exo__Asset_uid: 10000000-0000-0000-0000-000000000034
exo__Asset_label: List Layout
exo__Asset_description: Простой список ассетов с минимальным оформлением
exo__Asset_isDefinedBy: "[[!exo]]"
exo__Asset_createdAt: 2025-01-01T00:00:00
exo__Instance_class:
  - "[[exo__Class]]"
exo__Class_subClassOf:
  - "[[exo__Layout]]"
---

# List Layout

Простой список — минималистичное представление. Показывает ассеты как список с одной строкой на элемент.

## Специфичные свойства

- `ListLayout_template` — шаблон строки (какие свойства показывать)
- `ListLayout_showIcon` — показывать ли иконку класса

## Пример

```yaml
exo__Instance_class:
  - "[[exo__ListLayout]]"
exo__Layout_targetClass: "[[ems__Task]]"
exo__ListLayout_template: "{{label}} — {{status}}"
exo__ListLayout_showIcon: true
```

---
exo__Asset_uid: 10000000-0000-0000-0000-000000000043
exo__Asset_label: Column Width
exo__Asset_description: Ширина колонки (px, %, auto)
exo__Asset_isDefinedBy: "[[!exo]]"
exo__Asset_createdAt: 2025-01-01T00:00:00
exo__Instance_class:
  - "[[exo__DatatypeProperty]]"
exo__Property_domain: "[[exo__LayoutColumn]]"
exo__Property_range: "[[xsd__string]]"
---

# Column Width

Ширина колонки. Поддерживаемые форматы:
- `100px` — фиксированная ширина в пикселях
- `20%` — процент от ширины таблицы
- `auto` — автоматическая ширина по содержимому
- `1fr` — доля свободного пространства (CSS Grid)

## Пример

```yaml
exo__LayoutColumn_width: 150px
```

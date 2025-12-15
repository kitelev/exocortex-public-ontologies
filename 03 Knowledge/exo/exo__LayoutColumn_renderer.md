---
exo__Asset_uid: 10000000-0000-0000-0000-000000000044
exo__Asset_label: Column Renderer
exo__Asset_description: Тип рендерера для отображения значения колонки
exo__Asset_isDefinedBy: "[[!exo]]"
exo__Asset_createdAt: 2025-01-01T00:00:00
exo__Instance_class:
  - "[[exo__DatatypeProperty]]"
exo__Property_domain: "[[exo__LayoutColumn]]"
exo__Property_range: "[[xsd__string]]"
---

# Column Renderer

Определяет, как визуально отображать значение колонки.

## Встроенные рендереры

| Renderer | Описание |
|----------|----------|
| `text` | Простой текст (по умолчанию) |
| `link` | Кликабельная ссылка на ассет |
| `badge` | Цветной бейдж (для статусов) |
| `progress` | Прогресс-бар (для числовых значений 0-100) |
| `date` | Форматированная дата |
| `datetime` | Дата и время |
| `duration` | Длительность (часы:минуты) |
| `boolean` | Чекбокс |
| `rating` | Звёздочки (для оценок) |
| `tags` | Список тегов |

## Пример

```yaml
exo__LayoutColumn_renderer: badge
```

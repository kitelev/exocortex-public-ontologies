---
exo__Asset_uid: 10000000-0000-0000-0000-000000000033
exo__Asset_label: Calendar Layout
exo__Asset_description: Календарное представление с событиями на временной шкале
exo__Asset_isDefinedBy: "[[!exo]]"
exo__Asset_createdAt: 2025-01-01T00:00:00
exo__Instance_class:
  - "[[exo__Class]]"
exo__Class_subClassOf:
  - "[[exo__Layout]]"
---

# Calendar Layout

Календарь отображает ассеты на временной шкале. Подходит для задач, событий, дедлайнов.

## Специфичные свойства

- `CalendarLayout_startProperty` — свойство с датой начала
- `CalendarLayout_endProperty` — свойство с датой окончания
- `CalendarLayout_view` — вид по умолчанию (day, week, month)

## Пример

```yaml
exo__Instance_class:
  - "[[exo__CalendarLayout]]"
exo__Layout_targetClass: "[[ems__Effort]]"
exo__CalendarLayout_startProperty: "[[ems__Effort_startTimestamp]]"
exo__CalendarLayout_endProperty: "[[ems__Effort_endTimestamp]]"
exo__CalendarLayout_view: week
```
